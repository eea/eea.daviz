var DavizEdit = {'version': '1.0.0'};

DavizEdit.Status = {
  initialize: function(){
    this.status = jQuery('<dl>').addClass('portalMessage');
    this.type = jQuery('<dt>').text('Info');
    this.message = jQuery('<dd>');
    this.status.append(this.type).append(this.message);
    this.status.hide();
    jQuery('#daviz-page-title').after(this.status);
  },

  update: function(msg, type){
    this.status.hide();
    this.message.text(msg);
    this.status.show();
  }
};

DavizEdit.Facets = {
  initialize: function(){
    this.form = jQuery('.daviz-facets-settings form');
    this.action = this.form.attr('action');
    this.button = jQuery('input[type=submit]', this.form);

    var context = this;
    this.form.submit(function(){
      context.submit();
      context.button.removeClass('submitting');
      return false;
    });
  },

  submit: function(){
    var query = 'daviz.facets.save=ajax&';
    query += this.form.serialize();

    var context = this;
    this.button.addClass('daviz-ajax-loader');
    DavizEdit.Status.update('Saving ...');
    jQuery.post(this.action, query, function(data){
      DavizEdit.Status.update(data);
      context.button.removeClass('daviz-ajax-loader');
    });
  }
};

DavizEdit.Views = {
  initialize: function(){
    this.form = jQuery('.daviz-views-settings form');
    this.action = this.form.attr('action');
    this.button = jQuery('input[type=submit]', this.form);
    this.area = jQuery('#daviz-views-edit');
    this.update_tabs();

    var context = this;
    this.form.submit(function(){
      context.submit();
      context.button.removeClass('submitting');
      return false;
    });
  },

  submit: function(){
    var query = 'daviz.views.save=ajax&';
    query += this.form.serialize();

    var context = this;
    this.button.addClass('daviz-ajax-loader');
    DavizEdit.Status.update('Saving ...');
    jQuery.post(this.action, query, function(data){
      DavizEdit.Status.update(data);
      context.update();
      context.button.removeClass('daviz-ajax-loader');
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
      context.submit(this);
      return false;
    });
  },

  submit: function(form){
    form = jQuery(form);
    var action = form.attr('action');
    var button = jQuery('input[type=submit]', form);
    var query = button.attr('name') + '=' + 'ajax' + '&';
    query += form.serialize();

    button.addClass('daviz-ajax-loader');
    DavizEdit.Status.update('Saving ...');
    jQuery.post(action, query, function(data){
      DavizEdit.Status.update(data);
      button.removeClass('daviz-ajax-loader');
    });
  }
};

jQuery(document).ready(function(){
  DavizEdit.Status.initialize();
  DavizEdit.Facets.initialize();
  DavizEdit.Views.initialize();
});
