#!/usr/bin/python

import sys
from eltk.reader.BibtexReader import *

from eltk.config import ELTK_HOME

"""
This script converts a bibtex file to RDF


The following files are created:

    ELTK_HOME+'/examples/outputfiles/gold-bibliography.rdf  
    ELTK_HOME+'/examples/outputfiles/new_person.rdf
"""
if __name__=="__main__":

    
    bibfile=ELTK_HOME+'/examples/inputfiles/gold-bibliography.bib'   
    uri='http://purl.org/linguistics/bibliography/gold-bibliography.rdf'
    outfile=ELTK_HOME+'/examples/outputfiles/gold-bibliography.rdf'
    person_outfile=ELTK_HOME+'/examples/outputfiles/new_person.rdf'

    #do an error check on the bib file
    if checkBibFile(bibfile)=='bad':
        
        print 'Please fix these errors and re-run.'
        sys.exit

    else:

        #create bib store in memory
        bibstore=BibDB()
    
        #parse the bib file
        print 'Parsing bib file...\n'
        bibstore.parseBibtex(bibfile)
        
        #write RDF to local file
        print 'Writing rdf to local file...\n'
        bibstore.toRDF(uri,outfile,person_outfile)
