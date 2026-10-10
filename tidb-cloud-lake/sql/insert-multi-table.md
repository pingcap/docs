---
title: INSERT (multi-table)
summary: 単一のトランザクションで複数のテーブルに行を挿入します。挿入は、特定の条件に依存して実行することも（条件付き）、条件に関係なく実行することも（無条件）できます。
---

# INSERT (multi-table)

単一のトランザクションで複数のテーブルに行を挿入します。挿入は、特定の条件に依存して実行することも（条件付き）、条件に関係なく実行することも（無条件）できます。

> **Tip:**
>
> {{{ .lake }}} はアトミックな操作によってデータ整合性を保証します。挿入、更新、置換、削除は、完全に成功するか、完全に失敗するかのいずれかです。

関連情報: [INSERT](/tidb-cloud-lake/sql/insert.md)

## 構文 {#syntax}

```sql
-- Unconditional INSERT ALL: Inserts each row into multiple tables without any conditions or restrictions.
INSERT [ OVERWRITE ] ALL
    INTO <target_table> [ ( <target_col_name> [ , ... ] ) ] [ VALUES ( <source_col_name> [ , ... ] ) ]
    ...
SELECT ...

-- Conditional INSERT ALL: Inserts each row into multiple tables, but only if certain conditions are met.
INSERT [ OVERWRITE ] ALL
    WHEN <condition> THEN
        INTO <target_table> [ ( <target_col_name> [ , ... ] ) ] [ VALUES ( <source_col_name> [ , ... ] ) ]
      [ INTO ... ]

  [ WHEN ... ]

  [ ELSE INTO ... ]
SELECT ...

-- Conditional INSERT FIRST: Inserts each row into multiple tables, but stops after the first successful insertion.
INSERT [ OVERWRITE ] FIRST
    WHEN <condition> THEN
        INTO <target_table> [ ( <target_col_name> [ , ... ] ) ] [ VALUES ( <source_col_name> [ , ... ] ) ]
      [ INTO ... ]

  [ WHEN ... ]

  [ ELSE INTO ... ]
SELECT ...
```

| パラメータ                                | 説明                                                                                                                                                                                                                                                                                                                                 |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `OVERWRITE`                              | 挿入前に既存データを切り捨てるかどうかを示します。                                                                                                                                                                                                                                                                                   |
| `( <target_col_name> [ , ... ] )`        | データを挿入する対象テーブル内のカラム名を指定します。<br/>- 省略した場合、対象テーブルのすべてのカラムにデータが挿入されます。                                                                                                                                                                                                       |
| `VALUES ( <source_col_name> [ , ... ] )` | 対象テーブルに挿入するデータの取得元となるソースカラム名を指定します。<br/>- 省略した場合、サブクエリが返すすべてのカラムが対象テーブルに挿入されます。<br/>- `<source_col_name>` に列挙したカラムのデータ型は、`<target_col_name>` で指定したものと一致しているか、互換性がある必要があります。 |
| `SELECT ...`                             | 対象テーブルに挿入するデータを提供するサブクエリです。<br/>- サブクエリ内のカラムには明示的にエイリアスを割り当てることができます。これにより、WHEN 句および VALUES 句の中でそのエイリアスを使ってカラムを参照できます。                                                                                                             |
| `WHEN`                                   | 特定の対象テーブルにデータを挿入するタイミングを決定する条件文です。<br/>- 条件付きのマルチテーブル挿入では、少なくとも 1 つの WHEN 句が必要です。<br/>- 1 つの WHEN 句には複数の INTO 句を含めることができ、それらの INTO 句は同じテーブルを対象にすることもできます。<br/>- WHEN 句を無条件で実行するには、`WHEN 1 THEN ...` を使用できます。 |
| `ELSE`                                   | WHEN 句で指定したいずれの条件も満たされない場合に実行する動作を指定します。                                                                                                                                                                                                                                                          |

## 重要な注意事項 {#important-notes}

- `VALUES(...)` 式では、集約関数、外部 UDF、ウィンドウ関数は使用できません。

## 例 {#examples}

### 例 1: 無条件 INSERT ALL {#example-1-unconditional-insert-all}

この例では、無条件 INSERT ALL 操作を示します。`employee_data_source` テーブルの各行を、`employees` テーブルと `employee_history` テーブルの両方に挿入します。

