---
title: MAP_VALUES
summary: 返回 map 中的值。
---

# MAP_VALUES

返回 map 中的值。

## 语法 {#syntax}

```sql
MAP_VALUES( <map> )
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|----------------|
| `<map>`   | 输入的 map。 |

## 返回类型 {#return-type}

Array。

## 示例 {#examples}

```sql
SELECT MAP_VALUES({'a':1,'b':2,'c':3});

┌─────────────────────────────────┐
│ map_values({'a':1,'b':2,'c':3}) │
├─────────────────────────────────┤
│ [1,2,3]                         │
└─────────────────────────────────┘
```