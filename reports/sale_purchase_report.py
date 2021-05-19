import datetime

from odoo import models


class SalePurchaseReportXlsx(models.AbstractModel):
    # _name = 'report.module_name.report_name' Here report name should be the name of report that
    # is define in report.xml file at name section
    _name = 'report.daily_inventory_purchase_report.sale_purchase_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        for obj in lines:
            sheet = workbook.add_worksheet(f'daily_inventory_purchase_report_from_{obj.start_date}_to_{obj.end_date}')
            bold = workbook.add_format({'bold': True})
            products = self.env['product.product'].search([('product_tmpl_id.type', '=', 'product')])
            sheet.write(0, 0, 'Product Name', bold)
            sheet.write(0, 1, 'Inventory', bold)
            sheet.write(0, 2, 'Purchased quantity', bold)
            sheet.write(0, 3, 'Sale quantity', bold)
            sheet.write(0, 4, 'Previous inventory', bold)
            row = 1
            for product in products:
                lot_id = product._context.get('lot_id')
                owner_id = product._context.get('owner_id')
                package_id = product._context.get('package_id')
                present_inventory = product._compute_quantities_dict(lot_id, owner_id, package_id, obj.start_date,
                                                                     obj.end_date + datetime.timedelta(days=1))[
                    product.id]['qty_available']
                previous_inventory = product._compute_quantities_dict(lot_id, owner_id, package_id, to_date=(
                        obj.start_date))[product.id]['qty_available']

                purchased_quantity = \
                    product._compute_date_range_purchased_product_qty(obj.start_date, obj.end_date)[product.id][
                        'date_range_purchase_quantity']
                sale_quantity = product._compute_date_range_sales_count(obj.start_date, obj.end_date)[product.id][
                    'date_range_sale_quantity']
                sheet.write(row, 0, product.product_tmpl_id.name)
                sheet.write(row, 1, present_inventory)
                sheet.write(row, 2, purchased_quantity)
                sheet.write(row, 3, sale_quantity)
                sheet.write(row, 4, previous_inventory)
                row += 1
