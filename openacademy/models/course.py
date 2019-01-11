# -*- coding: utf-8 -*-

from odoo import api, fields, models

class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Course'

    name = fields.Char(string='Title', required=True)
    description = fields.Text()

    responsible_id = fields.Many2one('datasample.partner', string='Responsible')
    session_ids = fields.One2many('openacademy.session', 'course_id',
        string='Sessions')

    level = fields.Selection([(1, 'Beginner'), (2, 'Confirmed'), (3, 'Gooroo')],
       string='Difficulty Level')
    session_count = fields.Integer(compute="_compute_session_count")

    @api.depends('session_ids')
    def _compute_session_count(self):
        for course in self:
            course.session_count = len(course.session_ids)

class Session(models.Model):
    _name = 'openacademy.session'
    _description = 'Session'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    status = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done')],
        string='Status', default='draft')

    start_date = fields.Date(default=fields.Date.context_today)
    end_date = fields.Date(default=fields.Date.context_today)
    duration = fields.Float(digits=(6, 2), help='Duration in days', default=1)
    level = fields.Selection(related='course_id.level')

    course_id = fields.Many2one('openacademy.course', string='Course',
       ondelete='cascade', required=True)
    instructor_id = fields.Many2one('datasample.partner', string='Instructor')
    responsible_id = fields.Many2one(related='course_id.responsible_id',
        readonly=True, store=True)
    attendee_ids = fields.Many2many('datasample.partner', string='Attendees')
    attendees_count = fields.Integer(compute='_get_attendees_count', store=True)

    seats = fields.Integer()
    taken_seats = fields.Integer(compute='_compute_taken_seats', store=True)

    @api.depends('seats', 'attendee_ids')
    def _compute_taken_seats(self):
        for session in self:
            if not session.seats:
                session.taken_seats = 0
            else:
                session.taken_seats = len(session.attendee_ids) / session.seats * 100

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for session in self:
            session.attendees_count = len(session.attendee_ids)

    @api.onchange('seats', 'attendee_ids')
    def _check_taken_seats(self):
        for session in self:
            if session.taken_seats > 100:
                return {'warning': {
                    'title': 'Too many attendees for this session !',
                    'message':
                        'This session has %s and have already %s attendees registred.' % (
                            session.seats, len(session.attendee_ids)
                            )
                }}

    @api.onchange('start_date', 'end_date')
    def _compute_duration(self):
        for session in self:
            if not (session.start_date and session.end_date):
                return
            if session.end_date < session.start_date:
                return {'warning': {
                    'title': 'Incorrect date value',
                    'message': 'End date is earlier than start date'
                }}
            delta = fields.Date.from_string(session.end_date) - fields.Date.from_string(session.start_date)
            session.duration = delta.days + 1
        # if not (self.start_date and self.end_date):
        #     return
        # if self.end_date < self.start_date:
        #     return {'warning': {
        #         'title': 'Incorrect date value',
        #         'message': 'End date is earlier then start date'
        #     }}
        # delta = fields.Date.from_string(self.end_date) - fields.Date.from_string(self.start_date)
        # self.duration = delta.days + 1
