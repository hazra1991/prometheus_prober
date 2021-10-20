import os
import json
import socket
import getpass
from pathlib import Path
from .config_vault import __config__

# get project settings

proj_setting_file = Path(os.environ["PROJECT_SETTINGS_PATH"])
with open(proj_setting_file, "r") as file:
    conf = json.load(file)
    proj_conf = conf['project_setting']

# Gitlab TOKEN

if proj_conf["cred_loc"].lower() in ("cv", "credential vault", "credential_vault"):
    # get credentials from cred vault
    cref = proj_conf["cref"]
    if cref is None or isinstance(cref, int) or len(cref.strip()) == 0:
        raise ValueError(f"cref should be a non empty string not {cref}")
    cred_file = Path('/var/cv') / getpass.getuser() / 'creds' / f"{cref}"
    with open(cred_file, "r") as fd:
        v = json.load(fd)
        TOKEN = v["password"]
elif proj_conf["cred_loc"].lower() in ("env", "environment"):
    TOKEN = __config__['gitlab_env'][proj_conf['gitlab_env'].upper()]['token']
else:
    v = proj_conf["cred_loc"]
    msg = f"unsupported cred_loc value {v}: supports CV for credential vault or ENV for os env"
    raise ValueError(msg)

# system settings

__version__ = proj_conf['version']
server_address = socket.gethostname()
server_port = proj_conf['port']
control_only: bool = proj_conf['control_only']


# Setting up environment

pypi_upload_url = __config__['pypi_env'][proj_conf['pypi_uploader_env'].upper()]

gitlab_api_url = __config__['gitlab_env'][proj_conf['gitlab_env'].upper()]['api']
gitlab_instance = __config__['gitlab_env'][proj_conf['gitlab_env'].upper()]['instance']
gitlab_project_access_token = TOKEN
gitlab_project_id = proj_conf["project_id"].get(server_address)
gitlab_job_id: int = proj_conf["job_id"]

# logging
if len(proj_conf["log_dir"].strip()) > 0:
    log_dir = proj_conf["log_dir"]
else:
    log_dir = Path(os.path.dirname(os.path.dirname(__file__)))/"LOGS"
    log_dir.mkdir(parents=True, exist_ok=True)
