# Copyright (c) 2022, Devershi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WhatsappSetting(Document):
	def trwy(self):
		print('something')
	@frappe.whitelist()
	def demo(self):
		doc = frappe.new_doc('Whatsapp Setting')
		doc.title = 'Demohg'
		doc.insert()
