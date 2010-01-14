# -*- coding: UTF-8 -*-
#
# e-Linguistics Toolkit: unittest.alltests
#
# Copyright (C) 2008 ELTK Project
# Author: Scott Farrar <farrar@u.washington.edu>
# URL: <http://purl.org/linguistics/eltk>
# For license information, see LICENSE.TXT

import unittest

from eltk.test.test_Ontology import TestParseOntologyClass
from eltk.test.test_Ontology import TestCreateOntologyClass

from eltk.test.test_Meta import TestOWLClass

from eltk.test.test_functions import TestFunctions

suite1a = unittest.TestLoader().loadTestsFromTestCase(TestParseOntologyClass)
suite1b = unittest.TestLoader().loadTestsFromTestCase(TestCreateOntologyClass)

suite2 = unittest.TestLoader().loadTestsFromTestCase(TestOWLClass)

suite3 = unittest.TestLoader().loadTestsFromTestCase(TestFunctions)


runner = unittest.TextTestRunner()

runner.run(suite1a)
runner.run(suite1b)

runner.run(suite2)

runner.run(suite3)
