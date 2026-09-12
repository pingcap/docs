---
title: EXECUTE IMMEDIATE
summary: 执行 SQL 脚本。有关如何为 {{{ .lake }}} 编写 SQL 脚本，请参见 Stored Procedure & SQL Scripting。
---

# EXECUTE IMMEDIATE

执行 SQL 脚本。有关如何为 {{{ .lake }}} 编写 SQL 脚本，请参见 [存储过程与 SQL 脚本](/tidb-cloud-lake/sql/stored-procedure-scripting.md)。

## 语法 {#syntax}

```sql
EXECUTE IMMEDIATE $$
BEGIN
    <procedure_body>
    RETURN <return_value>;             -- Use to return a single value
    -- OR
    RETURN TABLE(<select_query>);      -- Use to return a table
END;
$$;
```

## 示例 {#examples}

以下示例使用循环从 -1 迭代到 2，对 sum 进行累加，结果为总和 (2)：

```sql
EXECUTE IMMEDIATE $$
BEGIN
    LET x := -1;
    LET sum := 0;
    FOR x IN x TO x + 3 DO
        sum := sum + x;
    END FOR;
    RETURN sum;
END;
$$;

┌────────┐
│ Result │
│ String │
├────────┤
│ 2      │
└────────┘
```

以下示例返回一个表，其中包含一列 `1 + 1`，其值为 2：

```sql
EXECUTE IMMEDIATE $$
BEGIN
    LET x := 1;
    RETURN TABLE(SELECT :x + 1);
END;
$$;

┌───────────┐
│   Result  │
│   String  │
├───────────┤
│ ┌───────┐ │
│ │ 1 + 1 │ │
│ │ UInt8 │ │
│ ├───────┤ │
│ │     2 │ │
│ └───────┘ │
└───────────┘
```