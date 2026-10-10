---
title: EXISTS
summary: exists 条件はサブクエリと組み合わせて使用され、サブクエリが少なくとも 1 行を返す場合に「満たされる」と見なされます。
---

# EXISTS

exists 条件はサブクエリと組み合わせて使用され、サブクエリが少なくとも 1 行を返す場合に「満たされる」と見なされます。

## 構文 {#syntax}

```sql
WHERE EXISTS ( <subquery> );
```

## 例 {#examples}

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