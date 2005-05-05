#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
Nifty script to convert HTML-tables to Wikipedia's syntax.


-file:filename
      will read any [[wikipedia link]] and use these articles

-sql:XYZ
      reads a local SQL cur dump, available at http://download.wikimedia.org/.
      Searches for pages with HTML tables, and tries to convert them on the live
      wiki. Example:
      python table2wiki.py -sql:20040711_cur_table.sql.sql -lang:de

SQL-Query

SELECT CONCAT('[[', cur_title, ']]')
       FROM cur
       WHERE (cur_text LIKE '%<table%'
         OR cur_text LIKE '%<TABLE%')
         AND cur_title REGEXP "^[A-N]"
         AND cur_namespace=0
       ORDER BY cur_title
       LIMIT 500


FEATURES
Save against missing </td>
Corrects attributes of tags

KNOWN BUGS
Broken HTML-tables will most likely result in broken wiki-tables!
Please check every article you change.


"""

# (C) 2003 Thomas R. Koll, <tomk32@tomk32.de>
#
# Distribute under the terms of the PSF license.
__version__='$Id$'

import re,sys,wikipedia,config,time

msg_no_warnings = {'de':'Bot: Tabellensyntax konvertiert',
                   'en':'User-controlled Bot: table syntax updated',
                   'es':'Bot controlado: actualizada sintaxis de tabla',
                   'nl':'Tabel gewijzigd van HTML- naar Wikisyntax',
                   'pt':'Bot: Sintaxe da tabela HTML para Wiki atualizada',
                  }

msg_one_warning = {'de':'Bot: Tabellensyntax konvertiert - %d Warnung!',
                   'en':'User-controlled Bot: table syntax updated - %d warning!',
                   'es':'Bot controlado: actualizada sintaxis de tabla - %d aviso!',
                   'nl':'Tabel gewijzigd van HTML- naar Wikisyntax - %d waarschuwing!',
                   'pt':'Bot: Sintaxe da tabela HTML para Wiki atualizada - %d aviso',
                  }

msg_multiple_warnings = {'de':'Bot: Tabellensyntax konvertiert - %d Warnungen!',
                         'en':'User-controlled Bot: table syntax updated - %d warnings!',
                         'es':'Bot controlado: actualizada sintaxis de tabla - %d avisos!',
                         'nl':'Tabel gewijzigd van HTML- naar Wikisyntax - %d waarschuwingen!',
                         'pt':'Bot: Sintaxe da tabela HTML para Wiki atualizada - %d avisos',
                        }

class TableSqlDumpGenerator:
    def __init__(self, sqlfilename):
        import sqldump
        self.sqldump = sqldump.SQLdump(sqlfilename, wikipedia.myencoding())

    def generate(self):
        tableTagR = re.compile('<table', re.IGNORECASE)
        for entry in self.sqldump.entries():
            if tableTagR.search(entry.text):
                pl = wikipedia.PageLink(wikipedia.getSite(), entry.full_title())
                yield pl

class SinglePageGenerator:
    '''Pseudo-generator'''
    def __init__(self, pl):
        self.pl = pl
    
    def generate(self):
        yield self.pl


class PreloadingGenerator:
    """
    Wraps around another generator. Retrieves up to 20 pages from that
    generator, loads them using Special:Export, and yields them one after
    the other. Then retrieves 20 more pages, etc.
    """
    def __init__(self, generator):
        self.generator = generator

    def preload(self, pages):
        try:
            wikipedia.getall(wikipedia.getSite(), pages, throttle=False)
        except wikipedia.SaxError:
            # Ignore this error, and get the pages the traditional way later.
            pass
        
    def generate(self):
        # this array will contain up to 20 pages and will be flushed
        # after these pages have been preloaded.
        somePages = []
        i = 0
        for pl in self.generator.generate():
            i += 1
            somePages.append(pl)
            # We don't want to load too many pages at once using XML export.
            # We only get 20 at a time.
            if i >= 20:
                self.preload(somePages)
                for refpl in somePages:
                    yield refpl
                i = 0
                somePages = []
        # preload remaining pages
        self.preload(somePages)
        for refpl in somePages:
            yield refpl

                         
class Table2WikiRobot:
    def __init__(self, generator, debug = False, quietMode = False):
        self.generator = generator
        self.debug = debug
        self.quietMode = quietMode

    def convertTable(self, table):
        '''
        Converts an HTML table to wiki syntax. If the table already is a wiki
        table or contains a nested wiki table, tries to beautify it.
        Returns the converted table, the number of warnings that occured and
        a list containing these warnings.

        Hint: if you give an entire page text as a parameter instead of a table only,
        this function will convert all HTML tables and will also try to beautify all
        wiki tables already contained in the text.
        '''
        warnings = 0
        # this array will contain strings that will be shown in case of possible
        # errors, before the user is asked if he wants to accept the changes.
        warning_messages = []
        newTable = table
        ##################
        # bring every <tag> into one single line.
        num = 1
        while num != 0:
            newTable, num = re.subn("([^\r\n]{1})(<[tT]{1}[dDhHrR]{1})",
                                   r"\1\r\n\2", newTable)
            
        ##################
        # every open-tag gets a new line.
    
    
        ##################
        # <table> tag with attributes, with more table on the same line
        newTable = re.sub("[\r\n]*?<(?i)(table) ([\w\W]*?)>([\w\W]*?)[\r\n ]*",
                         r"\r\n{| \2\r\n\3", newTable)
        # <table> tag without attributes, with more table on the same line
        newTable = re.sub("[\r\n]*?<(TABLE|table)>([\w\W]*?)[\r\n ]*",
                         r"\r\n{|\n\2\r\n", newTable)
        # <table> tag with attributes, without more table on the same line
        newTable = re.sub("[\r\n]*?<(TABLE|table) ([\w\W]*?)>[\r\n ]*",
                         r"\r\n{| \2\r\n", newTable)
        # <table> tag without attributes, without more table on the same line
        newTable = re.sub("[\r\n]*?<(TABLE|table)>[\r\n ]*",
                         "\r\n{|\r\n", newTable)
        # end </table>
        newTable = re.sub("[\s]*<\/(TABLE|table)>", "\r\n|}", newTable)
        
        ##################
        # captions
        newTable = re.sub("<(CAPTION|caption) ([\w\W]*?)>([\w\W]*?)<\/caption>",
                         r"\r\n|+\1 | \2", newTable)
        newTable = re.sub("(CAPTION|caption)([\w\W]*?)<\/caption>",
                         r"\r\n|+ \1", newTable)
        
        ##################
        # <th> often people don't write them within <tr>, be warned!
        newTable = re.sub("[\r\n]+<(TH|th)([^>]*?)>([\w\W]*?)<\/(th|TH)>",
                         r"\r\n!\2 | \3\r\n", newTable)
    
        # fail save. sometimes people forget </th>
        # <th> without attributes
        newTable, n = re.subn("[\r\n]+<(th|TH)>([\w\W]*?)[\r\n]+",
                             r"\r\n! \2\r\n", newTable)
        if n>0:
            warning_messages.append(u'WARNING: found <th> without </th>. (%d occurences)\n' % n)
            warnings += n
    
        # <th> with attributes
        newTable, n = re.subn("[\r\n]+<(th|TH)([^>]*?)>([\w\W]*?)[\r\n]+",
                             r"\n!\2 | \3\r\n", newTable)
        if n>0:
            warning_messages.append(u'WARNING: found <th> without </th>. (%d occurences\n)' % n)
            warnings += n
    
    
        ##################
        # very simple <tr>
        newTable = re.sub("[\r\n]*<(tr|TR)([^>]*?)>[\r\n]*",
                         r"\r\n|-----\2\r\n", newTable)
        newTable = re.sub("[\r\n]*<(tr|TR)>[\r\n]*",
                         r"\r\n|-----\r\n", newTable)
        
        ##################
        # normal <td> without arguments
        newTable = re.sub("[\r\n]+<(td|TD)>([\w\W]*?)<\/(TD|td)>",
                         r"\r\n| \2\r\n", newTable)
    
        ##################
        # normal <td> with arguments
        newTable = re.sub("[\r\n]+<(td|TD)([^>]*?)>([\w\W]*?)<\/(TD|td)>",
                         r"\r\n|\2 | \3", newTable)
    
        # WARNING: this sub might eat cells of bad HTML, but most likely it
        # will correct errors
        # TODO: some more docu please
        newTable, n = re.subn("[\r\n]+<(td|TD)>([^\r\n]*?)<(td|TD)>",
                             r"\r\n| \2\r\n", newTable)
        if n>0:
            warning_messages.append(u'WARNING: (sorry, bot code unreadable (1). I don\'t know why this warning is given.) (%d occurences)\n' % n)
            warnings += n
        
        # fail save, sometimes it's a <td><td></tr>
        #        newTable, n = re.subn("[\r\n]+<(td|TD)>([^<]*?)<(td|TD)><\/(tr|TR)>",
        #                             "\r\n| \\2\r\n", newTable)
        #        newTable, n = re.subn("[\r\n]+<(td|TD)([^>]*?)>([^<]*?)<(td|TD)><\/(tr|TR)>",
        #                             "\r\n|\\2| \\3\r\n", newTable)
        #
        newTable, n = re.subn("[\r\n]+<(td|TD)([^>]+?)>([^\r\n]*?)<\/(td|TD)>",
                             r"\r\n|\2 | \3\r\n", newTable)
        if n>0:
            warning_messages.append(u'WARNING: found <td><td></tr>, but no </td>. (%d occurences)\n' % n)
            warnings += n
        
        # fail save. sometimes people forget </td>
        # <td> without arguments, with missing </td> 
        newTable, n = re.subn("<(td|TD)>([^<]*?)[\r\n]+",
                             r"\r\n| \2\r\n", newTable)
        if n>0:
            warning_messages.append(u'WARNING: found <td> without </td>. (%d occurences)\n' % n)
            warnings += n
    
        # <td> with arguments, with missing </td> 
        newTable, n = re.subn("[\r\n]*<(td|TD)([^>]*?)>([\w\W]*?)[\r\n]+",
                             r"\r\n|\2 | \3\r\n", newTable)
        if n > 0:
            warning_messages.append(u'NOTE: Found <td> without </td>. This shouldn\'t cause problems.\n')
    
        # TODO: some docu please
        newTable, n = re.subn("<(td|TD)>([\w\W]*?)[\r\n]+",
                             r"\r\n| \2\r\n", newTable)
    
        if n>0:
            warning_messages.append(u'WARNING: (sorry, bot code unreadable (2). I don\'t know why this warning is given.) (%d occurences)\n' % n)
            warnings += n
    
    
        ##################
        # Garbage collecting ;-)
        newTable = re.sub("<td>[\r\n]*<\/tr>", "", newTable)
        newTable = re.sub("[\r\n]*<\/[Tt][rRdDhH]>", "", newTable)
        
        ##################
        # OK, that's only theory but works most times.
        # Most browsers assume that <th> gets a new row and we do the same
        #        newTable, n = re.subn("([\r\n]+\|\ [^\r\n]*?)([\r\n]+\!)",
        #                             "\\1\r\n|-----\\2", newTable)
        #        warnings = warnings + n
        # adds a |---- below for the case the new <tr> is missing
        #        newTable, n = re.subn("([\r\n]+\!\ [^\r\n]*?[\r\n]+)(\|\ )",
        #                             "\\1|-----\r\n\\2", newTable)
        #        warnings = warnings + n
        
        
        ##################
        # most <th> come with '''title'''. Senseless in my eyes cuz
        # <th> should be bold anyways.
        newTable = re.sub("[\r\n]+\!([^'\n\r]*)'''([^'\r\n]*)'''",
                         r"\r\n!\1\2", newTable)
        
        ##################
        # kills indention within tables. Be warned, it might seldom bring
        # bad results.
        # True by default. Set 'deIndentTables = False' in user-config.py
        if config.deIndentTables:
            num = 1
            while num != 0:
                newTable, num = re.subn("(\{\|[\w\W]*?)\n[ \t]+([\w\W]*?\|\})",
                                       r"\1\r\n\2", newTable)
                
        ##################
        # kills additional spaces after | or ! or {|
        # This line was creating problems, so I commented it out --Daniel
        # newTable = re.sub("[\r\n]+\|[\t ]+?[\r\n]+", "\r\n| ", newTable)
        # kills trailing spaces and tabs
        newTable = re.sub("\r\n(.*)[\t\ ]+[\r\n]+",
                         r"\r\n\1\r\n", newTable)
        # kill extra new-lines
        newTable = re.sub("[\r\n]{4,}(\!|\|)",
                         r"\r\n\1", newTable);
    
    
        ##################        
        # shortening if <table> had no arguments/parameters
        newTable = re.sub("[\r\n]+\{\|[\ ]+\| ", "\r\n\{| ", newTable)
        # shortening if <td> had no articles
        newTable = re.sub("[\r\n]+\|[\ ]+\| ", "\r\n| ", newTable)
        # shortening if <th> had no articles
        newTable = re.sub("\n\|\+[\ ]+\|", "\n|+ ", newTable)
        # shortening of <caption> had no articles
        newTable = re.sub("[\r\n]+\![\ ]+\| ", "\r\n! ", newTable)
        
        ##################
        # proper attributes. attribute values need to be in quotation marks.
        num = 1
        while num != 0:
            # group 1 starts with newlines, followed by a table tag
            # (either !, |, {|, or |---), then zero or more attribute key-value
            # pairs where the value already has correct quotation marks, and
            # finally the key of the attribute we want to fix here.
            # group 3 is the value of the attribute we want to fix here.
            # We recognize it by searching for a string of non-whitespace characters
            # - [^\s]+? - which is not embraced by quotation marks - [^"]
            # group 4 is a whitespace character and probably unnecessary..
            newTable, num = re.subn(r'([\r\n]+(\!|\||\{\|)[^\r\n\|]+)[ ]*=[ ]*([^"][^\s]+?[^"])(\s)',
                                   r'\1="\3"\4', newTable, 1)
           
        ##################
        # merge two short <td>s
        num = 1
        while num != 0:
            newTable, num = re.subn("[\r\n]+(\|[^\|\-\}]{1}[^\n\r]{0,35})" +
                                   "[\r\n]+(\|[^\|\-\}]{1}[^\r\n]{0,35})[\r\n]+",
                                   r"\r\n\1 |\2\r\n", newTable)
        ####
        # add a new line if first is * or #
        newTable = re.sub("[\r\n]+\| ([*#]{1})",
                         r"\r\n|\r\n\1", newTable)
        
        ##################
        # strip <center> from <th>
        newTable = re.sub("([\r\n]+\![^\r\n]+?)<center>([\w\W]+?)<\/center>",
                         r"\1 \2", newTable)
        # strip align="center" from <th> because the .css does it
        # if there are no other attributes than align, we don't need that | either
        newTable = re.sub("([\r\n]+\! +)align\=\"center\" +\|",
                         r"\1", newTable)
        # if there are other attributes, simply strip the align="center"
        newTable = re.sub("([\r\n]+\![^\r\n\|]+?)align\=\"center\"([^\n\r\|]+?\|)",
                         r"\1 \2", newTable)
        
        ##################
        # kill additional spaces within arguments
        num = 1
        while num != 0:
            newTable, num = re.subn("[\r\n]+(\||\!)([^|\r\n]*?)[ \t]{2,}([^\r\n]+?)",
                                   r"\r\n\1\2 \3", newTable)
            
        ##################
        # I hate those long lines because they make a wall of letters
        # Off by default, set 'splitLongParagraphs = True' in user-config.py
        if config.splitLongParagraphs:
            num = 1
            while num != 0:
                # TODO: how does this work? docu please.
                # why are only äöüß used, but not other special characters?
                newTable, num = re.subn("(\r\n[A-Z]{1}[^\n\r]{200,}?[a-zäöüß]\.)\ ([A-ZÄÖÜ]{1}[^\n\r]{200,})",
                                       r"\1\r\n\2", newTable)
        # show the changes for this table
        if self.debug:
            print table
            print newTable
        elif not self.quietMode:
            wikipedia.showColorDiff(table, newTable)
        return newTable, warnings, warning_messages

    def findTable(self, text):
        """
        Finds an HTML table (which can contain nested tables) inside a text.
        Returns the table and the start and end position inside the text.
        """
        start = text.find("<table")
        if start == -1:
            return None, 0, 0
        else:
            # depth level of table nesting
            depth = 1
            i = start + 1
            while depth > 0:
                if text.find("</table>", i) == -1:
                    print "More opening than closing table tags. Skipping."
                    return None, 0, 0
                # if another table tag is opened before one is closed
                if text.find("<table", i) > -1 and  text.find("<table", i) < text.find("</table>", i):
                    i = text.find("<table", i) + 1
                    depth += 1
                else:
                    i = text.find("</table>", i) + len("</table>") + 1
                    depth -= 1
            end = i
            return text[start:end], start, end
                        
    def convertAllHTMLTables(self, text):
        '''
        Converts all HTML tables in text to wiki syntax.
        Returns the converted text, the number of converted tables and the
        number of warnings that occured.
        '''
        convertedTables = 0
        warningSum = 0
        warningMessages = u''

        while True:
            table, start, end = self.findTable(text)
            if not table:
                # no more HTML tables left
                break
            print ">> Table %i <<" % (convertedTables + 1)
            # convert the current table
            newTable, warningsThisTable, warnMsgsThisTable = self.convertTable(table)
            print ""
            warningSum += warningsThisTable
            for msg in warnMsgsThisTable:
                warningMessages += 'In table %i: %s' % (convertedTables + 1, msg)
            text = text[:start] + newTable + text[end:]
            convertedTables += 1

        wikipedia.output(warningMessages)
            
        return text, convertedTables, warningSum

    def treat(self, pl):
        '''
        Loads a page, converts all HTML tables in its text to wiki syntax,
        and saves the converted text.
        Returns True if the converted table was successfully saved, otherwise
        returns False.
        '''
        wikipedia.output(u'\n>>> %s <<<' % pl.linkname())
        site = pl.site()
        try:
            text = pl.get()
        except wikipedia.NoPage:
            wikipedia.output(u"ERROR: couldn't find %s" % pl.linkname())
            return False
        except wikipedia.LockedPage:
            wikipedia.output(u'Skipping locked page %s' % pl.linkname())
            return False
        except wikipedia.IsRedirectPage:
            wikipedia.output(u'Skipping redirect %s' % pl.linkname())
            return False
        newText, convertedTables, warningSum = self.convertAllHTMLTables(text)
        if convertedTables == 0:
            wikipedia.output(u"No changes were necessary.")
        else:
            if config.table2wikiAskOnlyWarnings and warningSum == 0:
                doUpload = True
            else:
                if config.table2wikiSkipWarnings:
                    doUpload = True
                else:
                    print "There were %i replacement(s) that might lead to bad output." % warningSum
                    doUpload = (wikipedia.input(u'Do you want to change the page anyway? [y|N]') == "y")
            if doUpload:
                # get edit summary message
                if warningSum == 0:
                    wikipedia.setAction(wikipedia.translate(site.lang, msg_no_warnings))
                elif warningSum == 1:
                    wikipedia.setAction(wikipedia.translate(site.lang, msg_one_warning) % warningSum)
                else:
                    wikipedia.setAction(wikipedia.translate(site.lang, msg_multiple_warnings) % warningSum)
                pl.put(newText)

    def run(self):
        for pl in self.generator.generate():
            self.treat(pl)
            
def main():
    quietMode = False # use -quiet to get less output
    # if the -file argument is used, page titles are stored in this array.
    # otherwise it will only contain one page.
    articles = []
    # if -file is not used, this temporary array is used to read the page title.
    page_title = []
    debug = False
    source = None
    for arg in sys.argv[1:]:
        arg = wikipedia.argHandler(arg)
        if arg:
            if arg.startswith('-file:'):
                f=open(arg[6:], 'r')
                R=re.compile(r'.*\[\[([^\]]*)\]\].*')
                m = False
                for line in f.readlines():
                    m=R.match(line)            
                    if m:
                        articles.append(m.group(1))
                    else:
                        print "ERROR: Did not understand %s line:\n%s" % (
                            arg[6:], repr(line))
                f.close()
            elif arg.startswith('-sql'):
                if len(arg) == 4:
                    sqlfilename = wikipedia.input(u'Please enter the SQL dump\'s filename: ')
                else:
                    sqlfilename = arg[5:]
                source = 'sqldump'
            elif arg.startswith('-skip:'):
                articles = articles[articles.index(arg[6:]):]
            elif arg.startswith('-auto'):
                config.table2wikiAskOnlyWarnings = True
                config.table2wikiSkipWarnings = True
                print "Automatic mode!\n"
            elif arg.startswith('-quiet'):
                quietMode = True
            elif arg.startswith('-debug'):
                debug = True
            else:
                page_title.append(arg)

    if source == 'sqldump':
        gen = PreloadingGenerator(TableSqlDumpGenerator(sqlfilename))
    # if the page is given as a command line argument,
    # connect the title's parts with spaces
    elif page_title != []:
        page_title = ' '.join(page_title)
        pl = wikipedia.PageLink(wikipedia.getSite(), page_title)
        gen = PreloadingGenerator(SinglePageGenerator(pl))
    else:
        wikipedia.output(__doc__, 'utf-8')
        sys.exit(0)

    bot = Table2WikiRobot(gen, debug, quietMode)
    bot.run()
            
try:
    main()
except:
    wikipedia.stopme()
    raise
else:
    wikipedia.stopme()
