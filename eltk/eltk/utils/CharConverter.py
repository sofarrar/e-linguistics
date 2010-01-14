# -*- coding: UTF-8 -*-
#
# e-Linguistics Toolkit: CharConverter
#
# Copyright (C) 2008 ELTK Project
# Author: Scott Farrar <farrar@u.washington.edu>
# URL: <http://e-linguistics.org>
# For license information, see LICENSE.TXT

"""
The character conversion module is used to  convert between any two string conventions, e.g., unicode ipa and praat symbols. It is useful in converting Praat TextGrid annotation to LaTeX (and onto PDF). It is also useful for converting any data not in Unicode to Unicode IPA. Unicode IPA refers to IPA symbols encoded in UTF-8. There is the CharConverter class itself, its constructor and the convert method. 
"""

#the main dictionary
ipa_charmap={'p':['vl bilabial plosive','p','p','p'],
'b':['vd bilabial plosive','b','b','b'],
't':['vl alveolar plosive','t','t','t'],
'd':['vd alveolar plosive','d','d','d'],
'ʈ':['vl retroflex plosive','\:t','\\t.','t`'],
'ɖ':['vd retroflex plosive','\:d','\d.','d`'],
'ɟ':['vd palatal plosive','\\textbardotlessj','\j^','j`'],
'k':['ld velar plosive','k','k','k'],
'ɡ':['vd velar plosive','g','\gs','g'],
'q':['vl uvular plosive','q','q','q'],
'ɢ':['vd uvular plosive','\;G','\gc','G\\'],
'ʔ':['glottal plosive','P','\?g','?'],
'm':['bilabial nasal','m','m','m'],
'ɱ':['vl labiodental nasal','M','\mj','F'],
'n':['alveolar nasal','n','n','n'],
'ɳ':['vl retroflex nasal','\:n','\\n.','n`'],
'ɲ':['vl palatal nasal','\\textltailn','\\nj','J'],
'ŋ':['vl velar nasal','N','\\ng','N'],
'ɴ':['vl uvular nasal','\;N','\\nc','N\\'],
'ʙ':['vd bilabial trill','\;B','\\bc','B\\'],
'r':['vd alveolar trill','r','r','r'],
'ʀ':['vl uvular trill','\;R','\\rc','R\\'],
'':['labiodental flap','none','none','none'],
'ɾ':['vl alveolar tap','R','\\fh','4'],
'ɽ':['vl retroflex flap','\:r','\\f.','r`'],
'ɸ':['vl bilabial fricative','F','\\ff','p\\'],
'β':['vd bilabial fricative','B','\\bf','B'],
'f':['vl labiodental fricative','f','f','f'],
'v':['vd labiodental fricative','v','v','v'],
'θ':['vl dental fricative','T','\\tf','T'],
'ð':['vd dental fricative','D','\dh','D'],
's':['vl alveolar fricative','s','s','s'],
'z':['vd alveolar fricative','z','z','z'],
'ʃ':['vl postalveolar fricative','S','\sh','S'],
'ʒ':['vd postalveolar fricative','Z','\zh','Z'],
'ʂ':['vl retroflex fricative','\:s','\s.','s`'],
'ʐ':['vd retroflex fricative','\:z','\z.','z`'],
'ç':['vl palatal fricative','\c{c}','\c,','C'],
'ʝ':['vd palatal fricative','J','\jc','j\\'],
'x':['vl velar fricative','x','x','x'],
'ɣ':['vd velar fricative','G','\gf','G'],
'χ':['vl uvular fricative','X','\cf','X'],
'ʁ':['vd uvular fricative','K','\\ri','R\\'],
'ħ':['vl pharyngeal fricative','\\textcrh','\h-','X\\'],
'ʕ':['vd pharyngeal fricative','Q','\9e','?\\'],
'h':['vl glottal fricative','h','h','h'],
'ɦ':['vd glottal fricative','H','\h^','h\\'],
'ɬ':['vl alveolar lateral fricative','\\textbeltl','\l-','K'],
'ɮ':['vd alveolar lateral fricative','\\textlyoghlig','\lz','K\\'],
'ʋ':['vd labiodental approximant','V','\\vs','P'],
'ɹ':['vd (post)alveolar approximant','\*r','\\rt','r\\'],
'ɻ':['vd retroflex approximant','\:R','\\r.','r\`'],
'ɰ':['vd velar approximant','\\textturnmrleg','\ml','M\\'],
'l':['vd alveolar lateral approximant','l','l','l'],
'ɭ':['vd retroflex lateral approximant','\:l','\l.','l`'],
'ʎ':['vd palatal lateral approximant','L','\yt','L'],
'ʟ':['vd velar lateral approximant','\;L','\lc','L\\'],
'ɕ':['vl alveolopalatal fricative','C','\cc','s\\'],
'ʤ':['vd postalveolar affricate','\\textdyoghlig','none','dZ'],
'ɧ':['vl multiple-place fricative','\\texththeng','\hj','x\\'],
'ɥ':['labial-palatal approximant','4','\ht','H'],
'ʜ':['vl epiglottal fricative','\;H','\hc','H\\'],
'ɫ':['velarized vl alveolar lateral','\\textltilde','\l~','5'],
'ɺ':['vl alveolar lateral flap','\\textturnlonglegr','\\rl','l\\'],
'ʧ':['vl postalveolar affricate','\\textteshlig','none','tS'],
'ʍ':['vl labial-velar fricative','\*w','\wt','W'],
'ʑ':['vl alveolopalatal fricative','\\textctz','\zc','z\\'],
'ʡ':['vl epiglottal plosive','\\textbarglotstop','\?-','>\\'],
'ʢ':['vl epiglottal fricative','\\textbarrevglotstop','\9-','<\\'],
'w':['vd labio-velar approximant','w','w','w'],
'ʘ':['bilabial click','\!o','\O.','O\\'],
'ǀ':['dental click','\\textpipe','\|1','|\\'],
'ǃ':['retroflex click','!','!','!\\'],
'ǂ':['alveolar click','\\textdoublebarpipe','\|-','=\\'],
'ǁ':['alveolar lateral click','\\textdoublepipe','\|2','|\|\\'],
'ɓ':['vl bilabial implosive','\!b','\\b^','b_<'],
'ɗ':['vl alveolar implosive','\!d','\d^','d_<'],
'ʄ':['vl palatal implosive','\!j','\i-','J\_<'],
'ɠ':['vl velar implosive','\!g','\g^','g_<'],
'ʛ':['vl uvular implosive','\!G','\G^','G\_<'],
'ʼ':['ejective','\'','none','_>'],
'ʴ':['rhotacized','UNKNOWN','none','none'],
'ʰ':['aspirated','\\textsuperscript{h}','H','_h'],
'ʱ':['breathy-voice-aspirated','\\textsuperscript{H}','none','none'],
'ʲ':['palatalized','\\textsuperscript{j}','J','\''],
'ʷ':['labialized','\\textsuperscript{w}','W','_w'],
'ˠ':['velarized','\\textsuperscript{\\textgamma}','none','_G'],
'ˤ':['pharyngealized','\\textsuperscript{\\textrevglotstop}','none','_?\\'],
'˞':['rhotacized','\\textrhoticity','none','@`'],
'̥':['voiceless','\\r*','\0v','_0'],
'̊':['vl voiceless (use if character has descender)','UNKNOWN\\r{}','none','none'],
'̤':['breathy voiced','\"*','\:v','_t'],
'̪':['dental','\|[','\Nv','_d'],
'̬':['voiced','\\v*','none','_v'],
'̰':['creaky voiced','\~*','\~v','_k'],
'̺':['apical','\|]','none','_a'],
'̼':['linguolabial','UNKNOWN\|m{}','none','_N'],
'̻':['laminal','UNKNOWN\\textsubsquare{}','none','_m'],
'̚':['not audibly released','\\textcorner','none','_}'],
'̹':['more rounded','\|)','\3v','_O'],
'̃':['nasalized','\~','\~^\'','~'],
'̜':['less rounded','\|(','\cv','_c'],
'̟':['advanced','\|+','\+v','_+'],
'̠':['retracted','\=*','\-v','_-'],
'̈':['centralized','\"','\:^','_"'],
'̴':['velarized or pharyngealized','none','none','_e'],
'̽':['mid-centralized','UNKNOWN\|x{}','none','_x'],
'̝':['raised','\|\'','\T^','_r'],
'̩':['syllabic','UNKNOWN\s{}','\|v','='],
'̞':['lowered','\|`','\Tv','_o'],
'̯':['non-syllabic','UNKNOWN\\textsubarch{}','none','_^'],
'̘':['advanced tongue root','\|<','none','_A'],
'̙':['retracted tongue root','\|>','none','_q'],
'ˈ':['(primary) stress mark','"','\\\'1','"'],
'ˌ':['secondary stress','""','\\\'2','%'],
'ː':['length mark',':','\:f',':'],
'ˑ':['half-length',';','none',':\\'],
'̆':['extra-short','UNKNOWN\\u{}','none','_X'],
'͜':['tie bar below','UNKNOWN\\t*{}','none','-\\'],
'͡':['tie bar above','UNKNOWN\\t{}','\li','none'],
'|':['Minor (foot) group','\\textvertline','|','|'],
'‖':['Major (intonation) group','\\textdoublevertline','||','||'],
'.':['syllable break','.','.','none'],
'̋':['extra high tone','UNKNOWN\H{}','none','_T'],
'́':['high tone','HTONE','\\\'^','_H'],
'̄':['mid tone','MTONE','\-^','_M'],
'̀':['low tone','LTONE','\`^','_L'],
'̏':['extra low tone','\H*','none','_B'],
'̌':['rising tone','??\\v{}','UNKNOWN','_L_H'],
'̂':['falling tone','\^','none','_H_L'],
'↓':['downstep','\\textdownstep','none','<!>'],
'↑':['upstep','\\textupstep','none','<^>'],
'↗':['global rise','\\textglobrise','none','</>'],
'↘':['global fall','\\textglobfall','none','<\>'],
'i':['close front unrounded','i','i','i'],
'y':['close front rounded','y','y','y'],
'e':['close-mid front unrounded','e','e','e'],
'a':['open front unrounded','a','a','a'],
'u':['close back rounded','u','u','u'],
'o':['close-mid back rounded','o','o','o'],
'ɑ':['open back unrounded','A','\\as','A'],
'ɐ':['open-mid schwa','5','\\at','6'],
'ɒ':['open back rounded','6','\\ab','Q'],
'æ':['raised open front unrounded','\\ae','\\ae','{'],
'ɔ':['open-mid back rounded','O','\ct','O'],
'ə':['schwa','@','\sw','@'],
'ɘ':['close-mid schwa','9','\e-','@\\'],
'ɚ':['rhotacized schwa','\\textrhookschwa','\sr','@`'],
'ɛ':['open-mid front unrounded','E','\ef','E'],
'ɜ':['open-mid central','3','\er','3'],
'ɝ':['rhotacized open-mid central','\\textrhookrevepsilon','none','3`'],
'ɞ':['open-mid central rounded','\\textcloserevepsilon','\kb','3\\'],
'ɨ':['close central unrounded','1','\i-','1'],
'ɪ':['lax close front unrounded','I','\ic','I'],
'ɯ':['close back unrounded','W','\mt','M'],
'ø':['front close-mid rounded','\o','\o/','2'],
'ɵ':['rounded schwa','8','\o-','8'],
'œ':['front open-mid rounded','\oe','\oe','9'],
'ɶ':['front open rounded','\OE','\Oe','&'],
'ʉ':['close central rounded','\\textbaru','\\u-','}'],
'ʊ':['lax close back rounded','U','\hs','U'],
'ʌ':['open-mid back unrounded','\\textturnv','\\vt','V'],
'ɤ':['close-mid back unrounded','\\textramshorns','\\rh','7'],
'ʏ':['lax close front rounded','Y','\yc','Y'],
}
"""
The data source for the character converterm. Keys are ipa unicode objects, and values are  lists of symbols:

unicode: [informal name, tipa, praat, xsampa]

For example::

'ɖ':['vd retroflex plosive','\:d','\d.','d`']

Thus, '\:d' is the tipa symbol used for the voiced retroflex plosive.
"""


