# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    switch_user_enable = fields.Boolean(string='Switch User Enable')
    switch_user_by_password = fields.Boolean(string='Switch User By Password')
    switch_user_password = fields.Char(string='Switch User Password')


    def set_values(self):
        res = super(ResConfigSettings,self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('switch_user.switch_user_enable',self.switch_user_enable)
        self.env['ir.config_parameter'].sudo().set_param('switch_user.switch_user_by_password',self.switch_user_by_password)    
        self.env['ir.config_parameter'].sudo().set_param('switch_user.switch_user_password',self.switch_user_password)    
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        switch_user_param = self.env['ir.config_parameter'].sudo()
        user_enable = switch_user_param.get_param('switch_user.switch_user_enable')
        switch_user_by_password = switch_user_param.get_param('switch_user.switch_user_by_password')
        user_password = switch_user_param.get_param('switch_user.switch_user_password')
        
        res.update({
            'switch_user_enable' : user_enable,
            'switch_user_password':user_password,
            'switch_user_by_password':switch_user_by_password,
        })
        return res