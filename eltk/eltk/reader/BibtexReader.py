# e-Linguistics Toolkit:
#
# Copyright (C) 2008 ELTK Project
# Author:       Scott Farrar <farrar@u.washington.edu>
#               Steven Moran <stiv@u.washington.edu>
# URL: <http://e-linguistics.org>
# For license information, see LICENSE.TXT


#!/usr/bin/python
import sys
import codecs


from rdflib.Graph import Graph
from rdflib import Namespace
from rdflib import URIRef



from eltk.utils.CharConverter import *

"""
This module transforms a bibtex file to rdf.
"""

class BibDB:
    
    """
    Class for storing a bibtex database
    """

    def __init__(self):
        
        #the container for the entries extracted from bibfile
        self.entries={}

    def parseBibtex(self,bibfile):

        """ 
        Parse a bibtext file and extract entries

        @type   bibfile: string
        @param  bibfile: the filename to be read
        """
        f=open(bibfile,'r') 
    
        file_lines=f.readlines()
    
        #use the character converter from eltk.utils
        converter=CharConverter('latex','uni')    

        #loop over input file
        for line in file_lines:
         
            #replace latex special character codes w. unicode
            #
            #only works for this latex style: \x{y}
            #
            #this won't work: \{xy}
            #
            line=converter.convert(line)
            
            #if 'author' in line: print line
            
            #get rid of leading and trailing spaces
            line=line.strip()

            #skip over blank lines
            if line=='':
                continue
   

            #begin entry
            if line[0]=='@':
                
                if '@preamble' in line: pass

                #get the name for the entry
                entry_name=line[line.find("{")+1:line.find(",")]
                
                #create a new entry
                self.entries[entry_name]=Entry()
                
                #assign id using original bib files entry name
                self.entries[entry_name].id=entry_name
          
                #find the entry's type
                type=line[1:line.find('{')].lower()

                #normalize the type to camel-case, eg 'InCollection', not 'Incollection'
                type=type.capitalize()
                type=type.replace('Inproceedings','InProceedings')
                type=type.replace('Incollection','InCollection')
                type=type.replace('Inbook','InBook')
                type=type.replace('Phdthesis','PhdThesis')
                type=type.replace('Mastersthesis','MastersThesis')
                type=type.replace('Techreport','TechReport')
    
                self.entries[entry_name].type=type


            
            #if field uses " and also contains internal {}'s
            if line.find('\"')<line.find('{') and line.find('{')!=-1:
                #delete internal braces
                line.replace('{','')
                line.replace('}','')
            
                #normalize in favor of {}'s, not quotes
                #but leave internal quotes
                line=line.replace('\"','{',1)
                if line.count('\"')==1:
                    line=line.replace('\"','}')
                else:
                    line=rreplace(line,'\"','}')
 


            #process fields, line by line

            #non-integer fields
            if 'author' in line:

                #pick out string containing authors
                authors_string=line[line.find('{')+1:line.rfind('}')]
                
                #reformat the string and add to object
                self.entries[entry_name].authors=findAuthors(authors_string)
                
                #set authors_string in Entry
                self.entries[entry_name].authors_string=authors_string

            if 'editor' in line:
            
                #pick out string containing editors
                editors_string=line[line.find('{')+1:line.rfind('}')]
            
                #reformat the string and add to object (use same as authors)
                self.entries[entry_name].editors=findAuthors(editors_string)

                #set editors_string in Entry
                self.entries[entry_name].editors_string=editors_string

            if 'title' in line:
                #don't use title case due to bug in title() function (ie if there's a non-ascii char, then the next char get capitalized regardless of whether it's at the beginning of a word.)
                
                self.entries[entry_name].title=line[line.find('{')+1:line.rfind('}')]
                #.title()

            if 'booktitle' in line:
                #don't use title case as per note above
                self.entries[entry_name].booktitle=line[line.find('{')+1:line.rfind('}')]#.title()



            if 'journal' in line:
                self.entries[entry_name].journal=line[line.find('{')+1:line.rfind('}')]


            if 'pages' in line:
                self.entries[entry_name].pages=line[line.find('{')+1:line.rfind('}')]

            if 'publisher' in line:
                self.entries[entry_name].publisher=line[line.find('{')+1:line.rfind('}')]

            if 'address' in line:
                self.entries[entry_name].address=line[line.find('{')+1:line.rfind('}')]

            if 'location' in line:
                self.entries[entry_name].location=line[line.find('{')+1:line.rfind('}')]



            if 'school' in line:
                self.entries[entry_name].school=line[line.find('{')+1:line.rfind('}')]

            if 'organization' in line:
                self.entries[entry_name].organization=line[line.find('{')+1:line.rfind('}')]

            if 'institution' in line:
                self.entries[entry_name].institution=line[line.find('{')+1:line.rfind('}')]


            if 'series' in line:
                self.entries[entry_name].series=line[line.find('{')+1:line.rfind('}')]


            if 'edition' in line:
                self.entries[entry_name].edition=line[line.find('{')+1:line.rfind('}')]


            if 'howpublished' in line:
                self.entries[entry_name].howpublished=line[line.find('{')+1:line.rfind('}')]

            if 'month' in line:
                self.entries[entry_name].month=line[line.find('{')+1:line.rfind('}')]


            if 'note' in line:
                self.entries[entry_name].note=line[line.find('{')+1:line.rfind('}')]

            #various identifiers
            if 'doi' in line:
                self.entries[entry_name].doi=line[line.find('{')+1:line.rfind('}')]

            if 'isbn' in line:
                self.entries[entry_name].isbn=line[line.find('{')+1:line.rfind('}')]

            if 'issn' in line:
                self.entries[entry_name].issn=line[line.find('{')+1:line.rfind('}')]

            if 'lccn' in line:
                self.entries[entry_name].lccn=line[line.find('{')+1:line.rfind('}')]




            #integer fields
            if 'year' in line:

                self.entries[entry_name].year=findInt(line)

            if 'volume' in line:
                self.entries[entry_name].volume=findInt(line)

            if 'number' in line:
                self.entries[entry_name].number=findInt(line)


            if 'chapter' in line:
                self.entries[entry_name].chapter=findInt(line)

        print 'Found '+str(len(self.entries))+' entries'


        #post processing to fix entries w. editor and no author and
        #to replace id with the convention form makeID()

        #loop through entries
        keys=self.entries.keys()
        for k in keys:
            new_id=''
            
            #make the new ID
            if self.entries[k].authors_string=='':
                new_id=makeID(self.entries[k].editors_string,self.entries[k].year)
            else:
                new_id=makeID(self.entries[k].authors_string,self.entries[k].year)

             
            self.entries[new_id]=self.entries.pop(k)
            self.entries[new_id].id=new_id
           
    def toRDF(self,uri,outfile,person_outfile):
        """
        Create an RDF file; use given URI and local filename

        @type  uri: string
        @param uri: a uri
        @type  outfile: string
        @param outfile: a filename
        """
        
        base=uri
        namespace=uri+'#'

        #outfile=codecs.open(outfile,'w','utf-8')
        outfile=open(outfile,'w')
        outfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')

        outfile.write('<!DOCTYPE rdf:RDF [\n')
        outfile.write('<!ENTITY rdf "http://www.w3.org/1999/02/22-rdf-syntax-ns#" >\n')
        outfile.write('<!ENTITY bibtex "http://purl.org/net/nknouf/ns/bibtex#" >\n')
        outfile.write('<!ENTITY biblio "http://www.linguistics-ontology.org/bibliography/bibliography.owl#" >\n')
        outfile.write('<!ENTITY person "http://www.linguistics-ontology.org/bibliography/person.rdf#">\n')
        outfile.write(']>\n\n')

        outfile.write('<rdf:RDF xmlns="'+namespace+'"\n')    
        outfile.write('\txml:base="'+base+'"\n')
        outfile.write('\txmlns:bibtex="http://purl.org/net/nknouf/ns/bibtex#"\n')
        outfile.write('\txmlns:biblio="http://www.linguistics-ontology.org/bibliography/bibliography.owl#"\n')
        outfile.write('\txmlns:person="http://www.linguistics-ontology.org/bibliography/person.rdf#"\n')
        outfile.write('\txmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n')
        outfile.write('\txmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"')
    
        #close xmlns group
        outfile.write('>\n\n')


        outfile.write('\t<!--This document automatically created by the eltk toolkit-->\n\n')
        for k in self.entries.keys():
            
            outfile.write('\t<!--'+namespace+self.entries[k].id+'-->\n\n')
            
            

            outfile.write(self.entries[k].toRDF(namespace))

        outfile.write('</rdf:RDF>')

        outfile.close()

        #begin writing new person file if necessary
        #
        #call func to update person DB
        person_list=[]
        
        #loop over authors
        for k in self.entries.keys():
            for a in self.entries[k].authors:
                person_list.append(str(a).replace(' ',''))
        
        #loop over editors
        for k in self.entries.keys():
            for e in self.entries[k].editors:
                person_list.append(str(e).replace(' ',''))
        
        updatePersonDB(person_list,person_outfile)


            


