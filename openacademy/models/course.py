# -*- coding: utf-8 -*-

from odoo import api, fields, models

class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Course'

    name = fields.Char(string='Title', required=True)
    description = fields.Text()

    responsible_id = fields.Many2one('res.partner', string='Responsible')
    can_edit_responsible = fields.Boolean(compute='_compute_can_edit_responsible')
    session_ids = fields.One2many('openacademy.session', 'course_id',
        string='Sessions')

    level = fields.Selection([(1, 'Beginner'), (2, 'Confirmed'), (3, 'Gooroo')],
       string='Difficulty Level')
    session_count = fields.Integer(compute="_compute_session_count")
    attendees_count = fields.Integer(compute="_compute_attendees_count")

    currency_id = fields.Many2one('res.currency', "Currency")
    product_id = fields.Many2one('product.template', "Product")

    @api.depends('session_ids.attendees_count')
    def _compute_attendees_count(self):
        for course in self:
            course.attendees_count = len(course.mapped('session_ids.attendee_ids'))

    @api.depends('session_ids')
    def _compute_session_count(self):
        for course in self:
            course.session_count = len(course.session_ids)

    @api.depends('responsible_id')
    def _compute_can_edit_responsible(self):
        self.can_edit_responsible = self.env.user.has_group('openacademy.group_admin')

    @api.multi
    def open_attendees(self):
        self.ensure_one()
        attendee_ids = self.session_ids.mapped('attendee_ids')
        return {
            'name': 'Attendees of %s' % (self.name),
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'domain': [('id', 'in', attendee_ids.ids)]
        }


class Session(models.Model):
    _name = 'openacademy.session'
    _inherit = ['mail.thread']
    _order = 'name'
    _description = 'Session'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done')],
        string='Status', default='draft')
    level = fields.Selection(related='course_id.level')

    start_date = fields.Date(default=fields.Date.context_today)
    end_date = fields.Date(default=fields.Date.context_today)
    duration = fields.Float(digits=(6, 2), help='Duration in days', default=1)

    course_id = fields.Many2one('openacademy.course', string='Course',
       ondelete='cascade', required=True)
    instructor_id = fields.Many2one('res.partner', string='Instructor')
    responsible_id = fields.Many2one(related='course_id.responsible_id',
        readonly=True, store=True)
    attendee_ids = fields.Many2many('res.partner', string='Attendees')
    attendees_count = fields.Integer(compute='_get_attendees_count', store=True)

    seats = fields.Integer(default=1, help="Number of seats availible for this session")
    taken_seats = fields.Integer(compute='_compute_taken_seats', store=True)

    is_paid = fields.Boolean(default=False, string="Is Paid")
    product_id = fields.Many2one(related='course_id.product_id')
    price = fields.Float(related='product_id.lst_price')

    def _warning(self, title, message):
        return {'warning': {
            'title': title,
            'message': message,
            }}

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
    def _check_valid_seats(self):
        for record in self:
            if record.seats < 1:
                return self._warning(
                    'Not enough seats !',
                    'A session must contain at least one seat.'
                )
            if record.seats < record.attendees_count:
                return self._warning(
                    'Too many attendees for this session !',
                    'This session has %s and have already %s attendees registred.' % (record.seats, len(record.attendee_ids))
                )

    @api.onchange('start_date', 'end_date')
    def _compute_duration(self):
        for session in self:
            if not (session.start_date and session.end_date):
                return
            if session.end_date < session.start_date:
                return self._warning(
                    'Incorrect date value',
                    'End date is earlier than start date'
                )
            delta = fields.Date.from_string(session.end_date) - fields.Date.from_string(session.start_date)
            session.duration = delta.days + 1

    # Actions
    @api.multi
    def action_draft(self):
        for record in self:
            record.state = 'draft'
            record.message_post(body="Session '%s' state was reset to draft." % (record.name))

    @api.multi
    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'
            record.message_post(body="Session '%s' is confirmed !" % (record.name))

    @api.multi
    def action_done(self):
        for record in self:
            record.state = 'done'
            record.message_post(body="Session '%s' is marked as done." % (record.name))

    def _auto_confirm(self):
        for record in self:
            if record.taken_seats > 50 and record.state == 'draft':
                record.action_confirm()

    # Overide
    @api.multi
    def write(self, vals):
        res = super(Session, self).write(vals)
        for record in self:
            record._auto_confirm()
            if vals.get('instructor_id'):
                self.message_subscribe([vals['instructor_id']])
        return res

    @api.model
    def create(self, vals):
        res = super(Session, self).create(vals)
        res._auto_confirm()
        if vals.get('instructor_id'):
            res.message_subscribe([vals['instructor_id']])
        return res

    @api.multi
    def create_invoice(self):
        # We search existing invoice
        teacher_invoice = self.env['account.invoice'].search([
            ('partner_id', '=', self.instructor_id.id)
        ], limit=1)

        # If no existing invoice, we create one
        if not teacher_invoice:
            teacher_invoice = self.env['account.invoice'].create({
                'partner_id': self.instructor_id.id
            })

        # Then, we add a new line in the invoice of the session's responsible
        expense_account = self.env['account.account'].search([
            ('user_type_id', '=', self.env.ref('account.data_account_type_expenses').id)
        ], limit=1)
        self.env['account.invoice.line'].create({
            'invoice_id': teacher_invoice.id,
            'product_id': self.product_id.id,
            'price_unit': self.price,
            'account_id': expense_account.id,
            'name': 'Session',
            'quantity': 1,
        })

        # We mark the session as paid
        self.write({'is_paid': True})
