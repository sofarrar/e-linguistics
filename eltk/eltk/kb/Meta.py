# -*- coding: UTF-8 -*-
#
# e-Linguistics Toolkit: Meta 
#
# Copyright (C) 2008 ELTK Project
# Author: Scott Farrar <farrar@u.washington.edu>
# URL: <http://purl.org/linguistics/eltk>
# For license information, see LICENSE.TXT
"""
The core of the ELTK is an interface to the combined data models of the Web Ontology Language (OWL), Resource Description Framework Schema (RDFS) and the Resource Description Framework(RDF). That is, using the ELTK, OWL+RDFS+RDF entities are  imported into the Python programming environment such that classes, properties and individuals are created and manipulated alongside Python classes, methods and instances. The goal, then, is to produce Python code that reﬂects the OWL+RDFS+RDF data model. In this way, the developer can simply use the model at hand (loaded via an ontology and various RDF data graphs), not worrying about ways to re-model OWL+RDFS+RDF in Python. This approach  seems quite natural for a Semantic Web effort and  may be characterized as a type of ontology-driven software design (cf. [KoideTakeda2006]_).

In order to import the model into Python's OOP environment, we use **metaprogramming**, or the ability to write code to manipulate code. As inspired by [BabikHluchy2006]_, the OWL class hierarchy can be directly imported into the Python class hierarchy. 

In general OWL+RDFS+RDF is conceptually similar to the object-oriented programming (OOP) paradigm as used in Python. Both OWL+RDFS+RDF and OOP allow for classes and subclasses, inheritance and limited multiple inheritance. RDFS:subClassOf is translated directly to Python class inheritance.  Object composition and class instantiation are also similar. RDF:type is translated to Python class instantiation. But the semantics of OWL+RDFS+RDF is inconsistent with that of Python's in a number of key aspects. For example in most OOP languages, a class instance can only belong to a single class. That is, in Python, the expression 'type(MyInstance)' can only yield a single class. This ensures the behavior of instances based on the associated methods and variables of the instantiated class. In OWL+RDFS+RDF, however, a single individual (corresponding to an instance in OOP) can instantiate multiple classes in the same knowledge base. Thus, to provide a linguistics example, a particular language can be an individual of both ``EndangeredLanguage`` and of ``Koiné`` at the same time. In the ELTK we manage to integrate this facet of OWL semantics in a fairly seamless way.
"""
import __builtin__
from new import instancemethod

#note, fix rdflib imports when rdflib-2.5 is finalized

#rdflib-2.5 
#from rdflib.term import URIRef
from rdflib.URIRef import URIRef
from rdflib import Literal 
from rdflib.Namespace import Namespace

from eltk.utils.functions import getLocalName
from eltk.utils.functions  import quote


#####################
# Upper type structure 
# in RDFS
#####################


class RDFSResource(type):
    """
    RDFSResource is at the top of the metaclass hierarchy, the mother of all types, except for Python's builtin type.
    """
    uri = URIRef(u'http://www.w3.org/2000/01/rdf-schema#Resource')

#Py 3 syntax
#class RDFSClass(object, metaclass=RDFSRecsource): 
#    pass


class RDFSClass(type):
    __metaclass__ = RDFSResource
    
    
    uri = URIRef(u'http://www.w3.org/2000/01/rdf-schema#Class')


#####################################################################
#methods declared here to be added to classes and instances in Meta.py
######################################################################

#get the names of types
def getType(self):
    return self._types
 
#added to force uri to be unicode (must be string in < P3k)
def getURI(self):
    return URIRef(self.uri)

#to return all instances of a class
def getInstances(self):
    return self._instances

#doesn't work with 'print obj', only with 'print obj.__str__()'
#def __str__(self):
#    
#    return self.uri



###################################
# OWLClass
###################################

#trick to get around http://bugs.python.org/issue672115
# can't re-assign __base__ in newstyle classes when base
#was originally 'object', so had to make default base OWLThing
class OWLThing(object):
    uri = 'http://www.w3.org/2002/07/owl#Thing' 

