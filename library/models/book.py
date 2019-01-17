# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Book(models.Model):
    _inherit = 'product.product'

    resume = fields.Text(string='Resume')

    author_ids = fields.Many2many('res.partner', required=True, string='Author(s)',
        domain=[('is_author', '=', True)])
    publisher_id = fields.Many2one('res.partner', string='Publisher',
        domain=[('is_publisher', '=', True)])
    edition_date = fields.Date()
    isbn = fields.Char(string='ISBN')

    copy_ids = fields.One2many('library.copy', 'book_id', string='Book Copies')
    is_book = fields.Boolean('Is a book', default=False)


class BookCopy(models.Model):
    _name = 'library.copy'
    _description = 'Book Copy'
    _rec_name = 'reference'

    book_id = fields.Many2one('product.product', string="Book", required=True,
        domain=[('is_book', '=', True)],
        ondelete='cascade', delegate=True)
    reference = fields.Char(string='ref.', required=True)
    active = fields.Boolean(default=True)

    rental_ids = fields.One2many('library.rental', 'copy_id', string='Rentals')
    readers_count = fields.Integer(compute="_compute_readers_count")
    state = fields.Selection([('availible', 'Availible'), ('rented', 'Rented'), ('lost', 'Lost')],
        default='availible')

    def open_readers(self):
        self.ensure_one()
        reader_ids = self.rental_ids.mapped('customer_id')
        return {
            'name': 'Readers for %s' % (self.name),
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'domain': [('id', 'in', reader_ids.ids)],
            'target': 'new'
        }

    @api.depends('rental_ids.customer_id')
    def _compute_readers_count(self):
        for record in self:
            record.readers_count = len(record.mapped('rental_ids'))
