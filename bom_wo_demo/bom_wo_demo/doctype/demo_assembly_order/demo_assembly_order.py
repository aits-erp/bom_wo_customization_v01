import frappe
from frappe.model.document import Document


class DemoAssemblyOrder(Document):
	"""Demo-only Work Order-like form. It does not create stock transactions."""

	def validate(self):
		self._validate_items("required_items", "Required Items")
		self._validate_items("produced_items", "Produced Items")

	def _validate_items(self, fieldname, label):
		for row in self.get(fieldname) or []:
			if not row.item_code:
				frappe.throw(f"{label}: Row {row.idx} requires an Item Code.")
			if not row.qty or row.qty <= 0:
				frappe.throw(f"{label}: Row {row.idx} requires a positive quantity.")
