{
    'name': 'Bank Receipt Custom',
    'version': '1.0',
    'summary': 'Manual Bank Receipts under Accounting > Customers',
    'category': 'Accounting',
    'author': 'Your Name',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/bank_receipt_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
}