1. 従業員データを管理するためのテーブル（従業員の詳細情報と雇用履歴を含む）を作成し、その後、サンプルの従業員情報をソーステーブルに投入します。

    ```sql
    -- Create the employees table
    CREATE TABLE employees (
        employee_id INT,
        employee_name VARCHAR(100),
        hire_date DATE
    );
    
    -- Create the employee_history table
    CREATE TABLE employee_history (
        employee_id INT,
        hire_date DATE,
        termination_date DATE
    );
    
    -- Create the employee_data_source table
    CREATE TABLE employee_data_source (
        employee_id INT,
        employee_name VARCHAR(100),
        hire_date DATE
    );
    
    -- Insert data into the employee_data_source table
    INSERT INTO employee_data_source (employee_id, employee_name, hire_date)
    VALUES
        (1, 'Alice', '2023-01-15'),
        (2, 'Bob', '2023-02-20'),
        (3, 'Charlie', '2023-03-25');
    ```

2. 無条件 INSERT ALL 操作を使用して、`employee_data_source` テーブルから `employees` テーブルと `employee_history` テーブルの両方にデータを転送します。

```sql
-- Unconditional INSERT ALL: Insert data into the employees and employee_history tables
INSERT ALL
    INTO employees (employee_id, employee_name, hire_date) VALUES (employee_id, employee_name, hire_date)
    INTO employee_history (employee_id, hire_date) VALUES (employee_id, hire_date)
SELECT employee_id, employee_name, hire_date FROM employee_data_source;

-- Query the employees table
SELECT * FROM employees;

┌─────────────────────────────────────────────────────┐
│   employee_id   │   employee_name  │    hire_date   │
├─────────────────┼──────────────────┼────────────────┤
│               1 │ Alice            │ 2023-01-15     │
│               2 │ Bob              │ 2023-02-20     │
│               3 │ Charlie          │ 2023-03-25     │
└─────────────────────────────────────────────────────┘

-- Query the employee_history table
SELECT * FROM employee_history;

┌─────────────────────────────────────────────────────┐
│   employee_id   │    hire_date   │ termination_date │
├─────────────────┼────────────────┼──────────────────┤
│               1 │ 2023-01-15     │ NULL             │
│               2 │ 2023-02-20     │ NULL             │
│               3 │ 2023-03-25     │ NULL             │
└─────────────────────────────────────────────────────┘
```

### Example-2: 条件付き INSERT ALL と FIRST {#example-2-conditional-insert-all-first}

この例では、条件付き INSERT ALL を使用して、特定の条件に基づいて売上データを別々のテーブルに挿入する方法を示します。複数の条件を満たすレコードは、対応するすべてのテーブルに挿入されます。

1. 3 つのテーブル `products`、`high_quantity_sales`、`high_price_sales`、および `sales_data_source` を作成します。次に、`sales_data_source` テーブルに 3 件の売上レコードを挿入します。

    ```sql
    -- Create the high_quantity_sales table
    CREATE TABLE high_quantity_sales (
        sale_id INT,
        product_id INT,
        sale_date DATE,
        quantity INT,
        total_price DECIMAL(10, 2)
    );
    
    -- Create the high_price_sales table
    CREATE TABLE high_price_sales (
        sale_id INT,
        product_id INT,
        sale_date DATE,
        quantity INT,
        total_price DECIMAL(10, 2)
    );
    
    -- Create the sales_data_source table
    CREATE TABLE sales_data_source (
        sale_id INT,
        product_id INT,
        sale_date DATE,
        quantity INT,
        total_price DECIMAL(10, 2)
    );
    
    -- Insert data into the sales_data_source table
    INSERT INTO sales_data_source (sale_id, product_id, sale_date, quantity, total_price)
    VALUES
        (1, 101, '2023-01-15', 5, 100.00),
        (2, 102, '2023-02-20', 3, 75.00),
        (3, 103, '2023-03-25', 10, 200.00);
    ```

