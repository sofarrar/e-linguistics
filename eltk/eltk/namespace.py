#note, fix rdflib imports when rdflib-2.5 is finalized

#rdflib-2.5
#from rdflib.namespace import Namespace
from rdflib.Namespace import Namespace

"""
Various widely used namespaces are listed in the namespaces module.
"""

OWLNS=Namespace("http://www.w3.org/2002/07/owl#")
LINGNS=Namespace("http://purl.org/linguistics/")
GOLDNS=Namespace("http://purl.org/linguistics/gold#")
GOLDCOMMNS=Namespace("http://purl.org/linguistics/goldcomm/")
TERMSETNS=Namespace("http://purl.org/linguistics/goldcomm/termset/")
DATANS=Namespace("http://purl.org/linguistics/goldcomm/data/")


