#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Externals modules automatic setup checker and installer for various OS.
"""

#
# (C) DrTrigon, 2013
# (C) Pywikipedia team, 2013
#
# Distributed under the terms of the MIT license.
#
# Strongly inspired by files beeing part of VisTrails distribution
#   utils/installbundle.py
#   utils/requirements.py
# Copyright (C) 2006-2010 University of Utah. All rights reserved.
# GNU General Public License version 2.0 by the Free Software Foundation
#
__version__ = '$Id$'
#


# supports: 0. svn:externals
#           1. package management system (yum, apt-get, ...)
#           2. download from url (or svn, git repo)
#           3. checkout from mercurial repo ('hg clone ...' since url not available)
#           (what about python eggs?!)
# dependencies: (svn, python)
#               yum, apt-get or whatever your system uses
#               mercurial (hg)
#               patch
modules_needed = {
# TODO: vvv how to apply patches under windows, e.g. and other OS... ? (needed for BeautifulSoup.py and else)
#           'patch.py': ({},
#                        {  'url': 'https://python-patch.googlecode.com/files/patch-1.12.11.py',
#                          'path': '',}),                                   # OK
#                        {  'url': 'http://google-diff-match-patch.googlecode.com/files/diff_match_patch_20121119.zip',
#                          'path': 'diff_match_patch_20121119/python2',}),  # OK
#                        {  'url': 'http://downloads.sourceforge.net/project/unxutils/unxutils/current/UnxUtils.zip',
#                          'path': '?',}),                                  # OK
            'crontab': ({},
                        #{  'url': 'https://github.com/josiahcarlson/parse-crontab/archive/master.zip',
                        #  'path': 'parse-crontab-master/crontab',}),       # OK
                        {  'url': 'https://github.com/josiahcarlson/parse-crontab/archive/1ec538ff67df6a207993a6c5b6988f4f628c5776.zip',
                          'path': 'parse-crontab-1ec538ff67df6a207993a6c5b6988f4f628c5776/crontab',},
                        {}),                                               # OK
                'odf': ({},
                        #{  'url': 'https://pypi.python.org/packages/source/o/odfpy/odfpy-0.9.6.tar.gz',
                        #  'path': 'odfpy-0.9.6/odf',}),                    # OK
                        {  'url': 'https://pypi.python.org/packages/source/o/odfpy/odfpy-0.9.4.tar.gz',
                          'path': 'odfpy-0.9.4/odf',},
                        {}),                                               # OK
           'openpyxl': ({},
                        {  'url': 'https://bitbucket.org/ericgazoni/openpyxl/get/1.5.6.tar.gz',
                          'path': 'ericgazoni-openpyxl-e5934500ffac/openpyxl',},
                        {}),                                               # OK
#           'spelling': $ svn propedit svn:externals externals/.
#                         spelling http://svn.wikimedia.org/svnroot/pywikipedia/trunk/spelling/
#         'simplejson': $ svn propedit svn:externals externals/.
#                         simplejson http://simplejson.googlecode.com/svn/tags/simplejson-2.1.3/simplejson/
#         'simplejson': ({'linux-fedora': ['python-simplejson'],
#                         'linux-ubuntu': [''],},
   'BeautifulSoup.py': ({'linux-fedora': ['python-BeautifulSoup'],
                         'linux-ubuntu': [''],},
                        {  'url': 'https://pypi.python.org/packages/source/B/BeautifulSoup/BeautifulSoup-3.2.0.tar.gz',
                          'path': 'BeautifulSoup-3.2.0/BeautifulSoup.py',
                         #$ diff -Nau TEST_BeautifulSoup.py BeautifulSoup.py > patch-BeautifulSoup
                         'patch': 'patch-BeautifulSoup',},
                        {}),                                               # OK
             'irclib': ({'linux-fedora': ['python-irclib'],
                         'linux-ubuntu': [''],},
                        {}, # http://python-irclib.sourceforge.net/
                        {}),                                               # OK
          'colormath': ({'linux-fedora': [],
                         'linux-ubuntu': ['python-colormath'],},
                        {  'url': 'https://github.com/gtaylor/python-colormath/archive/master.zip',
                          'path': 'python-colormath-master/colormath',},
                        {}),                                               # OK
               'jseg': ({},
                        {  'url': 'http://vision.ece.ucsb.edu/segmentation/jseg/software/jseg.zip',
                          'path': 'jseg',
                         #$ diff -Nau --exclude="*.o" --exclude="*.pyc" --exclude="segdist_cpp*" TEST_jseg/ jseg/ > patch-jseg
                         'patch': 'patch-jseg',},
                        {}),                                               # OK
       'jseg/jpeg-6b': ({},
                        {  'url': 'http://vision.ece.ucsb.edu/segmentation/jseg/software/jpeg-6b.zip',
                          'path': 'jpeg-6b',},
                        {}),                                               # OK
              '_mlpy': ({},
                        {  'url': 'http://downloads.sourceforge.net/project/mlpy/mlpy%203.5.0/mlpy-3.5.0.tar.gz',
                          'path': 'mlpy-3.5.0/mlpy',},
                        {}),                                               # OK
           '_music21': ({},
                        {  'url': 'http://music21.googlecode.com/files/music21-1.4.0.tar.gz',
                          'path': 'music21-1.4.0',
                         #$ diff -Naur --exclude="*.pyc" TEST__music21/ _music21/ > patch-music21
                         'patch': 'patch-music21',},
                        {}),                                               # OK
# TODO: vvv (future; enable for and use in 'catimages.py', patch needed)
           '_ocropus': ({},
                        {},
                        {  'url': 'https://code.google.com/p/ocropus',
                           'rev': 'ocropus-0.6',}),                        # OK
# TODO: vvv (further clean-up and unlink - check with 'svn list')
#             'opencv': $ svn propedit svn:externals externals/.
#                         opencv https://svn.toolserver.org/svnroot/drtrigon/externals/opencv
#                       $ svn propedit svn:externals externals/opencv/haarcascades/haartraining/
#                         HaarTraining https://svn.toolserver.org/svnroot/drtrigon/externals/haartraining/HaarTraining
#                         HaarTraining.tar.gz https://svn.toolserver.org/svnroot/drtrigon/externals/haartraining/HaarTraining.tar.gz
#                         convert_cascade.c https://svn.toolserver.org/svnroot/drtrigon/externals/haartraining/convert_cascade.c
#                         create_pos_neg.py https://svn.toolserver.org/svnroot/drtrigon/externals/haartraining/create_pos_neg.py
#                         createtestsamples.pl https://svn.toolserver.org/svnroot/drtrigon/externals/haartraining/createtestsamples.pl
#                         createtrainsamples.pl https://svn.toolserver.org/svnroot/drtrigon/externals/haartraining/createtrainsamples.pl
'opencv/haarcascades': ({},
                        {  'url': 'https://svn.toolserver.org/svnroot/drtrigon/externals/haarcascades-full.tar.gz',
                          'path': 'haarcascades',},
                        {}),                                               # OK
#          'pdfminer' is not used anymore/at the moment...
#       'pycolorname': $ svn propset svn:externals 'pycolorname https://svn.toolserver.org/svnroot/drtrigon/externals/pycolorname' externals/.
             'pydmtx': ({'linux-fedora': ['python-libdmtx'],
                         'linux-ubuntu': ['libdmtx-dev'],},
                        {  'url': 'https://github.com/dmtx/dmtx-wrappers/archive/master.zip',
                          'path': 'dmtx-wrappers-master/python',
                         #$ diff -Nau --exclude="*.pyc" TEST_pydmtx/ pydmtx/ > patch-pydmtx
                         'patch': 'patch-pydmtx',},
                        {}),                                               # OK
             'py_w3c': ({},
                        {  'url': 'https://bitbucket.org/nmb10/py_w3c/downloads/py_w3c-v0.1.0.tar.gz',
                          'path': 'py_w3c-0.1.0/py_w3c',},
                        {}),                                               # OK
# TODO: vvv (include)
#               'TEST_slic': ({},
#                        {  'url': 'http://ivrg.epfl.ch/files/content/sites/ivrg/files/supplementary_material/RK_SLICsuperpixels/SLICSuperpixelsAndSupervoxelsCode.zip',
#                          'path': 'SLICSuperpixelsAndSupervoxelsCode/SLICSuperpixels',}),# OPEN
#               'TEST_slic': ({},
#                        {  'url': 'https://github.com/amueller/slic-python/archive/master.zip',
#                          'path': 'slic-python-master',}),                 # OPEN
# (2 download sources to same dir, compilation) + patch (at least for '__init__.py') needed
              '_zbar': ({'linux-fedora': ['zbar'],
                         'linux-ubuntu': ['python-zbar'],},
                        {  'url': 'https://pypi.python.org/packages/source/z/zbar/zbar-0.10.tar.bz2',
                          'path': 'zbar-0.10',
                         #$ diff -Nau --exclude="*.pyc" TEST__zbar/ _zbar/ > patch-zbar
                         'patch': 'patch-zbar',},
                        {}),                                               # OK
# TODO: vvv (include)
#               'TEST__bob': ({},
#                        {  'url': 'https://www.idiap.ch/software/bob/packages/bob-1.1.2.zip',
#                          'path': 'bob-1.1.2',
#                         #$ diff -Nau --exclude="*.pyc" TEST__bob/ _bob/ > patch-bob
#                         'patch': 'patch-bob',},
#                        {}),                                               # OPEN
# (complex compilation) + patch (at least for '__init__.py') needed
#     'TEST_xbob_flandmark': ({},
#                        {  'url': 'https://pypi.python.org/packages/source/x/xbob.flandmark/xbob.flandmark-1.0.9.zip',
#                          'path': 'xbob.flandmark-1.0.9',},
#                         #'patch': '',},
#                        {}),                                               # OPEN
# (complex compilation, dependent on '_bob') + patch (at least for '__init__.py') needed
}

modules_order = ['crontab', 'odf', 'openpyxl', 'BeautifulSoup.py', 'irclib',
                 'colormath', 'jseg', 'jseg/jpeg-6b', '_mlpy', '_music21',
                 '_ocropus', 'opencv/haarcascades', 'pydmtx', 'py_w3c',
                 '_zbar',]
# OPEN: 'patch.py', 'opencv', 'slic', '_bob', 'xbob_flandmark',


import os, sys

import wikipedia as pywikibot   # sets externals path
#from pywikibot.comms import http

# allow imports from externals
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


### BEGIN of VisTrails inspired and copied code ### ### ### ### ### ### ### ###

def has_logger():
    #return hasattr(sys.modules['wikipedia'], 'logger')
    return hasattr(pywikibot, 'logger')

# TODO: solve properly because this is just a work-a-round, because module
# externals get imported in wikipedia.py before logger is setup properly, which
# should be changed! (meanwhile this is acceptable because code here should be
# executed once only...)
def lowlevel_warning(text):
    if has_logger():
        pywikibot.warning(text)
    else:
        print "WARNING:", text


def guess_system():
    import platform
    return ("%s-%s" % (platform.system(), platform.dist()[0])).lower()

def show_question(which_files):
    lowlevel_warning("Required package missing: %s" % which_files)
    lowlevel_warning("A required package is missing, but externals can"
                     " automatically install it."
                     " If you say Yes, externals will need administrator"
                     " privileges, and you might be asked for the administrator"
                     " password.")
    lowlevel_warning("Give externals permission to try to install package?"
                     " (y/N)")
    v = raw_input().upper()
    return v == 'Y' or v == 'YES'


def python_module_exists(module_name):
    """python_module_exists(module_name): Boolean.
