from . import __version__ as app_version

app_name = "zfpl"
app_title = "ZFPL"
app_publisher = "Atom Global"
app_description = "An app for manufacturing process including token etc"
app_email = "info@atom-global.com"
app_license = "Please contact info@atom-global.com"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/zfpl/css/zfpl.css"
# app_include_js = "/assets/zfpl/js/zfpl.js"

# include js, css files in header of web template
# web_include_css = "/assets/zfpl/css/zfpl.css"
# web_include_js = "/assets/zfpl/js/zfpl.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "zfpl/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views


doctype_js = {
	"Token": "public/js/zfpl_token.js",
}


# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "zfpl.utils.jinja_methods",
#	"filters": "zfpl.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "zfpl.install.before_install"
# after_install = "zfpl.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "zfpl.uninstall.before_uninstall"
# after_uninstall = "zfpl.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "zfpl.utils.before_app_install"
# after_app_install = "zfpl.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "zfpl.utils.before_app_uninstall"
# after_app_uninstall = "zfpl.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "zfpl.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
    
    "Overtime":{
        "on_submit":"zfpl.zfpl.doctype.overtime.overtime.create_additional_salary",
    },
	"Token": {
        "before_trash": "zfpl.zfpl.doctype.token.token.on_token_trash"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"zfpl.tasks.all"
#	],
#	"daily": [
#		"zfpl.tasks.daily"
#	],
#	"hourly": [
#		"zfpl.tasks.hourly"
#	],
#	"weekly": [
#		"zfpl.tasks.weekly"
#	],
#	"monthly": [
#		"zfpl.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "zfpl.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "zfpl.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "zfpl.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["zfpl.utils.before_request"]
# after_request = ["zfpl.utils.after_request"]

# Job Events
# ----------
# before_job = ["zfpl.utils.before_job"]
# after_job = ["zfpl.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"zfpl.auth.validate"
# ]

fixtures = ['Custom Field']
