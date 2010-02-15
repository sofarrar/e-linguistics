# -*- coding: UTF-8 -*-
#
# e-Linguistics Toolkit: LinkedDataReader 
#
# Copyright (C) 2008 ELTK Project
# Author: Scott Farrar <farrar@u.washington.edu>
# URL: <http://purl.org/linguistics/eltk>
# For license information, see LICENSE.TXT
"""
The LinkedDataReader module contains the LinkedDataReader class used to read RDF resources.
"""
import abc

#note, fix rdflib imports when rdflib-2.5 is finalized

#rdflib-2.5
#from rdflib.graph import Graph
from rdflib.Graph import Graph

#from rdflib.namespace import Namespace
from rdflib.Namespace import Namespace

#from rdflib.term import URIRef
from rdflib.URIRef import URIRef

from rdflib import plugin, exceptions
from rdflib.syntax.parsers import Parser

from rdflib import RDF,RDFS

import eltk

from eltk.reader.Reader import Reader

from eltk.config import ELTK_HOME

from eltk.utils.functions import getLocalName
from eltk.utils.functions import quote

from eltk.utils import sparql


from eltk.kb.Meta import *
from eltk.kb.KBComponent import *

from eltk.namespace import *


#used in instancemethod below
def getSubClasses(self):
    return self._subclasses

