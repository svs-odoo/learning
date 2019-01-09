# -*- coding: utf-8 -*-

from odoo import fields, models

class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Course'

    name = fields.Char(string='Title', required=True)
    description = fields.Text()

    responsable_id = fields.Many2one('openacademy.partner', string='Responsible')
    session_ids = fields.One2many('openacademy.session', 'course_id',
        string='Sessions')

    level = fields.Selection([(1, 'Beginner'), (2, 'Confirmed'), (3, 'Gooroo')],
       string='Difficulty Level')

class Session(models.Model):
    _name = 'openacademy.session'
    _description = 'Session'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    status = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done')],
        string='Status', default='draft')

    start_date = fields.Date(default=fields.Date.context_today)
    duration = fields.Float(digits=(6, 2), help='Duration in days', default=1)

    course_id = fields.Many2one('openacademy.course', string='Course',
       ondelete='cascade', required=True)
    instructor_id = fields.Many2one('openacademy.partner', string='Instructor')
    attendee_ids = fields.Many2many('openacademy.partner', string='Attendees')
