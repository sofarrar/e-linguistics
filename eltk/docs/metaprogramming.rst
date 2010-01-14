.. _metaprogramming:

Metaprogramming
===============

The core of the ELTK is a seamless interface to the domain model of OWL. That is, OWL entities are  imported into the Python programming environment such that OWL classes, properties and individuals are created and manipulated alongside Python classes, methods and instances. The goal is to produce Python code that reﬂects the OWL domain model. In this way the developer can simply use the model at hand, not worrying about ways to re-model what is already in OWL. This approach  seems quite natural for a Semantic Web effort and  may be charac-
terized as a type of ontology-driven software design (cf. [KoideTakeda2006]_).

In order to import the OWL model into Python's OOP environment, we use **metaprogramming**, or the ability to write code to manipulate code. As inspired by [BabikHluchy2006]_, the OWL class hierarchy can be directly imported into the Python class hierarchy. 

In general OWL is conceptually similar to the object-oriented programming (OOP) paradigm, as used in Python. Both OWL and OOP allow for classes and subclasses, inheritance and limited multiple inheritance. Object composition and class instantiation are also similar. But OWL's semantics is inconsistent with that of Python's in a number of key aspects. For example in most OOP languages, a class instance can only belong to a single class. That is, in Python, the expression (MyInstance) can only yield a single class. This ensures the behavior of instances based on the associated methods and variables of the instantiated class. In OWL, however, a single individual (corresponding to an instance in OOP) can instantiate multiple classes in the same knowledge base. Thus, to provide a linguistics example, a particular language can be an indivual of both EndangeredLanguage and of Koine at the same time. In the ELTK we manage to integrate this facet of OWL semantics in a fairly seamless way.

.. [BabikHluchy2006] M. Babik and L. Hluchy. Deep integration of python with web ontology language. In Proceedings of the 2nd Workshop on Scripting for the Semantic Web, 2006.

.. [KoideTakeda2006] S. Koide and H. Takeda. Owl-full reasoning from an object oriented perspective. In R. Mizoguchi, Z. Shi, and F. Giunchiglia, editors, The Semantic Web ASWC 2006, pages 263–277. Springer, Berlin / Heidelberg, 2006.

