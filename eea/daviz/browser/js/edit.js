jQuery(document).ready(function(){
  var editor = jQuery('.daviz-views-edit');
  jQuery('ul', editor).show();
  jQuery('fieldset', editor).addClass('daviz-edit-fieldset');
  jQuery('form h1', editor).hide();
  editor.tabs();
});
