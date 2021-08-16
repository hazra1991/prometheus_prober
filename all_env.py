import os

__config__ = {
      "uploader_env": {
        "uploader_DEV": "http://dev.uploader.com/upload",
        "uploader_UAT": "http://uat.uploader.com/upload",
        "uploader_PROD": "http://prod.uploader.com/upload"
      },
      "gitlab_env": {

        "GITLAB_QA": {
          "instance": "QA",
          "api": "https://gitlab-qa.com/api/v4",
          "token": ""
        },

        "GITLAB_PROD": {
          "instance": "PROD",
          "api": "https://gitlab.com/api/v4",
          "token": ""
        },

        "GITLAB_AWS_QA": {
          "instance": "AWS_QA",
          "api": "https://gitlab.qa.aws.com/api/v4",
          "token": ""
        },
        "GITLAB_AWS_PROD": {
          "instance": "AWS_PROD",
          "api": "https://gitlab.aws.com/api/v4",
          "token": ""
        }

      }
}
