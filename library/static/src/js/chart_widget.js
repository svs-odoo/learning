odoo.define('library.ChartWidget', function (require) {
"use strict";

var ajax = require('web.ajax');
var Widget = require('web.Widget');

var ChartWidget = Widget.extend({
    tagName: 'canvas',
    jsLibs: ['library/static/lib/chart_js/Chart.js'],

    /**
     * @override
     */
    init: function (parent, data) {
        this._super.apply(this, arguments);
        this.data = data;
    },
    /**
     * @override
     */
    willStart: function () {
        return Promise.all([
            ajax.loadLibs(this),
            this._super.apply(this, arguments)
        ]);
    },
    /**
     * @override
     */
    start: function () {
        this._renderChart();
        return this._super.apply(this, arguments);
    },

    // --------------------------------------------------------------------------
    // Private
    // --------------------------------------------------------------------------
    _renderChart: function () {
        var self = this;
        new Chart(this.el, {
            type: 'pie',
            data: {
                labels: ['Availible', 'Rented', 'Lost'],
                datasets: [{
                    label: '# of Books',
                    data: [
                        this.data.nb_availible_book,
                        this.data.nb_rented_book,
                        this.data.nb_lost_book
                    ],
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 99, 132, 0.2)',
                    ],
                    borderColor: [
                        'rgb(75, 192, 192)',
                        'rgb(54, 162, 235)',
                        'rgb(255, 99, 132)',
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                onClick: function (event, chartElements) {
                    var types = ['availible', 'rented', 'lost'];
                    if (chartElements && chartElements.length) {
                        self.trigger_up('openBooks', {state: types[chartElements[0]._index]});
                    }
                }
            }
        });
    },
});

return ChartWidget;

});