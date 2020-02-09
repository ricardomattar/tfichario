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
from urllib import parse, request

import glb

def call(**kwargs):
    username = glb.username
    password = glb.password
    params = copy.deepcopy(kwargs)
    print(username, password, params)
    return post(username, password, params)


def post(username, password, params, url='http://localhost:8080/brv1'):
    # def post(username, password, params, url='http://localhost:8000/hotel'):
    response = ''
    try:
        timestamp = str(time.time())
        jparams = json.dumps(params)
        password_hash = hashlib.sha1(password.encode()).hexdigest()
        hmac = hashlib.sha1((timestamp + jparams + password_hash).encode()).hexdigest()
        data = urllib.parse.urlencode({'timestamp': timestamp,
                                 'username': username,
                                 'hmac': hmac,
                                 'params': jparams}).encode()
        req = urllib.request.Request(url=url, data=data)
        response = request.urlopen(req).read()
    except HTTPError as e:
           error = e.read()
           print(error)
           return ''

    except:
        print(traceback.format_exc())
        return ''

    print('Response', response)
    return json.loads(response)


def teste(password):
    username = 'admin'
    # password = 'secreta'
    params = {}
    params['method'] = 'usuarios.query'
    params['nome'] = 'ad'
    print(post(username, password, params))

    username = 'admin'
    # password = 'secreta'
    params = {}
    params['method'] = 'usuarios.authenticate'
    params['nome'] = 'admin'
    print(post(username, password, params))


# if __name__ == '__main__':
#     glb.username = 'admin'
#     glb.password = 'secreta'
#     print(call(method='testes.rpc_teste'))