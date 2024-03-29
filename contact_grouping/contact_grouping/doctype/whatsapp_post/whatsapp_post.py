
# Copyright (c) 2022, Devershi and contributors
# For license information, please see license.txt

import frappe
import requests
import json
from datetime import datetime
#from frappe.model.document import Document

#class WhatsappPost(Document):
#	pass
from frappe.model.document import Document

class WhatsappPost(Document):
	def validate(self):
		if self.scheduled_time:
			current_time = frappe.utils.now_datetime()
			scheduled_time = frappe.utils.get_datetime(self.scheduled_time)
			if scheduled_time < current_time:
				frappe.throw(("Scheduled Time must be future time."))
#		frappe.db.set_value(post_status = 'Scheduled'
#		frappe.db.commit()
		self.template_status()
	def template_status(self):
		temp = frappe.get_doc('Whatsapp Template',self.message_template)
		if temp.temp_status == 'Approved':
			pass
		else:
			frappe.throw(('Whatsapp Template status not Approved yet, update the status or try again later'))

	def after_insert(self):
#		frappe.db.set_value("Whatsapp Post",self.name,"post_status",'Scheduled')
#		frappe.db.commit()
#		self.append('campaign_status',{'title':self.name,'sent_status':'0','pending_status':'0','read_status':'0','failed_status':'0'})
		self.post_status = 'Scheduled'
		self.save()

	@frappe.whitelist()
	def message_post(self):

		print(self.message_template)
		# MessageBird Access Token
		messagebird_doc = frappe.get_single('Messagebird Setting')
		messagebird_token = messagebird_doc.get_password('access_token')
		# Whatsapp Sender Access Token
		whatsapp_token = frappe.get_value('Whatsapp Setting',self.msg_sender,'whatsapp_access_token')
		# Whatsapp Message Template
		message = self.message_template
		# Recipents
		contact_table = frappe.get_doc('Contact Group',self.msg_to)
		print('loop')
		for entry in contact_table.contact:
			print('loop0')
			number = frappe.get_value('Customer',((frappe.get_doc('Contact Group Member',entry.get('contacts'))).contact),'mobile_no')
			print(number)
			response = self.post(messagebird_token,whatsapp_token,message,number)
			response = json.loads(response)

			#Creating message

#			doc = frappe.new_doc('Message')
#			doc.message_text = message
#			doc.message_id = response['id']
#			doc.contact_id = frappe.get_doc('Sync contact',frappe.get_doc('Contact Group Member',entry.get('contacts')).contact).customer_id
#			doc.insert()


#			time = re.search(r'\d{2}:\d{2}:\d{2}', response['updatedDatetime']).group()
#			date = re.search(r'\d{4}-\d{2}-\d{2}', response['updatedDatetime']).group()
#
#			date_time = datetime.strptime(f'{date} {time}', '%Y-%m-%d %H:%M:%S')
#			date_time_format = date_time.strftime("%d-%m-%Y %H:%M:%S")
			#Linking Message to Contact

			doc = frappe.get_doc('Sync contact',frappe.get_doc('Contact Group Member',entry.get('contacts')).contact)
			doc.append("message",{"status_update_time":frappe.utils.now_datetime(),"status":response["status"].upper(),"campaign":self.name,"sent_time":frappe.utils.now_datetime(),"message_text": message,"message_id":response['id'],"contact_id":frappe.get_doc('Sync contact',frappe.get_doc('Contact Group Member',entry.get('contacts')).contact).customer_id})
			doc.save()

		frappe.db.set_value("Whatsapp Post",self.name,"post_status",'Posted')
		frappe.db.commit()
	def post(self,messagebird_token,whatsapp_token,message,number):
		print('defi')
		url = "https://conversations.messagebird.com/v1/send"
		payload = json.dumps({
 			"to": number,
 			"from": whatsapp_token,
 			"type": "hsm",
 			"content": {
				"hsm": {
					"namespace": "5ba2d0b7_f2c6_433b_a66e_57b009ceb6ff",
					"templateName": message,
					"language": {
					"policy": "deterministic",
					"code": "en"
					}
				}
			}
		})

		headers = {
			'Authorization': f'AccessKey {messagebird_token}',
			'Content-Type': 'application/json'
			}

		response = requests.request("POST", url, headers=headers, data=payload)
		print(response.text)
		return response.text
#			print(number)

#		print(messagebird_token)
#		print(whatsapp_token)
#		print(message)

#	def after_insert(self):
#		self.append('campaign_status',{'title':self.name,'sent_status':'0','pending_status':'0','read_status':'0','failed_status':'0'})
#		self.save()

#	@frappe.whitelist()
#	def update_status(self):
#		sent = frappe.db.get_values("Whatsapp Messages",{'campaign':self.name,'status':'SENT'}, 'name', as_dict=1)
#		print(f'\n\nCamp list{sent}')
#		doc = frappe.get_doc('Whatsapp Status',self.name)
#		print('f\n\n Doctype{doc.name}')
#		doc.sent_status = len(sent)
#		doc.save()

def process_scheduled_whatsapp_message():
	posts = frappe.get_list(
		"Whatsapp Post",
		filters={"post_status": "Scheduled", "docstatus": 1},
		fields=["name", "scheduled_time"],
	)
	start = frappe.utils.now_datetime()
	end = start + datetime.timedelta(minutes=10)
	for post in posts:
		if post.scheduled_time:
			post_time = frappe.utils.get_datetime(post.scheduled_time)
			if post_time > start and post_time <= end:
				whatsapp_post = frappe.get_doc("Whatsapp Post", post.name)
				whatsapp_post.message_post()
