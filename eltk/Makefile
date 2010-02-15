PYTHON = python

.PHONY: usage all doc clean clean_code clean_up test

usage:
	@echo "make dist -- Build distributions (output to dist/)"
	@echo "make clean -- Remove all built files and temporary files"
	@echo "make clean_up -- Remove temporary files"

########################################################################
# DISTRIBUTIONS
########################################################################

#dist: zipdist gztardist rpmdist windist dmgdist
dist: gztardist

gztardist: clean_code
	$(PYTHON) setup.py -q sdist --format=gztar
zipdist: clean_code
	$(PYTHON) setup.py -q sdist --format=zip
rpmdist: clean_code
	$(PYTHON) setup.py -q bdist --format=rpm
windist: clean_code
	$(PYTHON) setup.py -q bdist --format=wininst
docdist:
	find doc -print | egrep -v '.svn|.DS_Store' | zip dist/nltk-doc-$(VERSION).zip -@

test:
	$(PYTHON) eltk/test/alltests.py

datadist:
	find nltk_data -print | egrep -v '.svn|.DS_Store' | zip -n .zip:.gz dist/nltk-data-$(VERSION).zip -@

nightlydist: codedist
	REVISION = `svn info | grep Revision: | sed "s/Revision: //"`

checksums:
	md5 dist/nltk-$(VERSION).tar.gz
	openssl sha1 dist/nltk-$(VERSION).tar.gz
	openssl rmd160 dist/nltk-$(VERSION).tar.gz


###############
# DOCS
# ##############
#

doc:
	$(MAKE) -C docs html

########################################################################
# CLEAN
########################################################################

.PHONY: clean clean_up

clean:
	rm -rf dist build MANIFEST


clean_code:
	rm -f `find . -name '*.pyc'`
	rm -f `find . -name '*.pyo'`
	rm -f `find . -name '*~'`
	rm -f MANIFEST # regenerate manifest from MANIFEST.in