latex_charmap={'Ä':['\"{A}'],
'ä':['\\"{a}'],
'Á':['\\\'{A}'],
'á':['\\\'{a}'],
'À':['\\`{A}'],
'à':['\\`{a}'],
'Â':['\\^{A}'],
'â':['\\^{a}'],
'Å':['\\AA{}'],
'å':['\\aa{}'],
'Æ':['\\AE{}'],
'æ':['\\ae{}'],
'Ç':['\\c{C}'],
'ç':['\\c{c}'],
'Ë':['\\"{E}'],
'ë':['\\"{e}'],
'É':['\\\'{E}'],
'é':['\\\'{e}'],
'È':['\\`{E}'],
'è':['\\`{e}'],
'Ê':['\\^{E}'],
'ê':['\\^{e}'],
'Í':['\\\'{I}'],
'í':['\\\'{i}'],
'Ï':['\\"{I}'],
'ï':['\\"{i}'],
'ĩ':['\\~{i}'],
'Ñ':['\\~{N}'],
'ñ':['\\~{n}'],
'Ö':['\\"{O}'],
'ö':['\\"{o}'],
'Ó':['\\\'{O}'],
'ó':['\\\'{o}'],
'Ø':['\\O{}'],
'ø':['\\o{}'],
'Ô':['\\^{O}'],
'ô':['\\^{o}'],
'Œ':['\\OE{}'],
'œ':['\\oe{}'],
'ß':['\\ss'],
'Ü':['\\"{U}'],
'ü':['\\"{u}'],
'Ú':['\\\'{U}'],
'ú':['\\\'{u}'],
'ũ':['\\~{u}'],
'¡':['\\textexclamdown'],
'¿':['\\textquestiondown'],
}
"""
Another dictionary is used for conversion to LaTex. Keys are common characters used in latex docs, e.g., ö. Values are list which include the corresponding latex escape character, e.g, \"{o}. The ipa_charmap is not used because many of the common latex characters are not IPA.
"""


