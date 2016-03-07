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
    self.textarea = jQuery('#spreadsheet', self.context).addClass('spreadsheet-textarea');
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
    self.table = data;

    if(self.grid){
      self.grid.destroy();
      jQuery(".daviz-data-table", self.context).remove();
    }

    if(!self.table.items.length){
      self.textarea.slideDown();
      return;
    }else{
      self.textarea.slideUp();
    }

    self.gridview = jQuery('<div>')
      .addClass('daviz-slick-table')
      .addClass('daviz-data-table')
      .addClass('daviz-jsongrid')
      .width(self.context.parent().width())
      .height(400);
    self.textarea.after(self.gridview);

    var colNames = Object.keys(self.table.properties || {});
    var cols = [];
    var i;
    for (i = 0; i < colNames.length; i++){
        var newCol = {
            name: colNames[i],
            order: self.table.properties[colNames[i]].order
        };
        cols.push(newCol);
    }
    cols = cols.sort(function(a,b){return a.order-b.order;});

    colNames = [];
    for (i = 0; i < cols.length; i++){
        colNames.push(cols[i].name);
    }

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

    var href_parts = window.location.href.split("/");
    var rename = false;
    href_parts[href_parts.length -1] = "daviz.json";
    jQuery.ajax({
        url: href_parts.join("/"),
        async: false,
        success: function(data){
            try{
                data = JSON.parse(data);
                if (jQuery.isEmptyObject(data.properties)){
                    rename = true;
                }
            }
            catch(err){
                rename = true;
            }
        }
    });

    jQuery.each(colNames, function(index, key){
      var colType = self.table.properties[key].columnType || self.table.properties[key].valueType;
      var label = self.table.properties[key].label || key;

      var editor = Slick.Editors.Text;
      var formatter;
      if(colType === 'date'){
        editor = Slick.Editors.Date;
      }
      if(colType === 'boolean'){
        editor = self.YesNoSelectEditor;
        formatter = self.boolean_formatter;
      }

      var column = {
        id: key,
        name: label,
        field: key,
        toolTip: colType,
        sortable: false,
        selectable: true,
        resizable: true,
        focusable: true,
        editor: editor,
        header: {
          menu: EEA.Daviz.ColumnMenu({columnType: colType, rename:rename})
        }
      };

      if(formatter){
        column.formatter = formatter;
      }

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

    self.table.items = jQuery.map(self.table.items, function(item, index){
      item.num = index + 1;
      return item;
    });

    self.grid = new Slick.Grid('.daviz-data-table', self.table.items, columns, options);

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
      item.num = self.table.items.length + 1;
      self.grid.invalidateRow(self.table.items.length);
      self.table.items.push(item);
      self.grid.updateRowCount();
      self.grid.render();
    });

    // Header right-click
    self.grid.onHeaderContextMenu.subscribe(function(e, args){
      e.preventDefault();
      jQuery('.slick-header-menubutton', e.srcElement).click();
    });

    self.grid.onCellChange.subscribe(function(e, args){
      self.save(false);
    });
  },

  boolean_formatter: function(row, cell, value, columnDef, dataContext) {
    if (value === undefined || value === 'null') {
      return '';
    }
    return value ? "Yes" : "No";
  },

  YesNoSelectEditor: function(args) {
    var $select;
    var defaultValue;
    var scope = this;

    this.init = function () {
      $select = $("<SELECT tabIndex='0' class='editor-yesno'><OPTION value='yes'>Yes</OPTION><OPTION value='no'>No</OPTION><OPTION value='null'>Null</OPTION></SELECT>");
      $select.appendTo(args.container);
      $select.focus();
    };

    this.destroy = function () {
      $select.remove();
    };

    this.focus = function () {
      $select.focus();
    };

    this.loadValue = function (item) {
      if (item[args.column.field] === undefined || item[args.column.field] === 'null') {
        $select.val(defaultValue = '');
      } else {
        $select.val((defaultValue = item[args.column.field]) ? "yes" : "no");
      }
      $select.select();
    };

    this.serializeValue = function () {
      if ($select.val() === "null") {
        return "null";
      } else {
        return ($select.val() == "yes");
      }
    };

    this.applyValue = function (item, state) {
      item[args.column.field] = state;
    };

    this.isValueChanged = function () {
      return ($select.val() != defaultValue);
    };

    this.validate = function () {
      return {
        valid: true,
        msg: null
      };
    };

    this.init();
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
    if(self.textarea.is(':visible')){
      self.textarea.slideUp();
    }else{
      self.textarea.slideDown();
    }
  },

  edit_header: function(column){
    var self = this;
    var text = column.name;
    var popup = jQuery("<div title='Rename column: " + column.name + "' />")
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
            var value = jQuery('input', popup).val();
            self.table.properties[column.id].label = value;
            self.grid.updateColumnHeader(column.id, value);
            self.save(false);
            jQuery(this).dialog('close');
          }
        }
    });
  },

  convert_column: function(to, column){
    var self = this;
    self.table.properties[column.id].columnType = to;
    self.save(true);
  },

  save: function(reload){
    var self = this;
    self.loading();
    jQuery.ajax({
      type: 'POST',
      url: '@@daviz-json2table.tsv',
      dataType: 'text',
      data: {'json': JSON.stringify(self.table)},
      success: function(data){
        self.textarea.val(data);
        if(reload){
          self.textarea.change();
        }
      },
      error: function(jqXHR, textStatus, errorThrown){
        // XXX Do something;
      },
      complete: function(jqXHR, textStatus){
        self.loading();
      }
    });
  },

  loading: function(){
    var self = this;
    var style, img;

    img = jQuery('div[style*="pencil.png"]', self.context);
    if(img.length){
      style = img.attr('style');
      style = style.replace('pencil.png', 'ajax-loader-small.gif');
      img.attr('style', style);
      return;
    }

    img = jQuery('div[style*="ajax-loader-small.gif"]', self.context);
    if(img.length){
      style = img.attr('style');
      style = style.replace('ajax-loader-small.gif', 'pencil.png');
      img.attr('style', style);
      return;
    }

  }
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

  // Always display the tutorial and example links on top of the data table
  jQuery("#fieldset-data-input .eeaforms-group-help").remove();
  jQuery("#spreadsheet_help").show();
  updateTutorialLinks();
});
