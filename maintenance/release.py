# -*- coding: utf-8 -*-
""" This tool prepares and sets the framework directory for final release by
performing several actions:

* create docs from docstrings in HTML and LaTeX (PDF) format
  [doxygen]
* run unittests
  [nosetests]
* create coverage report in HTML format
  [coverage]

Script very similar to the one given in
@see https://github.com/valhallasw/pywikipedia-nightly-generation/blob/master/tests.sh
@see http://lists.wikimedia.org/pipermail/pywikipedia-l/2012-January/007120.html
@see http://nedbatchelder.com/code/coverage/
"""
#
# (C) Pywikipedia bot team, 2013
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'
#

import sys, os

scriptdir = os.path.dirname(sys.argv[0])
if not os.path.isabs(scriptdir):
    scriptdir = os.path.abspath(os.path.join(os.curdir, scriptdir))
scriptdir = os.path.split(scriptdir)[0]

docsdir     = os.path.join(scriptdir, 'docs/')
coveragedir = os.path.join(docsdir, 'coverage/')

os.chdir( scriptdir )


print '* create docs from docstrings in HTML and LaTeX (PDF) format\n' \
      '  [doxygen]'
if not os.path.exists(docsdir):
    os.mkdir(docsdir)
os.system('date > %s' % os.path.join(docsdir, 'release-doxygen.log'))
os.system('doxygen &>> %s' % os.path.join(docsdir, 'release-doxygen.log'))


print '* run unittests\n' \
      '  [nosetests]'
#open('user-config.py', 'w').write("""
#usernames['wikipedia']['en'] = 'pwb-nightly-test-runner'
#mylang='en'
#family='wikipedia'
#""")
#os.system('date > ../output/test_pywikipedia.txt')
#os.system('nosetests --with-xunit --xunit-file=../output/xunit_pywikipedia.xml tests 2>> ../output/test_pywikipedia.txt')
os.system('date > %s' % os.path.join(docsdir, 'release-nosetests.log'))
os.system('nosetests 2>> %s' % os.path.join(docsdir, 'release-nosetests.log'))


print '* create coverage report in HTML format\n' \
      '  [coverage]'
#os.system('coverage report -m')
os.system('coverage html --directory=%s' % os.path.join(docsdir, 'coverage/'))
