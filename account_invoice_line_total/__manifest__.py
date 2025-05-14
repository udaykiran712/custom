{
    'name': 'Account Invoice Line Total',
    'version': '1.0',
    'summary': 'Add total with tax in invoice lines',
    'description': """
    This module adds a field to display the total amount (with tax) in the invoice lines.
    """,
    'category': 'Accounting',
    'author': 'Your Name',
    'website': 'http://www.example.com',
    'depends': ['sale', 'account', 'stock', 'mrp', 'point_of_sale'],
    'data': [
        'views/account_move_line_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    'auto_install': False,
}
