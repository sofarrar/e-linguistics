# -*- coding: UTF-8 -*-
#
# e-Linguistics Toolkit: test_ontology
#
# Copyright (C) 2008 ELTK Project
# Author: Scott Farrar <farrar@u.washington.edu>
# URL: <http://purl.org/linguistics/eltk>
# For license information, see LICENSE.TXT


import unittest

#rdflib2.5
#from rdflib.term import URIRef
from rdflib.URIRef import URIRef

from eltk.kb.Ontology import *
from eltk.config import ELTK_HOME

class TestParseOntologyClass(unittest.TestCase):

    """
    Used to test the loading and parsing of RDF graphs (owl files) as eltk ontologies
    """

    def setUp(self):
        self.gold=Ontology(identifier = URIRef(u'http://purl.org/linguistics/data/myonto/'))
        self.gold.parse(ELTK_HOME+"/examples/inputfiles/test_ontology.owl")


    def testEntityReference(self):
        #test simple reference: name and uri
        self.assertEqual(self.gold.MyClass1.name,'MyClass1')
        self.assertEqual(self.gold.MyClass1.uri,u'http://www.test.org/test_ontology.owl#MyClass1')

    def testEntityReference_nonascii(self):
        #test reference with non-ascii char's
        
        #class
        cu=self.gold.getEntity(u'http://www.test.org/test_ontology.owl#MyClass_unicoɖe')
        self.assertEqual(OWLClass,type(cu))
        self.assertEqual(u'http://www.test.org/test_ontology.owl#MyClass_unico%C9%96e',cu.uri)
        self.assertEqual(u'MyClass_unico%C9%96e',cu.name)

        #instance
        i=self.gold.getEntity(u'http://www.test.org/test_ontology.owl#MYINSTANCEɖ')
        
        #b/c uri isn't quoted in Meta, see note in Meta.py
        self.assertEqual(URIRef(u'http://www.test.org/test_ontology.owl#MYINSTANCEɖ'),i.uri)
        self.assertEqual(u'MYINSTANCEɖ',i.name)




    def testGetEntity_class(self):
        
        #test class as argument
        c=self.gold.getEntity(u'http://www.test.org/test_ontology.owl#MyClass1')
        self.assertEqual(OWLClass,type(c))
        self.assertEqual(u'http://www.test.org/test_ontology.owl#MyClass1',c.uri)
        self.assertEqual(u'MyClass1',c.name)



    def testGetEntity_objectproperty(self):
        
        #test obj property as argument
        op=self.gold.getEntity(u'http://www.test.org/test_ontology.owl#myobjectproperty')
        self.assertEqual(OWLObjectProperty,type(op))
        self.assertEqual(u'http://www.test.org/test_ontology.owl#myobjectproperty',op.uri)
        self.assertEqual(u'myobjectproperty',op.name)

    def testGetEntity_dataproperty(self):
        
        #test data property as argument
        dp=self.gold.getEntity(u'http://www.test.org/test_ontology.owl#mydataproperty')
        self.assertEqual(OWLDatatypeProperty,type(dp))
        self.assertEqual(u'http://www.test.org/test_ontology.owl#mydataproperty',dp.uri)
        self.assertEqual(u'mydataproperty',dp.name)


    def testGetEntity_individual(self):
        #test individidual as argument
        
        #test one type
        c1=self.gold.getEntity(u'http://www.test.org/test_ontology.owl#MyClass1')
        i1=self.gold.getEntity(u'http://www.test.org/test_ontology.owl#MYINSTANCE1')
        self.assertEqual(u'MYINSTANCE1',i1.name)
        self.assertEqual(URIRef(u'http://www.test.org/test_ontology.owl#MYINSTANCE1'),i1.uri)
        self.assertEqual([c1],type(i1)) 
        
        #test two types
        c2=self.gold.getEntity(u'http://www.test.org/test_ontology.owl#MyClass2')
        i2=self.gold.getEntity(u'http://www.test.org/test_ontology.owl#MYINSTANCE2')
        self.assertTrue((c1 and c2) in type(i2)) 

        #test three types
        c3=self.gold.getEntity(u'http://www.test.org/test_ontology.owl#MyClass3')
        i3=self.gold.getEntity(u'http://www.test.org/test_ontology.owl#MYINSTANCE3')
        self.assertTrue((c1 and c2 and c3) in type(i3)) 


class TestCreateOntologyClass(unittest.TestCase):
    
    """
    Used to test the creation of ontologies as objects in the Python OOP environment
    """


    def setUp(self):

        #create onto URI
        self.uri=URIRef(u'http://purl.org/linguistics/test_onto.owl')
        #create onto
        self.myonto=Ontology(self.uri)
        
    def testAddClass(self):
        
       
        #create and add a class
        Lexeme = OWLClass.new(u'http://purl.org/linguistics/gold/Lexeme')
        self.myonto.addEntity(Lexeme)
        
        #ontology has member Lexeme
        self.assertTrue(self.myonto.Lexeme)
        
    def testAddObjectProperty(self):
        
        #create and add an object property
        hasEntry = OWLObjectProperty.new(u'http://purl.org/linguistics/gold/hasEntry')
        self.myonto.addEntity(hasEntry)

        #ontology has member hasEntry
        self.assertTrue(self.myonto.hasEntry) 

    def testAddIndividual(self):

        MyClass = OWLClass.new(u'http://purl.org/linguistics/test_onto/MyClass')
        self.myonto.addEntity(MyClass)

        #print MyClass('MYINDIV',[])
        self.myonto.addEntity(MyClass('MYINDIV',[]))

        #ontology has member MYINDIV
        self.assertTrue(self.myonto.MYINDIV)

    def testAddTriple(self):

         
        MyClass = OWLClass.new(u'http://purl.org/linguistics/test_onto/MyClass')
        myobjprop = OWLObjectProperty.new(u'http://purl.org/linguistics/test_onto/myProp')

        

        #create two individuals
        i1 = MyClass('http://www.test.org/MYINDIV_1',[]) 
        i2 = MyClass('http://www.test.org/MYINDIV_2',[]) 

        self.myonto.add((i1.getURI(),myobjprop.getURI(),i2.getURI()))
        
        answer = []
        
        #iterate over triples
        for x in self.myonto.triples((i1.getURI(),myobjprop.getURI(),i2.getURI())):
            answer.append(x)
        

        #test that triple is really there
        self.assertTrue((i1.getURI(),myobjprop.getURI(),i2.getURI()) in answer)

#suite = unittest.TestLoader().loadTestsFromTestCase(TestOntologyClass)
#unittest.TextTestRunner(verbosity=2).run(suite)


if __name__=='__main__':
    unittest.main()

