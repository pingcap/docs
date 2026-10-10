---
title: SHOW TABLE FUNCTIONS
summary: 現在サポートされているテーブル関数の一覧を表示します。
---

# SHOW TABLE FUNCTIONS

現在サポートされているテーブル関数の一覧を表示します。

## 構文 {#syntax}

```sql
SHOW TABLE_FUNCTIONS [LIKE '<pattern>' | WHERE <expr>] | [LIMIT <limit>]
```

## 例 {#example}

```sql
SHOW TABLE_FUNCTIONS;
+------------------------+
| name                   |
+------------------------+
| numbers                |
| numbers_mt             |
| numbers_local          |
| fuse_snapshot          |
| fuse_segment           |
| fuse_block             |
| fuse_statistic         |
| clustering_information |
| sync_crash_me          |
| async_crash_me         |
| infer_schema           |
+------------------------+
```

`"number"` で始まるテーブル関数を表示します。

```sql
SHOW TABLE_FUNCTIONS LIKE 'number%';
+---------------+
| name          |
+---------------+
| numbers       |
| numbers_mt    |
| numbers_local |
+---------------+
```

`WHERE` を使用して `"number"` で始まるテーブル関数を表示します。

```sql
SHOW TABLE_FUNCTIONS WHERE name LIKE 'number%';
+---------------+
| name          |
+---------------+
| numbers       |
| numbers_mt    |
| numbers_local |
+---------------+
```