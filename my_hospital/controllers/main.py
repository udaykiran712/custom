from odoo import http
from odoo.http import request


class Hospital(http.Controller):
    @http.route('/hospital/patient/', website=True, auth='public')
    def hospital_patient(self, **kwargs):
        # return  "Hello ODOO Mates"

        patients = request.env['hospital.patient'].sudo().search([])
        # Here we are extracting all the info from patient.py
        print("patients - ---", patients)
        return request.render("my_hospital.patients_page", {  # patients_page is the id in template.xml file
            'patients': patients
        })
