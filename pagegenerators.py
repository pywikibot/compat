#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
This module offers a wide variety of page generators. A page generator is an
object that is iterable (see http://www.python.org/dev/peps/pep-0255/ ) and
that yields page objects on which other scripts can then work.

In general, there is no need to run this script directly. It can, however,
be run for testing purposes. It will then print the page titles to standard
output.

These parameters are supported to specify which pages titles to print:

&params;
"""
__version__='$Id$'

parameterHelp = """\
-cat              Work on all pages which are in a specific category.
                  Argument can also be given as "-cat:categoryname".

-uncat            Work on all pages which are not categorised.

-uncatcat         Work on all categories which are not categorised.

-uncatfiles       Work on all files which are not categorised.

-file             Read a list of pages to treat from the named text file.
                  Page titles in the file must be enclosed with [[brackets]]. 
                  Argument can also be given as "-file:filename".

-filelinks        Work on all pages that use a certain image/media file.
                  Argument can also be given as "-file:filename".

-yahoo            Work on all pages that are found in a Yahoo search.
                  Depends on python module pYsearch.  See yahoo_appid in
                  config.py for instructions.

-search           Work on all pages that are found in a MediaWiki search
                  across all namespaces.

-google           Work on all pages that are found in a Google search.
                  You need a Google Web API license key. Note that Google
                  doesn't give out license keys anymore. See google_key in
                  config.py for instructions.
                  Argument can also be given as "-google:searchstring".

-interwiki        Work on the given page and all equivalent pages in other
                  languages. This can, for example, be used to fight
                  multi-site spamming.
                  Attention: this will cause the bot to modify
                  pages on several wiki sites, this is not well tested,
                  so check your edits!

-links            Work on all pages that are linked from a certain page.
                  Argument can also be given as "-links:linkingpagetitle".

-new              Work on the 60 newest pages. If given as -new:x, will work
                  on the x newest pages.

-ref              Work on all pages that link to a certain page.
                  Argument can also be given as "-ref:referredpagetitle".

-start            Specifies that the robot should go alphabetically through
                  all pages on the home wiki, starting at the named page.
                  Argument can also be given as "-start:pagetitle"

-prefixindex      Work on pages commencing with a common prefix.  Argument
                  may also be given as "-prefixindex:namespace:pagename".

-subcat           Like -cat, but also includes pages in subcategories of the
                  given category.
                  Argument can also be given as "-subcat:categoryname".

-transcludes      Work on all pages that use a certain template.
                  Argument can also be given as "-transcludes:Template:Title".

-unusedfiles      Work on all description pages of images/media files that are
                  not used anywhere.
                  Argument can be given as "-unusedfiles:n" where
                  n is the maximum number of articles to work on.

-unwatched        Work on all articles that are not watched by anyone.
                  Argument can be given as "-unwatched:n" where
                  n is the maximum number of articles to work on.

-weblink          Work on all articles that contain an external link to
                  a given URL; may be given as "-weblink:url"

-withoutinterwiki Work on all pages that don't have interlanguage links.
                  Argument can be given as "-withoutinterwiki:n" where
                  n is some number (??).
"""



docuReplacements = {
    '&params;': parameterHelp
}


# Standard library imports
import re, codecs, sys
import threading, Queue
import urllib, urllib2, time

# Application specific imports
import wikipedia, date, catlib
import config

def AllpagesPageGenerator(start ='!', namespace = None, includeredirects = True):
    """
    Using the Allpages special page, retrieve all articles' titles, and yield
    page objects.
    If includeredirects is False, redirects are not included. If
    includeredirects equals the string 'only', only redirects are added.
    """
    if namespace==None:
        namespace = wikipedia.Page(wikipedia.getSite(), start).namespace()
    title = wikipedia.Page(wikipedia.getSite(), start).titleWithoutNamespace()
    for page in wikipedia.getSite().allpages(start=title, namespace=namespace, includeredirects = includeredirects):
        yield page

def PrefixingPageGenerator(prefix, namespace=None, includeredirects=True):
    for page in AllpagesPageGenerator(prefix, namespace, includeredirects):
        if page.titleWithoutNamespace().startswith(prefix):
            yield page
        else:
            break

def NewpagesPageGenerator(number = 100, get_redirect = False, repeat = False, site = None):
    if site is None:
        site = wikipedia.getSite()
    for page in site.newpages(number=number, get_redirect=get_redirect, repeat=repeat):
        yield page[0]

def FileLinksGenerator(referredImagePage):
    for page in referredImagePage.usingPages():
        yield page

def ImagesPageGenerator(pageWithImages):
    for page in pageWithImages.imagelinks(followRedirects = False, loose = True):
        yield page

def UnusedFilesGenerator(number = 100, repeat = False, site = None, extension = None):
    if site is None:
        site = wikipedia.getSite()
    for page in site.unusedfiles(number=number, repeat=repeat, extension=extension):
        yield wikipedia.ImagePage(page.site(), page.title())

def WithoutInterwikiPageGenerator(number = 100, repeat = False, site = None):
    if site is None:
        site = wikipedia.getSite()
    for page in site.withoutinterwiki(number=number, repeat=repeat):
        yield page

def InterwikiPageGenerator(page):
    yield page
    for iwPage in page.interwiki():
        yield iwPage

def ReferringPageGenerator(referredPage, followRedirects=False,
                           withTemplateInclusion=True,
                           onlyTemplateInclusion=False):
    '''Yields all pages referring to a specific page.'''
    for page in referredPage.getReferences(followRedirects,
                                           withTemplateInclusion,
                                           onlyTemplateInclusion):
        yield page

def CategorizedPageGenerator(category, recurse=False, start=None):
    '''
    Yields all pages in a specific category.

    If recurse is True, pages in subcategories are included as well; if
    recurse is an int, only subcategories to that depth will be included
    (e.g., recurse=2 will get pages in subcats and sub-subcats, but will
    not go any further).
    If start is a string value, only pages whose title comes after start
    alphabetically are included.
    '''
    for page in category.articles(recurse = recurse, startFrom = start):
        if page.title() >= start:
            yield page

def SubCategoriesPageGenerator(category, recurse=False):
    '''
    Yields all subcategories in a specific category.

    If recurse is True, pages in subcategories are included as well; if
    recurse is an int, only subcategories to that depth will be included
    (e.g., recurse=2 will get pages in subcats and sub-subcats, but will
    not go any further).
    '''
    for page in category.subcategories(recurse = recurse):
        yield page

def UnCategorizedCategoryGenerator(number = 100, repeat = False, site = None):
    if site is None:
        site = wikipedia.getSite()
    for page in site.uncategorizedcategories(number=number, repeat=repeat):
        yield page

def UnCategorizedImageGenerator(number = 100, repeat = False, site = None):
    if site is None:
        site = wikipedia.getSite()
    for page in site.uncategorizedimages(number=number, repeat=repeat):
        yield page

def NewimagesPageGenerator(number = 100, repeat = False, site = None):
    if site is None:
        site = wikipedia.getSite()
    for page in site.newimages(number, repeat=repeat):
        yield page[0]

def UnCategorizedPageGenerator(number = 100, repeat = False, site = None):
    if site is None:
        site = wikipedia.getSite()
    for page in site.uncategorizedpages(number=number, repeat=repeat):
        yield page

def LonelyPagesPageGenerator(number = 100, repeat = False, site = None):
    if site is None:
        site = wikipedia.getSite()
    for page in site.lonelypages(number=number, repeat=repeat):
        yield page

def UnwatchedPagesPageGenerator(number = 100, repeat = False, site = None):
    if site is None:
        site = wikipedia.getSite()
    for page in site.unwatchedpages(number=number, repeat=repeat):
        yield page

def AncientPagesPageGenerator(number = 100, repeat = False, site = None):
    if site is None:
        site = wikipedia.getSite()
    for page in site.ancientpages(number=number, repeat=repeat):
        yield page[0]

def DeadendPagesPageGenerator(number = 100, repeat = False, site = None):
    if site is None:
        site = wikipedia.getSite()
    for page in site.deadendpages(number=number, repeat=repeat):
        yield page

def LongPagesPageGenerator(number = 100, repeat = False, site = None):
    if site is None:
        site = wikipedia.getSite()
    for page in site.longpages(number=number, repeat=repeat):
        yield page[0]

def ShortPagesPageGenerator(number = 100, repeat = False, site = None):
    if site is None:
        site = wikipedia.getSite()
    for page in site.shortpages(number=number, repeat=repeat):
        yield page[0]

def LinkedPageGenerator(linkingPage):
    """Yields all pages linked from a specific page."""
    for page in linkingPage.linkedPages():
        yield page

def TextfilePageGenerator(filename=None):
    '''
    Read a file of page links between double-square-brackets, and return
    them as a list of Page objects. filename is the name of the file that
    should be read. If no name is given, the generator prompts the user.
    '''
    if filename is None:
        filename = wikipedia.input(u'Please enter the filename:')
    site = wikipedia.getSite()
    f = codecs.open(filename, 'r', config.textfile_encoding)
    R = re.compile(ur'\[\[(.+?)(?:\]\]|\|)') # title ends either before | or before ]]
    for pageTitle in R.findall(f.read()):
        site = wikipedia.getSite()
        # If the link doesn't refer to this site, the Page constructor
        # will automatically choose the correct site.
        # This makes it possible to work on different wikis using a single
        # text file, but also could be dangerous because you might
        # inadvertently change pages on another wiki!
        yield wikipedia.Page(site, pageTitle)
    f.close()

def PagesFromTitlesGenerator(iterable):
    """Generates pages from the titles (unicode strings) yielded by iterable"""
    for title in iterable:
        if not isinstance(title, basestring):
            break
        yield wikipedia.Page(wikipedia.getSite(), title)

def LinksearchPageGenerator(link, step=500, site = None):
    """Yields all pages that include a specified link, according to
    [[Special:Linksearch]].
    Retrieves in chunks of size "step" (default 500).
    Does not guarantee that resulting pages are unique.
    """
    if site is None:
        site = wikipedia.getSite()
    elRX = re.compile('<a .* class="external ?" .*</a>.*<a .*>(.*)</a>') #TODO: de-uglify?
    offset = 0
    pageyeldlist = list()
    found = step
    while found == step:
        found = 0
        url = site.linksearch_address(link,limit=step,offset=offset)
        wikipedia.output(u'Querying [[Special:Linksearch]]...')
        data = site.getUrl(url)
        for elM in elRX.finditer(data):
            found += 1
            pagenameofthelink = elM.group(1)
            if pagenameofthelink in pageyeldlist:
                continue
            else:
                pageyeldlist.append(pagenameofthelink)
                yield wikipedia.Page(site, pagenameofthelink)
        offset += step

def SearchPageGenerator(query, number = 100, namespaces = None, site = None):
    """
    Provides a list of results using the internal MediaWiki search engine
    """
    if site is None:
        site = wikipedia.getSite()
    for page in site.search(query, number=number, namespaces = namespaces):
        yield page[0]

class YahooSearchPageGenerator:
    '''
    To use this generator, install pYsearch
    '''
    def __init__(self, query = None, count = 100): # values larger than 100 fail
        self.query = query or wikipedia.input(u'Please enter the search query:')
        self.count = count;

    def queryYahoo(self, query):
       from yahoo.search.web import WebSearch
       srch = WebSearch(config.yahoo_appid, query=query, results=self.count)

       dom = srch.get_results()
       results = srch.parse_results(dom)
       for res in results:
           url = res.Url
           yield url

    def __iter__(self):
        site = wikipedia.getSite()
        # restrict query to local site
        localQuery = '%s site:%s' % (self.query, site.hostname())
        base = 'http://%s%s' % (site.hostname(), site.nice_get_address(''))
        for url in self.queryYahoo(localQuery):
            if url[:len(base)] == base:
                title = url[len(base):]
                page = wikipedia.Page(site, title)
                yield page

class GoogleSearchPageGenerator:
    '''
    To use this generator, you must install the pyGoogle module from
    http://pygoogle.sf.net/ and get a Google Web API license key from
    http://www.google.com/apis/index.html . The google_key must be set to your
    license key in your configuration.
    '''
    def __init__(self, query = None):
        self.query = query or wikipedia.input(u'Please enter the search query:')

    #########
    # partially commented out because it is probably not in compliance with Google's "Terms of
    # service" (see 5.3, http://www.google.com/accounts/TOS?loc=US)
    def queryGoogle(self, query):
        #if config.google_key:
        if True:
            #try:
                for url in self.queryViaSoapApi(query):
                    yield url
                return
            #except ImportError:
                #pass
        # No google license key, or pygoogle not installed. Do it the ugly way.
        #for url in self.queryViaWeb(query):
        #    yield url

    def queryViaSoapApi(self, query):
        import google
        google.LICENSE_KEY = config.google_key
        offset = 0
        estimatedTotalResultsCount = None
        while not estimatedTotalResultsCount or offset < estimatedTotalResultsCount:
            while (True):
                # Google often yields 502 errors.
                try:
                    wikipedia.output(u'Querying Google, offset %i' % offset)
                    data = google.doGoogleSearch(query, start = offset, filter = False)
                    break
                except:
                    # SOAPpy.Errors.HTTPError or SOAP.HTTPError (502 Bad Gateway)
                    # can happen here, depending on the module used. It's not easy
                    # to catch this properly because pygoogle decides which one of
                    # the soap modules to use.
                    wikipedia.output(u"An error occured. Retrying in 10 seconds...")
                    time.sleep(10)
                    continue

            for result in data.results:
                #print 'DBG: ', result.URL
                yield result.URL
            # give an estimate of pages to work on, but only once.
            if not estimatedTotalResultsCount:
                wikipedia.output(u'Estimated total result count: %i pages.' % data.meta.estimatedTotalResultsCount)
            estimatedTotalResultsCount = data.meta.estimatedTotalResultsCount
            #print 'estimatedTotalResultsCount: ', estimatedTotalResultsCount
            offset += 10

    #########
    # commented out because it is probably not in compliance with Google's "Terms of
    # service" (see 5.3, http://www.google.com/accounts/TOS?loc=US)

    #def queryViaWeb(self, query):
        #"""
        #Google has stopped giving out API license keys, and sooner or later
        #they will probably shut down the service.
        #This is a quick and ugly solution: we just grab the search results from
        #the normal web interface.
        #"""
        #linkR = re.compile(r'<a href="([^>"]+?)" class=l>', re.IGNORECASE)
        #offset = 0

        #while True:
            #wikipedia.output("Google: Querying page %d" % (offset / 100 + 1))
            #address = "http://www.google.com/search?q=%s&num=100&hl=en&start=%d" % (urllib.quote_plus(query), offset)
            ## we fake being Firefox because Google blocks unknown browsers
            #request = urllib2.Request(address, None, {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; de; rv:1.8) Gecko/20051128 SUSE/1.5-0.1 Firefox/1.5'})
            #urlfile = urllib2.urlopen(request)
            #page = urlfile.read()
            #urlfile.close()
            #for url in linkR.findall(page):
                #yield url
            #if "<div id=nn>" in page: # Is there a "Next" link for next page of results?
                #offset += 100  # Yes, go to next page of results.
            #else:
                #return
    #########

    def __iter__(self):
        site = wikipedia.getSite()
        # restrict query to local site
        localQuery = '%s site:%s' % (self.query, site.hostname())
        base = 'http://%s%s' % (site.hostname(), site.nice_get_address(''))
        for url in self.queryGoogle(localQuery):
            if url[:len(base)] == base:
                title = url[len(base):]
                page = wikipedia.Page(site, title)
                yield page

def MySQLPageGenerator(query):
    '''

    '''
    import MySQLdb as mysqldb
    site = wikipedia.getSite()
    conn = mysqldb.connect(config.db_hostname, db = site.dbName(),
                           user = config.db_username,
                           passwd = config.db_password)
    cursor = conn.cursor()
    wikipedia.output(u'Executing query:\n%s' % query)
    query = query.encode(site.encoding())
    cursor.execute(query)
    while True:
        try:
            namespaceNumber, pageName = cursor.fetchone()
            print namespaceNumber, pageName
        except TypeError:
            # Limit reached or no more results
            break
        #print pageName
        if pageName:
            namespace = site.namespace(namespaceNumber)
            pageName = unicode(pageName, site.encoding())
            if namespace:
                pageTitle = '%s:%s' % (namespace, pageName)
            else:
                pageTitle = pageName
            page = wikipedia.Page(site, pageTitle)
            yield page

def YearPageGenerator(start = 1, end = 2050):
    wikipedia.output(u"Starting with year %i" % start)
    for i in xrange(start, end + 1):
        if i % 100 == 0:
            wikipedia.output(u'Preparing %i...' % i)
        # There is no year 0
        if i != 0:
            current_year = date.formatYear(wikipedia.getSite().lang, i )
            yield wikipedia.Page(wikipedia.getSite(), current_year)

def DayPageGenerator(startMonth=1, endMonth=12):
    fd = date.FormatDate(wikipedia.getSite())
    firstPage = wikipedia.Page(wikipedia.getSite(), fd(startMonth, 1))
    wikipedia.output(u"Starting with %s" % firstPage.aslink())
    for month in xrange(startMonth, endMonth+1):
        for day in xrange(1, date.getNumberOfDaysInMonth(month)+1):
            yield wikipedia.Page(wikipedia.getSite(), fd(month, day))

def NamespaceFilterPageGenerator(generator, namespaces):
    """
    Wraps around another generator. Yields only those pages that are in one
    of the given namespaces.

    The namespace list can contain both integers (namespace numbers) and
    strings/unicode strings (namespace names).
    """
    # convert namespace names to namespace numbers
    for i in xrange(len(namespaces)):
        ns = namespaces[i]
        if isinstance(ns, unicode) or isinstance(ns, str):
            index = wikipedia.getSite().getNamespaceIndex(ns)
            if index is None:
                raise ValueError(u'Unknown namespace: %s' % ns)
            namespaces[i] = index
    for page in generator:
        if page.namespace() in namespaces:
            yield page

def RedirectFilterPageGenerator(generator):
    """
    Wraps around another generator. Yields only those pages that are not redirects.
    """
    for page in generator:
        if not page.isRedirectPage():
            yield page

def DuplicateFilterPageGenerator(generator):
    """
    Wraps around another generator. Yields all pages, but prevents
    duplicates.
    """
    seenPages = []
    for page in generator:
        if page not in seenPages:
            seenPages.append(page)
            yield page

def RegexFilterPageGenerator(generator, regex):
    """
    Wraps around another generator. Yields only thos pages, which titles are positively
    matched to regex.
    """
    reg = re.compile(regex, re.I)

    for page in generator:
	if reg.match(page.titleWithoutNamespace()):
            yield page

def CombinedPageGenerator(generators):
    """
    Wraps around a list of other generators. Yields all pages generated by the
    first generator; when the first generator stops yielding pages, yields those
    generated by the second generator, etc.
    """
    for generator in generators:
        for page in generator:
            yield page

def CategoryGenerator(generator):
    """
    Wraps around another generator. Yields the same pages, but as Category
    objects instead of Page objects. Makes sense only if it is ascertained
    that only categories are being retrieved.
    """
    for page in generator:
        yield catlib.Category(page.site(), page.title())

def PageWithTalkPageGenerator(generator):
    """
    Wraps around another generator. Yields the same pages, but for non-talk pages, it
    also includes associated talk pages.
    This generator does not check if the talk page in fact exists.
    """
    for page in generator:
        yield page
        if not page.isTalkPage():
            yield page.toggleTalkPage()

class _Preloader(threading.Thread):
    def __init__(self, queue, generator, pageNumber):
        threading.Thread.__init__(self)
        self.queue = queue
        self.generator = generator
        self.pageNumber = pageNumber
        # identification for debugging purposes
        self.setName('Preloader-Thread')
        # This thread dies when the main program terminates
        self.setDaemon(True)

    def preload(self, pages):
        try:
            while len(pages) > 0:
                # It might be that the pages are on different sites,
                # e.g. because the -interwiki parameter was used.
                # Query the sites one by one.
                site = pages[0].site()
                pagesThisSite = [page for page in pages if page.site() == site]
                pages = [page for page in pages if page.site() != site]
                wikipedia.getall(site, pagesThisSite, throttle=False)
                for page in pagesThisSite:
                    yield page
        except IndexError:
            # Can happen if the pages list is empty. Don't care.
            pass
        except wikipedia.SaxError:
            # Ignore this error, and get the pages the traditional way later.
            pass

    def run(self):
        try:
            # this array will contain up to pageNumber pages and will be flushed
            # after these pages have been preloaded and yielded.
            somePages = []
            for page in self.generator:
                somePages.append(page)
                # We don't want to load too many pages at once using XML export.
                # We only get a maximum number at a time.
                if len(somePages) >= self.pageNumber:
                    for refpage in self.preload(somePages):
                        self.queue.put(refpage)
                    somePages = []
            if somePages:
                # preload remaining pages
                for refpage in self.preload(somePages):
                    self.queue.put(refpage)
            self.queue.put(None)    # to signal end of list
        except Exception, e:
            wikipedia.output(str(e))
            self.queue.put(None)    # to signal end of list

def PreloadingGenerator(generator, pageNumber=60):
    """
    Yields the same pages as generator generator. Retrieves 60 pages (or
    another number specified by pageNumber), loads them using
    Special:Export, and yields them one after the other. Then retrieves more
    pages, etc. Thus, it is not necessary to load each page separately.
    Operates asynchronously, so the next batch of pages is loaded in the
    background before the first batch is fully consumed.
    """
    if pageNumber < 2:
        raise ValueError("PreloadingGenerator needs to load more than 1 page.")
    pagequeue = Queue.Queue(min(pageNumber//2, 10))
    # Note: queue size will determine how quickly the Preloader goes back for
    # more pages. If the queue size is unlimited, it will preload all pages
    # before yielding any of them to the consumer. If the queue size is small,
    # it will wait until most pages have been yielded before preloading the
    # next batch. This value tries to strike a compromise, but may need
    # adjustment based upon experience.
    preloader = _Preloader(pagequeue, generator, pageNumber)
    preloader.start()
    while True:
        # Queue.get() blocks the main thread. This means that the
        # program wouldn't react to CTRL-C while it is waiting for
        # a queue element.
        # Thus, there is a timeout to the blocking, so that Python
        # can check once a second if there is a KeyboardInterrupt.
        try:
            p = pagequeue.get(timeout = 1)
        except Queue.Empty:
            # This is expected. Keep waiting.
            continue
        if p is None:
            return
        yield p

class GeneratorFactory:
    """
    This factory is responsible for processing command line arguments
    that are used by many scripts and that determine on which pages
    to work on.
    """
    def __init__(self):
        pass

    def setCategoryGen(self, arg, length, recurse = False):
        if len(arg) == length:
            categoryname = wikipedia.input(u'Please enter the category name:')
        else:
            categoryname = arg[length + 1:]

        ind = categoryname.find('|')
        if ind > 0:
            startfrom = categoryname[ind + 1:]
            categoryname = categoryname[:ind]
        else:
            startfrom = None

        cat = catlib.Category(wikipedia.getSite(), 'Category:%s' % categoryname)
        return CategorizedPageGenerator(cat, start = startfrom, recurse = recurse)

    def handleArg(self, arg):
        gen = None
        if arg.startswith('-filelinks'):
            fileLinksPageTitle = arg[11:]
            if not fileLinksPageTitle:
                fileLinksPageTitle = wikipedia.input(u'Links to which image page should be processed?')
            if fileLinksPageTitle.startswith(wikipedia.getSite().namespace(6) + ":"):
                fileLinksPage = wikipedia.ImagePage(wikipedia.getSite(),
                                                    fileLinksPageTitle)
            else:
                fileLinksPage = wikipedia.ImagePage(wikipedia.getSite(),
                                                'Image:' + fileLinksPageTitle)
            gen = FileLinksGenerator(fileLinksPage)
        elif arg.startswith('-unusedfiles'):
            if len(arg) == 12:
                gen = UnusedFilesGenerator()
            else:
                gen = UnusedFilesGenerator(number = int(arg[13:]))
        elif arg.startswith('-unwatched'):
            if len(arg) == 10:
                gen = UnwatchedPagesPageGenerator()
            else:
                gen = UnwatchedPagesPageGenerator(number = int(arg[11:]))
        elif arg.startswith('-withoutinterwiki'):
            if len(arg) == 17:
                gen = WithoutInterwikiPageGenerator()
            else:
                gen = WithoutInterwikiPageGenerator(number = int(arg[18:]))
        elif arg.startswith('-interwiki'):
            title = arg[11:]
            if not title:
                title = wikipedia.input(u'Which page should be processed?')
            page = wikipedia.Page(wikipedia.getSite(), title)
            gen = InterwikiPageGenerator(page)
        elif arg.startswith('-file'):
            textfilename = arg[6:]
            if not textfilename:
                textfilename = wikipedia.input(u'Please enter the local file name:')
            gen = TextfilePageGenerator(textfilename)
        elif arg.startswith('-cat'):
            gen = self.setCategoryGen(arg, 4)
        elif arg.startswith('-uncatfiles'):
            gen = UnCategorizedImageGenerator()
        elif arg.startswith('-uncatcat'):
            gen = UnCategorizedCategoryGenerator()
        elif arg.startswith('-uncat'):
            gen = UnCategorizedPageGenerator()
        elif arg.startswith('-subcat'):
            gen = self.setCategoryGen(arg, 7, recurse = True)
        elif arg.startswith('-ref'):
            referredPageTitle = arg[5:]
            if not referredPageTitle:
                referredPageTitle = wikipedia.input(u'Links to which page should be processed?')
            referredPage = wikipedia.Page(wikipedia.getSite(), referredPageTitle)
            gen = ReferringPageGenerator(referredPage)
        elif arg.startswith('-links'):
            linkingPageTitle = arg[7:]
            if not linkingPageTitle:
                linkingPageTitle = wikipedia.input(u'Links from which page should be processed?')
            linkingPage = wikipedia.Page(wikipedia.getSite(), linkingPageTitle)
            gen = LinkedPageGenerator(linkingPage)
        elif arg.startswith('-weblink'):
            url = arg[9:]
            if not url:
                url = wikipedia.input(u'Pages with which weblink should be processed?')
            gen = LinksearchPageGenerator(url)
        elif arg.startswith('-transcludes'):
            transclusionPageTitle = arg[len('-transcludes:'):]
            if not transclusionPageTitle:
                transclusionPageTitle = wikipedia.input(u'Pages that transclude which page should be processed?')
            transclusionPage = wikipedia.Page(wikipedia.getSite(), 'Template:%s' % transclusionPageTitle)
            gen = ReferringPageGenerator(transclusionPage, onlyTemplateInclusion = True)
        elif arg.startswith('-start'):
            firstPageTitle = arg[7:]
            if not firstPageTitle:
                firstPageTitle = wikipedia.input(u'At which page do you want to start?')
            namespace = wikipedia.Page(wikipedia.getSite(), firstPageTitle).namespace()
            firstPageTitle = wikipedia.Page(wikipedia.getSite(), firstPageTitle).titleWithoutNamespace()
            gen = AllpagesPageGenerator(firstPageTitle, namespace, includeredirects = False)
        elif arg.startswith('-prefixindex'):
            prefix = arg[13:]
            namespace = None
            if not prefix:
                prefix = wikipedia.input(u'What page names are you looking for?')
            colon = prefix.find(':')
            if colon > 0:
                namespace = wikipedia.getSite().getNamespaceIndex(prefix[0:colon])
                # If the text before the colon is a valid namespace that
                # that is not the main namespace, use the remainder.
                if namespace:
                    prefix = prefix[colon+1:]
            gen = PrefixingPageGenerator(prefix = prefix, namespace = namespace)
        elif arg.startswith('-newimages'):
            limit = arg[11:] or wikipedia.input(u'How many images do you want to load?')
            gen = NewimagesPageGenerator(number = int(limit))
        elif arg.startswith('-new'):
            if len(arg) >=5:
              gen = NewpagesPageGenerator(number = int(arg[5:]))
            else:
              gen = NewpagesPageGenerator(number = 60)
        elif arg.startswith('-search'):
            mediawikiQuery = arg[8:]
            if not mediawikiQuery:
                mediawikiQuery = wikipedia.input(u'What do you want to search for?')
            # In order to be useful, all namespaces are required
            gen = SearchPageGenerator(mediawikiQuery, namespaces = [])
        elif arg.startswith('-google'):
            gen = GoogleSearchPageGenerator(arg[8:])
        elif arg.startswith('-regex'):
            if len(arg) == 6:
                regex = wikipedia.input(u'What page names are you looking for?')
            else:
                regex = arg[7:]
            gen = RegexFilterPageGenerator(wikipedia.getSite().allpages(), regex)
        elif arg.startswith('-yahoo'):
            gen = YahooSearchPageGenerator(arg[7:])
        else:
            return None
        # make sure all yielded pages are unique
        gen = DuplicateFilterPageGenerator(gen)
        return gen

if __name__ == "__main__":
    try:
        gen = None
        genFactory = GeneratorFactory()
        for arg in wikipedia.handleArgs():
            generator = genFactory.handleArg(arg)
            if generator:
                gen = generator
        if gen:
            for page in gen:
                wikipedia.output(page.title(), toStdout = True)
        else:
            wikipedia.showHelp('pagegenerators')
    finally:
        wikipedia.stopme()
