// LingDesktop: 
// //
// // Copyright (C) 2010 LingDesktop Project
// // Author:       Scott Farrar <farrar@uw.edu>
// //               Dwight van Tuyl <dvantuyl@uw.edu> 
// // URL: <http://purl.org/linguistics/lingdeskop>
// // For license information, see LICENSE.txt
//
//

var queries = [
    ['Suffix orthographicRep "xyz"','all suffixes of the form "ish"'],
    ['Verb hasConstituent Suffix','all verbs with a suffix'],
    ['noun hasConsistuent Morpheme, where Morpheme hasInflection Case','Case on noun'],
    ['orthographicRep "paucal number"','data labeled "paucal number"']
    ];
 
 
var samplequery = new Ext.form.ComboBox({
    

    width: 200,
    store: new Ext.data.SimpleStore({
        fields: ['sample-sparql','prose-form'],
        data : queries 
    }),
    displayField: 'prose-form',
    typeAhead: true,
    mode: 'local',
    triggerAction: 'all',
    emptyText:'Sample Query',
    selectOnFocus:true,
    onSelect: function(record){
        
        Ext.getCmp('query-textarea').setValue(record.get('sample-sparql'));
        //Ext.getCmp('query-textarea').append(record.get('sample-sparql'));
        
        this.collapse();
        this.reset();

    
    }

});