class Entry:
    """
    Class for storing bibliographic entries.
    
    Entry is currently bibtex-centric, but could account for other styles such as Endnote.
    """
    def __init__(self):

        #these fields match bibtex
        self.id=''
        self.type=''#eg, Article, InProceedings, etc.
        self.authors=[] 
        self.authors_string='' #this is for makeID
        self.editors=[]
        self.editors_string='' #for makeID if there's no author for entry
        self.title=''
        self.booktitle=''
        self.journal=''
        self.year=''
        self.month=''
        self.pages=''
        self.volume=''
        self.number=''
        self.publisher=''
        self.address=''
        self.location=''
        self.school=''
        self.note=''
        self.series=''
        self.edition=''
        self.howpublished=''
        self.organization=''
        self.chapter=''
        self.institution=''
        self.doi=''
        self.isbn=''
        self.issn=''
        self.lccn=''




    def toRDF(self,namespace):
        """
        Returns a block of RDF based on these files:
            - U{http://www.linguistics-ontology.org/bibliography/gold-bibliography.rdf}
            - U{http://zeitkunst.org/bibtex/0.1/bibtex.owl}
        """
        s=''
        s=s+'\t<bibtex:'+self.type+' rdf:about=\"'+namespace+self.id+'\">\n'

        #get the authors
        if self.authors!=[]:
            s=s+'\t\t<biblio:hasAuthorList>\n\t\t\t<rdf:Seq>\n'
            counter=1
            for a in self.authors:
                
                #remove spaces, etc
                #a=a.replace(' ','')
                #maybe put in camel case??
                #a=a.replace('.','')
                
                print a.localPart()     

                s=s+'\t\t\t\t<rdf:_'+str(counter)+' rdf:resource=\"&person;'+a.localPart()+'\"/>\n'
                counter+=1
            s=s+'\t\t\t</rdf:Seq>\n\t\t</biblio:hasAuthorList>\n'

        #get the editors
        if self.editors!=[]:
            s=s+'\t\t<biblio:hasEditorList>\n\t\t\t<rdf:Seq>\n'
            counter=1
            for a in self.editors:

                #remove spaces, etc
                #a=a.replace(' ','')
                #maybe put in camel case??
                #a=a.replace('.','')
                
                
                s=s+'\t\t\t\t<rdf:_'+str(counter)+' rdf:resource=\"&person;'+a.localPart()+'\"/>\n'
                counter+=1
            s=s+'\t\t\t</rdf:Seq>\n\t\t</biblio:hasEditorList>\n'


        #get the year
        if self.year!='': s=s+'\t\t<bibtex:hasYear>'+self.year+'</bibtex:hasYear>\n'


        #get the month
        if self.month!='': s=s+'\t\t<bibtex:hasMonth>'+self.month+'</bibtex:hasMonth>\n'



        #get the title
        if self.title!='':
            s=s+'\t\t<bibtex:hasTitle>'+self.title+'</bibtex:hasTitle>\n'
        
        #get the booktitle
        if self.booktitle!='':
            s=s+'\t\t<bibtex:hasBookTitle>'+self.booktitle+'</bibtex:hasBookTitle>\n'


        #get the journal name
        if self.journal!='':
            s=s+'\t\t<bibtex:hasJournal>'+self.journal+'</bibtex:hasJournal>\n'

        #get the volume
        if self.volume!='':
            s=s+'\t\t<bibtex:hasVolume>'+self.volume+'</bibtex:hasVolume>\n'

        if self.number!='':
            s=s+'\t\t<bibtex:hasNumber>'+self.number+'</bibtex:hasNumber>\n'
        
        if self.series!='':
            s=s+'\t\t<bibtex:hasSeries>'+self.series+'</bibtex:hasSeries>\n'
 
        if self.edition!='':
            s=s+'\t\t<bibtex:hasEdition>'+self.edition+'</bibtex:hasEdition>\n'
 
        #get the pages
        if self.pages!='':
            s=s+'\t\t<bibtex:hasPages>'+self.pages+'</bibtex:hasPages>\n'

        #get the chapter
        if self.chapter!='':
            s=s+'\t\t<bibtex:hasChapter>'+self.chapter+'</bibtex:hasChapter>\n'



        #get the publisher
        if self.publisher!='':
            s=s+'\t\t<bibtex:hasPublisher>'+self.publisher+'</bibtex:hasPublisher>\n'

        #get the address
        if self.address!='':
            s=s+'\t\t<bibtex:hasAddress>'+self.address+'</bibtex:hasAddress>\n'

        #get the location
        if self.location!='':
            s=s+'\t\t<bibtex:hasLocation>'+self.location+'</bibtex:hasLocation>\n'

        #get the school
        if self.school!='':
            s=s+'\t\t<bibtex:hasSchool>'+self.school+'</bibtex:hasSchool>\n'


        #get the organization
        if self.organization!='':
            s=s+'\t\t<bibtex:hasOrganization>'+self.organization+'</bibtex:hasOrganization>\n'


        #get the institution
        if self.institution!='':
            s=s+'\t\t<bibtex:hasInstitution>'+self.institution+'</bibtex:hasInstitution>\n'

        if self.howpublished!='':
            s=s+'\t\t<bibtex:howPublished>'+self.howpublished+'</bibtex:howPublished>\n'

        if self.note!='':
            s=s+'\t\t<rdfs:comment>'+self.note+'</rdfs:comment>\n'

        if self.doi!='':
            s=s+'\t\t<bibtex:doi>'+self.doi+'</bibtex:doi>\n'
        if self.isbn!='':
            s=s+'\t\t<bibtex:isbn>'+self.isbn+'</bibtex:isbn>\n'
        if self.issn!='':
            s=s+'\t\t<bibtex:issn>'+self.issn+'</bibtex:issn>\n'
        if self.lccn!='':
            s=s+'\t\t<bibtex:lccn>'+self.lccn+'</bibtex:lccn>\n'




        #close entry group
        s=s+'\t</bibtex:'+self.type+'>\n\n'

        return s

    def toString(self):
        """
        mostly for debugging
        """
        
        s='---------\n'+self.type+'\n'
        
        if self.type=='article':
            
            for a in self.authors:
                s=s+a+', '

            s=s+'('+self.year+') '+self.title+' in '+self.journal+' '+self.volume+' ('+self.number+'),'+'pp. '+self.pages
        
        if self.type=='book':
            for a in self.authors:
                s=s+a+', '

            s=s+'('+self.year+') '+self.title+' '+self.publisher+': '+self.address
 
        if self.type=='incollection':
            for a in self.authors:
                s=s+a+', '

            s=s+'('+self.year+') '+self.title+' In '

            for e in self.editors:
                s=s+e+', '

            s=s+'(Eds.)'+self.booktitle+' '+self.publisher+': '+self.address
        
        
        return s

