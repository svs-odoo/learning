# -*- coding: utf-8 -*-

from odoo import fields, http
from odoo.http import request
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import date

class OpenAcademy(http.Controller):
    @http.route('/library/', auth='public', website=True)
    def library(self, **kwarg):
        copies = request.env['library.copy'].search([('state', '=', 'availible')])
        return request.render('library.rent_page', {
            'copies': copies
        })

    @http.route('/library/<int:id>', auth='public', website=True)
    def book(self, id):
        copy = request.env['library.copy'].search([('id', '=', id)])
        return request.render('library.book_page', {
            'copy': copy
        })

    @http.route('/library/rent/<int:id>', auth='public', website=True)
    def rent(self, id):
        partner = request.env.user.partner_id
        copy = request.env['library.copy'].search([('id', '=', id)])

        rental = request.env['library.rental'].create({
            'copy_id': copy.id,
            'customer_id': partner.id,
            'rental_date': fields.Date.today(),
            'return_date': fields.Date.today(),
        })
        rental.action_confirm()
        return request.redirect('/library/')

    @http.route('/library/statistics/', auth='user', type='json')
    def statistics(self):
        Copy = request.env['library.copy']
        Payment = request.env['library.payment']
        Rental = request.env['library.rental']
        first_day = date.today().replace(day=1).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        last_day = date.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        rental_month_domain = [('rental_date', '>=', first_day), ('rental_date', '<=', last_day)]
        lost_books = Rental.search([('state', '=', 'lost')] + rental_month_domain)
        payment_month_domain = [('date', '>=', first_day), ('date', '<=', last_day)]
        nb_rentals = Rental.search_count(rental_month_domain)

        return {
            'money_in': sum(Payment.search(payment_month_domain).mapped('amount')),
            'nb_rentals': nb_rentals,
            'nb_lost_books': len(lost_books),
            'nb_availible_book': Copy.search_count([('state', '=', 'availible')]),
            'nb_rented_book': Copy.search_count([('state', '=', 'rented')]),
            'nb_lost_book': Copy.search_count([('active', '=', False), ('state', '=', 'lost')])
        }
