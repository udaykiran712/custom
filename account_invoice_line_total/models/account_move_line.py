from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    line_total_with_tax = fields.Monetary(
        string="Total Amount",
        compute='_compute_line_total_with_tax',
        currency_field='currency_id',
        store=True
    )

    @api.depends('price_subtotal', 'tax_ids', 'quantity', 'price_unit')
    def _compute_line_total_with_tax(self):
        for line in self:
            taxes = line.tax_ids.compute_all(
                line.price_unit,
                line.currency_id,
                line.quantity,
                product=line.product_id,
                partner=line.move_id.partner_id
            )
            line.line_total_with_tax = taxes['total_included']
