from odoo import fields, models


class ViinProductAttributeLine(models.Model):
    _name = 'viin.product.attribute.line'
    _description = 'Viin product attribute line'

    name = fields.Char(string = 'Name', translate = True)
    attribute_id = fields.Many2one('viin.product.attribute', string = 'Attribute')
    product_id = fields.Many2one('viin.product', string = 'Product')
    value_ids = fields.Many2many('viin.product.attribute.value', string="Values", domain="[('attribute_id', '=', attribute_id)]")