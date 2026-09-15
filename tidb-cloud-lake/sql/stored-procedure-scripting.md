---
title: 存储过程与 SQL 脚本
summary: {{{ .lake }}} 中的存储过程可让你将运行在服务器端的 SQL 逻辑封装起来，并支持控制流、变量、游标和动态语句。本文介绍如何创建存储过程，以及如何编写为其提供支持的内联脚本。
---

# 存储过程与 SQL 脚本

{{{ .lake }}} 中的存储过程可让你将运行在服务器端的 SQL 逻辑封装起来，并支持控制流、变量、游标和动态语句。本文介绍如何创建存储过程，以及如何编写为其提供支持的内联脚本。

## 定义存储过程 {#defining-a-procedure}

```sql
CREATE [OR REPLACE] PROCEDURE <name>(<param_name> <data_type>, ...)
RETURNS <return_type> [NOT NULL]
LANGUAGE SQL
[COMMENT = '<text>']
AS $$
BEGIN
    -- Declarations and statements
    RETURN <scalar_value>;
    -- Or return a query result
    -- RETURN TABLE(<select_query>);
END;
$$;
```

| 组成部分 | 说明 |
|-----------|-------------|
| `<name>` | 存储过程的标识符。可选是否带上 schema 限定。 |
| `<param_name> <data_type>` | 使用 {{{ .lake }}} 标量类型定义的输入参数。参数按值传递。 |
| `RETURNS <return_type> [NOT NULL]` | 声明逻辑返回类型。`NOT NULL` 强制返回不可为空的响应。 |
| `LANGUAGE SQL` | {{{ .lake }}} 当前仅接受 `SQL`。 |
| `RETURN` / `RETURN TABLE` | 结束执行，并返回标量结果或表格结果。 |

使用 [`CREATE PROCEDURE`](/tidb-cloud-lake/sql/create-procedure.md) 持久化定义，使用 [`CALL`](/tidb-cloud-lake/sql/call-procedure.md) 运行存储过程，使用 [`DROP PROCEDURE`](/tidb-cloud-lake/sql/drop-procedure.md) 删除它。

### 最小示例 {#minimal-example}

```sql
CREATE OR REPLACE PROCEDURE convert_kg_to_lb(kg DOUBLE)
RETURNS DOUBLE
LANGUAGE SQL
COMMENT = 'Converts kilograms to pounds'
AS $$
BEGIN
    RETURN kg * 2.20462;
END;
$$;

CALL PROCEDURE convert_kg_to_lb(10);
```

## 存储过程中的语言基础 {#language-basics-inside-procedures}

### DECLARE 部分 {#declare-section}

存储过程可以以可选的 `DECLARE` 块开头，在可执行部分之前初始化变量。该块中的每一项都遵循与 `LET` 相同的语法：`name [<data_type>] [:= <expr> | DEFAULT <expr>]`。如果省略初始化器，则该变量必须在读取前先被赋值；过早引用会引发错误 3129。

```sql
CREATE OR REPLACE PROCEDURE sp_with_declare()
RETURNS INT
LANGUAGE SQL
AS $$
DECLARE
    counter INT DEFAULT 0;
BEGIN
    counter := counter + 5;
    RETURN counter;
END;
$$;

CALL PROCEDURE sp_with_declare();
```

`DECLARE` 部分接受与 `LET` 相同的定义，包括可选的数据类型、`RESULTSET` 和 `CURSOR` 声明。每一项后都要使用分号。

### 变量与赋值 {#variables-and-assignment}

使用 `LET` 声明变量或常量。你可以选择提供类型注解，并使用 `:=` 或 `DEFAULT` 关键字指定初始化器。如果没有初始化器，则变量必须在读取前先被赋值；否则会引发错误 3129。重新赋值时省略 `LET`。

