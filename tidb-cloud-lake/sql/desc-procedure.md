---
title: DESC PROCEDURE
summary: 特定のストアドプロシージャに関する詳細情報を表示します。
---

# DESC PROCEDURE

特定のストアドプロシージャに関する詳細情報を表示します。

## 構文 {#syntax}

```sql
DESC | DESCRIBE PROCEDURE <procedure_name>([<parameter_type1>, <parameter_type2>, ...])
```

- プロシージャにパラメータがない場合は、空の括弧を使用します: `DESC PROCEDURE <procedure_name>()`;
- パラメータがあるプロシージャの場合は、エラーを避けるために正確な型を指定してください。

## 例 {#examples}

この例では、`sum_even_numbers` という名前のストアドプロシージャを作成してから、その詳細を表示します。

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