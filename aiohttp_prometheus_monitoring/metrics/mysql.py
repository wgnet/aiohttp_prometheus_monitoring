import aiomysql

from pymysql.err import DatabaseError

from aiohttp_prometheus_monitoring.metrics.base import BaseMetric


class MySQLMetric(BaseMetric):
    def __init__(self, database, user, password, host, port=3006, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.connection_params = {
            'db': database,
            'user': user,
            'password': password,
            'host': host,
            'port': port
        }
        self.exc = DatabaseError

    @staticmethod
    async def select_one(connection_params):
        async with aiomysql.create_pool(**connection_params) as pool:
            async with pool.get() as conn:
                async with conn.cursor() as cur:
                    await cur.execute('SELECT 1;')
                    result = await cur.fetchall()
                    return result

    async def check(self):
        response = await self.select_one(self.connection_params)
        return response == ((1,),)
