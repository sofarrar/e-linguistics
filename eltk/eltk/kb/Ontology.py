# -*- coding: UTF-8 -*-
#
# e-Linguistics Toolkit: Ontology
#
# Copyright (C) 2008 ELTK Project
# Author: Scott Farrar <farrar@u.washington.edu>
# URL: <http://purl.org/linguistics/eltk>
# For license information, see LICENSE.TXT
"""
The Ontology module provides a way to create a conceptualization of (some part of) the linguistics domain.  The module is used together with the Meta module (containing metaclasses) to bring an ontological conceptualization into the Python OOP framework. The implementation consists of a 3-layered model: the OWL data model, the RDF  graph model, and Python's OOP model. Entities from  an ontology are key when instantiating linked data, as each datum is typed according to the ontology being used.  Using Description Logic terminology, if a LinkedData object is the ABox, then an Ontology object is the TBox.
"""
from rdflib.URIRef import URIRef

from eltk.config import ELTK_HOME
from eltk.kb.KBComponent import KBComponent

class Ontology(KBComponent):
    """
    Not implemented yet, not sure whether this is needed. For now, use KBComponent
    """
    pass
        

#specific methods to be added for ontologies, e.g., getClases, etc.


if __name__=='__main__':


    #for testing: deserialize a graph into a KB object, serialize it back out again
    from eltk.reader.LinkedDataReader import LinkedDataReader
    from eltk.config import ELTK_HOME
    
    ##########
    #read graph
    reader = LinkedDataReader()
    GOLD_graph = reader.parseGraph(ELTK_HOME+'/examples/inputfiles/gold-2008.owl')
    
    ############
    #de-serialize
    GOLD = reader.buildPyModel()



