import os
import json
from pathlib import Path
from all_env import __config__

with open("PROJECT_SETTINGS.json", "r") as file:
    conf = json.load(file)
    proj_conf = conf['project_setting']

__version__ = proj_conf['version']
server_address = proj_conf['server']
server_port = proj_conf['port']
control_only: bool = proj_conf['control_only']

# Setting up environment

pypi_upload_url = __config__['uploader_env'][proj_conf['uploader_env'].upper()]

gitlab_api_url = __config__['gitlab_env'][proj_conf['gitlab_env'].upper()]['api']
gitlab_instance = __config__['gitlab_env'][proj_conf['gitlab_env'].upper()]['instance']
gitlab_project_access_token = __config__['gitlab_env'][proj_conf['gitlab_env'].upper()]['token']
gitlab_project_id = proj_conf["project_id"]
gitlab_job_id: int = proj_conf["job_id"]

# logging
if len(proj_conf["log_dir"].strip()) > 0:
    log_dir = proj_conf["log_dir"]
else:
    log_dir = Path(os.path.dirname(__file__))/"LOGS"
    log_dir.mkdir(parents=True, exist_ok=True)

