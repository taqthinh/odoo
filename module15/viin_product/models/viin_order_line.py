from odoo import fields, models


class ViinOrderLine(models.Model):
    _name = 'viin.order.line'
    _description = 'Viin order line'
                
    product_id = fields.Many2one('viin.product', string='Product',required = True)
    number_of_products = fields.Integer(string = 'Number of Products')
    order_id = fields.Many2one('viin.order', string='Order', required=True)
    _sql_constraints = [
        ('check_number_of_products', 'CHECK(number_of_products >= 0)', "The Number of Product must be greater than 0!")
    ]