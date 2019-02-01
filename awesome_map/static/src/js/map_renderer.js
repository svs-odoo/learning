odoo.define('awesome_map.MapRenderer', function (require) {
"use strict";

var AbstractRenderer = require('web.AbstractRenderer');

var MapRenderer = AbstractRenderer.extend({

    // -------------------------------------------------------------------------
    // Private
    // -------------------------------------------------------------------------

    /**
     * @override
     */
    _render: function () {
        var html = "";
        _.map(this.state, function (data) {
            var style = "display: inline-block;" +
                        "background-color: rgba(255, 255, 255, 0.5);" +
                        "border: 1px solid rgba(0, 0, 0, 0.2);" +
                        "border-radius: 2px;" +
                        "margin: 2px;" +
                        "padding: 2px 8px;";
            html += "<div style=\"" + style + "\">";
            html += "[ " + data.id + " ]</br>lat.: " + data.latitude + "<br/>lon.: " + data.longitude;
            html += "</div>";
        });
        this.$el.html(html);
        return this._super.apply(this, arguments);
    },
});

return MapRenderer;

});
