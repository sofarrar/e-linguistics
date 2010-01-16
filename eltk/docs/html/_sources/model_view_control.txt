.. _model_view_control:

Model-View-Control
==================

Within the framework of `e-linguistics <http://purl.org/linguistics/e-linguistics>`_, there are components that may be described in terms of the model-view-control design pattern. This provides a clear way to loosely couple the components into a cohesive whole, yet maintain modularity for each component.


Model
-----

Within the MVC pattern, the *model* refers to some data model typically expressed in a relational database. Within e-linguistics, the model is the  conceptualization of linguistic knowledge. In fact, the model consists of a knowledge level and a logical level (cf. Guarino 1995). First, there is the knowledge captured by the `GOLD Community of Practice <http://purl.org/linguistics/goldcomm>`_, or GOLDComm for short. The knowledge itself is partitioned into an ontology (GOLD), (potentially several) subontologies called Community of Practice Extensions (COPEs) and an arbitrarily large collection of instance data, that instantiates GOLD and COPE concepts. 

On the logical level, there is the  abstract graph model of the `Resource Description Framework (RDF) <http://ww.w3.org/RDF/>`_. The ontology and instance data, then, are expressed using the more basic subject-predicate-object model of RDF.  (It should be noted that linguistic knowledge could be expressed using some other logical structure.) The concrete serialization of the RDF model could be expressed in RDF/XML, N3 notation, an RDF database, etc. For the purposes of the current project, we will use RDF/XML to expose the structure of the data. This provides a "hook" for interoperability with other projects and tools. We will also make use of RDF databases, those optimized to work with the underlying RDF model.

View
----

With the MVC pattern, the *view* refers to data display. In e-linguistics the view consists of the various ways to visualize linguistics data. Lexical data, for instance, may be viewed as a structured entry with a headword and a definition, etymological info, etc. Data commonly expressed in structured paradigms may be given in tabular or interlinear form. Phonological descriptions may be given either as a simple collection of forms, or as a phonological rules.


Control
-------

Control refers to how the user is able to drive the system in order to access the data for manipulation: changing, validating, viewing, etc. For the  *control* component, the various modules of the `e-Linguistics Toolkit (ELTK) <http://purl.org/linguistics/eltk>`_ are used. Specifically, the ELTK provides a mechanism (through Python's metaclasses) to import GOLDComm's content into the Python object-oriented programming platform. Classes, relations, and individuals from the GOLD ontology are translated into first order Python entities: classes, methods and instances. This way, the programmer (or application) can have *control* over the entire *model*. This allows for the efficient access to GOLDComm's content without having to worry about its form or serialization. Direct manipulation of the model can provide for content validation of GOLDComm data. For instance, nouns in a particular language may not be associated with the locative case.


Summary of ELTK's functionality:

    * model manipulation -- access to GOLDComm's content

    * data migration -- translation of un- or semi-structured data to GOLDComm

    * content validation -- verifying that data do not violate the conceptualization 

    * display -- the creation of display structures for human consumption

Django
------

Finally, there is `Django <http://www.djangoproject.com>`_, the Python web framework used to bring everything together as a cohesive unit. Django provides the means to build a website, facilitate web services, and access a db system. Django  itself resembles the MVC pattern, (see  `this explanation <http://www.djangobook.com/en/2.0/chapter05/>`_). However, it is probably better described as a MTV pattern:


  * Model -- data access layer for getting at data expressed according to GOLDComm

  * Template -- data display component used to expose the data in various human friendly formats. HTML templates are used to accomplish this.

  * View -- the bridge between model and template



