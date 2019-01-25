odoo.define('awesome_tshirt.ChartWidget', function (require) {
"use strict";

var ajax = require('web.ajax');
var core = require('web.core');
var Widget = require('web.Widget');

var _t = core._t;


var ChartWidget = Widget.extend({
    tagName: 'canvas',
    libs: {
        jsLibs: ['/awesome_tshirt/static/lib/chart.js/Chart.js'],
    },

    /**
     * @override
     */
    init: function (parent, orders_by_size) {
        this._super.apply(this, arguments);
        this.data = {
            sizeLabel: ['S', 'M', 'L', 'XL', 'XXL'],
            color: [
                '#AF2BBF',
                '#BF684E',
                '#BF6DBB',
                '#925FB7',
                '#785BC6',
            ],
            borderColor: [
                '#AF2BBF',
                '#BF684E',
                '#BF6DBB',
                '#925FB7',
                '#785BC6',
            ],
            orders_by_size: orders_by_size || {},
        };
    },

    /**
     * @override
     */
    willStart: function () {
        return Promise.all([
            this._super.apply(this, arguments),
            ajax.loadLibs(this.libs),
        ]);
    },

    /**
     * @override
     */
    start: function () {
        this._renderPieChart();
        this._super.apply(this, arguments);
    },

    // -------------------------------------------------------------------------
    // Private
    // -------------------------------------------------------------------------

    /**
     * @private
     */
    _renderPieChart: function () {
        var self = this;
        var chartData = _.map(this.data.sizeLabel, function (size) {
            size = size.toLowerCase();
            return self.data.orders_by_size[size] || 0;
        });

        var config = {
            type: 'pie',
            data: {
                datasets: [{
                    label: "Size",
                    data: chartData,
                    backgroundColor: this.data.color,
                    borderColor: [
                        'rgb(0, 0, 0)',
                        'rgb(0, 0, 0)',
                        'rgb(0, 0, 0)',
                        'rgb(0, 0, 0)',
                        'rgb(0, 0, 0)',
                    ],
                    borderWidth: 1,
                }],
                labels: this.data.sizeLabel,
            },
            options: {
                responsive: true,
                onClick: this._onChartClicked.bind(this),
            }
        };

        new Chart(this.el, config);
    },


    // -------------------------------------------------------------------------
    // Handlers
    // -------------------------------------------------------------------------

    _onChartClicked: function (ev, chartElement) {
        if (chartElement[0]) {
            var index = chartElement[0]._index;
            var orders_size = chartElement[0]._chart.config.data.labels[index];

            this.trigger_up('open_orders', {
                name: _t('Orders for size ') + orders_size,
                domain: [
                    ['size', '=', orders_size.toLowerCase()],
                    ['state', '!=', 'cancelled'],
                ],
            });
        }
    },
});


return ChartWidget;

});