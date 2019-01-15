# -*- coding: utf-8 -*-

from odoo import fields, models

class Publisher(models.Model):
    _name = 'library.publisher'
    _description = 'Publisher'

    name = fields.Char(require=True)
    book_ids = fields.One2many('library.book', 'publisher_id', string='Published Books')
