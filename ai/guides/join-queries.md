---
title: Multiple Table Joins
summary: アプリケーションで複数のテーブル結合を使用する方法を学習します。
---

# 複数のテーブルのテーブル結合 {#multiple-table-joins}

リレーショナルデータベースであるTiDBでは、異なる構造（例： `chunks` ）を持つテーブルに多様なデータを単一のデータベースに格納できます。また、結合を使用して複数のテーブルのデータを結合し、複雑なクエリを実行すること`documents` `users` `chats` 。

## 基本的な使い方 {#basic-usage}

### ステップ1. テーブルを作成し、サンプルデータを挿入する {#step-1-create-tables-and-insert-sample-data}

<SimpleTab groupId="language">
<div label="Python" value="python">

すでに[TiDBに接続](/ai/guides/connect.md)使用して`TiDBClient`あると仮定します。

`documents`テーブルを作成し、いくつかのサンプル データを挿入します。

```python
from pytidb import Session
from pytidb.schema import TableModel, Field
from pytidb.sql import select

class Document(TableModel):
    __tablename__ = "documents"
    id: int = Field(primary_key=True)
    title: str = Field(max_length=255)

client.create_table(schema=Document, if_exists="overwrite")
client.table("documents").truncate()
client.table("documents").bulk_insert([
    Document(id=1, title="The Power of Positive Thinking"),
    Document(id=2, title="The Happiness Advantage"),
    Document(id=3, title="The Art of Happiness"),
])
```

`chunks`テーブルを作成し、いくつかのサンプル データを挿入します。

```python
class Chunk(TableModel):
    __tablename__ = "chunks"
    id: int = Field(primary_key=True)
    text: str = Field(max_length=255)
    document_id: int = Field(foreign_key="documents.id")

client.create_table(schema=Chunk, if_exists="overwrite")
client.table("chunks").truncate()
client.table("chunks").bulk_insert([
    Chunk(id=1, text="Positive thinking can change your life", document_id=1),
    Chunk(id=2, text="Happiness leads to success", document_id=2),
    Chunk(id=3, text="Finding joy in everyday moments", document_id=3),
])
```

</div>
<div label="SQL" value="sql">

`documents`テーブルを作成し、いくつかのサンプル データを挿入します。

```sql
CREATE TABLE documents (
    id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL
);

INSERT INTO documents (id, title) VALUES
    (1, 'The Power of Positive Thinking'),
    (2, 'The Happiness Advantage'),
    (3, 'The Art of Happiness');
```

`chunks`テーブルを作成し、いくつかのサンプル データを挿入します。

```sql
CREATE TABLE chunks (
    id INT PRIMARY KEY,
    text VARCHAR(255) NOT NULL,
    document_id INT NOT NULL,
    FOREIGN KEY (document_id) REFERENCES documents(id)
);

INSERT INTO chunks (id, text, document_id) VALUES
    (1, 'Positive thinking can change your life', 1),
    (2, 'Happiness leads to success', 2),
    (3, 'Finding joy in everyday moments', 3);
```

</div>
</SimpleTab>

### ステップ2. 結合クエリを実行する {#step-2-perform-a-join-query}

<SimpleTab groupId="language">
<div label="Python" value="python">

```python
with Session(client.db_engine) as db_session:
    query = (
        select(Chunk)
        .join(Document, Chunk.document_id == Document.id)
        .where(Document.title == "The Power of Positive Thinking")
    )
    chunks = db_session.exec(query).all()

[(c.id, c.text, c.document_id) for c in chunks]
```

</div>
<div label="SQL" value="sql">

結合クエリを実行して、テーブル`chunks`とテーブル`documents`のデータを結合します。

```sql
SELECT c.id, c.text, c.document_id
FROM chunks c
JOIN documents d ON c.document_id = d.id
WHERE d.title = 'The Power of Positive Thinking';
```

</div>
</SimpleTab>
