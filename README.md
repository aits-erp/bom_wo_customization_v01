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
