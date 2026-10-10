---
title: UPDATE
summary: テーブル内の行を新しい値で更新します。必要に応じて、他のテーブルの値を使用できます。
---

# UPDATE

テーブル内の行を新しい値で更新します。必要に応じて、他のテーブルの値を使用できます。

> **Tip:**
>
> {{{ .lake }}} はアトミックな操作によってデータ整合性を保証します。insert、update、replace、delete は、完全に成功するか、完全に失敗するかのいずれかです。

## 構文 {#syntax}

```sql
UPDATE <target_table>
       SET <col_name> = <value> [ , <col_name> = <value> , ... ] -- Set new values
        [ FROM <additional_tables> ] -- Use values from other tables
        [ WHERE <condition> ] -- Filter rows
```

## `error_on_nondeterministic_update` 設定の構成 {#configuring-error-on-nondeterministic-update-setting}

`error_on_nondeterministic_update` 設定は、UPDATE 文が決定的な更新ルールなしに複数のソース行と結合するターゲット行を更新しようとしたときに、エラーを返すかどうかを制御します。

- `error_on_nondeterministic_update` = `true`（デフォルト）の場合: ターゲット行が複数のソース行に一致し、どの値を使用するかを選択する明確なルールがないとき、{{{ .lake }}} はエラーを返します。
- `error_on_nondeterministic_update` = `false` の場合: ターゲット行が複数のソース行と結合する場合でも UPDATE 文は実行されますが、最終的な更新結果は非決定的になる可能性があります。

例:

次のテーブルを考えます。

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

次の UPDATE 文を実行します。

```sql
UPDATE target
SET target.price = source.price
FROM source
WHERE target.id = source.id;
```

- `error_on_nondeterministic_update = true` の場合、このクエリは失敗します。これは、target の id = 2 が source 内の複数行に一致し、更新内容が曖昧になるためです。

  ```sql
  SET error_on_nondeterministic_update = 1;

  root@localhost:8000/default> UPDATE target
  SET target.price = source.price
  FROM source
  WHERE target.id = source.id;

  error: APIError: QueryFailed: [4001]multi rows from source match one and the same row in the target_table multi times
  ```

- `error_on_nondeterministic_update = false` の場合、更新は成功しますが、id = 2 の target.price は実行順序に応じて 399.99 または 349.99 のいずれかに更新される可能性があります。

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

## 例 {#examples}

次の例では、テーブル内の行を直接更新する方法と、別のテーブルの値を使って更新する方法の両方を示します。

まず **bookstore** テーブルを作成してサンプルデータを挿入し、その後、特定の行を直接更新します。次に、2 つ目のテーブル **book_updates** を使用して、**book_updates** の値に基づいて **bookstore** テーブルの行を更新します。

### ステップ 1: bookstore テーブルを作成して初期データを挿入する {#step-1-create-the-bookstore-table-and-insert-initial-data}

このステップでは、**bookstore** という名前のテーブルを作成し、サンプルの書籍データを格納します。

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

### ステップ 2: 更新前の bookstore テーブルを表示する {#step-2-view-the-bookstore-table-before-the-update}

ここで、**bookstore** テーブルの内容を確認して初期データを見てみましょう。

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

### ステップ 3: 単一の行を直接更新する {#step-3-update-a-single-row-directly}

次に、book_id `103` の書籍名を変更するために更新します。

```sql
UPDATE bookstore
SET book_name = 'The long answer (2nd)'
WHERE book_id = 103;
```

### ステップ 4: 更新後の bookstore テーブルを表示する {#step-4-view-the-bookstore-table-after-the-update}

それでは、テーブルを再度確認して、直接更新した結果を見てみましょう。

```sql
SELECT book_name FROM bookstore WHERE book_id=103;

┌───────────────────────┐
│       book_name       │
├───────────────────────┤
│ The long answer (2nd) │
└───────────────────────┘
```

### ステップ 5: 更新値用の新しいテーブルを作成する {#step-5-create-a-new-table-for-updated-values}

このステップでは、**book_updates** という 2 つ目のテーブルを作成します。このテーブルには、**bookstore** テーブルの更新に使用する新しい書籍名を格納します。

```sql
CREATE TABLE book_updates (
  book_id INT,
  new_book_name VARCHAR
);

INSERT INTO book_updates VALUES (103, 'The long answer (Revised)');
INSERT INTO book_updates VALUES (104, 'Wartime friends (Expanded Edition)');
```

### ステップ 6: book_updates の値を使って bookstore テーブルを更新する {#step-6-update-the-bookstore-table-using-values-from-book-updates}

ここでは、**book_updates** テーブルの値を使って **bookstore** テーブルを更新します。

```sql
UPDATE bookstore
SET book_name = book_updates.new_book_name
FROM book_updates
WHERE bookstore.book_id = book_updates.book_id;
```

### Step 7: 更新後の bookstore テーブルを確認する {#step-7-view-the-bookstore-table-after-the-update}

最後に、**bookstore** テーブルをもう一度確認し、**book_updates** の値を使って名前が更新されたことを確認します。

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