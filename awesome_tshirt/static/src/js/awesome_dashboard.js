odoo.define('awesome_tshirt.dashboard', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var ChartWidget = require('awesome_tshirt.ChartWidget');
var ControlPanelMixin = require('web.ControlPanelMixin');
var core = require('web.core');
var fieldUtils = require('web.field_utils');

var _t = core._t;
var qweb = core.qweb;


var Dashboard = AbstractAction.extend(ControlPanelMixin, {
    template: 'AwesomeDashboard',
    custom_events: {
        open_orders: '_onOpenOrders'
    },

    /**
     * @override
     */
    willStart: function () {
        var self = this;
        var promSuper = this._super.apply(this, arguments);
        var promStats = this._renderStats().then(function (stats) {
            stats.average_time = fieldUtils.format.float_time(stats.average_time);
            self.stats = stats;
        });

        return Promise.all([promSuper, promStats]);
    },

    /**
     * @override
     */
    start: function () {
        var self = this;

        var promChart = this._renderChart();
        var promSuper = this._super.apply(this, arguments);
        this._renderButtons();

        return Promise.all([
            promChart,
            promSuper,
        ]).then(function () {
            self._updateControlPanel();
        });
    },

    /**
     * @override
     */
    destroy: function () {
        this._super.apply(this, arguments);
        if (this.$buttons) {
            this.$buttons.off();
        }
    },

    /**
     * @override
     */
    do_show: function () {
        this._super.apply(this, arguments);
        this._updateControlPanel();
    },


    // --------------------------------------------------------------------------
    // Private
    // --------------------------------------------------------------------------

    /**
     * @private
     * @param {*} params
     */
    _openCancelledOrders: function (params) {
        this._openLastestOrders({
            name: _t('Cancelled Orders'),
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

        this._openOrders({
            name: params.name,
            domain: domain,
        });
    },

    /**
     * @private
     */
    _openNewOrders: function () {
        this._openLastestOrders({
            name: _t('New Orders'),
            domain: [['state', '!=', 'cancelled']],
        });
    },

    /**
     * @private
     */
    _openOrders: function (params) {
        this.do_action({
            res_model: 'awesome_tshirt.order',
            name: params.name,
            domain: params.domain,
            views: [[false, 'list'], [false, 'form']],
            type: 'ir.actions.act_window'
        });
    },

    /**
     * @private
     */
    _renderButtons: function () {
        this.$buttons = $(qweb.render('AwesomeDashboard.Buttons'));
        this.$buttons.on('click', '.o_customer_btn', this._openCustomer.bind(this));
        this.$buttons.on('click', '.o_new_orders_btn', this._openNewOrders.bind(this));
        this.$buttons.on('click', '.o_cancelled_orders_btn', this._openCancelledOrders.bind(this));
    },

    /**
     * @private
     * @returns {Promise}
     */
    _renderChart: function () {
        var pieChart = new ChartWidget(this, this.stats.orders_by_size);
        this.$('.o_fancy_chart').empty();
        return pieChart.appendTo(this.$('.o_fancy_chart'));
    },

    /**
     * @private
     * @returns {Promise<array>}
     */
    _renderStats: function () {
        return this._rpc({
            route: '/awesome_tshirt/statistics'
        });
    },

    /**
     * @private
     */
    _updateControlPanel: function () {
        this.update_control_panel({
            cp_content: {
                $buttons: this.$buttons,
            },
        });
    },

    // --------------------------------------------------------------------------
    // Handlers
    // --------------------------------------------------------------------------

    _onOpenOrders: function (ev) {
        this._openOrders({
            name: ev.data.name,
            domain: ev.data.domain
        });
    },
});


core.action_registry.add('awesome_tshirt.dashboard', Dashboard);

return Dashboard;

});