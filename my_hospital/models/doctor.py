from odoo import api, fields, models, _


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = "Hospital Doctor"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "doctor_name"

    doctor_name = fields.Char(string="Name", required=True, tracking=True)
    age = fields.Integer(string="Age", tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], required=True, default='male', tracking=True)
    note = fields.Text(string="Description")
    image = fields.Binary(string="Patient Image")
