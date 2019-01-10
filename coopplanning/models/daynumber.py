# -*- coding: utf-8 -*-

from odoo import fields, models

class DayNumber(models.Model):
    _name = 'coopplanning.daynumber'
    _description = 'Day of the Week (number)'

    name = fields.Char()
    number = fields.Integer('Day Number', help='From 1 to 7, where 1 is the first day when the instance begin.')
    active = fields.Boolean(default=True)
