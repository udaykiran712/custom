from odoo import api, fields, models, _


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"
    _order = 'name desc'

    name = fields.Char(string="Order Reference", required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    patient_name = fields.Char(related='patient_id.name', string="Patient", required=True)
    patient_reference = fields.Char(related='patient_id.reference', string="Patient", required=True)
    age = fields.Integer(string="Age", related='patient_id.age', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True)

    note = fields.Text(string="Description")
    prescription = fields.Text(string="Prescription")

    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')], default='draft',
        string="Status", tracking=True)
    date_appointment = fields.Date(string="Date")
    date_checkup = fields.Datetime(string="Check Up Time")
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=True)
    prescription_line_ids = fields.One2many('', '', string="Prescription Lines")

    def action_confirm(self):
        self.state = 'confirm'

        # #odoo search method
        # patients  = self.env['hospital.patient'].search([])
        # print("patients...", patients)
        # 
        # # search with filter
        # female_patients  = self.env['hospital.patient'].search([('gender', '=' ,'female')])
        # print("female_patients...", female_patients)
        # 
        # #search with and operation
        # female_patients_above_age  = self.env['hospital.patient'].search([('gender', '=' ,'female'),('age', '>' ,10)])
        # print("female_patients above 10...", female_patients_above_age)
        # 
        # #search with or operation
        # female_patients_or_age  = self.env['hospital.patient'].search(['|', ('gender', '=' ,'female'),('age', '>' ,10)])
        # print("female_patients or  10 age ...", female_patients_or_age)
        # 
        # male_patients  = self.env['hospital.patient'].search([('gender', '=' ,'male'),('age', '>' ,10)])
        # print("male_patients...", male_patients)

        # odoo search count
        # patients_count = self.env['hospital.patient'].search_count([])
        # print("patients_count...", patients_count)

        # browse 

        # browse_result = self.env['hospital.patient'].browse([4])
        # browse_results = self.env['hospital.patient'].search([('id','=',4)])
        # print(browse_result)
        # print(browse_results)

        # #exists
        # if browse_result.exists():
        #     print("Existing")
        # else:
        #     print("Non-Existing")

        # vals = {
        #     'name':'Rahul',
        #     'age':20
        # }
        # created_record = self.env['hospital.patient'].create(vals)
        # print("created_record",created_record)

        # write method

        # record_to_update = self.env['hospital.patient'].browse(3)
        # if record_to_update.exists():
        #     vals = {
        #         'age': 20,
        #         'note':'Cough'
        #     }
        #     record_to_update.write(vals)

        # copy method

        # record_to_copy = self.env['hospital.patient'].browse(3)
        # record_to_copy.copy()

        # unlink

        # record_to_delete = self.env['hospital.patient'].browse(13)
        # record_to_delete.unlink()

        # patient = self.env['hospital.patient'].search([('id','=',4)])
        # print("patient_name",patient.name)
        # print("patient_name",patient.age)

        # display_name

        # print("Display Name...", patient.display_name)

        # name_get

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s - %s' % (rec.patient_reference, rec.patient_id)))
        return res

    def action_done(self):
        self.state = 'done'

    def action_set_to_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Patient'
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        # 'hospital.appointment' is the code name given in data.xml
        res = super(HospitalAppointment, self).create(vals)
        return res

    # if you want to give multiple id fields below , give by comma(,)
    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            if self.patient_id.gender:
                self.gender = self.patient_id.gender
            if self.patient_id.note:
                self.note = self.patient_id.note
        else:
            self.gender = ""
            self.note = ""


class AppointmentPrescriptionLines(models.Model):
    _name = "hospital.prescription.lines"
    _description = "Appointment Prescription Lines"

    name = fields.Char(string="Medicine")
    qty = fields.Integer(string="Quantity")
