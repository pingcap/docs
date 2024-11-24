---
title: Integrate Vector Search with LlamaIndex
summary: Learn how to integrate TiDB Vector Search with LlamaIndex.
---

# Integrate Vector Search with LlamaIndex

This tutorial demonstrates how to integrate the [vector search](/tidb-cloud/vector-search-overview.md) feature of TiDB with [LlamaIndex](https://www.llamaindex.ai).

> **Note**
>
> TiDB Vector Search is only available for TiDB (>= v8.4) and [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless). It is not available for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated).

> **Tip**
>
> You can view the complete [sample code](https://github.com/run-llama/llama_index/blob/main/docs/docs/examples/vector_stores/TiDBVector.ipynb) on Jupyter Notebook, or run the sample code directly in the [Colab](https://colab.research.google.com/github/run-llama/llama_index/blob/main/docs/docs/examples/vector_stores/TiDBVector.ipynb) online environment.

## Prerequisites

To complete this tutorial, you need:

- [Python 3.8 or higher](https://www.python.org/downloads/) installed.
- [Jupyter Notebook](https://jupyter.org/install) installed.
- [Git](https://git-scm.com/downloads) installed.
- A TiDB Cloud Serverless cluster. Follow [creating a TiDB Cloud Serverless cluster](/tidb-cloud/create-tidb-cluster-serverless.md) to create your own TiDB Cloud cluster if you don't have one.

## Get started

This section provides step-by-step instructions for integrating TiDB Vector Search with LlamaIndex to perform semantic searches.

### Step 1. Create a new Jupyter Notebook file

In the root directory, create a new Jupyter Notebook file named `integrate_with_llamaindex.ipynb`:

```shell
touch integrate_with_llamaindex.ipynb
```

### Step 2. Install required dependencies

In your project directory, run the following command to install the required packages:

```shell
pip install llama-index-vector-stores-tidbvector
pip install llama-index
```

Open the `integrate_with_llamaindex.ipynb` file in Jupyter Notebook and add the following code to import the required packages:

```python
import textwrap

from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.tidbvector import TiDBVectorStore
```

### Step 3. Configure environment variables

Take the following steps to obtain the cluster connection string and configure environment variables:

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

   - **Connection Type** is set to `Public`.
   - **Branch** is set to `main`.
   - **Connect With** is set to `SQLAlchemy`.
   - **Operating System** matches your environment.

4. Click the **PyMySQL** tab and copy the connection string.

   > **Tip:**
   >
   > If you have not set a password yet, click **Generate Password** to generate a random password.

5. Configure environment variables.

   This document uses [OpenAI](https://platform.openai.com/docs/introduction) as the embedding model provider. In this step, you need to provide the connection string obtained from from the previous step and your [OpenAI API key](https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key).

   To configure the environment variables, run the following code. You will be prompted to enter your connection string and OpenAI API key:

   ```python
   # Use getpass to securely prompt for environment variables in your terminal.
   import getpass
   import os

   # Copy your connection string from the TiDB Cloud console.
   # Connection string format: "mysql+pymysql://<USER>:<PASSWORD>@<HOST>:4000/<DB>?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
   tidb_connection_string = getpass.getpass("TiDB Connection String:")
   os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
   ```

### Step 4. Load the sample document

#### Step 4.1 Download the sample document

In your project directory, create a directory named `data/paul_graham/` and download the sample document [`paul_graham_essay.txt`](https://github.com/run-llama/llama_index/blob/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt) from the [run-llama/llama_index](https://github.com/run-llama/llama_index) GitHub repository.

```shell
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

#### Step 4.2 Load the document

Load the sample document from `data/paul_graham/paul_graham_essay.txt` using the `SimpleDirectoryReader` class.

```python
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
print("Document ID:", documents[0].doc_id)

for index, document in enumerate(documents):
   document.metadata = {"book": "paul_graham"}
```

### Step 5. Embed and store document vectors

#### Step 5.1 Initialize the TiDB vector store

The following code creates a table named `paul_graham_test` in TiDB, which is optimized for vector search.

```python
tidbvec = TiDBVectorStore(
   connection_string=tidb_connection_url,
   table_name="paul_graham_test",
   distance_strategy="cosine",
   vector_dimension=1536,
   drop_existing_table=False,
)
```

Upon successful execution, you can directly view and access the `paul_graham_test` table in your TiDB database.

#### Step 5.2 Generate and store embeddings

The following code parses the documents, generates embeddings, and stores them in the TiDB vector store.

```python
storage_context = StorageContext.from_defaults(vector_store=tidbvec)
index = VectorStoreIndex.from_documents(
   documents, storage_context=storage_context, show_progress=True
)
```

The expected output is as follows:

```plain
Parsing nodes: 100%|██████████| 1/1 [00:00<00:00,  8.76it/s]
Generating embeddings: 100%|██████████| 21/21 [00:02<00:00,  8.22it/s]
```

### Step 6. Perform a vector search

The following creates a query engine based on the TiDB vector store and performs a semantic similarity search.

```python
query_engine = index.as_query_engine()
response = query_engine.query("What did the author do?")
print(textwrap.fill(str(response), 100))
```

> **Note**
>
> `TiDBVectorStore` only supports the [`default`](https://docs.llamaindex.ai/en/stable/api_reference/storage/vector_store/?h=vectorstorequerymode#llama_index.core.vector_stores.types.VectorStoreQueryMode) query mode.

The expected output is as follows:

```plain
The author worked on writing, programming, building microcomputers, giving talks at conferences,
publishing essays online, developing spam filters, painting, hosting dinner parties, and purchasing
a building for office use.
```

### Step 7. Search with metadata filters

To refine your searches, you can use metadata filters to retrieve specific nearest-neighbor results that match the applied filters.

#### Query with `book != "paul_graham"` filter

The following example excludes results where the `book` metadata field is `"paul_graham"`:

```python
from llama_index.core.vector_stores.types import (
   MetadataFilter,
   MetadataFilters,
)

query_engine = index.as_query_engine(
   filters=MetadataFilters(
      filters=[
         MetadataFilter(key="book", value="paul_graham", operator="!="),
      ]
   ),
   similarity_top_k=2,
)
response = query_engine.query("What did the author learn?")
print(textwrap.fill(str(response), 100))
```

The expected output is as follows:

```plain
Empty Response
```

#### Query with `book == "paul_graham"` filter

The following example filters results to include only documents where the `book` metadata field is `"paul_graham"`:

```python
from llama_index.core.vector_stores.types import (
   MetadataFilter,
   MetadataFilters,
)

query_engine = index.as_query_engine(
   filters=MetadataFilters(
      filters=[
         MetadataFilter(key="book", value="paul_graham", operator="=="),
      ]
   ),
   similarity_top_k=2,
)
response = query_engine.query("What did the author learn?")
print(textwrap.fill(str(response), 100))
```

The expected output is as follows:

```plain
The author learned programming on an IBM 1401 using an early version of Fortran in 9th grade, then
later transitioned to working with microcomputers like the TRS-80 and Apple II. Additionally, the
author studied philosophy in college but found it unfulfilling, leading to a switch to studying AI.
Later on, the author attended art school in both the US and Italy, where they observed a lack of
substantial teaching in the painting department.
```

### Step 8. Delete documents

Delete the first document from the index:

```python
tidbvec.delete(documents[0].doc_id)
```

Check whether the documents had been deleted:

```python
query_engine = index.as_query_engine()
response = query_engine.query("What did the author learn?")
print(textwrap.fill(str(response), 100))
```

The expected output is as follows:

```plain
Empty Response
```

## See also

- [Vector Data Types](/tidb-cloud/vector-search-data-types.md)
- [Vector Search Index](/tidb-cloud/vector-search-index.md)