class LinkedDataReader(Reader):

    """
    LinkedDataReader is a reader that is meant to process LinkedData resources, i.e., RDF+RDFS+OWL files.
    """


    def parseGraph(self,inputfile,identifier=''):
    
        """
        parseGraph is a wrapper around the rdflib.Graph.Graph class.
        
        :param inputfile: An input file location
        :type inputfile: str
        :param indentifier: An identifier for the resource, can be null.
        :type indentifier: rdflib.URIRef.URIRef
        :rtype: rdflib.Graph.Graph
        """

        #create a graph with declared identifier
        self.graph = Graph(identifier=identifier)
        
        #parse in the contents
        self.graph.parse(inputfile)
        
        """
        this doesn't work. the graph gets reset when the the id is reset???
        #try and retrieve the original identifier
        #which should be dc:identifier
        if not identifier:
            
            for po in self.graph.predicate_objects():
                if po[0] ==  URIRef('http://purl.org/dc/elements/1.1/identifier'):
                    
                    self.graph._Graph__identifier = po[1]
        """
        
        #container for triples
        self.kb =  KBComponent()
        
       

        #list of URIs to imp
        
        #print len(self.graph)

        #merge graphs
        #for g in imports:
        #    parseGraph(g)    
            
        #    merge (self.graph, self.graph.parse(i))


        #return self.kb
        #self.buildPyModel()
        
        #return self.kb
        return self.graph
    

    def buildPyModel(self):
        """
        buildPyModel iterates over all triples in Graph and converts to Python's OOP model.

        :rtype: eltk.kb.KBComponent.KBComponent
        """


        #main loop to add OWL classes and object/data properties to KBComponent as attributes
        #
        #loop over subjects in triples (same as looping over triples) 
        #
        #This could be done using sparql queries, but that's less efficient
        
        self.kb.uri = self.graph.identifier

        for s in self.graph.subjects():
            
            #don't attempt to reassign instance attribute
            #   if it's already there
            #still not 100% sure what the problem is
            #so this is a hack. dc:'identifier' causes the problem
            if not hasattr(self.graph,quote(getLocalName(s))):   
                
                #loop over all predicate_objects 
                for i in self.graph.predicate_objects(s):
                    
                    #if an OWL class is found
                    if i[0]==URIRef(RDFtype.uri) and i[1]==OWLClass.uri:

                        #create the class and add as attribute
                        setattr(self.kb,quote(getLocalName(s)),OWLClass.new(s))
                    
                    #if an OWL ObjectProperty is found
                    elif i[0]==URIRef(RDFtype.uri) and i[1]==OWLObjectProperty.uri:
                        
                        #create ObjectProperties and add as attribute
                        setattr(self.kb,quote(getLocalName(s)),OWLObjectProperty.new(s))

                    #if an OWL DatatypeProperty is found
                    elif i[0]==URIRef(RDFtype.uri) and i[1]==OWLDatatypeProperty.uri:
                        
                        #create DatatypeProperty and add as attribute
                        setattr(self.kb,quote(getLocalName(s)),OWLDatatypeProperty.new(s))
        
        #add individuals to ontology
        #
        #keys: URIRef for the indiv
        #values:  list of types for individuals, that is:
        #   ind_class_pair[k][0] is the URIRef of first class
        #   ind_class_pair[k][1:] are the URIRefs for any other classes
        ind_class_pair=sparql.getIndividuals(self.graph) 
        

        for k in ind_class_pair.keys():    



            #get the local names of first class
            cls_name=getLocalName(ind_class_pair[k][0])
            
            #print cls_name 
            #
            #don't instantiate when cls_name is an OWL metatype
            #used when reading an OWL file
            #
            if cls_name not in ['Class','AnnotationProperty','ObjectProperty','DatatypeProperty','FunctionalProperty','InverseFunctionalProperty','TransitiveProperty','SymmetricProperty','Ontology']:
                
                #print cls_name

                #if an indiv. has only one type
                if len(ind_class_pair[k])==1:

                    #use quote for unicode symbols in local URI name
                    #
                    #instantiate a class 
                    
                    indiv = ''
                    
                    #this conditional added if concept isn't in resource, but is up a
                    #level, ie in GOLD or some other COPE 
                    #
                    #maybe 'import eltk' and use eltk.GOLD here???
                    #
                    if quote(cls_name) in dir(self.kb):
                        
                        indiv=getattr(self.kb,quote(cls_name)).__call__(k,[])
                
                    else:
                        
                        getattr(eltk.GOLD,quote(cls_name)).__call__(k,[])
                        
                    #assign the indiv to the ontology using the local
                    #name of the indiv
                    setattr(self.kb,quote(getLocalName(k)),indiv)
                    

                #if an indiv. has multiple types
                else:
                
                    #the list to hold multiple types
                    other_classes=[]
                    
                    #build list of classes
                    for c in ind_class_pair[k][1:]:
                        
                        #hack1, I don't know what wrong so I added this if
                        if c !=URIRef('http://www.w3.org/2002/07/owl#Class'):
                            other_classes.append(getattr(self.kb,getLocalName(c)))
                    
                    #get the class
                    
                    #hack2: the try statement is another hack related to OWLThing
                    #maybe related to problem above in hack1
                    try: 
                        indiv=getattr(self.kb,cls_name).__call__(k,other_classes)
                    except:
                        pass
                    #assign the indiv with more than one type 
                    #to the ontology using the local
                    #name of the indiv              
                    setattr(self.kb,quote(getLocalName(k)),indiv)

        #######LOOP to add base classes#######
        for attr_name in dir(self.kb):
            
            attr = getattr(self.kb,attr_name)

            if type(attr) is OWLClass:

                #start w. list
                bases = []
                
                
                list_base_urirefs = sparql.getBaseClasses(self.graph,attr.uri)
                
                for base_uriref in list_base_urirefs:
                    
                    bases.append(getattr(self.kb,getLocalName(base_uriref)))

                #print attr.__bases__ 
                #print object 
                
                #if attr.__bases__ != (object,):
                #print tuple(bases,)   
                
                if bases != []:
                    
                    try:
                        attr.__bases__ = tuple(bases,) 
                    except:
                        print 'MRO problem with: ',attr
        
        self.addAttr()
        self.addFunc() 

        return self.kb


    
    #!!!
    #
    #may need to augmenting, e.g., rdfs:label isn't added as an attribute
    #
    def addAttr(self):
        """
        addAttr adds attributes to individuals. If the RDF graph contains:
            myindiv --pred--> obj
        then  add 'obj' as the attribute called 'pred'. Thus:
        
        >>> myindiv.pred
        >>> obj

        addAttr also adds triples to self.kb.
        
        
        :rtype: None
        """
        
        #iterate over all attributes 
        for attribute in self.kb.__dict__.iteritems():
            
            #print self.kb.__dict__

            predicate_objects = {} 
            
            #print attribute

            #only pick attributes that are instances of classes
            # (trick: since by def. all Py's types are type object, not lists)
            # 
            #if type(type(attribute[1])) is list: <--works too    

            if type(type(attribute[1])) in [OWLClass,RDFSResource]:
                
                
                #iterate over (predicate, object) pairs (see rdflib.Graph)
                for po in self.graph.predicate_objects(attribute[1].getURI()):
                    
                    #filter:
                    #   RDF:type <--- maybe more???
            
                    if po[0]!=URIRef(RDFtype.uri):
                        
                        if po[0] in predicate_objects.keys():
                            predicate_objects[po[0]].append(po[1])
                        else:
                            predicate_objects[po[0]] = [po[1]]
                
               
                for pred in predicate_objects.keys():
                    
                    #objects to assign to attribute
                    obj_list=[]

                    for obj in predicate_objects[pred]:
                        
                        if hasattr(self.graph,quote(getLocalName(obj))):
                            
                            #print getLocalName(obj)

                            obj_list.append(getattr(self.graph,quote(getLocalName(obj))))
                            
                        #there is no such class in the current ontology
                        #the object is of a type not in the current domain
                        else:
                            pass
                    
                    #assign the attribute its value
                    setattr(attribute[1],quote(getLocalName(pred)),obj_list)
                     
                    #print attribute[1], pred 

    def addFunc(self):
        """
        addFunc attaches various useful instance methods to each kb attribute:
            - a function that returns all subclasses
            
            - a function that returns all instances
        
        
        :rtype: None
        """
        #iterate over all attributes
        for attribute in self.kb.__dict__.iteritems():
           
            #only process those that are indirectly or directly instances of OWLClass
            if isinstance(attribute[1],OWLClass): 
                
                #issue sparql query
                subclasses_uri = sparql.getSubClasses(self.graph,attribute[1].uri)
                
                subclasses = [] 

                for uri in subclasses_uri:

                    subclasses.append(getattr(self.kb,getLocalName(uri)))
                
                
                #if subclasses == []: subclasses = None                        
                
                #add func in 2 steps
                #1. add the data attribute
                setattr(attribute[1],'_subclasses',subclasses)
                #2. add method itself which calls data attribute
                attribute[1].getSubClasses = instancemethod(getSubClasses,attribute[1])



