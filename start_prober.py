
# !/usr/bin/env python3

import env
import sys

from src.logger import get_logger
from prometheus_client import start_http_server
from src.probe_scheduler import ProberScheduler
from prober_init import PROBER_LIST, Availability_collection

if len(sys.argv) > 1:
    val = sys.argv[1]
    if val == 'debug':
        logger = get_logger('Debug-MODE-ON', 'DEBUG')
        for prober in PROBER_LIST:
            prober._logger = logger
    else:
        raise ValueError(f"the provided flag {val} is not valid")
else:
    logger = get_logger("ProberScheduler", "info", log_dir=env.log_dir, backup_count=5)

scheduler = ProberScheduler(PROBER_LIST, logger=logger, sanity_interval=6.0)
logger.info(f"Starting Metric endpoint on {env.server_address}:{env.server_port}")
start_http_server(port=env.server_port, addr=env.server_address, registry=Availability_collection)
logger.info("Starting the main Scheduler")
scheduler.start()
