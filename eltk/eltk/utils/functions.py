# -*- coding: UTF-8 -*-
# e-Linguistics Toolkit: functions
#
# Copyright (C) 2008 ELTK Project
# Author: Scott Farrar <farrar@u.washington.edu>
# URL: <http://e-linguistics.org>
# For license information, see LICENSE.TXT
"""
The functions module contains various utility functions, mostly for string processing, IGT element detection (redup. forms, clitic forms, etc), and tipa latex clean-up functions.
"""

from re import sub,compile

from random import randrange

from decimal import * 

from urlparse import urlsplit

import urllib



def formatEscapes(s):
    """
    Returns a string with an extra slash in front of Python's escape char's
    
    :type s: string
    :param s: any string
    :return: a string with an extra slash in front of Python's escape char's   
    :rtype: string
    """

    if s.endswith('\\'): s=s+'\\'
    s=s.replace('\'','\\\'')
    #s=s.replace('\\\'','\\\\\'')
    #s=s.replace('\\','\\\\')
    s=s.replace('\\a','\\\\a')
    s=s.replace('\\b','\\\\b')
    s=s.replace('\\f','\\\\f')
    s=s.replace('\\n','\\\\n')
    s=s.replace('\\r','\\\\r')
    s=s.replace('\\t','\\\\t')
    s=s.replace('\\v','\\\\v')
    s=s.replace('\\u','\\\\u')
    #print type(s)
    return s



def tipaClean(s):
    """
    Fixes some issues with tipa package in latex, e.g. filling in spaces and 
    merging commands with {}'s, e.g., \textsuperscript{}a to \textsuperscript{a} 

    :type s: str
    :param s: a string with possible ill-formed tipa
    :return: returns a formatted string containing correct tipa code
    :rtype: str
    """  
    
    #a list of tipa commands
    tex_cmds=[ '\^', '\\textupstep', '\!G', '\\textcorner', '\;L', '\|`', '\\textteshlig', '\|[', '\\textsuperscript{w}', '\|]', '\\textdoublepipe', '\\textramshorns', '\!g', '\c{c}', '\\textturnmrleg', '\\textvertline', '\'', '\;R', '\!j', '\:t', '\\textturnv', '\\textbeltl', '\:z', '\|>', '\!o', '\|\'', '\;H', '\\r*', '\\textdyoghlig', '\\textsuperscript{h}', '\|)', '\;N', '\\textdoublebarpipe', '\\textltailn', '\!b', '\!d', '\\textsuperscript{\\textgamma}', '\\textsuperscript{\\textrevglotstop}', '\\texththeng', '\o', '\:R', '\OE', '\`', '\=', '\\textbaru', '\"', '\*w', '\\textctz', '\\textdownstep', '\\textglobrise', '\\textdoublevertline', '\;B', '\|<', '\|(', '\\textbarglotstop', '\=*', '\"*', '\\v*', '\\textsuperscript{H}', '\~*', '\\textbardotlessj', '\:d', '\\textrhookschwa', '\\textcloserevepsilon', '\;G', '\\textlyoghlig', '\\textturnlonglegr', '\\textltilde', '\~', '\:s', '\H*', '\\textglobfall', '\|+', '\\textbarrevglotstop', '\\textcrh', '\:n', '\\textsuperscript{j}', '\\textpipe', '\oe', '\\textrhookrevepsilon', '\\textrhoticity', '\\ae', '\:l', '\*r', '\:r']
   

    for t in tex_cmds:

        if not t.endswith('}'):
            s=s.replace(t,t+' ')
    #regex to replace \command{}a with \command{a} 
    s=sub('{}(?P<exp>.)','{\g<exp>}',s)

    
    #for tone
    s=s.replace('\' \`','\^')

    s=s.replace('\` \\\'','\\v')

    s=sub('(?P<exp>.)HTONE','\\\'\g<exp>',s)
    s=sub('(?P<exp>.)LTONE','\`\g<exp>',s)
    s=sub('(?P<exp>.)MTONE','\=\g<exp>',s)
    
    s=sub('(?P<exp>.)\\\\\^','\^\g<exp>',s)
    s=sub('(?P<exp>.)\\\v','\v\g<exp>',s)

    s=sub('(?P<exp>.)\\\~','\~\g<exp>',s)


    return s

