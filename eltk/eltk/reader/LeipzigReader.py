#
# e-Linguistics Toolkit: LeipzigReader
#
# Copyright (C) 2008 ELTK Project
# Author: Scott Farrar <farrar@u.washington.edu>
# URL: <http://e-linguistics.org>
# For license information, see LICENSE.TXT
"""
The LeipzigReader module is used to read a text file in Leipzig Glossing Rules format (with some additions). Here's the expected input format:

GOLD concept name
Ethnologue15 language code
citation
comment
IGT line 1
IGT line 2
IGT line 3

See <eltk/examples/inputfiles/MorphosyntaxExamples.txt>
"""

from os.path import abspath

from eltk.reader.Reader import Reader
from eltk.reader.LinkedDataReader import LinkedDataReader
from eltk.reader.TermsetReader import TermsetReader

from eltk.utils.functions import *
from eltk.kb.KBComponent import *

from eltk.config import ELTK_HOME
reader = LinkedDataReader()
GOLD_graph = reader.parseGraph(ELTK_HOME+'/examples/inputfiles/gold-2008.owl')
GOLD = reader.buildPyModel()



class LeipzigReader(Reader):
    
    """
    The reader for Leipzig IGT.
    """
    
    def __init__(self,termset=None):

        self.termset = termset        
        
        self.kb = KBComponent() 

    def makeLinkedData(self,filename,ns='http://purl.org/linguistics/data/'):
        """
        :returns: 
        """

        self.ns = ns

        #read the file
        Reader.read(self,filename)
        
        lines=self.inputfile.readlines()
        

        #quick and dirty storage of ex's
        self.examples={}

        #number of examples
        num=0

        flag=1

        new_id=''
        source=[]
        lang=''
        gloss=[]
        translation=''
        concepts=[]

        

        #total lines per example, 1-7, igt on lines 5-7
        for l in lines:
            l=l.strip()
            if l.startswith('#'): continue

            #reset flag at a blank line
            if l=='':
                flag=1


            else:

                if flag==1:
                    concepts=l.split(',')
                    
                    
                    #for r in range(0,len(concepts)):
                    for r in concepts:
                        #concepts[r]=concepts[r].strip()
                        r = r.strip()

                if flag==2: 
                    lang=l

                #if flag==3: 

                #if flag==4: 

                if flag==5: 
                    #source=parseIGTLine(l)
                    source=parseIGTLine(l)
                    #print source
                if flag==6: 
                    gloss=parseIGTLine(l) 
                
                if flag==7: 
                    translation=l
                    
                    num=num+1


                    #only process well formed IGT 
                    if validate(source,gloss,translation):
                        self.instantiateIGT(self.ns+makeID('igt_example'),lang,source,gloss,translation) 
                        
                #increment
                flag=flag+1


        print '\n', num,' total examples found.\n'
        return self.kb        



    def instantiateIGT(self,new_id,lang,source,gloss,translation):
        """
        Create instances of GOLD entities and add them to new ontology model

        :type new_id: str
        :param new_ID: a random id string
        :type lang: str
        :param land: a 3 letter code
        :type source: list 
        :param source: a list of strings from line 1 of IGT
        :type gloss: list
        :param gloss: a list of glossed from line 2 of IGT          
        :type translation: str
        :param translation: a translation from line 3 of IGT
        """

        
        igt = GOLD.InterlinearGlossedText(new_id)

        sourceline=GOLD.OrthographicPhrase(self.ns+makeID()) #,[gold.Clause])  
        
        self.kb += (igt, GOLD.hasSourceLine, sourceline) 
        
        self.kb += (sourceline,GOLD.orthographicRep,unpack(source).rstrip())

        
        #process words
        for w,gloss_word in zip(source,gloss):
            
            
            form = unpack(w).rstrip()
            synword=GOLD.SyntacticWord(self.ns+makeID(form),[]) 
            
            self.kb += (synword,GOLD.orthographicRep,form)
 
            self.kb += (sourceline,GOLD.hasSyntacticConstituent,synword)

            #now process glosses
            for m,gloss in zip(w,gloss_word):
                 
                form = m
                morpheme=GOLD.MorphologicalUnit(self.ns+makeID(form))
                
                self.kb += (morpheme,GOLD.orthographicRep,form)
                
                self.kb += (synword,GOLD.hasMorphologicalConstituent,morpheme)
               
                gloss = gloss.rstrip('-')

                #usually a feature value, e.g., PST
                gloss_meaning = self.termset.getTermMeaning(gloss)
                
                if gloss_meaning is not None:        
                    #add the property to the morpheme
                    self.kb += (morpheme,GOLD.hasProperty,gloss_meaning)

                        
                else:

                    #for now, assume it's an English gloss and add the translation to the morpheme
                    #won't work in cases where gloss label isn't in termset, e.g.,
                    #  ALLAT, IMM
                    #also when English word is ambiguously in terset, e.g.,
                    #  ON, ALL, 

                    English_word = GOLD.SyntacticWord
                    self.kb += (English_word, GOLD.orthographicRep, gloss)
                    self.kb += (morpheme,GOLD.literalTranslation,English_word)


        #process translation line
        transline=GOLD.OrthographicSentence(self.ns+makeID(),[GOLD.Clause])
        self.kb += (transline,GOLD.orthographicRep,translation)

        #add lang line - translation line triple
        self.kb += (sourceline,GOLD.freeTranslation,transline)

        #self.ontology.addTriple(igt,gold.hasTranslationLine,transline)
        self.kb += (igt,GOLD.hasTranslationLine,transline)


 
if __name__=='__main__':

    termset_reader=TermsetReader()
    termset = termset_reader.makeLinkedData(ELTK_HOME+'/examples/inputfiles/LeipzigTermset.termset')
     
     
    myreader = LeipzigReader(termset)

    mykb = myreader.makeLinkedData(ELTK_HOME+'/examples/inputfiles/MorphosyntaxExamples.txt')
    #this is an example w only 2 IGTs
    #mykb = myreader.makeLinkedData(ELTK_HOME+'/examples/inputfiles/foo')
   

    mykb_graph = mykb.buildRDFGraph('http://purl.org/linguistics/data/LeipzigData.rdf')

    mykb_graph.serialize(ELTK_HOME+'/examples/outputfiles/LeipzigData.rdf')

    







    #some test code 
    #
    #
    #create a new reader
    #myreader=IGTReader()
    #set the namespace for data
    #myreader.setNS('http://purl.org/linguistics/data/igt/')
    #set the URI for the ontology that will contain the data
    #myreader.setOntologyURI('http://purl.org/linguistics/data/igt/gold-2008-examples.owl') 

    #read in a termset
    #myreader.readTermset('file:'+abspath('../examples/outputfiles/LeipzigTermset.owl'))

    #read a data file
    #myreader.readLeipzig(abspath('../examples/inputfiles/MorphosyntaxExamples.txt'))
    
    #myreader.readLeipzig('/home/farrar/svn_projects/GOLDComm/data/igt/MorphosyntaxExamples.txt')


    #for k in myreader.examples.keys():
    #    print k
    #    for e in myreader.examples[k]:
    #        print e
    #    print '\n'

    #write transformed data to file
    #myreader.writeData('file:/home/farrar/Desktop/gold-2008-examples.owl')





    #testing unpack
    #print unpack([['Mereka'], ['di'], ['Ja-', 'karta'], ['sekarang.']])
    #print unpack([['di'], ['Ja-', 'karta']])
    #print unpack(['Ja-','karta'])
    #print unpack([['Ja-','karta'],['da']])



