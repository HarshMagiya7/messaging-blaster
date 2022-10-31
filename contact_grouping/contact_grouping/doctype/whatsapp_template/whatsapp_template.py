# Copyright (c) 2022, Devershi and ributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
import json

class WhatsappTemplate(Document):

#	def validate(self):
	#	try:
	#		amit
	#	except:
	#		frappe.throw((f'Error'))

	def validate(self):
	#	frappe.throw((f'Error'))
		global status
		status = ''
		status = self.get_status()
		if status:
			pass
		else:
		#	print(status)

		#except:
			frappe.throw((f'Error'))

	def get_status(self):

		access_token_doc = frappe.get_doc('Messagebird Setting')
		access_token = access_token_doc.get_password('access_token')

		try:
			print('loop')
			if self.button:
				response = self.create_template_buttons(self.message,self.button_1,self.button_2,access_token,self.temp_name)
			else:
				response = self.create_template(self.message,access_token,self.temp_name)
			print(response)
			response = json.loads(response)
			status = response['status'].capitalize()
			return status
		except:
			pass

	def create_template_buttons(self,body,first_button,second_button,access,name):
		url = "https://integrations.messagebird.com/v2/platforms/whatsapp/templates"

		payload = json.dumps({
		"language": "en",
		"components": [
			{
				"type": "BODY",
				"text": body
			},
			{
				"type": "BUTTONS",
				"buttons": [
					{
						"type": "QUICK_REPLY",
						"text": first_button
					},
					{
						"type": "QUICK_REPLY",
						"text": second_button
					}
				]
			}
			],
			"name": name,
			"category": "TRANSACTIONAL"
		})
		headers = {
			'Authorization': f'AccessKey {access}',
			'Content-Type': 'application/json'
		}

		response = requests.request("POST", url, headers=headers, data=payload)

		return response.text



	def create_template(self,body,access,name):
		url = "https://integrations.messagebird.com/v2/platforms/whatsapp/templates"

		payload = json.dumps({
		"language": "en",
		"components": [
			{
				"type": "BODY",
				"text": body
			}
			],
			"name": name,
			"category": "TRANSACTIONAL"
		})
		headers = {
			'Authorization': f'AccessKey {access}',
			'Content-Type': 'application/json'
		}

		response = requests.request("POST", url, headers=headers, data=payload)

		return response.text

	def after_insert(self):

		frappe.db.set_value('Whatsapp Template', self.name ,'temp_status', status)
		frappe.db.commit()

	@frappe.whitelist()
	def update_status(self):

		access_token_doc = frappe.get_doc('Messagebird Setting')
		access_token = access_token_doc.get_password('access_token')

		url = f"https://integrations.messagebird.com/v2/platforms/whatsapp/templates/{self.name}"

		payload={}
		headers = {
			'Authorization': f'AccessKey {access_token}',
			'Content-Type': 'application/json'
		}

		response = requests.request("GET", url, headers=headers, data=payload)
		status =  json.loads(response.text)[0]['status']
		self.db_set("temp_status", status.capitalize())
		frappe.db.commit()

	@frappe.whitelist()
	def delete_temp(self):
		access_token_doc = frappe.get_doc('Messagebird Setting')
		access_token = access_token_doc.get_password('access_token')

		url = f"https://integrations.messagebird.com/v2/platforms/whatsapp/templates/{self.name}"

		payload={}
		headers = {
			'Authorization': f'AccessKey {access_token}',
			'Content-Type': 'application/json'
		}
		print(headers)
		response = requests.request("DELETE", url, headers=headers, data=payload)

		if response.text:
			frappe.throw((response.text))
		else:
			frappe.msgprint(('Deleted'))
			self.db_set("temp_status", 'Deleted')
			frappe.db.commit()

	@frappe.whitelist()
	def print_msg(self):
		frappe.msgprint(('Success'))
