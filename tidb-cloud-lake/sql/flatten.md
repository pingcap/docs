---
title: FLATTEN
summary: 将嵌套的 JSON 或数组数据转换为表格格式，其中每个元素或字段都表示为单独的一行。
---

# FLATTEN

将嵌套的 JSON 或数组数据转换为表格格式，其中每个元素或字段都表示为单独的一行。

## 语法 {#syntax}

```sql
[LATERAL] FLATTEN (
  INPUT => <expr>
  [, PATH => <expr>]
  [, OUTER => TRUE | FALSE]
  [, RECURSIVE => TRUE | FALSE]
  [, MODE => 'OBJECT' | 'ARRAY' | 'BOTH']
)
```

## 参数 {#parameters}

| 参数 | 描述 | 默认值 |
|-----------|-------------|---------|
| `INPUT` | 要展开的 JSON 或数组数据 | 必填 |
| `PATH` | 要展开的数组/对象路径 | 无 |
| `OUTER` | 包含结果为零的行（其值为 NULL） | `FALSE` |
| `RECURSIVE` | 展开嵌套元素 | `FALSE` |
| `MODE` | 展开对象、数组或两者 | `'BOTH'` |
| `LATERAL` | 启用与前置表表达式的交叉引用 | 可选 |

## 输出列 {#output-columns}

| 列 | 描述 |
|--------|-------------|
| `SEQ` | 输入的序列号 |
| `KEY` | 展开后值的键（如果没有则为 NULL） |
| `PATH` | 展开元素的路径 |
| `INDEX` | 数组索引（对象为 NULL） |
| `VALUE` | 展开元素的值 |
| `THIS` | 正在展开的元素 |

**注意：** 使用 LATERAL 时，由于动态交叉引用，输出列可能会有所不同。

## 示例 {#examples}

### 基本展开 {#basic-flattening}

```sql
-- Flatten a JSON object with nested structures
SELECT * FROM FLATTEN(
  INPUT => PARSE_JSON(
    '{"name": "John", "languages": ["English", "Spanish"], "address": {"city": "New York"}}'
  )
);
```

结果会将顶层键展开：

```text
| seq | key       | path      | index | value                | this                 |
|-----|-----------|-----------|-------|----------------------|----------------------|
| 1   | name      | name      | NULL  | "John"               | {original JSON}      |
| 1   | languages | languages | NULL  | ["English","Spanish"]| {original JSON}      |
| 1   | address   | address   | NULL  | {"city":"New York"}  | {original JSON}      |
```

### 使用 PATH 参数 {#using-path-parameter}

```sql
-- Flatten only the languages array by specifying the PATH
SELECT * FROM FLATTEN(
  INPUT => PARSE_JSON(
    '{"name": "John", "languages": ["English", "Spanish"]}'
  ),
  PATH => 'languages'
);
```

结果会将数组元素展开：

```text
| seq | key  | path         | index | value     | this               |
|-----|------|--------------|-------|-----------|-------------------|
| 1   | NULL | languages[0] | 0     | "English" | ["English","Spanish"] |
| 1   | NULL | languages[1] | 1     | "Spanish" | ["English","Spanish"] |
```

### 递归展开 {#recursive-flattening}

```sql
-- Recursively flatten nested objects and arrays
SELECT * FROM FLATTEN(
  INPUT => PARSE_JSON(
    '{"name": "John", "address": {"city": "New York", "zip": 10001}}'
  ),
  RECURSIVE => TRUE
);
```

结果会将嵌套对象展开：

```text
| seq | key     | path         | index | value       | this            |
|-----|---------|--------------|-------|-------------|-----------------|
| 1   | name    | name         | NULL  | "John"      | {original JSON} |
| 1   | address | address      | NULL  | {"city":...}| {original JSON} |
| 1   | city    | address.city | NULL  | "New York"  | {"city":...}    |
| 1   | zip     | address.zip  | NULL  | 10001       | {"city":...}    |
```

### 使用 LATERAL FLATTEN {#using-lateral-flatten}

```sql
-- Use LATERAL FLATTEN to transform a JSON array into rows
-- This allows direct access to array elements without a table
SELECT
  f.value:item::STRING AS item_name,
  f.value:price::FLOAT AS price
FROM
  LATERAL FLATTEN(
    INPUT => PARSE_JSON('[
      {"item":"coffee", "price":2.50},
      {"item":"donut", "price":1.20}
    ]')
  ) f;
```

结果：

```text
| item_name | price |
|-----------|-------|
| coffee    | 2.5   |
| donut     | 1.2   |
```