odoo.define('awesome_tshirt.QuickOrderNavigation', function (require) {
"use strict";

var core = require('web.core');
var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');

var _t = core._t;


var QuickOrderNavigation = Widget.extend({
    template: 'QuickOrderNavigation',
    events: {
        'keydown .o_input': '_onKeyDown',
    },

    _onKeyDown: function (ev) {
        if (ev.key === 'Enter') { // Enter
            var id = parseInt(this.$('input').val());

            if (!_.isNaN(id)) {
                var self = this;

                this.do_action({
                    res_id: id,
                    res_model: 'awesome_tshirt.order',
                    target: 'new',
                    type: 'ir.actions.act_window',
                    views: [[false, 'form']],
                }).then(undefined, function () {
                    self.do_warn(
                        _t('Order not found'),
                        _t("No order with this ID found in the database")
                    );
                });
            }
        }
    },
});


SystrayMenu.Items.push(QuickOrderNavigation);
return QuickOrderNavigation;

});
