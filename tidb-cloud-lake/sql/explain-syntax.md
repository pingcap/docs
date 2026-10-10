---
title: EXPLAIN SYNTAX
summary: 整形された SQL コードを出力します。このコマンドは SQL フォーマッタとして機能し、コードを読みやすくします。
---

# EXPLAIN SYNTAX

整形された SQL コードを出力します。このコマンドは SQL フォーマッタとして機能し、コードを読みやすくします。

## 構文 {#syntax}

```sql
EXPLAIN SYNTAX <statement>
```

## 例 {#examples}

```sql
EXPLAIN SYNTAX select a, sum(b) as sum from t1 where a in (1, 2) and b > 0 and b < 100 group by a order by a;

 ----
 SELECT
     a,
     sum(b) AS sum
 FROM
     t1
 WHERE
     a IN (1, 2)
     AND b > 0
     AND b < 100
 GROUP BY a
 ORDER BY a
```

```sql
EXPLAIN SYNTAX copy into 's3://mybucket/data.csv' from t1 file_format = ( type = CSV field_delimiter = ',' record_delimiter = '\n' skip_header = 1);

 ----
 COPY
 INTO 's3://mybucket/data.csv'
 FROM t1
 FILE_FORMAT = (
     field_delimiter = ",",
     record_delimiter = "\n",
     skip_header = "1",
     type = "CSV"
 )
```