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
  warning.attr('title', label.text());
  warning.dialog({
      bgiframe: true,
      autoOpen: false,
      modal: true,
      width: 600,
      dialogClass: 'daviz-confirm-overlay',
      buttons: {
        Continue: function(){
          currentForm.submit();
          jQuery(this).dialog('close');
        },
        Cancel: function(){
          jQuery('input[type=submit]', form).removeClass('submitting');
          jQuery(this).dialog('close');
        }
      }
  });

  jQuery('#spreadsheet', form).change(function(){
    changed = true;
  });

  jQuery('#external', form).change(function(){
    changed = true;
  });

  jQuery(document).bind('qq-file-uploaded', function(evt, data){
    changed = true;
  });

  // If there is no data previously set, we're in the add form, so exit
  if(relatedItems === 0){
    if(!spreadsheet.length || (spreadsheet.val().trim() === "")){
      if(!external.length || (external.val().trim() === "")){
        return;
      }
    }
  }

  // Add confirmation dialog on form submit
  form.submit(function(evt){
    if(jQuery(relatedSelector, form).length !== relatedItems){
      changed = true;
    }

    if(changed){
      currentForm = this;
      warning.dialog('open');
      return false;
    }else{
      return true;
    }
  });

  jQuery("[name='form.button.cancel']", form).click(function(){
    changed = false;
    relatedItems = jQuery(relatedSelector, form).length;
  });
});
