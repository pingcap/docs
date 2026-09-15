---
title: TO_NULLABLE
summary: 将一个值转换为其可空等价形式。
---

# TO_NULLABLE

将一个值转换为其可空等价形式。

当你将此函数应用于一个值时，它会检查该值是否已经能够保存 NULL 值。如果该值已经能够保存 NULL 值，函数将直接返回该值而不做任何更改。

但是，如果该值不能保存 NULL 值，`TO_NULLABLE` 函数会修改该值，使其能够保存 NULL 值。它通过将该值包装在一个能够保存 NULL 值的结构中来实现这一点，这意味着该值今后可以保存 NULL 值。

## 语法 {#syntax}

```sql
TO_NULLABLE(x);
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|----------------------------|
| x         | 原始值。        |

## 返回类型 {#return-type}

返回与输入值相同数据类型的值；如果输入值原本不是可空类型，则会将其包装在一个可空容器中。

## 示例 {#examples}

```sql
SELECT typeof(3), TO_NULLABLE(3), typeof(TO_NULLABLE(3));

typeof(3)       |to_nullable(3)|typeof(to_nullable(3))|
----------------+--------------+----------------------+
TINYINT UNSIGNED|             3|TINYINT UNSIGNED NULL |

```