class OWLClass(type):
 
    #used to get OWLClass to be of type 'RDFSClass'
    __metaclass__=RDFSClass  


    def __init__(cls,name,bases,dict):
        
        #call the init method of the superclass
        super(OWLClass, cls).__init__(name, bases, dict)
        
    uri = URIRef(u'http://www.w3.org/2002/07/owl#Class')

    @staticmethod
    def new(uri,bases=(OWLThing,)):
        """
        'new' creates a new class in memory
        """
        
        #has to be string
        uri=quote(URIRef(uri))
        
        name=getLocalName(uri)
        
        #private list of instances
        _instances=[]

        

        cls=OWLClass(name,bases,{'uri':uri,'name':name, '_instances':_instances, 'bases':bases})
    
        #add the appropriate class methods
        cls.getURI = instancemethod(getURI,cls)
        cls.getInstances = instancemethod(getInstances,cls)
       


        return cls    
   

    def __call__(cls, *lstArgs, **dictArgs):
        """
        Creates an instance (OWL individual)
        """
        
        #create the instance of cls in memory
        instance = cls.__new__(cls)
        
        #doesn't seem to be necessary
        #instance.__init__()
        
        #set attributes

        #gives the illusion of instantiating multiple classes 
        #this is a dirty hack, but perhaps all that's possible given
        #Python's semantics
        #print type(instance)
       
        instance._types=[]
        
        if len(lstArgs)==2:
            instance._types=lstArgs[1]
        
        instance._types.append(__builtin__.type(instance))
        
        #store the type name for use in Ontology.py
        if len(lstArgs)==2:
            instance._type_names=[]
            for t in lstArgs[1]:
                instance._type_names.append(t.name)
       
        #quote is not strictly needed here, but it's added to be
        #consistent with the uri of 'cls' in 'new'
        instance.uri=quote(URIRef(lstArgs[0]))
        
        instance.name=getLocalName(instance.uri)

        #instance.uri=instance.uri.replace('#','/')
        

        #instance.getTypeNames=instancemethod(getTypeNames,instance,cls)

        instance.getURI = instancemethod(getURI,instance,cls)

        #print 'created a '+cls.name
        cls._instances.append(instance)

        return instance
    


#################
#  RDFProperty
################


class RDFProperty(type):
    
    __metaclass__ = RDFSResource
    
    uri = URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#type')


    def __init__(cls,name,bases,dict):
    
        #call the init method of the superclass
        super(RDFProperty, cls).__init__(name, bases, dict)
 

    @staticmethod
    def new(uri):
        """
        Constructor to create class in memory
        """
        
        uri=quote(URIRef(uri))

        name=getLocalName(uri)
        
        cls=RDFProperty(name,(),{'uri':uri,'name':name})
    
        #add the appropriate class method
        cls.getURI = instancemethod(getURI,cls)

        return cls    
    
    def __call__(cls, *lstArgs, **dictArgs):
        
        assert len(lstArgs) == 2,\
                "Please provide two arguments: subject and object"


        #return a tuple (handy for adding to RDF graphs)
        return (lstArgs[0],cls,lstArgs[1])


"""
RDFtype is an instance of RDFProperty used throughout, so it is declared here.
"""
RDFtype=RDFProperty.new('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')




class RDFSsubClassOf(type):
    __metaclass__ = RDFProperty


###################################
# OWLObjectProperty
###################################



class OWLObjectProperty(type):
    
    #the metaclass is actually RDFSsubClassOf, since this is true in OWL+RDFS+RDF
    #    inst(OWLObjectProperty,RDFSsubClassOf)
    #but, since RDFProperty is callable, I have to cheat here

    __metaclass__ = RDFSResource

    uri = URIRef(u'http://www.w3.org/2002/07/owl#ObjectProperty')

    def __init__(cls,name,bases,dict):

        
        super(OWLObjectProperty, cls).__init__(name, bases, dict)
    

    @staticmethod
    def new(uri):
        """
        constructor
        """
        uri=quote(URIRef(uri))
        name=getLocalName(uri)
        
        cls=OWLObjectProperty(name,(),{'uri':uri,'name':name})
        
        #add the appropriate class method
        cls.getURI = instancemethod(getURI,cls)

        return cls


    def __call__(cls, *lstArgs, **dictArgs):
        """
        Creates an instance of an OWLObjectProperty
        """
        assert len(lstArgs) == 2,\
                "Please provide two arguments: subject and object"

        

        #return None
        #return a tuple (handy for adding to RDF graphs)
        return (lstArgs[0],cls,lstArgs[1])



###################################
# OWLDatatypeProperty
###################################



