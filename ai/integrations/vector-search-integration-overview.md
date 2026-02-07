---
title: Vector Search Integration Overview
summary: An overview of TiDB vector search integration, including supported AI frameworks, embedding models, and ORM libraries.
aliases: ['/tidb/stable/vector-search-integration-overview/','/tidb/dev/vector-search-integration-overview/','/tidbcloud/vector-search-integration-overview/']
---

# Vector Search Integration Overview

This document provides an overview of TiDB vector search integration, including supported AI frameworks, embedding models, and Object Relational Mapping (ORM) libraries.

> **Note:**
>
> - The vector search feature is in beta. It might be changed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.
> - The vector search feature is available on [TiDB Self-Managed](/overview.md), [{{{ .starter }}}](/tidb-cloud/select-cluster-tier.md#starter), [{{{ .essential }}}](/tidb-cloud/select-cluster-tier.md#essential), and [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated). For TiDB Self-Managed and TiDB Cloud Dedicated, the TiDB version must be v8.4.0 or later (v8.5.0 or later is recommended).

## AI frameworks

TiDB provides official support for the following AI frameworks, enabling you to easily integrate AI applications developed based on these frameworks with TiDB Vector Search.

| AI frameworks | Tutorial                                                                                          |
|---------------|---------------------------------------------------------------------------------------------------|
| LangChain     | [Integrate Vector Search with LangChain](/ai/integrations/vector-search-integrate-with-langchain.md)   |
| LlamaIndex    | [Integrate Vector Search with LlamaIndex](/ai/integrations/vector-search-integrate-with-llamaindex.md) |

You can also use TiDB for various tasks such as document storage and knowledge graph storage for AI applications.

## Embedding models and services

TiDB Vector Search supports storing vectors of up to 16383 dimensions, which accommodates most embedding models.

You can use either self-deployed open-source embedding models or third-party embedding APIs to generate vectors.

The following table lists some mainstream embedding service providers and the corresponding integration tutorials.

| Embedding service providers | Tutorial                                                                                                            |
|-----------------------------|---------------------------------------------------------------------------------------------------------------------|
| Jina AI                     | [Integrate Vector Search with Jina AI Embeddings API](/ai/integrations/vector-search-integrate-with-jinaai-embedding.md) |

## Object Relational Mapping (ORM) libraries

You can integrate TiDB Vector Search with your ORM library to interact with the TiDB database.

The following table lists the supported ORM libraries and the corresponding integration tutorials:

<table>
  <tr>
    <th>Language</th>
    <th>ORM/Client</th>
    <th>How to install</th>
    <th>Tutorial</th>
  </tr>
  <tr>
    <td rowspan="4">Python</td>
    <td>TiDB Vector Client</td>
    <td><code>pip install tidb-vector[client]</code></td>
    <td><a href="/tidb/v8.5/vector-search-get-started-using-python">Get Started with Vector Search Using Python</a></td>
  </tr>
  <tr>
    <td>SQLAlchemy</td>
    <td><code>pip install tidb-vector</code></td>
    <td><a href="/tidb/v8.5/vector-search-integrate-with-sqlalchemy">Integrate TiDB Vector Search with SQLAlchemy</a></td>
  </tr>
  <tr>
    <td>peewee</td>
    <td><code>pip install tidb-vector</code></td>
    <td><a href="/tidb/v8.5/vector-search-integrate-with-peewee">Integrate TiDB Vector Search with peewee</a></td>
  </tr>
  <tr>
    <td>Django</td>
    <td><code>pip install django-tidb[vector]</code></td>
    <td><a href="/tidb/v8.5/vector-search-integrate-with-django-orm">Integrate TiDB Vector Search with Django</a></td>
  </tr>
</table>
