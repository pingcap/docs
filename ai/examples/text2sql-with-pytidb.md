---
title: Text2SQL Example
summary: Convert natural language queries into SQL statements using AI models.
---

# Text2SQL Example

This demo shows how to build an AI-powered interface that converts natural-language questions into SQL queries and executes them against TiDB. Built with PyTiDB, OpenAI GPT, and Streamlit, it lets you query your database using plain English.

## Prerequisites

- **Python 3.10+**
- **A TiDB Cloud Starter cluster** (Go to <https://tidbcloud.com/> to create a free cluster for quick testing)
- **OpenAI API key** (Get an API key from [OpenAI](https://platform.openai.com/api-keys))

## How to run

### Step 1. Clone the repository

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

Open the browser and visit `http://localhost:8501`

* Enter your OpenAI API key in the left sidebar
* Enter the TiDB connection string in the left sidebar, for example: `mysql+pymysql://root@localhost:4000/test`

## Related resources

- **Source Code**: [View on GitHub](https://github.com/pingcap/pytidb/tree/main/examples/text2sql)