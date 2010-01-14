
from eltk.config import ELTK_HOME
from eltk.kb.Ontology import Ontology 
from eltk.reader.Reader import ReaderFactory

"""
This script shows how to import an ontology into the Python OOP environment
"""

if __name__=='__main__':

    #load a local owl file and populate the ontology
    reader = ReaderFactory().getDataReader(ELTK_HOME+'/examples/inputfiles/gold-2008.owl')
    
    #build an ontology and assign it a  URI
    GOLD = reader.buildPyModel(u'http://purl.org/linguistics/gold')

    #print the class and object/datatype property names as a test
    for c in dir(GOLD):
        print c


    print "\n If you see a bunch of GOLD class and object/datatype property URIs, the ontology loaded successfully."


#import config 
    

