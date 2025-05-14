from odoo import models, fields, api, _
from odoo.exceptions import UserError


class BankReceipt(models.Model):
    _name = 'bank.receipt'
    _description = 'Bank Receipt'

    name = fields.Char(string='Receipt Reference', required=True, copy=False, readonly=True,
                       default=lambda self: ('New'))
    date = fields.Date(string='Date', default=fields.Date.today, required=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    customer_bank_id = fields.Many2one('res.partner.bank', string='Customer Bank Account', required=True)
    to_partner_id = fields.Many2one('res.partner', string='To Account', required=True)
    to_bank_id = fields.Many2one('res.partner.bank', string='To Bank Account', required=True)
    amount = fields.Monetary(string='Amount', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.company.currency_id)
    payment_type = fields.Selection(
        [('send', 'Send'), ('receive', 'Receive')],
        string='Payment Type',
        required=True,
        default='send'
    )
    journal_id = fields.Many2one('account.journal', string='Journal', required=True)
    remarks = fields.Text(string='Remarks')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('invoice_created', 'Invoice Created'),
        ('posted', 'Posted'),
        ('paid', 'Paid'),
    ], string='Status', default='draft', readonly=True)

    invoice_id = fields.Many2one('account.move', string='Created Invoice', readonly=True)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id and self.partner_id.bank_ids:
            self.customer_bank_id = self.partner_id.bank_ids[0].id
        else:
            self.customer_bank_id = False

    @api.onchange('to_partner_id')
    def _onchange_to_partner_id(self):
        if self.to_partner_id and self.to_partner_id.bank_ids:
            self.to_bank_id = self.to_partner_id.bank_ids[0].id
        else:
            self.to_bank_id = False

    def action_submit(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError("Only draft receipts can be submitted.")
            # Create draft invoice
            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': rec.partner_id.id,
                'invoice_date': rec.date,
                'journal_id': rec.journal_id.id,
                'currency_id': rec.currency_id.id,
                'invoice_origin': rec.name,
                'invoice_line_ids': [
                    (0, 0, {
                        'name': rec.remarks or 'Bank Receipt',
                        'quantity': 1,
                        'price_unit': rec.amount,
                    }),
                ],
            }
            invoice = self.env['account.move'].create(invoice_vals)
            rec.invoice_id = invoice.id
            rec.state = 'invoice_created'

    def action_pay(self):
        for rec in self:
            if not rec.invoice_id:
                raise UserError("No invoice linked to this receipt.")
            invoice = rec.invoice_id
            if invoice.state == 'draft':
                invoice.action_post()  # This generates the invoice number
                rec.state = 'posted'
            # Register payment
            payment_register = self.env['account.payment.register'].with_context(
                active_model='account.move', active_ids=[invoice.id]
            ).create({
                'payment_date': fields.Date.today(),
                'journal_id': rec.journal_id.id,
                'amount': rec.amount,
            })
            payment_register.action_create_payments()
            rec.state = 'paid'
