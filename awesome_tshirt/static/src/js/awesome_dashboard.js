odoo.define('awesome_tshirt.dashboard', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
// var ControlPanelMixin = require('web.ControlPanelMixin');
var core = require('web.core');
var _t = core._t;


var Dashboard = AbstractAction.extend({
    template: 'AwesomeDashboard',
    events: {
        'click .o_customer_btn': '_openCustomer',
        'click .o_new_orders_btn': '_openNewOrders',
        'click .o_cancelled_orders_btn': '_openCancelledOrders',
    },

    // --------------------------------------------------------------------------
    // Private
    // --------------------------------------------------------------------------

    /**
     * @private
     */
    _openCancelledOrders: function (params) {
        this._openLastestOrders({
            name: 'Cancelled Orders',
            domain: [['state', '=', 'cancelled']],
        });
    },

    /**
     * @private
     */
    _openCustomer: function (params) {
        this.do_action('base.action_partner_customer_form');
    },

    /**
     * @private
     */
    _openLastestOrders: function (params) {
        var domain = params.domain || [];

        // Get the date of 7 days ago from now
        var limitDate = moment().subtract(7, 'd');
        // Format date
        limitDate = limitDate.local('en').format('YYYY-MM-DD HH:mm:ss');
        domain.concat([['create_date', '>=', limitDate]]);

        this.do_action({
            res_model: 'awesome_tshirt.order',
            name: _t(params.name),
            views: [[false, 'list'], [false, 'form']],
            domain: domain,
            type: 'ir.actions.act_window',
        });
    },

    /**
     * @private
     */
    _openNewOrders: function () {
        this._openLastestOrders({
            name: 'New Orders'
        });
    }
});


core.action_registry.add('awesome_tshirt.dashboard', Dashboard);

return Dashboard;

});