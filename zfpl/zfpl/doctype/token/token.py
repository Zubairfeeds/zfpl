# Copyright (c) 2024, Atom Global and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class Token(Document):
	pass



@frappe.whitelist()
def make_grn(source_name, target_doc=None):
    target_doc = get_mapped_doc("Token", source_name, {
        "Token": {
            "doctype": "Purchase Receipt",
            "field_map": {
                # Map other fields as needed
            }
        },
        "Token Item": {
            "doctype": "Purchase Receipt Item",
            "field_map": {
                "item_name": "item_name",
                "item_code": "item_code",  # Adjust this mapping based on your actual field names
                # Map other fields as needed
            }
        }
    }, target_doc)

    return target_doc

def on_token_trash(doc, method):
    frappe.log_error("Token deletion triggered for: " + doc.name, "Before Trash Event")
    
    if doc.weigh_slip:
        try:
            frappe.client.set_value(
                "Weigh Slip",
                doc.weigh_slip,
                "status",
                "Open"
            )
            frappe.log_error("Weigh Slip status set to 'Open'", "Weigh Slip Status Update")
        except Exception as e:
            frappe.log_error("Error updating Weigh Slip status: " + str(e), "Weigh Slip Status Error")