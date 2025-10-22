---
title: 向量检索集成概览
summary: TiDB 向量检索集成的概览，包括支持的 AI 框架、嵌入模型和 ORM 库。
---

# 向量检索集成概览

本文档提供了 TiDB 向量检索集成的概览，包括支持的 AI 框架、嵌入模型和对象关系映射（ORM）库。

<CustomContent platform="tidb">

> **Warning:**
>
> 向量检索功能为实验性功能。不建议在生产环境中使用。该功能可能会在没有提前通知的情况下发生变更。如果你发现了 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 向量检索功能处于 beta 阶段，可能会在没有提前通知的情况下发生变更。如果你发现了 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。

</CustomContent>

> **Note:**
>
> 向量检索功能适用于 TiDB 自建版、[TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)、[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)。对于 TiDB 自建版和 TiDB Cloud Dedicated，TiDB 版本需为 v8.4.0 及以上（推荐 v8.5.0 及以上）。

## AI 框架

TiDB 官方支持以下 AI 框架，帮助你轻松将基于这些框架开发的 AI 应用与 TiDB 向量检索集成。

| AI 框架      | 教程                                                                                                 |
|--------------|------------------------------------------------------------------------------------------------------|
| Langchain    | [Integrate Vector Search with LangChain](/vector-search/vector-search-integrate-with-langchain.md)   |
| LlamaIndex   | [Integrate Vector Search with LlamaIndex](/vector-search/vector-search-integrate-with-llamaindex.md) |

此外，你还可以将 TiDB 用于多种用途，例如作为 AI 应用的文档存储和知识图谱存储。

## 嵌入模型与服务

TiDB 向量检索支持存储最多 16383 维的向量，能够满足大多数嵌入模型的需求。

你可以选择自部署开源嵌入模型，或使用第三方嵌入服务商提供的嵌入 API 来生成向量。

下表列出了一些主流的嵌入服务商及其对应的集成教程。

| 嵌入服务商   | 教程                                                                                                              |
|--------------|-------------------------------------------------------------------------------------------------------------------|
| Jina AI      | [Integrate Vector Search with Jina AI Embeddings API](/vector-search/vector-search-integrate-with-jinaai-embedding.md) |

## 对象关系映射（ORM）库

你可以将 TiDB 向量检索与 ORM 库集成，以便与 TiDB 数据库进行交互。

下表列出了支持的 ORM 库及其对应的集成教程：

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