# -*- encoding: utf-8 -*-

{
    'name': 'Odoo 14 Account Bank Statement Import',
    'version': '14.0.1.0.0',
    'category': 'Accounting',
    'depends': ['account'],
    'website': 'https://www.odoomates.tech',
    'author': 'Odoo Mates, Odoo SA',
    'support': 'odoomates@gmail.com',
    'maintainer': 'Odoo Mates',
    'license': 'LGPL-3',
    'description': """Generic Wizard to Import Bank Statements In Odoo14 Community Edition.
(This module does not include any type of import format.)
OFX and QIF imports are available in Enterprise version.""",
    'data': [
        'security/ir.model.access.csv',
        'account_bank_statement_import_view.xml',
        'account_import_tip_data.xml',
        'wizard/journal_creation.xml',
        'views/account_bank_statement_import_templates.xml',
    ],
    'demo': [
        'demo/partner_bank.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': True,
}
