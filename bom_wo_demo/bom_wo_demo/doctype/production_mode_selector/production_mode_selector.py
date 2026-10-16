import frappe
from frappe.model.document import Document


class ProductionModeSelector(Document):
	"""A small Desk entry point for the isolated manufacturing-flow demo."""

	def validate(self):
		if not self.production_flow:
			frappe.throw("Select a production flow.")
