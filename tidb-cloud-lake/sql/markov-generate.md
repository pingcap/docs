---
title: MARKOV_GENERATE
summary: 使用由 MARKOV_TRAIN 训练得到的模型对数据集进行匿名化。
---

# MARKOV_GENERATE

使用由 [MARKOV_TRAIN](/tidb-cloud-lake/sql/markov-train.md) 训练得到的模型对数据集进行匿名化。

## 语法 {#syntax}

```sql
MARKOV_GENERATE( <model>, <params>, <seed>, <determinator> )
```

## 参数 {#arguments}

| 参数 | 描述 |
| ----------- | ----------- |
| `model` | markov_train 返回的模型 |
| `params`| Json 字符串：`{"order": 5, "sliding_window_size": 8}` <br/> order：用于生成字符串的 markov model 的阶数，<br/> 源字符串中滑动窗口的大小——其哈希值会作为 markov model 中 RNG 的 seed |
| `seed` | seed |
| `determinator`| 源字符串 |

## 返回类型 {#return-type}

字符串。

## 示例 {#examples}

从较小的数据填充集合中生成多个类似 PII 的列（name + email）：

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