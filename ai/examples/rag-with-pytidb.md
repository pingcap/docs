---
title: RAG Example
summary: Build a RAG application that combines document retrieval with language generation.
---

# RAG Example

This example demonstrates how to use PyTiDB to build a minimal RAG application.

The application uses [Ollama](https://ollama.com/download) for local embedding generation, [Streamlit](https://streamlit.io/) for the web UI, and [PyTiDB](https://github.com/pingcap/pytidb) to build the RAG pipeline.

<p align="center">
  <img src="https://github.com/user-attachments/assets/dfd85672-65ce-4a46-8dd2-9f77d826363e" alt="RAG application built with PyTiDB" width="600" />
  <p align="center"><i>RAG application built with PyTiDB</i></p>
</p>

## Prerequisites

- **Python 3.10+**
- **A TiDB Cloud Starter cluster** (Go to <https://tidbcloud.com/> to create a free cluster for quick testing)
- **Ollama** (Install from [Ollama](https://ollama.com/download))

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

### Step 4. Set up environment to connect to database

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

### Step 5. Run the Streamlit app

```bash
streamlit run main.py
```

Open the browser and visit `http://localhost:8501`

## Troubleshooting

### `502 Bad Gateway` Error

Try disabling your global proxy settings.

## Related resources

- **Source Code**: [View on GitHub](https://github.com/pingcap/pytidb/tree/main/examples/rag)