if __name__=='__main__':

    

    #reader = ReaderFactory().getDataReader('linkeddata')
    
    reader = LinkedDataReader()
     
    #GOLD_graph = reader.parseGraph(ELTK_HOME+'/examples/inputfiles/gold-2009.owl')
    GOLD_graph = reader.parseGraph('/home/farrar/git-repos/e-linguistics/goldcomm/gold/gold-2009.owl')
    
    GOLD = reader.buildPyModel()
    
    print GOLD.Noun.uri
    
    x = getattr(GOLD,'Noun')
    print x
    
    #for attr in dir(GOLD):
    #    entity = getattr(GOLD,attr)
    #    if type(entity) is Meta.OWLObjectProperty:
    #        print getLocalName(entity.uri)

    #termset = reader.parseGraph(ELTK_HOME+'/examples/outputfiles/LeipzigTermset.rdf') 
    #youcope = reader.parseGraph(ELTK_HOME+'/examples/outputfiles/YourCOPE.rdf') 
    #mycope = reader.parseGraph(ELTK_HOME+'/examples/outputfiles/MyCOPE.rdf') 
 
    
    #print GOLD.TenseProperty.getSubClasses()
    #print GOLD.LinguisticProperty.getSubClasses()
  

    #for attr in dir(GOLD):
    #    print type(getattr(GOLD,attr))


    #print len(termset.triples)

    #print dir(GOLD.AcousticProperty)
    #print GOLD.InablativeCase.uri
    #print GOLD.InablativeCase.getURI()
    #print GOLD.hasConstituent.uri
    #print GOLD.TenseProperty.uri
