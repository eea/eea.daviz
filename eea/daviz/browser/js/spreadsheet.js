jQuery(document).ready(function(){
  var context = jQuery('#archetypes-fieldname-spreadsheet');
  if(!context.length){
    return;
  }

  // EEAFormsGroup not initialized, see eea.forms
  if(context.EEAFormsGroup === undefined){
    return;
  }

  var fields = [
    '#archetypes-fieldname-spreadsheet',
    '#archetypes-fieldname-quickUpload',
    '#archetypes-fieldname-relatedItems'
  ];

  var options = {
    group: []
  };

  jQuery.each(fields, function(index, name){
    var field = jQuery(name, context.parent());
    if(field.length){
      var error = jQuery('.fieldErrorBox', field);
      if(error.length && error.text()){
        jQuery.data(field[0], 'errors', error.text());
      }
      options.group.push(field);
    }
  });

  context.EEAFormsGroup(options);
});
