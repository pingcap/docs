---
title: ARRAY_INSERT
summary: 在指定索引处向 JSON 数组中插入一个值，并返回修改后的 JSON 数组。
---

# ARRAY_INSERT

在指定索引处向 JSON 数组中插入一个值，并返回修改后的 JSON 数组。

## 别名 {#aliases}

- `JSON_ARRAY_INSERT`

## 语法 {#syntax}

```sql
ARRAY_INSERT(<json_array>, <index>, <json_value>)
```

| 参数 | 描述 |
|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `<json_array>` | 要修改的 JSON 数组。 |
| `<index>`      | 要插入值的位置。正索引会在指定位置插入；如果超出范围，则追加到末尾。负索引从数组末尾开始计数；如果超出范围，则插入到开头。 |
| `<json_value>` | 要插入到数组中的 JSON 值。 |

## 返回类型 {#return-type}

JSON 数组。

## 示例 {#examples}

当 `<index>` 为非负整数时，新元素会插入到指定位置，现有元素会向右移动。

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

负数 `<index>` 表示从数组末尾开始计数，其中 `-1` 表示最后一个元素之前的位置，`-2` 表示倒数第二个元素之前的位置，依此类推。

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