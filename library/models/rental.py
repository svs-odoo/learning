# -*- coding: utf-8 -*-

from odoo import fields, models

class Rental(models.Model):
    _name = 'library.rental'
    _description = 'Book Rental'

    customer_id = fields.Many2one('library.partner', string='Customer')
    book_id = fields.Many2one('library.book', string='Book')

    rental_date = fields.Date()
    return_date = fields.Date()

    customer_address = fields.Text(related='customer_id.address')
    customer_email = fields.Text(related='customer_id.email')

    book_author = fields.Many2many(related='book_id.author_ids')
    book_publisher = fields.Many2one(related='book_id.publisher_id')
    book_edition_date = fields.Date(related='book_id.edition_date')
    book_isbn = fields.Char(related='book_id.isbn')
