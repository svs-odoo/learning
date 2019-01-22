# -*- coding: utf-8 -*-
{
    'name': "Cooperative Management",

    'summary': """
        Manage a cooperative group
    """,

    'description': """
        Manage a cooperative group
    """,

    'author': "svs-odoo",
    'website': "http://www.odoo.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'contacts', 'datasample'],

    'data': [
        'security/ir.model.access.csv',
        'views/daynumber_views.xml',
        'views/task_views.xml',
        'views/menu_views.xml',
        'report/task.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
