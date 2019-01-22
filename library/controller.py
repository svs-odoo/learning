# -*- coding: utf-8 -*-

from odoo import fields, http
from odoo.http import request

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
