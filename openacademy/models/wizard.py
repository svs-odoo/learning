# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Wizard(models.TransientModel):
    _name = 'openacademy.wizard'
    _description = 'Wizard to add attendees to a session'

    def _default_attendees(self):
        return self.env['res.partner'].browse(self._context.get('active_ids'))

    session_id = fields.Many2one('openacademy.session', string="Session",
        required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees",
        required=True, default=_default_attendees)

    @api.multi
    def subscribe(self):
        for session in self.session_id:
            session.attendee_ids |= self.attendee_ids
        return {}
