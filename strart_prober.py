
#!/usr/bin/env python3

from prometheus_client import start_http_server
from src.probe_scheduler import ProberScheduler
from prober_init import PROBER_LIST,Availibility_collection
import env

scheduler = ProberScheduler(PROBER_LIST)
# logger.info('starting metrics endpoint')
start_http_server(port=8000,addr=env.server_address,registry=Availibility_collection)
scheduler.start()