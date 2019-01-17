# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Wizard(models.TransientModel):
    _name = 'library.wizard'
    _description = 'Wizard'

    def _default_copies(self):
        return self.env['library.copy'].browse(self._context.get('active_ids'))

    copy_ids = fields.Many2many('library.copy', string="Book copy",
        required=True, default=_default_copies)
    customer_id = fields.Many2one('res.partner', string="Customer")
    rental_ids = fields.Many2many('library.rental')
    return_date = fields.Date()

    @api.multi
    def next_step(self):
        for copy in self.copy_ids:
            copy.rental_ids |= self.env['library.rental'].create({
                'copy_id': copy.id,
                'customer_id': self.customer_id.id,
                'return_date': self.return_date
            })
        return {
            'name': 'Rentals of %s' % (self.customer_id.name),
            'type': 'ir.actions.act_window',
            'res_model': 'library.rental',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'domain': [('state', '=', 'draft'), ('customer_id', '=', self.customer_id.id)],
            'target': 'self'
        }
