frappe.ui.form.on("Production Mode Selector", {
	refresh(frm) {
		frm.set_intro(
			__("Choose a flow. BOM opens ERPNext's standard BOM screen; Assembly and Disassembly open demo forms."),
			"blue"
		);
		frm.add_custom_button(__("Open selected flow"), () => open_selected_flow(frm));
	},

	production_flow(frm) {
		frm.set_value("description", get_description(frm.doc.production_flow));
	}
});

function open_selected_flow(frm) {
	const routes = {
		BOM: ["List", "BOM"],
		Assembly: ["List", "Demo Assembly Order"],
		Disassembly: ["List", "Demo Disassembly Order"]
	};
	const route = routes[frm.doc.production_flow];
	if (!route) {
		frappe.msgprint(__("Select BOM, Assembly, or Disassembly first."));
		return;
	}
	frappe.set_route(...route);
}

function get_description(flow) {
	const descriptions = {
		BOM: __("Use ERPNext's standard BOM screen."),
		Assembly: __("Use the demo Assembly Order screen."),
		Disassembly: __("Use the demo Disassembly Order screen.")
	};
	return descriptions[flow] || "";
}