class Author:
    """Class for authors"""

    def __init__(self,f='',m='',l=''):
        self.first=f
        self.middle=m
        self.last=l


    def __str__(self):
        
        if self.middle!='':
            return self.first+' '+self.middle+' '+self.last
        else: return self.first+' '+self.last

    #returns the most info about the author's name, to be used
    #for creating URIs
    def localPart(self):

        a=self.first+self.middle+self.last
        return a.replace(' ','')
       


def findAuthors(auth_string):
    """ 
    Return a list of authors with first and last names
    
    @type  auth_string: string 
    @param auth_string: A string w. typical bibtex style author/editor list
    
    """
    
    authors=[]

    #first look for individual authors
    auth_string=auth_string.split(' and ')

    for author in auth_string:
        first=''
        middle=''
        last=''

        #first normalize inverted names
        if ',' in author:
            first_piece=author[:author.find(',')].strip()
            last_piece=author[author.find(',')+1:].strip()
            author=last_piece+' '+first_piece

        #just delete spaces and punc, e.g. "Scott O. Farrar" --> "ScottOFarrar"
        #else: 
            


        #take first token as first
        first=author[:author.find(' ')].strip()
                    
        last=findLast(author).strip()
        

        #middle is everything between first and last
        first_end=len(first)
        last_start=len(author)-len(last)
        middle=author[first_end:last_start].strip() 
        #print middle
    
        fullname=first+' '
        #to give proper spacing
        if middle!='': fullname=fullname+middle+' '
        fullname=fullname+last

        authors.append(Author(first,middle,last))
    return authors

        
