---
title: REPLACE
summary: REPLACE INTO は、以下のデータソースを使用して、テーブルに複数の新しい行を挿入することも、行がすでに存在する場合は既存の行を更新することもできます。
---

# REPLACE

> **Note:**
>
> v1.1.55 で導入されました。

REPLACE INTO は、以下のデータソースを使用して、テーブルに複数の新しい行を挿入することも、行がすでに存在する場合は既存の行を更新することもできます。

- 直接値

- クエリ結果

- stage 上のファイル: {{{ .lake }}} では、REPLACE INTO 文を使用して stage 上のファイルからテーブル内のデータを置き換えることができます。これは、{{{ .lake }}} の [Query Staged Files](/tidb-cloud-lake/sql/stage.md) 機能を使用して stage 上のファイルをクエリし、その結果をテーブルに取り込むことで実現されます。

> **Tip:**
>
> {{{ .lake }}} は、アトミックな操作によってデータ整合性を保証します。挿入、更新、置換、削除は、すべて完全に成功するか、完全に失敗するかのいずれかです。

## 構文 {#syntax}

```sql
REPLACE INTO <table_name> [ ( <col_name> [ , ... ] ) ]
    ON (<CONFLICT KEY>) ...
```

REPLACE INTO は、指定した conflict key がテーブル内で見つかった場合は既存の行を更新し、conflict key が存在しない場合は新しい行を挿入します。conflict key とは、テーブル内の行を一意に識別するカラム、または複数カラムの組み合わせであり、REPLACE INTO 文を使用して新しい行を挿入するか既存の行を更新するかを判断するために使用されます。以下の例を参照してください。

```sql
CREATE TABLE employees (
    employee_id INT,
    employee_name VARCHAR(100),
    employee_salary DECIMAL(10, 2),
    employee_email VARCHAR(255)
);

-- This REPLACE INTO inserts a new row
REPLACE INTO employees (employee_id, employee_name, employee_salary, employee_email)
ON (employee_email)
VALUES (123, 'John Doe', 50000, 'john.doe@example.com');

-- This REPLACE INTO updates the inserted row
REPLACE INTO employees (employee_id, employee_name, employee_salary, employee_email)
ON (employee_email)
VALUES (123, 'John Doe', 60000, 'john.doe@example.com');
```

## 分散 REPLACE INTO {#distributed-replace-into}

`REPLACE INTO` は、クラスター環境での分散実行をサポートしています。分散 REPLACE INTO を有効にするには、ENABLE_DISTRIBUTED_REPLACE_INTO を 1 に設定します。これにより、クラスター環境でのデータロード (load) のパフォーマンスとスケーラビリティを向上させることができます。

```sql
SET enable_distributed_replace_into = 1;
```

## 例 {#examples}

### 例 1: 直接値による置換 {#example-1-replace-with-direct-values}

この例では、直接値を使用してデータを置き換えます。

```sql
CREATE TABLE employees(id INT, name VARCHAR, salary INT);

REPLACE INTO employees (id, name, salary) ON (id)
VALUES (1, 'John Doe', 50000);

SELECT  * FROM Employees;
+------+----------+--------+
| id   | name     | salary |
+------+----------+--------+
| 1    | John Doe |  50000 |
+------+----------+--------+
```

### 例 2: クエリ結果による置換 {#example-2-replace-with-query-results}

この例では、クエリ結果を使用してデータを置き換えます。

```sql
CREATE TABLE employees(id INT, name VARCHAR, salary INT);

CREATE TABLE temp_employees(id INT, name VARCHAR, salary INT);

INSERT INTO temp_employees (id, name, salary) VALUES (1, 'John Doe', 60000);

REPLACE INTO employees (id, name, salary) ON (id)
SELECT id, name, salary FROM temp_employees WHERE id = 1;

SELECT  * FROM Employees;
+------+----------+--------+
| id   | name     | salary |
+------+----------+--------+
|    1 | John Doe |  60000 |
+------+----------+--------+
```

### 例 3: stage 上のファイルによる置換 {#example-3-replace-with-staged-files}

この例では、stage 上のファイルのデータを使用して、テーブル内の既存データを置き換える方法を示します。

1. `sample` という名前のテーブルを作成します

    ```sql
    CREATE TABLE sample
    (
        id      INT,
        city    VARCHAR,
        score   INT,
        country VARCHAR DEFAULT 'China'
    );
    
    INSERT INTO sample
        (id, city, score)
    VALUES
        (1, 'Chengdu', 66);
    ```

2. サンプルデータを含む内部 stage を設定します

    まず、`mystage` という名前の stage を作成します。次に、この stage にサンプルデータをロードします。

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

3. `REPLACE INTO` を使用して、stage 上の Parquet ファイルから既存データを置き換えます

    > **Tip:**
    >
    > [COPY INTO](/tidb-cloud-lake/sql/copy-into-table.md) コマンドで使用できる FILE_FORMAT と COPY_OPTIONS を使って、ファイル形式や各種 copy 関連設定を指定できます。

    ```sql
    REPLACE INTO sample
        (id, city, score)
    ON
        (Id)
    SELECT
        $1, $2, $3
    FROM
        @mystage
        (FILE_FORMAT => 'parquet');
    ```

4. データの置換を確認します

これで、sample テーブルをクエリして変更内容を確認できます。

```sql
SELECT * FROM sample;
```

結果は次のようになります。

```sql
┌─────────────────────────────────────────────────────────────────────────┐
│        id       │       city       │      score      │      country     │
│ Nullable(Int32) │ Nullable(String) │ Nullable(Int32) │ Nullable(String) │
├─────────────────┼──────────────────┼─────────────────┼──────────────────┤
│               1 │ Chengdu          │              80 │ China            │
│               3 │ Chongqing        │              90 │ China            │
│               6 │ Hangzhou         │              92 │ China            │
│               9 │ Hong Kong        │              88 │ China            │
└─────────────────────────────────────────────────────────────────────────┘
```