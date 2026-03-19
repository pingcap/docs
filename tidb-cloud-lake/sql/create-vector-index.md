---
title: CREATE VECTOR INDEX
summary: Creates a Vector index on a VECTOR column for a table to enable efficient similarity search using the HNSW (Hierarchical Navigable Small World) algorithm.
---

# CREATE VECTOR INDEX

> **Note:**
>
> Introduced or updated in v1.2.777.

Creates a Vector index on a [VECTOR](/tidb-cloud-lake/sql/vector.md) column for a table to enable efficient similarity search using the HNSW (Hierarchical Navigable Small World) algorithm.

## Syntax

```sql
-- Create a Vector index on an existing table
CREATE [OR REPLACE] VECTOR INDEX [IF NOT EXISTS] <index_name>
ON [<database>.]<table_name>(<column>)
distance = '<metric>' [m = <number>] [ef_construct = <number>]

-- Create a Vector index when creating a table
CREATE [OR REPLACE] TABLE <table_name> (
    <column_definitions>,
    VECTOR INDEX <index_name> (<column>)
        distance = '<metric>' [m = <number>] [ef_construct = <number>]
)...
```

### Parameters

- **`distance`** (required) - Specifies the distance metric(s) to use for similarity search. Multiple metrics can be combined with commas:
  - `'cosine'` - Cosine distance (best for semantic similarity, text embeddings)
  - `'l1'` - L1 distance / Manhattan distance (good for feature comparison, sparse data)
  - `'l2'` - L2 distance / Euclidean distance (best for geometric similarity, image features)
  - Example: `distance = 'cosine,l1,l2'` supports all three metrics

- **`m`** (optional, default: 16) - Controls the number of bidirectional connections each node has in the HNSW graph:
  - Higher values increase memory usage but can improve search accuracy
  - Must be greater than 0
  - Typical range: 8-64

- **`ef_construct`** (optional, default: 100) - Controls the size of the dynamic candidate list during index construction:
  - Higher values improve index quality but increase construction time and memory
  - Must be >= 40
  - Typical range: 40-500

## How Vector Index Works

Vector indexes in Databend use the HNSW algorithm to build a multi-layered graph structure:

1. **Graph Structure**: Each vector is a node with connections to its nearest neighbors
2. **Search Process**: Queries navigate through graph layers, from coarse to fine, to find approximate nearest neighbors quickly
3. **Quantization**: Raw vectors are quantized to reduce storage and improve query performance (with negligible accuracy loss)
4. **Automatic Building**: The index is automatically built as data is written. Every INSERT, COPY, or data load operation automatically generates the index for new rows - no manual maintenance required

## Examples

### Creating a Table with Vector Index

```sql
-- Simple vector index for embeddings
CREATE TABLE documents (
    id INT,
    title VARCHAR,
    content TEXT,
    embedding VECTOR(1024),
    VECTOR INDEX idx_embedding(embedding) distance = 'cosine'
);
```

### Creating a Vector Index with Custom Parameters

```sql
-- Vector index with multiple distance metrics and tuned parameters
CREATE TABLE images (
    id INT,
    filename VARCHAR,
    feature_vector VECTOR(512),
    VECTOR INDEX idx_features(feature_vector)
        distance = 'cosine,l2'
        m = 32
        ef_construct = 200
);
```

### Creating a Vector Index on an Existing Table

```sql
CREATE TABLE products (
    id INT,
    name VARCHAR,
    description TEXT,
    embedding VECTOR(768)
);

-- Add vector index after table creation
CREATE VECTOR INDEX idx_product_embedding
ON products(embedding)
distance = 'cosine,l1,l2'
m = 20
ef_construct = 150;
```

### Multiple Vector Indexes on Different Columns

```sql
CREATE TABLE multimodal_data (
    id INT,
    text_embedding VECTOR(384),
    image_embedding VECTOR(512),
    VECTOR INDEX idx_text(text_embedding) distance = 'cosine',
    VECTOR INDEX idx_image(image_embedding) distance = 'l2'
);
```

### Viewing Indexes

Use [SHOW INDEXES](/tidb-cloud-lake/sql/show-indexes.md) to view all indexes:

```sql
SHOW INDEXES;
```

Result:
```
┌──────────────────────┬────────┬──────────┬────────────────────────────┬──────────────────────────┐
│ name                 │ type   │ original │ definition                 │ created_on               │
├──────────────────────┼────────┼──────────┼────────────────────────────┼──────────────────────────┤
│ idx_embedding        │ VECTOR │          │ documents(embedding)       │ 2025-05-13 01:22:34.123  │
│ idx_product_embedding│ VECTOR │          │ products(embedding)        │ 2025-05-13 01:23:45.678  │
└──────────────────────┴────────┴──────────┴────────────────────────────┴──────────────────────────┘
```

### Using Vector Index for Similarity Search

```sql
-- Create a table with vector index
CREATE TABLE wiki_articles (
    id INT,
    title VARCHAR,
    embedding VECTOR(8),
    VECTOR INDEX idx_embedding(embedding) distance = 'cosine'
);

-- Insert sample data (8-dimensional vectors for demonstration)
INSERT INTO wiki_articles VALUES
(1, 'Machine Learning', [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]),
(2, 'Deep Learning', [0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85]),
(3, 'Natural Language Processing', [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]),
(4, 'Computer Vision', [0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]);

-- Find the 2 most similar articles to a query vector using cosine distance
SELECT id, title, cosine_distance(embedding, [0.12, 0.22, 0.32, 0.42, 0.52, 0.62, 0.72, 0.82]) AS distance
FROM wiki_articles
ORDER BY distance ASC
LIMIT 2;
```

Result:
```
┌────┬─────────────────┬──────────────┐
│ id │ title           │ distance     │
├────┼─────────────────┼──────────────┤
│  1 │ Machine Learning│ 0.00012345   │
│  2 │ Deep Learning   │ 0.00023456   │
└────┴─────────────────┴──────────────┘
```

## Performance Tuning

### Choosing Distance Metrics

Choose the appropriate distance metric based on your use case. See [Vector Functions](/tidb-cloud-lake/sql/vector-functions.md) for querying with distance functions.

- **Cosine distance**: Best for text embeddings from models like BERT, GPT, where vector magnitude doesn't matter
- **L2 (Euclidean) distance**: Best for image features, spatial data where absolute differences matter
- **L1 (Manhattan) distance**: Good for sparse vectors and when you want to emphasize individual dimension differences

### Tuning HNSW Parameters

| Parameter      | Lower Value                          | Higher Value                         |
|----------------|--------------------------------------|--------------------------------------|
| `m`            | Less memory, faster construction     | Better accuracy, more memory         |
| `ef_construct` | Faster construction, lower quality   | Better quality, slower construction  |

**Recommended configurations:**

- **Small datasets (< 100K vectors)**: Default settings (`m=16`, `ef_construct=100`)
- **Medium datasets (100K - 1M vectors)**: `m=24`, `ef_construct=150`
- **Large datasets (> 1M vectors)**: `m=32`, `ef_construct=200`
- **High accuracy requirements**: `m=48`, `ef_construct=300`

## Limitations

- Vector indexes only support columns with [VECTOR](/tidb-cloud-lake/sql/vector.md) data type
- The `distance` parameter is required; indexes without it will be ignored
- Quantization may introduce negligible errors in distance calculations (typically < 0.01%)
- Index size increases with higher `m` values (approximately `m * vector_dimension * 4 bytes` per vector)