```sql
CREATE OR REPLACE PROCEDURE sp_demo_variables()
RETURNS FLOAT
LANGUAGE SQL
AS $$
BEGIN
    LET total DECIMAL(10, 2) DEFAULT 100;
    LET rate FLOAT := 0.07;
    LET surcharge FLOAT := NULL; -- Explicitly initialize before use
    LET tax FLOAT DEFAULT rate;  -- DEFAULT can reference initialized variables

    total := total * rate; -- Multiply by the rate
    total := total + COALESCE(surcharge, 5); -- Reassign without LET
    total := total + tax;

    RETURN total;
END;
$$;

CALL PROCEDURE sp_demo_variables();
```

在存储过程中的任何位置引用未初始化的变量，都会引发错误 3129。

### 变量作用域 {#variable-scope}

变量的作用域限定在其所在的外层块内。内层块可以遮蔽外层绑定，而在退出该块时，外层值会被恢复。

```sql
CREATE OR REPLACE PROCEDURE sp_demo_scope()
RETURNS STRING
LANGUAGE SQL
AS $$
BEGIN
    LET threshold := 10;
    LET summary := 'outer=' || threshold;

    IF threshold > 0 THEN
        LET threshold := 5; -- Shadows the outer value
        summary := summary || ', inner=' || threshold;
    END IF;

    summary := summary || ', after=' || threshold;
    RETURN summary;
END;
$$;

CALL PROCEDURE sp_demo_scope();
```

### 注释 {#comments}

存储过程支持单行注释（`-- text`）和多行注释（`/* text */`）。

```sql
CREATE OR REPLACE PROCEDURE sp_demo_comments()
RETURNS FLOAT
LANGUAGE SQL
AS $$
BEGIN
    -- Calculate price with tax
    LET price := 15;
    LET tax_rate := 0.08;

    /*
        Multi-line comments are useful for documenting complex logic.
        The following line returns the tax-inclusive price.
    */
    RETURN price * (1 + tax_rate);
END;
$$;

CALL PROCEDURE sp_demo_comments();
```

### Lambda 表达式 {#lambda-expressions}

Lambda 表达式用于定义内联逻辑，可以传递给数组函数，或在查询中调用。其形式为 `<parameter> -> <expression>`（当提供多个参数时，请将参数放在括号中）。该表达式可以包含类型转换、条件逻辑，甚至对过程变量的引用。

- 当 lambda 在 SQL 语句中运行时，使用 `:variable_name` 在 lambda 内部引用过程变量。
- `ARRAY_TRANSFORM` 和 `ARRAY_FILTER` 等函数会对输入数组中的每个元素计算一次 lambda。

```sql
CREATE OR REPLACE PROCEDURE sp_demo_lambda_array()
RETURNS STRING
LANGUAGE SQL
AS $$
BEGIN
    RETURN TABLE(
        SELECT ARRAY_TRANSFORM([1, 2, 3, 4], item -> (item::Int + 1)) AS incremented
    );
END;
$$;

CALL PROCEDURE sp_demo_lambda_array();
```

Lambda 也可以出现在由过程执行的查询中。

```sql
CREATE OR REPLACE PROCEDURE sp_demo_lambda_query()
RETURNS STRING
LANGUAGE SQL
AS $$
BEGIN
    RETURN TABLE(
        SELECT
            number,
            ARRAY_TRANSFORM([number, number + 1], val -> (val::Int + 1)) AS next_values
        FROM numbers(3)
    );
END;
$$;

CALL PROCEDURE sp_demo_lambda_query();
```

当 lambda 在 SQL 语句上下文中运行时，可通过在过程变量前加上 `:` 来在 lambda 内部捕获这些变量。

```sql
CREATE OR REPLACE PROCEDURE sp_lambda_filter()
RETURNS STRING
LANGUAGE SQL
AS $$
BEGIN
    LET threshold := 2;
    RETURN TABLE(
        SELECT ARRAY_FILTER([1, 2, 3, 4], element -> (element::Int > :threshold)) AS filtered
    );
END;
$$;

CALL PROCEDURE sp_lambda_filter();
```

