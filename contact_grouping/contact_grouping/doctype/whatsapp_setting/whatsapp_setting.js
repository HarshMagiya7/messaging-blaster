// Copyright (c) 2022, Devershi and contributors
// For license information, please see license.txt

frappe.ui.form.on('Whatsapp Setting', {
	refresh: function(frm) {
		frm.add_custom_button(__('Post'), function() {
                                frappe.call({
                                        doc: frm.doc,
                                        method: 'demo',
                                        freeze: true,
                                        callback: function() {
                                                frm.reload_doc();
	                               }
		});
	 })}
});
