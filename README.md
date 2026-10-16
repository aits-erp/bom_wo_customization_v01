### BOM / Work Order Demo

An isolated ERPNext Desk demo for selecting one of three manufacturing flows:

- **BOM** routes to ERPNext's standard BOM list; no standard behaviour is changed.
- **Assembly** opens a Work-Order-like custom form with production and required-item sections.
- **Disassembly** opens a reverse-production custom form with a source item and recovered-item section.

The custom Assembly and Disassembly DocTypes are intentionally **demo-only**. They validate basic user input but do not create Stock Entries, affect inventory, or modify ERPNext Work Orders. This lets the user demonstrate the intended screens safely before the production Work Order customization is started.

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app bom_wo_demo
bench --site <site-name> migrate
bench --site <site-name> clear-cache
```

After migration, open **Production Mode Selector** from Desk, create a selector record, choose BOM, Assembly, or Disassembly, and click **Open selected flow**.

### Manual materials on standard Work Orders

The app also adds a **Production Mode** select field to ERPNext Work Orders.

- **BOM** requires a BOM and retains the standard ERPNext workflow unchanged.
- **Assembly** and **Disassembly** use manually maintained Required Items and do not generate BOM-derived materials.
- After submitting an Assembly or Disassembly Work Order, use **Create → Material Transfer** or **Create → Manufacture**. The app creates a normal draft Stock Entry with quantities scaled to the requested partial-production quantity. Review and submit that Stock Entry through ERPNext's standard form, particularly where serial or batch details are required.
- Manual modes block Job Cards/operations, Production Plan-linked Work Orders, and subcontracting combinations until they receive dedicated integration and tests.

This feature must be installed and verified on a non-production ERPNext v15 site before use. The repository currently has no Bench or site, so the integration tests and ledger verification could not be run here.

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/bom_wo_demo
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
