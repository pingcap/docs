---
title: Raw Queries
summary: アプリケーションで生のクエリを使用する方法を学習します。
---

# 生のクエリ {#raw-queries}

このガイドでは、アプリケーションで生の SQL クエリを実行する方法について説明します。

## 生のSQLでデータを操作する {#operate-data-with-raw-sql}

`client.execute()`メソッドを使用して、 `INSERT` 、 `UPDATE` 、 `DELETE` 、およびその他のデータ操作ステートメントを実行します。

```python
client.execute("INSERT INTO chunks(text, user_id) VALUES ('sample text', 5)")
```

### SQLインジェクション防止 {#sql-injection-prevention}

`execute()`と`query()`両方の方法は、**パラメータ化された SQL**機能をサポートしており、動的 SQL ステートメントの構築時に[SQLインジェクション](https://en.wikipedia.org/wiki/SQL_injection)回避するのに役立ちます。

```python
client.execute(
    "INSERT INTO chunks(text, user_id) VALUES (:text, :user_id)",
    {
        "text": "sample text",
        "user_id": 6,
    },
)
```

## 生のSQLでデータをクエリする {#query-data-with-raw-sql}

`client.query()`メソッドを使用して、 `SELECT` 、 `SHOW` 、およびその他のクエリ ステートメントを実行します。

### クエリ結果を出力する {#output-query-result}

`client.query()`メソッドは、いくつかのヘルパー メソッドを含む`SQLQueryResult`インスタンスを返します。

-   `to_pydantic()`
-   `to_list()`
-   `to_pandas()`
-   `to_rows()`
-   `scalar()`

#### ピダンティックモデルとして {#as-pydantic-model}

`to_pydantic()`メソッドは、Pydantic モデルのリストを返します。

```python
client.query("SELECT id, text, user_id FROM chunks").to_pydantic()
```

#### SQLAlchemyの結果行として {#as-sqlalchemy-result-rows}

`to_rows()`メソッドはタプルのリストを返します。各タプルは 1 行を表します。

```python
client.query("SHOW TABLES;").to_rows()
```

#### 辞書のリストとして {#as-a-list-of-dictionaries}

`to_list()`メソッドは、クエリ結果を辞書のリストに変換します。

```python
client.query(
    "SELECT id, text, user_id FROM chunks WHERE user_id = :user_id",
    {
        "user_id": 3
    }
).to_list()
```

#### pandasデータフレームとして {#as-pandas-dataframe}

`to_pandas()`メソッドはクエリ結果を`pandas.DataFrame`に変換し、ノートブック内で人間にわかりやすい形式で表示します。

```python
client.query("SELECT id, text, user_id FROM chunks").to_pandas()
```

#### スカラー値として {#as-scalar-value}

`scalar()`メソッドは、結果セットの最初の行の最初の列を返します。

```python
client.query("SELECT COUNT(*) FROM chunks;").scalar()
```
