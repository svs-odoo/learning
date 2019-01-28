odoo.define('awesome_tshirt.late_boolean', function (require) {
"use strict";

var basic_fields = require('web.basic_fields');
var field_registry = require('web.field_registry');

var FieldBoolean = basic_fields.FieldBoolean;


var LateBooleanWidget = FieldBoolean.extend({
    className: 'o_late_marker',

    init: function () {
        this._super.apply(this, arguments);
        this.customColors = {
            lateColor: this.nodeOptions.late_color || false,
            notLateColor: this.nodeOptions.not_late_color || false,
        };
    },

    // -------------------------------------------------------------------------
    // Private
    // -------------------------------------------------------------------------

    _render: function () {
        if (this.isSet()) {
            var cssClass = this.value ? 'is-late' : '';

            this.$el.html($('<div>').addClass(cssClass));

            var customColor = this.value ? this.customColors.lateColor : this.customColors.notLateColor;
            if (customColor) {
                this.$el.find('div').css('background-color', customColor);
            }
        }
    },
});


field_registry.add('late_boolean', LateBooleanWidget);

});