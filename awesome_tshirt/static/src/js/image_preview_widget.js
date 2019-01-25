odoo.define('awesome_tshirt.preview_widget', function (require) {
"use strict";

var basic_fields = require('web.basic_fields');
var field_registry = require('web.field_registry');

var FieldChar = basic_fields.FieldChar;


var ImagePreviewWidget = FieldChar.extend({

    // -------------------------------------------------------------------------
    // Private
    // -------------------------------------------------------------------------

    _renderReadonly: function () {
        if (this.isSet()) {
            this.$el.html($('<img>', {src: this.value}));
        }
    },
});


field_registry.add('image_preview', ImagePreviewWidget);

});