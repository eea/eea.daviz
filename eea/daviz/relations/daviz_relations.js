/*jslint white: false, browser: true, devel: true */
/*global  jQuery: false, DavizInlineResizer: true */

// InternetExplorer 8 compatibility
if (!Array.prototype.indexOf) {
    Array.prototype.indexOf = function (searchElement /*, fromIndex */ ) {
        "use strict";
        if (this === null) {
            throw new TypeError();
        }
        var t = {};
        var len = t.length >>> 0;
        if (len === 0) {
            return -1;
        }
        var n = 0;
        if (arguments.length > 1) {
            n = Number(arguments[1]);
            if (n != n) { // shortcut for verifying if it's NaN
                n = 0;
            } else if (n !== 0 && n !== Infinity && n !== -Infinity) {
                n = (n > 0 || -1) * Math.floor(Math.abs(n));
            }
        }
        if (n >= len) {
            return -1;
        }
        var k = n >= 0 ? n : Math.max(len - Math.abs(n), 0);
        for (; k < len; k++) {
            if (k in t && t[k] === searchElement) {
                return k;
            }
        }
        return -1;
    };
}

var DavizChartSelection = function (btnel) {
        var btn            = jQuery(btnel);
        var chart_titles   = btn.parent().parent();
        var divparent      = chart_titles.parent();
        var metadata       = divparent.find('.metadata');
        var uid            = metadata.find('.daviz_uid').text();
        var url            = metadata.find('.url').text();
        var select_charts_definition = metadata.find("select.select_charts_definition");
        var select_charts_selection = metadata.find(".select_charts_selection");

        var popup = jQuery("<div/>");

        var chart_definitions = [];        // full chart options
        var chart_selection = [];          // selected charts [chart_id, embed_type]
        var order = [];     // temporary array used to hold order

        // we need an array with the selected charts and their embed type
        select_charts_selection.find('input').each(function(i,el){
            var xel = jQuery(el);
            var chart_id = xel.attr('name');
            chart_selection.push({
                id:chart_id,
                embed:xel.attr('value')
            });
            order.push(chart_id);
        });

        // we take the charts from the select and put them in a JS array
        select_charts_definition.find('option').each(function(i,el){
            var xel = jQuery(el);
            var chart_id = xel.attr('value');
            chart_definitions.push({
                id:chart_id,
                label:xel.text(),
                image:xel.attr('rel')
            });
            if (order.indexOf(chart_id) === -1) { order.push(chart_id); }
        });

        function sorter(a,b) {
            return order.indexOf(a.id) > order.indexOf(b.id);
        }

        chart_definitions.sort(sorter);

        // returns embed type given a chart_id
        // will return null if chart is not selected
        function get_embed_type(chart_id){
            var embed = null;
            jQuery(chart_selection).each(function(){
                if (chart_id == this.id){
                    embed = this.embed;
                }
            });
            return embed;
        }

        // return all definition info for the chart_id
        function get_info(chart_id){
            var info = null;
            jQuery(chart_definitions).each(function(){
                if (chart_id == this.id){
                    info = this;
                }
            });
            return info;
        }

        function make_chart_options(charts){
            // builds the chart selection area
            var thisel = jQuery("<ul class='reorder' style='padding:0' />");


            // TODO: preserve order from selected charts
            jQuery(charts).each(function(){
                var info = this;
                var chart_id = info.id;
                var embed_type = get_embed_type(chart_id);
                var is_activated = (embed_type !== null);
                // check for exhibits - if so, the current chart is not supported for embedding
                var is_exhibit = ((chart_id == 'daviz.map') || (chart_id == 'daviz.tabular') || (chart_id == 'daviz.tile') || (chart_id == 'daviz.timeline'));

                var p = jQuery("<li style='overflow:hidden; display:list-item; clear:both' class='list-item'>");
                var chk_div = jQuery("<div/>");
                if ((!is_activated) && (!is_exhibit)) {
                    chk_div.css({'display':'none'});
                    p.addClass('disabled');
                }

                var disabler = "";
                if (!is_exhibit) {
                    disabler = jQuery("<input>").attr({
                        'type':'checkbox',
                        'class':'disabler',
                        'checked':is_activated
                    });
                    disabler.change(function(){
                        chk_div.fadeToggle();
                        jQuery(this).parent().toggleClass('disabled');
                    });
                }
                var title = jQuery("<span style='font-weight:bold'>");
                title.text(" " + info.label + ':');
                p.append(disabler, title, "<br/>", chk_div);

                p.prepend(jQuery("<img>").attr('src', info.image+'/image_thumb').css({
                    'float':'left',
                    'border':'1px solid black',
                    'margin':'3px'
                }));
                p.prepend(jQuery("<span />").attr({
                    'title':'Drag & drop to set order',
                    'class':'handler ui-icon ui-icon-arrowthick-2-n-s',
                    'style':'float:left'
                }));

                if (!is_exhibit) {
                    var inp_live = jQuery("<input>").attr({
                        'type':'checkbox',
                        'name':'live',
                        'class':'selector',
                        'value':chart_id
                        });
                    var inp_preview = inp_live.clone();
                    inp_preview.attr('name', "preview");
                    // to fill in here

                    if (embed_type === 'preview') {
                        inp_preview.attr('checked', true);
                    } else {    // live is default
                        inp_live.attr('checked', true);
                    }

                    inp_live.change(function(){
                        var checked = inp_preview.attr('checked');
                        inp_preview.attr('checked', !checked);
                    });
                    inp_preview.change(function(){
                        var checked = inp_live.attr('checked');
                        inp_live.attr('checked', !checked);
                    });
                    chk_div.append(inp_live, 'live', inp_preview, 'preview');
                } else {
                    chk_div.html("Exhibits are currently not supported for embedding.");
                }
                thisel.append(p);
            });

            return thisel;
        }

        var nodes = make_chart_options(chart_definitions);

        btn.after(popup);
        popup.append(nodes);

        popup.sortable({
            handle:'.handler',
            items:'.list-item',
            placeholder: 'ui-state-highlight',
            axis:'y'
        });

        // we need to hardcode height otherwise the dialog gets too minified
        var width = Math.min(popup.width(), 500) + 100;
        var height = Math.min(popup.height(), 500) + 200;

        popup.dialog({
            'title':'Select charts',
            modal: true,
            minWidth:width,
            'width':width,
            minHeight:height,
            'height':height,
            buttons: {
                'OK': function () {

                    // this is what the input_nodes look like
                    //<input type="checkbox" name="live" class="selector" value="chart_1">
                    var input_nodes = nodes.find("li:not(.disabled) input.selector:checked");

                    // Show which charts have been selected;
                    var selected_charts = chart_titles.find('.selected_charts');
                    selected_charts.empty();
                    if (!input_nodes.length){
                        selected_charts.append("<span>No chart selected</span>");
                    }

                    // save options into select_charts_selection
                    select_charts_selection.empty();
                    jQuery(input_nodes).each(function(){
                        var node = jQuery(this);
                        var chart_id = node.attr('value');
                        var embed = node.attr('name');
                        jQuery("<input/>", {
                            'type':'hidden',
                            'value':embed,
                            'name':chart_id
                         }).appendTo(select_charts_selection);

                        // display that the chart has been selected;

                        var info = get_info(chart_id);

                        var span = jQuery("<span>");
                        span.addClass("chart-title");
                        span.text(info.label + ": " + embed);
                        // var img = jQuery("<img>", {'src':info.image + '/image_icon'});
                        // span.prepend(img);
                        selected_charts.append(span);

                    });

                    //return jQuery(this).dialog('close');

                    var b = this;
                    jQuery.ajax({
                        type: 'POST',
                        url: url,
                        data: {
                            'daviz_uid': uid,
                            'charts':select_charts_selection.find("input").serialize()
                        },
                        error: function () {
                            alert("Could not save data on server");
                        },
                        success: function () {
                            jQuery(b).dialog('close');
                        }
                    });
                },
                'Cancel': function () {
                    // select.replaceWith(cloned_select);
                    jQuery(this).dialog('close');
                }
            }
        });

    };

jQuery(document).ready(function($){
    // handle inline resize
    jQuery(document).delegate(".googlechart_dashboard", "google-chart-inlineresized", function(evt, value){
        var metadata = jQuery(this).closest(".embedded-daviz-visualization").find(".metadata");
        var part_url = metadata.find(".part_url").text();
        var uid = metadata.find(".daviz_uid").text();
        value.daviz_uid = uid;
        value.chart_id = value.chart_id;
        jQuery.ajax({
            type: 'POST',
            url: part_url + "/@@set_daviz_size",
            data: value,
            error: function(){
                alert("Could not save data on server");
            },
            success: function(data){
            }
        });
    });
});
