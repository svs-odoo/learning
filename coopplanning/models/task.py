# -*- coding: utf-8 -*-

from odoo import fields, models

class TaskType(models.Model):
    _name = 'coopplanning.task.type'
    _description = 'Task Type'

    name = fields.Char()
    description = fields.Text()

    area = fields.Char()
    active = fields.Boolean(default=True)

class TaskTemplate(models.Model):
    _name = 'coopplanning.task.template'
    _description = 'Task Template'

    name = fields.Char()

    day_nb_id = fields.Many2one('coopplanning.daynumber', string='day')
    tasktype_id = fields.Many2one('coopplanning.task.type', string='Task Type')

    start_time = fields.Float()
    duration = fields.Float(help="Duration in Hour")

    worker_nb = fields.Integer(default=1, required=True)
    worker_ids = fields.Many2many('coopplanning.partner')
    active = fields.Boolean(default=True)
