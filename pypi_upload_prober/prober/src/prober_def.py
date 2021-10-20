import requests
from ..conf import env
import time

from requests.exceptions import ConnectionError
from .probe_scheduler import BaseProber
from .utils import retryOnException, retryUntilTrue
from .errors import JobError, JobNotFoundError, RetryTimedOut


class AvailabilityProber(BaseProber):
 
    def __init__(self, name, metric, interval,log_dir=None):
        super().__init__(name, metric, interval, log_dir=log_dir)
        metric = self.get_defined_metric
        self.log = self.logger
        self.success = metric["pypi_success_total"]
        self.failed = metric["pypi_failed_total"]
        self.project_id = env.gitlab_project_id
        self.pypi_url = env.pypi_upload_url
        self.gitlab_instance = env.gitlab_instance
        self.control = env.control_only
        self.prober_run_count = 0
        self.prober_start_time = time.ctime()
        self.gitlab_api = env.gitlab_api_url
        self.job_id = self.get_latest_jobid()

    def probe(self):
        self.prober_run_count += 1
        self.log.info("\n=========================================")
        self.log.info(f"Total run for prober:- {self._name} since {self.prober_start_time} is {self.prober_run_count}")
        self.log.info(f"triggering new job for job id : -{self.job_id}")
        try:
            if self.retrigger_and_update_job() is True:
                self.log.info(f" New job triggering done ID :- {self.job_id}")
            if self.get_job_status():
                try:
                    res = self.triggerPypiUploader()
                except ConnectionError:
                    self.failed.inc()
                    self.log.exception("Failed to connect to PyPi uploader")
                    return
            else:
                raise JobError()
        except (JobError, RetryTimedOut):
            self.success.inc()
            self.log.exception("gitlab error caught as , publishing success metric")
            return
        if res:
            self.log.info(f"{res.text} {res.status_code}, artifact was uploaded , publishing Metric")
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

    @retryUntilTrue(timeout=240.0, delay=10)
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
            elif status in {"failed", "canceled"}:
                raise JobError(f"The triggered job id {self.job_id} current status is :- {status},Please refer logs")
            else:
                self.log.warning(f"No valid response received for job {self.job_id} status {status}")
        else:
            self.log.error(f"Failed request to url {url}\n returned status code {res.status_code}: - {res.content}")

    def get_latest_jobid(self):
        url = f"{self.gitlab_api}/projects/{self.project_id}/jobs"
        self.log.info(f"requesting job id to url :- {url}")
        res = requests.get(url, headers={"PRIVATE-TOKEN": env.gitlab_project_access_token}, verify=False)
        if res:
            self.log.info("Fetching latest success job stage: build")
            job_list = res.json()
            for job in job_list:
                if job.get('stage') == 'build' and job.get('status') == "success" and job.get('tag') is True:
                    job_id = job['id']
                    pipeline_id = job['pipeline']['id']
                    msg = "latest job id with stage:build, status:success, tag:True is"
                    self.log.info(f'\n=================\n {msg}::- {job_id}\n===pipeline - {pipeline_id}==============')
                    return job_id
            msg = "[x] ==================================\n No successful build job found for the project"
            self.log.error(f'{msg}:- {self.project_id}\n==================')
            raise JobNotFoundError(msg)
        else:
            msg = f"server url {url} did not respond with a valid code {res.status_code} , {res.text}"
            self.log.error(f"server returned status {res.status_code} ,msg {res.text},{msg}")
            raise ConnectionError(msg)

