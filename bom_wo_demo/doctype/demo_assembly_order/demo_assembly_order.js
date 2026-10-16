frappe.ui.form.on("Demo Assembly Order", {
	refresh(frm) {
		frm.set_intro(__("Demo only: this form mirrors Work Order data entry and does not create Stock Entries."), "orange");
		frm.add_custom_button(__("Open Work Order"), () => frappe.set_route("List", "Work Order"));
	},

	production_item(frm) {
		if (frm.doc.production_item && !frm.doc.uom) {
			frappe.db.get_value("Item", frm.doc.production_item, "stock_uom").then(({ message }) => {
				if (message && message.stock_uom) frm.set_value("uom", message.stock_uom);
			});
		}
	}
});
