# -*- coding: latin1 -*-
"""
Created on Mon Oct  5 02:46:32 2015

@author: ricardo
"""

import traceback

import logging
import logging.handlers
logger = logging.getLogger()


def rpc_teste(params):
    try:
        testea()
        return (200, True)
        
    except:
        return (500, traceback.format_exc())
    
def testea():
    return 5/0    