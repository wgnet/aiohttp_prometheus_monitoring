# -*- coding: utf-8 -*-

import aioamqp

from aiohttp_prometheus_monitoring.metrics.base import BaseMetric


class AmqpMetric(BaseMetric):
    def __init__(self, user, password, host, port=5672, vhost='/', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.url = 'amqp://{user}:{password}@{host}:{port}/{vhost}'.format(
            user=user,
            password=password,
            host=host,
            port=port,
            vhost=vhost
        )
        self.exc = aioamqp.exceptions.AioamqpException

    @staticmethod
    async def connect_amqp(url):
        transport, protocol = await aioamqp.from_url(url)
        return transport, protocol

    async def check(self):
        transport, protocol = await self.connect_amqp(self.url)
        is_connected = protocol is not None and protocol.state == aioamqp.protocol.OPEN and transport is not None

        if is_connected:
            await protocol.close()

        return is_connected
