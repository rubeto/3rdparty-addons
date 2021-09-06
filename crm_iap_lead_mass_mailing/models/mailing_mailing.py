from odoo import fields, models


class MailingMailing(models.Model):

    _inherit = 'mailing.mailing'

    create_lead_open = fields.Boolean(string='Create Lead/Opportunity '
                                             'on mail open')