Returns if python module of given name can be safely imported."""

    module_name = module_name.replace(u'.py', u'')
    module_name = module_name[1:] if module_name[0] == u'_' else module_name

    try:
        sys.modules[module_name]
        return True
    except KeyError:
        pass
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False


def linux_ubuntu_install(package_name):
    cmd = 'apt-get install -y'

    if type(package_name) == str:
        cmd += ' ' + package_name
    elif type(package_name) == list:
        for package in package_name:
            if type(package) != str:
                raise TypeError("Expected string or list of strings")
            cmd += ' ' + package

    lowlevel_warning("externals wants to install package(s) '%s'" %
                     package_name)
    sucmd = "sudo %s" % cmd

    result = os.system(sucmd)

    return (result == 0) # 0 indicates success

def linux_fedora_install(package_name):
    cmd = 'yum -y install'

    if type(package_name) == str:
        cmd += ' ' + package_name
    elif type(package_name) == list:
        for package in package_name:
            if type(package) != str:
                raise TypeError("Expected string or list of strings")
            cmd += ' ' + package

    lowlevel_warning("externals wants to install package(s) '%s'" %
                     package_name)
    sucmd = "su -c'%s'" % cmd

    result = os.system(sucmd)

    return (result == 0)

def linux_install(dependency_dictionary):
    """Tries to import a python module. If unsuccessful, tries to install
