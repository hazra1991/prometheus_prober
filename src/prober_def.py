import requests
from .probe_scheduler import BaseProber
import env



class AvailibilityProber(BaseProber):
 
    def __init__(self,name , interval , metric):
        super().__init__(name,metric,interval)
        print(self.get_defined_metric)
        metric = self.get_defined_metric
        self.success =  metric["pypi_success_total"]
        self.failed =  metric["pypi_failed_total"]
        self.build_api =  f"https://gitlab.com/api/v4/projects/{env.gitlab_project_id}/trigger/pipeline"
        self.job_id_url =  f"https://gitlab.com/api/v4/projects/27281625/pipelines/349847744/jobs"

    def probe(self):
        print("runnint")
        pipeline_id, project_id = self.trigger_build_pipeline()
        import time
        time.sleep(56)
        job_id = self.get_job_id(pipeline_id,project_id)

        res  = requests.post("http://127.0.0.1:5000/upload",data={"project_id":project_id,"job_id":job_id})
        if res.status_code == 200:
            print("this is started ")
            # logger()
            self.success.inc()
        else:
            self.failed.inc()
            
    def trigger_build_pipeline(self):
        data = requests.post(self.build_api,headers = {"PRIVATE-TOKEN":"wETWuu9XbtXFzxuph-yr"},data={"token":"57ded7f06a8f596b045a8716a017ab","ref":"stage"}).json()
        return data.get("id"),data.get("project_id")
        # print(data)
    def get_job_id(self,pipeline_id,project_id):
        url = f"https://gitlab.com/api/v4/projects/{project_id}/pipelines/{pipeline_id}/jobs"
        data = requests.get(url,headers = {"PRIVATE-TOKEN":"wETWuu9XbtXFzxuph-yr"}).json()
        print(data)
        return data[0].get('id')

