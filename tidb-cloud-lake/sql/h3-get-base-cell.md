---
title: H3_GET_BASE_CELL
summary: 返回给定 [H3](https://eng.uber.com/h3/) 索引的基础单元编号。
---

# H3_GET_BASE_CELL

返回给定 [H3](https://eng.uber.com/h3/) 索引的基础单元编号。

## 语法 {#syntax}

```sql
H3_GET_BASE_CELL(h3)
```

## 示例 {#examples}

```sql
SELECT H3_GET_BASE_CELL(644325524701193974);

┌──────────────────────────────────────┐
│ h3_get_base_cell(644325524701193974) │
├──────────────────────────────────────┤
│                                    8 │
└──────────────────────────────────────┘
```