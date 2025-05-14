from odoo import api, fields, models, _

class SearchAppointmentWizard(models.TransientModel):
    _name = "search.appointment.wizard"
    _description = "Search Appointment Wizard"

    patient_id = fields.Many2one('hospital.patient', string="Patient" , required = True)

    def action_search_appointment_m1(self):
        action = self.env.ref('my_hospital.action_hospital_appointment').read()[0]
        action['domain'] = [('patient_id', '=', self.patient_id.id)]
        return action

    def action_search_appointment_m2(self):
        action = self.env["ir.actions.actions"]._for_xml_id("my_hospital.action_hospital_appointment")
        action['domain'] = [('patient_id', '=', self.patient_id.id)]
        return action

    def action_search_appointment_m3(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',  # any name
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hospital.appointment',  # which model u want to open when we click this button
            'target': 'current',
            'domain': [('patient_id', '=', self.patient_id.id)]
        }
