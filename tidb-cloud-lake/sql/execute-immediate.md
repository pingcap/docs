---
title: EXECUTE IMMEDIATE
summary: SQL スクリプトを実行します。{{{ .lake }}} 向けの SQL スクリプトの書き方については、Stored Procedure & SQL Scripting を参照してください。
---

# EXECUTE IMMEDIATE

SQL スクリプトを実行します。{{{ .lake }}} 向けの SQL スクリプトの書き方については、[Stored Procedure & SQL Scripting](/tidb-cloud-lake/sql/stored-procedure-scripting.md) を参照してください。

## 構文 {#syntax}

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

## 例 {#examples}

次の例では、ループを使用して -1 から 2 まで反復しながら sum を加算し、結果として合計値 (2) を返します。

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

次の例では、カラム `1 + 1` と値 2 を含むテーブルを返します。

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