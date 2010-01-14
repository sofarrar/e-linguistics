import codecs

from eltk.reader.LinkedDataReader import *

from eltk.kb.Meta import *

from eltk.utils.sparql import getComments

"""
This script creates the intial data for the GOLDComm db
"""

reader = LinkedDataReader()

print 'need to set GOLD_graph variable to your local environment'
#GOLD_graph = reader.parseGraph('/home/farrar/svn_projects/goldcomm/gold/gold-2009.owl')


GOLD = reader.buildPyModel()


jsonfile = codecs.open('initial_data.json','w','utf-8')

jsonfile.write('[')

for c in GOLD.getOWLClasses():
    
    comm = ''

    for comment in getComments(GOLD_graph,c.uri):
        
        comm=comm+comment
    


    urimodel = '\t{"pk": "%s", "model": "search.urimodel", "fields": {"label":"%s", "comment":"%s"}},\n\n'% (c.uri,c.name,comm[0:200])

    wordmodel = '\t{"pk": "%s", "model": "search.wordmodel", "fields": {"uri": ["%s"]}},\n\n' % (c.name,c.uri)

    jsonfile.write(urimodel)
    jsonfile.write(wordmodel)


jsonfile.write(']')

jsonfile.close()
