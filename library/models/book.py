# -*- coding: utf-8 -*-
from odoo import fields, models

class Book(models.Model):
    _name = 'library.book'
    _description = 'Book'

    name = fields.Char(string='Title', required=True)

    author_ids = fields.Many2many('library.partner', required=True, string='Author(s)')
    publisher_id = fields.Many2one('library.publisher', string='Publisher')
    edition_date = fields.Date()
    isbn = fields.Char(string='ISBN')

    rental_ids = fields.One2many('library.rental', 'book_id', string='Rentals')
