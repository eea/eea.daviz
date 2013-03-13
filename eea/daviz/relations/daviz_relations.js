/*jslint white: false, browser: true, devel: true */

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

        // we need an array with the selected charts and their embed type
        select_charts_selection.find('input').each(function(i,el){
            var xel = jQuery(el);
            chart_selection.push({
                id:xel.attr('name'),
                embed:xel.attr('value')
            });
        });
        // console.log("Chart selection", chart_selection);

        // we take the charts from the select and put them in a JS array
        select_charts_definition.find('option').each(function(i,el){
            var xel = jQuery(el);
            chart_definitions.push({
                id:xel.attr('value'),
                label:xel.text(),
                image:xel.attr('rel')
            });
        });
        // TODO: reorder charts based on order from select_charts
        // console.log("Chart definition", chart_definitions);

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

                var p = jQuery("<li style='overflow:hidden; display:list-item; clear:both' class='list-item'>");
                var chk_div = jQuery("<div/>");
                if (!is_activated) {
                    chk_div.css({'display':'none'});
                    p.addClass('disabled');
                }

                var disabler = jQuery("<input>").attr({
                    'type':'checkbox',
                    'class':'disabler',
                    'checked':is_activated
                });
                disabler.change(function(){
                    chk_div.fadeToggle();
                    $(this).parent().toggleClass('disabled');
                });
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
        var height = Math.min(popup.height(), 500) + 100;

        popup.dialog({
            'title':'Select charts',
            modal: true,
            minHeight:height,
            'height':height,
            buttons: {
                'OK': function () {

                    // this is what the input_nodes look like
                    //<input type="checkbox" name="live" class="selector" value="chart_1">
                    var input_nodes = nodes.find("li:not(.disabled) input.selector:checked");
                    // console.log("Input nodes", input_nodes);

                    // Show which charts have been selected;
                    var selected_charts = chart_titles.find('.selected_charts');
                    selected_charts.empty();
                    if (!input_nodes.length){
                        selected_charts.append("<span>No chart selected</span>");
                    }

                    // save options into select_charts_selection
                    select_charts_selection.empty();
                    $(input_nodes).each(function(){
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
                        // console.log("Info node", info);

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
