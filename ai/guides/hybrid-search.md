# Hybrid Search

Hybrid search is a technique that combines multiple search algorithms to deliver more accurate and relevant results.

TiDB supports both semantic search (also known as vector search) and keyword-based search (full-text search). By leveraging the strengths of both approaches, you can achieve superior search results through hybrid search.

<p align="center">
    <img src="https://docs-download.pingcap.com/media/images/docs/vector-search/hybrid-search-overview.svg" alt="hybrid search overview" width="800"/>
</p>

!!! tip

    For a complete example of hybrid search, refer to the [hybrid-search example](../examples/hybrid-search-with-pytidb.md).


## Basic Usage

### Step 1. Define an Embedding Function

Define an embedding function to generate vector representations of text data.

```python
from pytidb.embeddings import EmbeddingFunction

embed_fn = EmbeddingFunction(
    model_name="openai/text-embedding-3-small",
    api_key=os.getenv("OPENAI_API_KEY"),
)
```

### Step 2. Create a Table with Vector and Full-Text Indexes

=== "Python"

    After you have [connected to your TiDB database](./connect.md) using `TiDBClient` and get the `client` instance:

    You can now create a table with both a `FullTextField` and a `VectorField` to store the text data and its vector embedding.

    Example:

    ```python
    from pytidb.schema import TableModel, Field, FullTextField

    class Chunk(TableModel):
        __tablename__ = "chunks_for_hybrid_search"
        id: int = Field(primary_key=True)
        text: str = FullTextField()
        text_vec: list[float] = embed_fn.VectorField(source_field="text")

    table = client.create_table(schema=Chunk, if_exists="overwrite")
    ```

    In this example, PyTiDB will automatically create a full-text index on the `text` column and a vector index on the `text_vec` column.

### Step 3. Insert Sample Data

=== "Python"

    Use the `bulk_insert()` method to insert sample data into the table.

    ```python
    table.truncate()
    table.bulk_insert([
        Chunk(
            text="TiDB is a distributed database that supports OLTP, OLAP, HTAP and AI workloads.",
        ),
        Chunk(
            text="PyTiDB is a Python library for developers to connect to TiDB.",
        ),
        Chunk(
            text="LlamaIndex is a Python library for building AI-powered applications.",
        ),
    ])
    ```

    The `text_vec` field is automatically populated with the vector embedding of the text data via the [Auto Embedding](../guides/auto-embedding.md) feature.

### Step 4. Perform Hybrid Search

To enable hybrid search, set the `search_type` parameter to `hybrid` when calling the `search()` method.

```python
results = (
    table.search(
        "AI database", search_type="hybrid"
    )
    .limit(3)
    .to_list()
)

for item in results:
    item.pop("text_vec")
print(json.dumps(results, indent=4, sort_keys=True))
```

The search results contain three special fields:

- `_distance`: The distance between the query vector and the vector data in the table, as returned by the vector search.
- `_match_score`: The match score between the query and the text field, as returned by the full-text search.
- `_score`: The final score of the search result, calculated by the fusion algorithm.

```json title="Output"
[
    {
        "_distance": 0.4740166257687124,
        "_match_score": 1.6804268,
        "_score": 0.03278688524590164,
        "id": 60013,
        "text": "TiDB is a distributed database that supports OLTP, OLAP, HTAP and AI workloads."
    },
    {
        "_distance": 0.6428459116216618,
        "_match_score": 0.78427225,
        "_score": 0.03200204813108039,
        "id": 60015,
        "text": "LlamaIndex is a Python library for building AI-powered applications."
    },
    {
        "_distance": 0.641581407158715,
        "_match_score": null,
        "_score": 0.016129032258064516,
        "id": 60014,
        "text": "PyTiDB is a Python library for developers to connect to TiDB."
    }
]
```


## Fusion Methods

Fusion methods combine results from vector (semantic) and full-text (keyword) searches into a single, unified ranking. This ensures that the final results leverage both semantic relevance and keyword matching.

PyTiDB supports two fusion methods:

- `rrf`: Reciprocal Rank Fusion (default)
- `weighted`: Weighted Score Fusion

You can select the fusion method that best fits your use case to optimize hybrid search results.

### Reciprocal Rank Fusion (RRF)

Reciprocal Rank Fusion (RRF) is an algorithm that evaluates search results by leveraging the rank of documents in multiple result sets.

For more details, see the [RRF paper](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf).

=== "Python"

    Enable reciprocal rank fusion by specifying the `method` parameter as `"rrf"` in the `.fusion()` method.

    ```python
    results = (
        table.search(
            "AI database", search_type="hybrid"
        )
        .fusion(method="rrf")
        .limit(3)
        .to_list()
    )
    ```

    Parameters:

    - `k`: A constant (default: 60) to prevent division by zero and control the impact of high-ranked documents.

### Weighted Score Fusion

Weighted Score Fusion combines vector search and full-text search scores using weighted sum:

```python
final_score = vs_weight * vector_score + fts_weight * fulltext_score
```

=== "Python"

    Enable weighted score fusion by specifying the `method` parameter as `"weighted"` in the `.fusion()` method.

    For example, to give more weight to vector search, set the `vs_weight` parameter to 0.7 and the `fts_weight` parameter to 0.3:

    ```python
    results = (
        table.search(
            "AI database", search_type="hybrid"
        )
        .fusion(method="weighted", vs_weight=0.7, fts_weight=0.3)
        .limit(3)
        .to_list()
    )
    ```

    Parameters:

    - `vs_weight`: The weight of the vector search score.
    - `fts_weight`: The weight of the full-text search score.


## Rerank Method

Hybrid search also supports reranking using reranker-specific models. 

=== "Python"

    Use the `rerank()` method to specify a reranker that sorts search results by relevance between the query and the documents.

    **Example: Using JinaAI Reranker to rerank the hybrid search results**

    ```python
    reranker = Reranker(
        # Use the `jina-reranker-m0` model
        model_name="jina_ai/jina-reranker-m0",
        api_key="{your-jinaai-api-key}"
    )

    results = (
        table.search(
            "AI database", search_type="hybrid"
        )
        .fusion(method="rrf", k=60)
        .rerank(reranker, "text")
        .limit(3)
        .to_list()
    )
    ```

    To check other reranker models, see the [Reranking](../guides/reranking.md) guide.
