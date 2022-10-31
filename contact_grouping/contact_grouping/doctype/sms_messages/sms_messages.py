# Copyright (c) 2022, Devershi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SMSMessages(Document):
	def on_update(self):
		sent = len(frappe.db.get_values("SMS Messages",{'campaign':self.campaign,'sms_status':'SENT'}, 'name', as_dict=1))
		delivered = len(frappe.db.get_values("SMS Messages",{'campaign':self.campaign,'sms_status':'DELIVERED'}, 'name', as_dict=1))
		pending = len(frappe.db.get_values("SMS Messages",{'campaign':self.campaign,'sms_status':'BUFFERED'}, 'name', as_dict=1))
		all = len(frappe.db.get_values("SMS Messages",{'campaign':self.campaign}, 'name', as_dict=1))


		doc = frappe.get_doc('SMS Post',self.campaign)
		doc.sms_sent = sent
		doc.sms_delivered = delivered
		doc.sms_pending = pending
		doc.sms_not_delivered = all - sent - pending - delivered
		doc.total_sms = all
		doc.save()
#		frappe.msgprint(('Success'))
