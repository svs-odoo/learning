# -*- coding: utf-8 -*-

from odoo import api, fields, models

class Rental(models.Model):
    _name = 'library.rental'
    _description = 'Book Rental'

    customer_id = fields.Many2one('res.partner', string='Customer',
        required=True, domain=[('customer', '=', True)])
    copy_id = fields.Many2one('library.copy', string='Book Copy',
        required=True, domain=[('state', '=', 'availible')])
    book_id = fields.Many2one('product.product', string='Book',
        related="copy_id.book_id", readonly=True, domain=[('is_book', '=', True)])

    rental_date = fields.Date(default=fields.Date.context_today, required=True)
    return_date = fields.Date(required=True)
    state = fields.Selection([('draft', 'Draft'), ('rented', 'Rented'),
        ('returned', 'Returned'), ('lost', 'Lost')], default='draft')

    customer_address = fields.Text(compute='_compute_customer_address')
    customer_email = fields.Char(related='customer_id.email')

    book_authors = fields.Many2many(related='book_id.author_ids')
    book_publisher = fields.Many2one(related='book_id.publisher_id')
    book_edition_date = fields.Date(related='book_id.edition_date')
    book_isbn = fields.Char(related='book_id.isbn')

    @api.depends('customer_id')
    def _compute_customer_address(self):
        self.customer_address = self.customer_id.address_get()

    @api.multi
    def add_fee(self, type):
        for record in self:
            if type == 'time':
                price_id = self.env.ref('library.price_rent')
                delta_dates = fields.Date.from_string(record.return_date) - fields.Date.from_string(record.rental_date)
                amount = delta_dates.days * price_id.price / price_id.duration
            elif type == 'loss':
                price_id = self.env.ref('library.price_loss')
                amount = price_id.price
            else:
                return

            self.env['library.payment'].create({
                'customer_id': record.customer_id.id,
                'date': record.rental_date,
                'amount': -amount
            })

    # Actions
    @api.multi
    def action_confirm(self):
        for record in self:
            record.state = 'rented'
            record.copy_id.state = 'rented'
            record.add_fee('time')
            return

    @api.multi
    def action_return(self):
        for record in self:
            record.state = 'returned'
            record.copy_id.state = 'availible'

    @api.multi
    def action_lost(self):
        for record in self:
            record.state = 'lost'
            record.copy_id.state = 'lost'
            record.copy_id.active = False
            record.add_fee('loss')

    @api.model
    def _cron_check_date(self):
        late_rentals = self.search([('state', '=', 'rented'), ('return_date', '<', fields.Date.today())])
        template_id = self.env.ref('library.mail_template_book_return')
        for record in late_rentals:
            mail_id = template_id.send_mail(record.id)
