---
title: ARRAY_CONSTRUCT
summary: 指定した値で JSON 配列を作成します。
---

# ARRAY_CONSTRUCT

指定した値で JSON 配列を作成します。

## エイリアス {#aliases}

- `JSON_ARRAY`

## 構文 {#syntax}

```sql
ARRAY_CONSTRUCT(value1[, value2[, ...]])
```

## 戻り値の型 {#return-type}

JSON 配列。

## 例 {#examples}

### 例 1: 定数値または式を使用した JSON 配列の作成 {#example-1-creating-json-array-with-constant-values-or-expressions}

```sql
SELECT ARRAY_CONSTRUCT('Datalake', 3.14, NOW(), TRUE, NULL);

array_construct('datalake', 3.14, now(), true, null)         |
--------------------------------------------------------+
["Datalake",3.14,"2023-09-06 07:23:55.399070",true,null]|

SELECT ARRAY_CONSTRUCT('fruits', ARRAY_CONSTRUCT('apple', 'banana', 'orange'), OBJECT_CONSTRUCT('price', 1.2, 'quantity', 3));

array_construct('fruits', array_construct('apple', 'banana', 'orange'), object_construct('price', 1.2, 'quantity', 3))|
-------------------------------------------------------------------------------------------------------+
["fruits",["apple","banana","orange"],{"price":1.2,"quantity":3}]                                      |
```

### 例 2: テーブルデータから JSON 配列を作成 {#example-2-creating-json-array-from-table-data}

```sql
CREATE TABLE products (
    ProductName VARCHAR(255),
    Price DECIMAL(10, 2)
);

INSERT INTO products (ProductName, Price)
VALUES
    ('Apple', 1.2),
    ('Banana', 0.5),
    ('Orange', 0.8);

SELECT ARRAY_CONSTRUCT(ProductName, Price) FROM products;

array_construct(productname, price)|
------------------------------+
["Apple",1.2]                 |
["Banana",0.5]                |
["Orange",0.8]                |
```