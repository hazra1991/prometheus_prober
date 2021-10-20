import os

__config__ = {
      "pypi_env": {
        "PYPI_DEV": "http://dev.pypi-uploader.site.gs.com/upload",
        "PYPI_UAT": "http://uat.pypi-uploader.site.gs.com/upload",
        "PYPI_PROD": "http://prod.pypi-uploader.site.gs.com/upload"
      },
      "gitlab_env": {

        "GITLAB_QA": {
          "instance": "QA",
          "api": "https://gitlab-qa.gs.com/api/v4",
          "token": os.environ.get('GITLAB_QA_TOKEN', "")
        },

        "GITLAB_PROD": {
          "instance": "PROD",
          "api": "https://gitlab.gs.com/api/v4",
          "token": os.environ.get('GITLAB_PROD_TOKEN', "")
        },

        "GITLAB_AWS_QA": {
          "instance": "AWS_QA",
          "api": "https://gitlab.qa.aws.site.gs.com/api/v4",
          "token": os.environ.get('GITLAB_AWS_QA_TOKEN', "")
        },
        "GITLAB_AWS_PROD": {
          "instance": "AWS_PROD",
          "api": "https://gitlab.aws.site.gs.com/api/v4",
          "token": os.environ.get('GITLAB_AWS_PROD_TOKEN', "")
        }

      }
}
