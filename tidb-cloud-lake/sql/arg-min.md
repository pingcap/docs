---
title: ARG_MIN
summary: 最小の `val` 値に対応する `arg` 値を計算します。`val` の最小値に対して異なる `arg` 値が複数ある場合は、最初に見つかった値を返します。
---

# ARG_MIN

最小の `val` 値に対応する `arg` 値を計算します。`val` の最小値に対して異なる `arg` 値が複数ある場合は、最初に見つかった値を返します。

## 構文 {#syntax}

```sql
ARG_MIN(<arg>, <val>)
```

## 引数 {#arguments}

| 引数 | 説明                                                                                       |
| --------- | ------------------------------------------------------------------------------------------------- |
| `<arg>`   | [{{{ .lake }}} がサポートする任意のデータ型](/tidb-cloud-lake/sql/data-types.md) の引数 |
| `<val>`   | [{{{ .lake }}} がサポートする任意のデータ型](/tidb-cloud-lake/sql/data-types.md) の値    |

## 戻り値の型 {#return-type}

最小の `val` 値に対応する `arg` 値です。

`arg` の型と一致します。

## 例 {#example}

`id`、`name`、`score` の各カラムを持つ `students` テーブルを作成し、いくつかのデータを挿入します。

```sql
CREATE TABLE students (
  id INT,
  name VARCHAR,
  score INT
);

INSERT INTO students (id, name, score) VALUES
  (1, 'Alice', 80),
  (2, 'Bob', 75),
  (3, 'Charlie', 90),
  (4, 'Dave', 80);
```

次に、ARG_MIN を使用して、最も低いスコアを持つ学生の名前を取得できます。

```sql
SELECT ARG_MIN(name, score) AS student_name
FROM students;
```

結果:

```sql
| student_name |
|--------------|
| Bob      |
```