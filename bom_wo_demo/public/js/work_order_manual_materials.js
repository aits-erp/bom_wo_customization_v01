frappe.ui.form.on("Work Order", {
	refresh(frm) {
		set_manual_mode_ui(frm);
		add_manual_stock_entry_actions(frm);
	},

	custom_production_mode(frm) {
		if (is_manual_mode(frm) && frm.doc.bom_no) {
			frappe.confirm(
				__("Assembly and Disassembly do not manage BOM-derived materials. Clear the selected BOM and keep the visible Required Items for review?"),
				() => {
					frm.set_value("bom_no", "");
					set_manual_mode_ui(frm);
				},
				() => {
					frm.set_value("custom_production_mode", "BOM");
					set_manual_mode_ui(frm);
				}
			);
		} else {
			set_manual_mode_ui(frm);
		}
	},

	bom_no(frm) {
		if (is_manual_mode(frm)) return;
	},

	qty(frm) {
		if (is_manual_mode(frm)) return;
	}
});

function is_manual_mode(frm) {
	return ["Assembly", "Disassembly"].includes(frm.doc.custom_production_mode);
}

function set_manual_mode_ui(frm) {
	const manual = is_manual_mode(frm);
	const editable = manual && frm.doc.docstatus === 0;
	frm.toggle_reqd("bom_no", !manual);
	frm.toggle_display("bom_no", !manual || !!frm.doc.bom_no);

	if (manual) {
		// ERPNext's standard buttons call this function. Redirect supported actions
		// to the manual-row builder so a BOM-based entry is never generated.
		frm.events.make_se = (_frm, purpose) => {
			if (["Material Transfer for Manufacture", "Manufacture"].includes(purpose)) {
				make_manual_stock_entry(frm, purpose);
				return;
			}
			frappe.msgprint(__("This Stock Entry purpose is not supported in Assembly or Disassembly mode."));
		};
		frm.set_intro(
			__("{0} mode is active. Required Items are maintained manually and will not be regenerated from a BOM.", [frm.doc.custom_production_mode]),
			"orange"
		);
	}

	const grid = frm.fields_dict.required_items && frm.fields_dict.required_items.grid;
	if (!grid) return;
	["item_code", "required_qty", "source_warehouse", "allow_alternative_item"].forEach((fieldname) => {
		grid.update_docfield_property(fieldname, "read_only", !editable);
	});
	grid.cannot_add_rows = !editable;
	grid.cannot_delete_rows = !editable;
	grid.refresh();
}

function add_manual_stock_entry_actions(frm) {
	if (!is_manual_mode(frm) || frm.doc.docstatus !== 1) return;

	frm.add_custom_button(__("Material Transfer"), () => make_manual_stock_entry(frm, "Material Transfer for Manufacture"), __("Create"));
	frm.add_custom_button(__("Manufacture"), () => make_manual_stock_entry(frm, "Manufacture"), __("Create"));
}

function make_manual_stock_entry(frm, purpose) {
	const remaining = flt(frm.doc.qty) - flt(frm.doc.produced_qty);
	frappe.prompt(
		[{ fieldname: "qty", fieldtype: "Float", label: __("Quantity"), reqd: 1, default: remaining }],
		(values) => {
			frappe.call({
				method: "bom_wo_demo.api.make_manual_stock_entry",
				args: { work_order_name: frm.doc.name, purpose, qty: values.qty },
				freeze: true,
				freeze_message: __("Creating Stock Entry"),
				callback: (response) => {
					if (response.message && response.message.name) {
						frappe.set_route("Form", "Stock Entry", response.message.name);
					}
				}
			});
		},
		__(purpose)
	);
}
