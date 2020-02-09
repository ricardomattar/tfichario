# -*- coding: UTF-8 -*-
"""
Created on Sun Oct  4 06:56:41 2015

@author: ricardo
"""
from itertools import groupby
import unicodedata

from . import acentos
from . import acentos

def somente_numeros(valor):
    return "".join(_ for _ in valor if _ in "1234567890")    
    
#def remove_acentuacao(str):
#    lstr = str.lower()
#    try:
#        from unicodedata import normalize
#        return normalize('NFKD', lstr.decode('utf-8')).encode('ASCII', 'ignore')
#    
#    except:
#        return lstr



#def remove_acentuacao(s):
#    try:
#        st = unicode(s)
#    except:
#        st = s.decode('utf-8')
#    return ''.join(c for c in unicodedata.normalize('NFKD', st) if unicodedata.category(c) != 'Mn')

                      
#def remove_acentuacao(str):
#    return acentos.strip_diacriticals(str)

def remove_acentuacao(text):
    text = text.lower()
    # try:
    #     text = unicode(text)
    # except:
    #     text = text.decode('utf-8')
        
    text = unicodedata.normalize("NFKD", text) #D is for d-ecomposed
    clean_text = text.encode("ascii", "ignore")
    #clean_text = u"".join([ch for ch in text if not unicodedata.combining(ch)])
    return clean_text


 
def soundex(word):
    codes = ("bfpv","cgjkqsxz", "dt", "l", "mn", "r")
    soundDict = dict((ch, str(ix+1)) for ix,cod in enumerate(codes) for ch in cod)
    cmap2 = lambda kar: soundDict.get(kar, '9')
    sdx =  ''.join(cmap2(kar) for kar in word.lower())
    sdx2 = word[0].upper() + ''.join(k for k,g in list(groupby(sdx))[1:] if k!='9')
    sdx3 = sdx2[0:4].ljust(4,'0')
    return sdx3
    
if __name__ == '__main__':
    print(remove_acentuacao('RICARDO MATTAR ÁÉÍÓÚÇÃ'))
    print(remove_acentuacao(u'RICARDO MATTAR ÁÁÁÉÍÓÚÇÃ'))