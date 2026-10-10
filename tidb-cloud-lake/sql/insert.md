---
title: INSERT
summary: 1 つ以上の行をテーブルに挿入します。
---

# INSERT

1 つ以上の行をテーブルに挿入します。

> **Tip:**
>
> {{{ .lake }}} は、アトミックな操作によってデータ整合性を保証します。挿入、更新、置換、削除は、完全に成功するか、完全に失敗するかのいずれかです。

関連情報: [INSERT (multi-table)](/tidb-cloud-lake/sql/insert-multi-table.md)

## 構文 {#syntax}

```sql
INSERT { OVERWRITE [ INTO ] | INTO } <table>
    -- Optionally specify the columns to insert into
    ( <column> [ , ... ] )
    -- Insertion options:
    {
        -- Directly insert values or default values
        VALUES ( <value> | DEFAULT ) [ , ... ] |
        -- Insert the result of a query
        SELECT ...
    }
```

| パラメータ | 説明 |
|--------------------|----------------------------------------------------------------------------------|
| `OVERWRITE [INTO]` | 挿入前に既存データを切り捨てるかどうかを示します。 |
| `VALUES`           | 特定の値、またはカラムのデフォルト値を直接挿入できます。 |

## 重要な注意事項 {#important-notes}

- `VALUES(...)` 式では、集約関数、外部 UDF、ウィンドウ関数は使用できません。

## 例 {#examples}

### Example-1: Insert Values with OVERWRITE {#example-1-insert-values-with-overwrite}

この例では、INSERT OVERWRITE 文を使用して employee テーブルを切り捨て、新しいデータを挿入します。これにより、既存のすべてのレコードが、ID 100 の従業員に対して指定された値で置き換えられます。

```sql
CREATE TABLE employee (
    employee_id INT,
    employee_name VARCHAR(50)
);

-- Inserting initial data into the employee table
INSERT INTO employee(employee_id, employee_name) VALUES
    (101, 'John Doe'),
    (102, 'Jane Smith');

-- Inserting new data with OVERWRITE
INSERT OVERWRITE employee VALUES (100, 'John Johnson');

-- Displaying the contents of the employee table
SELECT * FROM employee;

┌────────────────────────────────────┐
│   employee_id   │   employee_name  │
├─────────────────┼──────────────────┤
│             100 │ John Johnson     │
└────────────────────────────────────┘
```

### Example-2: Insert Query Results {#example-2-insert-query-results}

SELECT 文の結果を挿入する場合、カラムの対応付けは SELECT 句内の位置に従います。そのため、SELECT 文内のカラム数は、INSERT 先テーブルのカラム数以上である必要があります。SELECT 文と INSERT 先テーブルでカラムのデータ型が異なる場合は、必要に応じて型変換が実行されます。

```sql
-- Creating a table named 'employee_info' with three columns: 'employee_id', 'employee_name', and 'department'
CREATE TABLE employee_info (
    employee_id INT,
    employee_name VARCHAR(50),
    department VARCHAR(50)
);

-- Inserting a record into the 'employee_info' table
INSERT INTO employee_info VALUES ('101', 'John Doe', 'Marketing');

-- Creating a table named 'employee_data' with three columns: 'ID', 'Name', and 'Dept'
CREATE TABLE employee_data (
    ID INT,
    Name VARCHAR(50),
    Dept VARCHAR(50)
);

-- Inserting data from 'employee_info' into 'employee_data'
INSERT INTO employee_data SELECT * FROM employee_info;

-- Displaying the contents of the 'employee_data' table
SELECT * FROM employee_data;

┌───────────────────────────────────────────────────────┐
│        id       │       name       │       dept       │
├─────────────────┼──────────────────┼──────────────────┤
│             101 │ John Doe         │ Marketing        │
└───────────────────────────────────────────────────────┘
```

この例では、sales テーブルの情報を集約して、製品ごとの販売数量合計や売上高などの集計済み販売データを格納する "sales_summary" というサマリーテーブルを作成する方法を示します。

