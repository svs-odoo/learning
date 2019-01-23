# -*- coding: utf-8 -*-
{
    'name': "Library",

    'summary': """
        Manage a Library: customers, books, etc....""",

    'description': """
        Manage a Library: customers, books, etc....
    """,

    'author': "svs-odoo",
    'website': "http://www.odoo.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'product', 'website', 'website_sale'],

    'data': [
        'assets.xml',
        'security/ir.model.access.csv',
        'views/dashboard.xml',
        'views/book_views.xml',
        'views/partner_views.xml',
        'views/price_views.xml',
        'views/rental_views.xml',
        'views/menu_views.xml',
        'views/wizard_views.xml',
        'data/cron.xml',
        'data/mail.xml',
        'website/template.xml',
    ],
    'demo': [
        'data/demo.xml',
    ],
    'qweb': [
        'static/src/xml/dashboard.xml'
    ],
    'installable': True,
    'application': True,
}
