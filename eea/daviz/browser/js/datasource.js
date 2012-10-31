jQuery(document).ready(function(){

  jQuery('#archetypes-fieldname-dataTitle').addClass('eea-daviz-source');
  jQuery('#archetypes-fieldname-dataLink').addClass('eea-daviz-source');
  jQuery('#archetypes-fieldname-dataOwner').addClass('eea-daviz-source');

  jQuery('.eea-daviz-source').wrapAll(
    '<div class="eea-daviz-source-group" />');
  var container = jQuery('.eea-daviz-source-group');

  var spreadsheet = jQuery('#archetypes-fieldname-spreadsheet');
  jQuery('#spreadsheet', spreadsheet).change(function(){
    spreadsheet.height('auto');
    if(!jQuery('.eea-daviz-source-group', spreadsheet).length){
      container.addClass('eea-daviz-source-group-highlight');
      spreadsheet.append(container);
    }
    container.show();
    jQuery(document).trigger('eea-wizard-changed');
  });

  var external = jQuery('#archetypes-fieldname-external');
  jQuery('#external', external).change(function(){
    external.height('auto');
    if(!jQuery('.eea-daviz-source-group', external).length){
      container.addClass('eea-daviz-source-group-highlight');
      external.append(container);
    }
    container.show();
    jQuery(document).trigger('eea-wizard-changed');
  });

  var quickUpload = jQuery('#archetypes-fieldname-quickUpload');
  jQuery(document).bind('qq-file-uploaded', function(evt, data){
    quickUpload.height('auto');
    if(!jQuery('.eea-daviz-source-group', quickUpload).length){
      container.addClass('eea-daviz-source-group-highlight');
      quickUpload.append(container);
    }
    container.show();
    jQuery(document).trigger('eea-wizard-changed');
  });

  function setNewTitle(newTitle){
    if (newTitle === ''){
      newTitle = 'Data Visualization';
    }
    var titleInput = jQuery('#archetypes-fieldname-title').find("input");
    if (titleInput.attr("originalvalue") === 'Data Visualization'){
      titleInput.attr("value", newTitle);
    }
  }
  jQuery('#archetypes-fieldname-dataTitle').find("input").change(function(){
    setNewTitle(jQuery(this).val());
  });

  jQuery(document).bind('EEA-REFERENCEBROWSER-FINISHEDUPDATE', function(evt, data){
    var newTitle = jQuery(jQuery(data).find(".tileHeadline")[0]).find("a").html();
    setNewTitle(newTitle);
  });

});
