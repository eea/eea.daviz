var DavizTableStyler = function(table, database){
  jQuery(table).addClass('listing');
};

var DavizTableRowStyler = function(item, database, tr) {
  if (tr.rowIndex % 2) {
    jQuery(tr).addClass('odd');
  } else {
    jQuery(tr).addClass('even');
  }
};

jQuery(document).ready(function(){
  var sections = jQuery("ul.chart-tabs");
  if(sections.length){
    sections.tabs("div.chart-panes > div");
  }
});
