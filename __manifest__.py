# -*- coding: utf-8 -*-
{
    'name': "Odoo module for DT-DATA test",

    'summary': """
        This module is for testing purposes only.""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Elio Linarez <elinarezv@gmail.com>",
    'website': "http://www.dt-data.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Invoicing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
