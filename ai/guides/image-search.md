---
title: Image Search
summary: Learn how to use image search in your application.
---

# Image Search

**Image search** helps you find similar images by comparing their visual content, not just text or metadata. This feature is useful for e-commerce, content moderation, digital asset management, and any scenario where you need to search for or deduplicate images based on appearance.

TiDB enables image search through **vector search**. With automatic embedding, you can generate image embeddings from image URLs, PIL images, or keyword text using a multimodal embedding model. TiDB then searches for similar vectors at scale.

> **Note:**
>
> For a complete example of image search, see [Image Search Example](/ai/examples/image-search-with-pytidb.md).

## Basic usage

### Step 1. Define an embedding function

To generate image embeddings, you need an embedding model that accepts image input.

For demonstration, you can use the multimodal embedding model of Jina AI.

Go to [Jina AI](https://jina.ai/embeddings) to create an API key, and then initialize the embedding function as follows:

```python hl_lines="7"
from pytidb.embeddings import EmbeddingFunction

image_embed = EmbeddingFunction(
    # Or another provider/model that supports multimodal input
    model_name="jina_ai/jina-embedding-v4",
    api_key="{your-jina-api-key}",
    multimodal=True,
)
```

### Step 2. Create a table and vector field

Use `VectorField()` to define a vector field for storing image embeddings. Set the `source_field` parameter to specify the field that stores image URLs.

```python
from pytidb.schema import TableModel, Field

class ImageItem(TableModel):
    __tablename__ = "image_items"
    id: int = Field(primary_key=True)
    image_uri: str = Field()
    image_vec: list[float] = image_embed.VectorField(
        source_field="image_uri"
    )

table = client.create_table(schema=ImageItem, if_exists="overwrite")
```

### Step 3. Insert image data

When you insert data, the `image_vec` field is automatically populated with an embedding generated from `image_uri`.

```python
table.bulk_insert([
    ImageItem(image_uri="https://example.com/image1.jpg"),
    ImageItem(image_uri="https://example.com/image2.jpg"),
    ImageItem(image_uri="https://example.com/image3.jpg"),
])
```

### Step 4. Perform image search

Image search is a type of vector search. With automatic embedding, you can provide an image URL, a PIL image, or keyword text directly, and each input is converted into an embedding for similarity matching.

#### Option 1: Search by image URL

Search for similar images by providing an image URL:

```python
results = table.search("https://example.com/query.jpg").limit(3).to_list()
```

The client converts the image URL into a vector. TiDB then returns the most similar images by comparing vectors.

#### Option 2: Search by PIL image

You can also search for similar images by providing an image file or bytes:

```python
from PIL import Image

image = Image.open("/path/to/query.jpg")

results = table.search(image).limit(3).to_list()
```

The client converts the PIL image object to a Base64 string before sending it to the embedding model.

#### Option 3: Search by keyword text

You can also search for similar images by providing keyword text.

For example, if you are working on a pet image dataset, you can search by keywords such as "orange tabby cat" or "golden retriever puppy" to find similar images.

```python
results = table.search("orange tabby cat").limit(3).to_list()
```

Then, the multimodal embedding model converts the keyword text into an embedding that captures its semantic meaning, and TiDB performs a vector search to find images with embeddings most similar to that keyword embedding.

## See also

- [Automatic embedding guide](/ai/guides/auto-embedding.md)
- [Vector search guide](/ai/concepts/vector-search-overview.md)
- [Image Search Example](/ai/examples/image-search-with-pytidb.md)
