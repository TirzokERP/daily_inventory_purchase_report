from odoo import models


class SalePurchaseReportXlsx(models.AbstractModel):
    # _name = 'report.module_name.report_name' Here report name should be the name of report that
    # is define in report.xml file at name section
    _name = 'report.daily_inventory_purchase_report.sale_purchase_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        # for obj in lines:
        #     report_name = obj.name
        #     # One sheet by partner
        #     sheet = workbook.add_worksheet(report_name)
        #     bold = workbook.add_format({'bold': True})
        #     sheet.write(0, 0, obj.name, bold)

        sheet = workbook.add_worksheet('test_report')
        bold = workbook.add_format({'bold': True})
        sheet.write(0, 0, 'test_report', bold)
