# -*- coding: utf-8 -*-

from odoo import api, fields, models

class Partner(models.Model):
    _inherit = 'res.partner'

    is_author = fields.Boolean(default=False)
    is_publisher = fields.Boolean(default=False)

    current_rental_ids = fields.One2many('library.rental', 'customer_id',
        string='Current Rentals', domain=[('state', '=', 'rented')])
    old_rental_ids = fields.One2many('library.rental', 'customer_id',
        string='Old Rentals', domain=[('state', '=', 'returned')])
    lost_rental_ids = fields.One2many('library.rental', 'customer_id',
        string='Lost Rentals', domain=[('state', '=', 'lost')])

    lost_book_nb = fields.Integer(compute='_compute_lost_book_number',
        string='Number of books the customer lost')
    payment_ids = fields.One2many('library.payment', 'customer_id',
        string='Payments')
    amount_owed = fields.Float(compute='_amount_owed', store=True)

    @api.multi
    def _compute_lost_book_number(self):
        for record in self:
            record.lost_book_nb = len(record.lost_rental_ids)

    @api.multi
    @api.depends('payment_ids.amount')
    def _amount_owed(self):
        for record in self:
            record.amount_owed = - sum(record.payment_ids.mapped('amount'))


class Payment(models.Model):
    _name = 'library.payment'
    _description = 'Payment'

    date = fields.Date(required=True, default=fields.Date.context_today)
    amount = fields.Float()
    customer_id = fields.Many2one('res.partner', string='Customer',
        domain=[('customer', '=', True)])
