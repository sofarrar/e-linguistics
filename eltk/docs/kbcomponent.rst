.. _kbcomponent:

KBComponent
===========

Background
----------

In order to understand the design of the ontology component of the ELTK, we provide a brief explanation of how data and ontologies are used within knowledge engineering, especially in the context of `Description Logics <http://dl.kr.org/>`_ and related languages such as the Web Ontology Language (OWL). Knowledge bases in the Description Logic world consist of two logically separate components: 

    * the ontology proper (called the TBox) 
    * the various assertions about concepts from the ontology (called the ABox) 
      
So, the standard description of such a knowledge base (KB) is  KB = <TBox, ABox>, where TBox is a set of classes and relations and ABox is a set of assertions about instances of classes. But since we're dealing with `Linked Data <http://linkeddata.org>`_, the situation is a bit more complex. 

Chunks of knowledge
--------------------

.. automodule:: eltk.kb.KBComponent

.. autoclass:: eltk.kb.KBComponent.KBComponent

.. .. automethod:: eltk.kb.Ontology.Ontology.__init__(self,identifier='')

.. .. automethod:: eltk.kb.Ontology.Ontology.parse(self, source, publicID=None, format="xml")

.. .. automethod:: eltk.kb.Ontology.Ontology.addEntity(self,ent)

.. Access methods
.. --------------

.. Ontology has several methods to access its data:

.. .. automethod:: eltk.kb.Ontology.Ontology.getClasses(self)

..  .. automethod:: eltk.kb.Ontology.Ontology.getObjProp(self)

..  .. automethod:: eltk.kb.Ontology.Ontology.getDatatypeProp(self)

..  .. automethod:: eltk.kb.Ontology.Ontology.getIndividuals(self)

..  .. automethod:: eltk.kb.Ontology.Ontology.getEntity(self,uri)



Illustration of usage
---------------------

Here's how to create a knowledge base component: ::

    >>> from eltk.kb.KBComponent import KBComponent
    >>> from eltk.kb.Meta import *

Create the KBComponent, and then some classes and properties: :: 

    >>> mykb = KBComponent()
    >>> hasConstituent = OWLObjectProperty.new(u'http://foo.org/hasConstituent')
    >>> Word = OWLClass.new(u'http://foo.org/Word')   
    >>> w1 = Word(u'http://foo.org/w1')
    >>> Morpheme = OWLClass.new(u'http://foo.org/Morpheme')   
    >>> m1 = Morpheme(u'http://foo.org/m1')

And add a statement to the KBComponent: ::

    >>> mykb += (w1, hasConstituent, m1)

The statement is in the form of a triple, and is equivalent to this: ::

    >>> mykb += hasConstituent(w1, m1)

See :doc:`meta` for an explanation.


Ontology
--------

.. autoclass:: eltk.kb.KBComponent.Ontology


Methods
-------

Here are the methods associated with KBComponent.

.. automethod:: eltk.kb.KBComponent.KBComponent.buildRDFGraph

Depending on the contents of a particular :class:`KBComponent`, several methods could be applicable.



