from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    invoice_multi_currency = fields.Boolean(related='company_id.invoice_multi_currency')
