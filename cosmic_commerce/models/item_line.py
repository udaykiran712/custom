from odoo import models, fields, api


class ItemLine(models.Model):
    _name = 'item.line'
    _description = 'Sales Order Item'

    order_ref_id = fields.Many2one('order.record', string='Order')

    product_sku_id = fields.Many2one('merchandise.offering', string='Product', required=True)
    quantity = fields.Integer(string='Qty', default=1)
    unit_price = fields.Float(string='Unit Price', related='product_sku_id.selling_price')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_price
