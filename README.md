# PyPI Upload Prober

Probes ,creates and exposes metrics for the [pypi_uploader_service](https://gitlab.gs.com/dx/py-eng/pypi-upload)

Dependencies ```requestes```, ```prometheus_client```, ```python3.7+```

```
pip install -r requirement.txt
```
Project Configs :- [pypi-upload-prober-config](https://gitlab.aws.site.gs.com/dx/py-eng/pypi-upload-prober-config)  
Monitoring Cofigs :- [pypi-prober-monitoring-config](https://gitlab.gs.com/dx/py-eng/sandbox/pypi-prober-monitoring-config)  
Artifact generator :- [pypi-uploader-prober-artifact-generator](https://gitlab.aws.site.gs.com/dx/py-eng/examples/pypi-uploader-prober-artifact-generator)  
Confluence :- [click here](https://confluence.site.gs.com/display/TECHPY/GSINET+PyPi+Uploader+User+Journey+and+SLO+table)

## Quick start
```export PYTHONPATH=${PWD}``` export python path if program does not start 
* The Entry point is **start_prober.py** just ```python start_prober.py``` . For custom settings files use ```python start_prober.py /path/to/PROJECT_SETTINHS.json```.  
* The required projects env settings can be done in ```PROJECT_SETTINGS.json``` by default 
* **The configuration for the current deployment is pulled form the PROJECT_SETTINGS.json defined in** [pypi-upload-prober-config](https://gitlab.aws.site.gs.com/dx/py-eng/pypi-upload-prober-config) 
Example:-
```json
{
  "project_setting": {
    "version": "1.0.0",
    "pypi_uploader_env": "PYPI_PROD",
    "gitlab_env": "GITLAB_AWS_PROD",
    "cred_loc": "CV",
    "cref": "dummycref6a6849236273263735173",
    "server": "",
    "log_dir": "",
    "control_only": false,
    "port": 8000,
    "project_id": 14012,
    "job_id": 23000050
  }
}
``` 
* **The project settings should be in the above format . Removing any key might result in critical errors**  
* For new / edit old environment  can be  done in ```config_vault.py``` then can be added into the project in ```env.py```

## General usage / components

The main probers working are defined in the ```src/prober_def.py```, the metrices are defined in ```src/metric.py```, probers are instantiated and set in the ```prober_init.py```, and the environment variables are defined int ```env.py```,the peoject settings are in ```PROJECT_SETTINGS.json```

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
from pypi_upload_prober.prober.src.probe_scheduler import ProberScheduler
from pypi_upload_prober.prober.conf import PROBER_LIST,Availibility_collection

scheduler = ProberScheduler(PROBER_LIST)
start_http_server(port=8000,addr='localhost',registry=Availibility_collection)
scheduler.start()
```