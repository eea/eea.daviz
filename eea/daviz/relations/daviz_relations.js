/*jslint white: false, browser: true, devel: true */

var DavizChartSelection = function (btnel) {
        var btn            = jQuery(btnel);
        var chart_titles   = btn.parent().parent();
        var divparent      = chart_titles.parent();
        var metadata       = divparent.find('.metadata');
        var uid            = metadata.find('.daviz_uid').text();
        var url            = metadata.find('.url').text();
        var select         = metadata.find("select.all_charts");
        var select_live    = jQuery("select[name='live']", metadata);
        var select_preview = jQuery("select[name='preview']", metadata);

        var popup = jQuery("<div>");

        var charts = [];        // full chart options
        var lives = [];         // just chart ids which are for live viewing
        var previews = [];      // just chartids which are for preview viewing

        select.find('option').each(function(i,el){
            var xel = jQuery(el);
            charts.push([xel.attr('value'), xel.text(), xel.attr('rel')]);
        });

        select_live.find('option').each(function(){lives.push(jQuery(this).attr('value'));});
        select_preview.find('option').each(function(){previews.push(jQuery(this).attr('value'));});

        function make_chart_options(charts){
            var thisel = jQuery("<div>");

            jQuery(charts).each(function(index, v){
                var chart_id = v[0];
                var is_activated = false;
                if ((lives.indexOf(chart_id) >= 0)||(previews.indexOf(chart_id) >=0)){
                    is_activated = true;
                }
                var p = jQuery("<p style='overflow:hidden'>");
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
                title.text(" " + v[1] + ':');
                p.append(disabler, title, "<br/>", chk_div); 

                p.prepend(jQuery("<img>").attr('src', v[2]+'/image_thumb').css({
                    'float':'left',
                    'border':'1px solid black',
                    'margin':'3px'
                }));

                var inp_live = jQuery("<input>").attr({
                    'type':'checkbox',
                    'name':'live',
                    'value':chart_id
                    });
                var inp_preview = inp_live.clone();
                inp_preview.attr('name', "preview");

                var flag = false;
                if (previews.indexOf(chart_id) >=0) {
                    inp_preview.attr('checked', true);
                    flag = true;
                }
                if (lives.indexOf(chart_id) >= 0 || !flag) { // always enable live if not previewed
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

        var nodes = make_chart_options(charts);

        btn.after(popup);
        popup.append(nodes);

        popup.dialog({
            modal: true,
            'title':'Select charts',
            buttons: {
                'OK': function () {

                    var l_nodes = nodes.find("p:not(.disabled) input[name='live']:checked");
                    var p_nodes = nodes.find("p:not(.disabled) input[name='preview']:checked");

                    var lives = [];
                    var previews = [];

                    $(l_nodes).each(function(){
                            lives.push($(this).val());
                    });

                    $(p_nodes).each(function(){
                            previews.push($(this).val());
                    });

                    select_preview.empty();
                    $(previews).each(function(){
                        jQuery("<option/>", {'value':this, 
                                             'textContent':this, 
                                             'selected':true}).appendTo(select_preview);
                    });

                    select_live.empty();
                    $(lives).each(function(){
                        jQuery("<option/>", {'value':this, 
                                             'textContent':this, 
                                             'selected':true}).appendTo(select_live);
                    });


                    var selected_charts = chart_titles.find('.selected_charts');
                    selected_charts.empty();
                    if (!(lives.length || previews.length)){
                        selected_charts.append("<span>No chart selected</span>");
                    }

                    jQuery("option", select).each(function(i, v){
                        var option = jQuery(v);
                        var chart_id = option.attr('value');
                        var is_activated = false;
                        if (lives.indexOf(chart_id) >= 0) {
                            is_activated = 'live';
                        }
                        if(previews.indexOf(chart_id) >=0) {
                            is_activated = 'preview';
                        }
                        if (is_activated){
                            var span = jQuery("<span>");
                            span.addClass("chart-title");
                            span.text(option.attr('textContent') + ": " + is_activated);
                            var img = jQuery("<img>");
                            var url = jQuery(option).attr('rel');
                            img.attr('src', url + '/image_icon');
                            //span.prepend(img);
                            selected_charts.append(span);
                        }
                    });

                    //return jQuery(this).dialog('close');

                    var b = this;
                    jQuery.ajax({
                        type: 'POST',
                        url: url, 
                        data: { 
                            'previews': select_preview.serialize(),
                            'lives':select_live.serialize(),
                            'daviz_uid': uid
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
