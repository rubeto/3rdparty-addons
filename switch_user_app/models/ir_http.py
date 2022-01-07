# -*- coding: utf-8 -*-
from odoo import models


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        res = super(IrHttp, self).session_info()
        res['switch_user_enable'] = self.env['ir.config_parameter'].sudo().get_param('switch_user.switch_user_enable') and self.env.user.has_group('switch_user_app.group_switch_user_menu')
        if res['switch_user_enable']:
            res['switch_user_by_password'] = self.env['ir.config_parameter'].sudo().get_param('switch_user.switch_user_by_password')
        return res