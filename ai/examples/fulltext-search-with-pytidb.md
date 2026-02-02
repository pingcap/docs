---
title: Fulltext Search Example
summary: Perform traditional text search using MySQL fulltext search capabilities.
---

# Full-Text Search Example

This example demonstrates how to build an E-commerce product search application using TiDB's full-text search feature with multilingual support. Users can search for products by keywords in their preferred language.

<p align="center">
  <img width="700" alt="E-commerce product search with full-text search" src="https://github.com/user-attachments/assets/c81ddad4-f996-4b1f-85c0-5cbb55bc2a3a" />
  <p align="center"><i>E-commerce product search with full-text search</i></p>
</p>

## Prerequisites

- **Python 3.10+**
- **A TiDB Cloud Starter cluster**: Create a free cluster here: [tidbcloud.com ↗️](https://tidbcloud.com/?utm_source=github&utm_medium=referral&utm_campaign=pytidb_readme)

## How to run

### Step 1. Clone the repository

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/fulltext_search/;
```

### Step 2. Install the required packages and setup environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### Step 3. Set up environment to connect to database

Go to the [TiDB Cloud console](https://tidbcloud.com/), create a new cluster if you don't have one, and then get the connection parameters on the connection dialog.

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