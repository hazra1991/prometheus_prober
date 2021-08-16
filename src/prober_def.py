import requests
import env
import time
import json
import os

from shutil import copy
from requests.exceptions import ConnectionError
from .probe_scheduler import BaseProber
from .utils import retryOnException, retryUntilTrue
from .errors import JobError


class AvailabilityProber(BaseProber):
 
    def __init__(self, name, metric, interval,log_dir=None):
        super().__init__(name, metric, interval, log_dir=log_dir)
        metric = self.get_defined_metric
        self.success = metric["pypi_success_total"]
        self.failed = metric["pypi_failed_total"]
        self.project_id = env.gitlab_project_id
        self.pypi_url = env.pypi_upload_url
        self.job_id = env.gitlab_job_id
        self.gitlab_instance = env.gitlab_instance
        self.control = env.control_only
        self.prober_run_count = 0
        self.prober_start_time = time.ctime()
        self.gitlab_api = env.gitlab_api_url
        self.log = self.logger
        self.PROJECT_SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))

    def probe(self):
        self.prober_run_count += 1
        self.log.info(f"Total run for prober:- {self._name} since {self.prober_start_time} is {self.prober_run_count}")
        self.log.info(f"triggering new job for job id : -{self.job_id}")
        if self.retrigger_and_update_job() is True:
            setting_file = f"{self.PROJECT_SETTINGS_PATH}/PROJECT_SETTINGS.json"
            copy(setting_file, f"{self.PROJECT_SETTINGS_PATH}/PROJECT_SETTINGS.json.bak")
            self.log.info("saving job id to PROJECT_SETTINGS.json")
            with open(setting_file, 'w') as file:
                p = env.conf
                p['project_setting']['job_id'] = self.job_id
                json.dump(p, file, indent=2)
            self.log.info("job id saved to PROJECT_SETTINGS.json")
        self.log.info(f" New job triggering done ID : -{self.job_id}")
        if self.get_job_status():
            res = self.triggerPypiUploader()
        else:
            raise JobError()
        if res and res.status_code == 200:
            self.log.info(f"{res.text} , artifact was uploaded , publishing Metric")
            self.success.inc()
        else:
            self.failed.inc()
            self.log.critical(f"upload failed {res.text} , {res.status_code}, publishing failed metric")

    def triggerPypiUploader(self):
        payload = {
            "project_id": self.project_id,
            "job_id": self.job_id,
            "gitlab_instance": self.gitlab_instance,
            "controls_only": self.control
        }
        self.log.info(f"Request POST to {self.pypi_url} with params: {payload}")
        res = requests.post(self.pypi_url, data=payload)
        return res

    @retryOnException(ConnectionError, retry=1, delay=2)
    def retrigger_and_update_job(self):
        trigger_job_api = f"{self.gitlab_api}/projects/{self.project_id}/jobs/{self.job_id}/retry"
        self.log.info(f"Requesting API {trigger_job_api},.Triggering job")
        res = requests.post(trigger_job_api, headers={"PRIVATE-TOKEN": env.gitlab_project_access_token}, verify=False)
        self.log.info(f"Returned status code :{res.status_code}")
        if res:
            self.job_id = res.json()['id']
            return True
        else:
            self.log.critical(f"\n====triggering failed code {res.status_code} ,message: {res.content}")
            raise JobError(str(res.content))

    @retryUntilTrue(timeout=120.0, delay=10)
    def get_job_status(self):
        url = f"{self.gitlab_api}/projects/{self.project_id}/jobs/{self.job_id}"
        res = requests.get(url, headers={"PRIVATE-TOKEN": env.gitlab_project_access_token}, verify=False)
        if res:
            status = res.json()['status']
            self.log.info(f"job {self.job_id} status {status} ")
            if status == "success":
                return True
            elif status == "pending":
                return False
            elif status == "running":
                return False
            elif status == "failed":
                raise JobError(f"The triggered job id {self.job_id} failed,Please refer logs")
            else:
                self.log.warning(f"No valid response received for job {self.job_id} status {status}")
        else:
            self.log.error(f"Failed request to url {url}\n returned status code {res.status_code}: - {res.content}")
