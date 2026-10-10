---
title: JSON_PATH_QUERY_ARRAY
summary: 指定した JSON 値に対して JSON パスが返すすべての JSON 項目を取得し、結果を配列にラップします。
---

# JSON_PATH_QUERY_ARRAY

指定した JSON 値に対して JSON パスが返すすべての JSON 項目を取得し、結果を配列にラップします。

## 構文 {#syntax}

```sql
JSON_PATH_QUERY_ARRAY(<variant>, '<path_name>')
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

**クエリのデモ: 製品詳細からすべての features を配列として抽出する**

```sql
SELECT
    name,
    JSON_PATH_QUERY_ARRAY(details, '$.features.*') AS all_features
FROM
    products;
```

**結果**

```
   name    |         all_features
-----------+-----------------------
 Laptop    | ["16GB", "512GB"]
 Smartphone | ["4GB", "128GB"]
 Headphones | ["20h", "5.0"]
```