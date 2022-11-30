from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ViinCategory(models.Model):
    _name = 'viin.category'
    _description = 'Viin category'
    _parent_store = True
    _parent_name = "parent_id"
    
    def _default_date(self):
        return fields.Date.today()
            
    name = fields.Char(string = 'Category Name', required = True, translate = True , help = "Enter the category name")
    category_code = fields.Char(string = 'category Code', compute = '_compute_code', groups = 'viin_category.viin_category_group_admin',
                     store = True)
    note = fields.Text(string = 'category note', translate = True)
    image = fields.Image(string = 'category Image')
    parent_id = fields.Many2one('viin.category', string = 'Parent Group', ondelete = 'restrict')
    product_ids = fields.Many2many('viin.product', string = 'Products')
    parent_path = fields.Char(index = True, readonly = True)
    
    @api.depends('name')
    def _compute_code(self):
        for r in self:
            if r.id:
                r.category_code = 'SP' + str(r.id)
            else:
                r.category_code = 'SP#'
                
    @api.depends_context('status_customer')
    def _change_status(self):
        print('change')
        pass
                
    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise ValidationError('Error! You cannot create recursivecategories.')
        
    @api.model
    def create(self, vals):
        if 'name' in vals:
            vals['name'] = vals['name'].upper()
            return super(ViinCategory, self).create(vals)
    
    @api.model_create_multi
    def create_multi(self, vals):
        if 'name' in vals:
            vals['name'] = vals['name'].lower() + '_by_api'
            return super(ViinCategory, self).create(vals)
