# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Partner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean(default=False)
    session_ids = fields.Many2many('openacademy.session', string='Attended Sessions',
       readonly=True)
