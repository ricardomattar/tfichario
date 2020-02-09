# -*- coding: latin1 -*-

#!/usr/bin/env python

from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.internet import reactor
from twisted.web.server import NOT_DONE_YET

import sys
import time
import threading
import multiprocessing
import uuid
import traceback
import zlib

import logging
import logging.handlers
logger = logging.getLogger()
            
class QueueManager(object):
    def __init__(self, in_queue, out_queue):
        self.in_queue = in_queue
        self.out_queue = out_queue
        
        self.requests = {}

        t = threading.Thread(target = self.replier, args = ())
        t.setDaemon(1)
        t.start()
                                                        
    def replier(self):
        while True:
            try:
                wuid, responseCode, result = self.out_queue.get()
                request = self.requests[wuid]
                del self.requests[wuid]
                reactor.callFromThread(self.send_request, request, responseCode, result)
                logger.debug('.')
                
            except:
                logger.exception('')
            
    def send_request(self, request, responseCode, result):
        #todo: fix request  _disconnected
        # http://stackoverflow.com/questions/10710047/twisted-http-server-error
        #request.setHeader('Content-Type', 'text/html; charset=utf-8')
        request.setHeader('Content-Type', 'text/html; charset=utf-8')
        request.setResponseCode(responseCode)
        request.write(result)
        request.finish()
        
    def enqueue_wu(self, request):
        try:
            wuid = uuid.uuid4().bytes
            self.requests[wuid] = request
            self.in_queue.put( (wuid, request.args) )
            logger.debug('.')
        
        except:
            logger.exception('')


class Root(Resource):
    def render_GET(self, request):
        #pprint(request.__dict__)
        return '''
        <html><body><h1>The twserver!</h1>
        <p>Nothing here yet...</p>
        </body></html>
        '''
        #return 'empty root'

class ResourceManager(Resource):
    def __init__(self, in_queue, out_queue):
        Resource.__init__(self)
        self.queue_manager = QueueManager(in_queue, out_queue)
        
#    def render_GET(self, request):
#        remote_address = (request.client.host, request.client.port)
#        logger.info('%s', remote_address)
#        args = request.args

    def render_POST(self, request):
        self.queue_manager.enqueue_wu(request)
        return NOT_DONE_YET

public_key_pem = ''
class PKPem(Resource):
    def render_GET(self, request):
        return public_key_pem
    
    def render_POST(self, request):
        return public_key_pem
                    
def exec_monitor(workers, period):
    while True:
        time.sleep(period)
        processes = multiprocessing.active_children()
        if len(processes) < workers:
            logger.critical('%s workers missing. rebooting twserver!', workers - len(processes))
            reactor.callFromThread(reactor.stop)

def start_worker(consumer, in_queue, out_queue):
    p = multiprocessing.Process(target = consumer, args=(in_queue, out_queue))
    p.daemon = True
    #p.name = 'Dispatcher-%s' % pn
    logger.info('Starting consumer process %s', p.name)
    p.start()
        
def run(workers = 4, consumer = None, port = 8000, path = 'srv'):
    in_queue = multiprocessing.Queue()
    out_queue = multiprocessing.Queue()
    
    if not consumer:
        logger.critical('No dispatch callback defined')
        #sys.exit(1)
                
    logger.info('Starting queue consumers')
    for pn in range(workers):
        start_worker(consumer, in_queue, out_queue)
        
    emt = threading.Thread(target = exec_monitor, args = (workers, 20))
    emt.setDaemon(1)
    logger.info('Starting execution monitor thread')
    emt.start()
    
    
    root = Resource()
    root.putChild("", Root())
    root.putChild("pem", PKPem())
    root.putChild(path, ResourceManager(in_queue, out_queue))
    
    reactor.listenTCP(port, Site(root))
    logger.info('Starting reactor')
    reactor.run()
    
