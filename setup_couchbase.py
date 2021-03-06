import os

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

BUCKET_PREFIX = "COUCHBASE_BUCKET_"
BUCKET_NAME_SUFFIX = "_NAME"
BUCKET_PASSWORD_SUFFIX = "_PASSWORD"
BUCKET_VIEWS_SUFFIX = "_VIEWS"

couchbase_host = os.environ['COUCHBASE_HOST']
couchbase_port = os.environ['COUCHBASE_PORT']
couchbase_username = os.environ['COUCHBASE_USERNAME']
couchbase_password = os.environ['COUCHBASE_PASSWORD']

couchbase_down = True

s = requests.Session()
retries = Retry(total=10, backoff_factor=1, status_forcelist=[502, 503, 504, 400, 500])
s.mount('http://', HTTPAdapter(max_retries=retries))

print("waiting for couchbase")

s.get("http://" + couchbase_host + ":" + couchbase_port + "/")

print("creating user")

print(s.post("http://" + couchbase_host + ":" + couchbase_port + "/settings/web", data={
    "username": couchbase_username,
    "password": couchbase_password,
    "port": "8091"
}).text)


def create_views():
    for (designDocument) in os.listdir(viewsDir + "/view"):
        print("Creating design document " + designDocument)
        views = {}
        for (view) in os.listdir(viewsDir + "/view/" + designDocument):
            print("Creating view " + view)

            with open(viewsDir + "/view/" + designDocument + "/" + view) as viewFile:
                javascript = viewFile.read()
                views[view[:-3]] = {"map": javascript}
        print(s.put(
            "http://" + couchbase_host + ":8092/" + bucketName + "/_design/" + designDocument,
            auth=auth, json={"views": views}).text)


def create_spacial_views():
    for (designDocument) in os.listdir(viewsDir + "/spacial"):
        print("Creating spacial design document " + designDocument)
        views = {}
        for (view) in os.listdir(viewsDir + "/spacial/" + designDocument):
            print("Creating spacial view " + view)

            with open(viewsDir + "/spacial/" + designDocument + "/" + view) as viewFile:
                javascript = viewFile.read()
                views[view[:-3]] = javascript
        print(s.put(
            "http://" + couchbase_host + ":8092/" + bucketName + "/_design/" + designDocument,
            auth=auth, json={"spatial": views}).text)


for env in os.environ:
    auth = (couchbase_username, couchbase_password)
    env = str(env)
    if env.startswith(BUCKET_PREFIX) and env.endswith(BUCKET_NAME_SUFFIX):
        bucketKey = env[len(BUCKET_PREFIX):-len(BUCKET_NAME_SUFFIX)]
        bucketName = os.environ[BUCKET_PREFIX + bucketKey + BUCKET_NAME_SUFFIX]
        bucketPassword = os.environ[BUCKET_PREFIX + bucketKey + BUCKET_PASSWORD_SUFFIX]
        print("Creating bucket " + bucketKey + " As " + bucketName)

        print(s.post("http://" + couchbase_host + ":" + couchbase_port + "/pools/default/buckets",
                     data={
                         'name': bucketName,
                         'ramQuotaMB': "200",
                         'saslPassword': bucketPassword,
                         'authType': 'sasl'
                     }, auth=auth).text)

        viewsDir = os.environ.get(BUCKET_PREFIX + bucketKey + BUCKET_VIEWS_SUFFIX)
        if (viewsDir):
            create_views()
            create_spacial_views()

print("couchbase setup")
