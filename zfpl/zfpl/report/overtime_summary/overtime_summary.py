# Copyright (c) 2024, Atom Global and contributors
# For license information, please see license.txt

import frappe


# # def execute(filters=None):
# # 	columns, data = [], []
# # 	return columns, data

def get_columns(group_by=None):
    columns = [
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 200, "align": "left"},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 200, "align": "left"},
        {"label": "Total Working Hours", "fieldname": "total_working_hours", "fieldtype": "Float", "align": "left", "width": 120,},
        {"label": "Standard Working Hours", "fieldname": "st_working_hours", "fieldtype": "Float", "align": "left", "width": 100,},
        {"label": "Total Overtime Hours", "fieldname": "total_overtime_hours", "fieldtype": "Float", "align": "left", "width": 100,},
        {"label": "Approved OT Hours", "fieldname": "payable_ot_hours", "fieldtype": "Float", "align": "left", "width": 100,},
        {"label": "Hourly Rate", "fieldname": "hourly_rate", "fieldtype": "Currency", "align": "left", "width": 100,},
        {"label": "Payable Overtime", "fieldname": "total_ot_payment", "fieldtype": "Currency", "align": "left", "width": 100,}
    ]

    if group_by:
        group_by_lower = group_by.lower()
        if group_by_lower == "branch":
            columns.insert(2, {"label": "Branch", "fieldname": "branch", "fieldtype": "Data", "width": 150, "align": "left"})
        elif group_by_lower == "department":
            columns.insert(2, {"label": "Department", "fieldname": "department", "fieldtype": "Data", "width": 150, "align": "left"})

    return columns if group_by else columns[:]


