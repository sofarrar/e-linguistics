// LingDesktop: 
//
// Copyright (C) 2010 LingDesktop Project
// Author:       Scott Farrar <farrar@uw.edu>
//               Dwight van Tuyl <dvantuyl@uw.edu> 
// URL: <http://purl.org/linguistics/lingdeskop>
// For license information, see LICENSE.txt

Ext.onReady(function() {
        
    Ext.BLANK_IMAGE_URL = '../htdocs/media/js/ext/resources/images/default/s.gif';

    Ext.QuickTips.init();


    var viewport = new Ext.Viewport({

        layout:'fit',

        items:[{

            xtype: 'grouptabpanel',

    		tabWidth: 130,

    		activeGroup: 0,

    		items: [{

    			mainItem: 1,

    			items: [{

    				title: 'Ticket',

                    layout: 'fit',

                    iconCls: 'x-icon-tickets',

                    tabTip: 'Tickets blah',

                    style: 'padding: 10px;',

    				items: [new SampleGrid([0,1,2,3,4])]

    			}, 

                {

                    xtype: 'portal',

                    title: 'Dashboard',

                    tabTip: 'Dashboard tabtip',

                    items:[{

                        columnWidth:.33,

                        style:'padding:10px 0 10px 10px',



    }); //eo viewport


})//eoi onReady
