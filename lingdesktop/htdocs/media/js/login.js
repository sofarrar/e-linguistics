// LingDesktop: 
//
// Copyright (C) 2010 LingDesktop Project
// Author:       Scott Farrar <farrar@uw.edu>
//               Dwight van Tuyl <dvantuyl@uw.edu> 
// URL: <http://purl.org/linguistics/lingdeskop>
// For license information, see LICENSE.txt

    // Create a variable to hold our EXT Form Panel. 
    // Assign various config options as seen.    
    var login = new Ext.FormPanel({ 
        labelWidth:80,
        //url:'loginrequest', 
        frame:true, 
        title:'Please Login', 
        defaultType:'textfield',
    monitorValid:true,
    // Specific attributes for the text fields for username / password. 
    // The "name" attribute defines the name of variables sent to the server.
        items:[{ 
                fieldLabel:'Username', 
                name:'username', 
                allowBlank:false 
            },{ 
                fieldLabel:'Password', 
                name:'password', 
                inputType:'password', 
                allowBlank:false 
            }],
 
    // All the magic happens after the user clicks the button     
        buttons:[{ 
                text:'Login',
                formBind: true,  
                // Function that fires when user clicks the button 
                handler:function(){ 
                    login.getForm().submit({ 
                        
                        
                        url:'login/', 
                        method:'POST',
                         
                        waitTitle:'Connecting', 
                        waitMsg:'Sending data...',
                        
                        //if success
                        success:function(){ 
                            Ext.Msg.alert('Status', 'Login Successful!', 
                                function(btn, text){
                                    if (btn == 'ok'){
                                        var redirect = '/mainmenu/'; 
                                        window.location = redirect;
                                    }    
                                });
                        },
 
                        //if failure
                        failure:function(form, action){ 
                            if(action.failureType == 'failure'){ 
                                obj = Ext.util.JSON.decode(action.response.responseText); 
                                Ext.Msg.alert('Login Failed!', obj.errors.reason); 
                            }
                            
                            else{ 
                                Ext.Msg.alert('Warning!', 'Authentication server is unreachable : ' + action.response.responseText); 
                            } 
                            
                            login.getForm().reset(); 
                        } 
                    }); 
                } 
            }] 
    });


Ext.BLANK_IMAGE_URL = '../htdocs/media/js/ext/resources/images/default/s.gif'; 

Ext.onReady(function(){
    Ext.QuickTips.init();
 
 
    // This just creates a window to wrap the login form. 
    // The login object is passed to the items collection.       
    var win = new Ext.Window({
        layout:'fit',
        width:300,
        height:150,
        closable: false,
        resizable: false,
        plain: true,
        border: false,
        items: [login]
    });
    win.show();
});