你还可以在 lambda 主体中放入复杂表达式，例如 `CASE` 逻辑。

```sql
CREATE OR REPLACE PROCEDURE sp_lambda_case()
RETURNS STRING
LANGUAGE SQL
AS $$
BEGIN
    RETURN TABLE(
        SELECT
            number,
            ARRAY_TRANSFORM(
                [number - 1, number, number + 1],
                val -> (CASE WHEN val % 2 = 0 THEN 'even' ELSE 'odd' END)
            ) AS parity_window
        FROM numbers(3)
    );
END;
$$;

CALL PROCEDURE sp_lambda_case();
```

## 控制流 {#control-flow}

### IF 语句 {#if-statements}

使用 `IF ... ELSEIF ... ELSE ... END IF;` 在过程内部进行分支处理。

```sql
CREATE OR REPLACE PROCEDURE sp_evaluate_score(score INT)
RETURNS STRING
LANGUAGE SQL
AS $$
BEGIN
    IF score >= 90 THEN
        RETURN 'Excellent';
    ELSEIF score >= 70 THEN
        RETURN 'Good';
    ELSE
        RETURN 'Review';
    END IF;
END;
$$;

CALL PROCEDURE sp_evaluate_score(82);
```

### CASE 表达式 {#case-expressions}

`CASE` 表达式提供了嵌套 `IF` 语句之外的另一种选择。

```sql
CREATE OR REPLACE PROCEDURE sp_membership_discount(level STRING)
RETURNS FLOAT
LANGUAGE SQL
AS $$
BEGIN
    RETURN CASE
        WHEN level = 'gold' THEN 0.2
        WHEN level = 'silver' THEN 0.1
        ELSE 0
    END;
END;
$$;

CALL PROCEDURE sp_membership_discount('silver');
```

### 范围 `FOR` {#range-for}

基于范围的循环会从下界迭代到上界（包含边界值）。使用可选的 `REVERSE` 关键字可以反向遍历该范围。

```sql
CREATE OR REPLACE PROCEDURE sp_sum_range(start_val INT, end_val INT)
RETURNS INT
LANGUAGE SQL
AS $$
BEGIN
    LET total := 0;
    FOR i IN start_val TO end_val DO
        total := total + i;
    END FOR;
    RETURN total;
END;
$$;

CALL PROCEDURE sp_sum_range(1, 5);
```

向前迭代时，范围循环要求下界小于或等于上界。

```sql
CREATE OR REPLACE PROCEDURE sp_reverse_count(start_val INT, end_val INT)
RETURNS STRING
LANGUAGE SQL
AS $$
BEGIN
    LET output := '';
    FOR i IN REVERSE start_val TO end_val DO
        output := output || i || ' ';
    END FOR;
    RETURN TRIM(output);
END;
$$;

CALL PROCEDURE sp_reverse_count(1, 5);
```

#### `FOR ... IN` 查询 {#for-in-queries}

直接对查询结果进行迭代。循环变量会将各列暴露为字段。

```sql
CREATE OR REPLACE PROCEDURE sp_sum_query(limit_rows INT)
RETURNS BIGINT
LANGUAGE SQL
AS $$
BEGIN
    LET total := 0;
    FOR rec IN SELECT number FROM numbers(:limit_rows) DO
        total := total + rec.number;
    END FOR;
    RETURN total;
END;
$$;

CALL PROCEDURE sp_sum_query(5);
```

