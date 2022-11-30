from odoo import fields, models


class ViinProductAttribute(models.Model):
    _name = 'viin.product.attribute'
    _description = 'Viin product attribute'

    name = fields.Char(string='Name', required=True, translate=True , help="Enter the attribute name")
    value_ids = fields.One2many('viin.product.attribute.value', 'attribute_id', string='Values')
    attribute_line_ids = fields.One2many('viin.product.attribute.line','attribute_id' ,string='Products attribute line')

    