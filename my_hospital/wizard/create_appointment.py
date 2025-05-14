from odoo import api, fields, models, _


class CreateAppointmentWizard(models.TransientModel):
    _name = 'create.appointment.wizard'
    _description = 'Create Appointment wizard'

    date_appointment = fields.Date(string="Date", required=False)
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)

    def action_create_appointment(self):
        print("Button is Clicked")
        vals = {
            'patient_id': self.patient_id.id,
            'date_appointment': self.date_appointment
        }
        # keys are the fields names in hospital.appointment and values are fileds of  create.appointment.wizard
        appointment_rec = self.env['hospital.appointment'].create(vals)
        print("appointment", appointment_rec.id)
        return {
            'name': _('Appointment'),  # any name
            'view_mode': 'form',
            'res_model': 'hospital.appointment',  # which model u want to open when we click this button
            'res_id': appointment_rec.id,
            'target': 'new',  # If you want open it as a popup if we delete this it will open in a new page
            'type': 'ir.actions.act_window',
        }

