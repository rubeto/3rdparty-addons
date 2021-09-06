import ast
from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class HelpdeskTeam(models.Model):

    _name = "helpdesk.ticket.team"
    _description = "Helpdesk Ticket Team"
    _inherit = ["mail.thread", "mail.alias.mixin"]

    name = fields.Char(string="Name", required=True)
    user_ids = fields.Many2many(comodel_name="res.users", string="Members")
    active = fields.Boolean(default=True)
    category_ids = fields.Many2many(
        comodel_name="helpdesk.ticket.category", string="Category"
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company,
    )
    user_id = fields.Many2one(
        comodel_name="res.users", string="Team Leader", check_company=True,
    )
    alias_id = fields.Many2one(
        comodel_name="mail.alias",
        string="Email",
        ondelete="restrict",
        required=True,
        help="The email address associated with \
                               this channel. New emails received will \
                               automatically create new tickets assigned \
                               to the channel.",
    )
    color = fields.Integer(string="Color Index", default=0)
    ticket_ids = fields.One2many(
        comodel_name="helpdesk.ticket", inverse_name="team_id", string="Tickets",
    )
    todo_ticket_ids = fields.One2many(
        related="ticket_ids",
        domain="[('closed', '=', False)]",
        string="Todo tickets",
        readonly=True,
    )
    todo_ticket_count = fields.Integer(
        string="Number of tickets", compute="_compute_todo_tickets"
    )
    todo_ticket_count_unassigned = fields.Integer(
        string="Number of tickets unassigned", compute="_compute_todo_tickets"
    )
    todo_ticket_count_unattended = fields.Integer(
        string="Number of tickets unattended", compute="_compute_todo_tickets"
    )
    todo_ticket_count_high_priority = fields.Integer(
        string="Number of tickets in high priority", compute="_compute_todo_tickets"
    )

    # ------------------------------------------------------------
    # ORM
    # ------------------------------------------------------------

    def write(self, vals):
        result = super(HelpdeskTeam, self).write(vals)
        if 'use_leads' in vals or 'use_opportunities' in vals:
            for team in self:
                alias_vals = team._alias_get_creation_values()
                team.write({
                    'alias_name': alias_vals.get('alias_name', team.alias_name),
                    'alias_defaults': alias_vals.get('alias_defaults'),
                })
        return result

    # ------------------------------------------------------------
    # MESSAGING
    # ------------------------------------------------------------

    def _alias_get_creation_values(self):
        values = super(HelpdeskTeam, self)._alias_get_creation_values()
        values['alias_model_id'] = self.env['ir.model']._get('helpdesk.ticket.team').id
        if self.id:
            values['alias_name'] = False
            values['alias_defaults'] = defaults = ast.literal_eval(self.alias_defaults or "{}")
            defaults['team_id'] = self.id
        return values

    @api.depends("ticket_ids", "ticket_ids.stage_id")
    def _compute_todo_tickets(self):
        for record in self:
            record.todo_ticket_ids = record.ticket_ids.filtered(
                lambda ticket: not ticket.closed
            )
            record.todo_ticket_count = len(record.todo_ticket_ids)
            record.todo_ticket_count_unassigned = len(
                record.todo_ticket_ids.filtered(lambda ticket: not ticket.user_id)
            )
            record.todo_ticket_count_unattended = len(
                record.todo_ticket_ids.filtered(lambda ticket: ticket.unattended)
            )
            record.todo_ticket_count_high_priority = len(
                record.todo_ticket_ids.filtered(lambda ticket: ticket.priority == "3")
            )

