odoo.define('awesome_map.MapView', function (require) {
"use strict";


var AbstractView = require('web.AbstractView');
var core = require('web.core');
var MapController = require('awesome_map.MapController');
var MapModel = require('awesome_map.MapModel');
var MapRenderer = require('awesome_map.MapRenderer');
var viewRegistry = require('web.view_registry');

var _lt = core._lt;


var MapView = AbstractView.extend({
    icon: 'fa-globe',
    config: {
        Controller: MapController,
        Model: MapModel,
        Renderer: MapRenderer,
    },
    display_name: _lt('Map'),

    init: function () {
        this._super.apply(this, arguments);
        this.loadParams.latitude = this.arch.attrs.latitude;
        this.loadParams.longitude = this.arch.attrs.longitude;
    },
});

viewRegistry.add('map', MapView);

});
