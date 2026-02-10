---
title: Image Search Example
summary: Build an image search application using multimodal embeddings for both text-to-image and image-to-image search.
---

# Image Search Example

This example shows how to build an image search app by combining TiDB vector search capabilities with multimodal embedding models.

With just a few lines of code, you can create a search system that understands both text and images.

- **Text-to-image search**: Find pet photos by describing what you want in natural language, such as "fluffy orange cat"
- **Image-to-image search**: Upload a photo to find visually similar pets by breed, color, pose, and more

<p align="center">
  <img width="700" alt="PyTiDB Image Search Demo" src="https://docs-download.pingcap.com/media/images/docs/ai/pet-image-search-via-multimodal-embeddings.png" />
  <p align="center"><i>Pet image search via multimodal embeddings</i></p>
</p>

## Prerequisites

Before you begin, ensure you have the following:

- **Python (>=3.10)**: Install [Python](https://www.python.org/downloads/) 3.10 or a later version.
- **A TiDB Cloud Starter cluster**: You can create a free TiDB cluster on [TiDB Cloud](https://tidbcloud.com/free-trial).
- **Jina AI API key**: You can get a free API key from [Jina AI Embeddings](https://jina.ai/embeddings/).

## How to run

### Step 1. Clone the `pytidb` repository

[`pytidb`](https://github.com/pingcap/pytidb) is the official Python SDK for TiDB, designed to help developers build AI applications efficiently.

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/image_search/
```

### Step 2. Install the required packages

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
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
TIDB_DATABASE=test

JINA_AI_API_KEY={your-jina-ai-api-key}
EOF
```

### Step 4. Download and extract the dataset

This demo uses the [Oxford Pets dataset](https://www.robots.ox.ac.uk/~vgg/data/pets/) to load pet images into the database for search.

*For Linux/MacOS:*

```bash
# Download the dataset
curl -L -o oxford_pets.tar.gz "https://thor.robots.ox.ac.uk/~vgg/data/pets/images.tar.gz"

# Extract the dataset
mkdir -p oxford_pets
tar -xzf oxford_pets.tar.gz -C oxford_pets
```

### Step 5. Run the app

```bash
streamlit run app.py
```

Open your browser and visit `http://localhost:8501`.

### Step 6. Load data

In the sample app, you can click the **Load Sample Data** button to load some sample data to the database.

Or if you want to load all the data in the Oxford Pets dataset, click the **Load All Data** button.

### Step 7. Search

1. Select the **Search type** in the sidebar.
2. Input a text description of the pet you're looking for, or upload a photo of a dog or cat.
3. Click the **Search** button.

## Related resources

- **Source Code**: [View on GitHub](https://github.com/pingcap/pytidb/tree/main/examples/image_search)