.. _meta:

Meta
=========

Background
----------

.. automodule:: eltk.kb.Meta

.. autoclass:: eltk.kb.Meta.RDFSResource

.. autoclass:: eltk.kb.Meta.RDFSClass

.. autoclass:: eltk.kb.Meta.RDFProperty

.. autodata:: eltk.kb.Meta.RDFtype

.. autoclass:: eltk.kb.Meta.OWLClass

.. autoclass:: eltk.kb.Meta.OWLObjectProperty

.. autoclass:: eltk.kb.Meta.OWLDatatypeProperty

Illustration of usage
---------------------

The first thing to do is to import the :mod:`Meta` module::

    >>> from eltk.kb.Meta import *

OWLClass
^^^^^^^^

In the simplest case, an OWL class can be created using the new constructor which takes some URI::

    >>> Word=OWLClass.new(u'http://mydomain.org/Word')

The new constructor is needed in order to create an instance of metaclass, i.e., Word. Its URI can be called using :meth:`getURI` ::

    >>> Word.getURI()
    >>> http://mydomain.org/Word

The following also works ::

    >>>Word.uri
    >>> http://mydomain.org/Word

To demonstrate inheritance, let's create another class::

    >>> Root=OWLClass.new(u'http://mydomain.org/Root')

And then create yet a third class that inherits from both Word and Root::

    >>> RootWord=OWLClass.new(u'RootWord',(Word,Root))

    >>> issubclass(RootWord,Root)
    True
    >>> issubclass(RootWord,Word)
    True

.. Need to fix this:

.. Thus, the correct typing is obtained for RootWord, as both a Root and a Word. However, :meth:`OWLEntity.type` produces this ::

..    >>> issubclass(RootWord,Word)
    True

.. And its type can be called using :meth:`OWLEntity.type`::

..    >>> type(Word)
..    >>> <class 'eltk.kb.OWLEntity.OWLClass'>

.. .. autofunction:: eltk.kb.OWLEntity.type
 
Instances
^^^^^^^^^

Instances of classes (cf. OWL individuals) can be created as follows: ::

    >>> Word = OWLClass.new('http://foo.org/Word')
    >>> w1 = Word(u'http://foo.org/word123')
    >>> w2 = Word(u'http://foo.org/word456')
    >>> type(w1)
    <class 'eltk.kb.Meta.Word'>

The getType method is defined to return a list of all types ::

    >>> getType(w1)
    [<class 'eltk.kb.Meta.Word'>] 

.. autofunction:: eltk.kb.Meta.getType

    >>> class1 = OWLClass.new(u'http://foo.org/class1')
    >>> class2 = OWLClass.new(u'http://foo.org/class2')
    >>> i = class1(u'http://foo.org/i',[class2])
    >>> getType(i)
    [<class '__main__.class2'>, <class '__main__.class1'>]

Properties
^^^^^^^^^^

There are two kinds of OWL properties: :class:`OWLObjectProperty` and :class:`OWLDatatypeProperty`. An :class:`OWLObjectProperty` can be created as follows ::

    >>> hasConstituent = OWLObjectProperty.new(u'http://foo.org/hasConstituent')

We now create a Morpheme individual in order to demonstrate has the property can be used ::

    >>> Morpheme = OWLClass.new(u'http//foo.org/Morpheme')
    >>> m1 = Morpheme(u'http:foo.org/m1')

The property can be used as follows, glossed as "the Word w1 has the Morpheme m1 as its constituent" ::

    >>>  hasConstituent(w1,m1)
    (<eltk.kb.Meta.Word object at 0x3a68dd0>, <class 'eltk.kb.Meta.hasConstituent'>, <eltk.kb.Meta.Morpheme object at 0x3a68f90>)

Notice that a 3-tuple (a triple) was returned. That is, when a property is called, a statement in the form of a triple is created.
