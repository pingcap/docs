---
title: MARKOV_GENERATE
summary: MARKOV_TRAIN で学習したモデルを使用してデータセットを匿名化します。
---

# MARKOV_GENERATE

[MARKOV_TRAIN](/tidb-cloud-lake/sql/markov-train.md) で学習したモデルを使用してデータセットを匿名化します。

## 構文 {#syntax}

```sql
MARKOV_GENERATE( <model>, <params>, <seed>, <determinator> )
```

## 引数 {#arguments}

| 引数 | 説明 |
| ----------- | ----------- |
| `model` | markov_train の戻りモデル |
| `params`| Json 文字列: `{"order": 5, "sliding_window_size": 8}` <br/> order：文字列生成に使用する markov モデルの次数。<br/> ソース文字列内のスライディングウィンドウのサイズ。このハッシュ値が markov モデルの RNG の seed として使用されます |
| `seed` | seed |
| `determinator`| ソース文字列 |

## 戻り値の型 {#return-type}

文字列。

## 例 {#examples}

小さな seed セットから、複数の PII 風カラム（name + email）を生成します。

```sql
-- 1) Train separate models on names and emails (PII text)
CREATE TABLE markov_name_model AS
SELECT markov_train(name) AS model
FROM (
  VALUES ('Alice Johnson'),('Bob Smith'),('Carol Davis'),('David Miller'),('Emma Wilson'),
         ('Frank Brown'),('Grace Lee'),('Henry Clark'),('Irene Torres'),('Jack White')
) AS t(name);

CREATE TABLE markov_email_model AS
SELECT markov_train(email) AS model
FROM (
  VALUES ('alice.johnson@gmail.com'),('bob.smith@yahoo.com'),('carol.davis@outlook.com'),
         ('david.miller@example.com'),('emma.wilson@example.com'),('frank.brown@gmail.com'),
         ('grace.lee@example.com'),('henry.clark@example.com'),('irene.torres@example.com'),
         ('jack.white@example.com')
) AS t(email);

-- 2) Generate synthetic name + email pairs; seed keeps it reproducible
SELECT
  markov_generate(n.model, '{"order":3,"sliding_window_size":12}', 3030, CONCAT('orig_', number))                AS fake_name,
  markov_generate(e.model, '{"order":3,"sliding_window_size":12}', 3030, CONCAT('orig_', number, '@example.com')) AS fake_email
FROM numbers(6)
JOIN markov_name_model n
JOIN markov_email_model e
LIMIT 6;
-- Sample output
+----------------+-------------------------+
| fake_name      | fake_email              |
+----------------+-------------------------+
| Frank Brown    | henry.clark@example     |
| Grace Johnso   | quinn.foster@example    |
| Rachel         | paul.adams@example      |
| Carol David    | olivia.baker@example    |
| Jack White     | frank.brown@gmail.com   |
| Noah Harris    | race.johnson@example    |
+----------------+-------------------------+
```