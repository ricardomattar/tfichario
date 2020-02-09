# -*- coding: latin1 -*-
"""
Created on Thu Aug  6 13:03:36 2015

@author: ricardo
"""

import urllib
import time
import hashlib
import json
import copy
import traceback

from urllib.error import HTTPError

import glb

def call(**kwargs):
    username = glb.username
    password = glb.password
    params = copy.deepcopy(kwargs)
    print(username, password, params)
    return post(username, password, params)
    

def post(username, password, params, url='http://localhost:8080/br_v1'):
    #def post(username, password, params, url='http://localhost:8000/hotel'):
    response = ''
    try:
        timestamp = str(time.time())
        jparams = json.dumps(params)
        password_hash = hashlib.sha1(password).hexdigest()
        hmac = hashlib.sha1(timestamp + jparams + password_hash).hexdigest()
        data = urllib.urlencode({'timestamp': timestamp,
                                 'username': username,
                                 'hmac': hmac,
                                 'params': jparams})
        response = urllib.request.urlopen(url=url, data=data).read()
    except:
        pass           
#    except HTTPError as e:
#        error = e.read()
#        glb.error(json.loads(error))
#        glb.info('ERRO ::: %s' % time.asctime())
#        return ''
        
#    except:
#        glb.error(json.loads(traceback.format_exc()))
#        glb.info('ERRO ::: %s' % time.asctime())
#        return ''

#    glb.info('Ok ::: %s' % time.asctime())
#    glb.error('')
    print(response, 'a')
    return 'asd'
    return json.loads(response)


def teste(password):
    username='admin'
    #password = 'secreta'
    params = {}
    params['method'] = 'usuarios.query'
    params['nome'] = 'ad'
    print(post(username, password, params))


    username='admin'
    #password = 'secreta'
    params = {}
    params['method'] = 'usuarios.authenticate'
    params['nome'] = 'admin'
    print(post(username, password, params))
    
if __name__ == '__main__':
    glb.username='admin'
    glb.password='secreta'
    print(call(method='testes.rpc_teste'))
