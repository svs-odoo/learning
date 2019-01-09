# -*- coding: utf-8 -*-

from odoo import fields, models

class Publisher(models.Model):
    _name = 'library.publisher'
    _description = 'Publisher'

    name = fields.Char(require=True)
    book_ids = fields.Many2many('library.book', string='Published Books')
