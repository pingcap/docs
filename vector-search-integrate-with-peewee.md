---
title: Integrate TiDB Vector Search with peewee
summary: Learn how to integrate TiDB Vector Search with peewee to store embeddings and perform semantic searches.
---

# Integrate TiDB Vector Search with peewee

This tutorial walks you through how to use [peewee](https://docs.peewee-orm.com/) to interact with the [TiDB Vector Search](/tidb-cloud/vector-search-overview.md), store embeddings, and perform vector search queries.

> **Note**
>
> TiDB Vector Search is currently in beta and only available for [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters.

## Prerequisites

To complete this tutorial, you need:

- [Python 3.8 or higher](https://www.python.org/downloads/) installed.
- [Git](https://git-scm.com/downloads) installed.
- A TiDB Serverless cluster. Follow [creating a TiDB Serverless cluster](/tidb-cloud/create-tidb-cluster-serverless.md) to create your own TiDB Cloud cluster if you don't have one.

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

For your existing project, you can install the following packages:

```bash
pip install peewee pymysql python-dotenv tidb-vector
```

### Step 4. Configure the environment variables

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

    - **Endpoint Type** is set to `Public`.
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

#### Define a vector column optimized with index

Define a 3-dimensional vector column and optimize it with a [vector search index](/tidb-cloud/vector-search-index.md) (HNSW index).

```python
class DocumentWithIndex(Model):
    class Meta:
        database = db
        table_name = 'peewee_demo_documents_with_index'

    content = TextField()
    embedding = VectorField(3, constraints=[SQL("COMMENT 'hnsw(distance=cosine)'")])
```

TiDB will use this index to accelerate vector search queries based on the cosine distance function.

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

- [Vector Data Types](/tidb-cloud/vector-search-data-types.md)
- [Vector Search Index](/tidb-cloud/vector-search-index.md)
