# Copyright (c) 2022, Devershi and contributors
# For license information, please see license.txt

# import frappe

from frappe.model.document import Document
import frappe
import requests
import json
import re
from datetime import datetime
class SMSPost(Document):
	def validate(self):
		if self.scheduled_time:
			current_time = frappe.utils.now_datetime()
			scheduled_time = frappe.utils.get_datetime(self.scheduled_time)
			if scheduled_time < current_time:
				frappe.throw(("Scheduled Time must be future time."))
		self.post_status = 'Scheduled'
		self.validate_placeholder()
	@frappe.whitelist()
	def message_post(self):

		# MessageBird Access Token
		messagebird_doc = frappe.get_single('Messagebird Setting')
		messagebird_token = messagebird_doc.get_password('access_token')

		# Recipents
		contact_table = frappe.get_doc('Contact Group',self.msg_to)
		for entry in contact_table.contact:
			number = frappe.get_value('Customer',((frappe.get_doc('Contact Group Member',entry.get('contacts'))).contact),'mobile_no')
			customer_doc = frappe.get_doc('Customer',((frappe.get_doc('Contact Group Member',entry.get('contacts'))).contact))
			personalized_text = self.placeholder(self.sms_text,customer_doc)
			response = self.post(messagebird_token,personalized_text,number)
			response = json.loads(response)
			item = response['recipients']['items'][0]

#			time = re.search(r'\d{2}:\d{2}:\d{2}', item['statusDatetime']).group()
#			date = re.search(r'\d{4}-\d{2}-\d{2}', item['statusDatetime']).group()

#			date_time = datetime.strptime(f'{date} {time}', '%Y-%m-%d %H:%M:%S')
#			date_time_format = date_time.strftime("%d-%m-%Y %H:%M:%S")

			# Creating SMS Message Doc
			doc = frappe.get_doc('Sync contact',frappe.get_doc('Contact Group Member',entry.get('contacts')).contact)
			doc.append("sms_message",{"campaign":self.name,"sms_sent_time":frappe.utils.now_datetime(),"sms_body":personalized_text,"sms_id":response['id'],"sms_status":item['status'],"sms_status_update_time":frappe.utils.now_datetime()})
			doc.save()

		frappe.db.set_value("SMS Post",self.name,"post_status",'Posted')
		frappe.db.commit()
	def post(self,token,text,number):
		url = "https://rest.messagebird.com/messages"
		headers = {
			'Authorization': f'AccessKey {token}',
			'Content-Type': 'application/json'
			}
		payload=json.dumps({"recipients":number,"originator":"919665065389","body":text,"reference":"11353278"})
		print(f'\n\n{payload}\n\n')
		response = requests.request("POST", url, headers=headers, data=payload)
		print(response.text)
		return response.text

	def placeholder(self,text,doc):
		place_holder = re.findall('{\w+}', text)
#		print(place_holder)
#		print(0)
		if not place_holder:
			return text
#		print(1)
		values = []
		for var in place_holder:
#			print(var)
			var = var.replace('{','')
#			print(var)
			var = var.replace('}','')
#			print(var)
			values.append(doc.get(var))
#			print(values)
		for i in range(len(place_holder)):
			text = text.replace(place_holder[i],values[i])
		return text
	def validate_placeholder(self):
		place_holder = re.findall('{\w+}', self.sms_text)
		if not place_holder:
			return
		doc = frappe.get_last_doc('Customer').name
		for var in place_holder:
			var = var.replace('{','')
			var = var.replace('}','')
			try:
				value = frappe.get_value('Customer',doc,var)
			except:
				frappe.throw((f'Customer doc has no attribute "{var}"'))
#				print('error')
	def update_status(self):
		sent = len(frappe.db.get_values("SMS Messages",{'campaign':self.name,'sms_status':'SENT'}, 'name', as_dict=1))
		delivered = len(frappe.db.get_values("SMS Messages",{'campaign':self.name,'sms_status':'DELIVERED'}, 'name', as_dict=1))
		pending = len(frappe.db.get_values("SMS Messages",{'campaign':self.name,'sms_status':'BUFFERED'}, 'name', as_dict=1))
		all = len(frappe.db.get_values("SMS Messages",{'campaign':self.name}, 'name', as_dict=1))

		print(f'sent:{sent}   delivered{delivered}    pending{pending}   all{all}')
#		doc = frappe.get_doc('SMS Post',self.name)
		self.sms_sent = sent
		self.sms_delivered = delivered
		self.sms_pending = pending
		self.sms_not_delivered = int(all) - int(sent) - int(delivered) - int(pending)
		self.total_sms = all
		print(self.total_sms)
		frappe.db.commit()
		print(self.total_sms)
