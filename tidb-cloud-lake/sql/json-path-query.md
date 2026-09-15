---
title: JSON_PATH_QUERY
summary: 获取指定 JSON 值中由 JSON 路径返回的所有 JSON 项。
---

# JSON_PATH_QUERY

获取指定 JSON 值中由 JSON 路径返回的所有 JSON 项。

## 语法 {#syntax}

```sql
JSON_PATH_QUERY(<variant>, '<path_name>')
```

## 返回类型 {#return-type}

VARIANT

## 示例 {#example}

**创建表并插入示例数据**

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

**查询演示：从产品详情中提取所有特性**

```sql
SELECT
    name,
    JSON_PATH_QUERY(details, '$.features.*') AS all_features
FROM
    products;
```

**结果**

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