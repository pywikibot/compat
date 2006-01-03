﻿# -*- coding: utf-8  -*-

import urllib
import family, config

__version__ = '$Id$'

# The Wikimedia family that is known as Wikipedia, the Free Encyclopedia

class Family(family.Family):
    
    def __init__(self):
        family.Family.__init__(self)
        self.name = 'wikipedia'

        self.langs = {
            'dk':'da.wikipedia.org',
            'jp':'ja.wikipedia.org',
            'minnan':'zh-min-nan.wikipedia.org',
            'nb':'no.wikipedia.org',
            'tokipona':'tokipona.wikipedia.org',
            'zh-cn':'zh.wikipedia.org',
            'zh-tw':'zh.wikipedia.org'
            }
        for lang in self.knownlanguages:
            self.langs[lang] = lang+'.wikipedia.org'

        # Most namespaces are inherited from family.Family.
        self.namespaces[4] = {
            '_default': u'Wikipedia',
            'ar': u'ويكيبيديا',
            'ast':u'Uiquipedia',
            'be': u'Вікіпэдыя',
            'bg': u'Уикипедия',
            'bn': u'উইকিপেডিয়া',
            'ca': u'Viquipèdia',
            'cs': u'Wikipedie',
            'csb': u'Wiki',
            'cy': u'Wicipedia',
            'el': u'Βικιπαίδεια',
            'eo': u'Vikipedio',
            'et': u'Vikipeedia',
#            'fa': u'ویکی‌پدیا',
            'fr': u'Wikipédia',
            'fur':u'Vichipedie',
            'fy': u'Wikipedy',
            'ga': u'Vicipéid',
            'gu': u'વિકિપીડિયા',
            'he': u'ויקיפדיה',
            'hi': u'विकिपीडिया',
            'hu': u'Wikipédia',
            'ka': u'ვიკიპედია',
            'ko': u'위키백과',
            'ku': u'Wîkîpediya',
            'la': u'Vicipaedia',
            'mt': u'Wikipedija',
            'nv': u'Wikiibíídiiya',
            'oc': u'Oiquipedià',
            'pa': u'ਵਿਕਿਪੀਡਿਆ',
            'ru': u'Википедия',
            'sk': u'Wikipédia',
            'sl': u'Wikipedija',
            'sr': u'Википедија',
            'tr': u'Vikipedi',
            'yi': u'װיקיפּעדיע',
        }
        self.namespaces[5] = {
            '_default': u'Wikipedia talk',
            'ab': u'Обсуждение Wikipedia',
            'af': u'WikipediaBespreking',
            'af': u'Wikipediabespreking',
            'als': u'Wikipedia Diskussion',
            'ar': u'نقاش ويكيبيديا',
            'ast': u'Uiquipedia discusión',
            'av': u'Обсуждение Wikipedia',
            'ay': u'Wikipedia Discusión',
            'ba': u'Обсуждение Wikipedia',
            'be': u'Абмеркаваньне Вікіпэдыя',
            'bg': u'Уикипедия беседа',
            'bm': u'Discussion Wikipedia',
            'bn': u'উইকিপেডিয়া আলাপ',
            'br': u'Kaozeadenn Wikipedia',
            'ca': u'Viquipèdia Discussió',
            'ce': u'Обсуждение Wikipedia',
            'cs': u'Wikipedie diskuse',
            'csb': u'Diskùsëjô Wiki',
            'cv': u'0',
            'cy': u'Sgwrs Wicipedia',
            'da': u'Wikipedia diskussion',
            'de': u'Wikipedia Diskussion',
            'el': u'Βικιπαίδεια συζήτηση',
            'eo': u'Vikipedio diskuto',
            'es': u'Wikipedia Discusión',
            'et': u'Vikipeedia arutelu',
            'eu': u'Wikipedia eztabaida',
            'fa': u"بحث Wikipedia",		# u'بحث ویکی‌پدیا',
            'fi': u'Keskustelu Wikipediasta',
            'fo': u'Wikipedia kjak',
            'fr': u'Discussion Wikipédia',
            'fur': u'Discussion Vichipedie',
            'fy': u'Wikipedy oerlis',
            'ga': u'Plé Vicipéide',
            'gn': u'Wikipedia Discusión',
            'gu': u'વિકિપીડિયા talk',
            'he': u'שיחת ויקיפדיה',
            'hi': u'विकिपीडिया वार्ता',
            'hr': u'Razgovor Wikipedia',
            'hu': u'Wikipédia vita',
            'ia': u'Discussion Wikipedia',
            'id': u'Pembicaraan Wikipedia',
            'is': u'Wikipediaspjall',
            'it': u'Discussioni Wikipedia',
            'ja': u'Wikipedia‐ノート',
            'ka': u'ვიკიპედია განხილვა',
            'ko': u'위키백과토론',
            'ku': u'Wîkîpediya nîqaş',
            'kv': u'Обсуждение Wikipedia',
            'la': u'Disputatio Vicipaediae',
            'li': u'Euverlik Wikipedia',
            'lt': u'Wikipedia aptarimas',
            'mk': u'Wikipedia разговор',
            'ms': u'Perbualan Wikipedia',
            'mt': u'Wikipedija talk',
            'nap': u'Discussioni Wikipedia',
            'nds': u'Wikipedia Diskuschoon',
            'nl': u'Overleg Wikipedia',
            'nn': u'Wikipedia-diskusjon',
            'no': u'Wikipedia-diskusjon',
            'nv': u"Wikiibíídiiya baa yinísht'į́",
            'oc': u'Discutida Oiquipedià',
            'os': u'0',
            'pa': u'ਵਿਕਿਪੀਡਿਆ ਚਰਚਾ',
            'pl': u'Dyskusja Wikipedii',
            'pt': u'Wikipedia Discussão',
            'qu': u'Wikipedia Discusión',
            'ro': u'Discuţie Wikipedia',
            'ru': u'Обсуждение Википедии',
            'sc': u'Wikipedia discussioni',
            'sk': u'Diskusia k Wikipédii',
            'sl': u'Pogovor k Wikipediji',
            'sq': u'Wikipedia diskutim',
            'sr': u'Разговор о Википедији',
            'sv': u'Wikipediadiskussion',
            'ta': u'Wikipedia பேச்சு',
            'tr': u'Vikipedi tartışma',
            'tt': u'Wikipedia bäxäse',
            'ty': u'Discussion Wikipedia',
            'udm': u'0',
            'uk': u'Обговорення Wikipedia',
            'vi': u'Thảo luận Wikipedia',
            'wa': u'Wikipedia copene',
            'yi': u'װיקיפּעדיע רעדן',
        }
            
        self.disambiguationTemplates = {
            '_default': [u'Disambig'],
            'af':  [u'Dubbelsinnig'],
            'als': [u'Begriffsklärung'],
            'ang': [u'Disambig'],
            'ar':  [u'Disambig', u'توضيح'],
            'be':  [u'Неадназначнасьць'],
            'bg':  [u'Пояснение'],
            'ca':  [u'Desambiguació'],
            'cs':  [u'Rozcestník'],
            'cy':  [u'Anamrwysedd'],
            'da':  [u'Flertydig'],
            'de':  [u'Begriffsklärung'],
            'el':  [u'Disambig'],
            'en':  [u'Disambig', u'LND', u'2LA', u'TLAdisambig', u'Disambiguation', u'2LCdisambig', u'4LA', u'Acrocandis', u'Hndis', u'Numberdis', u'Roadis', u'Geodis', u'Listdis', u'Interstatedis', u'Dab', u'Disambig-cleanup', u'Disamb'],
            'eo':  [u'Apartigilo'],
            'es':  [u'Desambiguacion', u'Desambiguación', u'Desambig'],
            'et':  [u'Täpsustuslehekülg'],
            'eu':  [u'Argipen'],
            'fa':  [u'ابهامزدایی'],
            'fi':  [u'Täsmennyssivu'],
            'fr':  [u'Homonymie'],
            'fy':  [u'Tfs'],
            'ga':  [u'Idirdhealú'],
            'gl':  [u'Homónimos'],
            'he':  [u'DisambiguationAfter', u'פירושונים'],
            'hr':  [u'Disambig'],
            'hu':  [u'Egyert'],
            'ia':  [u'Disambiguation'],
            'id':  [u'Disambig'],
            'io':  [u'Homonimo'],
            'is':  [u'Aðgreining'],
            'it':  [u'Disambigua'],
            'ja':  [u'Aimai'],
            'ka':  [u'არაორაზროვნება'],
            'ko':  [u'Disambig'],
            'ku':  [u'Cudakirin'],
            'la':  [u'Discretiva'],
            'lb':  [u'Homonymie'],
            'li':  [u'Verdudeliking'],
            'ln':  [u'Bokokani'],
            'lt':  [u'Disambig'],
            'mt':  [u'Diżambigwazzjoni'],
            'nds': [u'Mehrdüdig Begreep'],
            'nl':  [u'Dp', 'DP', 'Dp2', 'Dpintro'],
            'nn':  [u'Fleirtyding'],
            'no':  [u'Peker', u'Etternavn'],
            'pl':  [u'Disambig', u'DisambRulers', u'DisambigC'],
            'pt':  [u'Desambiguação'],
            'ro':  [u'Dezambiguizare'],
            'ru':  [u'Disambig', u'Значения'],
            'scn': [u'Disambigua'],
            'simple': [u'Disambig', u'Disambiguation'],
            'sk':  [u'Disambiguation'],
            'sl':  [u'Disambig'],
            'sq':  [u'Kthjellim'],
            'sr':  [u'Вишезначна одредница'],
            'su':  [u'Disambig'],
            'sv':  [u'Betydelselista', u'Disambig', u'Gaffel', u'Efternamn', 'Gren'],
            'th':  [u'แกกำกวม'],
            'tl':  [u'Paglilinaw'],
            'tr':  [u'Anlam ayrım'],
            'vi':  [u'Trang định hướng'],
            'wa':  [u'Omonimeye'],
            'zh':  [u'Disambig', u'消歧义', u'消歧义页'],
            'zh-min-nan': [u'Khu-piat-iah', 'KhPI'],
        }
        
        # On most Wikipedias page names must start with a capital letter, but some
        # languages don't use this.
            
        self.nocapitalize = ['jbo','tlh','tokipona']
            

        # on_one_line is a list of languages that want the interwiki links
        # one-after-another on a single line
        self.interwiki_on_one_line = ['hu']
        
        # A revised sorting order worked out on http://meta.wikimedia.org/wiki/User_talk:ChongDae#Re:_Chobot
        self.alphabetic_revised = ['aa','af','ak','als','am','ang','ab','ar',
           'an','roa-rup','as','ast','gn','av','ay','az','id','ms','bm',
           'bn','zh-min-nan','ban','jv','su','bug','ba','be','bh','mt',
           'bi','bo','bs','br','bg','ca','ceb','cv','cs','ch','ny','sn','tum',
           'cho','co','za','cy','da','de','dv','nv','dz','mh','et','na','el','en','es',
           'eo','eu','ee','to','fa','fo','fr','fy','ff','fur','ga','gv','sm','gd','gl',
           'gay','ki','gu','got','ko','ha','haw','hy','hi','ho','hr','io','ig','ia','ie',
           'iu','ik','os','xh','zu','is','it','he','kl','kn','kr','ka','ks','csb','kw',
           'rw','ky','rn','sw','kv','kg','ht','kj','ku','lad','lo','la','lv','lb','lt','li',
           'ln','jbo','lg','lmo','hu','mk','mg','ml','mi','mr','chm','mo','mn','mus','my',
           'nah','fj','nap','nl','cr','ne','ja','ce','pih','no','nn','oc','or','om','ng','hz','ug',
           'uz','pa','kk','pi','pam','ps','km','nds','pl','pt','ty','ro','rm','qu','ru',
           'se','sa','sg','sc','sco','st','tn','sq','scn','si','simple','sd','ss','sk',
           'sl','so','sr','sh','fi','sv','tl','ta','tt','te','th','vi','ti','tlh','tg',
           'tpi','chr','chy','ve','tr','tk','tw','udm','uk','ur','vec','vo','fiu-vro','wa','war',
           'wo','ts','ii','yi','yo','zh','zh-tw','zh-cn']

        # A sorting order for lb.wikipedia worked out by http://lb.wikipedia.org/wiki/User_talk:Otets
        self.alphabetic_lb = ['aa', 'af', 'ak', 'als', 'am', 'ang', 'ab', 'ar',
            'an', 'roa-rup', 'as', 'ast', 'gn', 'av', 'ay', 'az', 'id', 'ms', 'bm',
            'bn', 'zh-min-nan', 'ban', 'jv', 'su', 'bug', 'ba', 'be', 'bh', 'mt',
            'bi', 'bo', 'bs', 'br', 'bg', 'ca', 'ceb', 'cs', 'ch', 'chr', 'chy',
            'ny', 'sn', 'tum', 've', 'cho', 'co', 'za', 'cy', 'da', 'de', 'dv',
            'nv', 'dz', 'mh', 'et', 'na', 'el', 'en', 'es', 'eo', 'eu', 'ee', 'to',
            'fa', 'fo', 'fr', 'fy', 'ff', 'fur', 'ga', 'gv', 'sm', 'gd', 'gl',
            'gay', 'ki', 'gu', 'got', 'ha', 'haw', 'hy', 'he', 'hi', 'ho',
            'hr', 'io', 'ig', 'ilo', 'ia', 'ie', 'iu', 'ik', 'os', 'xh', 'zu', 'is', 'it',
            'ja', 'kl', 'kn', 'kr', 'ka', 'ks', 'csb', 'kw', 'rw', 'ky', 'rn', 'sw',
            'kv', 'kg', 'ko', 'ht', 'kj', 'ku', 'lad', 'lo', 'la', 'lv', 'lb', 'lt', 'li',
            'ln', 'jbo', 'lg', 'lmo', 'hu', 'mk', 'mg', 'ml', 'mi', 'mr', 'chm',
            'mo', 'mn', 'mus', 'my', 'nah', 'fj', 'nap', 'nl', 'cr', 'ne', 'ce',
            'pih', 'no', 'nn', 'oc', 'or', 'om', 'ng', 'hz', 'ug', 'uz', 'pa', 'kk',
            'pi', 'pam', 'ps', 'km', 'nds', 'pl', 'pt', 'ty', 'ro', 'rm', 'qu',
            'ru', 'se', 'sa', 'sg', 'sc', 'sco', 'st', 'tn', 'sq', 'scn', 'si',
            'simple', 'sd', 'ss', 'sk', 'sl', 'so', 'sr', 'sh', 'fi', 'sv', 'tl',
            'ta', 'tt', 'te', 'th', 'vi', 'ti', 'tlh', 'tg', 'tpi', 'cv', 'tr',
            'tk', 'tw', 'udm', 'uk', 'ur', 'vec', 'vo', 'fiu-vro', 'wa', 'war',
            'wo', 'ts', 'ii', 'yi', 'yo', 'zh', 'zh-tw', 'zh-cn']


        # Which languages have a special order for putting interlanguage links,
        # and what order is it? If a language is not in interwiki_putfirst,
        # alphabetical order on language code is used. For languages that are in
        # interwiki_putfirst, interwiki_putfirst is checked first, and
        # languages are put in the order given there. All other languages are put
        # after those, in code-alphabetical order.
        
           
        self.interwiki_putfirst = {
            'en': self.alphabetic,
            'et': self.alphabetic_revised,
            'fi': self.alphabetic_revised,
            'he': ['en'],
            'hu': ['en'],
            'lb': self.alphabetic_lb,
            'nn': ['no','nb','sv','da'] + self.alphabetic,
            'pl': self.alphabetic,
            'simple': self.alphabetic,
            'vi': self.alphabetic_revised
            }

        self.obsolete = {'dk':'da',
                    'minnan':'zh-min-nan',
                    'nb':'no',
                    'jp':'ja',
                    'tokipona':'none',
                    'zh-tw':'zh',
                    'zh-cn':'zh'}
            
        # Language codes of the largest wikis. They should be roughly sorted
        # by size.
        
        self.languages_by_size = [
            'en','de','fr','ja','sv','pl','nl','it','pt','es','zh','no','fi',
            'ru','da','eo','he','uk','bg','ca','sl','hu','cs','sk','sr','ko',
            'ro','id','et','nn','hr','gl','ms','lt','wa','lb','tr','ar','el',
            'io','simple','fa','af','tt','th','ast','la','cy','eu','is','bs',
            'ia','ka','mk','vi','scn','lv','fy','ku','nds','sq','be','ga','jv',
            'tl','te','mr','fo','gd','ta','os','hi','zh-min-nan','li','kn',
            'oc','su','cv','br','als','an','csb','se','sa','sh','co','hy',
            'kw','bn','ur','ang','mi','ks','sco','mn','ceb','mo','ie','mt',
            'ht','na','ml','yi','gu','tpi','nah','ln','rm','mg','fur','jbo',
            'sc','bm','pam','sw','nv','az','ne','iu','vo','fiu-vro','yo','am',
            'chr','qu','tk','roa-rup','ky','bo','haw','sn','uz','sm','tg','gn',
            'xh','st','km','kk','ab','tum','ba','ug','ps','bi','gv','pa','so',
            'kv','got','za','ay','as','ce','dz','fj','kl','lo','tn','zu','ik',
            'my','ss','ty','wo','ch','tw','av','pi','ha','chy','dv','ff','si',
            'ts','cho','ig','om','ve','aa','ak','arc','bh','ny','cr','ee','hz',
            'ho','kr','ki','rw','rn','kg','kj','lg','mh','mus','ng','or','sg',
            'sd','ti','to','ii']

        # other groups of language that we might want to do at once
            
        self.cyrilliclangs = ['ab', 'be', 'bg', 'ce', 'cv', 'kk', 'ky', 'mk', 'mn', 'mo', 'ru', 'sr', 'tg', 'uk'] # languages in Cyrillic
        
        # Languages that used to be coded in iso-8859-1
        self.latin1old = ['de', 'en', 'et', 'es', 'ia', 'la', 'af', 'cs',
                    'fr', 'pt', 'sl', 'bs', 'fy', 'vi', 'lt', 'fi', 'it',
                    'no', 'simple', 'gl', 'eu', 'nds', 'co', 'mi', 'mr',
                    'id', 'lv', 'sw', 'tt', 'uk', 'vo', 'ga', 'na', 'es',
                    'nl', 'da', 'dk', 'sv', 'test']
                    
        self.mainpages = {
            'aa' :			u'Main Page',
            'ab' :			u'Main Page',
            'af' :			u'Tuisblad',
            'ak' :			u'Main Page',
            'als':			u'Houptsyte',
            'am' :			u'ዋናው ገጽ',
            'an' :			u'Portalada',
            'ang':			u'Héafodsíde',
            'ar' :			u'الصفحة الرئيسية',
            'arc':			u'Main Page',
            'as' :			u'Main Page',
            'ast':			u'Portada',
            'av' :			u'Main Page',
            'ay' :			u'Main Page',
            'az' :			u'Main Page',
            'ba' :			u'Баш бит',
            'be' :			u'Галоўная старонка',
            'bg' :			u'Начална страница',
            'bh' :			u'Main Page',
            'bi' :			u'Main Page',
            'bm' :			u'Nyɛ fɔlɔ',
            'bn' :			u'প্রধান পাতা',
            'bo' :			u'Main Page',
            'br' :			u'Main Page',
            'bs' :			u'Početna strana',
            'ca' :			u'Portada',
            'ce' :			u'Main Page',
            'ceb':			u'Main Page',
            'ch' :			u'Main Page',
            'cho':			u'Main Page',
            'chr':			u'Main Page',
            'chy':			u'Main Page',
            'co' :			u'Main Page',
            'cr' :			u'Main Page',
            'cs' :			u'Hlavní strana',
            'csb':			u'Przédnô starna',
            'cv' :			u'Тĕп страницă',
            'cy' :			u'Hafan',
            'da' :			u'Forside',
            'de' :			u'Hauptseite',
            'dv' :			u'Main Page',
            'dz' :			u'Main Page',
            'ee' :			u'Main Page',
            'el' :			u'Κύρια Σελίδα',
            'en' :			u'Main Page',
            'eo' :			u'Ĉefpaĝo',
            'es' :			u'Portada',
            'et' :			u'Esileht',
            'eu' :			u'Azala',
            'fa' :			u'صفحه‌ی اصلی',
            'ff' :			u'Hello jaɓɓorgo',
            'fi' :			u'Etusivu',
            'fiu-vro':		u'Pääleht',
            'fj' :			u'Main Page',
            'fo' :			u'Forsíða',
            'fr' :			u'Accueil',
            'fur':			u'Pagjine principâl',
            'fy' :			u'Haadside',
            'ga' :			u'Príomhleathanach',
            'gd' :			u'Duille Mòr',
            'gl' :			u'Portada',
            'gn' :			u'Main Page',
            'got':			u'Main Page',
            'gu' :			u'મુખપૃષ્ઠ',
            'gv' :			u'Main Page',
            'ha' :			u'Main Page',
            'haw':			u'Main Page',
            'he' :			u'עמוד ראשי',
            'hi' :			u'मुख्य पृष्ठ',
            'ho' :			u'Main Page',
            'hr' :			u'Glavna stranica',
            'ht' :			u'Main Page',
            'hu' :			u'Kezdőlap',
            'hy' :			u'Գլխավոր Էջ',
            'hz' :			u'Main Page',
            'ia' :			u'Wikipedia:Frontispicio',
            'id' :			u'Halaman Utama',
            'ie' :			u'Principal págine',
            'ig' :			u'Main Page',
            'ii' :			u'Main Page',
            'ik' :			u'Main Page',
            'io' :			u'Frontispico',
            'is' :			u'Forsíða',
            'it' :			u'Pagina principale',
            'iu' :			u'Main Page',
            'ja' :			u'メインページ',
            'jbo':			u'ralju ckupau',
            'jv' :			u'Kaca Utama',
            'ka' :			u'მთავარი გვერდი',
            'kg' :			u'Main Page',
            'ki' :			u'Main Page',
            'kj' :			u'Main Page',
            'kk' :			u'Main Page',
            'kl' :			u'Main Page',
            'km' :			u'Main Page',
            'kn' :			u'ಮುಖ್ಯ ಪುಟ',
            'ko' :			u'대문',
            'kr' :			u'Main Page',
            'ks' :			u'Main Page',
            'ku' :			u'Serûpel',
            'kv' :			u'Main Page',
            'kw' :			u'Main Page',
            'ky' :			u'Main Page',
            'la' :			u'Pagina prima',
            'lb' :			u'Haaptsäit',
            'lg' :			u'Main Page',
            'li' :			u'Huidpazjena',
            'ln' :			u'Lonkásá ya liboso',
            'lo' :			u'Main Page',
            'lt' :			u'Pradžia',
            'lv' :			u'Sākumlapa',
            'mg' :			u'Fandraisana',
            'mh' :			u'Main Page',
            'mi' :			u'Hau Kāinga',
            'mk' :			u'Почетна страна',
            'ml' :			u'Main Page',
            'mn' :			u'Main Page',
            'mo' :			u'Main Page',
            'mr' :			u'मुखपृष्ठ',
            'ms' :			u'Laman Utama',
            'mt' :			u'Paġna prinċipali',
            'mus':			u'Main Page',
            'my' :			u'ဗဟုိစာမ္ယက္‌န္ဟာ',
            'na' :			u'Etang õgõg',
            'nah':			u'Main Page',
            'nds':			u'Hööftsiet',
            'ne' :			u'Main Page',
            'ng' :			u'Main Page',
            'nl' :			u'Hoofdpagina',
            'nn' :			u'Hovudside',
            'no' :			u'Hovedside',
            'nv' :			u'Íiyisíí Naaltsoos',
            'ny' :			u'Main Page',
            'oc' :			u'Acuèlh',
            'om' :			u'Main Page',
            'or' :			u'Main Page',
            'os' :			u'Сæйраг фарс',
            'pa' :			u'ਮੁੱਖ ਪੰਨਾ',
            'pam':			u'Main Page',
            'pi' :			u'Main Page',
            'pl' :			u'Strona główna',
            'ps' :			u'Main Page',
            'pt' :			u'Página principal',
            'qu' :			u'Qhapaq panka',
            'rm' :			u'Main Page',
            'rn' :			u'Main Page',
            'ro' :			u'Pagina principală',
            'roa-rup':		u'Main Page',
            'ru' :			u'Заглавная страница',
            'rw' :			u'Main Page',
            'sa' :			u'मुखपृष्ठं',
            'sc' :			u'Pàzina printzipale',
            'scn':			u'Paggina principali',
            'sco':			u'Main Page',
            'sd' :			u'Main Page',
            'se' :			u'Váldosiidu',
            'sg' :			u'Main Page',
            'sh' :			u'Glavna stranica / Главна страница',
            'si' :			u'Main Page',
            'simple':		u'Main Page',
            'sk' :			u'Hlavná stránka',
            'sl' :			u'Glavna stran',
            'sm' :			u'Main Page',
            'sn' :			u'Main Page',
            'so' :			u'Main Page',
            'sq' :			u'Faqja Kryesore',
            'sr' :			u'Главна страна',
            'ss' :			u'Main Page',
            'st' :			u'Main Page',
            'su' :			u'Tepas',
            'sv' :			u'Huvudsida',
            'sw' :			u'Mwanzo',
            'ta' :			u'முதற் பக்கம்',
            'te' :			u'మొదటి పేజీ',
            'tg' :			u'Main Page',
            'th' :			u'หน้าหลัก',
            'ti' :			u'Main Page',
            'tk' :			u'Main Page',
            'tl' :			u'Unang Pahina',
            'tn' :			u'Main Page',
            'to' :			u'Main Page',
            'tpi':			u'Main Page',
            'tr' :			u'Ana Sayfa',
            'ts' :			u'Main Page',
            'tt' :			u'Täwge Bit',
            'tum':			u'Main Page',
            'tw' :			u'Main Page',
            'ty' :			u'Main Page',
            'ug' :			u'Main Page',
            'uk' :			u'Головна стаття',
            'ur' :			u'صفحہ اول',
            'uz' :			u'Main Page',
            've' :			u'Main Page',
            'vi' :			u'Trang Chính',
            'vo' :			u'Cifapad',
            'wa' :			u'Mwaisse pådje',
            'wo' :			u'Main Page',
            'xh' :			u'Main Page',
            'yi' :			u'ערשטע זײַט',
            'yo' :			u'Main Page',
            'za' :			u'Main Page',
            'zh' :			u'首页',
            'zh-min-nan':	u'Thâu-ia̍h',
            'zu' :			u'Main Page',
        }
    
    def code2encodings(self, code):
        """Return a list of historical encodings for a specific language
           wikipedia"""
        # Historic compatibility
        if code == 'pl':
            return 'utf-8', 'iso8859-2'
        if code == 'ru':
            return 'utf-8', 'iso8859-5'
        if code in self.latin1old:
            return 'utf-8', 'iso-8859-1'
        return self.code2encoding(code),
