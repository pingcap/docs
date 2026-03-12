---
title: ARRAY_INSERT
title_includes: JSON_ARRAY_INSERT
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.762"/>

Inserts a value into a JSON array at the specified index and returns the updated JSON array.

## Aliases

- `JSON_ARRAY_INSERT`

## Syntax

```sql
ARRAY_INSERT(<json_array>, <index>, <json_value>)
```

| Parameter      | Description                                                                                                                                                                                              |
|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `<json_array>` | The JSON array to modify.                                                                                                                                                                                |
| `<index>`      | The position at which the value will be inserted. Positive indices insert at the specified position or append if out of range; negative indices insert from the end or at the beginning if out of range. |
| `<json_value>` | The JSON value to insert into the array.                                                                                                                                                                 |

## Return Type

JSON array.

## Examples

When the `<index>` is a non-negative integer, the new element is inserted at the specified position, and existing elements are shifted to the right.

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

A negative `<index>` counts from the end of the array, with `-1` representing the position before the last element, `-2` before the second last, and so on.

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
