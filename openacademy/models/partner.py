# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Partner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean(default=False)
    session_ids = fields.Many2many('openacademy.session', string='Attended Sessions',
       readonly=True)

    level = fields.Integer(compute='_get_level', string="Level", store=True)

    @api.depends('category_id', 'category_id.name')
    def _get_level(self):
        for partner in self:
            level = []
            for category in partner.category_id:
                if "Teacher Level" in category.name:
                    level.append(int(category.name.split(' ')[-1]))
                partner.level = max(level) if level else 0
