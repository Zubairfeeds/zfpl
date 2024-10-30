// Copyright (c) 2024, Atom Global and contributors
// For license information, please see license.txt


frappe.ui.form.on('Overtime Entry', {
    refresh: function (frm) {
        if (frm.doc.docstatus == 0 && !frm.is_new()) {
            frm.add_custom_button(__('Get Employees'), function () {
                get_employees(frm);
            }).toggleClass("btn-primary", !(frm.doc.employees || []).length);
        }
    }
});

function get_employees(frm) {
    var department = frm.doc.department;
    var branch = frm.doc.branch;
    var designation = frm.doc.designation;
    console.log('Msg ')

    frappe.call({
        method: 'zfpl.zfpl.doctype.overtime_entry.overtime_entry.get_employees',
        args: {
            doctype: frm.doctype,
            docname: frm.docname,
            department: department,
            branch: branch,
            designation: designation
        },
        callback: function (r) {
            if (r.message) {
                frm.clear_table("employees");

                $.each(r.message, function (i, employee) {
                    // if (department && employee.department != department) {
                    // 	frappe.throw('Employee department does not match selected department. Get Employees first.');
                    // }

                    var row = frm.add_child("employees");
                    row.employee = employee.name;
                    row.employee_name = employee.employee_name;
                });

                frm.refresh_field("employees");
            }
        }
    });
}
