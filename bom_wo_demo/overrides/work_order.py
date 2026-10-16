"""Narrow Work Order extension for BOM-optional manual material entry."""

import frappe
from frappe import _
from frappe.utils import cint, flt

from erpnext.manufacturing.doctype.work_order.work_order import WorkOrder
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from erpnext.stock.doctype.item.item import get_item_defaults


class ManualMaterialsWorkOrder(WorkOrder):
	"""Keep ERPNext's controller intact, overriding only BOM material generation."""

	def onload(self):
		super().onload()
		if self.use_manual_materials:
			# ERPNext's form uses this onload value to lock the Required Items grid.
			self.set_onload("allow_editing_items", 1)

	@property
	def use_manual_materials(self):
		mode = self.get("custom_production_mode")
		if not mode and cint(self.get("custom_use_manual_materials")):
			# Compatibility for a document saved before the mode migration ran.
			mode = "Assembly"
		return mode in ("Assembly", "Disassembly")

	def validate(self):
		if not self.use_manual_materials:
			if not self.bom_no:
				frappe.throw(_("BOM is required when Production Mode is BOM."))
			return super().validate()

		self._validate_manual_mode_context()
		self._prepare_manual_required_items()
		super().validate()
		self._validate_manual_required_items()

	def reset_use_multi_level_bom(self):
		if self.use_manual_materials:
			return
		return super().reset_use_multi_level_bom()

	def get_items_and_operations_from_bom(self):
		"""Never replace manually maintained rows when standard JS calls this method."""
		if self.use_manual_materials:
			return {}
		return super().get_items_and_operations_from_bom()

	def set_required_items(self, reset_only_qty=False):
		"""Prevent validate() and quantity changes from regenerating manual rows."""
		if self.use_manual_materials:
			self._prepare_manual_required_items()
			self.set_available_qty()
			return
		return super().set_required_items(reset_only_qty=reset_only_qty)

	def _validate_manual_mode_context(self):
		unsupported_fields = {
			"production_plan": _("Production Plan"),
			"production_plan_item": _("Production Plan Item"),
			"production_plan_sub_assembly_item": _("Production Plan Sub-assembly Item"),
			"subcontracting_inward_order": _("Subcontracting Inward Order"),
		}
		for fieldname, label in unsupported_fields.items():
			if self.get(fieldname):
				frappe.throw(
					_("Assembly and Disassembly cannot be used with {0}.").format(label),
					title=_("Unsupported manual-material combination"),
				)

		if self.operations:
			frappe.throw(
				_("Assembly and Disassembly currently do not support operations or Job Cards."),
				title=_("Unsupported manual-material combination"),
			)

	def _prepare_manual_required_items(self):
		"""Fill only missing item data; never overwrite a user-selected warehouse."""
		for row in self.get("required_items") or []:
			if not row.item_code:
				continue

			item = frappe.get_cached_value(
				"Item",
				row.item_code,
				["item_name", "description", "stock_uom", "disabled", "is_stock_item"],
				as_dict=True,
			)
			if not item:
				continue

			row.item_name = item.item_name
			row.description = item.description
			row.stock_uom = item.stock_uom
			row.include_item_in_manufacturing = 1
			if not row.source_warehouse:
				row.source_warehouse = (
					self.source_warehouse
					or get_item_defaults(row.item_code, self.company).get("default_warehouse")
					or get_item_group_defaults(row.item_code, self.company).get("default_warehouse")
				)

	def _validate_manual_required_items(self):
		rows = self.get("required_items") or []
		if not rows:
			frappe.throw(_("Add at least one Required Item for Assembly or Disassembly."))

		for row in rows:
			if not row.item_code:
				frappe.throw(_("Required Items: Row {0} needs an Item Code.").format(row.idx))
			if flt(row.required_qty) <= 0:
				frappe.throw(_("Required Items: Row {0} needs a positive Required Qty.").format(row.idx))
			if not row.stock_uom:
				frappe.throw(_("Required Items: Row {0} has no Stock UOM.").format(row.idx))
			if not row.source_warehouse:
				frappe.throw(_("Required Items: Row {0} needs a Source Warehouse.").format(row.idx))

			item = frappe.get_cached_value(
				"Item", row.item_code, ["disabled", "is_stock_item"], as_dict=True
			)
			if not item or item.disabled:
				frappe.throw(_("Required Items: Item {0} is disabled or does not exist.").format(row.item_code))
			if not cint(item.is_stock_item):
				frappe.throw(_("Required Items: Item {0} must be a stock item.").format(row.item_code))
