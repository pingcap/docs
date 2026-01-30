# Embeddings Integration

## Overview

TiDB provides a unified interface for integrating with various embedding providers and models:

- **Programmatic use**: Use the `EmbeddingFunction` class from the AI SDK to create embedding functions for specific providers or models.
- **SQL use**: Use the `EMBED_TEXT` function to generate embeddings directly from text data.


## Embedding Function

=== "Python"

  Use the `EmbeddingFunction` class to work with different embedding providers and models.

  ```python
  from pytidb.embeddings import EmbeddingFunction

  embed_func = EmbeddingFunction(
      model_name="<provider_name>/<model_name>",
  )
  ```

  **Parameters:**

  - `model_name` *(required)*:  
    Specifies the embedding model to use, in the format `{provider_name}/{model_name}`.

  - `dimensions` *(optional)*:
    The dimensionality of output vector embeddings. If not provided and the model lacks a default dimension, a test string is embedded during initialization to determine the actual dimension automatically.

  - `api_key` *(optional)*: 
    The API key for accessing the embedding service. If not explicitly set, retrieves the key from the provider's default environment variable.

  - `api_base` *(optional)*:
    The base URL of the embedding API service.

  - `use_server` *(optional)*:
    Whether to use TiDB Cloud's hosted embedding service. Defaults to `True` for TiDB Cloud Starter.

  - `multimodal` *(optional)*:
    Whether to use a multimodal embedding model. When enabled, `use_server` is automatically set to `False`, and the embedding service is called client-side.

=== "SQL"

  ```sql
  SELECT EMBED_TEXT('{model_id}', '{text}', '{extra_params}');
  ```

  **Parameters:**

  - `model_id` *(required)*:
    The ID of the embedding model, in the format `{provider_name}/{model_name}`, for example, `tidbcloud_free/amazon/titan-embed-text-v2`.

  - `text` *(required)*:
    The text to generate embeddings from.

  - `extra_params` *(optional)*:
    Additional parameters sent to the embedding API. Refer to the embedding provider's documentation for supported parameters.

## Supported Providers

The following embedding providers are supported. Click on the corresponding provider to learn how to integrate and enable automatic embedding for your data.

- [TiDB Cloud Hosted](embedding-tidb-cloud-hosted.md)
- [OpenAI](embedding-openai.md)
- [OpenAI Compatible](embedding-openai-compatible.md) 
- [Cohere](embedding-cohere.md)
- [Jina AI](embedding-jinaai.md)
- [Google Gemini](embedding-gemini.md)
- [Hugging Face](embedding-huggingface.md)
- [NVIDIA NIM](embedding-nvidia-nim.md)
