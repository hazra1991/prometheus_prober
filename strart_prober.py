
#!/usr/bin/env python3

from prometheus_client import start_http_server
from src.probe_scheduler import ProberScheduler
from prober_init import PROBER_LIST,Availibility_collection

scheduler = ProberScheduler(PROBER_LIST)
# logger.info('starting metrics endpoint')
start_http_server(8000, registry=Availibility_collection)
# start_http_server(8002, registry=registry2)
scheduler.start()