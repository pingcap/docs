---
title: Integrate Vector Search with LlamaIndex
summary: 
---

# Integrate Vector Search with LlamaIndex

This tutorial will walk you through how to integrate the TiDB vector search feature with LlamaIndex.

> **Note**
>
> TiDB Vector Search is only available for TiDB Serverless at this moment.

> **Tips**
> 
> You can check the complete [sample code](https://github.com/run-llama/llama_index/blob/main/docs/docs/examples/vector_stores/TiDBVector.ipynb) on Jupyter Notebook, or run the sample code directly in the [colab](https://colab.research.google.com/github/run-llama/llama_index/blob/main/docs/docs/examples/vector_stores/TiDBVector.ipynb) online environment.


## Prerequisites

To complete this tutorial, you need:

- [Python 3.8 or higher](https://www.python.org/downloads/) installed.
- [Jupyter Notebook](https://jupyter.org/install) installed.
- [Git](https://git-scm.com/downloads) installed.
- A TiDB Serverless cluster running.

<CustomContent platform="tidb-cloud">

**If you don't have a TiDB cluster, you can create one as follows:**

- Follow [Creating a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.

</CustomContent>

## Get Started

In this section, you can learn step-by-step how to use LlamaIndex to integrate with TiDB vector search and perform semantic search.

### Step 1. Create a new Jupyter Notebook file

Create a new Jupyter Notebook file in your preferred directory.

```shell
touch integrate_with_llamaindex.ipynb
```

### Step 2. Install required dependencies

Run the following command on your project directory to install the required packages:

```shell
pip install llama-index-vector-stores-tidbvector
pip install llama-index
```

Import the required packages in your code:

```python
import textwrap

from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.tidbvector import TiDBVectorStore
```

### Step 3. Set up environments

#### Step 3.1 Obtains the connection string to the TiDB cluster

<SimpleTab>
<div label="TiDB Serverless">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

   - **Endpoint Type** is set to `Public`
   - **Branch** is set to `main`
   - **Connect With** is set to `SQLAlchemy`
   - **Operating System** matches your environment.

4. Switch to the **PyMySQL** tab and click the **Copy** icon to copy the connection string.

</div>

</SimpleTab>

#### Step 3.2 Configure the environment variables

Configure the TiDB connection string and [OpenAI API key](https://platform.openai.com/api-keys) in the Jupyter Notebook. 

```python
import getpass
import os

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
tidb_connection_url = getpass.getpass(
   "TiDB connection URL (format - mysql+pymysql://root@127.0.0.1:4000/test): "
)
```

### Step 4. Load the sample document

#### Step 4.1 Download the sample document

Download the sample document `paul_graham_essay.txt` from the GitHub repository.

```shell
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

#### Step 4.2 Load documents

Load the sample document from the directory with the `SimpleDirectoryReader` class.

```python
documents = SimpleDirectoryReader("./data/paul_graham").load_data()
print("Document ID:", documents[0].doc_id)

for index, document in enumerate(documents):
   document.metadata = {"book": "paul_graham"}
```

### Step 5. Build index

#### Step 5.1 Initializes the TiDB vector store

The code snippet below creates a table named `paul_graham_test` in TiDB, optimized for vector searching. 

```python
tidbvec = TiDBVectorStore(
   connection_string=tidb_connection_url,
   table_name="paul_graham_test",
   distance_strategy="cosine",
   vector_dimension=1536,
   drop_existing_table=False,
)
```

Upon successful execution of this code, you will be able to view and access the `paul_graham_test` table directly within your TiDB database.

#### Step 5.2 Builds vector indexes from the documents

The code snippet below will parse the documents, generate embeddings, and store them in the TiDB vector store.

```python
storage_context = StorageContext.from_defaults(vector_store=tidbvec)
index = VectorStoreIndex.from_documents(
   documents, storage_context=storage_context, show_progress=True
)
```

Excepted output:

```plain
Parsing nodes: 100%|██████████| 1/1 [00:00<00:00,  8.76it/s]
Generating embeddings: 100%|██████████| 21/21 [00:02<00:00,  8.22it/s]
```

### Step 6. Semantic similarity search

Creates a query engine based on the TiDB vector store and performs a semantic similarity search.

```python
query_engine = index.as_query_engine()
response = query_engine.query("What did the author do?")
print(textwrap.fill(str(response), 100))
```

> **Note**
>
> `TiDBVectorStore` only supports [`default`](https://docs.llamaindex.ai/en/stable/api_reference/storage/vector_store/?h=vectorstorequerymode#llama_index.core.vector_stores.types.VectorStoreQueryMode) query mode for now.

Expected output:

```plain
The author worked on writing, programming, building microcomputers, giving talks at conferences,
publishing essays online, developing spam filters, painting, hosting dinner parties, and purchasing
a building for office use.
```

### Step 7. Search with metadata filters

Perform searches with metadata filters to retrieve the top-k nearest-neighbor documents that align with the applied filters.

#### Step 7.1 Query with `book != "paul_graham"` filter

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

Expected output:

```plain
Empty Response
```

#### Step 7.2 Query with `book == "paul_graham"` filter

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

Expected output:

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

Expected output:

```plain
Empty Response
```

## See also

- [Vector Column](/tidb-cloud/vector-search-vector-column.md)
- [Vector Index](/tidb-cloud/vector-search-vector-index.md)