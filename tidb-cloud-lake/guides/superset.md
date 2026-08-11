---
title: Connect to TiDB Cloud Lake with Apache Superset
summary: Learn how to install the TiDB Cloud Lake SQLAlchemy dialect in Apache Superset and connect Superset to a TiDB Cloud Lake warehouse.
---

# Connect to TiDB Cloud Lake with Apache Superset

[Apache Superset](https://superset.apache.org/) is an open-source data exploration and visualization platform. Superset connects to {{{ .lake }}} through the [TiDB Cloud Lake dialect for SQLAlchemy](https://github.com/tidbcloud/lake-sqlalchemy).

## Prerequisites

Before you begin, make sure that you have the following:

- Docker
- A {{{ .lake }}} account, database, and warehouse
- The host, username, password, database, and warehouse name for your connection

For information about obtaining connection information, see [Connect to a Warehouse](/tidb-cloud-lake/guides/warehouse.md#connecting-to-a-warehouse).

## Build a Superset image

The official Superset image does not include the {{{ .lake }}} SQLAlchemy dialect. Create a file named `Dockerfile` with the following content:

```dockerfile
FROM apache/superset

USER root
RUN pip install --no-cache-dir tidbcloudlake-sqlalchemy
USER superset
```

The `tidbcloudlake-sqlalchemy` package installs the required {{{ .lake }}} Python driver as a dependency.

Build the image:

```shell
docker build -t superset-lake .
```

Start a container from the image:

```shell
docker run -d \
    -p 8080:8088 \
    -e "SUPERSET_SECRET_KEY=<your-secret-key>" \
    --name superset \
    superset-lake
```

## Initialize Superset

Create an administrator account:

```shell
docker exec -it superset superset fab create-admin \
    --username admin \
    --firstname Superset \
    --lastname Admin \
    --email admin@example.com \
    --password <admin-password>
```

Apply database migrations:

```shell
docker exec -it superset superset db upgrade
```

Initialize Superset:

```shell
docker exec -it superset superset init
```

Open `http://localhost:8080` and sign in with the administrator account.

## Connect Superset to TiDB Cloud Lake

1. In Superset, select **Settings** > **Data** > **Connect Database**.
2. Select **Other** as the database type.
3. Enter a display name, such as `TiDB Cloud Lake`.
4. Enter the SQLAlchemy URI in the following format:

    ```text
    lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>
    ```

5. Click **Test Connection**.
6. After the connection test succeeds, click **Connect**.

You can now create datasets in Superset from {{{ .lake }}} tables and use them in charts and dashboards.

## Related resources

- [`tidbcloudlake-sqlalchemy` on PyPI](https://pypi.org/project/tidbcloudlake-sqlalchemy/)
- [Apache Superset documentation](https://superset.apache.org/docs/intro)
