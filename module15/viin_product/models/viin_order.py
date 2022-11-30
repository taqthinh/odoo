from odoo import fields, models, api
from odoo.exceptions import UserError


class ViinOrder(models.Model):
    _name = 'viin.order'
    _description = 'Viin order'
    _rec_name = 'order_code'
                
    order_code = fields.Char(string = 'Order Code', readonly = True, compute = '_compute_code', store = True)
    note = fields.Text(string = 'Order note', translate = True)
    note_uper = fields.Text(string = 'Order note uper', translate = True)
    total_price = fields.Monetary(string = 'Total price', compute = '_compute_total_price',
                     store = True,
                     compute_sudo = True)
    currency_id = fields.Many2one('res.currency', string = 'Currency', default = lambda self: self.env.company.currency_id.id,)
    customer_id = fields.Many2one('viin.customer', string = 'Customer', required = True)
    order_line_ids = fields.One2many('viin.order.line', 'order_id', string = 'Order')
    order_status_ids = fields.One2many('viin.order.status', 'order_id', string = 'Orders')
    state = fields.Selection(string = 'Status', selection = [('wait_for_confirmation', 'wait for confirmation'),
                                                         ('confirmed', 'Confirmed'),
                                                         ('delivering', 'Delivering'),
                                                         ('completed', 'Completed'),
                                                         ('canceled', 'Canceled'),
                                                         ], default = 'wait_for_confirmation')
    dropout_reason = fields.Text(string = 'Dropout Reason')

    @api.depends('order_line_ids')
    def _compute_total_price(self):
        for r in self:
            if r.order_line_ids:
                total = 0
                for p in r.order_line_ids:
                    total += p.product_id.price * p.number_of_products
                r.total_price = total
            else:
                r.total_price = 0

    @api.onchange('note')
    def _uper_note(self):
        for r in self:
            if r.note:
                r.note_uper = r.note.upper()
    
    @api.depends('order_line_ids')
    def _compute_code(self):
        last_id = self.env['viin.order'].search([])[-1].id
        self.order_code = 'OD' + str(last_id + 1)
        
    @api.model
    def is_allowed_state(self, current_state, new_state):
        allowed_states = [('wait_for_confirmation', 'confirmed'), ('confirmed', 'delivering'), ('delivering', 'completed'), ('wait_for_confirmation', 'canceled'), ('confirmed', 'canceled')]
        return (current_state, new_state) in allowed_states
    
    def change_state(self, state):
        for order in self:
            if order.is_allowed_state(order.state, state):
                order.state = state
            else:
                raise UserError("Changing order status from %s to %s is not allowed." % (order.state, state))
    
    def change_to_confirmed(self):
        self.change_state('confirmed')
    
    def change_to_delivering(self):
        self.change_state('delivering')
    
    def change_to_completed(self):
        self.change_state('completed')
    
    def change_to_canceled(self):
        for order in self:
            if order.is_allowed_state(order.state, 'canceled'):
                return self.env.ref('viin_product.viin_order_cancel_action').read()[0]
            else:
                raise UserError("Changing order status from %s to %s is not allowed." % (order.state, 'canceled'))
