frappe.listview_settings['Whatsapp Template'] = {

    onload: function (listview) {

        // Add a button for doing something useful.
        listview.page.add_inner_button(__("Button"), function () {
			frappe.call({
                                doc: frm.doc,
                                method: 'contact_grouping.whatsapp_template.whatsapp_template.print_msg',
                                freeze: true,
                                callback: function() {
                                        frm.reload_doc();
                                }
                        });  // change to your function's name
        })
//        .addClass("btn-warning").css({'color':'darkred','font-weight': 'normal'});
        // The .addClass above is optional.  It just adds styles to the button.
    }
};
