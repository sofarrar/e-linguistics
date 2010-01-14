# LingDesktop: README 
#
# Copyright (C) 2010 LingDesktop Project
# Author:       Scott Farrar <farrar@uw.edu>
#               Dwight van Tuyl <dvantuyl@uw.edu> 
# URL: <http://purl.org/linguistics/lingdeskop>
# For license information, see LICENSE.txt


LingDesktop
===========

Important
---------

first see:
http://code.djangoproject.com/wiki/NewbieMistakes

Uploading for deployment
------------------------

A Django project requires special care when migrating from a local machine to a deployment environment. For instance, you'll need to change a few things in the settings file. So, when uploading to a deployment server:


-set DEBUG = True to DEBUG = False 
 
-reset soft link, lingdesktop/htdocs/media/js/ext to wherever the ext library is on the server


Double check URLs
------------------

-double check all path and url values in js dir, that they do not contain local paths 


Server config
-------------

-verifiy that server can import packages like eltk 

-set path in lingdesktop.fcgi file for eltk 

-see sample lingdesktop.fcgi script at end of this README

-set egg cache var to a local dir and chmod 777, ie +wxr

Database issues
----------------

-dir above db must be 777, at least for sqlite3

-specify full path to db in settings file

-db should be 777

for debugging:
--------------

(this pertains to the Patas server)

apache reset:

sudo /etc/init.d/httpd restart

see error log:

/var/log/httpd/error_log




Sample .fcgi file
------------------

#!/opt/python-2.6/bin/python2.6
import sys, os

# Add a custom python path.
sys.path.insert(0, "/home2/farrar/e-linguistics/dev")
sys.path.insert(0, "/home2/farrar/lib/eltk")

# Switch to the directory of your project.  (Optional.)
os.chdir("/home2/farrar/e-linguistics/dev/lingdesktop/")

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "lingdesktop.settings"

# Set the egg cache to somewhere the web server can write to
os.environ['PYTHON_EGG_CACHE'] = '/home2/farrar/tmp'

#I was testing w this setting:
#
#os.environ['PYTHON_EGG_CACHE'] = '/home2/farrar/e-linguistics/dev/lingdesktop/tmp'

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")


