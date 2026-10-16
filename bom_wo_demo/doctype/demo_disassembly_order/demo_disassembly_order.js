frappe.ui.form.on("Demo Disassembly Order", {
	refresh(frm) {
		frm.set_intro(__("Demo only: this form models reverse production and does not create Stock Entries."), "orange");
		frm.add_custom_button(__("Open Work Order"), () => frappe.set_route("List", "Work Order"));
	},

	source_item(frm) {
		if (frm.doc.source_item && !frm.doc.source_uom) {
			frappe.db.get_value("Item", frm.doc.source_item, "stock_uom").then(({ message }) => {
				if (message && message.stock_uom) frm.set_value("source_uom", message.stock_uom);
			});
		}
	}
});
