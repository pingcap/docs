---
title: JSON_PATH_QUERY_FIRST
summary: 指定した JSON 値に対して、JSON path が返す最初の JSON 項目を取得します。
---

# JSON_PATH_QUERY_FIRST

指定した JSON 値に対して、JSON path が返す最初の JSON 項目を取得します。

## 構文 {#syntax}

```sql
JSON_PATH_QUERY_FIRST(<variant>, '<path_name>')
```

## 戻り値の型 {#return-type}

VARIANT

## 例 {#example}

**Create a Table and Insert Sample Data**

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

**製品詳細から最初の feature を抽出するクエリのデモ**

```sql
SELECT
    name,
    JSON_PATH_QUERY(details, '$.features.*') AS all_features,
    JSON_PATH_QUERY_FIRST(details, '$.features.*') AS first_feature
FROM
    products;
```

**結果**

```sql
+------------+--------------+---------------+
| name       | all_features | first_feature |
+------------+--------------+---------------+
| Laptop     | "16GB"       | "16GB"        |
| Laptop     | "512GB"      | "16GB"        |
| Smartphone | "4GB"        | "4GB"         |
| Smartphone | "128GB"      | "4GB"         |
| Headphones | "20h"        | "20h"         |
| Headphones | "5.0"        | "20h"         |
+------------+--------------+---------------+
```