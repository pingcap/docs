---
title: MAP_KEYS
summary: 返回 map 中的键。
---

# MAP_KEYS

返回 map 中的键。

## 语法 {#syntax}

```sql
MAP_KEYS( <map> )
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|----------------|
| `<map>`   | 输入的 map。 |

## 返回类型 {#return-type}

Array。

## 示例 {#examples}

```sql
SELECT MAP_KEYS({'a':1,'b':2,'c':3});

┌───────────────────────────────┐
│ map_keys({'a':1,'b':2,'c':3}) │
├───────────────────────────────┤
│ ['a','b','c']                 │
└───────────────────────────────┘
```