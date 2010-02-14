# -*- coding: UTF-8 -*-
#from  __builtin__ import type

import unittest

from rdflib.URIRef import URIRef

from eltk.kb.Meta import OWLClass, getType

class TestOWLClass(unittest.TestCase):

    def setUp(self):
        self.Word=OWLClass.new(u'Wordɖ') 
        self.Root=OWLClass.new(u'http://foo.org#Root')
        self.RootWord=OWLClass.new(u'RootWord',(self.Word,self.Root))
        
        self.rw1=self.Word(u'myrootword1',[self.Root])

    def testURI(self):
        
        """
        test reference to name and uri
        """

        #uri is returned as a URIRef
        self.assertEqual(URIRef(u'http://foo.org#Root'),self.Root.getURI())
        
        self.assertEqual(u'Root',self.Root.name)
    
    def testMetaClass(self):
        """
        test basics of metaclass implementation 
        """
        
        #oddly, this works if unit test is run as main
        #
        val1=isinstance(OWLClass,__builtins__.type)
        #
        #but the follow is needed if run using a suite, ie from alltests.py 
        #val1=isinstance(OWLClass,__builtins__['type'])
        #val1=isinstance(OWLClass,type)
        
        self.assertEqual(val1,True)

        val2=issubclass(OWLClass,__builtins__.type)
        #val2=issubclass(OWLClass,__builtins__['type'])
        #val2=issubclass(OWLClass,type)
        
        self.assertEqual(val2,True)
        
        #val3=type(OWLClass)
        #self.assertEqual(val3,type)
        #self.assertEqual(val3,__builtins__['type'])
        #self.assertEqual(val3,__builtins__.type)


    def testDerivedClass(self):
        
        """
        test class w. two types
        """

        self.assertTrue(isinstance(self.Word,OWLClass))
         
        self.assertTrue(issubclass(self.RootWord,self.Root))
         
        self.assertTrue(issubclass(self.RootWord,self.Word))


    def testClassInstance(self):

        """
        test simple type
        """
        self.assertTrue(isinstance(self.rw1,self.Word))
        self.assertTrue(self.Root in getType(self.rw1))
        
        self.assertFalse(isinstance(self.rw1,self.Root))

    def testNonAsciiClassName(self):

        """
        test non-ascii for classes
        """
        val1=self.Word.uri
        self.assertEqual(val1,'Word%C9%96')



#suite = unittest.TestLoader().loadTestsFromTestCase(TestOWLClass)
#unittest.TextTestRunner(verbosity=2).run(suite)


if __name__=='__main__':
    unittest.main()


