# -*- coding: utf-8 -*-

from odoo import api, fields, models

class TaskType(models.Model):
    _name = 'coopplanning.task.type'
    _description = 'Task Type'

    name = fields.Char()
    description = fields.Text()

    area = fields.Many2one('datasample.area')
    active = fields.Boolean(default=True)


class TaskTemplate(models.Model):
    _name = 'coopplanning.task.template'
    _description = 'Task Template'

    name = fields.Char()

    day_nb_id = fields.Many2one('coopplanning.daynumber', string='Day')
    day_number = fields.Integer(related='day_nb_id.number')
    task_type_id = fields.Many2one('coopplanning.task.type', string='Task Type')

    start_time = fields.Date(default=fields.Date.context_today)
    end_time = fields.Date(default=fields.Date.context_today)
    duration = fields.Float(help="Duration in Hour")

    worker_nb = fields.Integer(default=1, required=True)
    worker_ids = fields.Many2many('datasample.partner', string="Recurrent worker assigned")
    active = fields.Boolean(default=True)

    task_area = fields.Many2one(related='task_type_id.area')
    archive = fields.Boolean(default=False)

    @api.onchange('start_time', 'end_time')
    def _check_date_time(self):
        for record in self:
            if not (record.start_time and record.end_time):
                return
            if record.end_time < record.start_time:
                return {'warning': {
                    'title': "Incorrect date value",
                    'message': "End date is earlier than start date"
                }}