---
title: DECODE
summary: DECODE 函数按顺序将选择表达式与每个搜索表达式进行比较。一旦某个搜索表达式与选择表达式匹配，就返回对应的结果表达式。如果未找到匹配项且提供了默认值，则返回默认值。
---

# DECODE

DECODE 函数按顺序将选择表达式与每个搜索表达式进行比较。一旦某个搜索表达式与选择表达式匹配，就返回对应的结果表达式。如果未找到匹配项且提供了默认值，则返回默认值。

## 语法 {#syntax}

```sql
DECODE( <expr>, <search1>, <result1> [, <search2>, <result2> ... ] [, <default> ] )
```

## 参数 {#arguments}

- `expr`：与每个搜索表达式进行比较的“选择表达式”。通常这是一个列，但也可以是子查询、字面量或其他表达式。
- `searchN`：要与选择表达式进行比较的搜索表达式。如果找到匹配项，则返回对应的结果。
- `resultN`：当对应的搜索表达式与选择表达式匹配时将返回的值。
- `default`：可选。如果提供了该参数且没有任何搜索表达式匹配，则返回此默认值。

## 使用说明 {#usage-notes}

- 与 `CASE` 不同，选择表达式中的 `NULL` 值会与搜索表达式中的 `NULL` 值匹配。
- 如果有多个搜索表达式都能匹配，则只返回第一个匹配项的结果。

## 示例 {#examples}

```sql
CREATE TABLE t (a VARCHAR);
INSERT INTO t (a) VALUES
    ('1'),
    ('2'),
    (NULL),
    ('4');
```

带默认值 `'other'` 的示例（注意，`NULL` 等于 `NULL`）：

```sql
SELECT a, decode(a,
                       1, 'one',
                       2, 'two',
                       NULL, '-NULL-',
                       'other'
                      ) AS decode_result
    FROM t;
```

结果：

```
┌─a─┬─decode_result─┐
│ 1 │ one           │
│ 2 │ two           │
│   │ -NULL-        │
│ 4 │ other         │
└───┴───────────────┘
```