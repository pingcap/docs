---
title: ST_SYMDIFFERENCE
summary: 返回两个 GEOMETRY 对象中不重叠的部分。
---

# ST_SYMDIFFERENCE

返回两个 GEOMETRY 对象中不重叠的部分。

此函数仅支持 GEOMETRY 值。

## 语法 {#syntax}

```sql
ST_SYMDIFFERENCE(<geometry1>, <geometry2>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|---------------|--------------------------------------------------------|
| `<geometry1>` | 该参数必须是 GEOMETRY 类型的表达式。 |
| `<geometry2>` | 该参数必须是 GEOMETRY 类型的表达式。 |

> **注意：**
>
> 如果两个输入的 GEOMETRY 对象具有不同的 SRID，则该函数会报错。

## 返回类型 {#return-type}

GEOMETRY。

## 示例 {#examples}

```sql
SELECT ST_ASWKT(ST_SYMDIFFERENCE(TO_GEOMETRY('POINT(0 0)'), TO_GEOMETRY('POINT(1 1)')));

╭──────────────────────────────────────────────────────────────────────────────────╮
│ st_aswkt(st_symdifference(to_geometry('POINT(0 0)'), to_geometry('POINT(1 1)'))) │
├──────────────────────────────────────────────────────────────────────────────────┤
│ MULTIPOINT(0 0,1 1)                                                              │
╰──────────────────────────────────────────────────────────────────────────────────╯
```