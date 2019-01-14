# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Partner(models.Model):
    _inherit = 'res.partner'

    firstname = fields.Char(require=True)
    lastname = fields.Char(require=True)
    # name = fields.Char(compute='_compute_name', store=True)

    # @api.depends('firstname', 'lastname')
    # def _compute_name(self):
    #     for partner in self:
    #         if not (partner.firstname and partner.lastname):
    #             return
    #         partner.name = partner.firstname + " " + partner.lastname
