// LingDesktop: 
// //
// // Copyright (C) 2010 LingDesktop Project
// // Author:       Scott Farrar <farrar@uw.edu>
// //               Dwight van Tuyl <dvantuyl@uw.edu> 
// // URL: <http://purl.org/linguistics/lingdeskop>
// // For license information, see LICENSE.txt
//
//


/*********************************************************
 quicksearch is the combo box to enable a quick search for
 concepts. Makes ajax call to /search/word
 
 ***********************************************************/
 
 var ds = new Ext.data.JsonStore({
    url: 'word',
    root: 'resultset',  // the root of the array you'll send down
    //idProperty: 'id',
    fields: ['label','comment']
});

 
 

    // Custom rendering Template for results
    var resultTpl = new Ext.XTemplate(
        '<tpl for="."><div class="search-item">',
            '<h3><span><br/>{label} </span></h3>',
            '{comment}',
        '</div></tpl>'
    );

    
     var textsearch = new Ext.form.ComboBox({
       id: 'textsearch',
       store: ds,
       displayField: 'label',
       typeAhead: true,
       mode: 'remote',
       queryParam: 'query',
       selectOnFocus: true,
       valueNotFoundText: 'not found...',
       emptyText: 'quick find',
       minChars: 4,
       hideTrigger: true,
       loadingText: 'Searching...',
       width: 150,
       pageSize:10,
       tpl: resultTpl,        
       itemSelector: 'div.search-item',
       
       //doesn't quite work
       //listeners: {
       //       onEsc:function(){
       //              this.reset();
       //       }
       //},
       
       onSelect: function(record){ 

       
              


              

              //Ext.getCmp('results').body.update(record.data.label);
              this.clearValue();
              Ext.getCmp('query-textarea').reset();
              Ext.getCmp('query-textarea').append(record.data.label);
              //this.setValue(record.data.label);
              this.collapse();
              this.reset();


        }
    });
