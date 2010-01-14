# e-Linguistics Toolkit: GraphManager
#
# Copyright (C) 2008 ELTK Project
# Author: Steven Moran <stiv@u.washington.edu>                                  # URL: <http://e-linguistics.org>
# For license information, see LICENSE.TXT 
"""
This module is used to interact with a set of merged RDF/OWL graphs.
"""

from rdflib.Namespace import Namespace
from rdflib.Graph import Graph
from rdflib.URIRef import URIRef
from rdflib.Literal import Literal 
# allows for prettier printing of rdflib.Literals
from rdflib.URIRef import URIRef
from rdflib.BNode import BNode

class GraphManager:
    """
    GraphManager takes a list of RDF and OWL files, merges them, and provides convenience methods for extracting data from the (combined) graph. Note: It contains GOLD specific funtion calls. Also, when the documentation refers to 'object' this should be interpreted by the user as the object node within the graph (subject predicate object) entity relations and not 'object' in the sense of OOP. Also, the term 'subject' should be considered the 'subject' node.
    """
    # todo: implement multiple constructors
    #    def __init__(self, graphs):
    def __init__(self, graphs):
        """
        Constructor takes a list of URLs that point to RDF/OWL files.
        :type graphs: list
        :param graphs: a list RDF/OWL files 
        """
        self.g = Graph()

        if type(graphs) == str:
            self.g.parse(graphs)
        else:
            for i in range(0, len(graphs)):
                self.g.parse(graphs[i])

        # for testing - todo: load all namespaces from a merged graph in the code below
        self.owl = Namespace("http://www.w3.org/2002/07/owl#")
        self.rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        self.biblio = Namespace("http://www.linguistics-ontology.org/bibliography/bibliography.owl#")
        self.goldbib = Namespace("http://www.linguistics-ontology.org/bibliography/gold-bibliography.rdf#")
        self.gold = Namespace("http://purl.org/linguistics/gold/")
        self.rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
        self.bibtex = Namespace("http://purl.oclc.org/NET/nknouf/ns/bibtex#")
        self.person = Namespace("http://www.linguistics-ontology.org/bibliography/person.rdf#")

        # get namespaces from graph            
        self.namespaces = []
        namespaces = self.g.namespaces()

    def __del__(self):
        """
        Desconstructor for the Graph object
        """
        self.g.close()

    def getPredicateObjects(self, subject):
        """
        Return a list of predicate and object tuples for a given subject

        :type subject: str
        :param subject: a URI
        :rtype: list
        :return: a list of predicate and object tuples that match the 
        """
        return list(self.g.predicate_objects(subject))

    def getClasses(self):
        """
        Returns all subjects that match rdfs:type predicates and owl:Class objects. Returns a list of type rdflib.Literal.Literal.        

        :rtype: list
        :return: a list of rdflib.URIRef.URIRef objects
        """
        return list(self.g.subjects(self.rdf["type"], self.owl["Class"]))

    def getBibtexPublicationType(self):
        """
        Returns a list of rdflib.Literal.Literal objects

        :rtype: list
        """
        return list(self.g.subjects(self.rdf["about"], self.x["Barnes1984"]))

    def getDescription(self, subject):
        """
        Gets each class' rdfs:comment. Takes a list of subjects. Returns a list of lists of rdflib.Literals, which are of type list, e.g.
        [rdflib.Literal('Verbalizer is the class of category changing units that change nouns into verbs.', language=None, datatype=None)]. Print on an rdflib.Literal prints the URI.

        :type subject: str
        :param subject: a URI

        :rtype: list
        """
        return list(self.g.objects(subject, self.rdfs["comment"]))

    def getDescriptions(self, l):
        """
        Gets each class' rdfs:comment. Takes a list of subjects. Returns a list of lists of rdflib.Literals, which are of type list, e.g.
        [rdflib.Literal('Verbalizer is the class of category changing units that change nouns into verbs.', language=None, datatype=None)]

        :type l: list
        :param l: a list of subject nodes

        :rtype: list
        :return: a list of lists of rdflib.Literals, which are of type list, e.g.
        [rdflib.Literal('Verbalizer is the class of category changing units that change nouns into verbs.', language=None, datatype=None)]        

        """
        results = []
        for i in l:
            relations = list(self.g.objects(i, self.rdfs["comment"]))
            results.append(relations)
        return results

    def getCitations(self, subject):
        """
        Return a list of objects where the subject parameter matches the biblio["hasCitation"] predicate

        :type subject: str
        :param subject: a URI
        :rtype: list
        """
        return list(self.g.objects(subject, self.biblio["hasCitation"]))

    def getCitationsPages(self, subject):
        """
        Return a list of objects where the subject parameter matches the biblio["hasPageInformation"] predicate

        :type subject: str
        :param subject: a URI
        :rtype: list
        """
        return list(self.g.objects(subject, self.biblio["hasPageInformation"]))

    def getCitationsBibtexEntry(self, subject):
        """
        Return a list of objects where the subject parameter matches the biblio["hasEntry"] predicate

        :type subject: str
        :param subject: a URI
        :rtype: list
        """
        return list(self.g.objects(subject, self.biblio["hasEntry"]))

    def getCitationsBibtexTitle(self, subject):
        """
        Get object matches of a graph given a tuple (subject, biblio:hasBookTitle). The subject passed it needs to be a string and not a rdflib.URI object. 

        :type subject: str
        :param subject: subject passed it needs to be a string and not a rdflib.URI object
        :rtype: list
        """
        return list(self.g.objects(subject, self.biblio["hasBookTitle"]))

    def getCitationsBibtexAuthors(self, subject):
        """
        Get object matches of a graph given a tuple (subject, biblio:hasAuthorList). The subject passed it needs to be a string and not a rdflib.URI object. 

        :type subject: str
        :param subject: subject passed it needs to be a string and not a rdflib.URI object
        :rtype: list
        """
        # return self.g.objects(subject, self.biblio["hasAuthorList"]))  # double-check this
        return list(self.g.objects(subject, self.biblio["hasAuthorList"]))

    # bibtex:hasYear
    def getCitationsBibtexPublicationYear(self, subject):
        """
        Get object matches of a graph given a tuple (subject, biblio:hasBookTitle). The subject passed it needs to be a string and not a rdflib.URI object. 

        :type subject: str
        :param subject: subject passed it needs to be a string and not a rdflib.URI object
        :rtype: list
        """
        print list(self.g.objects(self.bibtex["Book"], self.biblio["hasAuthorList"]))
        
    # bibtex:hasPublisher
    def getCitationsBibtexPublisher(self, subject):
        """
        Return a list of objects where the subject parameter matches the biblio["hasPublisher"] predicate

        :type subject: str
        :param subject: a URI
        :rtype: list
        """
        return list(self.g.objects(subject, self.biblio["hasPublisher"]))

    # bibtex:hasAddress
    def getCitationsBibtexAddress(self, subject):
        """
        Return a list of objects where the subject parameter matches the biblio["hasAddress"] predicate

        :type subject: str
        :param subject: a URI
        :rtype: list
        """
        return list(self.g.objects(subject, self.biblio["hasAddress"]))

    # rdfs:comment
    def getCitationsBibtexComment(self, subject):
        """
        Return a list of objects where the subject parameter matches the rdfs["comment"] predicate

        :type subject: str
        :param subject: a URI
        :rtype: list
        """
        return list(self.g.objects(subject, self.rdfs["comment"]))

    # biblio:hasEditorList
    def getCitationsBibtexEditors(self, subject):
        """
        Return a list of objects where the subject parameter matches the biblio["hasEditorList"] predicate

        :type subject: str
        :param subject: a URI
        :rtype: list
        """
        return list(self.g.objects(subject, self.biblio["hasEditorList"]))

    # bibtex:hasSeries
    def getCitationsBibtexSeries(self, subject):
        """
        Return a list of objects where the subject parameter matches the biblio["hasSeries"] predicate

        :type subject: str
        :param subject: a URI
        :rtype: list
        """
        return list(self.g.objects(subject, self.biblio["hasSeries"]))

    # bibtex:hasVolume
    def getCitationsBibtexVolume(self, subject):
        """
        Return a list of objects where the subject parameter matches the biblio["hasVolume"] predicate

        :type subject: str
        :param subject: a URI
        :rtype: list
        """
        return list(self.g.objects(subject, self.biblio["hasVolume"]))

    # bibtex:hasJournal
    def getCitationsBibtexJournal(self, subject):
        """
        Return a list of objects where the subject parameter matches the biblio["hasJournal"] predicate

        :type subject: str
        :param subject: a URI
        :rtype: list
        """
        return list(self.g.objects(subject, self.biblio["hasJournal"]))

    # <bibtex:Article rdf:about="Barnes1984">
    # <bibtex:InCollection rdf:about="Noonan1994">
    # <bibtex:Book rdf:about="Miller1965">

    def getCitationsBibtexPublicationType(self, object):
        uri = object[0]
        # print "OBJECT:", uri
        ref_split = uri.partition("#")
        ref = ref_split[2]
        print "REF:", ref
        # return list of URIs instead of rdflib.URIRef objects (for now)
        subjects = list(self.g.subjects(self.rdf["about"], ref))
        print "SUBJECTS:", subjects
        return subjects

    # test this - doesn't seem to work in the interpreter
    def getLabel(self, subject):
        """
        Return a list of objects where the subject parameter matches the rdfs["label"] predicate

        :type subject: str
        :param subject: a URI
        :rtype: list
        """
        return list(self.g.objects(subject, self.rdfs["label"]))

    def getLabels(self, l):
        """
        Return a list of objects where the subject parameter matches the rdfs["label"] predicate

        :type l: list
        :param l: a list of subject (strs) as URIs
        :rtype: list
        """        
        results = []
        for i in l:
            relations = list(self.g.objects(i, self.rdfs["label"]))
            results.append(relations)
        return results

    def getSubClasses(self, subject):
        """
        Returns a list of rdflib.URIRef objects that contains the subClassOf relations for the passed in subject.

        :type subject: str
        :param subject: a URI
        :rtype: list
        """
        return list(self.g.objects(subject, self.rdfs["subClassOf"]))

    def getCitaton(self, c):
        objects = list(self.g.objects())
        pass

    # doesn't work -- fix this
    def isDefinedBy(self):
        """
        Returns a list of of (rdflib.URIRef, rdflib.URIRef) tuples for (subject, object) defined by the predicate rdfs:isDefinedBy.

        :rtype: list
        """
        return list(self.g.subject_objects(self.rdfs["isDefinedBy"]))

    # BEGIN BIBMANAGER METHODS

    def printGraph(self):
        """
        Print the graph
        """
        print self.g.serialize()

    def getAuthorList(self, subject):
        """ 
        Return a list of subjects that match rdf:type biblio:hasAuthorList

        :type subject: str
        :param subject: a URI
        :rtype list
        """
        return list(self.g.objects(subject, self.biblio["hasAuthorList"]))

    def getEditorList(self, subject):
        """ 
        Return a list of subjects that match rdf:type biblio:hasEditorList

        :type subject: str
        :param subject: a URI
        :rtype: list
        """
        return list(self.g.objects(subject, self.biblio["hasEditorList"]))

    def getSeq(self, subject):
        """ 
        Returns a sequence of objects that match the subject parameter and rdf:_1

        :type subject: str
        :param subject: a URI
        :rtype: list
        """
        return list(self.g.objects(subject, self.rdf["_1"]))

    def getSeqs(self, bnode):
        """ 
        Return a list of predicates_object tuples that have a bnode

        :type bnode: str
        :param bnode: a URI
        :rtype: list
        """
        return list(self.g.predicate_objects(bnode))

    def getYear(self, subject):
        """ 
        Return a list of subjects that match rdf:type bibtex:hasYear

        :type subject: str
        :param subject: a URI
        :rtype: list
        """
        return list(self.g.objects(subject, self.bibtex["hasYear"]))

    def getTitle(self, subject):
        """ 
        Return a list of subjects that match rdf:type bibtex:Title

        :type subject: str
        :param subject: a URI
        :rtype: list
        """
        return list(self.g.objects(subject, self.bibtex["hasTitle"]))

    def getJournal(self, subject):
        """ 
        Return a list of subjects that match rdf:type bibtex:hasJournal

        :type subject: str
        :param subject: a URI
        :rtype: list
        """
        return list(self.g.objects(subject, self.bibtex["hasJournal"]))

    def getVolume(self, subject):
        """ 
        Return a list of subjects that match rdf:type bibtex:hasVolume

        :type subject: str
        :param subject: a URI
        :rtype: list
        """
        return list(self.g.objects(subject, self.bibtex["hasVolume"]))

    def getPublisher(self, subject):
        """ 
        Return a list of subjects that match rdf:type bibtex:hasPublisher

        :type subject: str
        :param subject: a URI
        :rtype: list
        """
        return list(self.g.objects(subject, self.bibtex["hasPublisher"]))

    def getAddress(self, subject):
        """ 
        Return a list of subjects that match rdf:type bibtex:hasAddress

        :type subject: str
        :param subject: a URI
        :rtype: list
        """
        return list(self.g.objects(subject, self.bibtex["hasAddress"]))

    def getChapter(self, subject):
        """ 
        Return a list of subjects that match rdf:type bibtex:hasChapter

        :type subject: str
        :param subject: a URI
        :rtype: list
        """
        return list(self.g.objects(subject, self.bibtex["hasChapter"]))

    def getPages(self, subject):
        """ 
        Return a list of subjects that match rdf:type bibtex:hasPages

        :type subject: str
        :param subject: a URI
        :rtype: list
        """
        return list(self.g.objects(subject, self.bibtex["hasPages"]))

    def getBookTitle(self, subject):
        """ 
        Return a list of subjects that match rdf:type bibtex:hasBookTitle

        :type subject: str
        :param subject: a URI
        :rtype: list
        """
        return list(self.g.objects(subject, self.bibtex["hasBookTitle"]))

    def getArticles(self):
        """
        Return a list of subjects that match rdf:type bibtex:Article

        :rtype: list
        """
        return list(self.g.subjects(self.rdf["type"], self.bibtex["Article"]))

    def getInCollections(self):
        """ 
        Return a list of subjects that match rdf:type bibtex:InCollection

        :rtype: list
        """
        return list(self.g.subjects(self.rdf["type"], self.bibtex["InCollection"]))

    def getInProceedings(self):
        """ 
        Return a list of subjects that match rdf:type bibtex:InProceedings

        :rtype: list
        """
        return list(self.g.subjects(self.rdf["type"], self.bibtex["InProceedings"]))

    def getBooks(self):
        """ 
        Return a list of subjects that match rdf:type bibtex:Book

        :rtype: list
        """
        return list(self.g.subjects(self.rdf["type"], self.bibtex["Book"]))

    def getMiscs(self):
        """ 
        Return a list of subjects that match rdf:type bibtex:Misc

        :rtype: list
        """
        return list(self.g.subjects(self.rdf["type"], self.bibtex["Misc"]))

    def getTechReports(self):
        """ 
        Return a list of subjects that match rdf:type bibtex:TechReport

        :rtype: list
        """        
        return list(self.g.subjects(self.rdf["type"], self.bibtex["TechReport"]))

    def getPhdTheses(self):       
        """ 
        Return a list of subjects that match rdf:type bibtex:PhDThesis

        :rtype: list
        """
        return list(self.g.subjects(self.rdf["type"], self.bibtex["PhdThesis"]))

    def __len__(self):
        """ 
        Return length of (merged) graph(s).

        :rtype: int
        :return: length of the graph
        """
        return len(self.g)

    def getLength(self):
        """ 
        Return length of (merged) graph(s).

        :rtype: int
        :return: length of the graph
        """
        return len(self.g)

    def getAuthors(self, subject):
        """
        Return a list of authors that match the subject and biblio:hasAuthorList, e.g.:
        s: rdf:about="http://www.linguistics-ontology.org/bibliography/gold-bibliography.rdf#Leman1980"
        p: biblio:hasAuthorList

        :type subject: str
        :param subject: a URI
        :rtype: list
        """
        return list(self.g.objects(subject, self.biblio["hasAuthorList"]))

    # not yet tested
    def getSubjectObjects(self, predicate):
        """ 
        Returns a list of (subject, object) tuples for the given predicate. The predicate may be passed as either a uri or as a tuple of (uri_prefix, concept).

        :type predicate: str
        :param predicate: a URI
        :rtype: list
        """

        if type(predicate) == []:
            return list(subject_objects(predicate[0], predicate[1]))
        else:
            return list(subject_objects(predicate))

