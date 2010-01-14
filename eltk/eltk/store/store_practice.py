import MySQLdb

import abc

#note, fix rdflib imports when rdflib-2.5 is finalized

#rdflib-2.5
#from rdflib.graph import Graph
from rdflib.Graph import Graph, ReadOnlyGraphAggregate,ConjunctiveGraph

#from rdflib.namespace import Namespace
from rdflib.Namespace import Namespace

#from rdflib.term import URIRef
from rdflib.URIRef import URIRef

from rdflib import Literal

from rdflib import plugin, exceptions
from rdflib.syntax.parsers import Parser

from rdflib import RDF,RDFS

from rdflib.store import Store

#connect to mysql
#NOTE: replace params with your local mysql settings
#db = MySQLdb.connect(user='farrar',passwd=";lkjJK")

#c = db.cursor()

#c.execute("""show databases;""")

#row = c.fetchall()

#if db has already been created
#if ('GOLDComm',) in row:
    
#then delete it in order to create empty instance
#    c.execute("""drop database GOLDComm;""")

#create empty instance
#c.execute("""create database GOLDComm;""")


#NOTE: replace params with your local mysql settings
configString = "host=localhost,user=farrar,password=;lkjJK,db=GOLDComm"

# Get the mysql plugin. You may have to install the python mysql libraries
store = plugin.get('MySQL', Store)('GOLDComms_id')

#this works too
#store = MySQL(identifier,configuration)

#use rdflib to create schema for instance, that is, create doens't "create the db, rather, it creates the schema for the db
store.open(configString, create=False)
#print store.identifier

###################
# a ConjunctiveGraph
###################
conjgraph = ConjunctiveGraph(store=store,identifier=URIRef('http://purl.org/linguistics/gold'))

data = Namespace('http://purl.org/linguistics/data/')

conjgraph.bind('data',data)

#probably no triples should be added the conjgraph
#conjgraph.add((data['lingsign123'], data['orthographicRep'], Literal('dog')))
#conjgraph.add((data['lingsign456'], data['orthographicRep'], Literal('cat')))
#conjgraph.add((data['lingsign789'], data['orthographicRep'], Literal('fish')))

#print conjgraph.default_context
conjgraph.commit()
"""


##############
# Plain Graph1
################
"""
graph1 = Graph(store, identifier = URIRef('http://purl.org/linguistics/e-linguistics/signs'))


graph1.add((URIRef('myname'), RDFS.label, Literal('blah')))

graph1.commit()
"""


##############
# Plain Graph2
################

"""
graph2 = Graph(store, identifier = URIRef('http://purl.org/linguistics/e-linguistics/phons'))


graph2.add((URIRef('you'), RDFS.label, Literal('you')))

graph2.commit()

#adding more than one conjunctive graph seems to make no difference. Both have all triples
#
#conjgraph2 = ConjunctiveGraph(store=store,identifier=URIRef('http://conjgraph2'))
#conjgraph2.add((URIRef('I'), RDFS.label, Literal('I')))
#conjgraph2.commit()

"""
print '******'

print len(store), ' is the length of the store'
print len(conjgraph), ' is the length of the conjgraph'
#print len(conjgraph2)
print len(graph1),' is the length of the graph1' 
print len(graph2),' is the length of the graph2'


ga = ReadOnlyGraphAggregate([graph1,graph2])

print len(ga), ' is the length of a subset graph'
"""

#to read from a store
#for t in conjgraph:
#    print t,'\n'

#ns = dict(rdf=RDF.RDFNS,rdfs=RDFS.RDFSNS)
#for i in conjgraph.query('SELECT ?o WHERE {?x <http://purl.org/linguistics/data/orthographicRep> ?o } ',initNs=ns):
#    print i




# display the graph in RDF/XML
#
#Note: serializing conjgraph prints entire store
#
#print '*******conjgraph***********\n',conjgraph.serialize()
#print '*******graph1***********\n',graph1.serialize()
#print '*******graph2***********\n',graph2.serialize()


#get indiv graphs in the store
#prints top-lovel conjgraph and subgraphs
#for c in store.contexts():
#    print c



