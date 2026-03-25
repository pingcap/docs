---
title: Text2SQL Example
summary: Convert natural language queries into SQL statements using AI models.
---

# Text2SQL Example

This demo shows how to build an AI-powered interface that converts natural-language questions into SQL queries and executes them against TiDB. Built with [`pytidb`](https://github.com/pingcap/pytidb) (the official Python SDK for TiDB), OpenAI GPT, and Streamlit, it lets you query your database using plain English.

## Prerequisites

Before you begin, ensure you have the following:

- **Python (>=3.10)**: Install [Python](https://www.python.org/downloads/) 3.10 or a later version.
- **A TiDB Cloud Starter cluster**: You can create a free TiDB cluster on [TiDB Cloud](https://tidbcloud.com/free-trial).
- **OpenAI API key**: Get an OpenAI API key from [OpenAI](https://platform.openai.com/api-keys).

## How to run

### Step 1. Clone the `pytidb` repository

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/text2sql/
```

### Step 2. Install the required packages

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### Step 3. Run the Streamlit app

```bash
streamlit run app.py
```

### Step 4. Use the app

Open your browser and visit `http://localhost:8501`.

1. Enter your OpenAI API key in the left sidebar
2. Enter the TiDB connection string in the left sidebar, for example: `mysql+pymysql://root@localhost:4000/test`

## Related resources

- **Source Code**: [View on GitHub](https://github.com/pingcap/pytidb/tree/main/examples/text2sql)