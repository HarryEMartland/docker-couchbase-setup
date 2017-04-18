# Couchbase Setup

This docker contain can be used to help setup Couchbase.
The initial use case was for disposable environments for testing or developing against.
The container consists of a single python script which reads the environment variables holding the desired setup for couchbase.
Http requests are made to the couchbase server to create a user and buckets using the provided configuration.

## Usage

Included in this project is an example docker-compose file showing how this container could be used.
The environment variables used to set up couchbase are as follows;

#### Global Environment Variables
|      Variable     | Description |
|-------------------|-------------|
|     COUCHBASE_HOST|The host of the couchbase server. May be the name of a couchbase container.|
| COUCHBASE_USERNAME|The admin user for couchbase. Use this to log in to the UI.|
| COUCHBASE_PASSWORD|The password for the admin user.|

#### Bucket Environment Variables

Bucket variables are grouped by a 'bucket key' this is not necessarily the name of the bucket in couchbase.
In the example docker compose file, two buckets are created and so two 'bucket keys' are used.


|                Variable                | Description |
|----------------------------------------|-------------|
|     COUCHBASE_BUCKET_\<bucket key>_NAME|The name of the bucket in couchbase. This is used to access the buckets by applications.|
| COUCHBASE_BUCKET_\<bucket key>_PASSWORD|The password to access the bucket using sasl authentication. May be blank.|