2. 条件付き INSERT ALL を使用して、特定の条件に基づいて複数のテーブルに行を挿入します。数量が 4 より大きいレコードは `high_quantity_sales` テーブルに挿入され、合計価格が 50 を超えるレコードは `high_price_sales` テーブルに挿入されます。

    ```sql
    -- Conditional INSERT ALL: Inserts each row into multiple tables, but only if certain conditions are met.
    INSERT ALL
        WHEN quantity > 4 THEN INTO high_quantity_sales
        WHEN total_price > 50 THEN INTO high_price_sales
    SELECT * FROM sales_data_source;
    
    SELECT * FROM high_quantity_sales;
    
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
    │     sale_id     │    product_id   │    sale_date   │     quantity    │        total_price       │
    ├─────────────────┼─────────────────┼────────────────┼─────────────────┼──────────────────────────┤
    │               1 │             101 │ 2023-01-15     │               5 │ 100.00                   │
    │               3 │             103 │ 2023-03-25     │              10 │ 200.00                   │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘
    
    SELECT * FROM high_price_sales;
    
    ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
    │     sale_id     │    product_id   │    sale_date   │     quantity    │        total_price       │
    ├─────────────────┼─────────────────┼────────────────┼─────────────────┼──────────────────────────┤
    │               1 │             101 │ 2023-01-15     │               5 │ 100.00                   │
    │               2 │             102 │ 2023-02-20     │               3 │ 75.00                    │
    │               3 │             103 │ 2023-03-25     │              10 │ 200.00                   │
    └─────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```

3. `high_quantity_sales` テーブルと `high_price_sales` テーブルのデータを空にします。

    ```sql
    TRUNCATE TABLE high_quantity_sales;
    
    TRUNCATE TABLE high_price_sales;
    ```

4. 条件付き INSERT FIRST を使用して、特定の条件に基づいて複数のテーブルに行を挿入します。各行について、最初の挿入が成功した時点で処理を停止します。そのため、ID が 1 と 3 の売上レコードは、手順 2 の条件付き INSERT ALL の結果とは異なり、`high_quantity_sales` テーブルにのみ挿入されます。

```sql
-- Conditional INSERT FIRST: Inserts each row into multiple tables, but stops after the first successful insertion.
INSERT FIRST
    WHEN quantity > 4 THEN INTO high_quantity_sales
    WHEN total_price > 50 THEN INTO high_price_sales
SELECT * FROM sales_data_source;

SELECT * FROM high_quantity_sales;

┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│     sale_id     │    product_id   │    sale_date   │     quantity    │        total_price       │
├─────────────────┼─────────────────┼────────────────┼─────────────────┼──────────────────────────┤
│               1 │             101 │ 2023-01-15     │               5 │ 100.00                   │
│               3 │             103 │ 2023-03-25     │              10 │ 200.00                   │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘

SELECT * FROM high_price_sales;

┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│     sale_id     │    product_id   │    sale_date   │     quantity    │        total_price       │
├─────────────────┼─────────────────┼────────────────┼─────────────────┼──────────────────────────┤
│               2 │             102 │ 2023-02-20     │               3 │ 75.00                    │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Example-3: 明示的なエイリアスを使用した挿入 {#example-3-insert-with-explicit-alias}

この例では、VALUES 句でエイリアスを使用して、`employees` テーブルから `employee_history` テーブルへ、雇用日が '2023-02-01' より後の行を条件付きで挿入する方法を示します。

1. `employees` と `employee_history` の 2 つのテーブルを作成し、`employees` テーブルにサンプルの従業員データを挿入します。

    ```sql
    -- Create tables
    CREATE TABLE employees (
        employee_id INT,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        hire_date DATE
    );
    
    CREATE TABLE employee_history (
        employee_id INT,
        full_name VARCHAR(100),
        hire_date DATE
    );
    
    INSERT INTO employees (employee_id, first_name, last_name, hire_date)
    VALUES
        (1, 'John', 'Doe', '2023-01-01'),
        (2, 'Jane', 'Smith', '2023-02-01'),
        (3, 'Michael', 'Johnson', '2023-03-01');
    ```

2. エイリアスを使用した条件付き挿入により、`employees` テーブルから `employee_history` テーブルへレコードを転送し、雇用日が '2023-02-01' より後のものを対象に絞り込みます。

```sql
INSERT ALL
    WHEN hire_date >= '2023-02-01' THEN INTO employee_history
        VALUES (employee_id, full_name, hire_date) -- Insert with the alias 'full_name'
SELECT employee_id, CONCAT(first_name, ' ', last_name) AS full_name, hire_date -- Alias the concatenated full name as 'full_name'
FROM employees;

SELECT * FROM employee_history;

┌─────────────────────────────────────────────────────┐
│   employee_id   │     full_name    │    hire_date   │
│ Nullable(Int32) │ Nullable(String) │ Nullable(Date) │
├─────────────────┼──────────────────┼────────────────┤
│               2 │ Jane Smith       │ 2023-02-01     │
│               3 │ Michael Johnson  │ 2023-03-01     │
└─────────────────────────────────────────────────────┘
```