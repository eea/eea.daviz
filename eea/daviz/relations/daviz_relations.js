/*jslint white: true, browser: true, devel: true */
var DavizChartSelection = function (btnel) {
        var btn = jQuery(btnel);
        var divparent = btn.parent().parent();
        var metadata = divparent.find('.metadata');
        var popup = jQuery("<div>");

        btn.after(popup);
        popup.html('<p><label>Select chart</label></p>');

        var select = divparent.find('select');
        var cloned_select = select.clone();
        popup.append(cloned_select);

        var uid = metadata.find('.daviz_uid').text();
        var url = metadata.find('.url').text();

        var chart_titles = jQuery(divparent).find('.chart-titles');

        popup.dialog({
            modal: true,
            buttons: {
                'OK': function () {
                    select.replaceWith(cloned_select);
                    chart_titles.find('span').remove();
                    var selected_options = jQuery(cloned_select).find('option:selected');
                    if (!selected_options.length) {
                        chart_titles.append("<span>No chart selected</span>");
                    }
                    selected_options.each(function () {
                        var span = jQuery("<span>");
                        span.addClass("chart-title");
                        span.text(jQuery(this).text());
                        var img = jQuery("<img>");
                        var url = jQuery(this).attr('rel');
                        img.attr('src', url + '/image_icon');
                        span.prepend(img);
                        chart_titles.append(span);
                    });
                    var b = this;
                    jQuery.ajax({
                        type: 'POST',
                        url: url, 
                        data: { 
                            'chart': cloned_select.serialize(),
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
