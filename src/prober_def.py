import requests
from .probe_scheduler import BaseProber



class AvailibilityProber(BaseProber):
 
    def __init__(self,name , interval , metric):
        super().__init__(name,metric,interval)
        print(self.get_defined_metric)
        metric = self.get_defined_metric
        self.success =  metric["pypi_success_total"]
        self.failed =  metric["pypi_failed_total"]
        

    def probe(self):
        print("runnint")

        res  = requests.get("http://127.0.0.1:5000/upload")
        if res.status_code == 200:
            print("this is started ")
            # logger()
            self.success.inc()
        else:
            self.failed.inc()
