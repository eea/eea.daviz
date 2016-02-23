jQuery(document).ready(function(){
  jQuery('#archetypes-fieldname-provenances').addClass('eea-daviz-source');


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
    jQuery("#fieldsetlegend-data-provenance").parent().remove();
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
    jQuery("#fieldsetlegend-data-provenance").parent().remove();
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
    jQuery("#fieldsetlegend-data-provenance").parent().remove();
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

  function EditInheritedProvenances(){
    jQuery('.eea-daviz-readonly').removeClass('eea-daviz-readonly');
    jQuery('#archetypes-fieldname-provenances').find('input').removeClass('eea-daviz-readonly').removeAttr('readonly');
    jQuery('#archetypes-fieldname-provenances').find('select').removeClass('eea-daviz-readonly').removeAttr('disabled');
    jQuery('.datagridwidget-manipulator').find('img').show();
    jQuery('#datagridwidget-add-button').show();
    jQuery('.edit-provenances').hide();
    jQuery(document).trigger('eea-wizard-changed');
  }

  function MakeAllSelectAutocompletWidget(){
    jQuery.each(jQuery('select[name="provenances.owner:records"]'), function(idx, col){
      if (!jQuery(col).data("SelectAutocompleteWidget")){
        jQuery(col).parent().find(".selectautocomplete_widget").remove();
        jQuery(col).SelectAutocompleteWidget();
      }
    });
  }

  function setDataGridWidgetTRLabels(){
    jQuery('#datagridwidget-tbody-provenances').find(".eea-datagridwidget-tr-label").remove();
    jQuery.each(jQuery('#datagridwidget-tbody-provenances').find("tr"), function(idx, tr){
        var tr_label = jQuery("<td>").addClass("eea-datagridwidget-tr-label").text("Data Provenance #"+(idx+1).toString());
        jQuery(tr).prepend(tr_label);
    });
    if (jQuery().SelectAutocompleteWidget){
        MakeAllSelectAutocompletWidget();
    }
  }

  function setColumnClasses(){
    jQuery('[name="provenances.title:records"]').closest("td").addClass("datagridwidget-column-1");
    jQuery('[name="provenances.link:records"]').closest("td").addClass("datagridwidget-column-2");
    jQuery('[name="provenances.owner:records"]').closest("td").addClass("datagridwidget-column-3");
    setDataGridWidgetTRLabels();
    jQuery(document).trigger('eea-wizard-changed');
  }

  jQuery(".datagridwidget-add-button").text("Add new provenance info");
  jQuery("#fieldset-data-provenance").delegate(".datagridwidget-manipulator img", "click", setColumnClasses);
  jQuery("#fieldset-data-provenance").delegate(".datagridwidget-add-button", "click", setColumnClasses);
  setDataGridWidgetTRLabels();
  if (jQuery('#inheritedprovenance').attr('checked')){
    jQuery('#archetypes-fieldname-provenances').addClass('eea-daviz-readonly');
    jQuery('.datagridwidget-manipulator').find('img').hide();
    jQuery('#datagridwidget-add-button').hide();
    jQuery('#archetypes-fieldname-provenances').find('input').addClass('eea-daviz-readonly').attr('readonly', 'readonly');
    jQuery('#archetypes-fieldname-provenances').find('select').addClass('eea-daviz-readonly').attr('disabled', 'disabled');
    jQuery('#archetypes-fieldname-provenances').append('<span class="edit-provenances">The provenance info is inherited from the related datasources. You can edit them by clicking on the <b>Edit provenance info</b> button</span> <br/>');
    jQuery('#archetypes-fieldname-provenances').append('<input type="button" class="edit-provenances" value="Edit procenance info"/>');
    jQuery('input.edit-provenances').bind('click', EditInheritedProvenances);
  }

});

if (window.Browser) {
  window.Browser.onUploadComplete = function(){
    // don't reload the page after uploading file
  };
}
