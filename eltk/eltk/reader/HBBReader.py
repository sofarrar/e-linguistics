# e-Linguistics Toolkit: HBBReader 
#
# Copyright (C) 2008 ELTK Project
# Author: Scott Farrar <farrar@u.washington.edu>
# URL: <http://purl.org/linguistics/eltk>
# For license information, see LICENSE.TXT

"""
HBBReader  migrates an XML file structured according to the HBB format into RDF. 
"""
from os.path import abspath

from xml.dom.minidom import parse, parseString
from xml.sax import saxutils,make_parser,ContentHandler
from xml.sax.handler import feature_namespaces
from xml.sax.saxutils import escape

from eltk.reader.Reader import *

class HBBReader(Reader):
    """
    HBBReader is the main reader class.
    """
        

    def makeLinkedData(self,filename):
        
        #read the file
        Reader.read(self,filename)
        
        #create a parser using sax api
        sax_parser = make_parser()
        
        #not yet incorporated
        #findlang = FindLanguage()
        #sax_parser.setContentHandler(findlang)
        
        #handler for returning 3 lines of IGT
        sax_parser.setContentHandler(FindIGT())

        #now parse the input file
        sax_parser.parse(self.inputfile)

class FindLanguage(ContentHandler):
        
    def startElement(self,name,attr):
        if name != 'language': return

        code = attr.get('code', None)

        print 'found '+code

class FindIGT(ContentHandler):
    def __init__(self): 
        
        #several flags for checking the env
        self.inPhraseContent = 0
        self.inTextContent = 0
        self.inGlossContent = 0
        self.inGlsContent = 0
        self.inGramContent = 0
        
        #init lines to None
        self.ln1 = ""
        self.ln2 = ""
        self.ln3 = ""

    def startElement(self,name,attrs):
        """
        The startElement is basically several flag  sets and resets.
        """
        if name == 'phrase': self.inPhraseContent = 1 
        
        elif name == 'item' and attrs.get('type','')=='text': 
            self.inTextContent = 1 
            self.inGlossContent = 0
            self.inGlsContent = 0


        elif name == 'item' and attrs.get('type','')=='gloss': 
            self.inGlossContent = 1 
            self.inTextContent = 0 
            self.inGlsContent = 0

        elif name == 'item' and attrs.get('type','')=='gls':
            self.inGlsContent = 1
            self.inGlossContent = 0 
            self.inTextContent = 0


        elif name == 'item' and attrs.get('type','')=='gram':
            self.inGramContent = 1
            self.inGlsContent = 0
            self.inGlossContent = 0 
            self.inTextContent = 0



    def characters(self,ch):
        
        """
        Actual work is done here.
        """

        if self.inTextContent:
            self.ln1=self.ln1+' '+ch
        
        elif self.inGlossContent:
            self.ln2=self.ln2+' '+ch

        elif self.inGlsContent:
            self.ln3 = ch

        elif self.inGramContent:
            self.ln2 = self.ln2+'.'+ch

    def endElement(self,name):
       
        if name == 'item':

            self.inTextContent = 0
            self.inGlossContent = 0
            self.inGlsContent = 0
            self.inGramContent = 0

        if name == 'phrase':  
            
            if self.ln1 and self.ln2 and self.ln3:
                print self.ln1
                print self.ln2
                print self.ln3
                print '---------'
            
            self.ln1 = '' 
            self.ln2 = ''
            self.ln3 = ''

            self.inPhraseContent = 0
        
        

if __name__ == '__main__':

    myreader = ReaderFactory.getDataReader('hbbxml')
   
    myreader.makeLinkedData(ELTK_HOME+'/examples/inputfiles/odin_dump_new.xml')
