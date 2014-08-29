jQuery(document).ready(function(){
  var warning = jQuery('#archetypes-fieldname-dataWarning');
  if(!warning.length){
    return;
  }

  var currentForm;
  var relatedSelector;
  var changed = false;

  var form = warning.parents('form');
  var relatedItems = jQuery("select[name='relatedItems:list']", form);
  if(relatedItems.length){
    relatedSelector = "select[name='relatedItems:list'] option";
  }else{
    relatedSelector = "input[name='relatedItems:list']:checked";
  }

  relatedItems = jQuery(relatedSelector, form).length;
  var spreadsheet = jQuery('#spreadsheet', form);
  var external = jQuery('#external', form);

  var label = jQuery('div.label', warning).hide();

  // If there is no data previously set, we're in the add form, so exit
  if(relatedItems === 0){
    if(!spreadsheet.length || (spreadsheet.val().trim() === "")){
      if(!external.length || (external.val().trim() === "")){
        return;
      }
    }
  }
  jQuery("#fieldset-data-input")
    .css("position", "relative");
  jQuery("<div>")
    .addClass("eea-daviz-datasource-readonly")
    .css("background-color", "rgba(1,1,1,0.5)")
    .css("position", "absolute")
    .css("height", "100%")
    .css("width", "100%")
    .css("top", "0")
    .css("z-index", "1")
    .appendTo("#fieldset-data-input");
  jQuery("<div>")
    .addClass("portalMessage warningMessage")
    .html(label.find("span").html())
    .appendTo(".eea-daviz-datasource-readonly");
  jQuery("<br/>")
    .appendTo(".eea-daviz-datasource-readonly .portalMessage");
  jQuery("<input type='button'/>")
    .attr("value", "Unlock datasources")
    .appendTo(".eea-daviz-datasource-readonly .portalMessage")
    .click(function(){
        jQuery(".eea-daviz-datasource-readonly").remove();
    });
});
