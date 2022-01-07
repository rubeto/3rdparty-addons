# -*- coding: utf-8 -*-
from odoo.http import request
from odoo import http


class SwitchUser(http.Controller):

     @http.route('/web/switch_user/authenticate/', type="json",auth='user')
     def authenticate(self,db,user, password):
        request.session.__setattr__('switch_user',True)
        request.env.cr.execute(
            "SELECT login FROM res_users WHERE id=%s",
            [user]
        )
        [login] = request.env.cr.fetchone()
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()
