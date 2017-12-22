# -*- coding: utf-8 -*-

import aiopg
from psycopg2 import DatabaseError

from aiohttp_prometheus_monitoring.metrics.base import BaseMetric


class PostgresMetric(BaseMetric):
    def __init__(self, database, user, password, host, port=5432, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dsn = 'dbname={database} user={user} password={password} host={host} port={port}'.format(**{
            'database': database,
            'user': user,
            'password': password,
            'host': host,
            'port': port
        })
        self.exc = DatabaseError

    @staticmethod
    async def select_one(dsn):
        async with aiopg.create_pool(dsn) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute('SELECT 1')
                    result = []
                    async for row in cur:
                        result.append(row)
                    return result

    async def check(self):
        response = await self.select_one(self.dsn)
        return response == [(1,)]
