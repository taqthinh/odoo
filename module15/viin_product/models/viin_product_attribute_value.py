from odoo import fields, models


class ViinProductAttributeValue(models.Model):
    _name = 'viin.product.attribute.value'
    _description = 'Viin product attribute value'

    name = fields.Char(string = 'Name', translate = True)
    attribute_id = fields.Many2one('viin.product.attribute', string = 'Attribute')
    attribute_line_ids = fields.Many2many('viin.product.attribute.line', string="Lines")