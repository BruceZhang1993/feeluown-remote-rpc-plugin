import logging
import json
from abc import ABC

from feeluown.app import App
from fuocore import library, Library
from fuocore.playlist import PlaybackMode
from fuocore.serializers import serialize
from tornado import ioloop, web
from jsonrpcserver import method, async_dispatch as dispatch

logger = logging.getLogger('jsonrpc')


@method
async def ping():
    return 'pong'


@method
async def current():
    return serialize('json', JsonRpcService.fuoapp.player.current_song) \
        if JsonRpcService.fuoapp.player.current_song else None


@method
async def trackinfo(fuo: str):
    [_, __, provider_identify, ___, sid] = fuo.split('/')
    provider = JsonRpcService.fuoapp.library.get(provider_identify)
    song = provider.Song.get(sid)
    return serialize('json', song) if song else None


@method
async def status():
    fuoapp = JsonRpcService.fuoapp
    return {
        "track": {
            "provider": fuoapp.player.current_song.source,
            "title": fuoapp.player.current_song.title,
            "artists": [artist.name for artist in fuoapp.player.current_song.artists],
            "album": fuoapp.player.current_song.album_name,
            "duration": fuoapp.player.current_song.duration
        } if fuoapp.player.current_song else {},
        "player": {
            "state": fuoapp.player.state.name,
            "volume": fuoapp.player.volume,
            "repeat": int(fuoapp.playlist.playback_mode in (PlaybackMode.one_loop, PlaybackMode.loop)),
            "random": int(fuoapp.playlist.playback_mode == PlaybackMode.random),
            "position": fuoapp.player.position
        },
        "live_lyric": fuoapp.live_lyric.current_sentence
    }


@method
async def live_lyric():
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
