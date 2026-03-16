---
title: ARRAY_CONSTRUCT
title_includes: JSON_ARRAY
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>

Creates a JSON array with specified values.

## Aliases

- `JSON_ARRAY`

## Syntax

```sql
ARRAY_CONSTRUCT(value1[, value2[, ...]])
```

## Return Type

JSON array.

## Examples

### Example 1: Creating JSON Array with Constant Values or Expressions

```sql
SELECT ARRAY_CONSTRUCT('Databend', 3.14, NOW(), TRUE, NULL);

array_construct('databend', 3.14, now(), true, null)         |
--------------------------------------------------------+
["Databend",3.14,"2023-09-06 07:23:55.399070",true,null]|

SELECT ARRAY_CONSTRUCT('fruits', ARRAY_CONSTRUCT('apple', 'banana', 'orange'), OBJECT_CONSTRUCT('price', 1.2, 'quantity', 3));

array_construct('fruits', array_construct('apple', 'banana', 'orange'), object_construct('price', 1.2, 'quantity', 3))|
-------------------------------------------------------------------------------------------------------+
["fruits",["apple","banana","orange"],{"price":1.2,"quantity":3}]                                      |
```

### Example 2: Creating JSON Array from Table Data

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
