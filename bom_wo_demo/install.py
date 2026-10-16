"""Idempotent schema setup for the manual-material Work Order mode."""

from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def after_install():
	install_work_order_customizations()


def after_migrate():
	install_work_order_customizations()


def install_work_order_customizations():
	"""Install the field and make BOM validation conditional in the controller.

	`bom_no` cannot remain schema-mandatory because Frappe validates mandatory
	fields before the Work Order controller can permit manual mode. Standard mode
	is instead required by the controller override.
	"""
	create_custom_fields(
		{
			"Work Order": [
				{
					"fieldname": "custom_use_manual_materials",
					"label": "Manual Material Entry (No BOM)",
					"fieldtype": "Check",
					"default": "0",
					"insert_after": "bom_no",
					"description": "Use manually entered Required Items instead of BOM-derived materials.",
				}
			]
		},
		update=True,
	)

	make_property_setter("Work Order", "bom_no", "reqd", "0", "Check", for_doctype=False)
