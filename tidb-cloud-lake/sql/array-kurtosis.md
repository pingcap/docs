---
title: ARRAY_KURTOSIS
summary: 返回数组中数值的超额峰度。`NULL` 元素会被忽略；非数值元素会引发错误。
---

# ARRAY_KURTOSIS

返回数组中数值的超额峰度。`NULL` 元素会被忽略；非数值元素会引发错误。

## 语法 {#syntax}

```sql
ARRAY_KURTOSIS(<array>)
```

## 返回类型 {#return-type}

浮点型。

## 示例 {#examples}

```sql
SELECT ARRAY_KURTOSIS([1, 2, 3, 4]) AS kurt;

┌────────────────────────┐
│ kurt                   │
├────────────────────────┤
│ -1.200000000000001     │
└────────────────────────┘
```

```sql
SELECT ARRAY_KURTOSIS([1.5, 2.5, 3.5, 4.5]) AS kurt_decimal;

┌────────────────────────┐
│ kurt_decimal           │
├────────────────────────┤
│ -1.200000000000001     │
└────────────────────────┘
```

```sql
SELECT ARRAY_KURTOSIS([NULL, 2, 3, 4]) AS kurt_null;

┌────────────────┐
│ kurt_null      │
├────────────────┤
│ 0              │
└────────────────┘
```