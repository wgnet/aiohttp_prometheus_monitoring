#!/usr/bin/env python

import asyncio
import argparse

from aiohttp import web
from aiohttp_prometheus_monitoring import setup_monitoring

import settings


def create_app(loop):
    app = web.Application()
    loop.run_until_complete(setup_monitoring(settings.MONITORING, app))
    return app


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Example Http Worker', add_help=True)
    parser.add_argument('-p', '--port', required=False, default=9000, type=int, help='port for http')
    parser.add_argument('--host', required=False, default='0.0.0.0', type=str, help='host for http')
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    web.run_app(create_app(loop), host=args.host, port=args.port)
