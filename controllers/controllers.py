# -*- coding: utf-8 -*-
# from odoo import http


# class DailyInventoryPurchaseReport(http.Controller):
#     @http.route('/daily_inventory_purchase_report/daily_inventory_purchase_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/daily_inventory_purchase_report/daily_inventory_purchase_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('daily_inventory_purchase_report.listing', {
#             'root': '/daily_inventory_purchase_report/daily_inventory_purchase_report',
#             'objects': http.request.env['daily_inventory_purchase_report.daily_inventory_purchase_report'].search([]),
#         })

#     @http.route('/daily_inventory_purchase_report/daily_inventory_purchase_report/objects/<model("daily_inventory_purchase_report.daily_inventory_purchase_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('daily_inventory_purchase_report.object', {
#             'object': obj
#         })
