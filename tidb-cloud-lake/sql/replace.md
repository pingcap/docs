---
title: REPLACE
summary: REPLACE INTO 可以使用以下数据来源，向表中插入多行新数据；如果这些行已存在，则修改现有行。
---

# REPLACE

> **Note:**
>
> 于 v1.1.55 中引入。

`REPLACE INTO` 可以使用以下数据来源，向表中插入多行新数据；如果这些行已存在，则修改现有行：

- 直接值

- 查询结果

- stage 文件：{{{ .lake }}} 支持通过 `REPLACE INTO` 语句将 stage 文件中的数据替换到表中。这是通过 {{{ .lake }}} 查询 [查询 Stage 文件](/tidb-cloud-lake/sql/stage.md) 并随后将查询结果写入表中来实现的。

> **Tip:**
>
> {{{ .lake }}} 通过原子操作确保数据完整性。插入、修改、替换和删除操作要么全部成功，要么全部失败。

## 语法 {#syntax}

```sql
REPLACE INTO <table_name> [ ( <col_name> [ , ... ] ) ]
    ON (<CONFLICT KEY>) ...
```

当在表中找到指定的冲突键时，`REPLACE INTO` 会修改现有行；如果冲突键不存在，则插入新行。冲突键是表中的一个列或多个列的组合，用于唯一标识一行，并用于在执行 `REPLACE INTO` 语句时判断是插入新行还是修改现有行。示例如下：

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

## 分布式 REPLACE INTO {#distributed-replace-into}

`REPLACE INTO` 支持在集群环境中进行分布式执行。你可以通过将 `ENABLE_DISTRIBUTED_REPLACE_INTO` 设置为 `1` 来启用分布式 `REPLACE INTO`。这有助于提升集群环境中的数据加载性能和扩展性。

```sql
SET enable_distributed_replace_into = 1;
```

## 示例 {#examples}

### 示例 1：使用直接值进行替换 {#example-1-replace-with-direct-values}

以下示例使用直接值替换数据：

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

### 示例 2：使用查询结果进行替换 {#example-2-replace-with-query-results}

以下示例使用查询结果替换数据：

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

### 示例 3：使用 stage 文件进行替换 {#example-3-replace-with-staged-files}

以下示例演示如何使用 stage 文件中的数据替换表中的现有数据。

1. 创建一个名为 `sample` 的表

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

2. 设置一个包含示例数据的内部 stage

    首先，创建一个名为 `mystage` 的 stage。然后，将示例数据加载到该 stage 中。

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

3. 使用 `REPLACE INTO` 和 stage 中的 Parquet 文件替换现有数据

    > **Tip:**
    >
    > 你可以使用 [COPY INTO](/tidb-cloud-lake/sql/copy-into-table.md) 命令中提供的 `FILE_FORMAT` 和 `COPY_OPTIONS` 来指定文件格式以及各种与复制相关的设置。

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

4. 验证数据替换结果

现在，你可以查询 `sample` 表来查看变更：

```sql
SELECT * FROM sample;
```

结果应如下所示：

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