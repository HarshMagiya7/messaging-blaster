# Copyright (c) 2022, Devershi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json
import requests
class Synccontact(Document):

	@frappe.whitelist()
	def sync_all_contact(self):

		contacts_to_upload = []
		all_contacts_list = self.get_all_contacts()
		synced_contacts_list = self.get_synced_contact_list()

		for i in range(len(all_contacts_list)):
			if all_contacts_list[i] not in synced_contacts_list:
				contacts_to_upload.append(all_contacts_list[i])
		print('ALL')
		print(all_contacts_list)
		print('Sync')
		print(synced_contacts_list)
		print('remaining')
		print(contacts_to_upload)
		self.upload_contacts(contacts_to_upload)

	def get_all_contacts(self):

		contact_dict = frappe.get_list('Customer')
		contact_list = self.dict_to_list(contact_dict)

		return contact_list

	def get_synced_contact_list(self):

		sync_contact_dict = frappe.get_list('Sync contact')
		sync_contact_list = self.dict_to_list(sync_contact_dict)

		return sync_contact_list

	def dict_to_list(self,contact_dict):

		contact_list = []
		for i in range(len(contact_dict)):
			contact_list.append(contact_dict[i]['name'])

		return contact_list

	def upload_contacts(self,contact_list):

		for i in range(len(contact_list)):
			try:
				contact = frappe.get_doc('Customer',contact_list[i])
				token_doc = frappe.get_doc('Messagebird Setting')
				token = token_doc.get_password('access_token')
				id_data = self.upload_to_messagebird(contact.mobile_no,contact.customer_name,token)
				number_id = json.loads(id_data)['id']
				new = frappe.new_doc('Sync contact')
				print(new)
				new.customer = contact_list[i]
				new.customer_id = number_id
				print(number_id)
				new.insert()
				print('end')
				frappe.db.commit()
			except:
				pass

	def upload_to_messagebird(self,mobile_no,customer_name,token):

		url = "https://rest.messagebird.com/contacts"

		payload=f'msisdn={mobile_no}&firstName={customer_name}'
		headers = {
		  'Authorization': f'AccessKey {token}',
		  'Content-Type': 'application/x-www-form-urlencoded'
		}

		response = requests.request("POST", url, headers=headers, data=payload)
		print(response.text)
		#print(headers)
		return response.text
