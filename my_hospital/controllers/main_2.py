from odoo import http
from odoo.http import request


class PatientDetails(http.Controller):

    @http.route('/contactus', website=True, auth='public')
    def patient_details(self):
        # patients = request.env['hospital.patient'].sudo().search([])
        # Here we are extracting all the info from patient.py
        # print("patients - ---", patients)
        return request.render("my_hospital.patients_details_page", {  # patients_page is the id in template.xml file
            # 'patients': patients
        })
