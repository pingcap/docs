---
title: Utility Functions
summary: 本文档介绍了 TiDB 支持的实用函数。
---

# Utility Functions

本文档介绍了 TiDB 支持的实用函数，旨在简化常见数据转换，以提升可读性。

## `FORMAT_BYTES()`

`FORMAT_BYTES()` 函数将字节数转换为易于阅读的格式。

```sql
SELECT FORMAT_BYTES(10*1024*1024);
```

```
+----------------------------+
| FORMAT_BYTES(10*1024*1024) |
+----------------------------+
| 10.00 MiB                  |
+----------------------------+
1 row in set (0.001 sec)
```

## `FORMAT_NANO_TIME()`

`FORMAT_NANO_TIME()` 函数将纳秒数转换为易于阅读的时间格式。

```sql
SELECT FORMAT_NANO_TIME(1000000);
```

```
+---------------------------+
| FORMAT_NANO_TIME(1000000) |
+---------------------------+
| 1.00 ms                   |
+---------------------------+
1 row in set (0.001 sec)
```