the appropriate bundle and then reimport. py_import tries to be smart
about which system it runs on."""

    # Ugly fix to avoid circular import
    distro = guess_system()
    if not dependency_dictionary.has_key(distro):
        return False
    else:
        files = dependency_dictionary[distro]
        if files and show_question(files):
            callable_ = globals()[distro.replace('-', '_') + '_install']
            return callable_(files)
        else:
            return False

# TODO: work this out...
def windows_install(dependency_dictionary):
    return False

### END of VisTrails inspired and copied code   ### ### ### ### ### ### ### ###


def download_install(package, module, path):
    if package:
        lowlevel_warning(u'Download package "%s" from %s'
                         % (module, package['url']))
        import mimetypes, urllib2
        for i in range(3):
            response = urllib2.urlopen(package['url'])
            #response = http.request(pywikibot.getSite(), package['url'],
            #                        no_hostname = True, back_response = True)[0]
            if 'Content-Length' in response.headers:
                break
            lowlevel_warning(u'Could not retrieve data, re-trying ...')
        lowlevel_warning(u'Size of download: %s byte(s)'
                         % response.headers['Content-Length'])
        #mime = response.headers['Content-Type'].lower().split('/')
        mime = mimetypes.guess_type(package['url'], strict=True)[0].lower().split('/')
        lowlevel_warning(u'MIME type: %s' % mime)

        lowlevel_warning(u'Extract package "%s" to %s.'
                         % (module, os.path.join(path, module)))
        if len(mime) > 1:
            if   mime[1] == 'zip':
                import zipfile, StringIO
                arch = zipfile.ZipFile(StringIO.StringIO(response.read()))
            elif mime[1] == 'x-tar':
                import tarfile, StringIO
                arch = tarfile.open(fileobj=StringIO.StringIO(response.read()))
            arch.extractall(os.path.join(path, '__setup_tmp/'))
            arch.close()
            import shutil
            shutil.move(os.path.join(path, '__setup_tmp/', package['path']),
                        os.path.join(path, module))
            shutil.rmtree(os.path.join(path, '__setup_tmp/'))

            result = 0
            if 'patch' in package:
                lowlevel_warning(u'Install package "%s" by applying patch to %s.'
                                 % (module, os.path.join(path, module)))
                cmd = 'patch -p0 -d %s < %s' % (path, os.path.join(path, package['patch']))
                #os.chdir(path)
                #cmd = 'python patch.py -p0 -- < %s' % os.path.join(path, package['patch'])
                result = os.system(cmd)

            lowlevel_warning(u'Package "%s" installed to %s.'
                             % (module, os.path.join(path, module)))
            return (result == 0)

    return False

def mercurial_repo_install(package, module, path):
    if package:
        cmd = 'hg clone'
    
        lowlevel_warning(u'Mercurial clone "%s" from %s'
                         % (module, package['url']))
        cmd += " -r %s %s %s" % (package['rev'], package['url'],
                                 os.path.join(path, module))
    
        result = os.system(cmd)
    
        return (result == 0)

    return False


def check_setup(m):
    path = os.path.dirname(os.path.abspath(os.path.join(os.curdir, __file__)))
    mf = os.path.join(path, m)

    # search missing module
    if python_module_exists(m):
        return
    if os.path.exists(mf):
        return

    # install the missing module
    dist = guess_system().split(u'-')
    if globals()[dist[0] + '_install'](modules_needed[m][0]):
        return
    if download_install(modules_needed[m][1], m, path):
        return
    if mercurial_repo_install(modules_needed[m][2], m, path):
        return

    pywikibot.error(u'Package "%s" could not be found nor installed!' % m) 

def check_setup_all():
    #for m in modules_needed:
    for m in modules_order:
        check_setup(m)


#check_setup_all()
#check_setup('patch.py')
