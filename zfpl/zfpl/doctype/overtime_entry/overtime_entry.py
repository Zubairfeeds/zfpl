# Copyright (c) 2024, Atom Global and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.desk.reportview import get_filters_cond, get_match_cond
from frappe.model.document import Document

class OvertimeEntry(Document):
	pass


@frappe.whitelist()
def get_employees(doctype, docname, department=None, branch=None, designation=None):
    overtime_entry = frappe.get_doc(doctype, docname)
    filters = {}
    
    if department:
        filters["department"] = department
    if branch:
        filters["branch"] = branch
    if designation:
        filters["designation"] = designation        
    
    if filters:
        employees = frappe.get_all("Employee", filters=filters, fields=["name", "employee_name"])
    else:
        employees = frappe.get_all("Employee", fields=["name", "employee_name"])
    
    if employees:
        overtime_entry.set("employees", [])
        for employee in employees:
            overtime_entry.append("employees", {
                "employee": employee.name,
                "employee_name": employee.employee_name
            })
        overtime_entry.save()
    else:
        frappe.msgprint("No employees found.")


def create_overtime(doc, method):
    if doc.doctype == 'Overtime Entry':
        for employee in doc.get('employees'):
            overtime = frappe.new_doc('Overtime')
            overtime.from_date = doc.start_date
            overtime.to_date = doc.end_date
            overtime.employee = employee.employee
            overtime.overtime_entry = doc.name
            overtime.save()
