---
title: CALL PROCEDURE
summary: 通过调用存储过程名称来执行存储过程；如果该过程需要参数，也可以选择传入参数。
---

# CALL PROCEDURE

通过调用存储过程名称来执行存储过程；如果该过程需要参数，也可以选择传入参数。

## 语法 {#syntax}

```sql
CALL PROCEDURE <procedure_name>([<argument1>, <argument2>, ...])
```

## 示例 {#examples}

以下示例演示了如何创建并调用一个将重量从千克（kg）转换为磅（lb）的存储过程：

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

CALL PROCEDURE convert_kg_to_lb(10.00);

┌────────────┐
│   Result   │
├────────────┤
│ 22.0462000 │
└────────────┘
```