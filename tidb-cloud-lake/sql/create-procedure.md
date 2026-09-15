---
title: CREATE PROCEDURE
summary: 定义一个执行 SQL 操作并返回结果的存储过程。
---

# CREATE PROCEDURE

定义一个执行 SQL 操作并返回结果的存储过程。

## 语法 {#syntax}

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

| 参数 | 描述 |
|-----------------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| `<procedure_name>`                      | 存储过程的名称。                                                                                                    |
| `<parameter_name> <data_type>`          | 输入参数（可选），每个参数都需要指定数据类型。可以定义多个参数，并使用逗号分隔。 |
| `RETURNS <return_data_type> [NOT NULL]` | 指定返回值的数据类型。`NOT NULL` 可确保返回的值不能为 NULL。                        |
| `LANGUAGE`                              | 指定存储过程主体所使用的语言。目前仅支持 `SQL`。                       |
| `COMMENT`                               | 用于描述该存储过程的可选文本。                                                                                   |
| `AS ...`                                | 包含存储过程主体，其中可以包括 SQL 语句、变量声明、循环以及 RETURN 语句。        |

## 访问控制要求 {#access-control-requirements}

| 权限 | 对象类型 | 描述 |
|:-----------------|:------------|:---------------------|
| CREATE PROCEDURE | Global      | 创建存储过程。 |

要创建存储过程，执行该操作的用户或 [current_role](/tidb-cloud-lake/guides/roles.md) 必须具有 CREATE PROCEDURE [权限](/tidb-cloud-lake/guides/privileges.md)。

## 示例 {#examples}

以下示例定义了一个将重量从千克（kg）转换为磅（lb）的存储过程：

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

你还可以定义一个使用循环、条件和动态变量的存储过程。

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