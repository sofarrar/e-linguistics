# -*- coding: UTF-8 -*-
# e-Linguistics Toolkit: store 
#
# Copyright (C) 2008 ELTK Project
# Author:       Scott Farrar <farrar@u.washington.edu>
# URL: <http://purl.org/linguistics/eltk>
# For license information, see LICENSE.TXT

"""
The store module is the gatekeeper for populating and maintaining the RDF store db.
"""


from cStringIO import StringIO

#note, fix rdflib imports when rdflib-2.5 is finalized

#rdflib-2.5
#from rdflib.graph import Graph
from rdflib.Graph import Graph

#from rdflib.namespace import Namespace
from rdflib.Namespace import Namespace

#from rdflib.term import URIRef
from rdflib.URIRef import URIRef

from rdflib import RDF,RDFS

from rdflib.Graph import Graph, ConjunctiveGraph, ReadOnlyGraphAggregate

from rdflib import plugin, exceptions
from rdflib.syntax.parsers import Parser

#from rdflib.store.IOMemory import IOMemory
from rdflib.store import Store

from eltk.config import ELTK_HOME
from eltk.config import STORE_CONFIG 


from eltk.namespace import *

from eltk.utils.sparql import *    

from eltk.utils.functions import getLocalName

def getIdentifier(graph):
    """
    Return the dc:identifier from a graph, given its location
    
    :param graph: an input RDF graph 
    :type graph: rdflib.graph.Graph
    :rtype: rdflib.URIRef.URIRef
    """

    for t in graph.predicate_objects():
        
        if t[0]==URIRef("http://purl.org/dc/elements/1.1/identifier"):
            return URIRef(t[1])

#this class may turn out to be useful for
#programmatically creating queries from the UI
#
#class SparqlQuery(object):
#    def __init__(self,s,p,w):
#        
#        self.select_vars = s
#        self.predicate = p
#        self.where_vars = w
#    
#    def __str__(self):
#        return 



def addToStore(rdf_tuple):
    """
    Add an RDF graph to the store. 

    :param graph_tuple: (url,raw_rdf)
    :type graph_tuple: tuple
    """

    #Open the store
    #
    #get the db plugin
    store = plugin.get('MySQL', Store)() #('GOLDComms_id')
    
    #convert to config string compatible w RDFLIB
    rdflib_config_string = 'host='+STORE_CONFIG['host']+',user='+STORE_CONFIG['user']+',password='+STORE_CONFIG['password']+',db='+STORE_CONFIG['db']
    
    #open the store but don't reset/create it
    store.open(rdflib_config_string, create=False)
    
    #temp graph for determining identifier
    g = Graph()
    g.parse(StringIO(rdf_tuple[1]))
    
    #get the dc:identifier if one is declared in the graph
    graph_id = getIdentifier(g)
    #else, just use the URL
    if graph_id is None: graph_id = URIRef(rdf_tuple[0])
    


    #build arrary of contexts ids in store
    context_ids = []
    for c in store.contexts(): 
        context_ids.append(c.identifier)
   

    #######DOESN'T seem to WORK ???#############
    #
    #add graph if it's not already there
    #
    #The idea is to avoid adding a duplicate graph if graphs:
    # -have same dc:identifier
    # -are located at different URLs
    if graph_id not in context_ids:
     
        graph = Graph(store=store,identifier=graph_id)
        graph.parse(StringIO(rdf_tuple[1]))
        graph.commit()

    #################################################
    #experiment: add triples one by one from temp graph
    #    but doesn't work either
    # 
    #for t in g:
    #    store.add(t,context=g.identifier)
    #    
    #store.commit()

   
    #print '*********************************'
    #print 'added %s to store' % graph.identifier
    #print '%s was graph_id of type %s' % (graph_id,type(graph_id))
    #print '*********************************'
    

########################
#not yet used
#######################
#def getImports(graph):
#        
#    ns = dict(rdf=RDF.RDFNS,rdfs=RDFS.RDFSNS,owl=OWLNS)
#
#    import_resources = []
#        
#    for o in graph.query('SELECT ?o WHERE {?x owl:imports ?o} ', initNs=ns):
#        import_resources.append(o[0])
#
#    return import_resources




