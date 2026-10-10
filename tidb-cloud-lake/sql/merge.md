---
title: MERGE
summary: 指定したソースのデータを使用し、ステートメント内で指定された条件および一致条件に従って、ターゲットテーブル内の行に対して INSERT、UPDATE、または DELETE 操作を実行します。
---

# MERGE

指定したソースのデータを使用し、ステートメント内で指定された条件および一致条件に従って、ターゲットテーブル内の行に対して **INSERT**、**UPDATE**、または **DELETE** 操作を実行します。

サブクエリにできるデータソースは、JOIN 式を介してターゲットデータに関連付けられます。この式は、ソース内の各行がターゲットテーブル内で一致する行を見つけられるかどうかを評価し、その後、次の実行ステップでどの種類の句（MATCHED または NOT MATCHED）に進むべきかを決定します。

![Alt text](/media/tidb-cloud-lake/merge-into-single-clause.jpeg)

MERGE ステートメントには通常、MATCHED 句および / または NOT MATCHED 句が含まれ、一致した場合と一致しなかった場合を {{{ .lake }}} がどのように処理するかを指示します。MATCHED 句では、ターゲットテーブルに対して **UPDATE** または **DELETE** 操作を実行するかを選択できます。一方、NOT MATCHED 句で使用できるのは **INSERT** です。

## 複数の MATCHED 句と NOT MATCHED 句 {#multiple-matched-not-matched-clauses}

MERGE ステートメントには複数の MATCHED 句および / または NOT MATCHED 句を含めることができ、MERGE 操作中に満たされた条件に応じて異なるアクションを柔軟に指定できます。

![Alt text](/media/tidb-cloud-lake/merge-into-multi-clause.jpeg)

MERGE ステートメントに複数の MATCHED 句が含まれる場合、最後の句を除く各句には条件を指定する必要があります。これらの条件は、関連する操作が実行される基準を決定します。{{{ .lake }}} は指定された順序で条件を評価します。いずれかの条件が満たされると、指定された操作を実行し、残りの MATCHED 句をスキップして、ソース内の次の行に進みます。MERGE ステートメントに複数の NOT MATCHED 句も含まれる場合、{{{ .lake }}} は同様の方法で処理します。

## 構文 {#syntax}

```sql
MERGE INTO <target_table>
    USING (SELECT ... ) [AS] <alias> ON <join_expr> { matchedClause | notMatchedClause } [ ... ]

matchedClause ::=
  WHEN MATCHED [ AND <condition> ] THEN
  {
    UPDATE SET <col_name> = <expr> [ , <col_name2> = <expr2> ... ] |
    UPDATE * |
    DELETE  /* Removes matched rows from the target table */
  }

notMatchedClause ::=
  WHEN NOT MATCHED [ AND <condition> ] THEN
  { INSERT ( <col_name> [ , <col_name2> ... ] ) VALUES ( <expr> [ , ... ] ) | INSERT * }
```

| Parameter | 説明 |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| UPDATE \* | ソース内の対応する行の値を使用して、ターゲットテーブル内の一致した行のすべてのカラムを更新します。更新処理ではカラム名に基づいて対応付けが行われるため、ソースとターゲットのカラム名が一致している必要があります（順序は異なっていてもかまいません）。 |
| INSERT \* | ソース行の値を使用して、ターゲットテーブルに新しい行を挿入します。 |
| DELETE    | ターゲットテーブルから一致した行を削除します。これは、データのクリーンアップ、古くなったレコードの削除、またはソースデータに基づく条件付き削除ロジックの実装に使用できる強力な操作です。 |

## 出力 {#output}

MERGE は、データマージ結果の概要を次のカラムで返します。

| カラム                  | 説明                                          |
| ----------------------- | ---------------------------------------------------- |
| number of rows inserted | ターゲットテーブルに追加された新しい行の数。         |
| number of rows updated  | ターゲットテーブル内で変更された既存の行の数。 |
| number of rows deleted  | ターゲットテーブルから削除された行の数。         |

## 例 {#examples}

### 例 1: 複数の MATCHED 句を使用したマージ {#example-1-merge-with-multiple-matched-clauses}

この例では、MERGE を使用して `employees` から `salaries` へ従業員データを同期し、指定した条件に基づいて給与情報の挿入と更新を行います。

