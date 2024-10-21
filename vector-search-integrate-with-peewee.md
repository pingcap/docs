---
title: Integrate TiDB Vector Search with peewee
summary: Learn how to integrate TiDB Vector Search with peewee to store embeddings and perform semantic searches.
---

# Integrate TiDB Vector Search with peewee

This tutorial walks you through how to use [peewee](https://docs.peewee-orm.com/) to interact with the [TiDB Vector Search](/vector-search-overview.md), store embeddings, and perform vector search queries.

<CustomContent platform="tidb">

> **Warning:**
>
> The vector search feature is experimental. It is not recommended that you use it in the production environment. This feature might be changed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

</CustomContent>

> **Note:**
>
> The vector search feature is only available for TiDB Self-Managed clusters and [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) clusters.

## Prerequisites

To complete this tutorial, you need:

- [Python 3.8 or higher](https://www.python.org/downloads/) installed.
- [Git](https://git-scm.com/downloads) installed.
- A TiDB cluster.

<CustomContent platform="tidb">

**If you don't have a TiDB cluster, you can create one as follows:**

- Follow [Deploy a local test TiDB cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](/production-deployment-using-tiup.md) to create a local cluster.
- Follow [Creating a TiDB Cloud Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.

</CustomContent>
<CustomContent platform="tidb-cloud">

**If you don't have a TiDB cluster, you can create one as follows:**

- (Recommended) Follow [Creating a TiDB Cloud Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) to create a local cluster of v8.4.0 or a later version.

</CustomContent>

## Run the sample app

You can quickly learn about how to integrate TiDB Vector Search with peewee by following the steps below.

### Step 1. Clone the repository

Clone the [`tidb-vector-python`](https://github.com/pingcap/tidb-vector-python) repository to your local machine:

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### Step 2. Create a virtual environment

Create a virtual environment for your project:

```bash
cd tidb-vector-python/examples/orm-peewee-quickstart
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3. Install required dependencies

Install the required dependencies for the demo project:

```bash
pip install -r requirements.txt
```

Alternatively, you can install the following packages for your project:

```bash
pip install peewee pymysql python-dotenv tidb-vector
```

### Step 4. Configure the environment variables

Configure the environment variables depending on the TiDB deployment option you've selected.

<SimpleTab>
<div label="TiDB Cloud Serverless">

For a TiDB Cloud Serverless cluster, take the following steps to obtain the cluster connection string and configure environment variables:

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

    - **Connection Type** is set to `Public`.
    - **Branch** is set to `main`.
    - **Connect With** is set to `General`.
    - **Operating System** matches your environment.

    > **Tip:**
    >
    > If your program is running in Windows Subsystem for Linux (WSL), switch to the corresponding Linux distribution.

4. Copy the connection parameters from the connection dialog.

    > **Tip:**
    >
    > If you have not set a password yet, click **Generate Password** to generate a random password.

5. In the root directory of your Python project, create a `.env` file and paste the connection parameters to the corresponding environment variables.

    - `TIDB_HOST`: The host of the TiDB cluster.
    - `TIDB_PORT`: The port of the TiDB cluster.
    - `TIDB_USERNAME`: The username to connect to the TiDB cluster.
    - `TIDB_PASSWORD`: The password to connect to the TiDB cluster.
    - `TIDB_DATABASE`: The database name to connect to.
    - `TIDB_CA_PATH`: The path to the root certificate file.

    The following is an example for macOS:

    ```dotenv
    TIDB_HOST=gateway01.****.prod.aws.tidbcloud.com
    TIDB_PORT=4000
    TIDB_USERNAME=********.root
    TIDB_PASSWORD=********
    TIDB_DATABASE=test
    TIDB_CA_PATH=/etc/ssl/cert.pem
    ```

</div>
<div label="TiDB Self-Managed">

For a TiDB Self-Managed cluster, create a `.env` file in the root directory of your Python project. Copy the following content into the `.env` file, and modify the environment variable values according to the connection parameters of your TiDB cluster:

```dotenv
TIDB_HOST=127.0.0.1
TIDB_PORT=4000
TIDB_USERNAME=root
TIDB_PASSWORD=
TIDB_DATABASE=test
```

If you are running TiDB on your local machine, `TIDB_HOST` is `127.0.0.1` by default. The initial `TIDB_PASSWORD` is empty, so if you are starting the cluster for the first time, you can omit this field.

The following are descriptions for each parameter:

- `TIDB_HOST`: The host of the TiDB cluster.
- `TIDB_PORT`: The port of the TiDB cluster.
- `TIDB_USERNAME`: The username to connect to the TiDB cluster.
- `TIDB_PASSWORD`: The password to connect to the TiDB cluster.
- `TIDB_DATABASE`: The name of the database you want to connect to.

</div>

</SimpleTab>

### Step 5. Run the demo

```bash
python peewee-quickstart.py
```

Example output:

```text
Get 3-nearest neighbor documents:
  - distance: 0.00853986601633272
    document: fish
  - distance: 0.12712843905603044
    document: dog
  - distance: 0.7327387580875756
    document: tree
Get documents within a certain distance:
  - distance: 0.00853986601633272
    document: fish
  - distance: 0.12712843905603044
    document: dog
```

## Sample code snippets

You can refer to the following sample code snippets to develop your application.

### Create vector tables

#### Connect to TiDB cluster

```python
import os
import dotenv

from peewee import Model, MySQLDatabase, SQL, TextField
from tidb_vector.peewee import VectorField

dotenv.load_dotenv()

# Using `pymysql` as the driver.
connect_kwargs = {
    'ssl_verify_cert': True,
    'ssl_verify_identity': True,
}

# Using `mysqlclient` as the driver.
# connect_kwargs = {
#     'ssl_mode': 'VERIFY_IDENTITY',
#     'ssl': {
#         # Root certificate default path
#         # https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters/#root-certificate-default-path
#         'ca': os.environ.get('TIDB_CA_PATH', '/path/to/ca.pem'),
#     },
# }

db = MySQLDatabase(
    database=os.environ.get('TIDB_DATABASE', 'test'),
    user=os.environ.get('TIDB_USERNAME', 'root'),
    password=os.environ.get('TIDB_PASSWORD', ''),
    host=os.environ.get('TIDB_HOST', 'localhost'),
    port=int(os.environ.get('TIDB_PORT', '4000')),
    **connect_kwargs,
)
```

#### Define a vector column

Create a table with a column named `peewee_demo_documents` that stores a 3-dimensional vector.

```python
class Document(Model):
    class Meta:
        database = db
        table_name = 'peewee_demo_documents'

    content = TextField()
    embedding = VectorField(3)
```

### Store documents with embeddings

```python
Document.create(content='dog', embedding=[1, 2, 1])
Document.create(content='fish', embedding=[1, 2, 4])
Document.create(content='tree', embedding=[1, 0, 0])
```

### Search the nearest neighbor documents

Search for the top-3 documents that are semantically closest to the query vector `[1, 2, 3]` based on the cosine distance function.

```python
distance = Document.embedding.cosine_distance([1, 2, 3]).alias('distance')
results = Document.select(Document, distance).order_by(distance).limit(3)
```

### Search documents within a certain distance

Search for the documents whose cosine distance from the query vector `[1, 2, 3]` is less than 0.2.

```python
distance_expression = Document.embedding.cosine_distance([1, 2, 3])
distance = distance_expression.alias('distance')
results = Document.select(Document, distance).where(distance_expression < 0.2).order_by(distance).limit(3)
```

## See also

- [Vector Data Types](/vector-search-data-types.md)
- [Vector Search Index](/vector-search-index.md)
