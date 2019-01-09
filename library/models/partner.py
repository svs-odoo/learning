# -*- coding: utf-8 -*-

from odoo import fields, models

class Partner(models.Model):
    _name = 'library.partner'
    _description = 'Partner'

    firstname = fields.Char(require=True)
    lastname = fields.Char(require=True)
    email = fields.Text()
    adress = fields.Text()

    partner_type = fields.Selection([('customer', 'Customer'), ('author', 'Author')],
        default='customer')

    rental_ids = fields.One2many('library.rental', 'customer_id', string='Rentals')
