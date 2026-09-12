---
title: EXPLAIN SYNTAX
summary: 输出格式化后的 SQL 代码。该命令可用作 SQL 格式化工具，使你的代码更易于阅读。
---

# EXPLAIN SYNTAX

输出格式化后的 SQL 代码。该命令可用作 SQL 格式化工具，使你的代码更易于阅读。

## 语法 {#syntax}

```sql
EXPLAIN SYNTAX <statement>
```

## 示例 {#examples}

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