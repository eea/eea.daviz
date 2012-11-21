var DavizChartSelection = function (btnel) {
        var btn = $(btnel);
        var divparent = btn.parent().parent();
        var metadata = divparent.find('.metadata');
        var popup = $("<div>");

        btn.after(popup);
        popup.html('<p><label>Select chart</label></p>');

        var select = divparent.find('select');
        var cloned_select = select.clone();
        popup.append(cloned_select);

        var uid = metadata.find('.daviz_uid').text();
        var url = metadata.find('.url').text();

        var chart_titles = $(divparent).find('.chart-titles');

        popup.dialog({
            modal:true,
            buttons:{
                'OK':function(){
                    select.replaceWith(cloned_select);
                    chart_titles.find('span').remove();
                    var selected_options = $(cloned_select).find('option:selected');
                    if (!selected_options.length) {
                        chart_titles.append("<span>No chart selected</span>");
                    };
                    selected_options.each(function(){
                        var span = $("<span>");
                        span.addClass("chart-title");
                        span.text($(this).text());
                        var img = $("<img>");
                        var url = $(this).attr('rel');
                        img.attr('src', url+'/image_icon');
                        span.prepend(img);
                        chart_titles.append(span);
                    });
                    var b = this;
                    $.ajax({
                        type:'POST',
                        url:url, 
                        data:{ 
                            'chart':cloned_select.serialize(),
                            'daviz_uid':uid
                        },
                        error:function(){
                            alert("Could not save data on server");
                        },
                        success:function(){
                            $(b).dialog('close');
                        }
                    });
                }, 
                'Cancel':function(){
                    // select.replaceWith(cloned_select);
                    $(this).dialog('close');
                }
            }
        });

};
