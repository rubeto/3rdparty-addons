{
    'name': 'Lead Generation from Mass Mail Open',
    'version': '14.0.1.0',
    'summery': 'Create Leads/Opportunities based on open rate of mail campaigns',
    'description': """
        Create Leads/Opportunities based on open rate of mail campaigns
    """,
    'author': 'Kareem Abuzaid, kareem.abuzaid123@gmail.com',
    'category': 'Sales/CRM',
    'license': "AGPL-3",
    'images': ['static/description/field.png'],
    'data': [
        'views/mailing_mailing.xml',
    ],
    'depends': [
        'mass_mailing',
        'crm',
        'crm_iap_lead',
    ],
    'application': False,
}
