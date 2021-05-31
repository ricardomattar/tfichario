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

from . import usuarios
from . import hospedes

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


methods = {}
methods.update(update_methods(usuarios))
methods.update(update_methods(hospedes))


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

def call(params):
    timestamp = params['timestamp']
    username = params['username']
    hmac = params['hmac']
    jparams = params['params']
    response_code, result = dispatch(timestamp, username, hmac, jparams)
    return(response_code, json.dumps(result))

def dispatch(timestamp, username, hmac, params):
    try:
        usuario, authenticated = authenticate(timestamp, username, hmac, params)
        if not authenticated:
            return (401, 'Unauthorized')

        #params = json.loads(jparams)
        params['__classe__'] = usuario['classe']
        # response_code, result = methods[params['method']](params)
        response_code, result = methods[params['method']](params, usuario = usuario['nome'])
        return (response_code, result)

    except:
        logger.exception('')
        return (500, traceback.format_exc())

def authenticate(timestamp, username, hmac, params):
    try:
        if (float(timestamp) + time_lag) < time.time():
            return (None, False)
        rc, usuario = usuarios.find({'nome': username})
        password_hash = usuario['password']
        finalhash = hashlib.sha1(str(timestamp).encode() + json.dumps(params).encode() + password_hash.encode()).hexdigest()
        if finalhash != hmac:
            return (None, False)
    except:
        logger.exception('')
        return (None, False)

    return (usuario, True)
