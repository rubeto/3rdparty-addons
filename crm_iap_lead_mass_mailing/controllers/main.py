from odoo import http
from odoo.http import request
from odoo.addons.mass_mailing.controllers.main import MassMailController


class LeadMassMailController(MassMailController):

    @http.route('/mail/track/<int:mail_id>/blank.gif', type='http', auth='public')
    def track_mail_open(self, mail_id, **post):
        """
        Create a new Lead/Opportunity on mail open
        """
        res = super(LeadMassMailController, self).track_mail_open(mail_id, **post)

        # get a reference to the mail message
        mail_message = request.env['mail.mail'].sudo().browse(mail_id)

        # check if mail message is related to a mailing
        # and the mailing creates new leads on mail open
        if mail_message.mailing_id and mail_message.mailing_id.create_lead_open:

            # create the new Lead/Opportunity
            request.env['crm.lead'].sudo().create({
                'name': f'{mail_message.email_to} opened mail in mailing: {mail_message.mailing_id.name}',
                'email_from': mail_message.mail_to,
            })
        return res
