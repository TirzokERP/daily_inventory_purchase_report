import datetime
from io import BytesIO

import xlsxwriter

from odoo import models


class SalePurchaseReportXlsx(models.AbstractModel):
    # _name = 'report.module_name.report_name' Here report name should be the name of report that
    # is define in report.xml file at name section
    _name = 'report.daily_inventory_purchase_report.sale_purchase_report'
    _inherit = 'report.report_xlsx.abstract'

    def add_workbook_format(self, workbook):
        colors = {
            'white_orange': '#FFFFDB',
            'orange': '#FFC300',
            'red': '#FF0000',
            'yellow': '#F6FA03',
        }

        wbf = {}
        wbf['header'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': '#FFFFDB', 'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header'].set_border()

        wbf['header_orange'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['orange'], 'font_color': '#000000',
             'font_name': 'Georgia'})
        wbf['header_orange'].set_border()

        wbf['header_yellow'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': colors['yellow'], 'font_color': '#000000',
             'font_name': 'Georgia'})
        wbf['header_yellow'].set_border()

        wbf['header_no'] = workbook.add_format(
            {'bold': 1, 'align': 'center', 'bg_color': '#FFFFDB', 'font_color': '#000000', 'font_name': 'Georgia'})
        wbf['header_no'].set_border()
        wbf['header_no'].set_align('vcenter')

        wbf['footer'] = workbook.add_format({'align': 'left', 'font_name': 'Georgia'})

        wbf['content_datetime'] = workbook.add_format({'num_format': 'yyyy-mm-dd hh:mm:ss', 'font_name': 'Georgia'})
        wbf['content_datetime'].set_left()
        wbf['content_datetime'].set_right()

        wbf['content_date'] = workbook.add_format({'num_format': 'yyyy-mm-dd', 'font_name': 'Georgia'})
        wbf['content_date'].set_left()
        wbf['content_date'].set_right()

        wbf['title_doc'] = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 20,
            'font_name': 'Georgia',
            'font_color': '#FDFEFE',
            'bg_color': '#27AE60 '
        })

        wbf['company'] = workbook.add_format({'align': 'left', 'font_name': 'Georgia'})
        wbf['company'].set_font_size(11)

        wbf['content'] = workbook.add_format()
        wbf['content'].set_left()
        wbf['content'].set_right()

        wbf['content_float'] = workbook.add_format({'align': 'right', 'num_format': '#,##0.00', 'font_name': 'Georgia'})
        wbf['content_float'].set_right()
        wbf['content_float'].set_left()

        wbf['content_number'] = workbook.add_format({'align': 'right', 'num_format': '#,##0', 'font_name': 'Georgia'})
        wbf['content_number'].set_right()
        wbf['content_number'].set_left()

        wbf['content_percent'] = workbook.add_format({'align': 'right', 'num_format': '0.00%', 'font_name': 'Georgia'})
        wbf['content_percent'].set_right()
        wbf['content_percent'].set_left()

        wbf['total_number'] = workbook.add_format(
            {'align': 'right', 'bg_color': colors['white_orange'], 'bold': 1, 'num_format': '#,##0',
             'font_name': 'Georgia'})
        wbf['total_number'].set_top()
        wbf['total_number'].set_bottom()
        wbf['total_number'].set_left()
        wbf['total_number'].set_right()

        return wbf, workbook

    def generate_xlsx_report(self, workbook, data, lines):
        wbf, workbook = self.add_workbook_format(workbook)
        for obj in lines:
            reoport_name = ''
            if obj.start_date == obj.end_date:
                report_name = f'Sales, purchase and inventory report of {obj.start_date}'
            else:
                report_name = f'Sales, purchase and inventory report from {obj.start_date} to {obj.end_date}'
            sheet = workbook.add_worksheet(report_name)
            sheet.merge_range('A1:G3', report_name, wbf['title_doc'])
            if obj.location_ids:
                query = f"""
                           SELECT
                            prod.id
                            FROM
                                stock_quant quant
                            LEFT JOIN
                                stock_location loc on loc.id=quant.location_id
                            LEFT JOIN
                                product_product prod on prod.id=quant.product_id
                            LEFT JOIN
                                product_template prod_tmpl on prod_tmpl.id=prod.product_tmpl_id
                            where prod_tmpl.type = 'product' and loc.id in ({','.join(map(str, obj.location_ids.ids))})
                        """
                self._cr.execute(query)
                product_ids = [item[0] for item in self._cr.fetchall()]
                products = self.env['product.product'].search([('id', 'in', product_ids)])
            else:
                products = self.env['product.product'].search([('product_tmpl_id.type', '=', 'product')])

            sheet.set_column(0, 0, 30)
            sheet.set_column(1, 4, 20)

            sheet.write(4, 0, 'Product Name', wbf['header'])
            sheet.write(4, 1, 'Inventory', wbf['header'])
            sheet.write(4, 2, 'Purchased quantity', wbf['header'])
            sheet.write(4, 3, 'Sale quantity', wbf['header'])
            sheet.write(4, 4, 'Previous inventory', wbf['header'])
            row = 5

            total_present_inventory = 0
            total_purchase_quantity = 0
            total_sale_quantity = 0
            total_previous_inventory = 0

            for product in products:
                lot_id = product._context.get('lot_id')
                owner_id = product._context.get('owner_id')
                package_id = product._context.get('package_id')
                present_inventory = product.with_context(location=obj.location_ids.ids) \
                    ._compute_quantities_dict(lot_id, owner_id, package_id, obj.start_date,
                                              obj.end_date + datetime.timedelta(days=1))[product.id]['qty_available']
                previous_inventory = \
                    product.with_context(location=obj.location_ids.ids)._compute_quantities_dict(lot_id, owner_id,
                                                                                             package_id,
                                                                                             to_date=(obj.start_date))[
                        product.id]['qty_available']

                purchased_quantity = \
                    product._compute_date_range_purchased_product_qty(obj.start_date, obj.end_date)[product.id][
                        'date_range_purchase_quantity']
                sale_quantity = product._compute_date_range_sales_count(obj.start_date, obj.end_date)[product.id][
                    'date_range_sale_quantity']

                # Total calculation
                total_purchase_quantity += purchased_quantity
                total_sale_quantity += sale_quantity
                total_previous_inventory += previous_inventory
                total_present_inventory += present_inventory
                # -------------------------
                sheet.write(row, 0, product.product_tmpl_id.name, wbf['content'])
                sheet.write(row, 1, present_inventory, wbf['content_number'])
                sheet.write(row, 2, purchased_quantity, wbf['content_number'])
                sheet.write(row, 3, sale_quantity, wbf['content_number'])
                sheet.write(row, 4, previous_inventory, wbf['content_number'])
                row += 1

            # Total calculation row
            next_row = row + 1
            sheet.write(next_row, 0, 'Total', wbf['total_number'])
            sheet.write(next_row, 1, total_present_inventory, wbf['total_number'])
            sheet.write(next_row, 2, total_purchase_quantity, wbf['total_number'])
            sheet.write(next_row, 3, total_sale_quantity, wbf['total_number'])
            sheet.write(next_row, 4, total_previous_inventory, wbf['total_number'])

        workbook.close()
