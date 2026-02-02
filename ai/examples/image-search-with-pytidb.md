---
title: Image Search Example
summary: Build an image search application using multimodal embeddings for both text-to-image and image-to-image search.
---

# Image Search Example

This example showcases how to build a powerful image search application by combining TiDB's vector search capabilities with multimodal embedding models.

With just a few lines of code, you can create an intelligent search system that understands both text and images.

- 🔍 **Text-to-Image Search**: Find the perfect pet photos by describing what you're looking for in natural language - from "fluffy orange cat"
- 🖼️ **Image-to-Image Search**: Upload a photo and instantly discover visually similar pets based on breed, color, pose and more

<p align="center">
  <img width="700" alt="PyTiDB Image Search Demo" src="https://github.com/user-attachments/assets/7ba9733a-4d1f-4094-8edb-58731ebd08e9" />
  <p align="center"><i>Pet image search via multimodal embeddings</i></p>
</p>


## Prerequisites

- **Python 3.10+**
- **A TiDB Cloud Starter cluster**: Create a free cluster here: [tidbcloud.com ↗️](https://tidbcloud.com/?utm_source=github&utm_medium=referral&utm_campaign=pytidb_readme)
- **Jina AI API Key**: Get your free API key at [jina.ai Embeddings ↗️](https://jina.ai/embeddings/)

## How to run

### Step 1. Clone the repository

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

### Step 3. Set up environment variables

Go to [TiDB Cloud console](https://tidbcloud.com/clusters) and get the connection parameters, then set up the environment variable like this:

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

In this demo, we will use the [Oxford Pets dataset](https://www.robots.ox.ac.uk/~vgg/data/pets/) to load pet images to the database for search.

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

Open `http://localhost:8501` in your browser.

### Step 6. Load data

In the sample app, you can click the **Load Sample Data** button to load some sample data to the database.

Or if you want to load all the data in the Oxford Pets dataset, click the **Load All Data** button.

### Step 7. Search

1. Select the **Search type** in the sidebar
2. Input a text description of the pet you're looking for, or upload a photo of a dog or cat
3. Click the **Search** button

## Related resources

- **Source Code**: [View on GitHub](https://github.com/pingcap/pytidb/tree/main/examples/image_search)