{
    'name': 'Cosmic Commerce',
    'version': '1.0',
    'summary': 'Manages customer profiles and order flow for Cosmic Commerce',
    'sequence': 10,
    'description': """  This module provides functionality for managing customer profiles,
        sales orders, and product offerings for Cosmic Commerce.""",
    'category': 'Productivity',
    'website': 'http://www.cosmic-commerce.com',
    'depends': ['base', 'mail', 'web', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'security/commerce_security.xml',
        'security/commerce_record_rules.xml',
        'views/customer_profile_views.xml',
        'views/order_record_views.xml',
        'views/merchandise_offering_views.xml',
        'views/tag_label_views.xml',
        'views/inherit_customer_profile_view.xml',
        'wizard/create_order_record_wizard.xml',
        'reports/order_report_action.xml',
        'reports/order_report_template.xml',
        'data/cron.xml',
        'data/server_actions.xml',
        'views/website_templates.xml'

    ],
    'assets': {
        'web.assets_backend': [
            'cosmic_commerce/static/src/css/report_styles.css',
        ],
    },
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto install': False,
    'license': 'LGPL-3',
}
