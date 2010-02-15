# e-Linguistics Toolkit: utils 
#
# Copyright (C) 2008 ELTK Project
# Author:       Scott Farrar <farrar@u.washington.edu>
# URL: <http://purl.org/linguistics/eltk>
# For license information, see LICENSE.TXT

"""
This utils module contains various useful functions concerning the store.
"""

import MySQLdb

from rdflib.store import Store
from rdflib import plugin

from eltk.config import STORE_CONFIG

def resetDB(dbconfig):
    """
    Reset a db and create a schema for the store.

    :param dbconfig: a config dict
    :type dbconfig: dict
    """
    
    host = dbconfig['host']
    user = dbconfig['user']
    password = dbconfig['password']
    database = dbconfig['db']
    
    
    db = MySQLdb.connect(host,user,password)

    c = db.cursor()

    c.execute("""show databases;""")

    row = c.fetchall()
    
    #if db has already been created
    if (database,) in row:
    
        #then delete it in order to create empty instance
        c.execute('drop database '+database+';')

        print "Dropping "+database
    
    #create empty instance
    c.execute('create database '+database+';')
    
    print "Creating "+database

    #create the store schema
    print "Initializing "+database
    
    store = plugin.get('MySQL', Store)() #('GOLDComms_id')
    
    #convert to config string compatible w RDFLIB
    rdflib_config_string = 'host='+host+',user='+user+',password='+password+',db='+database
    #open db and create schema
    store.open(rdflib_config_string, create=True)



if __name__=='__main__':

    resetDB(STORE_CONFIG)

