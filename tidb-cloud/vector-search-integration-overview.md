---
title: Vector Search Integration Overview
summary: 
---

# Vector Search Integration Overview

This document is an overview of TiDB vector search integration, including AI frameworks, embedded models, Object Relational Mapping (ORM) libraries, etc.

> **Note**
>
> The vector search feature is currently in beta and only available for [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters.

## AI Frameworks

TiDB provides official support for the following AI frameworks, making it easier to integrate AI applications developed based on these frameworks with TiDB Vector Search. 

Moreover, you can also use TiDB for various purposes such as document storage and knowledge graph storage for AI applications.

| AI Frameworks | Documentation                                                                                     |
|---------------|---------------------------------------------------------------------------------------------------|
| Langchain     | [Integrate Vector Search with LangChain](/tidb-cloud/vector-search-integrate-with-langchain.md)   |
| LlamaIndex    | [Integrate Vector Search with LlamaIndex](/tidb-cloud/vector-search-integrate-with-llamaindex.md) |

## Embedding Models / Services

The TiDB vector search feature supports storing vectors of up to 16,000 dimensions, which covers most embedding models.

You can use self-deployed open-source embedding models, or you can use the embeddings API provided by third-party Embedding providers to generate vectors.

The following lists some mainstream embedding service providers and how to integrate their Embedding API.

| AI Frameworks | Tutorial                                                                                                           |
|---------------|--------------------------------------------------------------------------------------------------------------------|
| JinaAI        | [Integrate Vector Search with JinaAI Embeddings API](/tidb-cloud/vector-search-integrate-with-jinaai-embedding.md) |


## Object Relational Mapping (ORM) Libraries

TiDB Vector Search feature can be integrated with ORM libraries to interact with the TiDB database.

The following table lists the supported ORM libraries:

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
    <td><a href="/tidb-cloud/vector-search-get-started-using-python-client.md">Get Started with Vector Search Using the Python Client</a></td>
  </tr>
  <tr>
    <td>SQLAlchemy</td>
    <td><code>pip install tidb-vector</code></td>
    <td><a href="/tidb-cloud/vector-search-integrate-with-sqlalchemy.md">Integrate TiDB Vector Search with SQLAlchemy</a></td>
  </tr>
  <tr>
    <td>Peewee</td>
    <td><code>pip install tidb-vector</code></td>
    <td><a href="/tidb-cloud/vector-search-integrate-with-peewee.md">Integrate TiDB Vector Search with Peewee</a></td>
  </tr>
  <tr>
    <td>Django</td>
    <td><code>pip install django-tidb[vector]</code></td>
    <td><a href="/tidb-cloud/vector-search-integrate-with-django-orm.md">Integrate TiDB Vector Search with Django</a></td>
  </tr>
</table>
