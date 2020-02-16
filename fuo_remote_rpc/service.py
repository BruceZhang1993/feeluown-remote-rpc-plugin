import logging
from abc import ABC

from feeluown.app import App
from fuocore import library
from tornado import ioloop, web
from jsonrpcserver import method, async_dispatch as dispatch

logger = logging.getLogger('jsonrpc')


@method
async def ping():
    return 'pong'


@method
async def lyric():
    return str(JsonRpcService.fuoapp.live_lyric.current_sentence)


class MainHandler(web.RequestHandler, ABC):
    async def post(self):
        request = self.request.body.decode()
        logger.debug('JSONRPC Request: {}'.format(request))
        response = await dispatch(request)
        logger.debug('JSONRPC Response: {}'.format(str(response)))
        if response.wanted:
            self.write(str(response))


class JsonRpcService:
    fuoapp: App
    app: web.Application

    def __init__(self, app: App):
        JsonRpcService.fuoapp = app
        self.app = web.Application([(r'/jsonrpc', MainHandler)])

    def start(self):
        self.app.listen(27000)

    def stop(self):
        logger.debug('not implemented')
