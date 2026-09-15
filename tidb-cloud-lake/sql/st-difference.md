---
title: ST_DIFFERENCE
summary: 返回第一个 GEOMETRY 对象中未被第二个 GEOMETRY 对象覆盖的部分。
---

# ST_DIFFERENCE

返回第一个 GEOMETRY 对象中未被第二个 GEOMETRY 对象覆盖的部分。

该函数仅支持 GEOMETRY 值。

## 语法 {#syntax}

```sql
ST_DIFFERENCE(<geometry1>, <geometry2>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|---------------|--------------------------------------------------------|
| `<geometry1>` | 该参数必须是 GEOMETRY 类型的表达式。 |
| `<geometry2>` | 该参数必须是 GEOMETRY 类型的表达式。 |

> **注意：**
>
> 如果两个输入的 GEOMETRY 对象具有不同的 SRID，该函数会报错。

## 返回类型 {#return-type}

GEOMETRY。

## 示例 {#examples}

```sql
SELECT ST_ASWKT(ST_DIFFERENCE(TO_GEOMETRY('POINT(0 0)'), TO_GEOMETRY('POINT(1 1)')));

╭───────────────────────────────────────────────────────────────────────────────╮
│ st_aswkt(st_difference(to_geometry('POINT(0 0)'), to_geometry('POINT(1 1)'))) │
├───────────────────────────────────────────────────────────────────────────────┤
│ POINT(0 0)                                                                    │
╰───────────────────────────────────────────────────────────────────────────────╯
```