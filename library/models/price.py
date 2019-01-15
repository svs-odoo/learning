# -*- coding: utf-8 -*-
from odoo import fields, models

class Price(models.Model):
    _name = 'library.price'
    _description = 'Price'

    name = fields.Char()
    duration = fields.Float('Duration in days', default=1)
    price = fields.Float()
    type = fields.Selection([('time', 'Based on time'), ('one', 'One shot')],
        default='time')
