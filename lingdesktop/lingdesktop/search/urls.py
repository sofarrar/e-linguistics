# LingDesktop: 
#
#Copyright (C) 2010 LingDesktop Project
#     Author:       Scott Farrar <farrar@uw.edu>
#                   Dwight van Tuyl <dvantuyl@uw.edu> 
#     URL: <http://purl.org/linguistics/lingdeskop>
#     For license information, see LICENSE.txt


from django.conf.urls.defaults import *
from lingdesktop import settings

urlpatterns = patterns('lingdesktop.search.views',
        (r'^results/$','results'),
        (r'^contact/$','contact'),
        (r'searchpage','searchpage'),
        (r'textSearch','textSearch'),

        
        (r'word','findword'),

        (r'sparql','sparqlquery'),

        #testing
        #use wildcard to return any json
        (r'concepts.json','servejson'),
        (r'topics-remote.json','serveforum'),

        
)
