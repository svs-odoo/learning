# -*- coding: utf-8 -*-

from odoo import fields, models

class Partner(models.Model):
    _name = 'coopplanning.partner'
    _description = 'Volunteer'

    name = fields.Char(require=True)
