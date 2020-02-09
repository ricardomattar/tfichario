# -*- coding: latin1 -*-
"""
Created on Sat Aug 15 19:29:24 2015

@author: ricardo
"""

import time
import json
import hashlib
import inspect
import traceback

import logging
import logging.handlers
logger = logging.getLogger()

time_lag = 7200

def update_methods(module):
    m={}
    for o in inspect.getmembers(module):        
        if inspect.isfunction(o[1]):
            if o[0][:4] == 'rpc_':
                m[module.__name__.split('.')[-1] + '.' + o[0]] = o[1]
    return m

import usuarios
import hospedes
import testes

methods = {}
methods.update(update_methods(usuarios))
methods.update(update_methods(hospedes))
methods.update(update_methods(testes))

            
def consumer(in_queue, out_queue):
    while True:
        try:
            wuid, params = in_queue.get()
            timestamp = params['timestamp'][0]
            username = params['username'][0]
            hmac = params['hmac'][0]
            jparams = params['params'][0]
            response_code, result = dispatch(timestamp, username, hmac, jparams)
            out_queue.put( (wuid, response_code, json.dumps(result) ) )
            
        except:
            logger.exception('')
            out_queue.put( (wuid, 500, traceback.format_exc()) )
            
def dispatch(timestamp, username, hmac, jparams):
    try:
        usuario, authenticated = authenticate(timestamp, username, hmac, jparams)
        if not authenticated:
            return (401, 'Unauthorized')
            
        params = json.loads(jparams)
        params['__classe__'] = usuario['classe']
        response_code, result = methods[params['method']](params)
        return (response_code, result)
        
    except:
        logger.exception('')
        return (500, traceback.format_exc())
        
def authenticate(timestamp, username, hmac, params):
    try:    
        logger.info('%s', timestamp)
        if (float(timestamp) + time_lag) < time.time():
            return (None, False)
        rc, usuario = usuarios.find({'nome': username})
        password_hash = usuario['password']
        finalhash = hashlib.sha1(str(timestamp) + params + password_hash).hexdigest()
        if finalhash != hmac:
            return (None, False)
    except:
        logger.exception('')
        return (None, False)
                
    return (usuario, True)
    