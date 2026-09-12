---
title: MAP_SIZE
summary: 返回 MAP 的大小。
---

# MAP_SIZE

返回 MAP 的大小。

## 语法 {#syntax}

```sql
MAP_SIZE( <map> )
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|----------------|
| `<map>`   | 输入的 map。 |

## 返回类型 {#return-type}

UInt64。

## 示例 {#examples}

```sql
SELECT MAP_SIZE({'a':1,'b':2,'c':3});

┌───────────────────────────────┐
│ map_size({'a':1,'b':2,'c':3}) │
├───────────────────────────────┤
│ 3                             │
└───────────────────────────────┘
```