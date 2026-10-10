---
title: HUMANIZE_SIZE
summary: 接尾辞 (KiB、MiB など) 付きの読みやすいサイズを返します。
---

# HUMANIZE_SIZE

接尾辞 (KiB、MiB など) 付きの読みやすいサイズを返します。

## 構文 {#syntax}

```sql
HUMANIZE_SIZE(x);
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|----------------------------|
| x         | 数値のサイズ。        |

## 戻り値の型 {#return-type}

文字列。

## 例 {#examples}

```sql
SELECT HUMANIZE_SIZE(1024 * 1024)
+-------------------------+
| HUMANIZE_SIZE((1024 * 1024)) |
+-------------------------+
| 1 MiB                    |
+-------------------------+
```