---
title: Get Started with TiDB + AI via Python
summary: Learn how to get started with vector search in TiDB using Python SDK.
aliases: ['/tidb/stable/vector-search-get-started-using-sql/','/tidb/dev/vector-search-get-started-using-sql/','/tidbcloud/vector-search-get-started-using-sql/']
---

# Get Started with TiDB + AI via Python

In this guide, you will learn how to get started with [vector search](/ai/concepts/vector-search-overview.md) in TiDB using Python SDK. Follow along to build your first AI application working with TiDB.

## Prerequisites

- Go to [tidbcloud.com](https://tidbcloud.com/) to create a TiDB Cloud Starter cluster for free or using [tiup playground](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb/#deploy-a-local-test-cluster) to deploy a TiDB Self-Managed cluster for local testing.

## Installation

[pytidb](https://github.com/pingcap/pytidb) is the official Python SDK for TiDB, designed to help developers build AI applications efficiently.

To install the Python SDK, run the following command:

```bash
pip install pytidb
```

To use built-in embedding function, install the `models` extension (alternative):

```bash
pip install "pytidb[models]"
```

## Connect to database

<SimpleTab>
<div label="TiDB Cloud Starter">

You can get these connection parameters from the [TiDB Cloud console](https://tidbcloud.com/clusters):

1. Navigate to the [Clusters page](https://tidbcloud.com/clusters), and then click the name of your target cluster to go to its overview page.
2. Click **Connect** in the upper-right corner. A connection dialog is displayed, with connection parameters listed.

For example, if the connection parameters are displayed as follows:

```text
HOST:     gateway01.us-east-1.prod.shared.aws.tidbcloud.com
PORT:     4000
USERNAME: 4EfqPF23YKBxaQb.root
PASSWORD: abcd1234
DATABASE: test
CA:       /etc/ssl/cert.pem
```

The corresponding Python code to connect to the TiDB Cloud Starter cluster would be as follows:

```python
from pytidb import TiDBClient

client = TiDBClient.connect(
    host="gateway01.us-east-1.prod.shared.aws.tidbcloud.com",
    port=4000,
    username="4EfqPF23YKBxaQb.root",
    password="abcd1234",
    database="test",
)
```

> **Note:**
>
> The preceding example is for demonstration purposes only. You need to fill in the parameters with your own values and keep them secure.

</div>
<div label="TiDB Self-Managed">

Here is a basic example for connecting to a self-managed TiDB cluster:

```python
from pytidb import TiDBClient

client = TiDBClient.connect(
    host="localhost",
    port=4000,
    username="root",
    password="",
    database="test",
    ensure_db=True,
)
```

> **Note:**
>
> Make sure to update the connection parameters according to your actual deployment.

</div>
</SimpleTab>

Once connected, you can use the `client` object to operate tables, query data, and more.

## Create an embedding function

When working with [embedding models](/ai/concepts/vector-search-overview.md#embedding-model), you can leverage the embedding function to automatically vectorize your data at both insertion and query stages. It natively supports popular embedding models like OpenAI, Jina AI, Hugging Face, Sentence Transformers, and others.

<SimpleTab>
<div label="OpenAI">

Go to [OpenAI platform](https://platform.openai.com/api-keys) to create your API key for embedding.

```python
from pytidb.embeddings import EmbeddingFunction

text_embed = EmbeddingFunction(
    model_name="openai/text-embedding-3-small",
    api_key="<your-openai-api-key>",
)
```

</div>
<div label="Jina AI">

Go to [Jina AI](https://jina.ai/embeddings/) to create your API key for embedding.

```python
from pytidb.embeddings import EmbeddingFunction

text_embed = EmbeddingFunction(
    model_name="jina/jina-embeddings-v3",
    api_key="<your-jina-api-key>",
)
```

</div>
</SimpleTab>

## Create a table

As an example, create a table named `chunks` with the following columns:

- `id` (int): the ID of the chunk.
- `text` (text): the text content of the chunk.
- `text_vec` (vector): the vector embeddings of the text.
- `user_id` (int): the ID of the user who created the chunk.

```python hl_lines="6"
from pytidb.schema import TableModel, Field, VectorField

class Chunk(TableModel):
    id: int | None = Field(default=None, primary_key=True)
    text: str = Field()
    text_vec: list[float] = text_embed.VectorField(source_field="text")
    user_id: int = Field()

table = client.create_table(schema=Chunk, if_exists="overwrite")
```

Once created, you can use the `table` object to insert data, search data, and more.

## Insert Data

Now let's add some sample data to our table.

```python
table.bulk_insert([
    # 👇 The text will be automatically embedded and populated into the `text_vec` field.
    Chunk(text="PyTiDB is a Python library for developers to connect to TiDB.", user_id=2),
    Chunk(text="LlamaIndex is a framework for building AI applications.", user_id=2),
    Chunk(text="OpenAI is a company and platform that provides AI models service and tools.", user_id=3),
])
```

## Search for nearest neighbors

To search for nearest neighbors of a given query, you can use the `table.search()` method. This method performs a [vector search](/ai/guides/vector-search.md) by default.

```python
table.search(
    # 👇 Pass the query text directly, it will be embedded to a query vector automatically.
    "A library for my artificial intelligence software"
)
.limit(3).to_list()
```

In this example, vector search compares the query vector with the stored vectors in the `text_vec` field of the `chunks` table and returns the top 3 most semantically relevant results based on similarity scores.

The closer `_distance` means the more similar the two vectors are.

```json title="Expected output"
[
    {
        'id': 2,
        'text': 'LlamaIndex is a framework for building AI applications.',
        'text_vec': [...],
        'user_id': 2,
        '_distance': 0.5719928358786761,
        '_score': 0.4280071641213239
    },
    {
        'id': 3,
        'text': 'OpenAI is a company and platform that provides AI models service and tools.',
        'text_vec': [...],
        'user_id': 3,
        '_distance': 0.603133726213383,
        '_score': 0.396866273786617
    },
    {
        'id': 1,
        'text': 'PyTiDB is a Python library for developers to connect to TiDB.',
        'text_vec': [...],
        'user_id': 2,
        '_distance': 0.6202191842385758,
        '_score': 0.3797808157614242
    }
]
```

## Delete data

To delete a specific row from the table, you can use the `table.delete()` method:

```python
table.delete({
    "id": 1
})
```

## Drop table

When you no longer need a table, you can drop it using the `client.drop_table()` method:

```python
client.drop_table("chunks")
```

## Next steps

- Learn more details about [Vector Search](/ai/guides/vector-search.md), [Full-Text Search](/ai/guides/vector-search-full-text-search-python.md) and [Hybrid Search](/ai/guides/vector-search-hybrid-search.md) in TiDB.
