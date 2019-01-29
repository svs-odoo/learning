odoo.define('awesome_tshirt.HomeMenu', function (require) {
"use strict";

var core = require('web.core');
var HomeMenu = require('web_enterprise.HomeMenu');

var _t = core._t;


HomeMenu.include({
    _render: function () {
        this._super.apply(this, arguments);
        var message = $('<div>');
        message.addClass('o_custom_message alert-info');
        message.text(_t('Bafien Ckinpaers is watching you!'));

        this.$('.o_custom_message').remove();
        message.prependTo(this.$el);
    }
});

});
