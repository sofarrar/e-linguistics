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



    store = plugin.get('MySQL', Store)() #('GOLDComms_id')
    
    #convert to config string compatible w RDFLIB
    rdflib_config_string = 'host='+STORE_CONFIG['host']+',user='+STORE_CONFIG['user']+',password='+STORE_CONFIG['password']+',db='+STORE_CONFIG['db']
    
    #open
    store.open(rdflib_config_string, create=False)

    graph1=''
    graph2=''

    """
    for c in store.contexts():
        #print c.identifier
        #print c.identifier
        if c.identifier==URIRef('http://purl.org/linguistics/gold'):
            graph1 = c

        if c.identifier==URIRef('http://uakari.ling.washington.edu/e-linguistics/goldcomm/data/LeipzigData.rdf'):
            graph2 = c

    #print len(graph1)
    #print len(graph2)
    #ga = ReadOnlyGraphAggregate([graph1,graph2])
    """


    cg = ConjunctiveGraph(store)
    print len(cg)
    #results = sparqlQuery('SELECT ?o WHERE {?s rdfs:comment ?o } ',graph1)
    #results = sparqlQuery("SELECT ?s WHERE {?s gold:orthographicRep 'karhulle' } ",graph2)

    results = sparqlQuery('SELECT  ?o WHERE {<http://purl.org/linguistics/gold/%s> rdfs:comment ?o }' % 'VerbPhrase',cg)


    #results = getUnitBasedOnForm(cg,"aqaɬxíla")


    for r in results:
        print r[0]





