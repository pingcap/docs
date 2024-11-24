---
title: Integrate TiDB Vector Search with Jina AI Embeddings API
summary: Learn how to integrate TiDB Vector Search with Jina AI Embeddings API to store embeddings and perform semantic search.
---

# Integrate TiDB Vector Search with Jina AI Embeddings API

This tutorial walks you through how to use [Jina AI](https://jina.ai/) to generate embeddings for text data, and then store the embeddings in TiDB vector storage and search similar texts based on embeddings.

> **Note**
>
> TiDB Vector Search is only available for TiDB (>= v8.4) and [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless). It is not available for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated).

## Prerequisites

To complete this tutorial, you need:

- [Python 3.8 or higher](https://www.python.org/downloads/) installed.
- [Git](https://git-scm.com/downloads) installed.
- A TiDB Cloud Serverless cluster. Follow [creating a TiDB Cloud Serverless cluster](/tidb-cloud/create-tidb-cluster-serverless.md) to create your own TiDB Cloud cluster if you don't have one.

## Run the sample app

You can quickly learn about how to integrate TiDB Vector Search with JinaAI Embedding by following the steps below.

### Step 1. Clone the repository

Clone the `tidb-vector-python` repository to your local machine:

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### Step 2. Create a virtual environment

Create a virtual environment for your project:

```bash
cd tidb-vector-python/examples/jina-ai-embeddings-demo
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3. Install required dependencies

Install the required dependencies for the demo project:

```bash
pip install -r requirements.txt
```

### Step 4. Configure the environment variables

Get the Jina AI API key from the [Jina AI Embeddings API](https://jina.ai/embeddings/) page. Then, obtain the cluster connection string and configure environment variables as follows:

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

   - **Connection Type** is set to `Public`
   - **Branch** is set to `main`
   - **Connect With** is set to `SQLAlchemy`
   - **Operating System** matches your environment.

   > **Tip:**
   >
   > If your program is running in Windows Subsystem for Linux (WSL), switch to the corresponding Linux distribution.

4. Switch to the **PyMySQL** tab and click the **Copy** icon to copy the connection string.

   > **Tip:**
   >
   > If you have not set a password yet, click **Create password** to generate a random password.

5. Set the Jina AI API key and the TiDB connection string as environment variables in your terminal, or create a `.env` file with the following environment variables:

   ```dotenv
   JINAAI_API_KEY="****"
   TIDB_DATABASE_URL="{tidb_connection_string}"
   ```

   The following is an example connection string for macOS:

   ```dotenv
   TIDB_DATABASE_URL="mysql+pymysql://<prefix>.root:<password>@gateway01.<region>.prod.aws.tidbcloud.com:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
   ```

### Step 5. Run the demo

```bash
python jina-ai-embeddings-demo.py
```

Example output:

```text
- Inserting Data to TiDB...
  - Inserting: Jina AI offers best-in-class embeddings, reranker and prompt optimizer, enabling advanced multimodal AI.
  - Inserting: TiDB is an open-source MySQL-compatible database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads.
- List All Documents and Their Distances to the Query:
  - distance: 0.3585317326132522
    content: Jina AI offers best-in-class embeddings, reranker and prompt optimizer, enabling advanced multimodal AI.
  - distance: 0.10858102967720984
    content: TiDB is an open-source MySQL-compatible database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads.
- The Most Relevant Document and Its Distance to the Query:
  - distance: 0.10858102967720984
    content: TiDB is an open-source MySQL-compatible database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads.
```

## Sample code snippets

### Get embeddings from Jina AI

Define a `generate_embeddings` helper function to call Jina AI embeddings API:

```python
import os
import requests
import dotenv

dotenv.load_dotenv()

JINAAI_API_KEY = os.getenv('JINAAI_API_KEY')

def generate_embeddings(text: str):
    JINAAI_API_URL = 'https://api.jina.ai/v1/embeddings'
    JINAAI_HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {JINAAI_API_KEY}'
    }
    JINAAI_REQUEST_DATA = {
        'input': [text],
        'model': 'jina-embeddings-v2-base-en'  # with dimension 768.
    }
    response = requests.post(JINAAI_API_URL, headers=JINAAI_HEADERS, json=JINAAI_REQUEST_DATA)
    return response.json()['data'][0]['embedding']
```

### Connect to the TiDB cluster

Connect to the TiDB cluster through SQLAlchemy:

```python
import os
import dotenv

from tidb_vector.sqlalchemy import VectorType
from sqlalchemy.orm import Session, declarative_base

dotenv.load_dotenv()

TIDB_DATABASE_URL = os.getenv('TIDB_DATABASE_URL')
assert TIDB_DATABASE_URL is not None
engine = create_engine(url=TIDB_DATABASE_URL, pool_recycle=300)
```

### Define the vector table schema

Create a table named `jinaai_tidb_demo_documents` with a `content` column for storing texts and a vector column named `content_vec` for storing embeddings:

```python
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Document(Base):
    __tablename__ = "jinaai_tidb_demo_documents"

    id = Column(Integer, primary_key=True)
    content = Column(String(255), nullable=False)
    content_vec = Column(
        # DIMENSIONS is determined by the embedding model,
        # for Jina AI's jina-embeddings-v2-base-en model it's 768.
        VectorType(dim=768),
        comment="hnsw(distance=cosine)"
```

> **Note:**
>
> - The dimension of the vector column must match the dimension of the embeddings generated by the embedding model.
> - In this example, the dimension of embeddings generated by the `jina-embeddings-v2-base-en` model is `768`.

### Create embeddings with Jina AI and store in TiDB

Use the Jina AI Embeddings API to generate embeddings for each piece of text and store the embeddings in TiDB:

```python
TEXTS = [
   'Jina AI offers best-in-class embeddings, reranker and prompt optimizer, enabling advanced multimodal AI.',
   'TiDB is an open-source MySQL-compatible database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads.',
]
data = []

for text in TEXTS:
    # Generate embeddings for the texts via Jina AI API.
    embedding = generate_embeddings(text)
    data.append({
        'text': text,
        'embedding': embedding
    })

with Session(engine) as session:
   print('- Inserting Data to TiDB...')
   for item in data:
      print(f'  - Inserting: {item["text"]}')
      session.add(Document(
         content=item['text'],
         content_vec=item['embedding']
      ))
   session.commit()
```

### Perform semantic search with Jina AI embeddings in TiDB

Generate the embedding for the query text via Jina AI embeddings API, and then search for the most relevant document based on the cosine distance between **the embedding of the query text** and **each embedding in the vector table**:

```python
query = 'What is TiDB?'
# Generate the embedding for the query via Jina AI API.
query_embedding = generate_embeddings(query)

with Session(engine) as session:
    print('- The Most Relevant Document and Its Distance to the Query:')
    doc, distance = session.query(
        Document,
        Document.content_vec.cosine_distance(query_embedding).label('distance')
    ).order_by(
        'distance'
    ).limit(1).first()
    print(f'  - distance: {distance}\n'
          f'    content: {doc.content}')
```

## See also

- [Vector Data Types](/tidb-cloud/vector-search-data-types.md)
- [Vector Search Index](/tidb-cloud/vector-search-index.md)
