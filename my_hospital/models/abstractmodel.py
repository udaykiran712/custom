from odoo import models, fields, api

class BaseTrackedModel(models.AbstractModel):

    _name = 'base.tracked'
    _description = 'Basic Abstract Tracked Model'
    _auto = False

    tracked = fields.Boolean(string='Tracked', default=False)

class Product(models.Model):
    _name = 'my.product'
    _description = 'My Product'
    _inherit = 'base.tracked'

    name = fields.Char(string='Name', required=True)
    price = fields.Float(string='Price')

class Customer(models.Model):
    _name = 'my.customer'
    _description = 'My Customer'
    _inherit = 'base.tracked'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')