class OWLDatatypeProperty(type):

    #the metaclass is actually RDFSsubClassOf, since this is true in OWL+RDFS+RDF
    #    inst(OWLDatatypeProperty,RDFSsubClassOf)
    #but, since RDFProperty is callable, I have to cheat here

    __metaclass__ = RDFSResource

    uri = URIRef(u'http://www.w3.org/2002/07/owl#DatatypeProperty')

    def __init__(cls,name,bases,dict):

        
        super(OWLDatatypeProperty, cls).__init__(name, bases, dict)
    

    @staticmethod
    def new(uri):
        """
        constructor
        """
        uri=quote(URIRef(uri))
        name=getLocalName(uri)
        
        cls=OWLDatatypeProperty(name,(),{'uri':uri,'name':name})
        
        #add the appropriate class method
        cls.getURI = instancemethod(getURI,cls)

        return cls


    def __call__(cls, *lstArgs, **dictArgs):
        """
        Creates an instance of an OWLDatatypeProperty 
        """
        assert len(lstArgs) == 2,\
                "Please provide two arguments: subject and object"

        try:
            if  not (type(lstArgs[1]) is unicode):
                raise TypeError
        except TypeError: 
            print "TypeError: Arg 2 \'"+ str(lstArgs[1])+"\' must be <type unicode>, not "+ str(type(lstArgs[1]))

        #return a tuple (handy for adding to RDF graphs)
        return (lstArgs[0],cls,Literal(lstArgs[1]))





def getType(obj):
    """
    Like Python's built-in type function, getType returns the type for a metaclass instance. However, unlike built-in type, this function returns a list of types and is, thus, used to simulate the multiple typing found with OWL.
    """
    return obj._types


if __name__=='__main__':



    print RDFSResource.__name__+' is of type '+ str(type(RDFSResource))
    print RDFSClass.__name__+' is of type '+ str(type(RDFSClass))
    print OWLClass.__name__+' is of type '+ str(type(OWLClass))
    

    Word = OWLClass.new('http://foo.org/Word')
    print Word.__name__+' is of type '+ str(type(Word))

    print type(Word),'*******'
    print Word.__bases__

    print type(Word)

    w1 = Word(u'http://foo.org/word123')
    #w2 = Word(u'http://foo.org/word123')


    print w1.uri +' is of type '+ str(type(w1))

    #print Word.getInstances()

    #for w in Word.getInstances():
    #    print w.uri
    
    #print type(RDFtype)
    #print RDFtype(w1,w2)
   

    #print type(OWLObjectProperty)
    #print OWLObjectProperty.uri

    #doesn't work ????
    #print OWLObjectProperty.getURI()

    #hasMeaning = OWLObjectProperty.new('http://gold.org/hasMeaning')
    #print type(hasMeaning) 
    #print hasMeaning.uri
    #print hasMeaning.getURI()

    #print hasMeaning(w1,w2)

    #orthographicRep = OWLDatatypeProperty.new(u'http://gold.org/orthographicRep')
    #print type(orthographicRep) 
    #print orthographicRep.uri
    #print orthographicRep.getURI()

    #print orthographicRep(w1,w2)
    
    #orthographicRep(w1,u'scott')
    
    Root = OWLClass.new(u'Root')

    RootWord = OWLClass.new(u'RootWord',(Word,Root))

    print Word.__bases__

    #Word.__bases__ = (Root,)
    
    """
    print type(RootWord)
    print RootWord.__bases__,'**********'
    print getType(w1)
    print type(RootWord)
   
    rw1 = RootWord(u'blah')

    print getType(rw1)

    print isinstance(rw1,Root)

    print issubclass(RootWord, Word)
    print issubclass(RootWord, Root)


    x = Word(u'http://foo.org/myconcept',[Root])
    print getType(x)



    print Root in getType(x)
    """


    ##########################################################
    #
    #   this code demonstrates instantiation and subtyping
    #
    #########################################################


    #print type(OWLClass)
    #returns True
    #print isinstance(OWLClass,__builtins__.type)
    #print issubclass(OWLClass,__builtins__.type)

    #print type(RDFSResource)
    #returns True
    #print isinstance(RDFSResource,object) 


   

    #hasName(w,w)

    #returns True
    #print isinstance(w,Word)
    #returns False
    #print isinstance(w,Root) 


    #RootWord=OWLClass.new(u'RootWord',(Word,Root))
    #print getType(RootWord) 
    #returns True
    #print issubclass(RootWord,Root) 
    #print issubclass(RootWord,Word) 
    
    ############################################################


    ############################################################
    #
    #   unicode (non-ASCII) tests
    #
    ###########################################################

    #using non-ascii as a var name  is illegal in Py2.5 and Py2.6
    #so this won't work:
    #    ɖoo=OWLClass.new(namespace+'ɖoo')
    #can convert to ɖoo to its hex in both cases 

    #but this will
    #create an instance
    #print '______________'
    #print 'non-ascii test:'
    #w1=Word(u'ɖoo',[])
    #print w1.name, ' is the name'
    #print w1.getURI(), ' is the uri'




   

