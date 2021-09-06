from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    invoice_multi_currency = fields.Boolean(string='Multi Currency '
                                                   'in Invoice',
                                            default=False)
