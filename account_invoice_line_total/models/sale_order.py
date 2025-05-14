from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    invoice_numbers = fields.Char(string="Invoice Numbers", compute='_compute_related_numbers')
    delivery_numbers = fields.Char(string="Delivery Numbers", compute='_compute_related_numbers')
    manufacturing_numbers = fields.Char(string="Manufacturing Orders", compute='_compute_related_numbers')

    @api.depends('invoice_ids', 'order_line')
    def _compute_related_numbers(self):
        for order in self:
            # Invoice Numbers
            invoice_numbers = order.invoice_ids.mapped('name')
            order.invoice_numbers = ', '.join(invoice_numbers) if invoice_numbers else ''

            # Delivery Numbers
            delivery_numbers = self.env['stock.picking'].search([('sale_id', '=', order.id)]).mapped('name')
            order.delivery_numbers = ', '.join(delivery_numbers) if delivery_numbers else ''

            # Manufacturing Orders (MO)
            mo_numbers = self.env['mrp.production'].search([('origin', '=', order.name)]).mapped('name')
            order.manufacturing_numbers = ', '.join(mo_numbers) if mo_numbers else ''
