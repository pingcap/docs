---
title: REFRESH INVERTED INDEX
summary: "{{{ .lake }}} は、新しいデータが書き込まれるたびに `SYNC` モードで inverted index を自動的に更新します。`REFRESH INVERTED INDEX` は主に、インデックスが宣言される前から存在していた行をバックフィルするために使用します。"
---

# REFRESH INVERTED INDEX

{{{ .lake }}} は、新しいデータが書き込まれるたびに `SYNC` モードで inverted index を自動的に更新します。`REFRESH INVERTED INDEX` は主に、インデックスが宣言される前から存在していた行をバックフィルするために使用します。

## 構文 {#syntax}

```sql
REFRESH INVERTED INDEX <index> ON [<database>.]<table> [LIMIT <limit>]
```

| パラメータ | 説明 |
|-----------|----------------------------------------------------------------------------------------------------------------------------------|
| `<limit>` | インデックス更新時に処理する行数の最大値を指定します。指定しない場合は、テーブル内のすべての行が処理されます。 |

## 例 {#examples}

```sql
-- Existing table with data loaded before the index was declared
CREATE TABLE IF NOT EXISTS customer_feedback(id INT, body STRING);
INSERT INTO customer_feedback VALUES
  (1, 'Great coffee beans'),
  (2, 'Needs fresh roasting');

-- Create the inverted index afterward
CREATE INVERTED INDEX customer_feedback_idx ON customer_feedback(body);

-- Backfill historical rows so the index covers earlier inserts
REFRESH INVERTED INDEX customer_feedback_idx ON customer_feedback;

-- Future inserts refresh automatically in SYNC mode
```