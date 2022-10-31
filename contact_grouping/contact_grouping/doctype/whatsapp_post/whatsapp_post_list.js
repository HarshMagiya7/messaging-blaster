frappe.listview_settings['Social Media Post'] = {
//	add_fields: ["status", "post_status"],
//	get_indicator: function(doc) {
//		return [__(doc.post_status), {
//			"Scheduled": "orange",
//			"Posted": "green",
//			"Error": "red",
//			"Deleted": "red"
//		}[doc.post_status]];
//	}
//}
//	refresh: function(frm) {
//              frm.add_custom_button(__('Get User Email Address'), function(){
//              frappe.msgprint(frm.doc.email);
 //     }, __("Utilities"));

//frappe.listview_settings[‘Invoice’] = {
	onload: function(listview) {
		listview.page.add_menu_item(__("Set as Open"), function() {
			listview.call_for_selected_items(method, {"status": "Open"});
		});

		listview.page.add_menu_item(__("Set as Closed"), function() {
			listview.call_for_selected_items(method, {"status": "Closed"});
		});

 // does not work
        listview.page.add_custom_button(__('Hello'), function() {
            frappe.msgprint("Hello World");
        })
	}
}
