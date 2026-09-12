---
title: DROP PROCEDURE
summary: 删除现有的存储过程。
---

# DROP PROCEDURE

删除现有的存储过程。

## 语法 {#syntax}

```sql
DROP PROCEDURE <procedure_name>([<parameter_type1>, <parameter_type2>, ...])
```

- 如果存储过程没有参数，请使用空括号：`DROP PROCEDURE <procedure_name>()`；
- 对于带参数的存储过程，请指定精确的类型以避免错误。

## 示例 {#examples}

以下示例先创建一个存储过程，然后将其删除：

```sql
CREATE PROCEDURE convert_kg_to_lb(kg DECIMAL(4, 2))
RETURNS DECIMAL(10, 2)
LANGUAGE SQL
COMMENT = 'Converts kilograms to pounds'
AS $$
BEGIN
    RETURN kg * 2.20462;
END;
$$;

DROP PROCEDURE convert_kg_to_lb(Decimal(4, 2));
```