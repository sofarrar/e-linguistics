# e-Linguistics Toolkit: config 
#
# Copyright (C) 2008 ELTK Project
# Author: Scott Farrar <farrar@u.washington.edu>
# URL: <http://purl.org/linguistics/eltk>
# For license information, see LICENSE.TXT
import os

from eltk import __file__
"""
The config file contains the ELTK_HOME variable and the particular Store config for your local db.
"""

ELTK_HOME=os.path.abspath(os.path.join(os.path.split(__file__)[0],''))

#change this for local settings
STORE_CONFIG = {'host':'localhost','user':'farrar','password':';lkjJK','db':'GOLDComm'}
