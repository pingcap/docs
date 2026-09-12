---
title: ARRAY_CONSTRUCT
summary: 使用指定的值创建 JSON 数组。
---

# ARRAY_CONSTRUCT

使用指定的值创建 JSON 数组。

## 别名 {#aliases}

- `JSON_ARRAY`

## 语法 {#syntax}

```sql
ARRAY_CONSTRUCT(value1[, value2[, ...]])
```

## 返回类型 {#return-type}

JSON 数组。

## 示例 {#examples}

### 示例 1：使用常量值或表达式创建 JSON 数组 {#example-1-creating-json-array-with-constant-values-or-expressions}

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

### 示例 2：根据表数据创建 JSON 数组 {#example-2-creating-json-array-from-table-data}

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