---
title: UPDATE
summary: 使用新值修改表中的行，并可选择使用其他表中的值。
---

# UPDATE

使用新值修改表中的行，并可选择使用其他表中的值。

> **Tip:**
>
> {{{ .lake }}} 通过原子操作确保数据完整性。插入、修改、替换和删除要么全部成功，要么全部失败。

## 语法 {#syntax}

```sql
UPDATE <target_table>
       SET <col_name> = <value> [ , <col_name> = <value> , ... ] -- Set new values
        [ FROM <additional_tables> ] -- Use values from other tables
        [ WHERE <condition> ] -- Filter rows
```

## 配置 `error_on_nondeterministic_update` 设置 {#configuring-error-on-nondeterministic-update-setting}

`error_on_nondeterministic_update` 设置用于控制：当 UPDATE 语句尝试修改某个目标行，而该目标行关联到多个源行且没有确定性的修改规则时，是否返回错误。

- 当 `error_on_nondeterministic_update` = `true`（默认值）时：如果某个目标行匹配到多个源行，且没有明确规则来选择使用哪个值，{{{ .lake }}} 会返回错误。
- 当 `error_on_nondeterministic_update` = `false` 时：即使某个目标行关联到多个源行，UPDATE 语句仍会继续执行，但最终的修改结果可能是不确定的。

示例：

考虑以下表：

```sql
CREATE OR REPLACE TABLE target (
    id INT,
    price DECIMAL(10, 2)
);

INSERT INTO target VALUES
(1, 299.99),
(2, 399.99);

CREATE OR REPLACE TABLE source (
    id INT,
    price DECIMAL(10, 2)
);

INSERT INTO source VALUES
(1, 279.99),
(2, 399.99),
(2, 349.99);  -- Duplicate id in source
```

执行以下 UPDATE 语句：

```sql
UPDATE target
SET target.price = source.price
FROM source
WHERE target.id = source.id;
```

- 当 `error_on_nondeterministic_update = true` 时，此查询会失败，因为 target 中 id = 2 匹配了 source 中的多行，导致修改存在歧义。

  ```sql
  SET error_on_nondeterministic_update = 1;

  root@localhost:8000/default> UPDATE target
  SET target.price = source.price
  FROM source
  WHERE target.id = source.id;

  error: APIError: QueryFailed: [4001]multi rows from source match one and the same row in the target_table multi times
  ```

- 当 `error_on_nondeterministic_update = false` 时，修改会成功，但 id = 2 的 target.price 可能会被修改为 399.99 或 349.99，具体取决于执行顺序。

  ```sql
  SET error_on_nondeterministic_update = 0;

  root@localhost:8000/default> UPDATE target
  SET target.price = source.price
  FROM source
  WHERE target.id = source.id;

  ┌────────────────────────┐
  │ number of rows updated │
  ├────────────────────────┤
  │                      2 │
  └────────────────────────┘

  SELECT * FROM target;

  ┌────────────────────────────────────────────┐
  │        id       │           price          │
  ├─────────────────┼──────────────────────────┤
  │               1 │ 279.99                   │
  │               2 │ 399.99                   │
  └────────────────────────────────────────────┘
  ```

## 示例 {#examples}

以下示例演示了如何修改表中的行，包括直接修改以及使用另一个表中的值进行修改。

我们将先创建一个 **bookstore** 表并插入一些示例数据，然后直接修改其中的特定行。之后，我们会使用第二个表 **book_updates**，根据 **book_updates** 中的值来修改 **bookstore** 表中的行。

### 第 1 步：创建 bookstore 表并插入初始数据 {#step-1-create-the-bookstore-table-and-insert-initial-data}

在这一步中，我们创建一个名为 **bookstore** 的表，并用一些示例图书数据填充它。

```sql
CREATE TABLE bookstore (
  book_id INT,
  book_name VARCHAR
);

INSERT INTO bookstore VALUES (101, 'After the death of Don Juan');
INSERT INTO bookstore VALUES (102, 'Grown ups');
INSERT INTO bookstore VALUES (103, 'The long answer');
INSERT INTO bookstore VALUES (104, 'Wartime friends');
INSERT INTO bookstore VALUES (105, 'Deconstructed');
```

### 第 2 步：在修改前查看 bookstore 表 {#step-2-view-the-bookstore-table-before-the-update}

现在，我们可以检查 **bookstore** 表的内容，以查看初始数据。

```sql
SELECT * FROM bookstore;

┌───────────────────────────────────────────────┐
│     book_id     │          book_name          │
├─────────────────┼─────────────────────────────┤
│             102 │ Grown ups                   │
│             103 │ The long answer             │
│             101 │ After the death of Don Juan │
│             105 │ Deconstructed               │
│             104 │ Wartime friends             │
└───────────────────────────────────────────────┘
```

### 第 3 步：直接修改单行 {#step-3-update-a-single-row-directly}

接下来，我们将修改 book_id 为 `103` 的图书名称。

```sql
UPDATE bookstore
SET book_name = 'The long answer (2nd)'
WHERE book_id = 103;
```

### 第 4 步：在修改后查看 bookstore 表 {#step-4-view-the-bookstore-table-after-the-update}

现在，再次检查该表以查看直接修改后的结果。

```sql
SELECT book_name FROM bookstore WHERE book_id=103;

┌───────────────────────┐
│       book_name       │
├───────────────────────┤
│ The long answer (2nd) │
└───────────────────────┘
```

### 第 5 步：创建一个用于存放更新值的新表 {#step-5-create-a-new-table-for-updated-values}

在这一步中，我们创建第二个表 **book_updates**，其中保存了更新后的图书名称，稍后将用它来修改 **bookstore** 表。

```sql
CREATE TABLE book_updates (
  book_id INT,
  new_book_name VARCHAR
);

INSERT INTO book_updates VALUES (103, 'The long answer (Revised)');
INSERT INTO book_updates VALUES (104, 'Wartime friends (Expanded Edition)');
```

### 第 6 步：使用 book_updates 中的值修改 bookstore 表 {#step-6-update-the-bookstore-table-using-values-from-book-updates}

现在，我们将使用 **book_updates** 表中的值来修改 **bookstore** 表。

```sql
UPDATE bookstore
SET book_name = book_updates.new_book_name
FROM book_updates
WHERE bookstore.book_id = book_updates.book_id;
```

### 第 7 步：查看修改后的 bookstore 表 {#step-7-view-the-bookstore-table-after-the-update}

最后，我们再次检查 **bookstore** 表，以确认名称已使用 **book_updates** 中的值完成修改。

```sql
SELECT * FROM bookstore;

┌──────────────────────────────────────────────────────┐
│     book_id     │              book_name             │
├─────────────────┼────────────────────────────────────┤
│             105 │ Deconstructed                      │
│             101 │ After the death of Don Juan        │
│             102 │ Grown ups                          │
│             104 │ Wartime friends (Expanded Edition) │
│             103 │ The long answer (Revised)          │
└──────────────────────────────────────────────────────┘
```