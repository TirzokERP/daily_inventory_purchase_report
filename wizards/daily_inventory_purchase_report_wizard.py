from datetime import timedelta

from odoo import models, fields, api
from odoo.tools import float_round


class DailyInventoryPurchaseReportWizard(models.TransientModel):
    _name = 'daily_inventory_purchase_report.wizard'
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)

    @api.onchange('start_date')
    def _onchange_start_date(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            self.end_date = self.start_date

    @api.onchange('end_date')
    def _onchange_end_date(self):
        if self.end_date and self.end_date < self.start_date:
            self.start_date = self.end_date

    def export_report(self):
        return self.env.ref('daily_inventory_purchase_report.sale_purchase_report').report_action(self)
