---
title: Integrate TiDB Vector Search with SQLAlchemy
summary: Learn how to integrate TiDB Vector Search with SQLAlchemy to store embeddings and perform semantic searches.
---

# Integrate TiDB Vector Search with SQLAlchemy

This tutorial walks you through how to use [SQLAlchemy](https://www.sqlalchemy.org/) to interact with [TiDB Vector Search](/tidb-cloud/vector-search-overview.md), store embeddings, and perform vector search queries.

> **Note**
>
> TiDB Vector Search is only available for TiDB (>= v8.4) and [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless). It is not available for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated).

## Prerequisites

To complete this tutorial, you need:

- [Python 3.8 or higher](https://www.python.org/downloads/) installed.
- [Git](https://git-scm.com/downloads) installed.
- A TiDB Cloud Serverless cluster. Follow [creating a TiDB Cloud Serverless cluster](/tidb-cloud/create-tidb-cluster-serverless.md) to create your own TiDB Cloud cluster if you don't have one.

## Run the sample app

You can quickly learn about how to integrate TiDB Vector Search with SQLAlchemy by following the steps below.

### Step 1. Clone the repository

Clone the `tidb-vector-python` repository to your local machine:

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### Step 2. Create a virtual environment

Create a virtual environment for your project:

```bash
cd tidb-vector-python/examples/orm-sqlalchemy-quickstart
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3. Install the required dependencies

Install the required dependencies for the demo project:

```bash
pip install -r requirements.txt
```

Alternatively, you can install the following packages for your project:

```bash
pip install pymysql python-dotenv sqlalchemy tidb-vector
```

### Step 4. Configure the environment variables

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your environment.

   - **Connection Type** is set to `Public`.
   - **Branch** is set to `main`.
   - **Connect With** is set to `SQLAlchemy`.
   - **Operating System** matches your environment.

   > **Tip:**
   >
   > If your program is running in Windows Subsystem for Linux (WSL), switch to the corresponding Linux distribution.

4. Click the **PyMySQL** tab and copy the connection string.

   > **Tip:**
   >
   > If you have not set a password yet, click **Generate Password** to generate a random password.

5. In the root directory of your Python project, create a `.env` file and paste the connection string into it.

   The following is an example for macOS:

   ```dotenv
   TIDB_DATABASE_URL="mysql+pymysql://<prefix>.root:<password>@gateway01.<region>.prod.aws.tidbcloud.com:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
   ```

### Step 5. Run the demo

```bash
python sqlalchemy-quickstart.py
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

from sqlalchemy import Column, Integer, create_engine, Text
from sqlalchemy.orm import declarative_base, Session
from tidb_vector.sqlalchemy import VectorType

dotenv.load_dotenv()

tidb_connection_string = os.environ['TIDB_DATABASE_URL']
engine = create_engine(tidb_connection_string)
```

#### Define a vector column

Create a table with a column named `embedding` that stores a 3-dimensional vector.

```python
Base = declarative_base()

class Document(Base):
    __tablename__ = 'sqlalchemy_demo_documents'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    embedding = Column(VectorType(3))
```

### Store documents with embeddings

```python
with Session(engine) as session:
   session.add(Document(content="dog", embedding=[1, 2, 1]))
   session.add(Document(content="fish", embedding=[1, 2, 4]))
   session.add(Document(content="tree", embedding=[1, 0, 0]))
   session.commit()
```

### Search the nearest neighbor documents

Search for the top-3 documents that are semantically closest to the query vector `[1, 2, 3]` based on the cosine distance function.

```python
with Session(engine) as session:
   distance = Document.embedding.cosine_distance([1, 2, 3]).label('distance')
   results = session.query(
      Document, distance
   ).order_by(distance).limit(3).all()
```

### Search documents within a certain distance

Search for documents whose cosine distance from the query vector `[1, 2, 3]` is less than 0.2.

```python
with Session(engine) as session:
    distance = Document.embedding.cosine_distance([1, 2, 3]).label('distance')
    results = session.query(
        Document, distance
    ).filter(distance < 0.2).order_by(distance).limit(3).all()
```

## See also

- [Vector Data Types](/tidb-cloud/vector-search-data-types.md)
- [Vector Search Index](/tidb-cloud/vector-search-index.md)
