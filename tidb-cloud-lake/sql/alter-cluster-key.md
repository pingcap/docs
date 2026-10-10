---
title: ALTER CLUSTER KEY
summary: テーブルのクラスターキーを変更します。
---

# ALTER CLUSTER KEY

テーブルのクラスターキーを変更します。

関連情報: [DROP CLUSTER KEY](/tidb-cloud-lake/sql/drop-cluster-key.md)

## 構文 {#syntax}

```sql
ALTER TABLE [ IF EXISTS ] <name> CLUSTER BY ( <expr1> [ , <expr2> ... ] )
```

## 例 {#examples}

```sql
-- Create table
CREATE TABLE IF NOT EXISTS playground(a int, b int);

-- Add cluster key by columns
ALTER TABLE playground CLUSTER BY(b,a);

INSERT INTO playground VALUES(0,3),(1,1);
INSERT INTO playground VALUES(1,3),(2,1);
INSERT INTO playground VALUES(4,4);

SELECT * FROM playground ORDER BY b,a;
SELECT * FROM clustering_information('db1','playground');

-- Delete cluster key
ALTER TABLE playground DROP CLUSTER KEY;

-- Add cluster key by expressions
ALTER TABLE playground CLUSTER BY(rand()+a);
```