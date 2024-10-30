// Copyright (c) 2024, Atom Global and contributors
// For license information, please see license.txt

frappe.ui.form.on('Overtime', {
	employee: function (frm) {
		fetchAttendanceData(frm);
		gross_monthly_salary(frm);
	},
});

function fetchAttendanceData(frm) {
	var employee = frm.doc.employee;
	var from_date = frm.doc.from_date;
	var to_date = frm.doc.to_date;

	frappe.call({
		method: 'zfpl.zfpl.doctype.overtime.overtime.get_attendance_data',
		args: {
			employee: employee,
			from_date: from_date,
			to_date: to_date,
		},
		callback: function (response) {
			var attendance_data = response.message;

			cur_frm.clear_table('overtime');

			for (var i = 0; i < attendance_data.length; i++) {
				var row = frm.add_child('overtime');
				row.employee_name = attendance_data[i].employee_name;
				row.working_hours = attendance_data[i].working_hours;
				row.attendance_date = attendance_data[i].attendance_date;
				row.att_name = attendance_data[i].name;

				fetchStandardWorkingHours(frm, row);
			}

			frm.refresh_field('overtime');
			updateTotalWorkingHours(frm);
		}
	});
}

function fetchStandardWorkingHours(frm, row) {
	frappe.call({
		method: 'zfpl.zfpl.doctype.overtime.overtime.get_standard_working_hours',
		callback: function (response) {
			var standard_working_hours = response.message;
			row.standard_working_hours = standard_working_hours;

			// Calculate overtime_hours
			row.overtime_hours = row.working_hours - row.standard_working_hours;
			// Set overtime_hours to 0 if negative
			if (row.overtime_hours < 0) {
				row.overtime_hours = 0;
			}

			// Refresh the form to show the updated child table
			frm.refresh_field('overtime');
		}
	});
}

function updateTotalWorkingHours(frm) {
	var total_working_hours = 0;
	var overtime_table = frm.doc.overtime || [];

	for (var i = 0; i < overtime_table.length; i++) {
		total_working_hours += overtime_table[i].working_hours;
	}

	frm.set_value('total_working_hours', total_working_hours);
}




function gross_monthly_salary(frm) {
	var employee = frm.doc.employee;

	frappe.call({
		method: 'zfpl.zfpl.doctype.overtime.overtime.get_gross_salary',
		args: {
			employee: employee
		},
		callback: function (response) {
			if (response.message) {
				frm.set_value('gross_monthly_salary', response.message);
			}
		}
	});
}





frappe.ui.form.on('Overtime', {
	before_save: function (frm) {
		var total_overtime_hours = 0;


		frm.doc.overtime.forEach(function (row) {
			total_overtime_hours += row.overtime_hours;
		});

		frm.set_value('total_overtime_hours', total_overtime_hours);

		// frm.set_value('payable_ot_hours', total_overtime_hours);
		console.log("Total Overtime/payable", total_overtime_hours);

		let gms = frm.doc.gross_monthly_salary;
		let hr = ((gms * 12) / 365) / 8;
		frm.set_value('hourly_rate', hr);

		let ot_payment = frm.doc.total_ot_payment;
		let payable_ot_hours = frm.doc.payable_ot_hours;
		hr = frm.doc.hourly_rate;
		let total_o_hours = frm.doc.total_overtime_hours;

		if (payable_ot_hours == 0) {
			ot_payment = total_o_hours * hr;
			frm.set_value('total_ot_payment', ot_payment);
		} else {
			ot_payment = payable_ot_hours * hr;
			frm.set_value('total_ot_payment', ot_payment);
		}
	},

	refresh: function (frm) {
		// Add a button to create expense claim
		if (frm.doc.docstatus == 1 && frm.doc.repay_from_salary == 0) {
			frm.add_custom_button(__('Create Expense Claim'), function () {
				frappe.call({
					method: 'zfpl.zfpl.doctype.overtime.overtime.make_expense_claim',
					args: {
						docname: frm.doc.name
					},
					// callback: function (r) {
					// 	if (r.message) {
					// 		var doc = frappe.model.sync(r.message);
					// 		frappe.set_route("Form", "Expense Claim", r.message.name);
					// 	}
					// }
					callback: function (r) {
						var doc = frappe.model.sync(r.message);
						frappe.set_route('Form', 'Expense Claim', r.message.name);
					}

				});
			});
		}
	}
});



// frappe.ui.form.on('Overtime', {
// 	refresh: function (frm) {
// 		// Add a button to create expense claim
// 		frm.add_custom_button(__('Create Expense Claim'), function () {
// 			frappe.call({
// 				method: 'zfpl.zfpl.doctype.overtime.overtime.make_expense_claim', // Change 'path.to.make_expense_claim' to the actual path of your function
// 				args: {
// 					source_name: frm.doc.name
// 				},
// 				callback: function (r) {
// 					if (r.message) {
// 						// Show a success message or perform any other action
// 						frappe.msgprint(__('Expense claim created successfully.'));
// 					}
// 				}
// 			});
// 		});
// 	}
// });







