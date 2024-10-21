---
title: Get Started with TiDB + AI via Python
summary: Learn how to quickly develop an AI application that performs semantic search using Python and TiDB Vector Search.
---

# Get Started with TiDB + AI via Python

This tutorial demonstrates how to develop a simple AI application that provides **semantic search** features. Unlike traditional keyword search, semantic search intelligently understands the meaning behind your query and returns the most relevant result. For example, if you have documents titled "dog", "fish", and "tree", and you search for "a swimming animal", the application would identify "fish" as the most relevant result.

Throughout this tutorial, you will develop this AI application using [TiDB Vector Search](/vector-search-overview.md), Python, [TiDB Vector SDK for Python](https://github.com/pingcap/tidb-vector-python), and AI models.

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

## Get started

The following steps show how to develop the application from scratch. To run the demo directly, you can check out the sample code in the [pingcap/tidb-vector-python](https://github.com/pingcap/tidb-vector-python/blob/main/examples/python-client-quickstart) repository.

### Step 1. Create a new Python project

In your preferred directory, create a new Python project and a file named `example.py`:

```shell
mkdir python-client-quickstart
cd python-client-quickstart
touch example.py
```

### Step 2. Install required dependencies

In your project directory, run the following command to install the required packages:

```shell
pip install sqlalchemy pymysql sentence-transformers tidb-vector python-dotenv
```

- `tidb-vector`: the Python client for interacting with TiDB vector search.
- [`sentence-transformers`](https://sbert.net): a Python library that provides pre-trained models for generating [vector embeddings](/vector-search-overview.md#vector-embedding) from text.

### Step 3. Configure the connection string to the TiDB cluster

Configure the cluster connection string depending on the TiDB deployment option you've selected.

<SimpleTab>
<div label="TiDB Cloud Serverless">

For a TiDB Cloud Serverless cluster, take the following steps to obtain the cluster connection string and configure environment variables:

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

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

</div>
<div label="TiDB Self-Managed">

For a TiDB Self-Managed cluster, create a `.env` file in the root directory of your Python project. Copy the following content into the `.env` file, and modify the environment variable values according to the connection parameters of your TiDB cluster:

```dotenv
TIDB_DATABASE_URL="mysql+pymysql://<USER>:<PASSWORD>@<HOST>:<PORT>/<DATABASE>"
# For example: TIDB_DATABASE_URL="mysql+pymysql://root@127.0.0.1:4000/test"
```

If you are running TiDB on your local machine, `<HOST>` is `127.0.0.1` by default. The initial `<PASSWORD>` is empty, so if you are starting the cluster for the first time, you can omit this field.

The following are descriptions for each parameter:

- `<USER>`: The username to connect to the TiDB cluster.
- `<PASSWORD>`: The password to connect to the TiDB cluster.
- `<HOST>`: The host of the TiDB cluster.
- `<PORT>`: The port of the TiDB cluster.
- `<DATABASE>`: The name of the database you want to connect to.

</div>

</SimpleTab>

### Step 4. Initialize the embedding model

An [embedding model](/vector-search-overview.md#embedding-model) transforms data into [vector embeddings](/vector-search-overview.md#vector-embedding). This example uses the pre-trained model [**msmarco-MiniLM-L12-cos-v5**](https://huggingface.co/sentence-transformers/msmarco-MiniLM-L12-cos-v5) for text embedding. This lightweight model, provided by the `sentence-transformers` library, transforms text data into 384-dimensional vector embeddings.

To set up the model, copy the following code into the `example.py` file. This code initializes a `SentenceTransformer` instance and defines a `text_to_embedding()` function for later use.

```python
from sentence_transformers import SentenceTransformer

print("Downloading and loading the embedding model...")
embed_model = SentenceTransformer("sentence-transformers/msmarco-MiniLM-L12-cos-v5", trust_remote_code=True)
embed_model_dims = embed_model.get_sentence_embedding_dimension()

def text_to_embedding(text):
    """Generates vector embeddings for the given text."""
    embedding = embed_model.encode(text)
    return embedding.tolist()
```

### Step 5. Connect to the TiDB cluster

Use the `TiDBVectorClient` class to connect to your TiDB cluster and create a table `embedded_documents` with a vector column.

> **Note**
>
> Make sure the dimension of your vector column in the table matches the dimension of the vectors generated by your embedding model. For example, the **msmarco-MiniLM-L12-cos-v5** model generates vectors with 384 dimensions, so the dimension of your vector columns in `embedded_documents` should be 384 as well.

```python
import os
from tidb_vector.integrations import TiDBVectorClient
from dotenv import load_dotenv

# Load the connection string from the .env file
load_dotenv()

vector_store = TiDBVectorClient(
   # The 'embedded_documents' table will store the vector data.
   table_name='embedded_documents',
   # The connection string to the TiDB cluster.
   connection_string=os.environ.get('TIDB_DATABASE_URL'),
   # The dimension of the vector generated by the embedding model.
   vector_dimension=embed_model_dims,
   # Recreate the table if it already exists.
   drop_existing_table=True,
)
```

### Step 6. Embed text data and store the vectors

In this step, you will prepare sample documents containing single words, such as "dog", "fish", and "tree". The following code uses the `text_to_embedding()` function to transform these text documents into vector embeddings, and then inserts them into the vector store.

```python
documents = [
    {
        "id": "f8e7dee2-63b6-42f1-8b60-2d46710c1971",
        "text": "dog",
        "embedding": text_to_embedding("dog"),
        "metadata": {"category": "animal"},
    },
    {
        "id": "8dde1fbc-2522-4ca2-aedf-5dcb2966d1c6",
        "text": "fish",
        "embedding": text_to_embedding("fish"),
        "metadata": {"category": "animal"},
    },
    {
        "id": "e4991349-d00b-485c-a481-f61695f2b5ae",
        "text": "tree",
        "embedding": text_to_embedding("tree"),
        "metadata": {"category": "plant"},
    },
]

vector_store.insert(
    ids=[doc["id"] for doc in documents],
    texts=[doc["text"] for doc in documents],
    embeddings=[doc["embedding"] for doc in documents],
    metadatas=[doc["metadata"] for doc in documents],
)
```

### Step 7. Perform semantic search

In this step, you will search for "a swimming animal", which doesn't directly match any words in existing documents.

The following code uses the `text_to_embedding()` function again to convert the query text into a vector embedding, and then queries with the embedding to find the top three closest matches.

```python
def print_result(query, result):
   print(f"Search result (\"{query}\"):")
   for r in result:
      print(f"- text: \"{r.document}\", distance: {r.distance}")

query = "a swimming animal"
query_embedding = text_to_embedding(query)
search_result = vector_store.query(query_embedding, k=3)
print_result(query, search_result)
```

Run the `example.py` file and the output is as follows:

```plain
Search result ("a swimming animal"):
- text: "fish", distance: 0.4562914811223072
- text: "dog", distance: 0.6469335836410557
- text: "tree", distance: 0.798545178640937
```

The three terms in the search results are sorted by their respective distance from the queried vector: the smaller the distance, the more relevant the corresponding `document`.

Therefore, according to the output, the swimming animal is most likely a fish, or a dog with a gift for swimming.

## See also

- [Vector Data Types](/vector-search-data-types.md)
- [Vector Search Index](/vector-search-index.md)