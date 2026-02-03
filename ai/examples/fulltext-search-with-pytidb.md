---
title: Full-Text Search Example
summary: Perform traditional text search using TiDB full-text search.
---

# Full-Text Search Example

This example demonstrates how to build an e-commerce product search app using TiDB full-text search with multilingual support. Users of this app can search for products by keywords in their preferred language.

<p align="center">
  <img width="700" alt="E-commerce product search with full-text search" src="https://github.com/user-attachments/assets/c81ddad4-f996-4b1f-85c0-5cbb55bc2a3a" />
  <p align="center"><i>E-commerce product search with full-text search</i></p>
</p>

## Prerequisites

- **Python 3.10+**
- **A TiDB Cloud Starter cluster** (Go to <https://tidbcloud.com/> to create a free cluster for quick testing)

## How to run

### Step 1. Clone the repository

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/fulltext_search/
```

### Step 2. Install the required packages and set up the environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### Step 3. Set up environment to connect to database

In the [TiDB Cloud console](https://tidbcloud.com/), create a cluster if you don't have one, and then copy the connection parameters from the connection dialog.

```bash
cat > .env <<EOF
TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USERNAME={prefix}.root
TIDB_PASSWORD={password}
TIDB_DATABASE=pytidb_fulltext_demo
EOF
```

### Step 4. Run the Streamlit app

```bash
streamlit run app.py
```

Open the browser and visit `http://localhost:8501`.

## Related resources

- **Source Code**: [View on GitHub](https://github.com/pingcap/pytidb/tree/main/examples/fulltext_search)