---
title: Working with Tables
summary: TiDB でテーブルを操作する方法を学びます。
---

# 表の操作 {#working-with-tables}

TiDBは、関連するデータのコレクションを整理して保存するためにテーブルを使用します。柔軟なスキーマ定義機能を備えているため、特定の要件に合わせてテーブルを設計できます。

テーブルには、異なるデータ型の複数の列を含めることができます。サポートされているデータ型には、テキスト、数値、ベクター、バイナリデータ（ `BLOB` ）、JSONなどがあります。

このドキュメントでは、 [`pytidb`](https://github.com/pingcap/pytidb)を使用してテーブルを操作する方法を説明します。

`pytidb`は、開発者が AI アプリケーションを効率的に構築できるように設計されています。

> **注記：**
>
> 完全な動作例については、リポジトリの[基本的な例](https://github.com/pingcap/pytidb/tree/main/examples/basic)参照してください。

## テーブルを作成する {#create-a-table}

### TableModelの使用 {#using-tablemodel}

`pytidb` 、テーブルのスキーマを表す`TableModel`クラスを提供します。このクラスは[ピダンティックモデル](https://docs.pydantic.dev/latest/concepts/models/)と互換性があり、宣言的にテーブルを定義できます。

次の例では、次の列を持つ`items`という名前のテーブルを作成します。

-   `id` : 整数型の主キー列
-   `content` : テキスト型の列
-   `embedding` : 3次元のベクトル型列
-   `meta` : JSON型の列

<SimpleTab groupId="language">
<div label="Python" value="python">

[データベースに接続する](/ai/guides/connect.md)を使用して`pytidb`インスタンスを取得したら、 `client`メソッドを`create_table`してテーブルを作成できます。

```python hl_lines="12"
from pytidb.schema import TableModel, Field, VectorField
from pytidb.datatype import TEXT, JSON

class Item(TableModel):
    __tablename__ = "items"

    id: int = Field(primary_key=True)
    content: str = Field(sa_type=TEXT)
    embedding: list[float] = VectorField(dimensions=3)
    meta: dict = Field(sa_type=JSON, default_factory=dict)

table = client.create_table(schema=Item, if_exists="overwrite")
```

`create_table`メソッドは次のパラメータを受け入れます。

-   `schema` : テーブル構造を定義する`TableModel`のクラス。
-   `if_exists` : テーブル作成モード。
    -   `raise` (デフォルト): テーブルが存在しない場合は作成し、既に存在する場合はエラーを発生させます。
    -   `skip` : テーブルが存在しない場合は作成し、既に存在する場合は何も行いません。
    -   `overwrite` : 既存のテーブルを削除し、新しいテーブルを作成します。これは**テストや開発**には便利ですが、本番環境では推奨されません。

テーブルが作成されると、 `table`オブジェクトを使用してデータの挿入、更新、削除、クエリを実行できます。

</div>
<div label="SQL" value="sql">

`CREATE TABLE`ステートメントを使用してテーブルを作成します。

```sql
CREATE TABLE items (
    id INT PRIMARY KEY,
    content TEXT,
    embedding VECTOR(3),
    meta JSON
);
```

</div>
</SimpleTab>

## テーブルにデータを追加する {#add-data-to-a-table}

### TableModelを使用 {#with-tablemodel}

`TableModel`インスタンスを使用して行を表し、それをテーブルに挿入できます。

単一のレコードを挿入するには:

<SimpleTab groupId="language">
<div label="Python" value="python">

`table.insert()`メソッドを使用して、テーブルに 1 つのレコードを挿入します。

```python
table.insert(
    Item(
        id=1,
        content="TiDB is a distributed SQL database",
        embedding=[0.1, 0.2, 0.3],
        meta={"category": "database"},
    )
)
```

</div>
<div label="SQL" value="sql">

`INSERT INTO`ステートメントを使用して、テーブルに 1 つのレコードを挿入します。

```sql
INSERT INTO items(id, content, embedding, meta)
VALUES (1, 'TiDB is a distributed SQL database', '[0.1, 0.2, 0.3]', '{"category": "database"}');
```

</div>
</SimpleTab>

複数のレコードを挿入するには:

<SimpleTab groupId="language">
<div label="Python" value="python">

`table.bulk_insert()`メソッドを使用して、テーブルに複数のレコードを挿入します。

```python
table.bulk_insert([
    Item(
        id=2,
        content="GPT-4 is a large language model",
        embedding=[0.4, 0.5, 0.6],
        meta={"category": "llm"},
    ),
    Item(
        id=3,
        content="LlamaIndex is a Python library for building AI-powered applications",
        embedding=[0.7, 0.8, 0.9],
        meta={"category": "rag"},
    ),
])
```

</div>
<div label="SQL" value="sql">

`INSERT INTO`ステートメントを使用して、複数のレコードをテーブルに挿入します。

```sql
INSERT INTO items(id, content, embedding, meta)
VALUES
    (2, 'GPT-4 is a large language model', '[0.4, 0.5, 0.6]', '{"category": "llm"}'),
    (3, 'LlamaIndex is a Python library for building AI-powered applications', '[0.7, 0.8, 0.9]', '{"category": "rag"}');
```

</div>
</SimpleTab>

### ディクト付き {#with-dict}

`dict`使って行を表し、それをテーブルに挿入することもできます。この方法はより柔軟で、データを挿入するために`TableModel`使用する必要がありません。

単一のレコードを挿入するには:

<SimpleTab groupId="language">
<div label="Python" value="python">

辞書と共に`table.insert()`メソッドを使用して、テーブルに 1 つのレコードを挿入します。

```python
table.insert({
    "id": 1,
    "content": "TiDB is a distributed SQL database",
    "embedding": [0.1, 0.2, 0.3],
    "meta": {"category": "database"},
})
```

</div>
<div label="SQL" value="sql">

`INSERT INTO`ステートメントを使用して、テーブルに 1 つのレコードを挿入します。

```sql
INSERT INTO items(id, content, embedding, meta)
VALUES (1, 'TiDB is a distributed SQL database', '[0.1, 0.2, 0.3]', '{"category": "database"}');
```

</div>
</SimpleTab>

## データをテーブルに保存する {#save-data-to-a-table}

`save`メソッドは、単一の行を挿入または更新する便利な方法を提供します。行の場合、主キーがテーブルに存在しない場合、このメソッドは新しい行としてテーブルに挿入します。レコードが既に存在する場合、このメソッドは行全体を上書きします。

> **注記：**
>
> テーブル内にレコードIDが既に存在する場合、 `table.save()`​​レコード全体を上書きします。レコードの一部のみを変更するには、 `table.update()`使用します。

<SimpleTab groupId="language">
<div label="Python" value="python">

`table.save()`メソッドを使用して、単一のレコードをテーブルに保存します。

**例: 新しいレコードを保存する**

```python
saved_record = table.save(
    Item(
        id=4,
        content="Vector databases enable AI applications",
        embedding=[1.0, 1.1, 1.2],
        meta={"category": "vector-db"},
    )
)
```

**例: 既存のレコードを保存する (レコード全体を上書きする)**

```python
# This overwrites the entire record with id=1
updated_record = table.save(
    Item(
        id=1,  # Existing ID
        content="Updated content for TiDB",
        embedding=[0.2, 0.3, 0.4],
        meta={"category": "updated"},
    )
)
```

</div>
<div label="SQL" value="sql">

レコードを保存するには、 `INSERT ... ON DUPLICATE KEY UPDATE`ステートメントを使用します。

**例: 新しいレコードを保存するか、存在する場合は更新する**

```sql
INSERT INTO items(id, content, embedding, meta)
VALUES (4, 'Vector databases enable AI applications', '[1.0, 1.1, 1.2]', '{"category": "vector-db"}')
ON DUPLICATE KEY UPDATE
    content = VALUES(content),
    embedding = VALUES(embedding),
    meta = VALUES(meta);
```

</div>
</SimpleTab>

## テーブルからデータをクエリする {#query-data-from-a-table}

テーブルからレコードを取得するには:

<SimpleTab groupId="language">
<div label="Python" value="python">

テーブルからレコードを取得するには、 `table.query()`メソッドを使用します。

**例: 最初の10件のレコードを取得する**

```python
result = table.query(limit=10).to_list()
```

</div>
<div label="SQL" value="sql">

`SELECT`ステートメントを使用して、テーブルからレコードを取得します。

**例: 最初の10件のレコードを取得する**

```sql
SELECT * FROM items LIMIT 10;
```

</div>
</SimpleTab>

クエリ条件に基づいてレコードを取得するには:

<SimpleTab groupId="language">
<div label="Python" value="python">

`filters`パラメータを`table.query()`メソッドに渡します。

```python
result = table.query(
    filters={"meta.category": "database"},
    limit=10
).to_list()
```

</div>
<div label="SQL" value="sql">

レコードをフィルタリングするには、 `WHERE`句を使用します。

**例: カテゴリ「データベース」のレコードを10件取得する**

```sql
SELECT * FROM items WHERE meta->>'$.category' = 'database' LIMIT 10;
```

</div>
</SimpleTab>

サポートされているフィルター操作と例の完全なリストについては、ガイド[フィルタリング](/ai/guides/filtering.md)を参照してください。

## テーブル内のデータを更新する {#update-data-in-a-table}

<SimpleTab groupId="language">
<div label="Python" value="python">

`table.update()`メソッドを使用して、レコードを[フィルター](/ai/guides/filtering.md)で更新します。

**例: `id`が1のレコードを更新する**

```python
table.update(
    values={
        "content": "TiDB Cloud Starter is a fully managed, auto-scaling cloud database service",
        "embedding": [0.1, 0.2, 0.4],
        "meta": {"category": "dbaas"},
    },
    filters={
        "id": 1
    },
)
```

</div>
<div label="SQL" value="sql">

`UPDATE`ステートメントを使用して、レコードを[フィルター](/ai/guides/filtering.md)で更新します。

**例: `id`が1のレコードを更新する**

```sql
UPDATE items
SET
    content = 'TiDB Cloud Starter is a fully managed, auto-scaling cloud database service',
    embedding = '[0.1, 0.2, 0.4]',
    meta = '{"category": "dbaas"}'
WHERE
    id = 1;
```

</div>
</SimpleTab>

## テーブルから削除する {#delete-from-a-table}

<SimpleTab groupId="language">
<div label="Python" value="python">

[フィルター](/ai/guides/filtering.md)のレコードを削除するには、 `table.delete()`メソッドを使用します。

**例: `id` 2のレコードを削除する**

```python
table.delete(
    filters={
        "id": 2
    }
)
```

</div>
<div label="SQL" value="sql">

`DELETE`ステートメントを使用して、 [フィルター](/ai/guides/filtering.md)のレコードを削除します。

**例: `id` 2のレコードを削除する**

```sql
DELETE FROM items WHERE id = 2;
```

</div>
</SimpleTab>

## テーブルを切り捨てる {#truncate-a-table}

<SimpleTab groupId="language">
<div label="Python" value="python">

テーブルからすべてのデータを削除しながらテーブル構造を維持するには、 `table.truncate()`メソッドを使用します。

```python
table.truncate()
```

テーブルが切り捨てられていることを確認するには、テーブルに 0 行が含まれていることを確認します。

```python
table.rows()
```

</div>
<div label="SQL" value="sql">

テーブルからすべてのデータを削除しながらテーブル構造を維持するには、 `TRUNCATE TABLE`ステートメントを使用します。

```sql
TRUNCATE TABLE items;
```

テーブルが切り捨てられていることを確認するには、テーブルに 0 行が含まれていることを確認します。

```sql
SELECT COUNT(*) FROM items;
```

</div>
</SimpleTab>

## テーブルを削除する {#drop-a-table}

<SimpleTab groupId="language">
<div label="Python" value="python">

データベースからテーブルを完全に削除するには、 `client.drop_table()`メソッドを使用します。

```python
client.drop_table("items")
```

テーブルがデータベースから削除されたことを確認するには:

```python
client.table_names()
```

</div>
<div label="SQL" value="sql">

データベースからテーブルを完全に削除するには、 `DROP TABLE`ステートメントを使用します。

```sql
DROP TABLE items;
```

テーブルがデータベースから削除されたことを確認するには:

```sql
SHOW TABLES;
```

</div>
</SimpleTab>
