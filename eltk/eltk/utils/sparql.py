# -*- coding: UTF-8 -*-
#
# e-Linguistics Toolkit: sparql
#
# Copyright (C) 2008 ELTK Project
# Author: Scott Farrar <farrar@u.washington.edu>
# URL: <http://purl.org/linguistics/eltk>
# For license information, see LICENSE.TXT 
"""
The sparql module contains several functions that wrap commonly used SPARQL queries in Python code.
"""

from rdflib import RDF,RDFS
from eltk.namespace import OWLNS,GOLDNS


def sparqlQuery(sparql_string,context):
    """
    sparqlQuery is a wrapper function for making queries over specific contexts within the store.

    :param sparql_string: Well formed SPARQL query
    :type sparql_string: str
    :param context: A graph
    :type context: rdflib.Graph.Graph
    :returns: A list of tuples containing the results
    :rtype: list
    """

    #Open the store
    #get the db plugin
    #store = plugin.get('MySQL', Store)() #('GOLDComms_id')
    
    #convert to config string compatible w RDFLIB
    #rdflib_config_string = 'host='+STORE_CONFIG['host']+',user='+STORE_CONFIG['user']+',password='+STORE_CONFIG['password']+',db='+STORE_CONFIG['db']
    
    #open
    #store.open(rdflib_config_string, create=False)

    
    results=[]
    ns = dict(rdf=RDF.RDFNS,rdfs=RDFS.RDFSNS, gold=GOLDNS)
    for i in context.query(sparql_string,initNs=ns):
        results.append(i)
    return results




def getBaseClasses(graph,cls_uri):
    """
    :param graph: the relevant graph to process
    :type graph: rdflib.Graph.Graph
    :param cls_uri: the URI of the particular class
    :type cls_uri: rdflib.URIRef.URIRef
    :rtype: list
    """
    baseclasses = []

    ns = dict(rdf=RDF.RDFNS,rdfs=RDFS.RDFSNS,owl=OWLNS)
    
    for bc in graph.query('SELECT ?bc WHERE {<'+cls_uri+'> rdfs:subClassOf ?bc} ', initNs=ns):

        baseclasses.append(bc[0])
    return baseclasses

   

def getSubClasses(graph,cls_uri):
    """
    Given an rdflib.graph.Graph and a URIRef of some OWL class, return a list of subclasses
    
    
    :param graph: the graph to search
    :type graph: rdflib.graph.Graph
    :param cls_uri:
    :type cls_uri: rdflib.URIRef.URIRef
    :rtype: list
    """
    subclasses = []
        
    ns = dict(rdf=RDF.RDFNS,rdfs=RDFS.RDFSNS,owl=OWLNS)

    for sc in graph.query('SELECT ?sc WHERE {?sc rdfs:subClassOf <'+cls_uri+'> } ', initNs=ns):

        subclasses.append(sc[0])
    return subclasses


def getIndividuals(graph):
    """
    getIndividuals returns a dictionary where keys are URIRefs of individuals and values are lists of types (ie OWL class URIs)
    
    :param graph: the relevant graph to process
    :type graph: rdflib.graph.Graph
    :returns: (keys)  individual URIs, (values) lists of types, OWL class URIs 
    :rtype: dict
    """
    
    #to be returned 
    ind_class_pair={}

    ns = dict(rdf=RDF.RDFNS,rdfs=RDFS.RDFSNS,owl=OWLNS)

    #SPARQL query for finding all OWL individuals and their types, as a list
    #
    #for i in self.graph.query('SELECT ?i ?c WHERE {?i rdf:type ?c . ?c rdf:type <http://www.w3.org/2002/07/owl#Class> . }', initNs=ns):
        
    #use for termset
    for i in graph.query('SELECT ?i ?c WHERE {?i rdf:type ?c} ', initNs=ns):

        #build the return dict
        #
        #create indiv. and its type in a list
        if i[0] not in ind_class_pair.keys():
            ind_class_pair[i[0]]=[i[1]]
            
        
        #if an indiv. has multiple types, append to list
        else:
            
            ind_class_pair[i[0]].append(i[1])
    
    #precess triples, basically ABox statements
    return ind_class_pair


def getOWLClasses(graph):
    """
    Return all OWL Classes in a graph'
    
    
    :param graph: the graph to search
    :type graph: rdflib.graph.Graph
    :rtype: list
    """
    classes=[]

    ns = dict(rdf=RDF.RDFNS,rdfs=RDFS.RDFSNS,owl=OWLNS)

    for c in graph.query('SELECT ?c WHERE {?c rdf:type <http://www.w3.org/2002/07/owl#Class> } ', initNs=ns):

        classes.append(c)
        print c
    return classes