def findLast(author):
    """
    Return the last name of an author

    @type  author: string
    @param author: An author's full name
    """
    
    last=''
    
    #add to this list if other prefixes are needed
    prefixes=[' auf der ',' van der ',' de ',' von ',' van ']
    
    #first assume no prefix
    last=author[author.rfind(' ')+1:].strip()

    #but find prefix if author contains it
    for prefix in prefixes:
        if author.rfind(prefix)!=-1:
            last=author[author.rfind(prefix)+1:].strip()
    
    return last


def makeID(author_string,year):
    """
    Returns an ID for a bib entry based on the following algorithm:    
        1. For works w. more than 3 authors, use last name of first author plus '-etal' plus year
        2. For works w. one, two or three authors, concatenate all last names plus year
        3. Always use last name prefix, eg. 'von' or 'de' as part of last name
        
    @type author_string: string
    @param author_string: A string in typical bibtex form, containing author names
    @type year: int
    @param year: A year
    """
    id=''
    
    #make sure year is a string
    if type(year).__name__!='str': year=str(year)
    
    authors=findAuthors(author_string)
    
    if len(authors)>3:
        return authors[0].last.replace(' ','')+'-etal'+year

    else:
        for a in authors:
            id=id+a.last.replace(' ','')
        return id+year

#########################################
#begin utils
#
##########################################

