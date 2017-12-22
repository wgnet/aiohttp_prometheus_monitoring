# -*- coding: utf-8 -*-

from importlib import import_module

from prometheus_client import Gauge
from prometheus_async.aio.web import server_stats

from aiohttp_prometheus_monitoring.utils import PeriodicTask
from aiohttp_prometheus_monitoring.exceptions import WrongConfiguration
from aiohttp_prometheus_monitoring.views import ping


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
                kwargs['collector'] = Gauge(metric['name'], metric['description'], None)

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
