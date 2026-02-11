---
title: Auto Embedding
summary: アプリケーションで自動埋め込みを使用する方法を学習します。
---

# 自動埋め込み {#auto-embedding}

自動埋め込み機能は、テキスト データのベクター埋め込みを自動的に生成します。

> **注記：**
>
> 自動埋め込みの完全な例については、 [自動埋め込みの例](/ai/examples/auto-embedding-with-pytidb.md)参照してください。

## 基本的な使い方 {#basic-usage}

このドキュメントでは、 TiDB Cloudホストの埋め込みモデルをデモに使用しています。サポートされているプロバイダーの全リストについては、 [自動埋め込みの概要](/ai/integrations/vector-search-auto-embedding-overview.md#available-text-embedding-models)参照してください。

### ステップ1. 埋め込み関数を定義する {#step-1-define-an-embedding-function}

テキスト データのベクトル埋め込みを生成するための埋め込み関数を定義します。

```python
from pytidb.embeddings import EmbeddingFunction

embed_func = EmbeddingFunction(
    model_name="tidbcloud_free/amazon/titan-embed-text-v2",
)
```

### ステップ2. テーブルとベクトルフィールドを作成する {#step-2-create-a-table-and-a-vector-field}

テーブル スキーマにベクトル フィールドを作成するには、 `embed_func.VectorField()`使用します。

自動埋め込みを有効にするには、埋め込みたいフィールドに`source_field`設定します。

```python hl_lines="7"
from pytidb.schema import TableModel, Field
from pytidb.datatype import TEXT

class Chunk(TableModel):
    id: int = Field(primary_key=True)
    text: str = Field(sa_type=TEXT)
    text_vec: list[float] = embed_func.VectorField(source_field="text")

table = client.create_table(schema=Chunk, if_exists="overwrite")
```

埋め込みモデルによって自動的に決定されるため、 `dimensions`パラメータを指定する必要はありません。

ただし、 `dimensions`パラメータを設定してデフォルトのディメンションを上書きすることができます。

### ステップ3. サンプルデータを挿入する {#step-3-insert-some-sample-data}

テーブルにサンプルデータを挿入します。

```python
table.bulk_insert([
    Chunk(text="TiDB is a distributed database that supports OLTP, OLAP, HTAP and AI workloads."),
    Chunk(text="PyTiDB is a Python library for developers to connect to TiDB."),
    Chunk(text="LlamaIndex is a Python library for building AI-powered applications."),
])
```

データを挿入すると、 `text_vec`フィールドに`text`から生成された埋め込みが自動的に入力されます。

### ステップ4. ベクトル検索を実行する {#step-4-perform-a-vector-search}

クエリテキストを`search()`メソッドに直接渡すことができます。クエリテキストは自動的に埋め込まれ、ベクター検索に使用されます。

```python
table.search("HTAP database").limit(3).to_list()
```
