---
title: Basic CRUD Operations
summary: Learn fundamental PyTiDB operations including database connection, table creation, and data manipulation.
---

# Basic CRUD Operations

This example demonstrates basic CRUD (Create, Read, Update, Delete) operations using PyTiDB.

1. Connect to TiDB using the PyTiDB client.
2. Create a table with text, vector, and JSON columns.
3. Run basic CRUD operations on the data.

## Prerequisites

- **Python 3.10+**
- **A TiDB Cloud Starter cluster** (Go to <https://tidbcloud.com/> to create a free cluster for quick testing)

## How to run

### Step 1. Clone the repository

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/basic/
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
EOF
```

### Step 4. Run the demo

```bash
python main.py
```

*Expected output:*

```plain
=== CREATE TABLE ===
Table created

=== TRUNCATE TABLE ===
Table truncated

=== CREATE ===
Created 3 items

=== READ ===
ID: 1, Content: TiDB is a distributed SQL database, Metadata: {'category': 'database'}
ID: 2, Content: GPT-4 is a large language model, Metadata: {'category': 'llm'}
ID: 3, Content: LlamaIndex is a Python library for building AI-powered applications, Metadata: {'category': 'rag'}

=== UPDATE ===
Updated item #1
After update - ID: 1, Content: TiDB Cloud Starter is a fully-managed, auto-scaling cloud database service, Metadata: {'category': 'dbass'}

=== DELETE ===
Deleted item #2

=== FINAL STATE ===
ID: 1, Content: TiDB Cloud Starter is a fully-managed, auto-scaling cloud database service, Metadata: {'category': 'dbass'}
ID: 3, Content: LlamaIndex is a Python library for building AI-powered applications, Metadata: {'category': 'rag'}

=== COUNT ROWS ===
Number of rows: 2

=== DROP TABLE ===
Table dropped

Basic CRUD operations completed!
```

## Related Resources

- **Source Code**: [View on GitHub](https://github.com/pingcap/pytidb/tree/main/examples/basic)