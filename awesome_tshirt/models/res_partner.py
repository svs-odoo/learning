# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    order_ids = fields.One2many('awesome_tshirt.order', 'customer_id', string="Orders")
    has_active_order = fields.Boolean(compute='_compute_has_active_order', store=True)

    @api.depends('order_ids', 'order_ids.state')
    def _compute_has_active_order(self):
        for record in self:
            record.has_active_order = record.order_ids.filtered(lambda r: r.state not in ['sent', 'cancelled'])

    @api.multi
    def random_geo_localize(self):
        # Generate a random localisation
        from random import uniform

        ad_limit = 1 / 100000
        latitude_coef = 85
        longitude_coef = 175

        for partner in self:
            partner_latitude = uniform(-latitude_coef, latitude_coef + ad_limit)
            partner_longitude = uniform(-latitude_coef, latitude_coef + ad_limit)

            partner.write({
                'partner_latitude': partner_latitude,
                'partner_longitude': partner_longitude,
                'date_localization': fields.Date.context_today(partner),
            })
        return True
