# e-Linguistics Toolkit: PraatReader
#
# Copyright (C) 2008 ELTK Project
# Author: Scott Farrar <farrar@u.washington.edu>
# URL: <http://e-linguistics.org>
# For license information, see LICENSE.TXT


from xml.dom.minidom import *

from eltk.kb.Ontology import *

from eltk.utils.CharConverter import *
from eltk.utils.functions import *

from eltk.display.Dictionary import *
from eltk.display.igt import *

"""
This module will aid in reading Praat files. This aim is to populate an OWL ontology with instances extracted from the Praat file.

NOTE:
Though this file creates GOLD entities, the full functionality is not yet implemented. 
"""

#create ontology object and declare uri
gold=Ontology('http://purl.org/linguistics/gold')

#load GOLD remotely
#gold=load('http://purl.org/linguistics/gold')

#may be done locally, for speed
gold.load('file:'+abspath('../examples/inputfiles/gold-2008.owl'))



class PraatReader():

    """
    A class for parsing and processing Praat TextGrid files
    
    """

#from Termset
#    def __init__(self,ns=u'http://purl.org/linguistics/data/termset/'):
        
#        """
#        Init the termset and set its namespace 
#
#        @type ns: unicode
#        @param ns: a unicode obj representing a namespace
#        """       
#        self.namespace = Namespace(ns)
#        
#        self.ontology = Ontology()




    def __init__(self,ns=u'http://purl.org/linguistics/data/'):


        #assign user defined namespace, or simply use default
        self.ns=ns 

        #one converter per input file is read
        #(maybe change this to global if multiple files are to be read in a batch?
        self.converter=CharConverter('praat','uni')
        
        #the universe to populate
        #self.universe=LingUniverse()
        #self.universe=linguniv

        #will be used for interactive tier description
        self.user_defined_types=[]
    
        #for hashing time points, for speed
        self.time_points={}   

       
        #init basic data members 
        self.segments=[]
        self.morphemes=[]
        self.translations=[]
        self.notes=[]

    #def setNS(self,ns):
    #    """
    #    Set the namespace for the ontology.

    #    @type ns: str
    #    @param ns: a namespace string
    #    @rtype:
    #    @return:
    #    """

    def setURI(self,uri):
        """
        Ses the URI for the ontology.

        @type uri: str 
        @param uri: a string representing a URI
        """

        self.uri=uri
        self.ontology=Ontology(uri)

 

    def readPraat(self,filename):
        """
        Reads and parses a Praat TextGrid file.
        """

       
        try:
        
            self.input_file=open(filename, 'r')
        
            print('Trying to open '+filename+'...')

            

        except IOError:
            print error
            print('Make sure the path is correct.')
 

        
        print 'Reading Praat file...'

        #test input file for proper type
        try:

	    file_lines=self.input_file.readlines(8)

	    if file_lines[1]!='Object class = "TextGrid"\n':
	        raise IOError()

                        
            print 'This Praat file is good.'
            
           

            #go to beginning of file
            self.input_file.seek(0,0)

            #temp variables
            current_type=''
       

            #get user defined ling types
            for line in self.input_file:
 
                #find the name of the tier
	        if line.find('name = "')!=-1:
		    self.user_defined_types.append(findQuoted(line))


            self.input_file.seek(0,0)

            #BEGIN MAIN  ALGORITHM
            print 'Processing contents...' 
            #process line by line
            for line in self.input_file:
            
                #reset tier type as different types are encountered
                if line.find('IntervalTier')!=-1:
	            current_type='Interval'
    
	        elif line.find('PointTier')!=-1:
	            current_type='Point'
	
	        else: current_type=current_type

	        #find the name of the tier
	        if line.find('name = "')!=-1:
		    dstr_role = findQuoted(line)


	        #for handling individual intervals	
	        if line.find('intervals [')!=-1:
		    try:
                        time_interval=[]
                        data=''
                        time_interval.append(findNum(self.input_file.next()))
			time_interval.append(findNum(self.input_file.next()))
                        data=findQuoted(self.input_file.next())
			
                        #only build an interval if the text has content
			if (data.isspace()!=1 and data!=''):
			
                            self.handleData(data,dstr_role,time_interval)

		    except StopIteration:
		        pass


        except IOError:
            
            print "Input file is not well formed or not of type TextGrid."
	    print file_lines[1]
 

    def getUniverse(self):

        """
        A method for returning the ling. universe
        """

        return self.universe



    def handleData(self,data,dstr_role,time_interval):
        
        """
        Decide on the linguistic unit to instantiate 
        
        data            string repr. of linguistic form or grammar unit label
        dstr_role       how the data is used in the Praat file (gloss, translation, etc)
        time_interval   time alignment

        Instantiates units and add them to ling universe
        """

        start=time_interval[0]
        end=time_interval[1]


        #build data obj's and add to universe
        if dstr_role=='segment':
            data=self.converter.convert(data)
            #
            #deal w. linguniv
            #self.universe.addData(FormUnit('Munken',data,start,end))
            #self.segments.append(FormUnit('Munken',data,start,end))
            
            pass
            #print data, 'is a segment'

        elif dstr_role=='morpheme':
            
            #self.universe.addData(Morpheme('Munken',data,start,end))
                    #elif dstr_role=='Checked tone':
            #self.universe.addData(FormUnit(data)????)

            #self.morphemes.append(Morpheme('Munken',data,start,end))
            print data, ' is a Morpheme'

        elif dstr_role=='translation':
            #self.universe.addData(FormUnit('English',data,start,end))
            #self.translations.append(FormUnit('English',data,start,end))

            print data, ' is a translation'

        #bug here: notes show up as forms of morphemes
        #elif dstr_role=='notes':
        #    self.universe.addData(FormUnit('English',data,start,end))
     



    

    def printIGT(self,out_file):
        """
        build IGT objects based on number of translations
        (since trans are common to the set of morphemes and segments ); 
        assumes intervals are ordered (segment, syllable, morpheme, trans, notes)
        """

        igts=[]

        for t in self.translations:

            temp_morphemes=[]
            temp_segments=[]

	    #loop over morphemes to find those that are assoc'd with a translation 
	    for g in self.morphemes:
            
                if g.start>=t.start and g.end<=t.end:
                
                    temp_morphemes.append(g.label)
               
                
                    #loop over segment transcriptions to find those associated with each morpheme 
                    for p in self.segments:

                        if p.start==g.start and p.end==g.end:
                            #print p.text
                            temp_segments.append(p.getString())
 

            igts.append(IGT(temp_segments,  temp_morphemes, t.segments))
            
        c=IGTCollection(igts)	

        print 'there are', len(self.segments),'segment transcriptions'
        #print 'there are', len(self.syllables),'syllables'
        print 'there are', len(self.morphemes),'morphemes'
        print 'there are ', len(self.translations),' translations'
        print 'there are ', len(self.notes),' notes'

        for t in self.translations:
            print t.segments+' ',


        #c.toStndOut()    
        c.toLatex(out_file) 
     


if __name__=='__main__':

    pr=PraatReader()

    #set the namespace for data
    #pr.setNS('http://purl.org/linguistics/data/igt/')
    
    #set the URI for the ontology that will contain the data
    pr.setURI(URIRef(pr.namespace+u'igt/gold-2008-examples.owl') 


    pr.readPraat(ELTK_HOME+'/examples/inputfiles/praat_test.TextGrid')


