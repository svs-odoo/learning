# -*- coding: utf-8 -*-
from odoo import fields, models

class Area(models.Model):
    _name = 'datasample.area'
    _description = 'Area'

    name = fields.Char('Area', require=True)
    description = fields.Text()
    parent_area_id = fields.Many2one('datasample.area', string='Parent Area',
        ondelete='set null')
    responsible = fields.Many2one('datasample.partner', string='Responsible')
