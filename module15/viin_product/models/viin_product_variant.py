from odoo import fields, models


class ViinProductVariant(models.Model):
    _name = 'viin.product.variant'
    _description = 'Viin product variant'

    product_id = fields.Many2one('viin.product', string = 'Product')
