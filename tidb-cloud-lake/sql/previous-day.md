---
title: PREVIOUS_DAY
summary: 返回给定日期或时间戳之前最近一个指定星期几的日期。
---

# PREVIOUS_DAY

返回给定日期或时间戳之前最近一个指定星期几的日期。

## 语法 {#syntax}

```sql
PREVIOUS_DAY(<date_expression>, <target_day>)
```

| 参数                | 描述                                                                                                                                     |
|---------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| `<date_expression>` | 用于计算指定星期几上一次出现日期的 `DATE` 或 `TIMESTAMP` 值。                                                                            |
| `<target_day>`      | 要查找其上一次出现日期的目标星期几。可接受的值包括 `monday`、`tuesday`、`wednesday`、`thursday`、`friday`、`saturday` 和 `sunday`。 |

## 返回类型 {#return-type}

日期。

## 示例 {#examples}

如果你需要查找某个给定日期之前最近的星期五，例如 2024-11-13：

```sql
SELECT PREVIOUS_DAY(to_date('2024-11-13'), friday) AS last_friday;

┌─────────────┐
│ last_friday │
├─────────────┤
│ 2024-11-08  │
└─────────────┘
```