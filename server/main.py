#!/usr/bin/python3

import os
import time
import threading
import logging
import logging.handlers

import aiohttp
from aiohttp import web
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import hbr
import glb

logger = logging.getLogger('root')

LOG_FILENAME = 'registro.log'
logger.setLevel(logging.INFO)
#logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# formatter = logging.Formatter('%(asctime)s;%(levelname)-8s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
# formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s",
                            #   "%Y-%m-%d %H:%M:%S")
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10000000, backupCount=10)
handler.setFormatter(formatter)
logger.addHandler(handler)

serverdir = os.path.dirname(__file__)
static_dir = os.path.join(serverdir, 'static')

threadlist = []
period = 60


def message_dispatch():
    while True:
        try:
            message = glb.websocket_messages.get()
            for ws in glb.ws_list:
                if not ws.closed:
                    ws.send_str(message)
                else:
                    glb.ws_list.remove(ws)
        except:
            logger.exception("")

async def index(request):
    return web.HTTPFound(os.path.join('static', 'index.html'))

async def teste(request):
    return web.Response(text="Hello World. This is a shitty world indeed! Whatever it is anyway...")

async def br(request):
    data = await request.json()
    logger.info(data)
    response_code, result = hbr.consumer.call(data)
    if response_code == 200:
        return web.Response(text=result)
    elif response_code == 401:
        raise aiohttp.web.HTTPUnauthorized(text=result)
    else:
        raise aiohttp.web.HTTPServerError()

async def timestamp(request):
    return web.Response(text=str(int(time.time())))

async def websocket_handler(request):
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)

    glb.ws_list.append(ws)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                glb.ws_list.remove(ws)
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')

    return ws

def start_httpserver():
    logger.info('Starting http server')
    app = web.Application()

    app.router.add_get('/', index)
    app.router.add_get('/teste', teste)
    app.router.add_get('/timestamp', timestamp)
    app.router.add_static('/static/',
                          path=static_dir,
                          name='static')
    app.router.add_post('/brv1', br)
    app.router.add_route('GET', '/ws', websocket_handler)
    # app.router.add_get('/{name}', handle)

    # ==============================================================================
    # app.router.add_static('/',
    #                       '/home/ricardo/Dropbox/spyder3/horus/static/',
    #                       name='static',
    #                       show_index=True)
    #
    # ==============================================================================

    web.run_app(app, port=8080)

def run():
    start_httpserver()

if __name__ =="__main__":
    run()