---
title: Bitmap
summary: BITMAP 用于存储无符号 64 位整数的成员信息，并支持快速集合运算（计数、并集、交集等）。SELECT 语句会显示二进制 blob，因此请使用 Bitmap Functions 来解析这些值。
---

# Bitmap

> **注意：**
>
> 于 v1.1.45 引入。

## 概述 {#overview}

`BITMAP` 用于存储无符号 64 位整数的成员信息，并支持快速集合运算（计数、并集、交集等）。`SELECT` 语句会显示二进制 blob，因此请使用 [Bitmap 函数](/tidb-cloud-lake/sql/bitmap-functions.md) 来解析这些值。

## 示例 {#examples}

### 构建 Bitmap {#build-bitmaps}

`TO_BITMAP` 接受逗号分隔的字符串或 `UINT64` 值（视为单个元素）。`TO_STRING` 会将 bitmap 序列化回可读文本。

```sql
SELECT
  TO_BITMAP('1,2,3')                     AS str_input,
  TO_STRING(TO_BITMAP('1,2,3'))          AS round_tripped,
  TO_STRING(TO_BITMAP(123))              AS from_uint64;
```

结果：

```
┌────────────────────────────────┬──────────────────────────────────┬────────────────┐
│ str_input                      │ round_tripped                    │ from_uint64    │
├────────────────────────────────┼──────────────────────────────────┼────────────────┤
│ <bitmap binary>                │ 1,2,3                            │ 123            │
└────────────────────────────────┴──────────────────────────────────┴────────────────┘
```

### 持久化 Bitmap {#persist-bitmaps}

在将数组插入表之前，使用 `BUILD_BITMAP` 将其转换为 bitmap。随后，`BITMAP_COUNT` 等聚合函数即可快速读取已存储的值。

```sql
CREATE TABLE user_visits (
  user_id INT,
  page_visits BITMAP
);

INSERT INTO user_visits VALUES
  (1, BUILD_BITMAP([2, 5, 8, 10])),
  (2, BUILD_BITMAP([3, 7, 9])),
  (3, BUILD_BITMAP([1, 4, 6, 10]));

SELECT
  user_id,
  BITMAP_COUNT(page_visits) AS distinct_pages,
  BITMAP_HAS_ALL(page_visits, BUILD_BITMAP([10])) AS saw_page_10
FROM user_visits;
```

结果：

```
┌────────┬────────────────┬─────────────┐
│ user_id │ distinct_pages │ saw_page_10 │
├────────┼────────────────┼─────────────┤
│      1 │              4 │        true │
│      2 │              3 │       false │
│      3 │              4 │        true │
└────────┴────────────────┴─────────────┘
```