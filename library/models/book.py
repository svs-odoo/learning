# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Book(models.Model):
    _name = 'library.book'
    _description = 'Book'

    name = fields.Char(string='Title', required=True)
    resume = fields.Text(string='Resume')

    author_ids = fields.Many2many('res.partner', required=True, string='Author(s)')
    publisher_id = fields.Many2one('library.publisher', string='Publisher')
    edition_date = fields.Date()
    isbn = fields.Char(string='ISBN')

    copy_ids = fields.One2many('library.book.copy', 'book_id', string='Book Copies')


class BookCopy(models.Model):
    _name = 'library.book.copy'
    _description = 'Book Copy'
    _rec_name = 'reference'

    name = fields.Char(related='book_id.name')

    book_id = fields.Many2one('library.book', string="Book", required=True,
        ondelete='cascade', delegate=True)
    reference = fields.Char(compute='_compute_reference')
    note = fields.Char()

    rental_ids = fields.One2many('library.rental', 'copy_id', string='Rentals')

    @api.depends('book_id', 'note')
    def _compute_reference(self):
        if self.book_id:
            self.reference = self.name
        if self.note:
            self.reference += ' - ' + self.note
        else:
            self.reference += ' - [copy]'
