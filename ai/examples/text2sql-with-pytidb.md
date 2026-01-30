---
title: Text2SQL
description: "Convert natural language queries into SQL statements using AI models."
source_repo: "https://github.com/pingcap/pytidb/tree/main/examples/text2sql"
---

# Text2SQL Demo

This demo showcases an AI-powered interface that converts natural language questions into SQL queries and executes them against TiDB. Built with PyTiDB, OpenAI GPT, and Streamlit, it provides a seamless way to interact with your database using plain English.

## Prerequisites

- **Python 3.10+**
- **A TiDB Cloud Starter cluster**: Create a free cluster here: [tidbcloud.com ↗️](https://tidbcloud.com/?utm_source=github&utm_medium=referral&utm_campaign=pytidb_readme)
- **OpenAI API Key**: Get your API key at [OpenAI Platform ↗️](https://platform.openai.com/api-keys)


## How to run

**Step 1**: Clone the repository

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/text2sql/;
```

**Step 2**: Install the required packages

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

**Step 3**: Run the Streamlit app

```bash
streamlit run app.py
```

**Step 4**: Run streamlit app

Open the browser and visit `http://localhost:8501`

* Input OpenAI API key in left sidebar
* Input the TiDB Cloud connection string in left sidebar, the format is `mysql+pymysql://root@localhost:4000/test`

---

## Related Resources

- **Source Code**: [View on GitHub](https://github.com/pingcap/pytidb/tree/main/examples/text2sql)
- **Category**: Ai-Apps

- **Description**: Convert natural language queries into SQL statements using AI models.


[🏠 Back to Demo Gallery](../index.md){ .md-button .md-button--primary } 