if __name__=="__main__":
    g = GraphManager(["http://depts.washington.edu/eling/gold/gold-2008.owl", "http://depts.washington.edu/eling/bibliography/gold-bibliography.rdf", "http://depts.washington.edu/eling/bibliography/bibliography.owl"])
    classes = g.getClasses()
    for i in range(0, len(classes)):
        print "onto_element\turi\t", classes[i].encode("utf-8")
    #for i in range(0, 10):
        #print type(classes[i])
        #print type(g.getPredicateObjects(classes[i]))
        #print g.getCitationsBibtexAuthors(classes[i])

""" methods to add:
subject_predicates(self, object)
A generator of (subject, predicate) tuples for the given object
subjects(self, predicate, object)
A generator of subjects with the given predicate and object
transitive_objects(self, subject, property, remember)
Transitively generate objects for the `property` relationship
transitive_subjects(self, predicate, object, remember)
Transitively generate objects for the `property` relationship
triples(self, (s, p, o))
Generator over the triple store
predicate_objects(self, subject)
A generator of (predicate, object) tuples for the given subject
predicates(self, subject, object)
A generator of predicates with the given subject and object
objects(self, subject, predicate)
A generator of objects with the given subject and predicate
"""
# getPhonemicEnvironment(phoneme, lang)
# getConstituents(syntacticUnit)
# getExample(class)


