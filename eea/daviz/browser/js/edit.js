var DavizEdit = {'version': '1.0.0'};

/** Status
*/
DavizEdit.Status = {
  initialize: function(){
    this.area = jQuery('.daviz-settings');
    this.area.append(jQuery('<div>').addClass('daviz-cleanup'));
    this.lock = jQuery('<div>').addClass('daviz-status-lock');
    this.message = jQuery('<div>').addClass('daviz-ajax-loader');
    this.lock.prepend(this.message);
    this.area.prepend(this.lock);

    this.lock.dialog({
      show: 'slow',
      hide: 'slow',
      modal: true,
      closeOnEscape: false,
      autoOpen: false,
      draggable: false,
      resize: false,
      dialogClass: 'daviz-loading-overlay'
    });
  },

  start: function(msg){
    this.message.html(msg);
    this.lock.dialog('open');
  },

  stop: function(msg){
    this.message.html(msg);
    this.lock.dialog('close');
  }
};

/** Facets
*/
DavizEdit.Facets = {
  initialize: function(){
    var self = this;
    self.area = jQuery('.daviz-facets-edit').addClass('daviz-facets-edit-ajax');
    jQuery('.daviz-facet-edit', self.area).each(function(){
      var facet = new DavizEdit.Facet(jQuery(this));
    });

    // Sortable
    jQuery('.daviz-facets-edit-ajax').sortable({
      items: '.daviz-facet-edit',
      placeholder: 'ui-state-highlight',
      forcePlaceholderSize: true,
      opacity: 0.7,
      delay: 300,
      cursor: 'crosshair',
      tolerance: 'pointer',
      update: function(event, ui){
        self.sort(ui.item.parent());
      }
    });
  },

  sort: function(context){
    facets = jQuery('.facet-title', context);
    var order = jQuery.map(facets, function(value){
      return jQuery(value).text();
    });

    var action = jQuery('form', context).attr('action');
    var index = action.indexOf('@@');
    action = action.slice(0, index) + '@@daviz-edit.save';

    query = {'daviz.facets.save': 'ajax', order: order};
    DavizEdit.Status.start('Saving ...');
    jQuery.post(action, query, function(data){
      DavizEdit.Status.stop(data);
    });
  }
};

/** Facet
*/
DavizEdit.Facet = function(facet){
  this.initialize(facet);
};

DavizEdit.Facet.prototype = {
  initialize: function(facet){
    this.facet = facet;
    this.form = jQuery('form', facet);
    this.action = this.form.attr('action');
    this.button = jQuery('input[type=submit]', this.form);
    this.button.hide();

    var show = jQuery("div.field:has([id$=.show])", this.form).hide();
    this.show = jQuery("[id$=.show]", show);
    this.visible = this.show.attr('checked');
    this.addicon();

    var context = this;
    this.form.submit(function(){
      return false;
    });

    jQuery(':input', this.form).change(function(){
      context.submit();
      return false;
    });
  },

  addicon: function(){
    var self = this;
    var title = jQuery('h1', self.form);
    title.attr('title', 'Click and drag to change widget position');

    var html = title.html();
    var newhtml = jQuery('<div>').addClass('facet-title').html(html);
    title.html(newhtml);

    var msg = 'Hide facet';
    var css = 'ui-icon-hide';
    if(!self.visible){
      msg = 'Show facet';
      css = 'ui-icon-show';
      title.addClass('hidden');
    }
    var icon = jQuery('<div>')
      .html('h')
      .attr('title', msg)
      .addClass('ui-icon')
      .addClass(css);

    icon.click(function(){
      if(self.visible){
        self.visible = false;
        icon.removeClass('ui-icon-hide')
          .addClass('ui-icon-show')
          .attr('title', 'Show facet');
          title.addClass('hidden');
      }else{
        self.visible = true;
        icon.removeClass('ui-icon-show')
          .addClass('ui-icon-hide')
          .attr('title', 'Hide facet');
          title.removeClass('hidden');
      }
      self.show.click();
      self.submit();
    });
    title.prepend(icon);
  },

  submit: function(){
    var name = this.button.attr('name');
    var query = name + '=ajax&';
    query += this.form.serialize();

    DavizEdit.Status.start('Saving ...');
    jQuery.post(this.action, query, function(data){
      DavizEdit.Status.stop(data);
    });
  }
};

