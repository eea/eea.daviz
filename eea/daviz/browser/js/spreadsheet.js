if(window.DavizPresentationEdit === undefined){
  var DavizPresentationEdit = {'version': '1.0'};
}

DavizPresentationEdit.SpreadSheet = function(context, options){
  var self = this;
  self.context = context;
  self.settings = {
    group: [],
    label: '',
    help: ''
  };

  if(options){
    jQuery.extend(self.settings, options);
  }

  self.initialize();
};

DavizPresentationEdit.SpreadSheet.prototype = {
  initialize: function(){
    var self = this;
    self.groupFields();
  },

  groupFields: function(){
    var self = this;
    jQuery.each(self.settings.group, function(index, field){
      field.addClass('daviz-presentation-spreadsheet');
      var label = jQuery('label.formQuestion', field);
      var title = label.text();
      label.remove();
      field.before(
        jQuery('<h3>').addClass('daviz-presentation-spreadsheet').append(
          jQuery('<a>').addClass('daviz-ajax')
            .attr('href', '#' + field.attr('id')).html(title)
        )
      );
    });

    var parent = self.context.parent();
    jQuery('.daviz-presentation-spreadsheet', parent).wrapAll(
      '<div class="daviz-spreadsheet-accordion" />');
    var container = jQuery('.daviz-spreadsheet-accordion', parent);
    container.before(jQuery('<label>').text(self.settings.label));
    container.before(jQuery('<div>').addClass('formHelp').text(self.settings.help));
    container.accordion();
  }
};

jQuery.fn.EEADavizPresentationSpreadSheet = function(options){
  return this.each(function(){
    var context = jQuery(this).addClass('ajax');
    var spreadsheet = new DavizPresentationEdit.SpreadSheet(context, options);
  });
};

jQuery(document).ready(function(){
  var context = jQuery('#archetypes-fieldname-spreadsheet');
  if(!context.length){
    return;
  }

  var fields = [
    '#archetypes-fieldname-spreadsheet',
    '#archetypes-fieldname-quickUpload',
    '#archetypes-fieldname-relatedItems'
  ];

  var options = {
    group: [],
    label: 'Data sources',
    help: 'TAB separated files, SPARQL methods, etc'
  };

  jQuery.each(fields, function(index, name){
    var field = jQuery(name, context.parent());
    if(field.length){
      options.group.push(field);
    }
  });

  jQuery(context).EEADavizPresentationSpreadSheet(options);

});
