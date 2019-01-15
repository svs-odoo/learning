# -*- coding: utf-8 -*-
{
    'name': "OpenAcademy",

    'summary': """
        Create, organize and manage multiple courses easily""",

    'description': """
        Manage course, classes, teachers, students, ...
    """,

    'author': "svs-odoo",
    'website': "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Project',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'datasample', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/course_views.xml',
        'views/session_views.xml',
        'views/partner_views.xml',
        'views/menu_views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
        'demo/partner.xml',
    ],
    'installable': True,
    'application': True,
}
