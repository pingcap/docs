---
title: DECODE
summary: DECODE 関数は、選択式を各検索式と順番に比較します。検索式が選択式に一致すると、対応する結果式が返されます。一致が見つからず、デフォルト値が指定されている場合は、そのデフォルト値が返されます。
---

# DECODE

DECODE 関数は、選択式を各検索式と順番に比較します。検索式が選択式に一致すると、対応する結果式が返されます。一致が見つからず、デフォルト値が指定されている場合は、そのデフォルト値が返されます。

## 構文 {#syntax}

```sql
DECODE( <expr>, <search1>, <result1> [, <search2>, <result2> ... ] [, <default> ] )
```

## 引数 {#arguments}

- `expr`: 各検索式と比較される「選択式」です。通常はカラムですが、サブクエリ、リテラル、またはその他の式にすることもできます。
- `searchN`: 選択式と比較する検索式です。一致が見つかった場合、対応する結果が返されます。
- `resultN`: 対応する検索式が選択式に一致した場合に返される値です。
- `default`: 任意。一致する検索式がない場合、このデフォルト値が返されます。

## 使用上の注意 {#usage-notes}

- `CASE` とは異なり、選択式の NULL 値は、検索式の NULL 値と一致します。
- 複数の検索式が一致する場合でも、返されるのは最初に一致した結果だけです。

## 例 {#examples}

```sql
CREATE TABLE t (a VARCHAR);
INSERT INTO t (a) VALUES
    ('1'),
    ('2'),
    (NULL),
    ('4');
```

デフォルト値として 'other' を指定した例です（NULL は NULL と等しいことに注意してください）。

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