# -*- coding: utf-8 -*-

import asyncio
import logging
import traceback
from importlib import import_module
from concurrent.futures import ThreadPoolExecutor

from prometheus_client import Gauge, push_to_gateway, REGISTRY
from prometheus_async.aio.web import server_stats

from aiohttp_prometheus_monitoring.utils import PeriodicTask
from aiohttp_prometheus_monitoring.exceptions import WrongConfiguration
from aiohttp_prometheus_monitoring.views import ping


logger = logging.getLogger()


def import_by_path(dotted_path):
    try:
        module_path, object_name = dotted_path.rsplit('.', 1)
    except ValueError:
        raise WrongConfiguration("{} doesn't look like a module path".format(dotted_path))
    try:
        module = import_module(module_path)
    except ImportError as e:
        raise WrongConfiguration("Error importing module {}: {}".format(module_path, e))
    try:
        attr = getattr(module, object_name)
    except AttributeError:
        raise WrongConfiguration('Module "%s" has no "%s" object' % (module_path, object_name))

    return attr


async def init_metrics(config):
    tasks = []
    if 'metrics' in config:
        try:
            for metric in config['metrics']:
                metric_class = import_by_path(metric['module'])

                kwargs = metric['params']
                kwargs['collector'] = Gauge(metric['name'], metric['description'])

                task = PeriodicTask(metric['sleep_time'], metric_class, **kwargs)
                await task.start()
                tasks.append(task)

        except KeyError as e:
            raise WrongConfiguration('Config key {} is mandatory'.format(str(e)))

    return tasks


def init_monitoring_routes(config, app):
    if 'route_ping' in config:
        app.router.add_route('GET', config['route_ping'], ping)

    if 'route_metrics' in config:
        app.router.add_route('GET', config['route_metrics'], server_stats)


async def stop_monitoring_tasks(app):
    for task in app.monitoring_tasks:
        await task.stop()


async def setup_monitoring(config, app=None):
    app.monitoring_tasks = await init_metrics(config)
    app.on_shutdown.append(stop_monitoring_tasks)
    init_monitoring_routes(config, app)


def _push_metrics(job_name, url, grouping_key=None, registry=REGISTRY):
    try:
        push_to_gateway(url, job=job_name, registry=registry, grouping_key=grouping_key)
    except Exception:
        logger.exception(traceback.format_exc())
    else:
        logger.debug('Monitoring metrics pushed for job {}.'.format(job_name))


async def coro(job_name, url, grouping_key):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=2) as executor:
        await loop.run_in_executor(executor, _push_metrics, job_name, url, grouping_key)


async def periodic_coro(sleep_time, job_name, url, grouping_key):
    loop = asyncio.get_event_loop()
    while True:
        with ThreadPoolExecutor(max_workers=2) as executor:
            await loop.run_in_executor(executor, _push_metrics, job_name, url, grouping_key)
            await asyncio.sleep(sleep_time)


def push_metrics(job_name, url, grouping_key=None):
    return asyncio.ensure_future(coro(job_name, url, grouping_key))


def periodic_push_metrics(sleep_time, job_name, url, grouping_key=None):
    return asyncio.ensure_future(periodic_coro(sleep_time, job_name, url, grouping_key))


