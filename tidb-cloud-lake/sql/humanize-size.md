---
title: HUMANIZE_SIZE
summary: 返回带有后缀（KiB、MiB 等）的可读大小。
---

# HUMANIZE_SIZE

返回带有后缀（KiB、MiB 等）的可读大小。

## 语法 {#syntax}

```sql
HUMANIZE_SIZE(x);
```

## 参数 {#arguments}

| 参数 | 描述         |
|-----------|----------------------------|
| x         | 数值大小。        |

## 返回类型 {#return-type}

字符串。

## 示例 {#examples}

```sql
SELECT HUMANIZE_SIZE(1024 * 1024)
+-------------------------+
| HUMANIZE_SIZE((1024 * 1024)) |
+-------------------------+
| 1 MiB                    |
+-------------------------+
```