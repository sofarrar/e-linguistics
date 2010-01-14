// LingDesktop: 
//
// Copyright (C) 2010 LingDesktop Project
// Author:       Scott Farrar <farrar@uw.edu>
//               Dwight van Tuyl <dvantuyl@uw.edu> 
// URL: <http://purl.org/linguistics/lingdeskop>
// For license information, see LICENSE.txt



Ext.onReady(function(){
 
    var simple = new Ext.form.FormPanel({
 
 
        standardSubmit: true,
 
        collapsible:true,
        frame:true,
        title: 'Create a user account',
 
        width: 350,
        defaults: {width: 230},
        defaultType: 'textfield',
        items: [{
                fieldLabel: 'Username',
                name: 'username',
                allowBlank:false
            },
            {
            fieldLabel: 'E-mail address',
            name: 'e-mail',
            allowBlank: false
            },
            {
            fieldLabel: 'Password',
            name: 'password',
            allowBlank: false
            },
            {
                inputType: 'hidden',
                id: 'submitbutton',
                name: 'myhiddenbutton',
                value: 'hiddenvalue'
            }
 
        ],
        buttons: [{
            text: 'Create',
            handler: function() {
                simple.getForm().getEl().dom.action = 'create/';
                simple.getForm().getEl().dom.method = 'POST';
                simple.getForm().submit();
            }
        }]
 
 
    });
 
 
 
    simple.render('createuserform');
 
 
 
});