def get_data(filters):
    data = []
    subtotal = {}
    current_group = None
    branch_totals = {}  # Dictionary to store branch-wise subtotals
    department_totals = {}  # Dictionary to store department-wise subtotals
    grand_total = {
        "employee": "Grand Total",
        "total_working_hours": 0,
        "total_overtime_hours": 0,
        "hourly_rate": 0,
        "payable_ot_hours": 0,
        "total_ot_payment": 0
    }

    standard_working_hours = 8
    
    # Example query to fetch data based on the provided filters
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    employee = filters.get("employee")
    group_by = filters.get("group_by")
    branch = filters.get("branch")  # New filter for branch
    department = filters.get("department")  # New filter for department

    if from_date and to_date:
        # Construct the WHERE clause based on the provided filters
        where_clause = "`date` BETWEEN %s AND %s"
        params = [from_date, to_date]

        if employee:
            where_clause += " AND `employee` = %s"
            params.append(employee)

        # Fetch overtime data from the database based on date range and optionally employee filter
        if group_by:
            group_by_lower = group_by.lower()
            if group_by_lower == 'branch':
                overtime_records = frappe.db.sql("""
                    SELECT e.name AS employee, e.employee_name, o.total_working_hours, o.total_overtime_hours, o.hourly_rate, o.payable_ot_hours, o.total_ot_payment, 
                           e.branch AS group_field, e.department
                    FROM `tabEmployee` e
                    INNER JOIN `tabOvertime` o ON e.name = o.employee
                    WHERE {}
                """.format(where_clause), tuple(params), as_dict=True)
            elif group_by_lower == 'department':
                overtime_records = frappe.db.sql("""
                    SELECT e.name AS employee, e.employee_name, o.total_working_hours, o.total_overtime_hours, o.hourly_rate, o.payable_ot_hours, o.total_ot_payment, 
                           e.department AS group_field
                    FROM `tabEmployee` e
                    INNER JOIN `tabOvertime` o ON e.name = o.employee
                    WHERE {}
                """.format(where_clause), tuple(params), as_dict=True)
            else:
                overtime_records = frappe.db.sql("""
                    SELECT o.employee, o.employee_name, o.total_working_hours, o.total_overtime_hours, o.hourly_rate, o.payable_ot_hours, o.total_ot_payment, 
                           {} AS group_field
                    FROM `tabOvertime` o
                    WHERE {}
                    GROUP BY {}
                """.format(group_by_lower, where_clause, group_by_lower), tuple(params), as_dict=True)
        else:
            overtime_records = frappe.db.sql("""
                SELECT o.employee, o.employee_name, o.total_working_hours, o.total_overtime_hours, o.hourly_rate, o.payable_ot_hours, o.total_ot_payment
                FROM `tabOvertime` o
                WHERE {}
            """.format(where_clause), tuple(params), as_dict=True)

        # Populate data list with fetched results and calculate subtotals
        for record in overtime_records:
            st_working_hours = standard_working_hours

            if branch and record.get('group_field') != branch:  # Filter by branch if specified
                continue

            if department and record.get('group_field') != department:  # Filter by department if specified
                continue

            if group_by:
                if record['group_field'] != current_group:
                    if current_group:
                        data.append({
                            group_by_lower: current_group,
                            "total_working_hours": subtotal.get("total_working_hours", 0),
                            "total_overtime_hours": subtotal.get("total_overtime_hours", 0),
                            "hourly_rate": subtotal.get("hourly_rate", 0),
                            "payable_ot_hours": subtotal.get("payable_ot_hours", 0),
                            "total_ot_payment": subtotal.get("total_ot_payment", 0)
                        })
                        if group_by_lower == 'branch':
                            branch_totals[current_group] = subtotal.copy()  # Save subtotal for this branch
                        elif group_by_lower == 'department':
                            department_totals[current_group] = subtotal.copy()  # Save subtotal for this department
                        subtotal = {}
                    current_group = record['group_field']

                for key in ['total_working_hours', 'total_overtime_hours', 'hourly_rate', 'payable_ot_hours', 'total_ot_payment']:
                    subtotal[key] = subtotal.get(key, 0) + record.get(key, 0)

            data.append({
                "employee": record['employee'],
                "employee_name": record['employee_name'],
                "st_working_hours": st_working_hours,
                "total_working_hours": record['total_working_hours'],
                "total_overtime_hours": record['total_overtime_hours'],
                "hourly_rate": record['hourly_rate'],
                "payable_ot_hours": record['payable_ot_hours'],
                "total_ot_payment": record['total_ot_payment']
            })

        if group_by:
            if current_group:
                data.append({
                    group_by_lower: current_group,
                    "total_working_hours": subtotal.get("total_working_hours", 0),
                    "total_overtime_hours": subtotal.get("total_overtime_hours", 0),
                    "hourly_rate": subtotal.get("hourly_rate", 0),
                    "payable_ot_hours": subtotal.get("payable_ot_hours", 0),
                    "total_ot_payment": subtotal.get("total_ot_payment", 0)
                })
                if group_by_lower == 'branch':
                    branch_totals[current_group] = subtotal.copy()  # Save subtotal for this branch
                elif group_by_lower == 'department':
                    department_totals[current_group] = subtotal.copy()  # Save subtotal for this department

    # Calculate grand total for branches
    for subtotal in branch_totals.values():
        grand_total["total_working_hours"] += subtotal.get("total_working_hours", 0)
        grand_total["total_overtime_hours"] += subtotal.get("total_overtime_hours", 0)
        grand_total["hourly_rate"] += subtotal.get("hourly_rate", 0)
        grand_total["payable_ot_hours"] += subtotal.get("payable_ot_hours", 0)
        grand_total["total_ot_payment"] += subtotal.get("total_ot_payment", 0)

    # Calculate grand total for departments
    for subtotal in department_totals.values():
        grand_total["total_working_hours"] += subtotal.get("total_working_hours", 0)
        grand_total["total_overtime_hours"] += subtotal.get("total_overtime_hours", 0)
        grand_total["hourly_rate"] += subtotal.get("hourly_rate", 0)
        grand_total["payable_ot_hours"] += subtotal.get("payable_ot_hours", 0)
        grand_total["total_ot_payment"] += subtotal.get("total_ot_payment", 0)

    if not group_by:  # Calculate grand total by summing up all rows
        grand_total = {
            "employee": "Grand Total",
            "total_working_hours": sum(record["total_working_hours"] for record in data),
            "total_overtime_hours": sum(record["total_overtime_hours"] for record in data),
            "hourly_rate": sum(record["hourly_rate"] for record in data),
            "payable_ot_hours": sum(record["payable_ot_hours"] for record in data),
            "total_ot_payment": sum(record["total_ot_payment"] for record in data)
        }    

    data.append(grand_total)  # Append grand total row

    return data


def get_filters():
    return [
        {"fieldname": "from_date", "label": "From Date", "fieldtype": "Date", "default": frappe.utils.today(), "reqd": 1},
        {"fieldname": "to_date", "label": "To Date", "fieldtype": "Date", "default": frappe.utils.today(), "reqd": 1},
        {"fieldname": "employee", "label": "Employee", "fieldtype": "Link", "options": "Employee"},
        {"fieldname": "group_by", "label": "Group By", "fieldtype": "Select", "options": ["", "Branch", "Department"]},
        {"fieldname": "branch", "label": "Branch", "fieldtype": "Link", "options": "Branch"}  # New filter for branch
    ]

def execute(filters=None):
    group_by = filters.get("group_by")
    columns = get_columns(group_by)
    data = get_data(filters)
    return columns, data, get_filters()





