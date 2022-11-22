from odoo import fields, models, api
from odoo.exceptions import UserError


class ViinCustomer(models.Model):
    _name = 'viin.customer'
    _description = 'Viin Customer'
    name = fields.Char(string = 'Name', required = True, translate = True , help = "Enter the last name")
    image = fields.Image(string = 'Customer image')
    phone = fields.Char(string = 'Phone number', help = "Enter the phone number")
    address = fields.Text(string = 'address', translate = True , help = "Enter the address")
    note = fields.Text(string = 'Note', translate = True)
    
    order_ids = fields.One2many('viin.order', 'customer_id', string = 'orders')
    
    state = fields.Selection(string = 'Status', selection = [('new', 'New'),
                                                         ('vip', 'Vip'),
                                                         ('off', 'Off')], default = 'new')
    
    @api.model
    def is_allowed_state(self, current_state, new_state):
        allowed_states = [('new', 'vip'), ('vip', 'off'), ('off', 'vip'), ('new', 'off')]
        return (current_state, new_state) in allowed_states
    
    def change_customer_state(self, state):
        for customer in self:
            if customer.is_allowed_state(customer.state, state):
                customer.state = state
            else:
                raise UserError("Changing customer status from %s to %s is not allowed." % (customer.state, state))
            
    def change_to_new(self):
        self.change_customer_state('new')

    def change_to_vip(self):
        self.change_customer_state('vip')

    def change_to_off(self):
        self.change_customer_state('off')