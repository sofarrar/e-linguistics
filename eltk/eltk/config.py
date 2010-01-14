# e-Linguistics Toolkit: config 
#
# Copyright (C) 2008 ELTK Project
# Author: Scott Farrar <farrar@u.washington.edu>
# URL: <http://purl.org/linguistics/eltk>
# For license information, see LICENSE.TXT
import os


from eltk import __file__

ELTK_HOME=os.path.abspath(os.path.join(os.path.split(__file__)[0],''))

#change this for local settings
STORE_CONFIG = {'host':'localhost','user':'farrar','password':';lkjJK','db':'GOLDComm'}
