Run it (python version >= 3.5 required):

    $ pip install aiohttp aiohttp_prometheus_monitoring[redis]
    $ python ./main.py --port=9000

Open http://localhost:9000/metrics 

You will see metrics info like this:
 
    # HELP process_virtual_memory_bytes Virtual memory size in bytes.
    # TYPE process_virtual_memory_bytes gauge
    process_virtual_memory_bytes 288534528.0
    # HELP process_resident_memory_bytes Resident memory size in bytes.
    # TYPE process_resident_memory_bytes gauge
    process_resident_memory_bytes 28561408.0
    # HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
    # TYPE process_start_time_seconds gauge
    process_start_time_seconds 1512033478.94
    # HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
    # TYPE process_cpu_seconds_total counter
    process_cpu_seconds_total 0.23
    # HELP process_open_fds Number of open file descriptors.
    # TYPE process_open_fds gauge
    process_open_fds 11.0
    # HELP process_max_fds Maximum number of open file descriptors.
    # TYPE process_max_fds gauge
    process_max_fds 4096.0
    # HELP python_info Python platform information
    # TYPE python_info gauge
    python_info{implementation="CPython",major="3",minor="6",patchlevel="0",version="3.6.0"} 1.0
    # HELP monitoring_redis Check redis connection
    # TYPE monitoring_redis gauge
    monitoring_redis 1.0