/** Views
*/
DavizEdit.Views = {
  initialize: function(){
    var self = this;
    jQuery(document).bind('daviz-views-refreshed', function(evt, data){
      self.update_views(data);
    });
    jQuery(document).trigger('daviz-views-refreshed', {init: true});
  },

  update_views: function(form){
    var self = this;
    self.area = jQuery('.daviz-views-edit').addClass('daviz-views-edit-ajax');

    if(!form.init){
      var action = form.action;
      var i = action.indexOf('@@');
      action = action.slice(0, i) + '@@daviz-edit.views.html';
      DavizEdit.Status.start('Refreshing ...');
      jQuery.get(action, {}, function(data){
        self.area.html(data);
        self.update_tabs();
        DavizEdit.Status.stop("Done");
      });
    }else{
      self.update_tabs();
    }
  },

  update_tabs: function(){
    jQuery('.daviz-view-edit', this.area).each(function(){
      var view = new DavizEdit.View(jQuery(this));
    });
    this.area.tabs('destroy');
    var ul = jQuery('ul', this.area).show();
    jQuery('fieldset', this.area).addClass('daviz-edit-fieldset');
    jQuery('form h1', this.area).hide();
    this.area.tabs();
  }
};

/** View settings
*/
DavizEdit.View = function(view){
  this.initialize(view);
};

DavizEdit.View.prototype = {
  initialize: function(view){
    var self = this;
    self.view = view;
    self.form = jQuery('form', self.view);
    self.table = jQuery('div.field:has(label[for=daviz.properties.sources]) table', self.form);
    if(self.table.length){
      self.table.addClass('daviz-sources-table');
      var table = new DavizEdit.SourceTable(self.table);
    }

    self.form.submit(function(){
      self.submit();
      return false;
    });

    self.style();
  },

  style: function(){
    // Add links to URLs
    var self = this;
    var help = jQuery('.formHelp', this.view);
    help.each(function(){
      var here = jQuery(this);
      var text = self.replaceURL(here.text());
      here.html(text);
    });
  },

  replaceURL: function(inputText) {
    var replacePattern = /(\b(https?|ftp):\/\/[\-A-Z0-9+&@#\/%?=~_|!:,.;]*[\-A-Z0-9+&@#\/%=~_|])/gim;
    return inputText.replace(replacePattern, '<a href="$1" target="_blank">here</a>');
  },

  submit: function(){
    var self = this;
    var action = self.form.attr('action');
    var query = {};
    var array = self.form.serializeArray();

    jQuery.each(array, function(){
      if(query[this.name]){
        query[this.name].push(this.value);
      }else{
        query[this.name] = [this.value];
      }
    });

    var button = jQuery('.actionButtons input[type=submit]', self.form);
    var name = button.attr('name');
    query[name] = 'ajax';

    DavizEdit.Status.start('Saving ...');
    jQuery.post(action, query, function(data){
      button.removeClass('submitting');
      DavizEdit.Status.stop(data);
      if(name === 'daviz.properties.actions.save'){
        jQuery(document).trigger('daviz-views-refreshed', {
          init: false,
          action: action
        });
      }
    });
  }
};

DavizEdit.SourceTable = function(table){
  this.initialize(table);
};

DavizEdit.SourceTable.prototype = {
  initialize: function(table){
    var self = this;
    self.table = table;
    self.count = jQuery('input[name=daviz.properties.sources.count]', table.parent());

    self.button_add = jQuery('input[name=daviz.properties.sources.add]', table);
    self.button_add.click(function(){
      self.add(jQuery(this));
      return false;
    });

    self.button_remove = jQuery('input[name=daviz.properties.sources.remove]', table);
    if (!self.button_remove.length){
      self.button_remove = jQuery('<input>').attr('type', 'submit')
        .attr('name', 'daviz.properties.sources.remove')
        .val("Remove selected items");
      self.button_add.parent('td').prepend(self.button_remove);
    }

    self.button_remove.click(function(){
      self.remove(jQuery(this));
      return false;
    });

  },

  add: function(button){
    var self = this;
    button.removeClass('submitting');
    var count = parseInt(self.count.val(), 10);

    var check = jQuery('<input />').attr('type', 'checkbox')
      .addClass('editcheck')
      .attr('name', 'daviz.properties.sources.remove_' + count);
    var text = jQuery('<input />').attr('type', 'text').attr("value", "")
      .addClass('textType')
      .attr('name', 'daviz.properties.sources.' + count + '.');

    var td = jQuery('<td>').append(check).append(text);
    var row = jQuery('<tr>').append(td);

    self.table.prepend(row);

    count += 1;
    self.count.val(count);
  },

  remove: function(button){
    var self = this;
    button.removeClass('submitting');

    var checked = jQuery('input[type=checkbox]:checked', self.table);
    checked.each(function(){
      jQuery(this).parent().parent('tr').remove();
    });

    var count = parseInt(self.count.val(), 10);
    count -= checked.length;
    self.count.val(count);
  }
};


jQuery(document).ready(function(){
  DavizEdit.Status.initialize();
  DavizEdit.Facets.initialize();
  DavizEdit.Views.initialize();
});
