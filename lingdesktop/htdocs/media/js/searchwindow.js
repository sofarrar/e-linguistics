// LingDesktop: 
// //
// // Copyright (C) 2010 LingDesktop Project
// // Author:       Scott Farrar <farrar@uw.edu>
// //               Dwight van Tuyl <dvantuyl@uw.edu> 
// // URL: <http://purl.org/linguistics/lingdeskop>
// // For license information, see LICENSE.txt
//
//

Ext.onReady(function(){
    Ext.BLANK_IMAGE_URL = '../htdocs/media/js/ext/resources/images/default/s.gif';


    Ext.QuickTips.init();


    Ext.override(Ext.Window,{
        onEsc:function(){
	    Ext.emptyFn;  
	}
    });





    //main window
    var win = new Ext.Window({

        layout:'border',
        border: false,
        title: 'Welcome to LingDesktop Search',
        height: 500,
        width: 800,
        items: [
            {
                //main ontology panel
                title: 'Ontology Navigator',
                region:'west',
                collapsible: false,
                split: true,
                //margins: '5 0 0 0',
                //cmargins: '5 5 0 0',
                width: 250,
                //minSize: 100,
                //maxSize: 450,
                layout: 'accordion',
                border: false,
                
                //sections of the ontology to be displayed
                items: [
                    {
                        xtype:'treepanel',
                        id: 'phonetic-feature-tree',
                        title: 'phonetic features',
                        collapsed: true,
                        autoScroll:true,
                        animate:true,
                        ddGroup: 'gridDDGroup',
                        enableDrag:true,
                        containerScroll: true,
                        rootVisible: false,
                        frame: true,
                        // auto create TreeLoader
                        dataUrl: '../htdocs/media/json/PhoneticProperty.json',
			root: {
                            nodeType: 'async'
                        }
                    }, //eo feature-tree
                    
		    {
                        xtype:'treepanel',
                        id: 'morphosemantic-feature-tree',
                        title: 'morphosemantic features',
                        collapsed: true,
                        autoScroll:true,
                        animate:true,
                        ddGroup: 'gridDDGroup',
                        enableDrag:true,
                        containerScroll: true,
                        rootVisible: false,
                        frame: true,
                        // auto create TreeLoader
                        dataUrl: '../htdocs/media/json/MorphosemanticProperty.json',
			root: {
                            nodeType: 'async'
                        }
                    }, //eo feature-tree
		    {
                        xtype:'treepanel',
                        id: 'pos-tree',
                        title: 'parts of speech',
                        collapsed: true,
                        autoScroll:true,
                        animate:true,
                        ddGroup: 'gridDDGroup',
                        enableDrag:true,
                        containerScroll: true,
                        rootVisible: false,
                        frame: true,
                        root: {
                            nodeType: 'async'
                        },
                        // auto create TreeLoader
                        dataUrl: '../htdocs/media/json/POS.json'
                    },//eo pos-tree
                    {
                        xtype:'treepanel',
                        id: 'lingunit-tree',
                        title: 'linguistic units',
                        collapsed: true,
			ddGroup: 'gridDDGroup',
                        enableDrag:true,
                        autoScroll:true,
                        animate:true,
                        containerScroll: true,
                        rootVisible: false,
                        
                        frame: true,
                        root: {
                            nodeType: 'async'
                        },
                        // auto create TreeLoader
                        dataUrl: '../htdocs/media/json/lingunit.json'
                        
                    }//eo lingunit
                ]
            },

            {
                //main center component of window
                collapsible: false,
                region:'center',
                layout: 'border',
                border: false,
                margins: '5 5 5 5',
                items: [
                    {
                        //quick search
                        xtype:'form',
                        id: 'search-form',
                        title: ' ',
                        region: 'north',
			margins: '5 5 5 5',
                        height: 50,
                        layout: 'column',
                        items: [
                            //{columnWidth: .1},
	    
                            textsearch,
                            
                            {columnWidth: .1},

                            {columnWidth: .1},

                            {columnWidth: .1},
	    
                            //sample query combo was here,numberField    
                        ]
                    },
                    {
                        xtype: 'panel',
                        id: 'results-panel',
                        title: 'Results',
                        region: 'south',

                        //layout: 'fit',
                        height: 300,
                        minSize: 75,
                        maxSize: 250,
                        cmargins: '5 0 0 0',
                        collapsible: 'true',
                        autoScroll: true
                        //items: [{xtype: 'textarea', id: 'results-textarea', disabled: true}]
	
       
                    },

                    {
                        xtype: 'form',
			id: 'sparql-form',
                        region: 'center',
			margins: '5 5 5 5',
                        layout: 'fit',
			url: 'sparql',
			

			
                        items: [
                            {	
                                xtype: 'textarea',
                                id: 'query-textarea',
				region: 'north',
                                emptyText: 'Compose SPARQL query...',
                                listeners: {
				    //alert(Ext.getCmp('query-textarea').getForm();),
                                    setValue: function(blah){
                                    alert('ok');
                                    //focus: function(blah) {
                                    //valid: function(blah) {    
                                    //   alert('ok');
                                    }
                                }
                            }//eo textarea
			    

                        ],//eo items
                        buttonAlign: 'left',
                        buttons: [
                            {
				xtype:'button',
				text:'Submit',
				
				handler: function() {
				    
				    Ext.Ajax.request({
					
					
					params: {query: Ext.getCmp('query-textarea').getValue()},
					url: 'sparql',                
					success: function ( result, request ) {
					    //alert('success');
					    Ext.getCmp('results-panel').body.update('');
					    var jsonData = Ext.util.JSON.decode(result.responseText);
					    
					    
					    //Ext.getCmp('results-panel').body.update(jsonData.results[1].comment);
                            
				
					    var resultsLength = jsonData.results.length;

					    var resultsHtml = '<h1>{label}</h1> <p> {comment}</p>';
					    var resultsTpl = new Ext.Template(resultsHtml);
					    resultsTpl.compile();



					    Ext.getCmp('results-panel').setTitle('Results 1 to '+resultsLength);
                            
						for (var x = 0; x < resultsLength; x++){
                                   
						    var mylabel = jsonData.results[x].label;
						    var mycomment = jsonData.results[x].comment;
                                   
						    //also works
						    //Ext.getCmp('results').body.update(Ext.getCmp('results').body.dom.innerHtml + ' ' +comment); 
                             
						    resultsTpl.append(
						    Ext.getCmp('results-panel').body,
							{
                                                        label:mylabel,
                                                        comment:mycomment
						    }
						    );      
						}
					    
					}, // eo function onSuccess
					
					failure: function(result, request ) {
					    //alert('fail');
					    Ext.getCmp('results-panel').body.update('<h1>No results</h1>');

					}, //eo function failure		
					
					waitMsg:'Processing query...'
				    });
				} // eo function submit
			    },
                            {
                                xtype: 'button',
                                text: 'New Query',
                                handler:function() {
                                    Ext.getCmp('query-textarea').reset();
				    Ext.getCmp('results-panel').body.update('');

                                }
                            },
			    samplequery

                        ]
                    }//eo form
            ]
        }]
    });//eo win

    //Shows the window, rendering it first if necessary, or activates it and brings it to front if hidden.
    win.show(this);


	//Ext.getCmp('feature-tree').expandPath(Ext.getCmp('feature-tree').getRootNode().getPath());
	//Ext.getCmp('pos-tree').expandPath(Ext.getCmp('pos-tree').getRootNode().getPath());
	//Ext.getCmp('lingunit-tree').expandPath(Ext.getCmp('lingunit-tree').getRootNode().childNodes[0].getPath());
                        
	
    var target0 = Ext.getDom('query-textarea');        
    var dropTarget = new Ext.dd.DropTarget(target0, {
        ddGroup     : 'gridDDGroup',
	
	notifyDrop  : function(ddSource, e, data){
	
	    // Load the record into the form
	    Ext.getCmp('query-textarea').setValue(data.node.text);
	
	    return(true);
	}
    });
	
});//eo onReady
