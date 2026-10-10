---
title: Stored Procedure & SQL Scripting
summary: {{{ .lake }}} のストアドプロシージャを使用すると、制御フロー、変数、カーソル、動的ステートメントにアクセスしながら、サーバー上で実行される SQL ロジックをパッケージ化できます。このページでは、プロシージャの作成方法と、それを支えるインラインスクリプトの記述方法について説明します。
---

# Stored Procedure & SQL Scripting

{{{ .lake }}} のストアドプロシージャを使用すると、制御フロー、変数、カーソル、動的ステートメントにアクセスしながら、サーバー上で実行される SQL ロジックをパッケージ化できます。このページでは、プロシージャの作成方法と、それを支えるインラインスクリプトの記述方法について説明します。

## プロシージャの定義 {#defining-a-procedure}

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

| コンポーネント | 説明 |
|-----------|-------------|
| `<name>` | プロシージャの識別子です。スキーマ修飾は省略可能です。 |
| `<param_name> <data_type>` | {{{ .lake }}} のスカラー型で型付けされた入力パラメータです。パラメータは値渡しされます。 |
| `RETURNS <return_type> [NOT NULL]` | 論理的な戻り値の型を宣言します。`NOT NULL` は null 不可の応答を強制します。 |
| `LANGUAGE SQL` | {{{ .lake }}} は現在 `SQL` のみを受け付けます。 |
| `RETURN` / `RETURN TABLE` | 実行を終了し、スカラー結果または表形式の結果を返します。 |

定義を永続化するには [`CREATE PROCEDURE`](/tidb-cloud-lake/sql/create-procedure.md)、実行するには [`CALL`](/tidb-cloud-lake/sql/call-procedure.md)、削除するには [`DROP PROCEDURE`](/tidb-cloud-lake/sql/drop-procedure.md) を使用します。

### 最小の例 {#minimal-example}

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

## プロシージャ内の言語の基本 {#language-basics-inside-procedures}

### DECLARE セクション {#declare-section}

ストアドプロシージャは、実行可能セクションの前に変数を初期化するための省略可能な `DECLARE` ブロックで開始できます。ブロック内の各項目は `LET` と同じ構文に従います: `name [<data_type>] [:= <expr> | DEFAULT <expr>]`。初期化子を省略した場合、その変数は読み取る前に代入されている必要があります。早すぎる参照を行うと、エラー 3129 が発生します。

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

`DECLARE` セクションでは、オプションのデータ型、`RESULTSET`、`CURSOR` 宣言を含め、`LET` と同じ定義を使用できます。各項目の後にはセミコロンを付けてください。

### 変数と代入 {#variables-and-assignment}

変数または定数を宣言するには `LET` を使用します。型注釈と、`:=` または `DEFAULT` キーワードによる初期化子を任意で指定できます。初期化子がない場合、その変数は読み取る前に代入されている必要があります。事前に参照すると、エラー 3129 が発生します。再代入する場合は `LET` を省略します。

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

プロシージャ内のどこであっても、初期化されていない変数を参照するとエラー 3129 が発生します。

### 変数スコープ {#variable-scope}

変数のスコープは、それを囲むブロックに限定されます。内側のブロックは外側の束縛をシャドーイングでき、ブロックを抜けると外側の値が復元されます。

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

### コメント {#comments}

プロシージャでは、単一行コメント (`-- text`) と複数行コメント (`/* text */`) をサポートしています。

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

### ラムダ式 {#lambda-expressions}

ラムダ式は、配列関数に渡したり、クエリ内で呼び出したりできるインラインロジックを定義します。形式は `<parameter> -> <expression>` です（複数のパラメータを指定する場合は、パラメータを括弧で囲みます）。式には、キャスト、条件ロジック、さらにはプロシージャ変数への参照も含めることができます。

- ラムダが SQL 文内で実行される場合、ラムダ内でプロシージャ変数を参照するには `:variable_name` を使用します。
- `ARRAY_TRANSFORM` や `ARRAY_FILTER` などの関数は、入力配列の各要素に対してラムダを評価します。

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

