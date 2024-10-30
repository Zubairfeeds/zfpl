# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
# Copyright (c) 2024, Atom Global and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc


class Overtime(Document):
	pass


def validate(doc, method):
    existing_overtime = frappe.db.exists(
        "Overtime",
        # {
        #     "from_date": doc.from_date,
        #     "to_date": doc.to_date,
        #     "employee": doc.employee,
        #     "name": ("!=", doc.name) if doc.name else None
        # }
        {
            "employee": doc.employee,
            "name": ("!=", doc.name) if doc.name else None,
            "from_date": ("<=", doc.from_date),
            "to_date": (">=", doc.from_date)
        }
    )

    if existing_overtime:
        frappe.throw(_("Overtime is already created for {0} between {1} to {2}  date").format(doc.employee, doc.from_date, doc.to_date))




# @frappe.whitelist()
# def get_attendance_data(employee, from_date, to_date):

#     attendance_data = frappe.db.sql("""
#         SELECT name, employee_name, working_hours, attendance_date
#         FROM `tabAttendance`
#         WHERE employee = %s AND attendance_date BETWEEN %s AND %s
#     """, (employee, from_date, to_date), as_dict=True)
#     return attendance_data
@frappe.whitelist()
def get_attendance_data(employee, from_date, to_date):

    attendance_data = frappe.db.sql("""
        SELECT name, employee_name, working_hours, attendance_date
        FROM `tabAttendance`
        WHERE employee = %s 
            AND attendance_date BETWEEN %s AND %s
            AND docstatus != 'Cancelled'
            AND docstatus != '2'
    """, (employee, from_date, to_date), as_dict=True)

    return attendance_data

@frappe.whitelist()
def get_standard_working_hours():
    # Fetch standard_working_hours from HR Settings
    hr_settings = frappe.get_doc('HR Settings')
    return hr_settings.standard_working_hours

@frappe.whitelist()
def get_gross_salary(employee):
    salary_structure_assignment = frappe.get_value(
        'Salary Structure Assignment',
        {
			'employee': employee,
		 	'docstatus': 1,
		},
        'gross_monthly_salary'
    )

    return salary_structure_assignment

# @frappe.whitelist()
# def make_payment_entry(source_name, target_doc=None):
#     target_doc = get_mapped_doc("Overtime", source_name, {
#         "Overtime": {
#             "doctype": "Payment Entry",
#             "field_map": {
#                 "mode_of_payment": "mode_of_payment",
#                 "employee": "party",
#                 "total_ot_payment": "paid_amount"
#             }
#         },
#     }, target_doc)
#     target_doc.payment_type = "Pay",
#     target_doc.party_type = "Employee"

#     return target_doc


# @frappe.whitelist()
# def make_expense_claim(source_name, target_doc=None):
#     target_doc = get_mapped_doc("Overtime", source_name, {
#         "Overtime": {
#             "doctype": "Expense Claim",
#             "field_map": {
#                 "employee": "party",
#                 "name": "overtime"
#             }
#         },
#     }, target_doc)

#     # Add Expenses based on Overtime data
#     add_expenses_from_overtime(source_name, target_doc)

#     return target_doc

# def add_expenses_from_overtime(overtime_name, expense_claim_doc):
#     total_ot_payment = frappe.get_value("Overtime", overtime_name, "total_ot_payment")
#     date = frappe.get_value("Overtime", overtime_name, "date")

#     new_expense = frappe.new_doc('Expense Claim Detail')
#     new_expense.expense_type = 'Overtime'
#     new_expense.amount = total_ot_payment
#     new_expense.expense_date = date

#     # Append the new expense entry to the Expenses child table
#     expense_claim_doc.append('expenses', new_expense)


@frappe.whitelist()
def make_expense_claim(docname):
	expense_claim = frappe.db.exists("Expense Claim", {"overtime": docname})
	if expense_claim:
		frappe.throw(_("Expense Claim {0} already exists for the Expense Claim").format(expense_claim))

	overtime = frappe.get_doc("Overtime", docname)
	# service_expense = sum([flt(d.expense_amount) for d in vehicle_log.service_detail])

	# claim_amount = service_expense + (flt(vehicle_log.price) * flt(vehicle_log.fuel_qty) or 1)
	# if not claim_amount:
	# 	frappe.throw(_("No additional expenses has been added"))

	exp_claim = frappe.new_doc("Expense Claim")
	exp_claim.employee = overtime.employee
	exp_claim.overtime = overtime.name
	exp_claim.remark = _("Expense Claim for Overtime {0}").format(overtime.name)
	exp_claim.append(
		"expenses",
		{"expense_date": overtime.date, "expense_type": _("OverTime"), "amount": overtime.total_ot_payment},
	)
	return exp_claim.as_dict()





# @frappe.whitelist()
# def make_expense_claim(source_name):
#     # Create a new Expense Claim document
#     expense_claim = frappe.new_doc("Expense Claim")
    
#     # Get data from the Overtime document
#     overtime = frappe.get_doc("Overtime", source_name)
    
#     # Map fields from the Overtime document to the Expense Claim document
#     expense_claim.employee = overtime.employee
#     expense_claim.posting_date = overtime.date
#     # Map other fields as needed

#     # Save the Expense Claim document
#     expense_claim.insert()

#     # Add expenses based on Overtime data
#     add_expenses_from_overtime(source_name, expense_claim)

#     return expense_claim

# def add_expenses_from_overtime(overtime_name, expense_claim_doc):
#     total_ot_payment = frappe.get_value("Overtime", overtime_name, "total_ot_payment")
#     date = frappe.get_value("Overtime", overtime_name, "date")

#     new_expense = frappe.new_doc('Expense Claim Detail')
#     new_expense.expense_type = 'Overtime'
#     new_expense.amount = total_ot_payment
#     new_expense.expense_date = date

#     # Append the new expense entry to the Expenses child table
#     expense_claim_doc.append('expenses', new_expense)







# submitted through hook.py
def create_additional_salary(doc, method):
    if doc.docstatus == 1 and doc.repay_from_salary == 1 and doc.total_ot_payment != 0:
        company = frappe.db.get_value("Employee", doc.employee, "company")

        additional_salary = frappe.new_doc("Additional Salary")
        additional_salary.employee = doc.employee
        additional_salary.salary_component = 'Overtime'
        additional_salary.overwrite_salary_structure_amount = 0
        additional_salary.amount = doc.total_ot_payment
        additional_salary.payroll_date = doc.date
        additional_salary.company = company
        additional_salary.ref_doctype = doc.doctype
        additional_salary.ref_docname = doc.name
        additional_salary.insert()

        additional_salary.submit()