def getComments(graph,uri_string):
    """
    Return all comments associated with some URI
    
    
    :param graph: the graph to search
    :type graph: rdflib.Graph.Graph
    :param uri_string: a URI of some concept
    :type uri_string: str
    :rtype: list
    """


    comments=[]

    ns = dict(rdf=RDF.RDFNS,rdfs=RDFS.RDFSNS,owl=OWLNS)

    for c in graph.query('SELECT ?c WHERE {<%s> rdfs:comment ?c }' % uri_string, initNs=ns):

        comments.append(c[0])
        
    return comments




def getOWLObjectProperties(graph):
    """
    Return all OWL ObjectProperties in a graph'
    
    
    :param graph: the graph to search
    :type graph: rdflib.graph.Graph
    :rtype: list
    """
    object_props=[]

    ns = dict(rdf=RDF.RDFNS,rdfs=RDFS.RDFSNS,owl=OWLNS)

    for op in graph.query('SELECT ?op WHERE {?op rdf:type <http://www.w3.org/2002/07/owl#ObjectProperty> } ', initNs=ns):

        object_props.append(op)
        print op

    return object_props

def getOWLDatatypeProperties(graph):
    """
    Return all OWL DataProperties in a graph'
    
    :param graph: the graph to search
    :type graph: rdflib.graph.Graph
    :rtype: list
    """   
    data_props=[]

    ns = dict(rdf=RDF.RDFNS,rdfs=RDFS.RDFSNS,owl=OWLNS)

    for dp in graph.query('SELECT ?dp WHERE {?dp rdf:type <http://www.w3.org/2002/07/owl#DatatypeProperty> } ', initNs=ns):

        data_props.append(dp)
        
        print dp

    return data_props





def getABoxTriples(graph):
    """
    Return all triples in a graph'
    
    :param graph: the graph to search
    :type graph: rdflib.graph.Graph
    :rtype: list
    """

    ns = dict(rdf=RDF.RDFNS,rdfs=RDFS.RDFSNS,owl=OWLNS)
    
    triples = []
    
    for t in graph.query('SELECT ?s ?p ?o WHERE {?s ?p ?o} ', initNs=ns):
        triples.append(t)
    
        #if t[2]==URIRef(u'http://purl.org/linguistics/gold#Tense'): print t[0]
        print t

    return triples

def getUnitBasedOnForm(graph,form):
    """
    Return linguistic units accordings to a particular form 
    
    :param graph: the relevant graph
    :type graph: rdflib.graph.Graph
    :param form: the form to search for
    :type form: str
    :rtype: list
    """

    ns = dict(rdf=RDF.RDFNS,rdfs=RDFS.RDFSNS,owl=OWLNS,gold=GOLDNS)
    
    results = []
    
    #for t in graph.query("SELECT ?s  WHERE {?s gold:orthographicRep '%s' }" % form , initNs=ns):
    for r in graph.query("SELECT ?s ?o  WHERE {?s gold:orthographicRep ?o  }", initNs=ns):
        
        #if r[1]=='karhulle':
        if r[1].startswith(form):
        
            results.append(r[0])
             

    return results


def findDataType(graph,uri):
    
    """
    Return a Python data object's type given a URI
    
    :param uri: a URI of any linguistic datatype instance (IGT, Lex, etc.)
    :type uri: rdflib.URIRef.URIRef
    :rtype: rdflib.URIRef.URIRef
    """

    return_uri = ''

    ns = dict(rdf=RDF.RDFNS,rdfs=RDFS.RDFSNS,owl=OWLNS,gold=GOLDNS)
    
    datatype = graph.query("SELECT ?t WHERE {<"+uri+"> rdf:type ?t}", initNs=ns)
    
    for d in datatype:
        return_uri = d

    return return_uri[0]



if __name__=='__main__':

    #for testing
    from eltk.reader.LinkedDataReader import LinkedDataReader
    from eltk.config import ELTK_HOME
    from rdflib.URIRef import URIRef

    reader = LinkedDataReader()
    
    GOLD_graph = reader.parseGraph(ELTK_HOME+'/examples/inputfiles/gold-2009.owl')
    
    #x = getBaseClasses(GOLD_graph,URIRef('http://purl.org/linguistics/gold/CommonNoun'))    
    
    #print x

    #comments = getComments(GOLD_graph,'http://purl.org/linguistics/gold/CommonNoun')




    for c in comments:
        print c