ラムダは、プロシージャによって実行されるクエリ内でも使用できます。

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

ラムダが SQL 文のコンテキストで実行される場合、プロシージャ変数の先頭に `:` を付けることで、ラムダ内でその変数を参照できます。

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

`CASE` ロジックのような複雑な式を、ラムダ本体の中に記述することもできます。

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

## 制御フロー {#control-flow}

### IF 文 {#if-statements}

プロシージャ内で分岐するには、`IF ... ELSEIF ... ELSE ... END IF;` を使用します。

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

### CASE 式 {#case-expressions}

`CASE` 式は、入れ子になった `IF` 文の代替手段を提供します。

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

### 範囲 `FOR` {#range-for}

範囲ベースのループは、下限から上限まで（両端を含む）反復します。範囲を逆方向にたどるには、オプションの `REVERSE` キーワードを使用します。

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

範囲ループを順方向に進める場合、下限は上限以下である必要があります。

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

#### `FOR ... IN` クエリ {#for-in-queries}

クエリの結果を直接反復処理します。ループ変数は、カラムをフィールドとして公開します。

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

`FOR` は、事前に宣言された result-set 変数やカーソルに対しても反復できます（[クエリ結果の操作](#working-with-query-results) を参照）。

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

### Break and Continue {#break-and-continue}

`BREAK` はループを途中で終了するために使用し、`CONTINUE` は次の反復にスキップするために使用します。

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

ラベル付きループを終了したり、次の反復にスキップしたりするには、`BREAK <label>` または `CONTINUE <label>` を使用します。ラベルは、終了キーワードの後ろに付けて宣言します。たとえば `END LOOP main_loop;` のように記述します。

## クエリ結果の操作 {#working-with-query-results}

### 結果セット変数 {#result-set-variables}

後で反復処理できるようにクエリ結果を実体化するには、`RESULTSET` を使用します。

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

### カーソル {#cursors}

必要に応じて行を取得する必要がある場合は、カーソルを宣言します。

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

または、`RESULTSET` からカーソルを導出することもできます。

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

### 行の反復処理 {#iterating-rows}

結果セット変数とカーソルは、`FOR ... IN` ループで走査できます。

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

### テーブルを返す {#returning-tables}

表形式の結果を返すには、`RETURN TABLE(<query>)` を使用します。

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

保存された結果セットを返す場合も、同じ構文を使用します。

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

## 動的 SQL {#dynamic-sql}

### ステートメントの実行 {#executing-statements}

### 変数を使用した動的ブロック {#dynamic-blocks-with-variables}

動的ブロックは、その結果を `EXECUTE IMMEDIATE` の呼び出し元に返します。結果セットを生成するには、ブロック内で `RETURN TABLE` を使用します。

単一の SQL 文字列を実行し、その出力を取得することもできます。

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

## 注意事項と制限 {#notes-and-limitations}

- ストアドプロシージャは単一のトランザクション内で実行されます。エラーが発生すると、プロシージャ内で実行された処理はすべてロールバックされます。
- 数値型を宣言していても、返される値はクライアント側では文字列として表されます。
- `TRY ... CATCH` 構文はありません。入力を検証し、エラー条件を明示的に想定してください。
- 意図しないステートメントの実行を避けるため、識別子を動的 SQL テキストに連結する前に検証してください。
- スクリプトは `script_max_steps` 設定（デフォルトは 10,000）によって制限されます。長いループを実行する前に、この値を増やしてください。

  ```sql
  SET script_max_steps = 100000;
  ```

## 関連コマンド {#related-commands}

- [`CREATE PROCEDURE`](/tidb-cloud-lake/sql/create-procedure.md)
- [`CALL`](/tidb-cloud-lake/sql/call-procedure.md)
- [`SHOW PROCEDURES`](/tidb-cloud-lake/sql/show-procedures.md)
- [`DESCRIBE PROCEDURE`](/tidb-cloud-lake/sql/desc-procedure.md)
- [`EXECUTE IMMEDIATE`](/tidb-cloud-lake/sql/execute-immediate.md)