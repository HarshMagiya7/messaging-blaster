// Copyright (c) 2022, Devershi and contributors
// For license information, please see license.txt

frappe.ui.form.on('Whatsapp Post', {

	refresh: function(frm) {
//		if (frm.doc.docstatus === 1) {
			if (['Scheduled'].includes(frm.doc.post_status)) {
				frm.trigger('add_post_button');
		//	}
		}
},
	add_post_button : function(frm) {
			frm.add_custom_button(__('Post Now'), function() {
        	                frappe.call({
                	                doc: frm.doc,
                        	        method: 'message_post',
                                	freeze: true,
                                	callback: function() {
                                        	frm.reload_doc();
                               }

                        });
                }); 


 }
});


//		if (frm.doc.docstatus === 1) {
//			if (!['Posted', 'Deleted'].includes(frm.doc.post_status)) {
//				frm.trigger('add_post_btn');
//			}
