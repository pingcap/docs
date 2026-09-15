---
title: OBJECT_PICK
summary: 创建一个新的 JSON 对象，该对象仅包含输入 JSON 对象中指定的键。如果指定的键在输入对象中不存在，则会在结果中省略。
---

# OBJECT_PICK

创建一个新的 JSON 对象，该对象仅包含输入 JSON 对象中指定的键。如果指定的键在输入对象中不存在，则会在结果中省略。

## 别名 {#aliases}

- `JSON_OBJECT_PICK`

## 语法 {#syntax}

```sql
OBJECT_PICK(<json_object>, <key1> [, <key2>, ...])
```

## 参数 {#parameters}

| 参数 | 描述 |
|-----------|-------------|
| json_object | 要从中选取键的 JSON 对象（VARIANT 类型）。 |
| key1, key2, ... | 一个或多个字符串字面量，表示要包含在结果对象中的键。 |

## 返回类型 {#return-type}

返回一个 VARIANT，其中包含一个仅带有指定键及其对应值的新 JSON 对象。

## 示例 {#examples}

选取单个键：

```sql
SELECT OBJECT_PICK('{"a":1,"b":2,"c":3}'::VARIANT, 'a');
-- Result: {"a":1}
```

选取多个键：

```sql
SELECT OBJECT_PICK('{"a":1,"b":2,"d":4}'::VARIANT, 'a', 'b');
-- Result: {"a":1,"b":2}
```

选取包含不存在的键的情况（不存在的键会被忽略）：

```sql
SELECT OBJECT_PICK('{"a":1,"b":2,"d":4}'::VARIANT, 'a', 'c');
-- Result: {"a":1}
```