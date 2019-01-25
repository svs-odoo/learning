odoo.define('awesome_tshirt.preview_widget', function (require) {
"use strict";

var basic_fields = require('web.basic_fields');
var core = require('web.core');
var field_registry = require('web.field_registry');

var _t = core._t;
var FieldChar = basic_fields.FieldChar;


var ImagePreviewWidget = FieldChar.extend({

    isSet: function () {
        return true;
    },

    // -------------------------------------------------------------------------
    // Private
    // -------------------------------------------------------------------------

    _renderReadonly: function () {
        if (this.value) {
            this.$el.html($('<img>', {
                src: this.value,
                style: 'max-width: 300px',
            }));
        } else {
            this.$el.text(_t('MISSING TSHIRT DESIGN'));
            this.$el.addClass('alert-danger');
        }
    },
});


field_registry.add('image_preview', ImagePreviewWidget);

});