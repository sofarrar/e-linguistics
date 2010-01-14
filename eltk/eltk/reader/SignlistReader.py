# e-Linguistics Toolkit: SignlistReader 
#
# Copyright (C) 2008 ELTK Project
# Author: W.P. McNeill <billmcn@u.washington.edu>, Scott Farrar <farrar@u.washington.edu>
# URL: <http://purl.org/linguistics/eltk>
# For license information, see LICENSE.TXT

from rdflib.Graph import Literal
from rdflib.URIRef import URIRef

import eltk 
from eltk.reader.Reader import *
from eltk.kb.Signlist import Signlist

class SignlistReader(object):
    """Linguistic Signs Data List

    Reader for a comma-separated value file of linguistic signs and associated
    grammatical and semantic features.

    Each record in the input file has the fields:
			
        Form, Properties, Gloss 1, Gloss 2, ... Gloss n, Notes
	
    The number of Gloss fields is variable but there must be at least one.
    The Properties field contains a '.' delimited list of grammatical
    properties.	 Each of these must map to a GOLD URI via the term set passed
    in to the constructor.
    """

    def __init__(self,termset_uri):
        

        #to read the rdf termset file
        reader = ReaderFactory().getDataReader('linkeddata','')
        
        self.termset = reader.read(termset_uri)
        
        print len(self.termset.triples)
    

    def read(self,filename):
        

        try:
                    
            self.inputfile=open(filename,'r')
            print 'opening '+filename 
        except IOError: # as (errno, strerror):
            print "I/O error: cannot open: ", filename


        sign_list = Signlist() 

        #process file line by line
        
        for form, properties, glosses, note in self.enumerate_signlist_lines(self.inputfile.readlines()):
        
            sign = eltk.GOLD.LinguisticSign(form)
            
            print properties
        
        return sign_list
	

	
    def enumerate_signlist_lines(self, data):
        #for n, line, raw_line in self.enumerate_commented_text(data):


        for line in data:
            
            if line.startswith('#'): continue

	    fields = line.split(',')
            

            try:
	        form = unicode(fields.pop(0))
		properties = self.parse_properties(fields.pop(0))
		note =  unicode(fields.pop())
		glosses = [unicode(f) for f in fields]
		yield form, properties, glosses, note
	    except KeyError, e:
	        raise ValueError("Invalid sign list...")#"Invalid sign list line %d:%s" % (n, raw_line))

    def parse_properties(self, properties):
        """Parse a properties string read from the sign list

	    The Properties field contains a '.' delimited list of strings that map
	    to GOLD URIs via this reader's termset.

        :param properties: a string read from the Properties field
        :type properties: string
        """
        
        #return [self.termset.getTermMeaning(p) for p in properties.split(".")]
        
        for p in properties.split("."):
            print self.termset.getTermMeaning(p.strip())
        



if __name__=='__main__':


    #signlist = reader.read(ELTK_HOME+'/examples/inputfiles/signlist.csv')

    #print type(signlist.termset)

    #mygraph = signlist.buildRDFGraph(u'http://purl.org/linguistics/data/signlist.rdf')
    
    #mygraph.serialize(ELTK_HOME+'/examples/outputfiles/signlist.rdf')

   



