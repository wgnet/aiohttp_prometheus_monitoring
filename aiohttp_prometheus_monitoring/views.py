# -*- coding: utf-8 -*-

import aiohttp


async def ping(request):
    return aiohttp.web.Response(body='pong')
