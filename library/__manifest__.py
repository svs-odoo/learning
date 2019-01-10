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
        # 'views/views.xml',
        # 'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}