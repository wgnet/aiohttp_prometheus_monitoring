# -*- coding: utf-8 -*-

import asyncio
from contextlib import suppress


class PeriodicTask:
    def __init__(self, sleep_time, metric_class, *args, **kwargs):
        self.metric = metric_class(*args, **kwargs)
        self.sleep_time = sleep_time
        self.args = args
        self.kwargs = kwargs
        self.is_started = False
        self._task = None

    async def start(self):
        if not self.is_started:
            self.is_started = True
            self._task = asyncio.ensure_future(self._run())

    async def stop(self):
        if self.is_started:
            self.is_started = False
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task

    async def _run(self):
        while True:
            await self.metric.run_check()
            await asyncio.sleep(self.sleep_time)
