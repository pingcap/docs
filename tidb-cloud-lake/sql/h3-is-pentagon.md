---
title: H3_IS_PENTAGON
summary: 检查给定的 H3 索引是否表示一个五边形单元。
---

# H3_IS_PENTAGON

检查给定的 [H3](https://eng.uber.com/h3/) 索引是否表示一个五边形单元。

## 语法 {#syntax}

```sql
H3_IS_PENTAGON(h3)
```

## 示例 {#examples}

```sql
SELECT H3_IS_PENTAGON(599119489002373119);

┌────────────────────────────────────┐
│ h3_is_pentagon(599119489002373119) │
├────────────────────────────────────┤
│ true                               │
└────────────────────────────────────┘
```