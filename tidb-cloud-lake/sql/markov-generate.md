---
title: MARKOV_GENERATE
---

Using the model trained by [MARKOV_TRAIN](../07-aggregate-functions/aggregate-markov-train.md) to anonymize the dataset.

## Syntax

```sql
MARKOV_GENERATE( <model>, <params>, <seed>, <determinator> )
```

## Arguments

| Arguments | Description |
| ----------- | ----------- |
| `model` | The return model of markov_train |
| `params`| Json string: `{"order": 5, "sliding_window_size": 8}` <br/> order：order of markov model to generate strings，<br/> size of a sliding window in a source string - its hash is used as a seed for RNG in markov model |
| `seed` | seed |
| `determinator`| Source string |

## Return Type

String.

## Examples

Generate multiple PII-like columns (name + email) from small seed sets:

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
