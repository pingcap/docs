---
title: Vector Search Integration Overview
summary: 关于 TiDB 向量搜索集成的概述，包括支持的 AI 框架、嵌入模型和 ORM 库。
---

# Vector Search Integration Overview

本文档提供了 TiDB 向量搜索集成的概述，包括支持的 AI 框架、嵌入模型和对象关系映射（ORM）库。

<CustomContent platform="tidb">

> **Warning:**
>
> The vector search feature is experimental. It is not recommended that you use it in the production environment. This feature might be changed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> The vector search feature is in beta. It might be changed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

</CustomContent>

> **Note:**
>
> The vector search feature is available on TiDB Self-Managed, [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless), and [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated). For TiDB Self-Managed and TiDB Cloud Dedicated, the TiDB 版本必须是 v8.4.0 或更高（建议 v8.5.0 或更高）。

## AI 框架

TiDB 提供对以下 AI 框架的官方支持，方便你将基于这些框架开发的 AI 应用与 TiDB 向量搜索进行集成。

| AI 框架 | 教程 |
|---------|---------------------------------------------------------------------------------------------------|
| Langchain | [将向量搜索与 LangChain 集成](/vector-search/vector-search-integrate-with-langchain.md) |
| LlamaIndex | [将向量搜索与 LlamaIndex 集成](/vector-search/vector-search-integrate-with-llamaindex.md) |

此外，你还可以使用 TiDB 进行多种用途，例如文档存储和知识图谱存储，以支持 AI 应用。

## 嵌入模型和服务

TiDB 向量搜索支持存储最多 16383 维的向量，满足大部分嵌入模型的需求。

你可以使用自行部署的开源嵌入模型，或第三方嵌入提供商提供的 API 来生成向量。

下表列出一些主流的嵌入服务提供商及对应的集成教程。

| 嵌入服务提供商 | 教程 |
|----------------|--------------------------------------------------------------------------------------------------------------|
| Jina AI | [将向量搜索与 Jina AI Embeddings API 集成](/vector-search/vector-search-integrate-with-jinaai-embedding.md) |

## 对象关系映射（ORM）库

你可以将 TiDB 向量搜索与 ORM 库集成，以便与 TiDB 数据库交互。

下表列出支持的 ORM 库及对应的集成教程：

<table>
  <tr>
    <th>语言</th>
    <th>ORM/客户端</th>
    <th>安装方式</th>
    <th>教程</th>
  </tr>
  <tr>
    <td rowspan="4">Python</td>
    <td>TiDB Vector Client</td>
    <td><code>pip install tidb-vector[client]</code></td>
    <td><a href="/tidb/v8.5/vector-search-get-started-using-python">使用 Python 开始向量搜索</a></td>
  </tr>
  <tr>
    <td>SQLAlchemy</td>
    <td><code>pip install tidb-vector</code></td>
    <td><a href="/tidb/v8.5/vector-search-integrate-with-sqlalchemy">将 TiDB 向量搜索与 SQLAlchemy 集成</a></td>
  </tr>
  <tr>
    <td>peewee</td>
    <td><code>pip install tidb-vector</code></td>
    <td><a href="/tidb/v8.5/vector-search-integrate-with-peewee">将 TiDB 向量搜索与 peewee 集成</a></td>
  </tr>
  <tr>
    <td>Django</td>
    <td><code>pip install django-tidb[vector]</code></td>
    <td><a href="/tidb/v8.5/vector-search-integrate-with-django-orm">将 TiDB 向量搜索与 Django 集成</a></td>
  </tr>
</table>