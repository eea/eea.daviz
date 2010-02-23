function DavizTableStyler(table, database){
  jQuery(table).addClass('listing');
};

function DavizTableRowStyler(item, database, tr) {
  if (tr.rowIndex % 2) {
    jQuery(tr).addClass('odd');
  } else {
    jQuery(tr).addClass('even');
  }
};
