from odoo import api, fields, models, _
from datetime import datetime

from pydoc import browse

import logging

_logger = logging.getLogger(__name__)


class CustomerProfile(models.Model):
    _name = 'customer.profile'
    _description = 'Customer Profile'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Customer Name', help='The name of the customer', required=True)
    contact_email = fields.Char(string='Email')
    mobile_number = fields.Integer(string='Mobile Number')
    note = fields.Text(string="Description")
    age = fields.Integer(string="Age")
    date_start = fields.Date()
    birth_year = fields.Integer(string="Birth Year", compute='_compute_birth_year')
    category_labels_id = fields.Many2many('tag.label', 'customer_label_tag', 'customer_id', 'tag_id',
                                          string='Customer Tags')
    order_count = fields.Integer(string="Total Orders", compute='_compute_order_count')
    total_spent = fields.Float("Total Spent")

    def _compute_order_count(self):
        for customer in self:
            customer.order_count = self.env['order.record'].search_count([('buyer_id', '=', customer.id)])

    def action_view_orders(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Orders'),
            'res_model': 'order.record',
            'view_mode': 'list,form',
            'domain': [('buyer_id', '=', self.id)],
            'context': {'default_buyer_id': self.id},
        }

    def action_open_appointment_wizard(self):
        return {
            'name': 'Create a Draft Order',
            'type': 'ir.actions.act_window',
            'res_model': 'create.order.record.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_name': self.name,
                'default_age': self.age,
                'default_customer_id': self.id,
            },
        }

    def action_check(self):
        # ORM Method
        # customers = self.env['customer.profile'].search([])
        customers_search = self.env['customer.profile'].search([('age', '>', 0)], order='age', limit=5)
        data = customers_search.read(['name'])
        print(data)
        print(customers_search)
        customers_count = self.env['customer.profile'].search_count([])
        print(customers_count)
        browse_customers = self.env['customer.profile'].browse([10])
        print(browse_customers)
        if browse_customers.exists():
            print("Exists")
        else:
            print("Does not exists")

        vals = {'name': 'Anil', 'age': 28}
        # create_customer = self.env['customer.profile'].create(vals)

        # if browse_customers.exists():
        #     vals = {'name': 'Anil',
        #             'age': 28
        #             }
        #     self.env['customer.profile'].write(vals)

        # record_to_copy = self.env['customer.profile'].browse(9)
        # if record_to_copy.exists():
        #     # record_to_copy.copy({'name': record_to_copy.name})
        #     print('Copied')
        # else:
        #     print("Customer not found")
        #
        # record_to_copy.unlink()

        return {
            'name': _('Customers'),
            'view_mode': 'list',
            'res_model': 'customer.profile',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', customers_search.ids)]
        }

    @api.model
    def create(self, vals):
        if not vals.get('contact_email'):
            name = vals.get('name')
            age = vals.get('age')
            vals['contact_email'] = '{}{}@gmail.com'.format(name, age)
        res = super(CustomerProfile, self).create(vals)
        return res

    @api.depends('age')
    def _compute_birth_year(self):
        current_year = 2025
        for record in self:
            if record.age:
                record.birth_year = current_year - record.age
            else:
                record.birth_year = 0

    def action_mark_old_customers_vip(self):
        for record in self:
            vip_tag = self.env['tag.label'].search([('name', '=', 'VIP Customer')], limit=1)
            if not vip_tag:
                vip_tag = self.env['tag.label'].create({'name': 'VIP Customer'})

            if record.age and record.age > 60:
                if vip_tag not in record.category_labels_id:
                    record.category_labels_id = [(4, vip_tag.id)]
                    # 4 - Links an existing record with the specified id to the current record
                    # self.env.logger.info(f"Customer {record.name} marked as VIP.")
            else:
                if vip_tag in record.category_labels_id:
                    record.category_labels_id = [(3, vip_tag.id)]
                    # 3 -  Unlinks the related record with the specified id from the current record
                    # self.env.logger.info(f"VIP tag removed from customer {record.name} as age is no longer > 60.")

        return {}

    def _log_every_minute(self):
        _logger.info("Cosmic Commerce: This cron job ran!")
        print("This is a debug message: Cron has been triggered!")

    @api.model
    def _cron_update_customer_note_minute(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        customers = self.env['customer.profile'].search([])
        for customer in customers:
            new_note = f"Updated at : {current_time}"
            customer.write({'note': new_note})
            _logger.info(f"Updated note for customer '{customer.name}' at  {current_time}")

    def _set_vip_tag(self):
            vip_tag = self.env['tag.label'].search([('name', '=', 'VIP')], limit=1)
            if not vip_tag:
                vip_tag = self.env['tag.label'].create({'name': 'VIP'})
            for rec in self:
                if rec.total_spent >= 10000:
                    rec.category_labels_id = [(4, vip_tag.id)]