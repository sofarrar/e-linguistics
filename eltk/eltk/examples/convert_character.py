# -*- coding: UTF-8 -*-
from eltk.utils.CharConverter import *

"""
This script demostrates the use of CharConverter
"""

if __name__=='__main__':

    #latex to unicode test
    c0=CharConverter('latex','uni')
    print c0.convert('author = {S\\\'{a}ndor Hervey},')

    #unicode to latex test
    c1=CharConverter('uni','latex')
    print c1.convert('ä')


    #praat to uni test
    c2=CharConverter('praat','uni')
    print c2.convert('\\t.o')

    print 'If you do not see IPA characters, you may not have the required fonts installed.'
