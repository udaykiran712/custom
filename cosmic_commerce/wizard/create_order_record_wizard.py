from odoo import api, fields, models, _


class CreateOrderRecordWizard(models.TransientModel):
    _name = 'create.order.record.wizard'
    _description = 'Create Order Record wizard'

    customer_id = fields.Many2one('customer.profile', string="Select Customer", required=True)
    name = fields.Char(related='customer_id.name', string='Customer Name', readonly=False)
    age = fields.Integer(related='customer_id.age', string="Age", readonly=False)
    contact_email = fields.Char(related='customer_id.contact_email', string="Email", readonly=False)
    introduction_text = fields.Html(string='Introduction', compute='_compute_introduction_text')

    def action_create_order_record_appointment(self):

        vals = {
            'buyer_id': self.customer_id.id,
        }
        new_order_record = self.env['order.record'].create(vals)
        print("appointment", new_order_record.id)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'order.record',
            'view_mode': 'form',
            'res_id': new_order_record.id,
            'target': 'new',
            'name': 'Order Details',
        }

    @api.depends('name', 'age')
    def _compute_introduction_text(self):
        for res in self:
            if res.name and res.age:
                res.introduction_text = f"""
                    <div>
                        <h5>Hi, {res.name}</h5>
                        <p>Please create your draft order</p>
                        <p>Please save to confirm your draft order.</p>
                        <p>A Confirmation will be sent to your mail {res.contact_email}. Thank you  </p>
                    </div>
                """
            else:
                res.introduction_text = False

    @api.model
    def default_get(self, fields):
        defaults = super(CreateOrderRecordWizard, self).default_get(fields)
        print("defaults", defaults)

        active_id = self._context.get('active_id')
        print("active_id.......", active_id)
        active_model = self._context.get('active_model')
        print("active_model.......", active_model)


        if active_model == 'customer.profile' and active_id:
            customer = self.env['customer.profile'].browse(active_id)
            defaults['customer_id'] = customer.id

        return defaults
