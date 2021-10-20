# !/usr/bin/env python3

import sys
import os
from pathlib import Path

sys.path.append('/local/data/scratch/prometheus_client-0.11.0')
sys.path.append('/usr/lib/python3.6/site-packages/')

if len(sys.argv) > 1:
    settings_file = sys.argv[1]
    os.environ["PROJECT_SETTINGS_PATH"] = settings_file
else:
    settings_path = Path(os.path.dirname(__file__)) / "prober" / "conf" / "PROJECT_SETTINGS.json"
    os.environ["PROJECT_SETTINGS_PATH"] = str(settings_path)


if __name__ == "__main__":
    from prober.conf import env
    from prober.src.logger import get_logger
    from prometheus_client import start_http_server
    from prober.src.probe_scheduler import ProberScheduler
    from prober.conf.prober_init import PROBER_LIST, Availability_collection

    logger = get_logger("ProberScheduler", "info", log_dir=env.log_dir, backup_count=5)
    logger.info(f"using file {os.environ.get('PROJECT_SETTINGS_PATH')} to populate project settings ")
    scheduler = ProberScheduler(PROBER_LIST, logger=logger, sanity_interval=60.0)
    logger.info(f"Starting Metric endpoint on {env.server_address}:{env.server_port}")
    start_http_server(port=env.server_port, addr=env.server_address, registry=Availability_collection)
    logger.info("Starting the main Scheduler")
    scheduler.start()
