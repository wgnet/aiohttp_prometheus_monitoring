# -*- coding: utf-8 -*-

import aioredis

from aiohttp_prometheus_monitoring.metrics.base import BaseMetric


class RedisMetric(BaseMetric):
    def __init__(self, host, port=6379, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.host = host
        self.port = port
        self.exc = aioredis.RedisError

    @staticmethod
    async def set_redis_value(host, port):
        conn = await aioredis.create_connection((host, port))
        response = await conn.execute('SET', 'test-redis', 'test-redis')

        return conn, response

    async def check(self):
        conn, response = await self.set_redis_value(self.host, self.port)
        conn.close()
        return response == b'OK'
