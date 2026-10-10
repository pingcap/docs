---
title: ARRAY_INSERT
summary: 指定したインデックス位置に JSON 配列へ値を挿入し、更新後の JSON 配列を返します。
---

# ARRAY_INSERT

指定したインデックス位置に JSON 配列へ値を挿入し、更新後の JSON 配列を返します。

## エイリアス {#aliases}

- `JSON_ARRAY_INSERT`

## 構文 {#syntax}

```sql
ARRAY_INSERT(<json_array>, <index>, <json_value>)
```

| パラメータ | 説明 |
|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `<json_array>` | 変更対象の JSON 配列です。 |
| `<index>`      | 値を挿入する位置です。正のインデックスは指定位置に挿入し、範囲外の場合は末尾に追加されます。負のインデックスは末尾から数えた位置に挿入し、範囲外の場合は先頭に挿入されます。 |
| `<json_value>` | 配列に挿入する JSON 値です。 |

## 戻り値の型 {#return-type}

JSON 配列。

## 例 {#examples}

`<index>` が 0 以上の整数の場合、新しい要素は指定した位置に挿入され、既存の要素は右にシフトします。

```sql
-- The new element is inserted at position 0 (the beginning of the array), shifting all original elements to the right
SELECT ARRAY_INSERT('["task1", "task2", "task3"]'::VARIANT, 0, '"new_task"'::VARIANT);

-[ RECORD 1 ]-----------------------------------
array_insert('["task1", "task2", "task3"]'::VARIANT, 0, '"new_task"'::VARIANT): ["new_task","task1","task2","task3"]

-- The new element is inserted at position 1, between task1 and task2
SELECT ARRAY_INSERT('["task1", "task2", "task3"]'::VARIANT, 1, '"new_task"'::VARIANT);

-[ RECORD 1 ]-----------------------------------
array_insert('["task1", "task2", "task3"]'::VARIANT, 1, '"new_task"'::VARIANT): ["task1","new_task","task2","task3"]

-- If the index exceeds the length of the array, the new element is appended at the end of the array
SELECT ARRAY_INSERT('["task1", "task2", "task3"]'::VARIANT, 6, '"new_task"'::VARIANT);

-[ RECORD 1 ]-----------------------------------
array_insert('["task1", "task2", "task3"]'::VARIANT, 6, '"new_task"'::VARIANT): ["task1","task2","task3","new_task"]
```

負の `<index>` は配列の末尾から数えます。`-1` は最後の要素の直前、`-2` は最後から 2 番目の要素の直前、というように指定します。

```sql
-- The new element is inserted just before the last element (task3)
SELECT ARRAY_INSERT('["task1", "task2", "task3"]'::VARIANT, -1, '"new_task"'::VARIANT);

-[ RECORD 1 ]-----------------------------------
array_insert('["task1", "task2", "task3"]'::VARIANT, - 1, '"new_task"'::VARIANT): ["task1","task2","new_task","task3"]

-- Since the negative index exceeds the array’s length, the new element is inserted at the beginning
SELECT ARRAY_INSERT('["task1", "task2", "task3"]'::VARIANT, -6, '"new_task"'::VARIANT);

-[ RECORD 1 ]-----------------------------------
array_insert('["task1", "task2", "task3"]'::VARIANT, - 6, '"new_task"'::VARIANT): ["new_task","task1","task2","task3"]
```