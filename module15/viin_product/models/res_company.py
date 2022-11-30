import json

from odoo import  fields, models, api


class ResCompany(models.Model):
    _inherit = "res.company"
    
    note = fields.Text(string = 'Note')
    
    @api.model
    def create(self, vals):
        if 'phone' in vals:
            vals['name'] = vals['name'].upper()
            return super(ResCompany, self).create(vals)