def printList(list):
    """
    Given a list, returns a concatenated string of its elements.
    (opposite of split())

    @type list: list 
    @param: any list
    @rtype: str
    @return: returns a concatenated string of list elements 
    """
    lst_str=u''
    for item in list:
        if item is not None:
            lst_str=lst_str+item+u' '
    return lst_str

    
def printTipaList(list):
    """
    Given a list, returns a concatenated string of its elements, each enclosed 
    in '\textipa{...}.'

    :type list: list 
    :param list: any list
    :return: returns a concatenated string of list elements 
    :rtype: str
    """

    lst_str=u''
    for item in list:
        lst_str=lst_str+'\\textipa{'+item+'}'+u' '
    return lst_str

def findQuoted(s):
        """
        Return the contents of double quoted material.    
        
        :type s: string
        :param s: a string containing double quotes
        :return: returns the string between quotes
        :rtype: string
        """

	begin = s.find('"')
	end = s.find('"',begin+1)
	return s[begin+1:end]	

def findNum(s):
        """ 
        Find the first decimal number within an  arbitrary string
    
        FIX: does not return integers and throws error if no decimal found.
        
        :param s: a string possibly containing digits
        :type s: string
        :returns: a Decimal object
        :rtype: Decimal
        """

       
	patt=compile('0|[0-9]+\.[0-9]+')
        
        dec=Decimal(s[patt.search(s).start():patt.search(s).end()]).quantize(Decimal('.01'), rounding=ROUND_UP).__float__()
        return dec

"""
quote
"""
def quote(string):
    """
    Converts special characters to '%' forms: %xx%xx. This is used to convert URI strings because they have to be in ASCII.

    :param string: a URI string
    :type string: str
    :returns: a URI string with special char's converted to %xx%xx format.
    :rtype: string 
    """
    
    #convert to str
    string=string.encode('utf-8')

    #in Py3.0, this can be a unicode object instead of a string
    #but only strings work in  Py2.6
    #
    return urllib.quote(string,':/#')



def getLocalName(uri):

    """
    Returns the local part of a URI string; works with either according to slash or hash namespace conventions
    
    :param uri: unicode obj representing a URI
    :type uri: unicode
    :returns: the local part of the URI string
    :rtype: unicode 
    """

    #convert to str in case unicode
    #uri_string=uri_string.encode('utf-8') 
    
    if '#' in uri:
        return urlsplit(uri)[4]
    
    #also handles slash namespaces
    else:
        return uri[uri.rfind('/')+1:]

def getNamespace(uri):
    """
    Returns  namespace part of a URI; works with either according to slash or hash namespace conventions.

    :param uri: a unicode obj representing a URI
    :type uri: unicode 
    :returns: the namespace part of the URI string
    :rtype: unicode 
    """   

    if '#' in uri:
        return  uri[:uri.rfind('#')+1]       
    
    #also handles slash namespaces
    else:
        return  uri[:uri.rfind('/')+1]       


######These functions moved here from Leipzig reader#################
def validate(lingunits,glosses,translation):
    """
    Prints a warning to stdout if number of source items does not
    match number of gloss items.

    :param lingunits: units from line 1 of IGT
    :type lingunits: list
    :param glosses: units from line 2 of IGT
    :type glosses: list
    :param translation: translation string from line 3 of IGT
    :type translation: str
    :return: pass or fail
    :rtype: boolean
    """


    if len(lingunits)==len(glosses): 
        return True
    else: 
        print 'Warning: unaligned IGT'
        print 'Check alignment in: '+ translation
        return False

       

def makeID(string=''):
    

    """
    Returns an randomly generated id, e.g., from 'blah', generate 'blah2345'.
    
    :param string: the prefix
    :type string: string
    :returns: a random id string
    :rtype: string
    """

    random_id= string.strip().replace(' ','')    
    
    random_id=random_id+str(randrange(1000,9999))
    
    return random_id



def parseIGTWord(s):
    """
    Custom splitter when string is mixed with the following delimiters '-', '=', and '~', as is common within words of IGT lines. White space and '.' are not considered delimiters.

    :type s: string
    :param s: A string containing IGT delimiters
    :return: list of items to which the delimiters apply
    :rtype: list
    """
    
    items=[]
        
    i=''

    #loop over all char's in string
    for c in s:
            
        if c=='-' or c=='~' or c=='=': #or c=='<' or c=='>': 
            
            i=i+c

            items.append(i)
            
            i=''
        
        else: i=i+c
            
    #when no delimiter, or to catch last item in string
    if i is not '':
        
        items.append(i)

    return items



