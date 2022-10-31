// Copyright (c) 2022, Devershi and contributors
// For license information, please see license.txt

function updateContact(frm) {
    if (!frm.doc.group_name) return;
    let exist = [];
    if (!frm.is_new()) {
        $.each(frm.doc.contact, function(i, r) { exist.push(r.contacts); });
    }
frappe.db.get_list('Contact Group Member', {
        fields: ['name'],
        filters: {name: ['like', frm.doc.group_name + '%']}
    }).then(records => {
        $.each(records, function(i, r) {
            if (exist.indexOf(r.name) < 0) {
                exist.push(r.name);
                frm.add_child('contact', {contacts: r.name});
            }
        });
        exist.splice(0, exist.length);
    });
}
frappe.ui.form.on('Contact Group', {
refresh: function(frm) {
   frm.add_custom_button('Update Contacts', () => { updateContact(frm); });
},
customer: function(frm) { updateContact(frm); }
});
