# -*- coding: utf-8 -*-

from odoo import fields, models

class Partner(models.Model):
    _inherit = 'datasample.partner'
    _name = 'datasample.partner'

    email = fields.Text()
    address = fields.Text()

    partner_type = fields.Selection([('customer', 'Customer'), ('author', 'Author')],
        default='customer')

    rental_ids = fields.One2many('library.rental', 'customer_id', string='Rentals')
