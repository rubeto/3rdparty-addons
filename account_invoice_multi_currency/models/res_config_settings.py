from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    invoice_multi_currency = fields.Boolean(string='Multi Currency '
                                                   'in Invoice',
                                            related='company_id.invoice_multi_currency',
                                            readonly=False)
