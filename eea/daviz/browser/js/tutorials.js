

jQuery(document).ready(function(){
  jQuery("#daviz-tutorials").DavizTutorials();
});

if(window.DavizEdit === undefined){
  var DavizEdit = {'version': '4.0'};
}

DavizEdit.DavizTutorials = function(context, options){
    var self = this;
    self.context = context;
    self.initialize(options);
};

DavizEdit.DavizTutorials.prototype = {

    initialize: function(options){
        var self = this;

        //TODO: move tags in youtube video descriptions
        var video_tags = {
            "My first DaViz | DaViz tutorial" : "create, Basic tutorials",
            "Create DaViz - data via copy and paste | DaViz tutorial" : "create, Basic tutorials",
            "Create DaViz - data via CSV/TSV upload | DaViz tutorial" : "create, Basic tutorials",
            "Create DaViz - data from URL (external site) | DaViz tutorial" : "create, Basic tutorials",
            "Create DaViz - data from another DaViz | DaViz tutorial" : "create, Basic tutorials",
            "Create DaViz - data from SPARQL query (Linked Data) | DaViz tutorial" : "create, Basic tutorials",
            "Basic DaViz editing | DaViz tutorial" : "edit chart, Basic tutorials",
            "Add visualization - Bar chart | DaViz tutorial" : "edit chart, bar, Basic tutorials",
            "Add visualization - Column chart | DaViz tutorial" : "edit chart, column, Basic tutorials",
            "Basic chart customization | DaViz tutorial" : "edit chart, bar, Basic tutorials",
            "Add visualization - Pie chart | DaViz tutorial" : "edit chart, pie, Basic tutorials",
            "Add visualization - Line chart | DaViz tutorial" : "edit chart, line, Basic tutorials",
            "Add visualization - Map chart | DaViz tutorial" : "edit chart, map, Basic tutorials",
            "Rearrange charts | DaViz Tutorial" : "edit chart, Basic tutorials",
            "Add Visualisation - Chart with intervals | DaViz tutorial" : "edit chart, intervals, Basic tutorials",
            "Introduction to Exhibit visualizations | DaViz tutorial" : "exhibit, Advanced tutorials",
            "Map view - Exhibit visualization | DaViz tutorial" : "exhibit, map, Advanced tutorials",
            "Tabular view - Exhibit visualization | DaViz tutorial" : "exhibit, tabular, Advanced tutorials",
            "Timeline view - Exhibit visualization | DaViz tutorial" : "exhibit, timeline, Advanced tutorials",
            "Tile view - Exhibit visualization | DaViz tutorial" : "exhibit, tile, Advanced tutorials",
            "Lens - Exhibit visualization | DaViz tutorial" : "exhibit, lens, Advanced tutorials",
            "Facets - Exhibit visualization | DaViz tutorial" : "exhibit, facets, Advanced tutorials",
            "Hide/Show table columns - Using the table configurator | DaViz tutorial" : "edit chart, table, hide/show, Advanced tutorials",
            "Table formatters - Using the table configurator | DaViz tutorial" : "edit chart, table, formatters, Advanced tutorials",
            "Unpivot table - Using the table configurator | DaViz tutorial" : "edit chart, table, unpivot, Advanced tutorials",
            "Pivot table - Using the table configurator | DaViz tutorial" : "edit chart, table, pivot, Advanced tutorials",
            "Filter - Using the table configurator | DaViz tutorial" : "edit chart, table, rowfilters, Advanced tutorials",
            "Scatterplots matrix - Using the table configurator | DaViz tutorial" : "edit chart, table, scatterplots, matrices, Advanced tutorials",
            "Other matrices - Using the table configurator | DaViz tutorial" : "edit chart, table, matrices, Advanced tutorials",
            "Adding Filters, sorting and chart notes - Interactive charts | DaViz tutorial" : "edit chart, filters, notes, sort, Advanced tutorials",
            "Creating dashboards - Combine multiple charts in a dashboard | DaViz tutorial" : "dashboard, Advanced tutorials",
            "Embed charts or dashboards in other sites - Embedding in webpages | DaViz tutorial" : "view, embed, chart, dashboard, Advanced tutorials",
            "Keep chart's filter settings when embedding - Embedding in webpages | DaViz tutorial" : "view, embed, chart, dashboard, filters, Advanced tutorials",
            "Embed a static image - Embedding in webpages | DaViz tutorial" : "view, embed, chart, Advanced tutorials",
            "Customize CSS when embedding - Embedding in webpages | DaViz tutorial" : "view, embed, csscustomization, Advanced tutorials",
            "Embed and use DaViz in EEA indicators | DaViz tutorial" : "view, embed, chart, dashboard, indicators, Advanced tutorials",
            "Data visualisation web tool (DaViz): Intro and main features overview" : "intro",
            "Data Analysis - Differences | DaViz tutorial" : "differences, chart, data analysis, Basic tutorials",
            "Data Analysis - Trendlines | DaViz tutorial avi" : "trendlines, chart, data analysis, Basic tutorials",
            "Data Analysis - Intervals | DaViz tutorial" : "intervals, chart, data analysis, Basic tutorials"
        };

        this.context.addClass("daviz-tutorials");

        jQuery(window).bind('hashchange', function(evt){
            jQuery(".daviz-tutorials-main-playlist").scrollTop(0);
            var hash = window.location.hash;
            if (hash === "") {
                hash = "#All tutorials";
            }

            hash = hash.substr(1);
            self.updateTutorials(hash);
        });

        jQuery("<iframe>")
            .attr("width", 580)
            .attr("height", 315)
            .attr("frameborder", 0)
            .attr("allowfullscreen", true)
            .attr("src", "")
            .appendTo(this.context);

        jQuery("<div>")
            .addClass("daviz-tutorials-search")
            .appendTo(this.context);

        jQuery("<div>")
            .addClass("daviz-tutorials-main-playlist-title")
            .css("height", 20)
            .appendTo(".daviz-tutorials-search");

        jQuery("<div>")
            .addClass("daviz-tutorials-main-playlist")
            .css("height", self.context.find("iframe").attr("height") - 30)
            .appendTo(".daviz-tutorials-search");

        jQuery("<div>")
            .addClass("daviz-tutorials-tagcloud")
            .data("tags", {})
            .css("height", 400)
            .appendTo(".daviz-tutorials-search");

        var playlists = ["PLVPSQz7ahsByeq8nVKC7TT9apArEXBrV0", "PLVPSQz7ahsBxbe8pwzFWLQuvDSP9JFn8I"];
        jQuery.each(playlists, function(playlist_idx, playlist){
            jQuery.getJSON("http://gdata.youtube.com/feeds/api/playlists/" + playlist + "?v=2&alt=jsonc&orderby=position", function(data){
                var main_playlist = self.context.find(".daviz-tutorials-main-playlist");
                var div = jQuery("<div>")
                    .addClass("daviz-tutorials-playlist")
                    .attr("playlistid", data.data.id)
                    .appendTo(main_playlist);
                jQuery("<div>")
                    .addClass("daviz-tutorials-videos")
                    .appendTo(".daviz-tutorials-playlist[playlistid='" + data.data.id + "']");
                jQuery.each(data.data.items, function(item_idx, item){
//                    var description = [item.video.description, video_tags[item.video.title]].join(",");
                    var description = video_tags[item.video.title];
                    var tmp_tags = description.split(",");
                    tmp_tags.push("All tutorials");
                    var tags = [];
                    for (i = 0; i < tmp_tags.length; i++) {
                        var tag = tmp_tags[i].trim();
                        if (tag !== "") {
                            tags.push(tag);
                        }
                    }
                    self.updateTagCloud(tags);
                    var img = jQuery("<img>")
                        .attr("src", item.video.thumbnail.sqDefault);
                    var iframe = self.context.find("iframe");
                    var item_obj = jQuery("<div>")
                        .addClass("daviz-tutorials-videoitem")
                        .addClass("hidden-item")
                        .data("tags", tags)
                        .attr("videoid", item.video.id)
                        .appendTo(".daviz-tutorials-playlist[playlistid='" + data.data.id + "'] .daviz-tutorials-videos")
                        .click(function(){
                            jQuery(iframe)
                                .attr("src", "http://www.youtube.com/embed/"+jQuery(this).attr("videoid")+"?autoplay=1");
                            jQuery(".nowplaying")
                                .removeClass("nowplaying");
                            jQuery(this)
                                .addClass("nowplaying");
                        })
                        .prepend(img);
                    jQuery("<div>")
                        .text(item.video.title)
                        .appendTo(item_obj);
                });
                self.updateTutorials();
                jQuery(window).trigger('hashchange');
            });
        });
    },

    updateTutorials: function(tag){
        self = this;
        self.context.find(".daviz-tutorials-main-playlist").scrollTop(0);
        if ((tag === "") || (tag === undefined)){
            tag = "All tutorials";
        }

        jQuery(".daviz-tutorials-main-playlist-title")
            .text(tag);
        jQuery(".daviz-tutorials-tagcloud a")
            .removeClass("selected");
        jQuery(".daviz-tutorials-tagcloud a[tag='" + tag + "']")
            .addClass("selected");
        jQuery(".daviz-tutorials-videoitem")
            .addClass("hidden-item")
            .removeClass("nowplaying");
        self.context.find("iframe")
            .attr("src", "");
        jQuery.each(jQuery(".daviz-tutorials-videoitem"), function(idx, item){
            item = jQuery(item);
            if (jQuery.inArray(tag, item.data("tags")) !== -1) {
                if (self.context.find("iframe").attr("src") === ""){
                    item.addClass("nowplaying");
                    self.context.find("iframe")
                        .attr("src", "http://www.youtube.com/embed/"+item.attr("videoid"));
                }
                item.removeClass("hidden-item");
            }
        });
    },

    updateTagCloud: function(tags){
        self = this;
        tag_data = jQuery(".daviz-tutorials-tagcloud").data("tags");
        for (i = 0; i < tags.length; i++) {
            var tag = tags[i].trim();
            if (tag !== "") {
                if (tag_data[tag] === undefined) {
                    tag_data[tag] = 0;
                }
                tag_data[tag] ++;
            }
        }
        jQuery(".daviz-tutorials-tagcloud").data("tags", tag_data);
        var sorted_tags = [];
        jQuery.each(tag_data, function(key, value){
            sorted_tags.push({tag:key, count:value});
        });
        sorted_tags.sort(function (a,b){
            if (a.tag === 'All tutorials') {
                return -1;
            }
            if ((a.tag === 'Basic tutorials') && (b.tag !== 'All tutorials')){
                return -1;
            }
            if ((a.tag === 'Advanced tutorials') && (b.tag !== 'All tutorials') && (b.tag !== 'Basic tutorials')) {
                return -1;
            }

            if (b.tag === 'All tutorials') {
                return 1;
            }
            if ((b.tag === 'Basic tutorials') && (a.tag !== 'All tutorials')){
                return 1;
            }
            if ((b.tag === 'Advanced tutorials') && (a.tag !== 'All tutorials') && (a.tag !== 'Basic tutorials')) {
                return 1;
            }

            if (a.tag === 'intro'){
                return -1;
            }
            if (b.tag === 'intro'){
                return 1;
            }

            if (a.count > b.count) {
                return -1;
            }
            else if (a.count < b.count) {
                return 1;
            }
            else {
                return 0;
            }
        });
        jQuery(".daviz-tutorials-tagcloud")
            .empty();
        jQuery("<div>")
            .addClass("by-difficulty")
            .appendTo(".daviz-tutorials-tagcloud");
        jQuery("<label>")
            .text("Filter by difficulty:")
            .appendTo(".by-difficulty");
        jQuery("<ul>")
            .appendTo(".by-difficulty");

        jQuery("<div>")
            .addClass("by-topic")
            .appendTo(".daviz-tutorials-tagcloud");
        jQuery("<label>")
            .text("Filter by topic:")
            .appendTo(".by-topic");
        jQuery("<ul>")
            .appendTo(".by-topic");
        for (i=0; i<sorted_tags.length; i++){
            var container = ".daviz-tutorials-tagcloud .by-difficulty ul";
            if (i > 2){
                container = ".daviz-tutorials-tagcloud .by-topic ul";
            }
            var li = jQuery("<li>").appendTo(container);
            jQuery("<a>")
                .css("text-decoration", "none")
                .attr("tag", sorted_tags[i].tag)
                .attr("href", "daviz-tutorials.html#" + sorted_tags[i].tag)
                .text(sorted_tags[i].tag + "(" + sorted_tags[i].count+ ") ")
                .appendTo(li);
        }
    }
};

jQuery.fn.DavizTutorials = function(options){
    return this.each(function(){
        var tutorials = new DavizEdit.DavizTutorials(jQuery(this), options);
    });
};

function updateTutorialLinks() {
    jQuery(".eea-tutorial").empty();
    jQuery.each(jQuery(".eea-tutorial"), function(idx, tutorial){
        jQuery("<div>")
            .addClass("message")
            .text(jQuery(tutorial).attr("message"))
            .appendTo(tutorial);
        jQuery("<a>")
            .attr("href", "daviz-tutorials.html#"+jQuery(tutorial).attr("tutorial"))
            .attr("target", "_blank")
            .attr("title", "see video help")
            .appendTo(tutorial);
        jQuery("<span>")
            .addClass("eea-icon eea-icon-youtube-play tutorial-icon")
            .appendTo(jQuery(tutorial).find("a"));
        jQuery("<span>")
            .addClass("tutorial-title")
            .text("see video help")
            .appendTo(jQuery(tutorial).find("a"));
    });
}
