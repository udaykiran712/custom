from odoo import models, fields

class TagLabel(models.Model):
    _name = 'tag.label'
    _description = 'Customer Tag'

    name = fields.Char(string='Tag Name', required=True)
