---
title: PLUS
summary: 计算两个数值或十进制值的和。
---

# PLUS

计算两个数值或十进制值的和。

## 语法 {#syntax}

```sql
PLUS(<number1>, <number2>)
```

## 别名 {#aliases}

- [ADD](/tidb-cloud-lake/sql/add.md)

## 示例 {#examples}

```sql
SELECT ADD(1, 2.3), PLUS(1, 2.3);

┌───────────────────────────────┐
│  add(1, 2.3)  │  plus(1, 2.3) │
├───────────────┼───────────────┤
│ 3.3           │ 3.3           │
└───────────────────────────────┘
```