```sql
-- Create the 'employees' table as the source for merging
CREATE TABLE employees (
    employee_id INT,
    employee_name VARCHAR(255),
    department VARCHAR(255)
);

-- Create the 'salaries' table as the target for merging
CREATE TABLE salaries (
    employee_id INT,
    salary DECIMAL(10, 2)
);

-- Insert initial employee data
INSERT INTO employees VALUES
    (1, 'Alice', 'HR'),
    (2, 'Bob', 'IT'),
    (3, 'Charlie', 'Finance'),
    (4, 'David', 'HR');

-- Insert initial salary data
INSERT INTO salaries VALUES
    (1, 50000.00),
    (2, 60000.00);

-- Enable MERGE INTO

-- Merge data into 'salaries' based on employee details from 'employees'
MERGE INTO salaries
    USING (SELECT * FROM employees) AS employees
    ON salaries.employee_id = employees.employee_id
    WHEN MATCHED AND employees.department = 'HR' THEN
        UPDATE SET
            salaries.salary = salaries.salary + 1000.00
    WHEN MATCHED THEN
        UPDATE SET
            salaries.salary = salaries.salary + 500.00
    WHEN NOT MATCHED THEN
        INSERT (employee_id, salary)
            VALUES (employees.employee_id, 55000.00);

┌──────────────────────────────────────────────────┐
│ number of rows inserted │ number of rows updated │
├─────────────────────────┼────────────────────────┤
│                      2  │                      2 │
└──────────────────────────────────────────────────┘

-- Retrieve all records from the 'salaries' table after merging
SELECT * FROM salaries;

┌────────────────────────────────────────────┐
│   employee_id   │          salary          │
├─────────────────┼──────────────────────────┤
│               3 │ 55000.00                 │
│               4 │ 55000.00                 │
│               1 │ 51000.00                 │
│               2 │ 60500.00                 │
└────────────────────────────────────────────┘
```

### 例 2: UPDATE \* と INSERT \* を使用したマージ {#example-2-merge-with-update-insert}

この例では、MERGE を使用して target_table と source_table の間でデータを同期し、一致する行をソースの値で更新し、一致しない行を挿入します。

```sql
-- Create the target table target_table
CREATE TABLE target_table (
    ID INT,
    Name VARCHAR(50),
    Age INT,
    City VARCHAR(50)
);

-- Insert initial data into target_table
INSERT INTO target_table (ID, Name, Age, City)
VALUES
    (1, 'Alice', 25, 'Toronto'),
    (2, 'Bob', 30, 'Vancouver'),
    (3, 'Carol', 28, 'Montreal');

-- Create the source table source_table
CREATE TABLE source_table (
    ID INT,
    Name VARCHAR(50),
    Age INT,
    City VARCHAR(50)
);

-- Insert initial data into source_table
INSERT INTO source_table (ID, Name, Age, City)
VALUES
    (1, 'David', 27, 'Calgary'),
    (2, 'Emma', 29, 'Ottawa'),
    (4, 'Frank', 32, 'Edmonton');

-- Enable MERGE INTO

-- Merge data from source_table into target_table
MERGE INTO target_table AS T
    USING (SELECT * FROM source_table) AS S
    ON T.ID = S.ID
    WHEN MATCHED THEN
        UPDATE *
    WHEN NOT MATCHED THEN
    INSERT *;

┌──────────────────────────────────────────────────┐
│ number of rows inserted │ number of rows updated │
├─────────────────────────┼────────────────────────┤
│                      1  │                      2 │
└──────────────────────────────────────────────────┘

-- Retrieve all records from the 'target_table' after merging
SELECT * FROM target_table order by ID;

┌─────────────────────────────────────────────────────────────────────────┐
│        id       │       name       │       age       │       city       │
├─────────────────┼──────────────────┼─────────────────┼──────────────────┤
│               1 │ David            │              27 │ Calgary          │
│               2 │ Emma             │              29 │ Ottawa           │
│               3 │ Carol            │              28 │ Montreal         │
│               4 │ Frank            │              32 │ Edmonton         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 例 3: DELETE 操作を伴うマージ {#example-3-merge-with-delete-operation}

この例では、ソーステーブルの特定の条件に基づいて、MERGE を使用してターゲットテーブルからレコードを削除する方法を示します。

```sql
-- Create the customers table (target)
CREATE TABLE customers (
    customer_id INT,
    customer_name VARCHAR(50),
    status VARCHAR(20),
    last_purchase_date DATE
);

-- Insert initial customer data
INSERT INTO customers VALUES
    (101, 'John Smith', 'Active', '2023-01-15'),
    (102, 'Emma Johnson', 'Active', '2023-02-20'),
    (103, 'Michael Brown', 'Inactive', '2022-11-05'),
    (104, 'Sarah Wilson', 'Active', '2023-03-10'),
    (105, 'David Lee', 'Inactive', '2022-09-30');

-- Create the removals table (source with customers to be removed)
CREATE TABLE removals (
    customer_id INT,
    removal_reason VARCHAR(50),
    removal_date DATE
);

-- Insert data for customers to be removed
INSERT INTO removals VALUES
    (103, 'Account Closed', '2023-04-01'),
    (105, 'Customer Request', '2023-04-05');

-- Enable MERGE INTO

-- Use MERGE to delete inactive customers that appear in the removals table
MERGE INTO customers AS c
    USING removals AS r
    ON c.customer_id = r.customer_id
    WHEN MATCHED AND c.status = 'Inactive' THEN
        DELETE;

┌────────────────────────┐
│ number of rows deleted │
├────────────────────────┤
│                     2  │
└────────────────────────┘
```