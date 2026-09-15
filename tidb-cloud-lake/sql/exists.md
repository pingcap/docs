---
title: EXISTS
summary: exists 条件与子查询结合使用；如果子查询至少返回一行，则认为该条件“成立”。
---

# EXISTS

exists 条件与子查询结合使用；如果子查询至少返回一行，则认为该条件“成立”。

## 语法 {#syntax}

```sql
WHERE EXISTS ( <subquery> );
```

## 示例 {#examples}

```sql
SELECT number FROM numbers(5) AS A WHERE exists (SELECT * FROM numbers(3) WHERE number=1);
+--------+
| number |
+--------+
|      0 |
|      1 |
|      2 |
|      3 |
|      4 |
+--------+
```