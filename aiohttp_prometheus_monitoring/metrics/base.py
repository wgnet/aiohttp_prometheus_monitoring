# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__package__)


class BaseMetric:
    collector = None
    exc = ()

    def __init__(self, collector):
        self.collector = collector

    async def check(self) -> bool:
        raise NotImplemented

    async def run_check(self):
        try:
            ok = await self.check()
            self.collector.set(int(ok))
        except self.exc as e:
            logger.exception(e)
            self.collector.set(0)
        except Exception as e:
            logger.exception(e)
            self.collector.set(-1)
