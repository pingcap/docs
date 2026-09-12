---
title: H3_IS_RES_CLASS_III
summary: 检查给定的 H3 索引是否具有 Class III 方向的分辨率。
---

# H3_IS_RES_CLASS_III

检查给定的 [H3](https://eng.uber.com/h3/) 索引是否具有 Class III 方向的分辨率。

## 语法 {#syntax}

```sql
H3_IS_RES_CLASS_III(h3)
```

## 示例 {#examples}

```sql
SELECT H3_IS_RES_CLASS_III(635318325446452991);

┌─────────────────────────────────────────┐
│ h3_is_res_class_iii(635318325446452991) │
├─────────────────────────────────────────┤
│ true                                    │
└─────────────────────────────────────────┘
```