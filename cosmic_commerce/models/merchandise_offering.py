from odoo import models, fields

class MerchandiseOffering(models.Model):
    _name = 'merchandise.offering'
    _description = 'Product Offering'

    display_name = fields.Char(string='Product Name', required=True)
    selling_price = fields.Float(string='Sale Price')