def rreplace(uni,old,new):
    """
    Replaces the right-most occurrence of 'old' in a unicode object with 'new'
    
    @type   uni: string
    @param  uni: A unicode string
    @type   old: string
    @param  old: The string to be replaced
    @type   new: string
    @param  new: The new string
    """

    

    i=uni.rfind(old)
    v=''
    counter=0
    for c in uni:
        if counter==i:
            v=v+new
        else: v=v+c

        counter+=1
        
    return v


def findInt(line):
    """
    Returns the integer contained in a line such as:
    
    year = {1984},
    
    year = 1984
    
    year = 1984,
    
    year = {1984}
    
    @type  line: string
    @param line: A string containing an integer


    """
    int=0

    #if year is not in delimiters
    if line.find('{')==-1:
        line=line.replace(' ','')
        if line[len(line)-1]==',':
            int=line[line.find('=')+1:line.find(',')]
        else: int=line[line.find('=')+1:len(line)]

                   
    else: int=line[line.find('{')+1:line.rfind('}')]


    return int








def checkBibFile(f):
    """
    Check to see if input bib file is well-formed, looks for:
    -non-ASCII characters
    -field split over lines
    -@string or @preamble 
    """
    bibfile=open(f,'r')
    
    line_number=0

    #variable to test if errors are encountered
    e=''

    #flag for @string
    s=''

    for lines in bibfile.readlines():
        line_number+=1

        lines=lines.lower()
        
        #return a warning if there are split fields
        if '@string' in lines: print 'WARNING: @string found on line %s, ignoring...' % line_number
        if '@preamble' in lines: print 'WARNING: @preamble found on line %s, ignoring...' % line_number
        
        if ((lines.count('{')==1 and lines.count('}')==0) or (lines.count('\"')==1)) and  lines.find(',')==-1 : print 'WARNING: you may have a field spanning more than one line starting on line %s' % line_number       
       
        #return an error if there is a non-ascii character
        #try:
        #    lines.decode()
            
        #except UnicodeDecodeError, e:
        #    print 'Error: Line %s in input file contains non-ascii characters.\n' % line_number

    if e == '':
        return 'good'

    else: return 'bad'





