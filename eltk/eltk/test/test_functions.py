# -*- coding: UTF-8 -*-
#
# e-Linguistics Toolkit: test_functions
#
# Copyright (C) 2008 ELTK Project
# Author: Scott Farrar <farrar@u.washington.edu>
# URL: <http://e-linguistics.org>
# For license information, see LICENSE.TXT


import unittest

from eltk.utils.functions import *

class TestFunctions(unittest.TestCase):

    def setUp(self):
        pass
        #self.gold=Ontology("../examples/inputfiles/test_ontology.owl")


    def test_formatEscapes(self):
        "test format escapes"
        val=formatEscapes('abc\\tdef')
        self.assertEqual(val,'abc\\\\tdef')      

    """
    #test Py escape and tipa
    print formatEscapes('abc\\tdef')
    print tipaClean('\\textupstep{}a')
    
    
    print findQuoted('abc"def"ghi')
    print findNum('abc1.23def')

    #test quote w. only ASCII
    print quote(u'http://www.test.org/test#test')
    #test quote w. non-ASCII
    print quote(u'http://www.test.hamišaluǧ.org')

    #tests for URI handling
    print getLocalName(u'http://foo.org#mylocal')
    print getLocalName(u'http://foo.org/mylocal')
   
    print getNamespace(u'http://foo.org#mylocal')
    print getNamespace(u'http://foo.org/mylocal')

    print getLocalName(u'http://foo.org#mylocalš')
    print quote(u'http://foo.org#mylocalš')

    #tests for unpack
    print unpack([['abc'],['c'],['d-','e']])
    print unpack([['abc'],['c'],['d-','e']],'-')
    """
#suite = unittest.TestLoader().loadTestsFromTestCase(TestFunctions)
#unittest.TextTestRunner(verbosity=2).run(suite)


if __name__=='__main__':
    unittest.main()

