---
title: Boolean
summary: 基本逻辑数据类型。
---

# Boolean

## 概述 {#overview}

`BOOLEAN`（别名 `BOOL`）表示 `TRUE` 或 `FALSE`，并且始终使用一个字节的存储空间。在可能的情况下，数值和字符串输入会自动强制转换为布尔值。

| 输入类型 | 转换为 TRUE | 转换为 FALSE | 说明 |
|------------|-----------------|-------------------|-------|
| 数值    | 任何非零值     | 0                 | 负数会转换为 TRUE。 |
| 字符串     | `TRUE`           | `FALSE`           | 不区分大小写；其他文本无法转换。 |

## 示例 {#examples}

```sql
SELECT
  0::BOOLEAN            AS zero_is_false,
  42::BOOLEAN           AS nonzero_is_true,
  'True'::BOOLEAN       AS string_true,
  'false'::BOOLEAN      AS string_false;
```

结果：

```
┌───────────────┬──────────────────┬───────────────┬────────────────┐
│ zero_is_false │ nonzero_is_true  │ string_true   │ string_false   │
├───────────────┼──────────────────┼───────────────┼────────────────┤
│ false         │ true             │ true          │ false          │
└───────────────┴──────────────────┴───────────────┴────────────────┘
```

```sql
-- Casting unsupported text raises an error.
SELECT 'yes'::BOOLEAN;
```

结果：

```
ERROR 1105 (HY000): QueryFailed: [1006]cannot parse to type `BOOLEAN` while evaluating function `to_boolean('yes')` in expr `CAST('yes' AS Boolean)`
```