def updatePersonDB(person,new_file='new_person.rdf'):
    """
    Returns an RDF file containing person instances based on a bibtex file.
    Checks master person.rdf file to determine if person is already there.
    Only creates instance of new persons.

    @type   person: list
    @param  person: a list of names without spaces, e.g., ['JohnDoe','W.C.Fields']
    """

    g = Graph()
    
    #change this to URI, not local
    #person_url='http://linguistics-ontology.org/bibliography/person.rdf'
    person_url='file:/home/farrar/svn_projects/GOLDComm/bibliography/person.rdf'
    

    
    #check to see if person.rdf is accessible
    try:
 
        g.parse(person_url)

    except IOError:
        print 'Error: Cannot open url or url unreachable: '
        print '\t'+person_url
        print 'Check internet connection'



    RDF=Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    RDFS=Namespace("http://www.w3.org/2000/01/rdf-schema#")
    BIBLIO = Namespace("http://www.linguistics-ontology.org/bibliography/bibliography.owl#")

    ns = dict(rdf=RDF,rdfs=RDFS,biblio=BIBLIO)

    #list to store person uri's from master person.rdf file
    person_uris=[]

    #query for all person uri's
    for row in g.query('SELECT ?name WHERE { ?name rdf:type biblio:author }', initNs=ns):
        person_uris.append(row[0])
    
    #list to contain URI suffixes, material after '#'
    normalized_names=[]

    for p in person_uris:
        if '#' in p:
            normalized_names.append(p.rsplit('#')[1])

    #write local file with new person URIs
    outfile=open(new_file,'w')
    
    #header stuff
    outfile.write('<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n\
<rdf:RDF xmlns=\"http://www.linguistics-ontology.org/bibliography/person.rdf#\"\n\
    xml:base=\"http://www.linguistics-ontology.org/bibliography/person.rdf\"\n\
    xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\"\n\
    xmlns:bibtex=\"http://zeitkunst.org/bibtex/0.1/bibtex.owl#\"\n\
    xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n\
    xmlns:biblio=\"http://www.linguistics-ontology.org/bibliography/bibliography.owl#"\n\
    xmlns:dc=\"http://purl.org/dc/elements/1.1/\">\n\n')


    
    #check to see if there are duplicates
    #
    #Currently performs a simple match, but should be changed to 
    #be "deep match" based on some heuristic
    #
    #Currently, N.Chomsky is different from NoamChomsky
    for p in person: 
        if p not in normalized_names:
            outfile.write('\t<biblio:author rdf:about=\"#'+p.replace(' ','')+'\">\n')
            outfile.write('\t\t<rdfs:label>'+p+'</rdfs:label>\n')
            outfile.write('\t</biblio:author>\n')
    
    outfile.write('</rdf:RDF>')
    
    outfile.close()



if __name__=='__main__':



    #test updatePersonDB
    #new_persons=['ScottOwenFarrar','SMoran']
    #updatePersonDB(new_persons)


    bibstore=BibDB()

    #bibstore.parseBibtex('LLBookx.bib')
    bibstore.parseBibtex('/home/farrar/svn_projects/GOLDComm/bibliography/gold-bibliography.bib')
    
    
    
    bibstore.toRDF('http://www.linguistics-ontology.org/bibliography/gold-bibliography.rdf','gold-bibliography.rdf','person.rdf')


    #print makeID('Ferdinand de Saussure and Steve P. Moran and Emily Sue Bender and Tom Jones','1988') 

    #print makeID('Scott de Farrar and Steve P. Moran',2001)

    #####for testing findAuthors
    #a=findAuthors('Scott O. Farrar and Chieu Xuan Van')
    #a=findAuthors('Farrar, Scott O. and Van, Chieu Xuan')
    #a=findAuthors('von Neumann, Alex D.')
    #a=findAuthors('Dirk auf der Heider')
    #for i in a:
    #    print i
