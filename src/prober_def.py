import requests
from requests.exceptions import ConnectionError
from .probe_scheduler import BaseProber
from .utils import retryOnException
import env


class AvailibilityProber(BaseProber):
 
    def __init__(self,name , interval , metric):
        super().__init__(name,metric,interval)
        metric = self.get_defined_metric
        self.success =  metric["pypi_success_total"]
        self.failed =  metric["pypi_failed_total"]
        self.project_id = env.gitlab_project_id
        self.job_id = env.gitlab_job_id
        

    def probe(self):
        print("runnint")
  
        res = self.triggerPypiUploader()
        if res and res.status_code == 200:
            print("Success")
            self.success.inc()
        else:
            self.failed.inc()
            print("Failed")

    @retryOnException(ConnectionError,retry=4,delay=2)
    def triggerPypiUploader(self):
        payload =  {"project_id":self.project_id,"job_id":self.job_id,"control_only":False}
        res  = requests.post(self.pypi_url,data=payload)   
        return res