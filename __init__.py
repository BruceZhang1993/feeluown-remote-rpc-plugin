# *-- coding: utf-8 --*
__alias__ = 'FeelUOwn JSON RPC Plugin'
__version__ = '0.1.0'
__feeluown_version__ = '3.3.10'
__desc__ = 'Make FeelUOwn support JSONRPC protocol.'

import logging

from feeluown.app import App

from .fuo_remote_rpc.service import JsonRpcService

logger: logging.Logger = logging.getLogger('jsonrpc')
instance: JsonRpcService


def enable(app: App):
    global instance
    instance = JsonRpcService(app)
    instance.start()
    logger.info(__alias__ + ' enabled.')


def disable(app: App):
    global instance
    if instance:
        instance.stop()
    logger.info(__alias__ + ' disabled.')
