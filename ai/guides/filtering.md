---
title: Filtering
summary: アプリケーションでフィルタリングを使用する方法を学習します。
---

# フィルタリング {#filtering}

リレーショナル データベースである TiDB は、正確なクエリを実行するための[SQL演算子](https://docs.pingcap.com/tidbcloud/operators/)なフィルタリング条件と柔軟な組み合わせをサポートします。

## 概要 {#overview}

スカラーフィールドとJSONフィールドの両方でフィルタリングできます。JSONフィールドでのフィルタリングは、ベクター検索の[メタデータフィルタリング](/ai/guides/vector-search.md#metadata-filtering)でよく使用されます。

[`pytidb`](https://github.com/pingcap/pytidb)は、開発者が AI アプリケーションを効率的に構築できるように設計されています。

`pytidb`使用する場合、 `table.query()` 、 `table.delete()` 、 `table.update()` 、および`table.search()`メソッドに**filters**パラメータを渡すことでフィルタリングを適用できます。

**フィルター**パラメータは、 [辞書フィルター](#dictionary-filters)と[SQL文字列フィルター](#sql-string-filters) 2 つの形式をサポートします。

## 辞書フィルター {#dictionary-filters}

`pytidb`では、**フィルター**パラメータとして演算子を含む Python 辞書を使用して、フィルター条件を定義できます。

**フィルター**の辞書構造は次のとおりです。

```python
{
    "<key>": {
        "<operator>": <value>
    },
    ...
}
```

-   `<key>` : キーは、列名、JSON フィールドにアクセスするための JSON パス式 ( [メタデータフィルタリング](/ai/guides/vector-search.md#metadata-filtering)参照)、または[論理演算子](#logical-operators)になります。
-   `<operator>` : 演算子は[比較演算子](#compare-operators)または[包含演算子](#inclusion-operators)になります。
-   `<value>` : 値は演算子に応じてスカラー値または配列になります。

**例: `created_at`が 2024-01-01 より大きいレコードをフィルタリングする**

```python
table.query({
    # The `created_at` is a scalar field with DATETIME type
    "created_at": {
        "$gt": "2024-01-01"
    }
})
```

**例: `meta.category`が配列 [&quot;tech&quot;, &quot;science&quot;] に含まれるレコードをフィルタリングする**

```python
results = (
    table.search("some query", search_type="vector")
        .filter({
            # The `meta` is a JSON field, and its value is a JSON object like {"category": "tech"}
            "meta.category": {
                "$in": ["tech", "science"]
            }
        })
        .limit(10)
        .to_list()
)
```

### 比較演算子 {#compare-operators}

次の比較演算子を使用してレコードをフィルタリングできます。

| オペレーター | 説明      |
| ------ | ------- |
| `$eq`  | 等しい値    |
| `$ne`  | 値と等しくない |
| `$gt`  | 値より大きい  |
| `$gte` | 値以上     |
| `$lt`  | 値より小さい  |
| `$lte` | 値以下     |

**例: `user_id` 1に等しいレコードをフィルタリングする**

```python
{
    "user_id": {
        "$eq": 1
    }
}
```

`$eq`演算子は省略可能です。次のフィルタは前のフィルタと同等です。

```python
{
    "user_id": 1
}
```

### 包含演算子 {#inclusion-operators}

次の包含演算子を使用してレコードをフィルタリングできます。

| オペレーター | 説明                       |
| ------ | ------------------------ |
| `$in`  | 配列（文字列、整数、または浮動小数点数）     |
| `$nin` | 配列内にありません（文字列、整数、浮動小数点数） |

**例: `category`が配列 [&quot;tech&quot;, &quot;science&quot;] に含まれるレコードをフィルタリングする**

```python
{
    "category": {
        "$in": ["tech", "science"]
    }
}
```

### 論理演算子 {#logical-operators}

論理演算子`$and`と`$or`を使用して、複数のフィルターを組み合わせることができます。

| オペレーター | 説明                              |
| ------ | ------------------------------- |
| `$and` | リスト内の**すべての**フィルターに一致する結果を返します  |
| `$or`  | リスト内の**いずれかの**フィルターに一致する結果を返します |

**`$and`または`$or`の構文:**

```python
{
    "$and|$or": [
        {
            "field_name": {
                <operator>: <value>
            }
        },
        {
            "field_name": {
                <operator>: <value>
            }
        }
        ...
    ]
}
```

**例: `$and`を使用して複数のフィルターを組み合わせる:**

```python
{
    "$and": [
        {
            "created_at": {
                "$gt": "2024-01-01"
            }
        },
        {
            "meta.category": {
                "$in": ["tech", "science"]
            }
        }
    ]
}
```

## SQL文字列フィルター {#sql-string-filters}

SQL文字列を`filters`として使用することもできます。文字列は、 TiDB SQL構文の有効なSQL `WHERE`句（キーワード`WHERE`なし）である必要があります。

**例: `created_at`が 2024-01-01 より大きいレコードをフィルタリングする**

```python
results = table.query(
    filters="created_at > '2024-01-01'",
    limit=10
).to_list()
```

**例: JSONフィールド`meta.category`が「tech」に等しいレコードをフィルタリングする**

```python
results = table.query(
    filters="meta->>'$.category' = 'tech'",
    limit=10
).to_list()
```

`AND` 、 `OR` 、括弧を使用して複数の条件を組み合わせたり、TiDB でサポートされている[SQL演算子](https://docs.pingcap.com/tidbcloud/operators/)使用したりできます。

> **警告：**
>
> 動的なユーザー入力で SQL 文字列フィルターを使用する場合は、 [SQLインジェクション](https://en.wikipedia.org/wiki/SQL_injection)脆弱性を防ぐために常に入力を検証します。
