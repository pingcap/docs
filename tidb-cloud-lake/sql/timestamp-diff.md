---
title: TIMESTAMP_DIFF
summary: 计算两个时间戳之间的差值，并将结果作为 INTERVAL 返回。
---

# TIMESTAMP_DIFF

计算两个时间戳之间的差值，并将结果作为 INTERVAL 返回。

## 语法 {#syntax}

```sql
TIMESTAMP_DIFF(<timestamp1>, <timestamp2>)
```

## 返回类型 {#return-type}

INTERVAL（格式为 `hours:minutes:seconds`）。

## 示例 {#examples}

以下示例表明，2025 年 2 月 1 日与 2025 年 1 月 1 日之间的时间差为 744 小时，对应 31 天：

```sql
SELECT TIMESTAMP_DIFF('2025-02-01'::TIMESTAMP, '2025-01-01'::TIMESTAMP);

┌──────────────────────────────────────────────────────────────────┐
│ timestamp_diff('2025-02-01'::TIMESTAMP, '2025-01-01'::TIMESTAMP) │
├──────────────────────────────────────────────────────────────────┤
│ 744:00:00                                                        │
└──────────────────────────────────────────────────────────────────┘
```