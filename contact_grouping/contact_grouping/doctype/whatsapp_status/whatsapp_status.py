# Copyright (c) 2022, Devershi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class WhatsappStatus(Document):
	@frappe.whitelist()
	def update_status(self):
		sent = len(frappe.db.get_values("Whatsapp Messages",{'campaign':self.name,'status':'SENT'}, 'name', as_dict=1))
		read = len(frappe.db.get_values("Whatsapp Messages",{'campaign':self.name,'status':'READ'}, 'name', as_dict=1))
		failed = len(frappe.db.get_values("Whatsapp Messages",{'campaign':self.name,'status':'FAILED'}, 'name', as_dict=1))
		rejected = len(frappe.db.get_values("Whatsapp Messages",{'campaign':self.name,'status':'REJECTED'}, 'name', as_dict=1))
		all = len(frappe.db.get_values("Whatsapp Messages",{'campaign':self.name}, 'name', as_dict=1))
		accepted = len(frappe.db.get_values("Whatsapp Messages",{'campaign':self.name,'status':'ACCEPTED'}, 'name', as_dict=1))
		transmitted = len(frappe.db.get_values("Whatsapp Messages",{'campaign':self.name,'status':'TRANSMITTED'}, 'name', as_dict=1))
		pending = len(frappe.db.get_values("Whatsapp Messages",{'campaign':self.name,'status':'PENDING'}, 'name', as_dict=1))

		doc = frappe.get_doc('Whatsapp Status',self.name)
		doc.sent_status = sent
		doc.read_status = read
		doc.failed_status = failed + rejected
		doc.pending_status = pending
		doc.total_status = all
		doc.save()
