---
title: system.numbers
summary: 此表包含一个名为 number 的单个 UInt64 列，其中包含从零开始的几乎所有自然数。
---

# system.numbers

此表包含一个名为 number 的单个 UInt64 列，其中包含从零开始的几乎所有自然数。

你可以将此表用于测试，或者在需要进行暴力搜索时使用。

对此表的读操作也会并行化。

用于测试。

```sql
SELECT avg(number) FROM numbers(100000000);
+-------------+
| avg(number) |
+-------------+
|  49999999.5 |
+-------------+
```