from enum import Enum
from prometheus_client import Histogram
from prometheus_client.metrics import Counter
from .metric_base import Base


class Status(Enum):
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'
    def __str__(self):
        return str(self.value)


class Metrics(Base):
    """ set the metrics needed to be included in the Main prober ,
    Best practive is to define the fun name as the metric name and the return type should be a metric object """

    @Base.set_metric
    def pypi_success_total(self):          
        return Counter(
            name='pypi_total_success',
            documentation='Numebr times the pipy uploder runs',
            # labelnames=['status'],
            registry=self.get_collection_registry,
        )
    
    @Base.set_metric
    def pypi_failed_total(self):
        return Counter(
            name='pypi_total_run',
            documentation='Numebr times the pipy uploder runs',
            # labelnames=['status'],
            registry=self.get_collection_registry,
        )

    # @Base.set_metric
    def histogram(self):
        _second_buckets = (
            10.0, 30.0, 60.0, 120.0, 300.0,  # [10s, 300s/5m]
            float('inf')                     # > 300s/5m
        )

        return Histogram(
            name='run_latency_seconds',
            documentation='Ltency',
            registry=self.get_collection_registry,
            buckets=_second_buckets,
            labelnames=['stage'])