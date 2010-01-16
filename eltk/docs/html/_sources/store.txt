.. _store:

Store
=============


.. automodule:: eltk.store.store
    :members:

How to use store
-----------------

First create simple store with rdflib::

    >>> store = plugin.get('MySQL', Store)() #('GOLDComms_id')

You must convert the config string to one compatible with rdflib::

    >>> rdflib_config_string = 'host='+STORE_CONFIG['host']+',user='+STORE_CONFIG['user']+',password='+STORE_CONFIG['password']+',db='+STORE_CONFIG['db']

Open the store::

    >>> store.open(rdflib_config_string, create=False)

Create a conjunctive graph using the store::

    >>> cg = ConjunctiveGraph(store)
    >>> print len(cg)

Show the results::

    >>> results = sparqlQuery('SELECT  ?o WHERE {<http://purl.org/linguistics/gold/%s> rdfs:comment ?o }' % 'VerbPhrase',cg)

    >>> for r in results:
    >>>    print r[0]

Store Utils
============

.. automodule:: eltk.store.utils
    :members:


