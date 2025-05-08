---
title: Full-Text Search with Python
summary: Full-text search allows you to retrieve documents for exact keywords. In RAG (Retrieval-Augmented Generation) scenarios, you can use full-text search along with vector search together to improve the retrieval quality.
---

# Full-Text Search with Python

Unlike [Vector Search](/vector-search/vector-search-overview.md), which focuses on semantic similarity, full-text search allows you to retrieve documents for exact keywords. In RAG (Retrieval-Augmented Generation) scenarios, you can use full-text search along with vector search together to improve the retrieval quality.

The full-text search feature in TiDB provides the following capabilities:

- **Operate on Text Data**: You can search over any string columns directly without embedding process.

- **Support Hybrid-Languages**: No need to specify the language for high quality search. TiDB's text analyzer supports documents of multiple languages mixed in the same table and chooses the best analyzer for each document.

- **Order by Relevance**: The search result can be ordered by relevance using the widely used [BM25 ranking](https://en.wikipedia.org/wiki/Okapi_BM25) algorithm.

- **Support Full SQL Features**: All SQL features, such as pre-filtering, post-filtering, grouping, joining, can be used with full-text search.

> **Tip:**
>
> This document covers details about the full-text search feature using Python. For SQL usages, please refer to [Full-Text Search with SQL](/vector-search/vector-search-full-text-search-sql.md).
>
> Additionally, for guidelines of using full-text search and vector search together in your AI application, you may further refer to [Hybrid Search](/vector-search/vector-search-hybrid-search.md).

## Prerequisites

Full-Text search is still in the early stages, and we are continuously rolling it out to more customers. Currently, Full-Text Search is only available for the following service and regions:

- TiDB Serverless (Europe Region)

To complete this tutorial, make sure you have a TiDB Serverless cluster in the supported regions above. If you don't have a TiDB Serverless cluster, follow [Creating a TiDB Cloud Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own one.

## Getting Started

### Step1. Install Python SDK

[pytidb](https://github.com/pingcap/pytidb) is the official Python SDK for TiDB developers to build AI applications efficiently, which has built-in support for vector search and full-text search.

To install the SDK, run the following command:

```shell
pip install pytidb

# If you want to use built-in embedding function and rerankers.
# pip install "pytidb[models]"

# If you want to convert query result to pandas DataFrame.
# pip install pandas
```

### Step2. Connect to TiDB

```python
import os
from pytidb import TiDBClient

db = TiDBClient.connect(
    host="HOST_HERE",
    port=4000,
    username="USERNAME_HERE",
    password="PASSWORD_HERE",
    database="DATABASE_HERE",
)
```

The parameters above can be obtained from TiDB Cloud console:

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed, with connection parameters listed.

   As an example, for parameters displayed like this:

   ```text
   HOST:     gateway01.us-east-1.prod.shared.aws.tidbcloud.com
   PORT:     4000
   USERNAME: 4EfqPF23YKBxaQb.root
   PASSWORD: abcd1234
   DATABASE: test
   CA:       /etc/ssl/cert.pem
   ```

   The Python code to connect to the cluster would be:

   ```python
   db = TiDBClient.connect(
       host="gateway01.us-east-1.prod.shared.aws.tidbcloud.com",
       port=4000,
       username="4EfqPF23YKBxaQb.root",
       password="abcd1234",
       database="test",
   )
   ```

   Notice that the example code above are only for demonstration purposes. You should fill in the parameters with your own values, and well protect your credentials.

### Step3. Create Table and Full Text Index

As an example, we will create a table named `chunks` with the following schema:

- `id` (int): The ID of the chunk.
- `text` (text): The text content of the chunk.
- `user_id` (int): The ID of the user who created the chunk.

```python
from pytidb.schema import TableModel, Field

class Chunk(TableModel, table=True):
    __tablename__ = "chunks"

    id: int = Field(primary_key=True)
    text: str = Field()
    user_id: int = Field()

table = db.create_table(schema=Chunk)

if not table.has_fts_index("text"):
    table.create_fts_index("text")   # 👈 Create a fulltext index on the text column.
```

### Step4. Insert Data

```python
table.bulk_insert(
    [
        Chunk(id=2, text="bar", user_id=2),
        Chunk(id=3, text="baz", user_id=3),
        Chunk(id=4, text="qux", user_id=4),
    ]
)
```

### Step5. Perform Full-Text Search

After data is inserted, a full-text search can be performed as follows:

```python
df = (
  table.search("<query>", search_type="fulltext")
    .limit(2)
    .to_pandas()
)
```

See [PyTiDB Fulltext Search demo](https://github.com/pingcap/pytidb/blob/main/examples/fulltext_search) for a more complete example.

## See also

- [pytidb Python SDK Documentation](https://github.com/pingcap/pytidb)

- [Hybrid Search](/vector-search/vector-search-hybrid-search.md)

## Feedback & Help

Full-text search is still in the early stages with limited accessibility. If you would like to try full-text search in a region that is not yet available, or if you have feedback or need help, feel free to reach out to us:

<CustomContent platform="tidb">

- [Join our Discord](https://discord.gg/zcqexutz2R)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [Join our Discord](https://discord.gg/zcqexutz2R)
- [Visit our Support Portal](https://tidb.support.pingcap.com/)

</CustomContent>