import urllib

class CharConverter:
    """
    CharConverter is the main class used to convert  between two writing conventions.
    """

    def __init__(self,source,target):
        """
        Creates an instance of a character converter. Source is a string:  'uni', 'name', 'tipa', 'praat', 'xsampa', or 'latex'. Target is also a string, one of: 'uni','name','tipa','praat','xsampa',or 'latex'.    
        
        :param source: 'uni', 'name', 'tipa','praat', 'xsampa', or 'latex'
        :type source: string
        :param target: 'uni', 'name', 'tipa','praat', 'xsampa', or 'latex'
        :type target: unicode, string
        """

        self.new_map={}
        
        
        if source=='latex' or target=='latex':
        
            #print latex_charmap

            self.code={'latex':0}
            
            if source=='latex':

                for k,v in latex_charmap.iteritems():
                    self.new_map[v[0]]=k
                
            else: 

                for k,v in latex_charmap.iteritems():
                    self.new_map[k]=v[0]
        
        else:
            self.code={
                'name':0,
                'tipa':1,
                'praat':2,
                'xsampa':3,
                }        
        
            
            for k,v in ipa_charmap.iteritems():
            
                new_key=''
                new_val=''
            
                if source!='uni':
                    new_key=v[self.code[source]]
                else: new_key=k 

                if target!='uni':
                    new_val=v[self.code[target]]
                else: new_val=k

                self.new_map[new_key]=new_val
    
        #print self.new_map

    def convert(self,string):
        """
        Returns a new string by replacing string w. a new value based on map. String is the a string to be converted.
        
        :param string: string to be converted
        :type string: string
        :rtype: unicode
        """

        for k,v in self.new_map.iteritems():
            
            string=string.replace(k,v)
        return string          


if __name__=='__main__':

    elan_converter=CharConverter('xsampa','uni')
    print elan_converter.convert('kO nEnE Oku')

    c=CharConverter('uni','tipa')
    
    #should print '1'
    print c.convert('ɨ')
    
    #should print '\"{u}'
    c1=CharConverter('uni','latex')
    print c1.convert('ü')


















