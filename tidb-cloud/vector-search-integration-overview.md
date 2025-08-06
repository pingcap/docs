---
title: Vector Search Integration Overview
summary: An overview of TiDB Vector Search integration, including supported AI frameworks, embedding models, and ORM libraries.
---

# Vector Search Integration Overview

This document provides an overview of TiDB Vector Search integration, including supported AI frameworks, embedding models, and Object Relational Mapping (ORM) libraries.

> **Note**
>
<<<<<<< HEAD:tidb-cloud/vector-search-integration-overview.md
> TiDB Vector Search is only available for TiDB Self-Managed (TiDB >= v8.4) and [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless). It is not available for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated).
=======
> The vector search feature is experimental. It is not recommended that you use it in the production environment. This feature might be changed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> The vector search feature is in beta. It might be changed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

</CustomContent>

> **Note:**
>
> The vector search feature is available on TiDB Self-Managed, [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless), [{{{ .essential }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential), and [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated). For TiDB Self-Managed and TiDB Cloud Dedicated, the TiDB version must be v8.4.0 or later (v8.5.0 or later is recommended).
>>>>>>> d7c28f7510 (*: clarify feature unavailability on Starter and Essential clusters (#21509)):vector-search/vector-search-integration-overview.md

## AI frameworks

TiDB provides official support for the following AI frameworks, enabling you to easily integrate AI applications developed based on these frameworks with TiDB Vector Search.

| AI frameworks | Tutorial                                                                                          |
| ------------- | ------------------------------------------------------------------------------------------------- |
| Langchain     | [Integrate Vector Search with LangChain](/tidb-cloud/vector-search-integrate-with-langchain.md)   |
| LlamaIndex    | [Integrate Vector Search with LlamaIndex](/tidb-cloud/vector-search-integrate-with-llamaindex.md) |

Moreover, you can also use TiDB for various purposes, such as document storage and knowledge graph storage for AI applications.

## Embedding models and services

TiDB Vector Search supports storing vectors of up to 16383 dimensions, which accommodates most embedding models.

You can either use self-deployed open-source embedding models or third-party embedding APIs provided by third-party embedding providers to generate vectors.

The following table lists some mainstream embedding service providers and the corresponding integration tutorials.

| Embedding service providers | Tutorial                                                                                                            |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Jina AI                     | [Integrate Vector Search with Jina AI Embeddings API](/tidb-cloud/vector-search-integrate-with-jinaai-embedding.md) |

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
    <td><a href="/tidbcloud/vector-search-get-started-using-python">Get Started with Vector Search Using Python</a></td>
  </tr>
  <tr>
    <td>SQLAlchemy</td>
    <td><code>pip install tidb-vector</code></td>
    <td><a href="/tidbcloud/vector-search-integrate-with-sqlalchemy">Integrate TiDB Vector Search with SQLAlchemy</a></td>
  </tr>
  <tr>
    <td>peewee</td>
    <td><code>pip install tidb-vector</code></td>
    <td><a href="/tidbcloud/vector-search-integrate-with-peewee">Integrate TiDB Vector Search with peewee</a></td>
  </tr>
  <tr>
    <td>Django</td>
    <td><code>pip install django-tidb[vector]</code></td>
    <td><a href="/tidbcloud/vector-search-integrate-with-django-orm">Integrate TiDB Vector Search with Django</a></td>
  </tr>
</table>
