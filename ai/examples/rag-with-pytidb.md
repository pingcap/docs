---
title: RAG Example
summary: Build a RAG application that combines document retrieval with language generation.
---

# RAG Example

This example demonstrates how to use [`pytidb`](https://github.com/pingcap/pytidb) (the official Python SDK for TiDB) to build a minimal RAG application.

The application uses [Ollama](https://ollama.com/download) for local embedding generation, [Streamlit](https://streamlit.io/) for the web UI, and `pytidb` to build the RAG pipeline.

<p align="center">
  <img src="https://docs-download.pingcap.com/media/images/docs/ai/rag-application-built-with-pytidb.png" alt="RAG application built with PyTiDB" width="600" />
  <p align="center"><i>RAG application built with PyTiDB</i></p>
</p>

## Prerequisites

Before you begin, ensure you have the following:

- **Python (>=3.10)**: Install [Python](https://www.python.org/downloads/) 3.10 or a later version.
- **A TiDB Cloud Starter cluster**: You can create a free TiDB cluster on [TiDB Cloud](https://tidbcloud.com/free-trial).
- **Ollama**: Install from [Ollama](https://ollama.com/download).

## How to run

### Step 1. Prepare the inference API

Pull the embedding and LLM models with the Ollama CLI:

```bash
ollama pull mxbai-embed-large
ollama pull gemma3:4b
ollama run gemma3:4b
```

Verify that the `/embed` and `/generate` endpoints are running:

```bash
curl http://localhost:11434/api/embed -d '{
  "model": "mxbai-embed-large",
  "input": "Llamas are members of the camelid family"
}'
```

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "gemma3:4b",
  "prompt": "Hello, Who are you?"
}'
```

### Step 2. Clone the repository

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/rag/
```

### Step 3. Install the required packages and set up the environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### Step 4. Set environment variables

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/clusters) page, and then click the name of your target cluster to go to its overview page.
2. Click **Connect** in the upper-right corner. A connection dialog is displayed, with connection parameters listed.
3. Set environment variables according to the connection parameters as follows:

```bash
cat > .env <<EOF
TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USERNAME={prefix}.root
TIDB_PASSWORD={password}
TIDB_DATABASE=test
EOF
```

### Step 5. Run the Streamlit app

```bash
streamlit run main.py
```

Open your browser and visit `http://localhost:8501`.

## Troubleshooting

### `502 Bad Gateway` Error

Try disabling your global proxy settings.

## Related resources

- **Source Code**: [View on GitHub](https://github.com/pingcap/pytidb/tree/main/examples/rag)