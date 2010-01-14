#!/usr/local/bin/python
from distutils.core import setup
import eltk
setup(
    
    #Project metadata
    name='eltk',
    version = eltk.__version__,
    url = eltk.__url__,
    long_description = eltk.__longdescr__,
    license = eltk.__license__,
    keywords = eltk.__keywords__,
    maintainer = eltk.__maintainer__,
    maintainer_email = eltk.__maintainer_email__,
    author = eltk.__author__,
    author_email = eltk.__author__,

    #note: MANIFEST.in file is needed by setup.py sdist, for jars and data files
    #the following lines are used by setup.py install
    package_data = {'eltk.examples': ['inputfiles/*']},
    
    #the following was used when owlapi was used; it was left in as a reminder
    #package_data = {'eltk': ['owlapi-bin.jar','owlapi-src.jar'], 'eltk.examples': ['inputfiles/*']},
    
    
    #Package info
    packages=['eltk',
              'eltk.kb',
              'eltk.display',
              'eltk.examples',
              'eltk.reader',
              'eltk.utils',
              'eltk.test'],

    )

