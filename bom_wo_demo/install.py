"""Idempotent schema setup for the demo DocTypes and manual Work Order mode."""

from pathlib import Path

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from frappe.modules.import_file import import_file_by_path


def after_install():
	sync_demo_doctypes()
	install_work_order_customizations()


def after_migrate():
	sync_demo_doctypes()
	install_work_order_customizations()


def sync_demo_doctypes():
	"""Synchronize demo DocTypes even if a host skips the app's module scan.

	Normal ``bench migrate`` already syncs DocType JSON. This explicit fallback
	uses the app package path, rather than module discovery, and makes missing
	deployment files fail loudly with the precise path.
	"""
	# ``Bom Wo Demo`` is the app's module (not its package root), so Frappe
	# resolves controllers as ``bom_wo_demo.bom_wo_demo.doctype...``.
	doctype_root = Path(__file__).parent / "bom_wo_demo" / "doctype"
	doctypes = (
		"demo_assembly_item",
		"demo_assembly_order",
		"demo_disassembly_order",
		"production_mode_selector",
	)

	for doctype in doctypes:
		json_path = doctype_root / doctype / f"{doctype}.json"
		if not json_path.is_file():
			frappe.throw(f"Required BOM / Work Order demo DocType file is missing: {json_path}")
		import_file_by_path(str(json_path), force=False)


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
					"fieldname": "custom_production_mode",
					"label": "Production Mode",
					"fieldtype": "Select",
					"options": "BOM\nAssembly\nDisassembly",
					"default": "BOM",
					"insert_after": "bom_no",
					"description": "BOM uses the standard workflow. Assembly and Disassembly use manual Required Items without a BOM.",
				}
			]
		},
		update=True,
	)
	_hide_legacy_manual_material_field()
	_migrate_legacy_manual_material_records()

	make_property_setter("Work Order", "bom_no", "reqd", "0", "Check", for_doctype=False)


def _hide_legacy_manual_material_field():
	"""Retire the checkbox from the form without deleting historical data."""
	legacy_field = "Work Order-custom_use_manual_materials"
	if frappe.db.exists("Custom Field", legacy_field):
		frappe.db.set_value("Custom Field", legacy_field, {"hidden": 1, "read_only": 1})


def _migrate_legacy_manual_material_records():
	"""Existing checked records become Assembly, the nearest equivalent mode."""
	if not (
		frappe.db.has_column("Work Order", "custom_use_manual_materials")
		and frappe.db.has_column("Work Order", "custom_production_mode")
	):
		return

	frappe.db.sql(
		"""
		UPDATE `tabWork Order`
		SET custom_production_mode = 'Assembly'
		WHERE IFNULL(custom_use_manual_materials, 0) = 1
			AND IFNULL(custom_production_mode, '') = ''
		"""
	)
	frappe.db.sql(
		"""
		UPDATE `tabWork Order`
		SET custom_production_mode = 'BOM'
		WHERE IFNULL(custom_production_mode, '') = ''
		"""
	)
