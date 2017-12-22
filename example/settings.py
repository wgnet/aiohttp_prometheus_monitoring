
MONITORING = {
    'route_metrics': '/metrics',

    'metrics': [
        {
            'name': 'monitoring_redis',
            'description': 'Check redis connection',
            'module': 'aiohttp_prometheus_monitoring.metrics.redis.RedisMetric',
            'sleep_time': 60,
            'params': {
                'host': 'localhost',
                'port': '6379',
            }
        },
    ]
}
