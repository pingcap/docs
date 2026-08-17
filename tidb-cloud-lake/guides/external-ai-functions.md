---
title: External AI Functions
summary: Learn how to serve a Python embedding model through an external UDF Server and call it from TiDB Cloud Lake SQL queries.
---

# External AI Functions

External UDFs let {{{ .lake }}} queries call models and Python libraries that run on your infrastructure. You can deploy the UDF Server on CPU or GPU compute and scale it independently from the warehouse.

This example exposes a text embedding model as a scalar function that returns a `VECTOR` value.

## Prerequisites

- Python 3.10 or later for the model and UDF Server
- A public HTTPS endpoint that supports gRPC over HTTP/2
- The endpoint hostname added to your tenant UDF server allowlist by TiDB Cloud Support
- A table containing text to embed

## Step 1. Install the dependencies

```shell
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install tidbcloudlake-udf sentence-transformers
```

## Step 2. Create the embedding handler

Create `embedding_server.py`:

```python
from sentence_transformers import SentenceTransformer
from tidbcloudlake_udf import UDFServer, udf


model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")


@udf(
    input_types=["VARCHAR"],
    result_type="VECTOR(768)",
    skip_null=True,
)
def embed_text(value: str) -> list[float]:
    embedding = model.encode(value)
    return embedding.astype("float32").tolist()


if __name__ == "__main__":
    server = UDFServer("0.0.0.0:8815")
    server.add_function(embed_text)
    server.serve()
```

Start the server:

```shell
python3 embedding_server.py
```

## Step 3. Deploy and allow the endpoint

Deploy the Flight server behind a public HTTPS endpoint that preserves gRPC over HTTP/2. Configure authentication, scaling, high availability, and monitoring for the service.

Contact TiDB Cloud Support to add the endpoint hostname to your tenant UDF server allowlist. The server can bind to `0.0.0.0` inside its deployment, but the SQL `ADDRESS` must use the public hostname.

## Step 4. Register the function

```sql
CREATE FUNCTION embed_text(value VARCHAR)
RETURNS VECTOR(768)
LANGUAGE python
HANDLER = 'embed_text'
ADDRESS = 'https://udf.example.com';
```

## Step 5. Use embeddings in a query

```sql
SELECT
    id,
    title,
    COSINE_DISTANCE(
        embedding,
        embed_text('machine learning techniques')
    ) AS distance
FROM articles
ORDER BY distance
LIMIT 5;
```

External model calls add network and inference latency. Measure representative query concurrency and batch sizes before placing the function in a production query path.

## Related resources

- [CREATE FUNCTION](/tidb-cloud-lake/sql/create-function.md)
- [Choose a User-Defined Function Type](/tidb-cloud-lake/guides/choose-a-udf-type.md)
- [`tidbcloudlake-udf` on PyPI](https://pypi.org/project/tidbcloudlake-udf/)
