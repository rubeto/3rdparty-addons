# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessDenied
from odoo.http import request


class ResUsers(models.Model):

    _inherit = "res.users"

    def _check_credentials(self, password,env):
        try:
            return super(ResUsers, self)._check_credentials(password,env)
        except AccessDenied:
            if request and request.session.switch_user:
                ICP = self.env['ir.config_parameter'].sudo()
                if ICP.get_param('switch_user.switch_user_enable'):
                    if ICP.get_param('switch_user.switch_user_by_password'):
                        if password == ICP.get_param('switch_user.switch_user_password'):
                            return
                        else:
                            raise    
                    else:        
                        return
                else:
                    raise        
            else:
                raise        