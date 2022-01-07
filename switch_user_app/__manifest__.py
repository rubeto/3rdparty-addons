# -*- coding: utf-8 -*-
{
    'name': "Switch User",

    'summary': """This Module Allow User To Login By Other User Without Logout And Login Again""",

    'description': """
        Enable Switching User From Odoo Backend
    """,
    'author': "Zain-Alabdin",
    'website': "https://www.linkedin.com/in/zainalabdeen-merghani-56b7ab106",
    'category': 'Extra Tools',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base','web'],
    # always loaded
    'data': [
        'security/group.xml',
        # 'security/ir.model.access.csv',
        'views/assets.xml',
        'views/res_config_settings_views.xml',    ],
    'qweb':[
        'static/src/xml/template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "images":  ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'license': "AGPL-3",
}
