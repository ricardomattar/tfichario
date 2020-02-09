# -*- coding: latin1 -*-
"""
Created on Sun Oct 11 09:16:49 2015

@author: ricardo
"""

import post


pesquisa = post.call(username='admin', password='secreta', method='hospedes.rpc_query', query='ricardo%')
print(pesquisa)
                
