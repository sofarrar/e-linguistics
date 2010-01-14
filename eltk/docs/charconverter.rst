.. _charconverter:

Character Converter
===================

.. automodule:: eltk.utils.CharConverter

Illustration of usage
---------------------

Here's how to create a converter from XSampa (e.g., used in  Elan) to unicode IPA::

    >>> elan_converter=CharConverter('xsampa','uni')

Now convert a string in XSampa to Unicode IPA::

    >>> elan_converter.convert('kO nEnE Oku')
    'k\xc9\x94 n\xc9\x9bn\xc9\x9b \xc9\x94ku'

In order to see the results, use a print statement::

    >>> print elan_converter.convert('kO nEnE Oku')
    kɔ nɛnɛ ɔku

The converter can be used for common latex escape characters as well.

.. autodata:: eltk.utils.CharConverter.latex_charmap

The usage is the same::

    >>> latex_converter=CharConverter('uni','latex')
    >>> print latex_converter.convert('ü')
    \"{u}



.. autodata:: eltk.utils.CharConverter.ipa_charmap


.. automethod:: eltk.utils.CharConverter.CharConverter.__init__(self,source,target)

.. automethod:: eltk.utils.CharConverter.CharConverter.convert(string,string)


