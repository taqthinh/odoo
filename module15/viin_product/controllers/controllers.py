# -*- coding: utf-8 -*-
import json

from odoo import http
from odoo.addons.test_convert.tests.test_env import data
from odoo.http import request
from odoo.tools import date_utils

response = {
    "status":"1",
    "message":'success',
    "data": ''
    }


class ViinProduct(http.Controller):

    @http.route('/viin_product/login', type = 'json', auth = 'none')
    def authenticate(self, db, login, password, base_location = None):
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()

    @http.route('/viin_product/get_products', type = 'json', auth = 'user')
    def get_products(self, **kw):
        products = request.env['viin.product'].search([], limit = 8)
        data_string = json.dumps(products.read([]), indent = 4, sort_keys = True, default = str)
        try:
            return json.loads(data_string)
        except:
            return {
                "status":0,
                "message":'err'
                }

    @http.route('/viin_product/get_product_codes', type = 'json', auth = 'user')
    def get_product_codes(self, **kw):
        products = request.env['viin.product'].search([])
        response['data'] = products.mapped('product_code')
        try:
            return response
        except:
            return {
                "status":0,
                "message":'err'
                }

    @http.route('/viin_product/sort_products', type = 'json', auth = 'user')
    def sort_products(self, **kw):
        products = request.env['viin.product'].search([])
        products.sorted(key=lambda r: r[kw['type']])
        response['data'] = products.read([])
        try:
            return response
        except:
            return {
                "status":0,
                "message":'err'
                }
    @http.route('/viin_product/get_product_ids', type = 'json', auth = 'user')
    def get_product_ids(self, **kw):
        products = request.env['viin.product'].search([])
        response['data'] = products.ids
        try:
            return response
        except:
            return {
                "status":0,
                "message":'err'
                }

    @http.route('/viin_product/get_total_products', type = 'json', auth = 'user')
    def get_total_products(self, **kw):
        total = request.env['viin.product'].search_count([('price', '>', 0.0)])
        response['data'] = {
                "total":total
            }
        try:
            return response
        except:
            return {
                "status":0,
                "message":'err'
                }

    @http.route('/viin_product/get_products_default_rating', type = 'json', auth = 'user')
    def get_products_default_rating(self, **kw):
        fields_list = request.env['viin.product'].default_get(['rating'])
        return fields_list

    @http.route('/viin_product/get_product', type = 'json', auth = 'user')
    def get_product(self, **kw):
        product = request.env['viin.product'].browse(kw['id'])
        data_string = json.dumps(product.read(), indent = 4, sort_keys = True, default = str)
        try:
            return json.loads(data_string)
        except:
            return {
                "status":0,
                "message":'err'
                }

    @http.route('/viin_product/copy_product', type = 'json', auth = 'user')
    def copy_product(self, **kw):
        product = request.env['viin.product'].browse(kw['id'])
        res = product.copy({"name":'new name'})
        return res

    @http.route('/viin_product/create_product', type = 'json', auth = 'user')
    def create_product(self, **kw):
        try:
            data = request.env['viin.product'].create({
                    'name': kw['name'],
                    'price': kw['price'],
                    'note': kw['note'],
                    'attribute_ids': [1, 2],
                    'company_id':kw['company_id']
                    })
            response['data'] = data[0].read()
            return response
        except NameError as e:
            return e

    @http.route('/viin_product/update_product', type = 'json', auth = 'user')
    def update_product(self, **kw):
        try:
            product = request.env['viin.product'].browse(kw['id'])
            data = product.write({
                    'name': kw['name'],
                    'price': kw['price'],
                    'note': kw['note'],
                    })
            return data
        except NameError as e:
            return e

    @http.route('/viin_product/delete_product', type = 'json', auth = 'user')
    def delete_product(self, **kw):
        try:
            product = request.env['viin.product'].browse(kw['id'])
            res = product.unlink()
            response['data'] = res
            return response
        except NameError as e:
            return e

    @http.route('/viin_product/create_product_by_name', type = 'json', auth = 'user')
    def create_product_by_name(self, **kw):
        try:
            data = request.env['viin.product'].name_create({'name': kw['name']})
            response['data'] = data
            return response
        except:
            return {
                "status":0,
                "message": ''
                }
