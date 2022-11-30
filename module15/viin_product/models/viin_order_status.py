from odoo import fields, models, api


class ViinOrderStatus(models.Model):
    _name = 'viin.order.status'
    _description = 'Viin order status'
                
    note = fields.Text(string = 'Order note', translate = True)
    order_id = fields.Many2one('viin.order', string = 'Order', required = True)
    
