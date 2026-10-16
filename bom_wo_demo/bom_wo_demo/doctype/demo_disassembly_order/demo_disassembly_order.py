import frappe
from frappe.model.document import Document


class DemoDisassemblyOrder(Document):
	"""Demo-only reverse Work Order-like form. It does not create stock transactions."""

	def validate(self):
		if not self.source_item or not self.source_qty or self.source_qty <= 0:
			frappe.throw("Source Item and a positive Source Quantity are required.")
		for row in self.recovered_items or []:
			if not row.item_code:
				frappe.throw(f"Recovered Items: Row {row.idx} requires an Item Code.")
			if not row.qty or row.qty <= 0:
				frappe.throw(f"Recovered Items: Row {row.idx} requires a positive quantity.")
