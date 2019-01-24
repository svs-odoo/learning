odoo.define('awesome_tshirt.ChartWidget', function (require) {
"use strict";

var ajax = require('web.ajax');
var Widget = require('web.Widget');


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

    // --------------------------------------------------------------------------
    // Private
    // --------------------------------------------------------------------------

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
                        'rgba(255,99,132,1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                    ],
                    borderWidth: 1,
                }],
                labels: this.data.sizeLabel,
            },
            options: {
                responsive: true,
            }
        };

        new Chart(this.el, config);
    }
});


return ChartWidget;

});