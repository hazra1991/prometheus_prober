# PyPI Prober

Probes ,creates and exposes metrics for the [pypi_uploader_service](/urlforpypy)

Dependencies ```requestes```, ```prometheus_client```

```
pip install requestes
pip install prometheus_client

```

## General usage

The main probers working are defined in the ```src/prober_def.py```, the metrices are defined in ```src/metric.py```, probers are instantiated and set in the ```prober_init.py```, and teh environment variables are defined int ```env.py```

* To define metrices, create a metric class or use exixting one inside the ```src/metric.py``` and add all the needed metric as a function with return type as a prometious metric instance.
**All metric should inherit form ```probe_scheduler.Base``` and to set and activate the metric ```@Base.set_metric``` should be used. To get the collection registry use the property ```self.get_collection_registry```

```python
class Metrics(Base):

    @Base.set_metric
    def pypi_total_success(self):          
        return Counter(
            name='pypi_total_success',
            documentation='Numebr times the pipy uploder runs',
            # labelnames=['status'],
            registry=self.get_collection_registry,
        )
```

* Define all the probers in the ```src/prober_def.py``` file as a class ,every prober  should have a unique name and inherit from ```probe_scheduler.Baseprober```.  
**To get the defined metrices into the prober use ```self.get_defined_metric``` the property returns a dictionary of available metric types on which the keys are the function name defined in ```metric.py```** .The method works only after the parent is initialized. 
**The prober should have a ```probe``` function defined.** 
```python
class AvailibilityProber(BaseProber):
 
    def __init__(self,name , interval , metric):
        super().__init__(name,metric,interval)
        metric = self.get_defined_metric
        self.success =  metric["pypi_total_success"]       

    def probe(self):
        """define the logic """
        self.success.inc()

```
 
* Add the defined probers in to the ```src/prober_init.py``` file inside the PROBER_LIST variable, **name**, **interval** and **metric** for the prober to run is required.need to pass the collections Registry in to the Metric  
```python
Availibility_collection = CollectorRegistry(auto_describe=True)
PROBER_LIST = [

    Prober(
        name = "Availibility_prober",
        interval = 6,
        metric=Metrics(Availibility_collection)
]
```
* Schedule the prober and start the http server as shown below.
```python
from prometheus_client import start_http_server
from src.probe_scheduler import ProberScheduler
from prober_init import PROBER_LIST,Availibility_collection

scheduler = ProberScheduler(PROBER_LIST)
start_http_server(port=8000,addr='localhost',registry=Availibility_collection)
scheduler.start()
```