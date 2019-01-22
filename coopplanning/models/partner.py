# -*- coding: utf-8 -*-

from odoo import api, fields, models

class Partner(models.Model):
    _inherit = 'res.partner'

    task_count = fields.Integer(compute='_compute_task_count')
    task_ids = fields.One2many('coopplanning.task', 'worker_id', string="Tasks")

    @api.depends('task_ids')
    def _compute_task_count(self):
        for partner in self:
            partner.task_count = len(task_ids)
