from odoo import api, models, fields

from server.odoo.api import readonly


class OrderRecord(models.Model):
    _name = 'order.record'
    _description = 'Sales Order Record'
    _rec_name = 'reference'

    reference = fields.Char(string='Order Number', required=True, default='New')
    buyer_id = fields.Many2one('customer.profile', string='Customer', required=True, ondelete='restrict')
    mobile_number = fields.Integer(related='buyer_id.mobile_number', store=True)
    order_date = fields.Datetime(string='Order Placed', default=fields.Datetime.now)
    age = fields.Integer(string="Age", related='buyer_id.age', readonly=False, store=True)

    order_details_ids = fields.One2many('item.line', 'order_ref_id', string='Order Details')

    @api.onchange('buyer_id')
    def onchange_buyer_id(self):
        if self.buyer_id:
            self.age = self.buyer_id.age
        else:
            self.age = ""