```sql
-- Creating a table for sales data
CREATE TABLE sales (
    product_id INT,
    quantity_sold INT,
    revenue DECIMAL(10, 2)
);

-- Inserting some sample sales data
INSERT INTO sales (product_id, quantity_sold, revenue) VALUES
    (1, 100, 500.00),
    (2, 150, 750.00),
    (1, 200, 1000.00),
    (3, 50, 250.00);

-- Creating a summary table to store aggregated sales data
CREATE TABLE sales_summary (
    product_id INT,
    total_quantity_sold INT,
    total_revenue DECIMAL(10, 2)
);

-- Inserting aggregated sales data into the summary table
INSERT INTO sales_summary (product_id, total_quantity_sold, total_revenue)
SELECT
    product_id,
    SUM(quantity_sold) AS total_quantity_sold,
    SUM(revenue) AS total_revenue
FROM
    sales
GROUP BY
    product_id;

-- Displaying the contents of the sales_summary table
SELECT * FROM sales_summary;

┌──────────────────────────────────────────────────────────────────┐
│    product_id   │ total_quantity_sold │       total_revenue      │
├─────────────────┼─────────────────────┼──────────────────────────┤
│               1 │                 300 │ 1500.00                  │
│               3 │                  50 │ 250.00                   │
│               2 │                 150 │ 750.00                   │
└──────────────────────────────────────────────────────────────────┘
```

### Example-3: Insert Default Values {#example-3-insert-default-values}

この例では、department や status などのカラムにデフォルト値を設定した "staff_records" というテーブルを作成し、その後データを挿入して、デフォルト値の使用方法を示します。

```sql
-- Creating a table 'staff_records' with columns 'employee_id', 'department', 'salary', and 'status' with default values
CREATE TABLE staff_records (
    employee_id INT NULL,
    department VARCHAR(50) DEFAULT 'HR',
    salary FLOAT,
    status VARCHAR(10) DEFAULT 'Active'
);

-- Inserting data into 'staff_records' with default values
INSERT INTO staff_records
VALUES
    (DEFAULT, DEFAULT, DEFAULT, DEFAULT),
    (101, DEFAULT, 50000.00, DEFAULT),
    (102, 'Finance', 60000.00, 'Inactive'),
    (103, 'Marketing', 70000.00, 'Active');

-- Displaying the contents of the 'staff_records' table
SELECT * FROM staff_records;

┌───────────────────────────────────────────────────────────────────────────┐
│   employee_id   │    department    │       salary      │      status      │
├─────────────────┼──────────────────┼───────────────────┼──────────────────┤
│            NULL │ HR               │              NULL │ Active           │
│             101 │ HR               │             50000 │ Active           │
│             102 │ Finance          │             60000 │ Inactive         │
│             103 │ Marketing        │             70000 │ Active           │
└───────────────────────────────────────────────────────────────────────────┘
```

### Example-4: stage 内のファイルを使った挿入 {#example-4-insert-with-staged-files}

{{{ .lake }}} では、INSERT INTO 文を使用して stage 内のファイルからテーブルにデータを挿入できます。これは、{{{ .lake }}} が [Query Staged Files](/tidb-cloud-lake/sql/stage.md) を実行し、そのクエリ結果をテーブルに取り込める機能によって実現されています。

1. `sample` という名前のテーブルを作成します。

    ```sql
    CREATE TABLE sample
    (
        id      INT,
        city    VARCHAR,
        score   INT,
        country VARCHAR DEFAULT 'China'
    );
    ```

2. サンプルデータを含む内部 stage を設定します

    `mystage` という名前の内部 stage を作成し、そこにサンプルデータを格納します。

    ```sql
    CREATE STAGE mystage;
    
    COPY INTO @mystage
    FROM
    (
        SELECT *
        FROM
        (
            VALUES
            (1, 'Chengdu', 80),
            (3, 'Chongqing', 90),
            (6, 'Hangzhou', 92),
            (9, 'Hong Kong', 88)
        )
    )
    FILE_FORMAT = (TYPE = PARQUET);
    ```

3. `INSERT INTO` を使用して、stage 内の Parquet ファイルからデータを挿入します

    > **Tip:**
    >
    > [COPY INTO](/tidb-cloud-lake/sql/copy-into-table.md) コマンドで利用できる FILE_FORMAT と COPY_OPTIONS を使用して、ファイル形式や各種コピー関連設定を指定できます。`purge` を `true` に設定した場合、元のファイルはデータ更新が成功したときにのみ削除されます。

    ```sql
    INSERT INTO sample
        (id, city, score)
    ON
        (Id)
    SELECT
        $1, $2, $3
    FROM
        @mystage
        (FILE_FORMAT => 'parquet');
    ```

4. データが挿入されたことを確認します

```sql
SELECT * FROM sample;
```

結果は次のようになります。

```sql
┌─────────────────────────────────────────────────────────────────────────┐
│        id       │       city       │      score      │      country     │
├─────────────────┼──────────────────┼─────────────────┼──────────────────┤
│               1 │ Chengdu          │              80 │ China            │
│               3 │ Chongqing        │              90 │ China            │
│               6 │ Hangzhou         │              92 │ China            │
│               9 │ Hong Kong        │              88 │ China            │
└─────────────────────────────────────────────────────────────────────────┘
```