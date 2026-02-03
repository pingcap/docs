---
title: Auto Embedding Example
summary: Automatically generate embeddings for your text data using built-in embedding models.
---

# Auto Embedding Example

This example shows how to use the [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) feature with the [pytidb](https://github.com/pingcap/pytidb) client.

1. Connect to TiDB using the PyTiDB client.
2. Define a table with a VectorField configured for automatic embedding.
3. Insert plain text data: embeddings are populated automatically in the background.
4. Run vector searches with natural-language queries: embeddings are generated transparently.

## Prerequisites

- **Python 3.10+**
- **A TiDB Cloud Starter cluster** (Go to <https://tidbcloud.com/> to create a free cluster for quick testing)

## How to run

### Step 1. Clone the repository

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/auto_embedding/
```

### Step 2. Install the required packages

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### Step 3. Set up environment to connect to database

Go to the [TiDB Cloud console](https://tidbcloud.com/clusters) to get the connection parameters, and then set environment variables as follows:

```bash
cat > .env <<EOF
TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USERNAME={prefix}.root
TIDB_PASSWORD={password}
TIDB_DATABASE=test

# Using TiDB Cloud Free embedding model by default, which does not require setting up any API key
EMBEDDING_PROVIDER=tidbcloud_free
EOF
```

### Step 4. Run the demo

```bash
python main.py
```

**Expected output:**

```plain
=== Define embedding function ===
Embedding function (model id: tidbcloud_free/amazon/titan-embed-text-v2) defined

=== Define table schema ===
Table created

=== Truncate table ===
Table truncated

=== Insert sample data ===
Inserted 3 chunks

=== Perform vector search ===
id: 1, text: TiDB is a distributed database that supports OLTP, OLAP, HTAP and AI workloads., distance: 0.30373281240458805
id: 2, text: PyTiDB is a Python library for developers to connect to TiDB., distance: 0.422506501973434
id: 3, text: LlamaIndex is a Python library for building AI-powered applications., distance: 0.5267239638442787
```

## Related resources

- **Source Code**: [View on GitHub](https://github.com/pingcap/pytidb/tree/main/examples/auto_embedding)