from odoo import api, fields, models, _


class CustomerProfile(models.Model):
    _inherit = 'customer.profile'

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], required=True, tracking=True)
