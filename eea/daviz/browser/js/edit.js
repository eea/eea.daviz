var DavizEdit = {'version': '1.0.0'};

DavizEdit.Status = {
  initialize: function(){
    this.area = jQuery('.daviz-settings');
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

DavizEdit.Facets = {
  initialize: function(){
    this.form = jQuery('.daviz-facets-settings form');
    this.action = this.form.attr('action');
    this.button = jQuery('input[type=submit]', this.form);
    this.button.hide();

    var context = this;
    this.form.submit(function(){
      return false;
    });

    jQuery(':input', this.form).change(function(){
      context.submit();
      return false;
    });
  },

  submit: function(){
    var query = 'daviz.facets.save=ajax&';
    query += this.form.serialize();

    DavizEdit.Status.start('Saving ...');
    jQuery.post(this.action, query, function(data){
      DavizEdit.Status.stop(data);
    });
  }
};

DavizEdit.Views = {
  initialize: function(){
    this.form = jQuery('.daviz-views-settings form');
    this.action = this.form.attr('action');
    this.button = jQuery('input[type=submit]', this.form);
    this.button.hide();
    this.area = jQuery('#daviz-views-edit');
    this.update_tabs();

    var context = this;
    this.form.submit(function(){
      return false;
    });

    jQuery(':input', this.form).change(function(){
      context.submit();
      return false;
    });
  },

  submit: function(){
    var query = 'daviz.views.save=ajax&';
    query += this.form.serialize();

    var context = this;
    DavizEdit.Status.start('Saving ...');
    jQuery.post(this.action, query, function(data){
      context.update();
      DavizEdit.Status.stop(data);
    });
  },

  update: function(){
    var context = this;
    var i = this.action.indexOf('@@');
    var action = this.action.slice(0, i) + '@@daviz-edit.views.html';
    jQuery.get(action, {}, function(data){
      context.area.html(data);
      context.update_tabs();
    });
  },

  update_tabs: function(){
    this.area.tabs('destroy');
    jQuery('ul', this.area).show();
    jQuery('fieldset', this.area).addClass('daviz-edit-fieldset');
    jQuery('form h1', this.area).hide();
    this.area.tabs();
    DavizEdit.ViewSettings.initialize();
  }
};

DavizEdit.ViewSettings = {
  initialize: function(){
    this.forms = jQuery('#daviz-views-edit form');
    var context = this;
    this.forms.submit(function(){
      return false;
    });

    this.forms.submit(function(){
      var form = jQuery(this);
      context.submit(form);
      return false;
    });
  },

  submit: function(form){
    var action = form.attr('action');
    var button = jQuery('input[type=submit]', form);
    var query = button.attr('name') + '=' + 'ajax' + '&';
    query += form.serialize();

    DavizEdit.Status.start('Saving ...');
    jQuery.post(action, query, function(data){
      DavizEdit.Status.stop(data);
      button.removeClass('submitting');
    });
  }
};

jQuery(document).ready(function(){
  DavizEdit.Status.initialize();
  DavizEdit.Facets.initialize();
  DavizEdit.Views.initialize();
});
