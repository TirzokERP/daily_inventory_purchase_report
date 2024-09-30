# -*- coding: utf-8 -*-
{
    'name': "Tirzok Daily Inventory Purchase Report",

    'summary': """
        This report enables users to easily generate a consolidated report for the Sales, Purchases, and Inventory modules, providing comprehensive results in a streamlined manner.
        """,

    'description': """
        In this report, users can generate comprehensive data through the Sales module's reporting menu. The report provides detailed insights into stock levels, purchase quantities, sales volumes, and the previous day's stock quantities. This functionality is particularly useful when products are moved between warehouses, as it ensures accurate tracking of stock in and out.
        Additionally, the report offers a variety of filtering options, allowing users to customize the output based on specific needs. You can select multiple warehouses for analysis and filter data by various time frames, including day-wise, month-wise, quarterly, and yearly reports. These flexible filters enhance the precision of inventory tracking and reporting, making it easier to manage stock levels across different locations.
        Overall, the report simplifies complex data, offering users a clear and actionable view of inventory movement, helping them make informed decisions, and improving overall operational efficiency.

    """,

    'author': "Tirzok Private Limited",
    "license":  "GPL-3",
    'website': "https://tirzok.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sales',
    'version': '13.0',

    "live_test_url": "https://www.youtube.com/watch?v=3o7KR6p4l7Q",
    # any module necessary for this one to work correctly
    'depends': ['base', 'report_xlsx', 'stock', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'reports/sales_purchase_combine_report.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    "images":["static/description/Banner.png", "static/description/Icon.png"],

    "icon": "static/description/Icon.png",

    "documentation": ["doc/user_guide.html"],
}
