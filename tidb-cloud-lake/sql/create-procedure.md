---
title: CREATE PROCEDURE
summary: SQL 操作を実行し、結果を返すストアドプロシージャを定義します。
---

# CREATE PROCEDURE

SQL 操作を実行し、結果を返すストアドプロシージャを定義します。

## 構文 {#syntax}

```sql
CREATE PROCEDURE <procedure_name>(<parameter_name> <data_type>, ...)
RETURNS <return_data_type> [NOT NULL]
LANGUAGE <language>
[ COMMENT '<comment>' ]
AS $$
BEGIN
    <procedure_body>
    RETURN <return_value>;             -- Use to return a single value
    -- OR
    RETURN TABLE(<select_query>);      -- Use to return a table
END;
$$;
```

| パラメータ                               | 説明                                                                                                               |
|-----------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| `<procedure_name>`                      | プロシージャの名前です。                                                                                                    |
| `<parameter_name> <data_type>`          | 入力パラメータ（省略可能）です。各パラメータには指定されたデータ型が必要です。複数のパラメータを定義でき、カンマで区切ります。 |
| `RETURNS <return_data_type> [NOT NULL]` | 戻り値のデータ型を指定します。`NOT NULL` は、返される値が NULL にならないことを保証します。                        |
| `LANGUAGE`                              | プロシージャ本体を記述する言語を指定します。現在は `SQL` のみサポートされています。                       |
| `COMMENT`                               | プロシージャを説明する省略可能なテキストです。                                                                                   |
| `AS ...`                                | SQL 文、変数宣言、ループ、および RETURN 文を含むプロシージャ本体を囲みます。        |

## アクセス制御要件 {#access-control-requirements}

| Privilege        | Object Type | 説明          |
|:-----------------|:------------|:---------------------|
| CREATE PROCEDURE | Global      | プロシージャを作成します。 |

プロシージャを作成するには、操作を実行するユーザーまたは [current_role](/tidb-cloud-lake/guides/roles.md) が CREATE PROCEDURE [権限](/tidb-cloud-lake/guides/privileges.md) を持っている必要があります。

## 例 {#examples}

この例では、重量をキログラム（kg）からポンド（lb）に変換するストアドプロシージャを定義します。

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
```

ループ、条件、および動的変数を使用するストアドプロシージャを定義することもできます。

```sql

CREATE OR REPLACE PROCEDURE loop_test()
RETURNS INT
LANGUAGE SQL
COMMENT = 'loop test'
AS $$
BEGIN
    LET x RESULTSET := select number n from numbers(10);
    LET sum := 0;
    FOR x IN x DO
        FOR batch in 0 TO x.n DO
            IF batch % 2 = 0 THEN
                sum := sum + batch;
            ELSE
                sum := sum - batch;
            END IF;
        END FOR;
    END FOR;
    RETURN sum;
END;
$$;

-- Grant ACCESS PROCEDURE Privilege TO role test
GRANT ACCESS PROCEDURE ON PROCEDURE loop_test() to role test;

```

```sql
CALL PROCEDURE loop_test();

┌─Result─┐
│   -5   │
└────────┘
```