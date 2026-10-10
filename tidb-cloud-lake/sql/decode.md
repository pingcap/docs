---
title: DECODE
summary: DECODE 関数は、select expression を各 search expression と順番に比較します。search expression が selection expression に一致すると、対応する result expression が返されます。一致が見つからず、default value が指定されている場合は、その default value が返されます。
---

# DECODE

DECODE 関数は、select expression を各 search expression と順番に比較します。search expression が selection expression に一致すると、対応する result expression が返されます。一致が見つからず、default value が指定されている場合は、その default value が返されます。

## 構文 {#syntax}

```sql
DECODE( <expr>, <search1>, <result1> [, <search2>, <result2> ... ] [, <default> ] )
```

## 引数 {#arguments}

- `expr`: 各 search expression と比較される「select expression」です。通常はカラムですが、サブクエリ、リテラル、またはその他の式にすることもできます。
- `searchN`: select expression と比較する search expression です。一致が見つかった場合、対応する result が返されます。
- `resultN`: 対応する search expression が select expression に一致した場合に返される値です。
- `default`: 任意。一致する search expression がない場合、この default value が返されます。

## 使用上の注意 {#usage-notes}

- `CASE` とは異なり、select expression の NULL 値は、search expression の NULL 値と一致します。
- 複数の search expression が一致する場合でも、返されるのは最初に一致した結果だけです。

## 例 {#examples}

```sql
CREATE TABLE t (a VARCHAR);
INSERT INTO t (a) VALUES
    ('1'),
    ('2'),
    (NULL),
    ('4');
```

default value として 'other' を指定した例です（NULL は NULL と等しいことに注意してください）。

```sql
SELECT a, decode(a,
                       1, 'one',
                       2, 'two',
                       NULL, '-NULL-',
                       'other'
                      ) AS decode_result
    FROM t;
```

結果:

```
┌─a─┬─decode_result─┐
│ 1 │ one           │
│ 2 │ two           │
│   │ -NULL-        │
│ 4 │ other         │
└───┴───────────────┘
```