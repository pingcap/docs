---
title: JSON_PATH_QUERY
summary: 指定した JSON 値に対して、JSON path によって返されるすべての JSON 項目を取得します。
---

# JSON_PATH_QUERY

指定した JSON 値に対して、JSON path によって返されるすべての JSON 項目を取得します。

## 構文 {#syntax}

```sql
JSON_PATH_QUERY(<variant>, '<path_name>')
```

## 戻り値の型 {#return-type}

VARIANT

## 例 {#example}

**テーブルを作成してサンプルデータを挿入する**

```sql
CREATE TABLE products (
    name VARCHAR,
    details VARIANT
);

INSERT INTO products (name, details)
VALUES ('Laptop', '{"brand": "Dell", "colors": ["Black", "Silver"], "price": 1200, "features": {"ram": "16GB", "storage": "512GB"}}'),
       ('Smartphone', '{"brand": "Apple", "colors": ["White", "Black"], "price": 999, "features": {"ram": "4GB", "storage": "128GB"}}'),
       ('Headphones', '{"brand": "Sony", "colors": ["Black", "Blue", "Red"], "price": 150, "features": {"battery": "20h", "bluetooth": "5.0"}}');
```

**クエリのデモ: 製品詳細からすべての機能を抽出する**

```sql
SELECT
    name,
    JSON_PATH_QUERY(details, '$.features.*') AS all_features
FROM
    products;
```

**結果**

```sql
+------------+--------------+
| name       | all_features |
+------------+--------------+
| Laptop     | "16GB"       |
| Laptop     | "512GB"      |
| Smartphone | "4GB"        |
| Smartphone | "128GB"      |
| Headphones | "20h"        |
| Headphones | "5.0"        |
+------------+--------------+
```