`FOR` 也可以对先前声明的结果集变量或游标进行迭代（参见[处理查询结果](#working-with-query-results)）。

### `WHILE` {#while}

```sql
CREATE OR REPLACE PROCEDURE sp_factorial(n INT)
RETURNS INT
LANGUAGE SQL
AS $$
BEGIN
    LET result := 1;
    WHILE n > 0 DO
        result := result * n;
        n := n - 1;
    END WHILE;
    RETURN result;
END;
$$;

CALL PROCEDURE sp_factorial(5);
```

### `REPEAT` {#repeat}

```sql
CREATE OR REPLACE PROCEDURE sp_repeat_sum(limit_val INT)
RETURNS INT
LANGUAGE SQL
AS $$
BEGIN
    LET counter := 0;
    LET total := 0;

    REPEAT
        counter := counter + 1;
        total := total + counter;
    UNTIL counter >= limit_val END REPEAT;

    RETURN total;
END;
$$;

CALL PROCEDURE sp_repeat_sum(3);
```

### `LOOP` {#loop}

```sql
CREATE OR REPLACE PROCEDURE sp_retry_counter(max_attempts INT)
RETURNS INT
LANGUAGE SQL
AS $$
BEGIN
    LET retries := 0;
    LOOP
        retries := retries + 1;
        IF retries >= max_attempts THEN
            BREAK;
        END IF;
    END LOOP;

    RETURN retries;
END;
$$;

CALL PROCEDURE sp_retry_counter(5);
```

### Break 和 Continue {#break-and-continue}

使用 `BREAK` 可以提前退出循环，使用 `CONTINUE` 可以跳过当前迭代并进入下一次迭代。

```sql
CREATE OR REPLACE PROCEDURE sp_break_example(limit_val INT)
RETURNS INT
LANGUAGE SQL
AS $$
BEGIN
    LET counter := 0;
    LET total := 0;

    WHILE TRUE DO
        counter := counter + 1;
        IF counter > limit_val THEN
            BREAK;
        END IF;
        IF counter % 2 = 0 THEN
            CONTINUE;
        END IF;
        total := total + counter;
    END WHILE;

    RETURN total;
END;
$$;

CALL PROCEDURE sp_break_example(5);
```

使用 `BREAK <label>` 或 `CONTINUE <label>` 可以退出带标签的循环，或跳转到该循环的下一次迭代。标签通过追加在结束关键字之后来声明，例如 `END LOOP main_loop;`。

## 处理查询结果 {#working-with-query-results}

### 结果集变量 {#result-set-variables}

使用 `RESULTSET` 可以将查询结果物化，以便后续迭代。

```sql
CREATE OR REPLACE PROCEDURE sp_total_active_salary()
RETURNS DECIMAL(18, 2)
LANGUAGE SQL
AS $$
BEGIN
    -- Assume table hr_employees(id, salary, active) exists.
    LET employees RESULTSET := SELECT id, salary FROM hr_employees WHERE active = TRUE;
    LET total := 0;

    FOR emp IN employees DO
        total := total + emp.salary;
    END FOR;

    RETURN total;
END;
$$;

CALL PROCEDURE sp_total_active_salary();
```

### 游标 {#cursors}

当你需要按需提取行时，可以声明游标。

```sql
CREATE OR REPLACE PROCEDURE sp_fetch_two()
RETURNS INT
LANGUAGE SQL
AS $$
BEGIN
    -- Assume table stocks(sku, quantity) exists.
    LET cur CURSOR FOR SELECT quantity FROM stocks ORDER BY quantity;
    OPEN cur;

    LET first := 0;
    LET second := 0;

    FETCH cur INTO first;
    FETCH cur INTO second;

    CLOSE cur;
    RETURN first + second;
END;
$$;

CALL PROCEDURE sp_fetch_two();
```

或者，也可以从 `RESULTSET` 派生一个游标。

```sql
CREATE OR REPLACE PROCEDURE sp_first_number()
RETURNS INT
LANGUAGE SQL
AS $$
BEGIN
    LET recent RESULTSET := SELECT number FROM numbers(5);
    LET num_cursor CURSOR FOR recent;

    OPEN num_cursor;
    LET first_value := NULL;
    FETCH num_cursor INTO first_value;
    CLOSE num_cursor;

    RETURN first_value;
END;
$$;

CALL PROCEDURE sp_first_number();
```

### 遍历行 {#iterating-rows}

可以使用 `FOR ... IN` 循环来遍历结果集变量和游标。

```sql
CREATE OR REPLACE PROCEDURE sp_low_stock_count()
RETURNS INT
LANGUAGE SQL
AS $$
BEGIN
    LET inventory RESULTSET := SELECT sku, quantity FROM stocks;
    LET low_stock := 0;

    FOR item IN inventory DO
        IF item.quantity < 5 THEN
            low_stock := low_stock + 1;
        END IF;
    END FOR;

    RETURN low_stock;
END;
$$;

CALL PROCEDURE sp_low_stock_count();
```

### 返回表 {#returning-tables}

使用 `RETURN TABLE(<query>)` 输出表格结果。

```sql
CREATE OR REPLACE PROCEDURE sp_sales_summary()
RETURNS STRING
LANGUAGE SQL
AS $$
BEGIN
    RETURN TABLE(
        SELECT product_id, SUM(quantity) AS total_quantity
        FROM sales_detail
        WHERE sale_date = today()
        GROUP BY product_id
        ORDER BY product_id
    );
END;
$$;

CALL PROCEDURE sp_sales_summary();
```

返回已存储的结果集时使用相同的语法：

```sql
CREATE OR REPLACE PROCEDURE sp_return_cached()
RETURNS STRING
LANGUAGE SQL
AS $$
BEGIN
    LET latest RESULTSET := SELECT number FROM numbers(3);
    RETURN TABLE(latest);
END;
$$;

CALL PROCEDURE sp_return_cached();
```

## 动态 SQL {#dynamic-sql}

### 执行语句 {#executing-statements}

### 带变量的动态代码块 {#dynamic-blocks-with-variables}

动态代码块会将其结果返回给 `EXECUTE IMMEDIATE` 的调用方。使用代码块中的 `RETURN TABLE` 可以生成结果集。

你也可以运行单条 SQL 字符串并捕获其输出：

```sql
EXECUTE IMMEDIATE $$
BEGIN
    LET recent RESULTSET := EXECUTE IMMEDIATE 'SELECT number FROM numbers(3)';
    RETURN TABLE(recent);
END;
$$;

CREATE OR REPLACE PROCEDURE sp_dynamic_resultset()
RETURNS STRING
LANGUAGE SQL
AS $$
BEGIN
    LET recent RESULTSET := EXECUTE IMMEDIATE 'SELECT number FROM numbers(3)';
    RETURN TABLE(recent);
END;
$$;

CALL PROCEDURE sp_dynamic_resultset();
```

## 注意事项和限制 {#notes-and-limitations}

- 存储过程在单个事务中执行；任何错误都会回滚该过程中执行的工作。
- 返回值在客户端侧会以字符串形式呈现，即使声明的是数值类型也是如此。
- 不支持 `TRY ... CATCH` 结构；请显式验证输入并预判错误情况。
- 在将标识符拼接到动态 SQL 文本中之前，请先进行校验，以避免执行非预期的语句。
- 脚本受 `script_max_steps` 设置限制（默认值为 10,000）。运行长循环前，请先增大该值：

  ```sql
  SET script_max_steps = 100000;
  ```

## 相关命令 {#related-commands}

- [`CREATE PROCEDURE`](/tidb-cloud-lake/sql/create-procedure.md)
- [`CALL`](/tidb-cloud-lake/sql/call-procedure.md)
- [`SHOW PROCEDURES`](/tidb-cloud-lake/sql/show-procedures.md)
- [`DESCRIBE PROCEDURE`](/tidb-cloud-lake/sql/desc-procedure.md)
- [`EXECUTE IMMEDIATE`](/tidb-cloud-lake/sql/execute-immediate.md)