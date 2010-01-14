# e-Linguistics Toolkit: ElanReader
#
# Copyright (C) 2008 ELTK Project
# Author: Scott Farrar <farrar@u.washington.edu>
# URL: <http://e-linguistics.org>
# For license information, see LICENSE.TXT

from decimal import *
from xml.dom.minidom import *

from eltk.utils.functions import *

from eltk.utils.CharConverter import *

#note yet needed
#from eltk.display.Dictionary import *
#from eltk.display.IGT import *

from eltk.kb.Ontology import *

"""
This module will aid in reading ELAN files. This aim is to populate an OWL ontology with instances extracted from the ELAN file. 

NOTE:
Though this file creates GOLD entities, the full functionality is not yet implemented. 
"""

#create ontology object and declare uri
gold=Ontology('http://purl.org/linguistics/gold')

#load GOLD remotely
#gold=load('http://purl.org/linguistics/gold')

#may be done locally, for speed
gold.load('file:'+abspath('../examples/inputfiles/gold-2008.owl'))



class ElanReader(object):

    """
    A class for reading Elan eaf files

    """
    

    def __init__(self):
        
        #one converter per input file is read
        #(maybe change this to global if multiple files are to be read in a batch?
        #assume file is in XSAMPA, for now
        self.converter=CharConverter('xsampa','uni')
        
        #the universe to populate
        #self.universe=LingUniverse()

        #will be used for interactive tier description
        self.user_defined_types=[]
    
        #for hashing time points
        self.time_points={}   

    def setNS(self,ns):
        """
        Set the namespace for the ontology.

        @type ns: str
        @param ns: a namespace string
        @rtype:
        @return:
        """
        self.ns=ns 

    def setOntologyURI(self,uri):
        """
        Ses the URI for the ontology.

        @type uri: str 
        @param uri: a string representing a URI
        """

        self.ontology=Ontology(uri)


    def readElan(self, f):

        """Reads and parses an Elan file and populates the ling universe
        
        @type  f:string
        @param f:an eaf file name
        """
        
        print 'Reading Elan file...'

        self.file_in=open(f, 'r')


        #return IOError if root of eaf is not ANNOTATION_DOCUMENT
        try:
            
            file_lines=self.file_in.readlines(2)
        
            if file_lines[1][1:20]!='ANNOTATION_DOCUMENT':
                raise IOError
            print 'This Elan file is good.'        
            
        except IOError:
            print "Input file is not well formed or not of type 'eaf'."
        
        #go to beginning of file
        self.file_in.seek(0,0)

        #begin xml processing
        self.dom=parse(self.file_in)
        
       

        #store time points in a dict. for later use
        for t in self.dom.getElementsByTagName('TIME_SLOT'):
            self.time_points[t.getAttribute('TIME_SLOT_ID')]=t.getAttribute('TIME_VALUE')

        #store alignable elements in a dict. for later use
        self.alignable_elems=self.dom.getElementsByTagName('ALIGNABLE_ANNOTATION')


        #BEGIN MAIN ALGORITHM:
        
        print 'Processing contents...'
        
        #process tier by tier, based on whether they contain alignable or reference annotations
        tier_elems=self.dom.getElementsByTagName('TIER')

        #get user defined ling types
        for tier in tier_elems:
            self.user_defined_types.append(tier.getAttribute('LINGUISTIC_TYPE_REF'))
 
        #print self.user_defined_types

        for tier in tier_elems:
            
            #dstr_role='data structure role'
            #used to decide on what type of linguistic unit to instantiate
            dstr_role=tier.getAttribute('LINGUISTIC_TYPE_REF')
            
            

            alignable_elems=tier.getElementsByTagName('ALIGNABLE_ANNOTATION')
            if len(alignable_elems)>0:
                self.handleAnnotation(alignable_elems,dstr_role)

            ref_elems=tier.getElementsByTagName('REF_ANNOTATION')
            if len(ref_elems)>0:
                self.handleAnnotation(ref_elems,dstr_role)

    #BEGIN OTHER CLASS METHODS

    def handleAnnotation(self,elems,dstr_role):

        """
        Process ALIGNABLE_ANNOTATION and REF_ANNOTATION  elements
        
        @type  elems: 
        @param elems: the elements to start from

        @type  dstr_role:
        @param dstr_role: the element type
        """
        
        #print 'There are ',len(elems),' annotation elements.'
        for e in elems:
            annot_val_elems=e.getElementsByTagName('ANNOTATION_VALUE')
            if annot_val_elems>0:
                self.handleAnnotationValue(annot_val_elems,dstr_role,self.findTimeInterval(e))


    def handleAnnotationValue(self,annot_val_elems, dstr_role, time_interval):
        
        """ Process CDATA associated with ANNOTATION_VALUE elements.
        
        annot_val_elems         the elements to be processed
        dstr_role               element type to be passed on
        time_interval           time interval list to be passed on

        Calls handleData(...)
        """
        
        for v in annot_val_elems:
            for c in v.childNodes:
                if c.nodeType==3:
                    self.handleData(c.data,dstr_role,time_interval)

    def findTimeInterval(self,elem):

        """Build time interval list

        elem    the element to start from
        
        Return a list containing the start and end times 
        """
       
        if elem.tagName=='ALIGNABLE_ANNOTATION':

            start=elem.getAttribute('TIME_SLOT_REF1')
            end=elem.getAttribute('TIME_SLOT_REF2')
            
            #look up time refs in hash
            return [self.time_points[start],self.time_points[end]] 

       
        elif elem.tagName=='REF_ANNOTATION':
            
            ref=elem.getAttribute('ANNOTATION_REF')

            
            for e in self.alignable_elems:
                
                if e.getAttribute('ANNOTATION_ID')==ref:
                
                    #recursive call
                    return self.findTimeInterval(e)

        


    def handleData(self,data,dstr_role,time_interval):
       
        
        """Decide on which linguistic units to instantiate.
        
        data            string repr. of linguistic form or grammar unit label
        dstr_role       how the data is used in the Elan file (gloss, translation, etc)
        time_interval   time alignment
        
        Instantiates units and adds to ling. universe
        """
        
        start=float(time_interval[0])
        end=float(time_interval[1])


        #build data obj's and add to universe
        if dstr_role=='Sentence-level Transcription':
            
            #convert unicode to string (nec. for character converter)
            if type(data)==unicode: data=str(data)

            data=self.converter.convert(data)

            print data, ' is a Clause or Phrase'
            

            #generalize this later
            data=data.split()
            for d in data:
                print d, ' is a SyntacticWord'
                w=gold.SyntacticWord(self.ns+makeID(d),[])
                #self.universe.addData(FormUnit('Koshin',d,start,end))
                start=start+.00001

            #self.universe.addData(FormUnit(data,start,end))

        elif dstr_role=='Morpheme':
            
            #generalize this later
            ###############################################
            print data,'###data'
            data=data.split()
            for d in data:
                
                print d,'####d'
                #self.universe.addData(Morpheme('Koshin',d,start,end))
                start=start+.00001
            ################################################

            #self.universe.addData(Morpheme(data,start,end))
        
        #elif dstr_role=='Checked tone':
        #    self.universe.addData(FormUnit(data,start,end))
        elif dstr_role=='Sentence-level Translation':
            #print 'trans'
            pass
            #self.universe.addData(FormUnit('English',data,start,end))
        #elif dstr_role=='Notes':
        #    self.universe.addData(FormUnit(data,start,end)

    def writeData(self,outfile):
      self.ontology.save(outfile) 
 


if __name__=='__main__':

    #create an Elan reader
    er=ElanReader()

    #set the namespace for data
    er.setNS('http://purl.org/linguistics/data/igt/')
    #set the URI for the ontology that will contain the data
    er.setOntologyURI('http://purl.org/linguistics/data/igt/gold-2008-examples.owl') 



    #open an Elan file
    er.readElan('../examples/inputfiles/elan_test.eaf')

    #write transformed data to file
    er.writeData('file:/home/farrar/Desktop/gold-2008-examples.owl')



