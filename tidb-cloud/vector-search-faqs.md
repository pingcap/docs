---
title: Vector Search FAQs
summary: Learn about the FAQs related to TiDB Vector Search.
---

# Vector Search FAQs

This document lists the most frequently asked questions about TiDB Vector Search.

## General FAQs

### What is TiDB Vector Search?

TiDB Vector search allows you to power generative AI, or implement semantic search or similarity search for texts, images, videos, audios or any type of data. Rather than searching on the data itself, vector search allows you to search on the meanings of the data.

### What are the key use cases?

You can use machine learning models like OpenAI and Hugging Face to create and store vector embeddings in TiDB. Then you can use TiDB Vector Search for retrieval augmented generation (RAG), semantic search, recommendation engines, dynamic personalization, and other use cases.

### Does Vector Search work with articles, images or media files?

Yes. TiDB Vector Search can query any kind of data that can be turned into a vector embedding. You can store both vector embeddings and the data in the same TiDB cluster or even the same table without the need to set up other vector search engines.

### What AI integrations does TiDB Vector Search support?

TiDB Vector has now been integrated into [Langchain](/tidb-cloud/vector-search-integrate-with-langchain.md) and [LlamaIndex](/tidb-cloud/vector-search-integrate-with-llamaindex.md).

### Which vector embeddings does TiDB Vector Search support?

TiDB supports vector embeddings under the 16000-dimension limit.

### How can I speed up the Vector Search?

You can create an index over the vector column to speed up the Vector Search. See Build AI Apps with TiDB Vector Search for more details.

### How do I get support for Vector Search or about general usage of TiDB Serverless?

We value your feedback and always here to help, you can choose either way to get support:

- Discord: https://discord.gg/zcqexutz2R
- Support Portal: https://tidb.support.pingcap.com/