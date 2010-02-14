# -*- coding: UTF-8 -*-
#
# e-Linguistics Toolkit: Termset
#
# Copyright (C) 2008 ELTK Project
# Author: Scott Farrar <farrar@u.washington.edu>
# URL: <http://purl.org/linguistics/eltk>
# For license information, see LICENSE.TXT
"""
Termset is the Python data structure equivalent of  ``termset graphs`` which are logical components of the GOLD Community Model. Put simply, they contain term-concept mappings, e.g., "PST"--gold:PastTense. A termset contains a  set of scientific 'terms' used as part of an annotation system, usually the standard terms from a particular linguistic theory or community of practice. A term is a specific string representing a concept within some scientific domain. Terms may have a standard orthographic representation such as "past tense" or an abbreviation such as "PST".
"""

from eltk.kb.KBComponent import KBComponent
from eltk.reader.LinkedDataReader import LinkedDataReader
from eltk.config import ELTK_HOME


reader = LinkedDataReader()
GOLD_graph = reader.parseGraph(ELTK_HOME+'/examples/inputfiles/gold-2008.owl')
GOLD = reader.buildPyModel()



class Termset(KBComponent):
    """
    Termset is the class representing a termset.    
    """
   
    def getTermMeaning(self,term_string):
        """
        Given some abbreviation, e.g., 'PST', or full form, e.g., 'past tense', return the GOLD URI indicated by that string.
        
        :param term_string: the string representation (abbreviation or full form) of the term 
        :type term_string: string
        :returns: the URI of the GOLD concept represented by the string
        :rtype: rdflib.URIRef.URIRef
        """ 
        term = ''

        #loop over the triples (like a sparql query)
        for k in self.triples.keys():
            
            for i in self.triples[k]:
                
                
                if i[1]==term_string:
                    
                    #assign name of search string to 'term'
                    term= k
        
        for k in self.triples.keys():

            if k == term:
                
                for i in self.triples[k]:

                    
                    #if type(i[0]) is type(GOLD.hasMeaning):
                    if i[0].uri ==  GOLD.hasMeaning.uri:
                        return i[1]

        


if __name__=='__main__':

    #for termset reader

    mytermset = Termset()
   
    myterm = GOLD.Term(u'http://myterms.org/myterm123')
    
    mytermset += (myterm, GOLD.abbreviation, 'PST')
    mytermset += (myterm, GOLD.orthographicRep, 'past tense')
    mytermset += (myterm, GOLD.hasMeaning, GOLD.PastTense)
   

    #print mytermset.triples


    print mytermset.getTermMeaning('PST').name

    #mygraph = mytermset.buildRDFGraph(u'http://purl.org/linguistics/foo')
    
    #mygraph.serialize('mytermset.rdf')


