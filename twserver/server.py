# -*- coding: utf-8 -*-
import os
import sys
import logging
import logging.handlers

LOG_FILENAME = 'registro.log'
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(filename)s %(module)s %(funcName)s %(levelname)-8s %(message)s')
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10000000, backupCount=10)
handler.setFormatter(formatter)
logger.addHandler(handler)



from httpserver import httpserver
import hbr

if __name__ == '__main__':
    httpserver.run(workers = 8, consumer = hbr.consumer, port = 8000, path = 'hotel')
