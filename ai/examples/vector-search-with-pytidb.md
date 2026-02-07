---
title: Vector Search Example
summary: Implement semantic search using vector embeddings to find similar content.
---

# Vector Search Example

This example demonstrates how to build a semantic search application using TiDB and local embedding models. It uses vector search to find similar items by meaning (not just keywords).

The application uses [Ollama](https://ollama.com/download) for local embedding generation, [Streamlit](https://streamlit.io/) for the web UI, and [`pytidb`](https://github.com/pingcap/pytidb) (the official Python SDK for TiDB) to build the RAG pipeline.

<p align="center">
  <img width="700" alt="Semantic search with vector embeddings" src="https://github.com/user-attachments/assets/6d7783a5-ce9c-4dcc-8b95-49d5f0ca735a" />
  <p align="center"><i>Semantic search with vector embeddings</i></p>
</p>

## Prerequisites

Before you begin, ensure you have the following:

- **Python (>=3.10)**: Install [Python](https://www.python.org/downloads/) 3.10 or a later version.
- **A TiDB Cloud Starter cluster**: You can create a free TiDB cluster on [TiDB Cloud](https://tidbcloud.com/free-trial).
- **Ollama**: Install from [Ollama](https://ollama.com/download).

## How to run

### Step 1. Start the embedding service with Ollama

Pull the embedding model:

```bash
ollama pull mxbai-embed-large
```

Verify that the embedding service is running:

```bash
curl http://localhost:11434/api/embed -d '{
  "model": "mxbai-embed-large",
  "input": "Llamas are members of the camelid family"
}'
```

### Step 2. Clone the repository

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/vector_search/
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
    TIDB_DATABASE=pytidb_vector_search
    EOF
    ```

### Step 5. Run the Streamlit app

```bash
streamlit run app.py
```

Open your browser and visit `http://localhost:8501`.

## Related resources

- **Source Code**: [View on GitHub](https://github.com/pingcap/pytidb/tree/main/examples/vector_search)