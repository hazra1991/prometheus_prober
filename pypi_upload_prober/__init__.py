"""The version is taken at the runtime based on the release tag given and the gitlab variable CU_COMMIT_TAG"""

import os

__version__ = (
    os.environ.get('CI_COMMIT_TAG', 'snapshot')
    .replace('release-', '')
    .replace('dev-', '')
    .replace('uat-', '')
)