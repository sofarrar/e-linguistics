# e-Linguistics Toolkit: Reader 
#
# Copyright (C) 2008 ELTK Project
# Author: Scott Farrar <farrar@u.washington.edu>
# URL: <http://purl.org/linguistics/eltk>
# For license information, see LICENSE.TXT
"""
The Reader module contains the base class for all data and linked data readers.
"""


from os.path import abspath


from eltk.config import ELTK_HOME

class Reader(object):
    """
    Reader is the abstract class subsuming all types of file readers. There are several subtypes of readers. Each time a new reader is created, a makeLinkedData method should be created. 
    """
    #def __init__(self,filename):
    def read(self,filename):
        """
        Initialize a reader by passing it a filename.

        :param filename: filename string
        :type: string
        """
        #attempt to read the input file
        try:
            
            #import codecs 
            #self.inputfile = codecs.open(filename, 'r', 'utf-8')                
            self.inputfile=open(filename,'r')
        
        except IOError: # as (errno, strerror):
            print "I/O error: cannot open: ", filename

        

if __name__=='__main__':
    pass
    #termset = None
 
    #myreader = ReaderFactory.getDataReader('leipzig',termset)
    
    #myreader.makeLinkedData(ELTK_HOME+'/examples/inputfiles/MorphosyntaxExamples.


############DEAD CODE#############
#from eltk.reader.TermsetReader import TermsetReader
#from eltk.reader.LinkedDataReader import LinkedDataReader
#from eltk.reader.SignlistReader import SignlistReader
#from eltk.reader.HBBReader import HBBReader
#from eltk.reader.LeipzigReader import LeipzigReader 
#from eltk.reader.PraatReader import *


#from rdflib.URIRef import URIRef
#from rdflib.Namespace import Namespace

#from eltk.kb.Ontology import *
#from eltk.config import ELTK_HOME
#from eltk import GOLD 
#from eltk.namespace import TERMSETNS
#from eltk.kb.LinkedData import LinkedData

"""
The Reader module contains the ReaderFactory and the abstract Reader class. For more info on why the Readers were implemented this way, read about the `Factory Design Pattern <http://en.wikipedia.org/wiki/Factory_method_pattern>`_. The essential thing to note is that a new reader should be created to process each legacy or working data format.

class ReaderFactory(object):
    #ReaderFactory  creates the appropriate reader object.
    @staticmethod
    def getDataReader(file_type,termset=''):
    #def getDataReader(file_type,termset= ELTK_HOME+'/examples/outputfiles/LeipzigTermset.rdf'):
        #The getDataReader method determines the correct reader object. 
        if file_type == 'linkeddata':
            #print file_type,termset
            return LinkedDataReader()

       
        elif file_type == 'termset':
            return TermsetReader(termset)
        
        elif file_type=='signlist':
            return SignlistReader(termset)
        
        elif file_type=='leipzig':
            return LeipzigReader(termset)

        elif file_type == 'lexicon':
            return LexiconReader(termset)
        
        elif file_type == 'TextGrid':
            return PraatReader(termset)

        elif file_type == 'hbbxml':
            return HBBReader()


"""
