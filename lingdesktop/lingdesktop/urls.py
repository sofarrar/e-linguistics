# LingDesktop: 
#
#Copyright (C) 2010 LingDesktop Project
#     Author:       Scott Farrar <farrar@uw.edu>
#                   Dwight van Tuyl <dvantuyl@uw.edu> 
#     URL: <http://purl.org/linguistics/lingdeskop>
#     For license information, see LICENSE.txt



import os

from django.conf.urls.defaults import *
from lingdesktop import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/',include(admin.site.urls)),
    (r'^$','lingdesktop.views.index'),
    (r'^createuser/$','lingdesktop.views.createuser_prompt'),
    (r'^createuser/create/$','lingdesktop.views.createuser'),
    (r'^login/$','lingdesktop.views.login_prompt'),
    (r'^login/login/$','lingdesktop.views.loginuser'),
    (r'^logout/$','lingdesktop.views.logout_view'),

    (r'^accounts/login/$', 'django.contrib.auth.views.login'),


    #(r'^login/mainmenu/$','lingdesktop.views.mainmenu'),
    (r'^mainmenu/$','lingdesktop.views.mainmenu'),
    
    #add this back in
    #(r'^lingdesktop/$','lingdesktop.views.lingdesktop'),

    (r'^login/failure','lingdesktop.views.failure'),
    #(r'^termseteditor/', include('lingdesktop.termseteditor.urls')),
    (r'^search/', include('lingdesktop.search.urls'))
    
    #testing
    #(r'^htdocs/media/(.*)$', 'django.views.static.serve', static_files_dict)
)

#Scott added this to facilitate deployment
if settings.DEBUG:
    urlpatterns += patterns('', 
        (r'^htdocs/media/(.*)$', 'django.views.static.serve',{'document_root': os.path.join(settings.PROJECT_PATH, '..', 'htdocs/media/')})
    )
            

