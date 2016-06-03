import os

import requests

from invoke import task


API_URL = 'https://ci.appveyor.com/api'
TOKEN = os.environ["APPVEYOR_API_TOKEN"]
ACCOUNT_NAME = "lukasa"
PROJECT_NAME = "certitude"
BASE_URL = "https://ci.appveyor.com/api"


@task
def download_artifacts(build_id):
    s = requests.Session()
    s.headers = {
        "Authorization": "Bearer {}".format(TOKEN)
    }

    # Get project build details.
    print "Obtaining artifacts for {}".format(PROJECT_NAME)
    build_details_url = BASE_URL + "/projects/{}/{}/build/{}".format(
        ACCOUNT_NAME, PROJECT_NAME, build_id
    )
    r = s.get(build_details_url, stream=True)
    r.raise_for_status()

    for job in r.json()[u'build'][u'jobs']:
        # Get the artifact list because we don't know what the filename is.
        job_id = job[u'jobId']
        artifacts_url = BASE_URL + "/buildjobs/{}/artifacts/".format(job_id)

        print "Artifacts for {}".format(job_id)
        r = s.get(artifacts_url, stream=True)
        r.raise_for_status()

        artifact_name = r.json()[0][u'fileName']
        artifact = BASE_URL + "/buildjobs/{}/artifacts/{}".format(
            job_id, artifact_name
        )

        print "Downloading {} to {}".format(artifact, artifact_name)
        r = s.get(artifact, stream=True)
        r.raise_for_status()

        with open("{}".format(artifact_name), 'wb') as f:
            for chunk in r.iter_content(4096):
                f.write(chunk)
