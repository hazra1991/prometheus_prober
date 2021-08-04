
from prometheus_client import CollectorRegistry, start_http_server
from src.probe_scheduler import ProberScheduler
from src.prober_test import Prober
from src.metric import Metrics


registry = CollectorRegistry(auto_describe=True)

probers = [
        Prober(
            name = "prober1",
            interval = 3,
            metric=Metrics(registry),
            
        ),
        # Prober()
    ]

scheduler = ProberScheduler(*probers)
# logger.info('starting metrics endpoint')
start_http_server(8000, registry=registry)
scheduler.start()