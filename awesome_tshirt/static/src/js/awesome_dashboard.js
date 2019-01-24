odoo.define('awesome_tshirt.dashboard', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
// var ControlPanelMixin = require('web.ControlPanelMixin');
var core = require('web.core');
var MyCounter = require('awesome_tshirt.MyCounter');

var Dashboard = AbstractAction.extend({
    start: function () {
        var myCounter = new MyCounter();

        var promCounter = myCounter.appendTo(this.$el);
        var promSuper = this._super.apply(this, arguments);

        return Promise.all([promCounter, promSuper]);
    }
});

core.action_registry.add('awesome_tshirt.dashboard', Dashboard);

return Dashboard;

});