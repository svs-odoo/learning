# -*- coding: utf-8 -*-
{
    'name': "Data Sample",
    'summary': """Add data for training purpose""",
    'description': """Add a lot of data, like partner for example""",

    'author': "svs-odoo",
    'website': "http://www.odoo.com",

    'category': "Project",
    'version': "0.1",
    'depends': ['base'],

    'data': [
        "security/ir.model.access.csv"
    ],
    'demo': [
        'demo/partner.xml',
        'demo/area.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
