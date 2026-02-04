---
title: Hybrid Search Example
summary: Combine vector search and full-text search for more comprehensive results.
---

# Hybrid Search Example

This demo shows how to combine vector search and full-text search to improve the retrieval quality over a document set.

<p align="center">
    <img src="https://github.com/user-attachments/assets/6e1c639d-2160-44c8-86b4-958913b9eca5" alt="TiDB Hybrid Search Demo" width="700"/>
    <p align="center"><i>TiDB Hybrid Search Demo</i></p>
</p>

## Prerequisites

Before you begin, ensure you have the following:

- **Python (>=3.10)**: Install [Python](https://www.python.org/downloads/) 3.10 or a later version.
- **A TiDB Cloud Starter cluster**: You can create a free TiDB cluster on [TiDB Cloud](https://tidbcloud.com/free-trial).
- **OpenAI API key**: Get an OpenAI API key from [OpenAI](https://platform.openai.com/api-keys).

> **Note**
>
> Currently, full-text search is available only in the following product option and regions:
>
> - TiDB Cloud Starter: Frankfurt (`eu-central-1`), Singapore (`ap-southeast-1`)

## How to run

### Step 1. Clone the `pytidb` repository

[pytidb](https://github.com/pingcap/pytidb) is the official Python SDK for TiDB, designed to help developers build AI applications efficiently.

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/hybrid_search
```

### Step 2. Install the required packages and set up the environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### Step 3. Set environment variables

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/clusters) page, and then click the name of your target cluster to go to its overview page.
2. Click **Connect** in the upper-right corner. A connection dialog is displayed, with connection parameters listed.
3. Set environment variables according to the connection parameters as follows:

```bash
cat > .env <<EOF
TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USERNAME={prefix}.root
TIDB_PASSWORD={password}
TIDB_DATABASE=pytidb_hybrid_demo
OPENAI_API_KEY=<your-openai-api-key>
EOF
```

### Step 4. Run the demo

### Option 1. Run the Streamlit app

If you want to check the demo with a web UI, you can run the following command:

```bash
streamlit run app.py
```

Open your browser and visit `http://localhost:8501`

### Option 2. Run the demo script

If you want to check the demo with a script, you can run the following command:

```bash
python example.py
```

Expected output:

```
=== CONNECT TO TIDB ===
Connected to TiDB.

=== CREATE TABLE ===
Table created.

=== INSERT SAMPLE DATA ===
Inserted 3 rows.

=== PERFORM HYBRID SEARCH ===
Search results:
[
    {
        "_distance": 0.4740166257687124,
        "_match_score": 1.6804268,
        "_score": 0.03278688524590164,
        "id": 60013,
        "text": "TiDB is a distributed database that supports OLTP, OLAP, HTAP and AI workloads."
    },
    {
        "_distance": 0.6428459116216618,
        "_match_score": 0.78427225,
        "_score": 0.03200204813108039,
        "id": 60015,
        "text": "LlamaIndex is a Python library for building AI-powered applications."
    },
    {
        "_distance": 0.641581407158715,
        "_match_score": null,
        "_score": 0.016129032258064516,
        "id": 60014,
        "text": "PyTiDB is a Python library for developers to connect to TiDB."
    }
]
```

## Related resources

- **Source Code**: [View on GitHub](https://github.com/pingcap/pytidb/tree/main/examples/hybrid_search)