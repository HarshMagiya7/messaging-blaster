// Copyright (c) 2022, Devershi and contributors
// For license information, please see license.txt


frappe.ui.form.on('Contact Filter', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            let btn = __('Apply Filter');
            frm.add_custom_button(btn, function() { frm.trigger('add_filtered_contacts'); });
            frm.change_custom_button_type(btn, null, 'success');
        }
    },
    add_filtered_contacts: function(frm) {
        var doc = frm.doc,
        contact_group = doc.contact_group,
        contacts = [];
        
        let address_filters = {},
        session_filters = {},
        promises = [];
        
        if (doc.country) address_filters.country = doc.country;
        if (doc.city) address_filters.city = doc.city;
        if (doc.intent) session_filters.intent = doc.intent;
        if (doc.package) session_filters.package = doc.package;
        if (doc.start_date && doc.end_date) {
            session_filters.datetime = [
                'between',
                [doc.start_date + ' 00:00:00', doc.end_date + ' 00:00:00']
            ];
        } else if (doc.start_date) {
            session_filters.datetime = ['>=', doc.start_date + ' 00:00:00'];
        } else if (doc.end_date) {
            session_filters.datetime = ['<=', doc.end_date + ' 00:00:00'];
        }
        
        if (Object.keys(address_filters).length) {
            promises.push(frappe.db.get_list('Address', {
                fields: ['name'],
                filters: address_filters
            }));
        }
        if (Object.keys(session_filters).length) {
            promises.push(frappe.db.get_list('Session History Collection', {
                fields: ['customer'],
                filters: session_filters
            }));
        }
        if (!promises.length) return;
        (promises.length > 1 ? Promise.all(promises) : promises[0])
        .then(vals => {
            if (promises.length === 1) vals = [vals];
            var addresses = [];
            $.each(vals, function(i, data) {
                $.each(data, function(i, v) {
                    if (v.name) {
                        if (addresses.indexOf(v.name) < 0) addresses.push(v.name);
                    } else if (v.customer) {
                        if (contacts.indexOf(v.customer) < 0) contacts.push(v.customer);
                    }
                });
            });
            function process() {
                if (!contacts.length) return;
                frappe.db.get_list('Contact Group Member', {
                    fields: ['contact'],
                    filters: {
                        contact: ['in', contacts],
                        'contact_group': contact_group
                    }
                }).then(data => {
                    if (data.length) {
                        $.each(data, function(i, v) {
                            if (v.contact) {
                                let idx = contacts.indexOf(v.contact);
                                if (idx >= 0) contacts.splice(idx, 1);
                            }
                        });
                    }
                    if (!contacts.length) return;
                    
                    frappe.db.get_list('Sync contact', {
                        fields: ['customer'],
                        filters: {
                            customer: ['in', contacts]
                        }
                    }).then(verified => {
                        if (!verified.length) return false;
                        contacts = [];
                        $.each(verified, function(i, v) {
                            contacts.push(v.customer);
                        });
                        
                        var chunks = [];
                        if (contacts.length > 200) {
                            for (var n = 0, len = contacts.length; n < len; n += 200) {
                                chunks.push(contacts.slice(n, n + 200));
                            }
                        } else {
                            chunks.push(contacts);
                        }
                        for (var i = 0, l = chunks.length; i < l; i++) {
                            var docsList = [];
                            for (var x = 0, m = chunks[i].length; x < m; x++) {
                                docsList.push({
                                    doctype: 'Contact Group Member',
                                    contact_group: contact_group,
                                    contact: chunks[i].shift(),
                                });
                            }
                            frappe.call({
                                method: 'frappe.client.insert_many',
                                type: 'POST',
                                args: {docs: docsList.slice()}
                            });
                        }
                    });
                });
            }
            if (addresses.length) {
                frappe.db.get_list('Dynamic Link', {
                    fields: ['link_name'],
                    filters: {
                        parent: ['in', addresses],
                        parenttype: 'Address',
                        parentfield: 'links'
                    }
                }).then(function(ret) {
                    $.each(ret, function(i, v) {
                        if (v.link_name && contacts.indexOf(v.link_name) < 0) contacts.push(v.link_name);
                    });
                    process();
                });
            } else {
                process();
            }
        });
    }
});
