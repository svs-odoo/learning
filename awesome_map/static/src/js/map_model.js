odoo.define('awesome_map.MapModel', function (require) {
"use strict";

var AbstractModel = require('web.AbstractModel');

var MapModel = AbstractModel.extend({

    init: function () {
        this._super.apply(this, arguments);
        this.data = null;
    },

    // -------------------------------------------------------------------------
    // Public
    // -------------------------------------------------------------------------

    /**
     * @override
     */
    get: function () {
        return this.data;
    },

    /**
     * @override
     */
    load: function (params) {
        var self = this;
        var fields = [
            params.latitude,
            params.longitude,
        ];
        return this._rpc({
            model: params.modelName,
            method: 'search_read',
            context: params.context,
            domain: params.domain,
            fields: fields
        }).then(function (partnersData) {
            self.data = _.map(partnersData, function (data) {
                return {
                    id: data.id,
                    latitude: data[params.latitude],
                    longitude: data[params.longitude],
                };
            });
        });
    },
});

return MapModel;

});