def parseIGTLine(line):
    """    
    Returns an arrary (list of lists) of items within a line of IGT. (Does not assign a linguistics category to any of the items).

    :type line: string
    :param line: A string containing a line of IG
    :return: list of items/words in the line of IGT
    :rtype: list
    """
    
    #to remove extra spaces, tabs, etc.
    line=normalizeLine(line) 
    
    #items based on whitespace or tabs
    igt_line=[]
    


    for i in line.split():    
        
        igt_line.append(parseIGTWord(i))
    
    return igt_line


def normalizeLine(line):
    """
    Normalize the string, getting rid of extra spaces, tabs, etc.
    
    :type  line: string
    :param line: A typical line of IGT
    :return: A normalized line
    :rtype: string
    """

    norm=line.strip()

    #normalize tabs and spacing around '-' and '=' and '~'
    norm=sub(r'\s*-\s*',r'-',norm)
    norm=sub(r'\s*=\s*',r'=',norm)
    norm=sub(r'\s*~\s*',r'~',norm)

    return norm




def findClitics(word):
    """
    Return a list of clitics for words containing ='s as delimiters. Strategy is to locate the stem based on relative length.
    
    :type word: string
    :param word: A word with ='s delimiters
    :return: A list of clitic forms
    :rtype: list
    """
    clitics=[]

    morphemes=word.split('=')
          
    length=0

    stem=''

    #find the stem
    for m in morphemes:
        #use relative length strategy to find stem
        if len(m) > length:
            stem=m
            length=len(m)
        
    for m in morphemes:
        #don't return stem
        if m!=stem: clitics.append(m)

    return clitics

def findRedups(word):
    """
    Return a list of reduplicated morphemes for words containing ~'s as delimiters. 
    
    
    :type word: string
    :param word: A word with ~'s delimiters
    :return: The reduplicated form
    :rtype: string
    """
 
    morphemes=word.split('~') 
    
    
    redup=morphemes[0]

    for m in morphemes[1:]:
        
        if len(m)<=len(redup):
            redup=m

    return redup

def findInfixes(word):
    """
    Return a list of infix forms, those surrounded by <...>'s. 
    
    
    :type word: string
    :param word: A word with infixes delimited by <...>'s
    :return: list of infix forms
    :rtype: list
    """
    #forms to be returned
    infix_forms=[]

    infix_pattern=compile('<.*?>')


    for i in infix_pattern.findall(word):
        i=i.replace('<','')
        i=i.replace('>','')
        infix_forms.append(i)
    
    return infix_forms

def unpack(l,delimiter=''):
    """
    Recursive function: Returns a string by concatenating all elements of a list. Inserts a space between material from each list element, and removes any delimiters, e.g., '-'. For example, [['abc'],['c'],['d-','e']] returns 'abc c de'

    :type l: list
    :param l: A list of lists of strings
    :type delimiter: str
    :param delimiter: include a final delimiter, e.g., '-', default is ''.
    :return: concatenated string of all list contents
    :rtype: string
    """
    s=''
    for i in l:
        if type(i)==str:
            s=s+i+' '
        else:
            s=s+unpack(i,delimiter)
    #if s.find('-'): print s    
    #return s
    return s.replace('- ',delimiter)






if __name__=='__main__':

    #test Py escape and tipa
    print formatEscapes('abc\\tdef')
    print tipaClean('\\textupstep{}a')
    
    
    print findQuoted('abc"def"ghi')
    print findNum('abc1.23def')

    #test quote w. only ASCII
    print quote(u'http://www.test.org/test#test')
    #test quote w. non-ASCII
    print quote(u'http://www.test.hamišaluǧ.org')

    #tests for URI handling
    print getLocalName(u'http://foo.org#mylocal')
    print getLocalName(u'http://foo.org/mylocal')
   
    print getNamespace(u'http://foo.org#mylocal')
    print getNamespace(u'http://foo.org/mylocal')

    print getLocalName(u'http://foo.org#mylocalš')
    print quote(u'http://foo.org#mylocalš')

    #tests for unpack
    print unpack([['abc'],['c'],['d-','e']])
    print unpack([['abc'],['c'],['d-','e']],'-')


