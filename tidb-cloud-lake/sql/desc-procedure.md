---
title: DESC PROCEDURE
summary: 显示特定存储过程的详细信息。
---

# DESC PROCEDURE

显示特定存储过程的详细信息。

## 语法 {#syntax}

```sql
DESC | DESCRIBE PROCEDURE <procedure_name>([<parameter_type1>, <parameter_type2>, ...])
```

- 如果过程没有参数，请使用空括号：`DESC PROCEDURE <procedure_name>()`；
- 对于带参数的过程，请指定精确的类型以避免错误。

## 示例 {#examples}

以下示例创建了一个名为 `sum_even_numbers` 的存储过程，然后显示其详细信息。

```sql
CREATE PROCEDURE sum_even_numbers(start_val UInt8, end_val UInt8)
RETURNS UInt8 NOT NULL
LANGUAGE SQL
COMMENT='Calculate the sum of all even numbers'
AS $$
BEGIN
    LET sum := 0;
    FOR i IN start_val TO end_val DO
        IF i % 2 = 0 THEN
            sum := sum + i;
        END IF;
    END FOR;

    RETURN sum;
END;
$$;

DESC PROCEDURE sum_even_numbers(Uint8, Uint8);

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  Property │                                                                                        Value                                                                                       │
├───────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ signature │ (start_val,end_val)                                                                                                                                                                │
│ returns   │ (UInt8)                                                                                                                                                                            │
│ language  │ SQL                                                                                                                                                                                │
│ body      │ BEGIN\n    LET sum := 0;\n    FOR i IN start_val TO end_val DO\n        IF i % 2 = 0 THEN\n            sum := sum + i;\n        END IF;\n    END FOR;\n    \n    RETURN sum;\nEND; │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```