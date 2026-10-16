"""Server endpoints for draft Stock Entries generated from manual Work Order rows."""

import frappe
from frappe import _
from frappe.utils import flt


SUPPORTED_PURPOSES = {"Material Transfer for Manufacture", "Manufacture"}


@frappe.whitelist()
def make_manual_stock_entry(work_order_name, purpose, qty):
	"""Create a normal draft Stock Entry from a submitted manual-mode Work Order.

	The entry is deliberately left in Draft so the standard Stock Entry form can
	collect serial/batch details and run its normal validation before it posts
	stock ledger and accounting entries.
	"""
	if purpose not in SUPPORTED_PURPOSES:
		frappe.throw(_("Unsupported manual-material Stock Entry purpose."))

	work_order = frappe.get_doc("Work Order", work_order_name)
	work_order.check_permission("read")
	work_order.check_permission("write")
	frappe.has_permission("Stock Entry", "create", throw=True)

	if not work_order.custom_use_manual_materials:
		frappe.throw(_("This action is only available for Manual Material Entry Work Orders."))
	if work_order.docstatus != 1:
		frappe.throw(_("Submit the Work Order before creating a Stock Entry."))

	manufacture_qty = flt(qty)
	if manufacture_qty <= 0:
		frappe.throw(_("Quantity must be greater than zero."))

	remaining_qty = flt(work_order.qty) - flt(work_order.produced_qty)
	if purpose == "Manufacture" and manufacture_qty > remaining_qty:
		frappe.throw(_("Quantity exceeds the remaining quantity to manufacture ({0}).").format(remaining_qty))

	entry = frappe.new_doc("Stock Entry")
	entry.update(
		{
			"purpose": purpose,
			"company": work_order.company,
			"work_order": work_order.name,
			# Stock Entry uses this quantity to update the normal Work Order status.
			"fg_completed_qty": manufacture_qty,
			# There is no BOM, but this identifies a manufacturing entry to the
			# standard Stock Entry/Work Order update pipeline.
			"from_bom": 1,
			"project": work_order.project,
		}
	)

	if purpose == "Material Transfer for Manufacture":
		entry.to_warehouse = work_order.wip_warehouse
		_append_transfer_items(entry, work_order, manufacture_qty)
	else:
		entry.from_warehouse = work_order.source_warehouse if work_order.skip_transfer else work_order.wip_warehouse
		entry.to_warehouse = work_order.fg_warehouse
		_append_manufacture_items(entry, work_order, manufacture_qty)

	entry.set_stock_entry_type()
	entry.insert()
	return {"name": entry.name}


def _append_transfer_items(entry, work_order, manufacture_qty):
	for row in work_order.required_items:
		item_qty = _proportional_qty(row.required_qty, work_order.qty, manufacture_qty)
		pending_qty = flt(row.required_qty) - flt(row.transferred_qty)
		if item_qty > pending_qty:
			frappe.throw(
				_("Transfer quantity for item {0} exceeds its pending required quantity.").format(row.item_code)
			)
		_append_raw_material(entry, row, item_qty, row.source_warehouse, work_order.wip_warehouse)


def _append_manufacture_items(entry, work_order, manufacture_qty):
	for row in work_order.required_items:
		item_qty = _proportional_qty(row.required_qty, work_order.qty, manufacture_qty)
		if work_order.skip_transfer:
			source_warehouse = row.source_warehouse
		else:
			pending_qty = flt(row.transferred_qty) - flt(row.consumed_qty)
			if item_qty > pending_qty:
				frappe.throw(
					_("Transfer material for item {0} before manufacturing this quantity.").format(row.item_code)
				)
			source_warehouse = work_order.wip_warehouse
		_append_raw_material(entry, row, item_qty, source_warehouse, None)

	item = frappe.get_cached_value(
		"Item", work_order.production_item, ["item_name", "description", "stock_uom"], as_dict=True
	)
	entry.append(
		"items",
		{
			"item_code": work_order.production_item,
			"item_name": item.item_name,
			"description": item.description,
			"qty": manufacture_qty,
			"uom": item.stock_uom,
			"stock_uom": item.stock_uom,
			"conversion_factor": 1,
			"t_warehouse": work_order.fg_warehouse,
			"is_finished_item": 1,
		},
	)


def _append_raw_material(entry, row, qty, source_warehouse, target_warehouse):
	entry.append(
		"items",
		{
			"item_code": row.item_code,
			"item_name": row.item_name,
			"description": row.description,
			"qty": qty,
			"uom": row.stock_uom,
			"stock_uom": row.stock_uom,
			"conversion_factor": 1,
			"s_warehouse": source_warehouse,
			"t_warehouse": target_warehouse,
		},
	)


def _proportional_qty(required_qty, work_order_qty, manufacture_qty):
	return flt(required_qty) * flt(manufacture_qty) / flt(work_order_qty)
