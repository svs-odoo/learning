# -*- coding: utf-8 -*-

import math
from datetime import datetime
from pytz import UTC
from odoo import api, fields, models

def float_to_time(f):
    decimal, integer = math.modf(f)
    decimal = str(int(round(decimal * 60))).zfill(2)
    integer = str(int(integer))
    return "%s:%s" % (integer, decimal)

def floatime_to_hour_minute(f):
    decimal, integer = math.modf(f)
    decimal = int(round(decimal * 60))
    integer = int(integer)
    return integer, decimal

class TaskType(models.Model):
    _name = 'coopplanning.task.type'
    _description = 'Task Type'

    name = fields.Char()
    description = fields.Text()
    complete_name = fields.Char(compute='_compute_complete_name')

    area = fields.Many2one('datasample.area')
    active = fields.Boolean(default=True)

    @api.depends('name', 'description')
    def _compute_complete_name(self):
        self.complete_name = self.name + ' - ' + self.description


class TaskTemplate(models.Model):
    _name = 'coopplanning.task.template'
    _description = 'Task Template'

    name = fields.Char()

    day_nb_id = fields.Many2one('coopplanning.daynumber', string='Day')
    day_number = fields.Integer(related='day_nb_id.number')
    task_type_id = fields.Many2one('coopplanning.task.type', string='Task Type')

    start_time = fields.Float()
    end_time = fields.Float()
    duration = fields.Float(compute='_compute_duration', help="Duration in Hour", store=True)

    worker_nb = fields.Integer(default=1, required=True)
    worker_ids = fields.Many2many('res.partner', string="Recurrent worker assigned")
    active = fields.Boolean(default=True)

    task_area = fields.Many2one(related='task_type_id.area')
    archive = fields.Boolean(default=False)
    floating = fields.Boolean(default=False)

    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        for record in self:
            record.duration = record.end_time - record.start_time

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

    @api.multi
    def generate_task(self):
        self.ensure_one()
        task = self.env['coopplanning.task']
        today = datetime.today()
        h_begin, m_begin = floatime_to_hour_minute(self.start_time)
        h_end, m_end = floatime_to_hour_minute(self.end_time)

        for i in xrange(0, self.worker_nb):
            p_worker_id = False
            if i < len(self.worker_ids):
                p_worker_id = self.worker_ids[i].id
            p_start_time = fields.Datetime.context_timestamp(self, today).replace(hour=h_begin, minute=m_begin, second=0)
            p_end_time = fields.Datetime.context_timestamp(self, today).replace(hour=h_end, minute=m_end, second=0)

            task.create({
                'name': "%s (%s) - (%s) [%s]" % (self.name, float_to_time(self.start_time), float_to_time(self.end_time), i),
                'task_template_id': self.id,
                'task_type_id': self.task_type_id.id,
                'worker_id': p_worker_id,
                'start_time': p_start_time,
                'end_time': p_end_time
            })

    @api.onchange('floating')
    def _onchange_floating(self):
        if self.floating:
            self.worker_ids = False


class Task(models.Model):
    _name = 'coopplanning.task'
    _description = 'Task'

    name = fields.Char(related='task_type_id.complete_name')

    task_template_id = fields.Many2one('coopplanning.task.template')
    task_type_id = fields.Many2one('coopplanning.task.type')

    start_time = fields.Datetime()
    end_time = fields.Datetime()

    worker_id = fields.Many2one('res.partner')
