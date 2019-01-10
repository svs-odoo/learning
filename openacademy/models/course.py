# -*- coding: utf-8 -*-

from odoo import api, fields, models

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

    seats = fields.Integer()
    taken_seats = fields.Integer(compute='_compute_taken_seats', store=True)

    @api.depends('seats', 'attendee_ids')
    def _compute_taken_seats(self):
        for session in self:
            if not session.seats:
                session.taken_seats = 0
            else:
                session.taken_seats = len(session.attendee_ids) / session.seats * 100

    @api.onchange('seats', 'attendee_ids')
    def _check_taken_seats(self):
        for session in self:
            if self.taken_seats > 100:
                return {'warning': {
                    'title': 'Too many attendees for this session !',
                    'message':
                        'This session has %s and have already %s attendees registred.' % (
                            self.seats, len(self.attendees)
                            )
                }}
