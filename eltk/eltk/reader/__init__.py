# -*- coding: UTF-8 -*-
# e-Linguistics Toolkit:
#
# Copyright (C) 2008 ELTK Project
# Author:       Scott Farrar <farrar@u.washington.edu>
#               Steven Moran <stiv@u.washington.edu            
# URL: <http://e-linguistics.org>
# For license information, see LICENSE.TXT
"""
Various readers are used to migrate  so-called "legacy data", ie files that are not yet in a format compatible with the GOLD Community of Practice---those that contain no semantic markup. For each type of legacy data file/format, a new reader class will need to be written. For instance, there are readers for:

    * Praat TextGrid files
    * Elan eaf files
    * Leipzig Glossing Rules (in plain txt format)
    * simple termsets in CVS format (author terms mapped to GOLD URIs)
    * BibTeX files

Quite separate in terms of functionality is the reader for LinkedData.

"""


