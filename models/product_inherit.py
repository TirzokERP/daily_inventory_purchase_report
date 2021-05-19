from datetime import timedelta

from odoo import fields, models
from odoo.tools import float_round


class ProductInherit(models.Model):
    _inherit = 'product.product'

    def _compute_date_range_purchased_product_qty(self, from_date=None, to_date=None):
        date_from = fields.Datetime.to_string(fields.datetime.now() - timedelta(days=365))
        domain = [
            ('state', 'in', ['purchase', 'done']),
            ('product_id', 'in', self.ids)
        ]
        if from_date:
            domain.append(('date_order', '>=', from_date))
        else:
            domain.append(('date_order', '>=', date_from))
        if to_date:
            domain.append(('date_order', '<=', to_date))

        # order_lines = self.env['purchase.order.line'].search(domain)
        order_lines = self.env['purchase.order.line'].read_group(domain, ['product_id', 'product_uom_qty'], ['product_id'])
        purchased_data = dict([(data['product_id'][0], data['product_uom_qty']) for data in order_lines])
        res = dict()
        for product in self:
            res[product.id] = {}
            if not product.id:
                res[product.id]['date_range_purchase_quantity'] = 0.0
                continue
            res[product.id]['date_range_purchase_quantity'] = float_round(purchased_data.get(product.id, 0), precision_rounding=product.uom_id.rounding)
        return res

    def _compute_date_range_sales_count(self, from_date=None, to_date=None):
        r = {}
        res = {}
        self.sales_count = 0
        date_from = fields.Datetime.to_string(fields.datetime.now() - timedelta(days=365))

        done_states = self.env['sale.report']._get_done_states()

        domain = [
            ('state', 'in', done_states),
            ('product_id', 'in', self.ids)
        ]

        if from_date:
            domain.append(('date', '>=', from_date))
        else:
            domain.append(('date', '>=', date_from))
        if to_date:
            domain.append(('date', '<=', to_date))

        for group in self.env['sale.report'].read_group(domain, ['product_id', 'product_uom_qty'], ['product_id']):
            r[group['product_id'][0]] = group['product_uom_qty']
        for product in self:
            res[product.id] = {}
            if not product.id:
                res[product.id]['date_range_sale_quantity'] = 0.0
                continue
            res[product.id]['date_range_sale_quantity'] = float_round(r.get(product.id, 0), precision_rounding=product.uom_id.rounding)
        return res
