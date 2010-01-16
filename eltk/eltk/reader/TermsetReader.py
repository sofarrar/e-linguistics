from rdflib.URIRef import URIRef
from rdflib import Literal
from rdflib.Namespace import Namespace

#from rdflib import RDF 

#import eltk

from eltk.kb.Ontology import *
from eltk.config import ELTK_HOME

#from eltk import GOLD 
#from eltk import RDF

from eltk.namespace import TERMSETNS
from eltk.namespace import GOLDNS 

#from eltk.kb.LinkedData import LinkedData
#from eltk.kb.LinkedData import Termset

from eltk.kb.Termset import Termset

from eltk.reader.Reader import *
from eltk.reader.LinkedDataReader import LinkedDataReader 


from eltk.kb.Meta import RDFtype 

from eltk.config import ELTK_HOME
reader = LinkedDataReader()
GOLD_graph = reader.parseGraph(ELTK_HOME+'/examples/inputfiles/gold-2008.owl')
GOLD = reader.buildPyModel()



class TermsetReader(Reader):
    """
    TermsetReader is a type of Reader that processes termsets and returns Python objects.
    """
    

    #def makeTermset(self,uri):
    def makeLinkedData(self,filename,ns='http://purl.org/linguistics/data/'):
        
        """
        Create a Termset object

        :param uri: a uri
        :type uri: rdflib.URIRef.URIRef
        :rtype: eltk.kb.LinkedData.Termset
        """
        self.ns = ns

        #read the file
        Reader.read(self,filename)
        
        #the data container
        self.termset = Termset()
        
        #termset object
        mytermset = GOLD.Termset(URIRef(u'http://purl.org/linguistics/data/termset/mytermset'))
        
        

        #process file line by line
        lines=self.inputfile.readlines()

        for line in lines:
            
            if line.startswith('#'): continue
            
            data=line.split(',')
            
            #fix spaces between term name 
            name=data[1].strip().replace(' ','_')
    
            #if no orthographic representation is given, use abbreviation
            if name=='':
                name=data[0].strip()
            
            #create a gold:Term
            term_uri = URIRef(u'http://purl.org/linguistics/data/term/'+name)
            
            #create a term
            term=GOLD.Term(URIRef(term_uri),[])

            #add term to data store

            self.termset += (term,RDFtype,GOLD.Term)


            #add term to termset

            self.termset += (mytermset,GOLD.hasTerm,term)

            #link term to its abbreviation
            if data[0]:
                
                self.termset += (term,GOLD.abbreviation,data[0].strip())

            #link term to its representation
            if data[1].strip():
        
                self.termset += (term,GOLD.orthographicRep,data[1].strip())

            #attempt to reference OGLD entity referred to by term 
            try:     
                #retrieve GOLD entity referred to by term
                entity=getattr(GOLD,data[2].strip())
        

                #link term to the appropriate GOLD entity 
                self.termset += (term, GOLD.hasMeaning, entity)


            #link term to its comment
            #need to alter Ontology.py for this

            except AttributeError:
                print 'Skipping \"'+name+'\", not in current version of GOLD.'

        return self.termset 

#for local testing
if __name__ == '__main__':

    
    myreader=TermsetReader()

    termset = myreader.makeLinkedData(ELTK_HOME+'/examples/inputfiles/LeipzigTermset.termset')
    

    print termset.getTermMeaning('copula').name
    print termset.getTermMeaning('PST').name
    
    termset_graph = termset.buildRDFGraph(u'http://purl.org/linguistics/termset/LeipzigTermset.rdf')
    
    termset_graph.serialize(ELTK_HOME+'/examples/outputfiles/LeipzigTermset.rdf')



