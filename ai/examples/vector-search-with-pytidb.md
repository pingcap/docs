---
title: Vector Search Example
summary: Implement semantic search using vector embeddings to find similar content.
---

# Vector Search Example

This example demonstrates how to build a semantic search application using TiDB and local embedding models. It leverages vector search to find similar items based on meaning, not just keywords. The app uses Streamlit for the web UI and Ollama for local embedding generation.

<p align="center">
  <img width="700" alt="Semantic search with vector embeddings" src="https://github.com/user-attachments/assets/6d7783a5-ce9c-4dcc-8b95-49d5f0ca735a" />
  <p align="center"><i>Semantic search with vector embeddings</i></p>
</p>

## Prerequisites

- **Python 3.10+**
- **A TiDB Cloud Starter cluster**: Create a free cluster here: [tidbcloud.com ↗️](https://tidbcloud.com/?utm_source=github&utm_medium=referral&utm_campaign=pytidb_readme)
- **Ollama**: You can install it from [Ollama ↗️](https://ollama.com/download)

## How to run

### Step 1. Start the embedding service with Ollama

Pull the embedding model:

```bash
ollama pull mxbai-embed-large
```

Test the embedding service to make sure it is running:

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

### Step 4. Set up environment to connect to TiDB

Go to [TiDB Cloud console](https://tidbcloud.com/clusters) and get the connection parameters, then set up the environment variable like this:

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