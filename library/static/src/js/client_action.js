odoo.define('library.client_action', function (require) {
"use strict";


var ChartWidget = require('library.ChartWidget');
var ControlPanelMixin = require('web.ControlPanelMixin');
var core = require('web.core');
var AbstractAction = require('web.AbstractAction');

var QWeb = core.qweb;


var ClientAction = AbstractAction.extend(ControlPanelMixin, {
    template: 'LibraryDashboard',
    custom_events: {
        'openBooks': '_onOpenBooks'
    },

    /**
     * @override
     */
    init: function (parent, action) {
        this._super.apply(this, arguments);
        this.action_manager = parent;
        this.action = action;
    },
    /**
     * @override
     */
    willStart: function () {
        var self = this;

        var prom1 = this._rpc({route: '/library/statistics'}).then(function (stats) {
            self.stats = stats;
        });
        var prom2 = self._super.apply(this, arguments);

        return Promise.all([prom1, prom2]);
    },
    /**
     * @override
     */
    start: function () {
        var self = this;
        var args = arguments;

        this._renderButtons();
        this._updateControlPanel();
        var renderCharts = this._renderCharts;
        return self._super.apply(self, args).then(function () {
            return renderCharts.call(self);
        });
    },
    /**
     * Called when coming back with the breadcrumbs
     *
     * @override
     */
    do_show: function () {
        this._super.apply(this, arguments);
    },

    // --------------------------------------------------------------------------
    // Private
    // --------------------------------------------------------------------------

    /**
     * @private
     */
    _renderButtons: function () {
        this.$buttons = $(QWeb.render('LibraryDashboard.Buttons'));
        this.$buttons.on('click', '.o_lost_books', this._onOpenLostBooks.bind(this));
        this.$buttons.on('click', '.o_bad_customers', this._onOpenBadCustomer.bind(this));
    },
    /**
     * @private
     */
    _renderCharts: function () {
        var chart = new ChartWidget(this, this.stats);
        this.$('.o_fancy_chart').empty();

        return chart.appendTo(this.$('.o_fancy_chart'));
    },
    /**
     * @private
     */
    _updateControlPanel: function () {
        this.update_control_panel({
            breadcrumbs: this.action_manager._getBreadcrumbs(),
            cp_content: {
                $buttons: this.$buttons
            }
        });
    },

    // --------------------------------------------------------------------------
    // Handlers
    // --------------------------------------------------------------------------

    /**
     * @private
     */
    _onOpenBadCustomer: function () {
        this.do_action('library.bad_customer_action');
    },
    /**
     * @param {OdooEvent} ev
     * @private
     */
    _onOpenBooks: function (ev) {
        var validState = ['availible', 'rented', 'lost'];
        var action;
        var state = ev.data.state;

        if (validState.includes(state)) {
            action = 'library.copy_' + state + '_action';
        }

        if (action) {
            this.do_action(action);
        } else {
            this.do_warn('Wrong state, "' + state + '" isn\'t valid.');
        }
    },
    /**
     * @private
     */
    _onOpenLostBooks: function () {
        this.do_action('library.copy_lost_action');
    },
});

core.action_registry.add('library.dashboard', ClientAction);

});
