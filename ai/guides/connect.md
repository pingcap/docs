---
title: Connect to TiDB
summary: Learn how to connect to a TiDB database using the `pytidb` client.
---

# Connect to TiDB

This guide shows how to connect to a TiDB database using the `pytidb` client.

## Install the dependencies

[`pytidb`](https://github.com/pingcap/pytidb) is a Python client built on [SQLAlchemy](https://sqlalchemy.org/). It provides a series of high-level APIs to help you store and search vector embeddings without writing raw SQL.

To install the Python client, run the following command:

```bash
pip install pytidb
```

## Connect with connection parameters

Choose the steps based on your TiDB deployment type:

<SimpleTab>
<div label="TiDB Cloud Starter">

You can [create a TiDB Cloud Starter cluster](https://tidbcloud.com/free-trial/), and then get the connection parameters from the web console as follows:

1. Navigate to the [Clusters page](https://tidbcloud.com/clusters), and then click the name of your target cluster to go to its overview page.
2. Click **Connect** in the upper-right corner. A connection dialog is displayed, with connection parameters listed.
3. Copy the connection parameters to your code or environment variables.

Example code:

```python title="main.py"
from pytidb import TiDBClient

db = TiDBClient.connect(
    host="{gateway-region}.prod.aws.tidbcloud.com",
    port=4000,
    username="{prefix}.root",
    password="{password}",
    database="test",
)
```

> **Note:**
>
> For TiDB Cloud Starter, [TLS connection to the database](https://docs.pingcap.com/tidbcloud/secure-connections-to-starter-clusters/) is required when using a public endpoint. The `pytidb` client **automatically** enables TLS for TiDB Cloud Starter clusters.

</div>
<div label="TiDB Self-Managed">

Follow [Quick Start with TiDB Self-Managed](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb/#deploy-a-local-test-cluster) to deploy a TiDB cluster for testing.

Example code:

```python title="main.py"
from pytidb import TiDBClient

db = TiDBClient.connect(
    host="{tidb_server_host}",
    port=4000,
    username="root",
    password="{password}",
    database="test",
)
```

> **Note:**
>
> If you are using `tiup playground` to deploy a TiDB cluster for testing, the default host is `127.0.0.1` and the default password is empty.

</div>
</SimpleTab>

Once connected, you can use the `db` object to operate tables, query data, and more.

## Connect with connection string

If you prefer to use a connection string (database URL), you can follow the format based on your deployment type:

<SimpleTab>
<div label="TiDB Cloud Starter">

You can [create a TiDB Cloud Starter cluster](https://tidbcloud.com/free-trial/), and then get the connection parameters from the web console as follows:

1. Navigate to the [Clusters page](https://tidbcloud.com/clusters), and then click the name of your target cluster to go to its overview page.
2. Click **Connect** in the upper-right corner. A connection dialog is displayed with the connection parameters listed.
3. Copy the connection parameters and construct a connection string in the following format:

```python title="main.py"
from pytidb import TiDBClient

db = TiDBClient.connect(
    database_url="mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?ssl_verify_cert=true&ssl_verify_identity=true",
)
```

> **Note:**
>
> For TiDB Cloud Starter, [TLS connection to the database](https://docs.pingcap.com/tidbcloud/secure-connections-to-starter-clusters/) is required when using a public endpoint, so you need to set `ssl_verify_cert=true&ssl_verify_identity=true` in the connection string.

</div>
<div label="TiDB Self-Managed">

You can follow the format below to construct the connection string:

```python title="main.py"
from pytidb import TiDBClient

db = TiDBClient.connect(
    database_url="mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}",
)
```

> **Note:**
>
> If you are using `tiup playground` to deploy a TiDB cluster for testing, the connection string is:
>
> ```
> mysql+pymysql://root:@127.0.0.1:4000/test
> ```

</div>
</SimpleTab>

## Connect with SQLAlchemy DB engine

If your application already has a SQLAlchemy database engine, you can reuse it via the `db_engine` parameter:

```python title="main.py"
from pytidb import TiDBClient

db = TiDBClient(db_engine=db_engine)
```

## Next steps

After connecting to your TiDB database, you can explore the following guides to learn how to work with your data:

- [Working with Tables](/ai/guides/tables.md): Learn how to define and manage tables in TiDB.
- [Vector Search](/ai/guides/vector-search.md): Perform semantic search using vector embeddings.
- [Full-Text Search](/ai/guides/vector-search-full-text-search-python.md): Retrieve documents using keyword-based search.
- [Hybrid Search](/ai/guides/vector-search-hybrid-search.md): Combine vector and full-text search for more relevant results.
