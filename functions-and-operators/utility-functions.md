---
title: Utility Functions
summary: This document introduces utility functions supported in TiDB.
---

# Utility Functions

This document introduces utility functions supported in TiDB

## `FORMAT_BYTES()`

The `FORMAT_BYTES()` function formats a number of bytes into a human-readable format.

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

The `FORMAT_NANO_TIME()` function formats a number of nanoseconds as a human-readable number.

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
