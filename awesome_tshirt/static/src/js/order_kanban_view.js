odoo.define('awesome_tshirt.OrderKanbanView', function (require) {
"use strict";

var core = require('web.core');
var KanbanController = require('web.KanbanController');
var KanbanView = require('web.KanbanView');
var viewRegistry = require('web.view_registry');

var qweb = core.qweb;
var _t = core._t;


var OrderKanbanController = KanbanController.extend({
    events: _.extend({}, KanbanController.prototype.events, {
        'click .o_customer': '_onClickCustomer',
        'input .o_customer_search': '_onCustomerSearch',
    }),

    init: function () {
        this._super.apply(this, arguments);
        this.selectedCustomerID = false;
    },

    willStart: function () {
        var superDef = this._super.apply(this, arguments);
        var loadCustomersDef =this._loadCustomers();

        return $.when(superDef, loadCustomersDef);
    },

    start: function () {
        this._super.apply(this, arguments);
        this.$el.addClass('o_order_kanban_view');
    },

    // -------------------------------------------------------------------------
    // Public
    // -------------------------------------------------------------------------

    reload: function (params) {
        params = params || {};
        if (this.selectedCustomerID) {
            params.domain = [['customer_id', '=', this.selectedCustomerID]];
        } else {
            params.domain = [];
        }

        var superDef = this._super(params);
        var loadCustomersDef = this._loadCustomers();

        return $.when(superDef, loadCustomersDef);
    },

    // -------------------------------------------------------------------------
    // Private
    // -------------------------------------------------------------------------

    _loadCustomers: function () {
        var self = this;

        return this._rpc({
            route: '/web/dataset/search_read',
            model: 'res.partner',
            fields: ['display_name'],
            domain: [['has_active_order', '=', true]]
        }).then(function (data) {
            self.customers = data.records;
        });
    },

    _update: function () {
        var self = this;
        this._super.apply(this, arguments).then(function () {
            self.$('.o_kanban_view').prepend(qweb.render('OrderKanban.CustomerSidebar', {
                customers: self.customers,
                selectedCustomerID: self.selectedCustomerID,
            }));
        });
    },

    // -------------------------------------------------------------------------
    // Handlers
    // -------------------------------------------------------------------------

    _onClickCustomer: function (ev) {
        var customerID = $(ev.currentTarget).data('id');

        if (this.selectedCustomerID !== customerID) {
            this.selectedCustomerID = customerID;
        } else {
            this.selectedCustomerID = false;
        }

        this.reload();
    },

    _onCustomerSearch: function (ev) {
        var self = this;
        var filter = ev.target.value;
        // Get an array with only customers' name
        var customersName = _.pluck(this.customers, 'display_name');
        // Filter 'customersName' go get only name matching 'filter'
        var matches = fuzzy.filter(filter, customersName);
        // Get an array with only matched customers' index
        var indexes = _.pluck(matches, 'index');

        var filteredCustomers = _.map(indexes, function (index) {
            return self.customers[index];
        });

        this.$('.o_customer_list').replaceWith(qweb.render('OrderKanban.CustomerList', {
            customers: filteredCustomers,
            selectedCustomerID: this.selectedCustomerID,
        }));
    },
});


var OrderKanbanView = KanbanView.extend({
    config: _.extend({}, KanbanView.prototype.config, {
        Controller: OrderKanbanController,
    }),
    display_name: _t('Customer list'),
    icon: 'fa-th-list',
});


viewRegistry.add('order_kanban_view', OrderKanbanView);

});
