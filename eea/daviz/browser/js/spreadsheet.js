if(window.EEA === undefined){
  var EEA = {'version': 'eea.daviz'};
}

if(EEA.Daviz === undefined){
  EEA.Daviz = {'version': 'eea.daviz'};
}

EEA.Daviz.Spreadsheet = function(context, options){
 var self = this;
  self.context = context;

  self.settings = {
  };

  if(options){
    jQuery.extend(self.settings, options);
  }

  self.initialized = false;
  self.initialize();
};

EEA.Daviz.Spreadsheet.prototype = {
  initialize: function(){
    var self = this;
    if(self.initialized){
      return;
    }

    self.grid = null;
    self.textarea = jQuery('#spreadsheet', self.context);
    if(self.textarea.val().trim() !== ""){
      self.initialized = true;
      self.reload();
    }

    jQuery('#spreadsheet', self.context).change(function(){
      self.initialized = true;
      self.reload();
    });
  },

  reload: function(){
    var self = this;

    var table = self.textarea.val();
    EEA.Daviz.Status.start('Loading table ...');
    jQuery.ajax({
      type: 'POST',
      url: '@@daviz-table2json.json',
      dataType: 'json',
      data: {'table': table},
      success: function(data){
        self.reloadTable(data);
      },
      error: function(jqXHR, textStatus, errorThrown){
        // XXX Do something;
      },
      complete: function(jqXHR, textStatus){
        EEA.Daviz.Status.stop(textStatus);
      }
    });
  },

  reloadTable: function(data){
    var self = this;

    if(self.grid){
      self.grid.destroy();
      jQuery(".daviz-data-table", self.context).remove();
    }

    if(!data.items.length){
      self.textarea.show();
      return;
    }else{
      self.textarea.hide();
    }

    self.gridview = jQuery('<div>')
      .addClass('daviz-data-table')
      .addClass('daviz-jsongrid')
      .appendTo(self.context)
      .width(self.context.parent().width())
      .height(400);

    var colNames = Object.keys(data.properties || {});
    var columns = [
      {
        id: "selector",
        name: "",
        field: "num",
        cssClass: "slickgrid-index-column",
        width: 30,
        resizable: false,
        header: {
          buttons: [
            {
              image: "++resource++slickgrid-images/pencil.png",
              command: "edit",
              tooltip: "Edit raw table"
            }
          ]
        }
      }
    ];

    jQuery.each(colNames, function(index, key){
      var colType = data.properties[key].columnType || data.properties[key].valueType;
      var label = key;

      var column = {
        id: key,
        name: label,
        field: key,
        toolTip: colType,
        sortable: false,
        selectable: true,
        resizable: true,
        focusable: true,
        editor: Slick.Editors.Text,
        header: {
          menu: EEA.Daviz.ColumnMenu({columnType: colType})
        }
      };

      columns.push(column);
    });

    var options = {
      enableColumnReorder: false,
      enableCellNavigation: true,
      forceFitColumns: true,
      enableAddRow: true,
      editable: true,
      autoEdit: true
    };

    self.items = jQuery.map(data.items, function(item, index){
      item.num = index + 1;
      return item;
    });

    self.grid = new Slick.Grid('.daviz-data-table', self.items, columns, options);

    // Plugins

    // Menu
    var headerMenuPlugin = new Slick.Plugins.HeaderMenu({
      buttonImage: "++resource++slickgrid-images/down.gif"
    });

    headerMenuPlugin.onCommand.subscribe(function(e, args) {
      self.handle_menu_action(args);
    });

    // Buttons
    var headerButtonsPlugin = new Slick.Plugins.HeaderButtons();
    headerButtonsPlugin.onCommand.subscribe(function(e, args) {
      self.handle_menu_action(args);
    });

    self.grid.registerPlugin(headerMenuPlugin);
    self.grid.registerPlugin(headerButtonsPlugin);

    self.grid.onAddNewRow.subscribe(function (e, args) {
      var item = args.item;
      item.num = self.items.length + 1;
      self.grid.invalidateRow(self.items.length);
      self.items.push(item);
      self.grid.updateRowCount();
      self.grid.render();
    });
  },

  handle_menu_action: function(args){
    var self = this;
    var command = args.command;

    // Edit
    if(command === 'edit'){
      return self.edit_body(args);
    }

    // Rename
    if(command === "rename"){
      return self.edit_header(args.column);
    }

    // Change column type
    return self.convert_column(command, args.column);
  },

  edit_body: function(args){
    var self = this;
    console.log('Edit body');
    console.log(args);
  },

  edit_header: function(column){
    var self = this;
    var text = 'NOT-SET-YET';
    var popup = jQuery("<div title='Rename column: " + column.field + "' />")
      .append(
        jQuery('<input>').attr('type', 'text').val(text).width('80%')
      ).dialog({
        bgiframe: true,
        modal: true,
        dialogClass: 'daviz-confirm-overlay',
        width: 400,
        buttons: {
          Cancel: function(){
            jQuery(this).dialog('close');
          },
          Rename: function(){
            //facet.val(jQuery('input', this).val()).change();
            alert('Not implemented yet');
            jQuery(this).dialog('close');
          }
        }
    });
  },

  convert_column: function(to, column){
    var self = this;
    console.log(to);
    console.log(column);
  },
};

jQuery.fn.EEADavizSpreadsheet = function(options){
  return this.each(function(){
    var context = jQuery(this);
    var data = new EEA.Daviz.Spreadsheet(context, options);
    context.data('EEADavizSpreadsheet', data);
  });
};

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
    '#archetypes-fieldname-external',
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

  // Group fields
  context.EEAFormsGroup(options);

  // Spreadsheet
  context.EEADavizSpreadsheet();

  // Make formTabs a wizard
  jQuery("form[name='edit_form'] .formTabs").EEAFormsWizard();
  jQuery('#archetypes-fieldname-external').height('auto');

});
