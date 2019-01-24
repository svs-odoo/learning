odoo.define('awesome_tshirt.MyCounter', function (require) {
"use strict";

var Widget = require('web.Widget');

var MyCounterWidget = Widget.extend({
    template: 'MyCounter',
    events: {
        'click .fa-plus': '_increment',
        'click .fa-minus': '_decrement',
    },

    /**
     * @override
     */
    init: function (parent) {
        this._super.apply(this, arguments);
        this.count = 0;
    },

    // --------------------------------------------------------------------------
    // Private
    // --------------------------------------------------------------------------

    _decrement: function () {
        this.count--;
        this.renderElement();
    },

    _increment: function () {
        this.count++;
        this.renderElement();
    },
});

return MyCounterWidget;

});