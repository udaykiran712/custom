from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'


    name = fields.Char(string="Name", required=True, tracking=True)
    reference = fields.Char(string="Order Reference", required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    age = fields.Integer(string="Age", tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male', tracking=True)
    note = fields.Text(string="Description")
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')], default='draft',
        string="Status", tracking=True)
    responsible_id = fields.Many2one('res.partner', string="Responsible")
    # res.partner is the model name for getting the customers
    appointment_count = fields.Integer(string="Total Appointments", compute='_compute_appointment_count')
    image = fields.Binary(string="Patient Image")

    def _compute_appointment_count(self):
        print("self.....", self)
        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            print(appointment_count)
            rec.appointment_count = appointment_count

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_set_to_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    @api.model
    def create(self, vals_list):
        if not vals_list.get('note'):
            vals_list['note'] = "New Patient"

        if vals_list.get('reference', _('New')) == _('New'):
            vals_list['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
            # hospital.patient is the code given in data.xml file.
            # The if statement is optional, better to have it code readability.
        res = super(HospitalPatient, self).create(vals_list)
        # print("Successfully over ride create method")
        # print("res",res)
        # print("vals_list",vals_list)
        return res

    # HospitalPatient is the class name
    #
    # @api.model
    # def default_get(self, fields):
    #     result = super(HospitalPatient, self).default_get(fields)
    #     # In result it will have all the default key value pairs defined in the model
    #     result['gender'] = 'female'
    #     print("Overided", fields)
    #     return result
    #
    @api.constrains('name')
    def check_name(self):
        for rec in self:
            patients = self.env['hospital.patient'].search([('name', '=', rec.name), ('id', '!=', rec.id)])
            if patients:
                raise ValidationError(_("Name %s Already Exists" % rec.name))

    @api.constrains('age')
    def check_age(self):
        for rec in self:
            if rec.age <= 0:
                raise ValidationError("Age Should be greater than 0")



    _sql_constraints = [
        ('unique_name', 'unique (name)', 'Patient name must be unique!'),
        ('check_age', 'check (age > 0)', 'Age must be greater than 0!'),
    ]

