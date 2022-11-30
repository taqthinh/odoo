from odoo import fields, models


class ViinOrderCancel(models.TransientModel):
    _name = 'viin.order.cancel'
    _description = 'Viin Order cancel'

    def _default_order(self):
        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')
        return self.env[active_model].browse(active_id)

    order_id = fields.Many2one('viin.order', string='order', default=_default_order, required=True)
    dropout_reason = fields.Text(string='Dropout Reason', required=True)

    def action_confirm(self):
        self.order_id.write({
        'dropout_reason': self.dropout_reason,
        'state': 'canceled'
        })
