# -*- coding: utf-8 -*-

import asyncio
import aiohttp  # noqa

from aiohttp_prometheus_monitoring.metrics.base import BaseMetric


class HttpMetric(BaseMetric):
    def __init__(self, url, timeout=10, verify_ssl=True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.url = url
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.exc = (aiohttp.ClientError, asyncio.TimeoutError)

    @staticmethod
    async def http_get_status(url, timeout, verify_ssl):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=verify_ssl)) as session:
            async with session.get(url, timeout=timeout) as response:
                return response.status

    async def check(self):
        status = await self.http_get_status(self.url, self.timeout, self.verify_ssl)
        return status == 200
