---
title: Vector Search (Beta) Integrations
summary: Introduce how to integrate the TiDB Vector Search feature with programming languages and AI frameworks.
---

# Vector Search (Beta) Integrations

> **Note**
>
> The Vector Search feature is only available for TiDB Serverless at this moment.

## Programming Language Support

<table>
  <tr>
    <th>Language</th>
    <th>ORM/Client</th>
    <th>How to install</th>
    <th>Documentation</th>
  </tr>
  <tr>
    <td rowspan="4">Python</td>
    <td>TiDB Vector Client</td>
    <td><code>pip install tidb-vector[client]</code></td>
    <td><a href="https://github.com/pingcap/tidb-vector-python?tab=readme-ov-file#tidb-vector-client">Documentation</a></td>
  </tr>
  <tr>
    <td>SQLAlchemy</td>
    <td><code>pip install tidb-vector</code></td>
    <td><a href="https://github.com/pingcap/tidb-vector-python?tab=readme-ov-file#sqlalchemy">Documentation</a></td>
  </tr>
  <tr>
    <td>Peewee</td>
    <td><code>pip install tidb-vector</code></td>
    <td><a href="https://github.com/pingcap/tidb-vector-python?tab=readme-ov-file#peewee">Documentation</a></td>
  </tr>
  <tr>
    <td>Django</td>
    <td><code>pip install django-tidb[vector]</code></td>
    <td><a href="https://github.com/pingcap/django-tidb?tab=readme-ov-file#vector-beta">Documentation</a></td>
  </tr>
</table>

## AI Framework Support

### LangChain

TiDB has been integrated into LangChain as a vector store ([tutorial](https://python.langchain.com/v0.2/docs/integrations/vectorstores/tidb_vector/)) and a memory store ([tutorial](https://python.langchain.com/v0.2/docs/integrations/memory/tidb_chat_message_history/)).

You can directly try it on [colab](https://colab.research.google.com/github/langchain-ai/langchain/blob/master/docs/docs/integrations/vectorstores/tidb_vector.ipynb) without downloading.

### LlamaIndex

TiDB also supports LlamaIndex as a vector store index, see [tutorial](https://docs.llamaindex.ai/en/stable/examples/vector_stores/TiDBVector/) or have a try on [colab](https://colab.research.google.com/github/run-llama/llama_index/blob/main/docs/docs/examples/vector_stores/TiDBVector.ipynb).
