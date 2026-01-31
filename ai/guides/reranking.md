---
title: Reranking
summary: Learn how to use reranking in your application.
---

# Reranking

Reranking is a technique used to improve the relevance and accuracy of search results by re-evaluating and reordering them using a dedicated rerank model.

The search process works in two stages:

1. **Initial Retrieval**: Vector search identifies the top `k` most similar documents from the collection
2. **Reranking**: A reranking model evaluates these `k` documents based on the relevance between the query and the documents and reorders them to produce the final top `n` results (where `n` ≤ `k`)

This two-stage retrieval approach significantly improves both document relevance and accuracy.

## Basic usage

PyTiDB provides the `Reranker` class that allows you to use reranker models from multiple third-party providers.

1. Create a reranker instance

    ```python
    from pytidb.rerankers import Reranker

    reranker = Reranker(model_name="{provider}/{model_name}")
    ```

2. Apply reranker via `.rerank()` method

    ```python
    table.search("{query}").rerank(reranker, "{field_to_rerank}").limit(3)
    ```

## Supported providers

Here are some examples to use reranker models from third-party providers.

### Jina AI

To use the reranker provided by Jina AI, go to their [website](https://jina.ai/reranker) to create an API key.

For example:

```python
jinaai = Reranker(
    # Using the `jina-reranker-m0` model
    model_name="jina_ai/jina-reranker-m0",
    api_key="{your-jinaai-api-key}"
)
```
