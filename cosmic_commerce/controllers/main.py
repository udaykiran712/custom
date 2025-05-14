from odoo import http
from odoo.http import request
import random

class CosmicWebsite(http.Controller):

    @http.route('/', auth='public', website=True)
    def homepage(self, **kwargs):
        total_customers = request.env['customer.profile'].search_count([])
        total_orders = request.env['order.record'].search_count([])
        vip_customers = request.env['customer.profile'].search_count([('category_labels_id.name', '=', 'VIP Customer')])
        return request.render('cosmic_commerce.homepage_template', {
            'total_customers': total_customers,
            'total_orders': total_orders,
            'vip_customers': vip_customers
        })

    @http.route('/about', auth='public', website=True)
    def about(self, **kwargs):
        total_customers = request.env['customer.profile'].search_count([])
        random_index = random.randint(0, total_customers - 1)
        me = request.env['customer.profile'].search([], limit=1, offset=random_index)
        return request.render('cosmic_commerce.about_template', {'me': me})

    @http.route('/projects', auth='public', website=True)
    def projects(self, **kwargs):
        orders = request.env['order.record'].search([], order='order_date desc', limit=3)
        return request.render('cosmic_commerce.projects_template', {'orders': orders})

    @http.route('/vip-customers', auth='public', website=True)
    def vip_customers(self, **kwargs):
        vip_tag = request.env['tag.label'].search([('name', '=', 'VIP Customer')], limit=1)
        customers = request.env['customer.profile'].search([('category_labels_id', 'in', [vip_tag.id])])
        return request.render('cosmic_commerce.vip_customers_template', {'customers': customers})