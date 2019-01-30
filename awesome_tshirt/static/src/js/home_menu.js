odoo.define('awesome_tshirt.HomeMenu', function (require) {
"use strict";

var core = require('web.core');
var HomeMenu = require('web_enterprise.HomeMenu');

var _t = core._t;


HomeMenu.include({

    /**
     * @override
     */
    willStart: function () {
        var self = this;
        this._super.apply(this, arguments);

        this.textMessage = _t('Yipi-kee-aye, mother-father !');

        var def = this._rpc({
            route: '/awesome_tshirt/bafienistalkingtoyou',
        });
        def.then(function (receivedText) {
            self.textMessage = receivedText;
        });

        return def;
    },


    // -------------------------------------------------------------------------
    // Private
    // -------------------------------------------------------------------------

    /**
     * @override
     */
    _render: function () {
        this._super.apply(this, arguments);

        var $message = $('<div>');
        $message.addClass('o_custom_message alert-info');
        $message.text(this.textMessage);

        this.$('.o_custom_message').remove();
        $message.prependTo(this.$el);
    }
});

});
