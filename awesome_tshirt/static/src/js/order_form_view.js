odoo.define('awesome_tshirt.OrderFormView', function (require) {
"use strict";

var core = require('web.core');
var FormController = require('web.FormController');
var FormView = require('web.FormView');
var viewRegistry = require('web.view_registry');

var qweb = core.qweb;


var OrderFormController = FormController.extend({

    init: function () {
        this._super.apply(this, arguments);
        this.printing = false;
    },

    renderButtons: function () {
        this._super.apply(this, arguments);
        this.$buttons.addClass('o_order_form_buttons');
        this.$buttons.prepend(qweb.render('OrderFormView.Buttons'));
        this.$buttons.on('click', '.o_print_label', this._onPrintLabel.bind(this));
    },

    // -------------------------------------------------------------------------
    // Private
    // -------------------------------------------------------------------------

    _updateButtons: function () {
        this._super.apply(this, arguments);

        var disabled = this.mode === 'edit';
        var data = this.model.get(this.handle, {raw: true}).data;
        var printed = data.state === 'printed' && data.customer_id;

        var printButton = this.$buttons.find('.o_print_label');
        printButton.toggleClass('btn-primary', printed)
            .toggleClass('btn-secondary', !printed)
            .attr('disabled', !!disabled);
    },

    // -------------------------------------------------------------------------
    // Handlers
    // -------------------------------------------------------------------------

    _onPrintLabel: function () {
        if (this.printing) {
            // Must waiting current print is finished before print again.
            return;
        }

        var res_id = this.model.get(this.handle, {raw: true}).res_id;

        var self = this;
        this.printing = true;
        var always = function () {
            self.printing = false;
        };

        this._rpc({
            model: 'awesome_tshirt.order',
            method: 'print_label',
            args: [res_id],
        }).then(always, always);
    },
});


var OrderFormView = FormView.extend({
    config: _.extend({}, FormView.prototype.config, {
        Controller: OrderFormController,
    }),
});

viewRegistry.add('order_form_view', OrderFormView);

});