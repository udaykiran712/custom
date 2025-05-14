{
    'name': 'Custom POS Button',
    'version': '1.0',
    'license': 'LGPL-3',
    'category': 'Point of Sale',
    'summary': 'Adds a custom button to the POS interface',
    'depends': ['point_of_sale'],
    'data': [],
    'assets': {
        'point_of_sale.pos_assets': [
            'custom_pos_button/static/src/js/custom_button.js',
        ],
    },
    'installable': True,
    'auto_install': False,
}