#def parseGraph(uri):
#    
#    g = Graph(identifier='')
#    
#    g.parse(uri)
#            
#    for i in getImports(g):
#        
#        #how to merge?!
#        merge(g,parseGraph(i))
#        
#    return g


if __name__=='__main__':


    from eltk.reader.LinkedDataReader import LinkedDataReader
    from rdflib.Literal import Literal


    reader = LinkedDataReader()
     
    GOLD_graph = reader.parseGraph('/home/farrar/git-repos/e-linguistics/goldcomm/gold/gold-2009.owl')
    
    GOLD = reader.buildPyModel()


    #get the right plugin
    store = plugin.get('MySQL', Store)() 
    
    #convert to config string compatible w RDFLIB
    rdflib_config_string = 'host='+STORE_CONFIG['host']+',user='+STORE_CONFIG['user']+',password='+STORE_CONFIG['password']+',db='+STORE_CONFIG['db']
    
    #open the store (GOLDComm)
    store.open(rdflib_config_string, create=False)

    #declare conjunctive graph
    graph1=''
    
    #find the right conjgraph within the store
    for c in store.contexts():

        if c.identifier==URIRef('http://purl.org/goldcomm/user1'):
            graph1 = c
    

    from eltk.utils.sparql import findDataType
    from eltk.kb.Meta import getType
    
    #what you want to retrieve from the graph 
    user_data = URIRef(u'http://mynamespace/n1')

    #import a specialized sparql query to get the user data's type
    type = findDataType(graph1,user_data)
    
    #gold_class is the Python metaclass for that type, e.g., GOLD.Noun
    gold_class = getattr(GOLD,getLocalName(type))
    
    #create a GOLD instance
    gold_inst = gold_class(user_data)
    
    #print the URI for verification
    print gold_inst.uri

    
#########################END TEST#######################


    #from eltk.reader.LinkedDataReader import LinkedDataReader
    #from rdflib.Literal import Literal


    #reader = LinkedDataReader()
     
    #GOLD_graph = reader.parseGraph(ELTK_HOME+'/examples/inputfiles/gold-2009.owl')
    #GOLD_graph = reader.parseGraph('/home/farrar/git-repos/e-linguistics/goldcomm/gold/gold-2009.owl')
    
    #GOLD = reader.buildPyModel()
    
    #print GOLD.Noun.uri

    #conjgraph = ConjunctiveGraph(store=store,identifier=URIRef('http://purl.org/goldcomm/user1'))

    #data = Namespace('http://purl.org/linguistics/data/')

    #conjgraph.bind('data',data)
    
    #n1 = GOLD.Noun(URIRef(u'http://mynamespace/n1'))
    
    
    #conjgraph.add((n1.getURI(), URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'), GOLD.Noun.getURI()))
    
    #conjgraph.add((n1.getURI(), GOLD.orthographicRep.getURI(), Literal('dog')))
    #conjgraph.commit()
    
    
    #results = sparqlQuery('SELECT ?o WHERE {?s rdfs:comment ?o } ',graph1)
    #results = sparqlQuery("SELECT ?s WHERE {?s gold:orthographicRep 'karhulle' } ",graph2)

    #results = sparqlQuery('SELECT  ?o WHERE {<http://purl.org/linguistics/gold/%s> rdfs:comment ?o }' % 'VerbPhrase',cg)



    #results = getUnitBasedOnForm(cg,"aqaɬxíla")


    #for r in results:
    #    print r[0]



    #for c in store.contexts():
        #print c.identifier
        #print c.identifier
        #if c.identifier==URIRef('http://purl.org/linguistics/gold'):
        #if c.identifier==URIRef('http://purl.org/goldcomm/user1'):
            #graph1 = c

        #if c.identifier==URIRef('http://uakari.ling.washington.edu/e-linguistics/goldcomm/data/LeipzigData.rdf'):
            #graph2 = c

