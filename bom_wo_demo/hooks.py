app_name = "bom_wo_demo"
app_title = "Bom Wo Demo"
app_publisher = "aits"
app_description = "demo app"
app_email = "nikhil@aitsind.com"
app_license = "mit"

# Apps
# ------------------

# The demo routes to ERPNext's native BOM and Work Order screens and uses its
# Company, Item, UOM and Warehouse DocTypes in the demo forms.
required_apps = ["erpnext"]

after_install = "bom_wo_demo.install.after_install"
after_migrate = "bom_wo_demo.install.after_migrate"

override_doctype_class = {
	"Work Order": "bom_wo_demo.overrides.work_order.ManualMaterialsWorkOrder",
}

doctype_js = {
	"Work Order": "public/js/work_order_manual_materials.js",
}

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "bom_wo_demo",
# 		"logo": "/assets/bom_wo_demo/logo.png",
# 		"title": "Bom Wo Demo",
# 		"route": "/bom_wo_demo",
# 		"has_permission": "bom_wo_demo.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/bom_wo_demo/css/bom_wo_demo.css"
# app_include_js = "/assets/bom_wo_demo/js/bom_wo_demo.js"

# include js, css files in header of web template
# web_include_css = "/assets/bom_wo_demo/css/bom_wo_demo.css"
# web_include_js = "/assets/bom_wo_demo/js/bom_wo_demo.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "bom_wo_demo/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "bom_wo_demo/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "bom_wo_demo.utils.jinja_methods",
# 	"filters": "bom_wo_demo.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "bom_wo_demo.install.before_install"
# after_install = "bom_wo_demo.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "bom_wo_demo.uninstall.before_uninstall"
# after_uninstall = "bom_wo_demo.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "bom_wo_demo.utils.before_app_install"
# after_app_install = "bom_wo_demo.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "bom_wo_demo.utils.before_app_uninstall"
# after_app_uninstall = "bom_wo_demo.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "bom_wo_demo.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"bom_wo_demo.tasks.all"
# 	],
# 	"daily": [
# 		"bom_wo_demo.tasks.daily"
# 	],
# 	"hourly": [
# 		"bom_wo_demo.tasks.hourly"
# 	],
# 	"weekly": [
# 		"bom_wo_demo.tasks.weekly"
# 	],
# 	"monthly": [
# 		"bom_wo_demo.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "bom_wo_demo.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "bom_wo_demo.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "bom_wo_demo.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["bom_wo_demo.utils.before_request"]
# after_request = ["bom_wo_demo.utils.after_request"]

# Job Events
# ----------
# before_job = ["bom_wo_demo.utils.before_job"]
# after_job = ["bom_wo_demo.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"bom_wo_demo.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

