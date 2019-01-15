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

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/book_views.xml',
        'views/partner_views.xml',
        'views/rental_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
