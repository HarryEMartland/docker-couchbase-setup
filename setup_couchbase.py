import os
import requests
import time

BUCKET_PREFIX = "COUCHBASE_BUCKET_"
BUCKET_NAME_SUFFIX = "_NAME"
BUCKET_PASSWORD_SUFFIX = "_PASSWORD"

couchbase_host = os.environ['COUCHBASE_HOST']
couchbase_port = os.environ['COUCHBASE_PORT']
couchbase_username = os.environ['COUCHBASE_USERNAME']
couchbase_password = os.environ['COUCHBASE_PASSWORD']

couchbase_down = True
print("waiting for couchbase")
while (couchbase_down):
    try:
        requests.get("http://" + couchbase_host + ":" + couchbase_port + "/")
        couchbase_down = False
    except:
        time.sleep(1)

print("creating user")

requests.post("http://" + couchbase_host + ":" + couchbase_port + "/settings/web", data={
    "username": couchbase_username,
    "password": couchbase_password,
    "port": "8091"
})

for env in os.environ:
    auth = (couchbase_username, couchbase_password)
    env = str(env)
    if env.startswith(BUCKET_PREFIX) and env.endswith(BUCKET_NAME_SUFFIX):
        bucketKey = env[len(BUCKET_PREFIX):-len(BUCKET_NAME_SUFFIX)]
        bucketName = os.environ[BUCKET_PREFIX + bucketKey + BUCKET_NAME_SUFFIX]
        bucketPassword = os.environ[BUCKET_PREFIX + bucketKey + BUCKET_PASSWORD_SUFFIX]
        print("Creating bucket " + bucketKey + " As " + bucketName)

        requests.post("http://" + couchbase_host + ":" + couchbase_port + "/pools/default/buckets", data={
            'name': bucketName,
            'ramQuotaMB': "200",
            'saslPassword': bucketPassword,
            'proxyPort': "11214",
            'authType': 'sasl'
        }, auth=auth).raise_for_status()

print("couchbase setup")