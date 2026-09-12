---
title: Schema Evolution
summary: 使用 COPY INTO 加载数据时自动演进表结构。
---

# Schema Evolution

Schema Evolution 允许 {{{ .lake }}} 在执行 `COPY INTO` 时，自动将源文件中存在但目标表中缺失的列添加到目标表。目前它支持 **Parquet** 和 **NDJSON** 文件。

## 工作原理 {#how-it-works}

启用后，{{{ .lake }}} 会在加载前推导源文件的表结构，并将新列追加到表末尾。新列均为可空列，缺失的值会填充为 `NULL`。

不同文件格式的工作流程略有不同：

- **Parquet**：启用表选项后，`COPY INTO` 会直接从 Parquet 文件的表结构中推导新列。
- **NDJSON**：启用表选项后，`COPY INTO` 会使用 `AUTO` 采样值进行表结构推导。你也可以选择添加 `SCHEMA_EVOLUTION = (...)` 来覆盖文件和记录的采样限制。

## 启用 Schema Evolution {#enabling-schema-evolution}

将表选项 `ENABLE_SCHEMA_EVOLUTION` 设置为 `true`：

```sql
-- On an existing table
ALTER TABLE my_table SET OPTIONS(ENABLE_SCHEMA_EVOLUTION = true);

-- Or when creating a new table
CREATE TABLE my_table(id INT) ENABLE_SCHEMA_EVOLUTION = true;
```

如需禁用 Schema Evolution，请将其重新设置为 `false`：

```sql
ALTER TABLE my_table SET OPTIONS(ENABLE_SCHEMA_EVOLUTION = false);
```

## 权限 {#privileges}

当 `COPY INTO <table>` 从 stage 或外部位置加载文件并执行 Schema Evolution 推导时，执行加载的角色必须同时拥有目标表的 `INSERT` 和 `ALTER` 权限。之所以需要 `ALTER`，是因为 {{{ .lake }}} 可能会在加载前追加新列。

基于查询的 COPY 不受影响。例如，`COPY INTO <table> FROM (SELECT ... FROM @stage)` 仍保持现有的权限要求。

## Parquet 示例 {#parquet-example}

以下示例加载具有不同表结构的 Parquet 文件，并自动添加缺失列。

### 第 1 步：创建表和 stage {#step-1-create-a-table-and-stage}

```sql
CREATE OR REPLACE TABLE invoices(order_id INT);
CREATE OR REPLACE STAGE my_stage;
```

### 第 2 步：生成具有不同表结构的 Parquet 文件 {#step-2-generate-parquet-files-with-different-schemas}

```sql
-- File with columns: order_id, amount, currency
COPY INTO @my_stage FROM (
    SELECT 1 AS order_id, 100.50::DOUBLE AS amount, 'USD' AS currency
    UNION ALL
    SELECT 2, 250.50::DOUBLE, 'EUR'
) FILE_FORMAT = (TYPE = parquet);

-- File with columns: order_id, amount (no currency)
COPY INTO @my_stage FROM (
    SELECT 3 AS order_id, 75.50::DOUBLE AS amount
) FILE_FORMAT = (TYPE = parquet);
```

### 第 3 步：启用 Schema Evolution 并加载数据 {#step-3-enable-schema-evolution-and-load}

```sql
ALTER TABLE invoices SET OPTIONS(ENABLE_SCHEMA_EVOLUTION = true);

COPY INTO invoices
FROM @my_stage/
FILE_FORMAT = (TYPE = parquet MISSING_FIELD_AS = FIELD_DEFAULT);
```

### 第 4 步：验证结果 {#step-4-verify-results}

该表现在有三列。`amount` 和 `currency` 已被自动添加：

```sql
DESC invoices;
```

```text
┌─────────────────────────────────────────────────────────────┐
│   Field  │      Type      │  Null  │ Default │    Extra     │
├──────────┼────────────────┼────────┼─────────┼──────────────┤
│ order_id │ INT            │ YES    │ NULL    │              │
│ amount   │ DOUBLE         │ YES    │ NULL    │              │
│ currency │ VARCHAR        │ YES    │ NULL    │              │
└─────────────────────────────────────────────────────────────┘
```

```sql
SELECT * FROM invoices ORDER BY order_id;
```

```text
┌──────────────────────────────────────────────────┐
│ order_id │  amount  │ currency                    │
├──────────┼──────────┼─────────────────────────────┤
│        1 │   100.50 │ USD                         │
│        2 │   250.50 │ EUR                         │
│        3 │    75.50 │ NULL                        │
└──────────────────────────────────────────────────┘
```

第 3 行的 `currency = NULL`，因为其源文件中不包含该列。

## NDJSON 示例 {#ndjson-example}

{{{ .lake }}} 使用 `TYPE = ndjson` 加载 NDJSON 文件。NDJSON 文件不像 Parquet 文件那样内嵌列式表结构，因此 {{{ .lake }}} 会对文件内容进行采样，推导目标表中缺失的字段，并将它们追加为可空列。

### 第 1 步：创建表和 stage {#step-1-create-a-table-and-stage}

```sql
CREATE OR REPLACE TABLE events(id INT);
CREATE OR REPLACE STAGE events_stage;
```

### 第 2 步：生成具有不同字段的 NDJSON 文件 {#step-2-generate-ndjson-files-with-different-fields}

```sql
-- File with fields: id, city, score
COPY INTO @events_stage FROM (
    SELECT 1 AS id, 'SF' AS city, 9 AS score
    UNION ALL
    SELECT 2, 'NYC', 8
) FILE_FORMAT = (TYPE = ndjson);

-- File with fields: id, score (no city)
COPY INTO @events_stage FROM (
    SELECT 3 AS id, 7 AS score
) FILE_FORMAT = (TYPE = ndjson);
```

### 第 3 步：启用 Schema Evolution 并加载数据 {#step-3-enable-schema-evolution-and-load}

```sql
ALTER TABLE events SET OPTIONS(ENABLE_SCHEMA_EVOLUTION = true);

COPY INTO events
FROM @events_stage/
FILE_FORMAT = (TYPE = ndjson MISSING_FIELD_AS = FIELD_DEFAULT)
SCHEMA_EVOLUTION = (
  SAMPLE_FILES = AUTO,
  SAMPLE_RECORDS_PER_FILE = AUTO,
  SAMPLE_TOTAL_RECORDS = AUTO
);
```

这三个 `SCHEMA_EVOLUTION` 采样选项都接受 `AUTO` 或正整数：

| 选项 | 描述 |
|------|------|
| `SAMPLE_FILES` | 采样的文件数量。 |
| `SAMPLE_RECORDS_PER_FILE` | 从每个选中文件中采样的最大记录数。 |
| `SAMPLE_TOTAL_RECORDS` | 在所有选中文件中采样的最大记录总数。 |

如果省略 `SCHEMA_EVOLUTION`，{{{ .lake }}} 会对这三个采样选项全部使用 `AUTO`。当前 `AUTO` 的行为是最多采样 64 个文件、每个文件 1,000 条记录，以及总计 10,000 条记录。这些内部默认值可能会在未来版本中发生变化。如果你的加载任务对采样策略较为敏感，请显式设置 `SAMPLE_FILES`、`SAMPLE_RECORDS_PER_FILE` 和 `SAMPLE_TOTAL_RECORDS`。

#### NDJSON 推导规则 {#ndjson-inference-rules}

在对 NDJSON 运行 Schema Evolution 时，{{{ .lake }}} 会按照以下规则推导新列：

- Schema 仅根据采样到的 NDJSON 记录进行推导。未被采样覆盖的字段不会提前添加到目标表中。
- 每一行都必须是一个 JSON 对象。{{{ .lake }}} 使用顶层对象的字段名作为候选列名。
- 目标表中已存在的列不会重复添加。只会追加目标表中缺失的字段。
- 新字段的类型根据采样到的 JSON 值进行推导，例如整数型、float、字符串和布尔值。
- Schema Evolution 对 NDJSON 使用浅层推导：如果顶层字段值是对象或数组，则会将其作为 `VARIANT` 列追加，而不是递归展开。
- `NULL` 样本只会将该字段标记为可为空。它们不会强制后续的非空值变为 `VARCHAR` 或 `VARIANT`。
- 跨文件或记录的同名字段会被合并：整数型与 float 的冲突会变为 `DOUBLE`；其他标量冲突会变为 `VARCHAR`；任何涉及对象、数组或 `VARIANT` 的冲突都会变为 `VARIANT`。
- 如果在加载时遇到采样推导期间未推导出的额外字段，则加载会失败并报告这些字段名。请增大 `SAMPLE_FILES`、`SAMPLE_RECORDS_PER_FILE` 或 `SAMPLE_TOTAL_RECORDS` 后重试。

> **Note:**
>
> 默认情况下，`INFER_SCHEMA` 表函数不会限制 NDJSON 的嵌套深度。这里的规则描述的是 `COPY INTO` Schema Evolution 使用的浅层推导。

例如，以下 NDJSON 记录会推导出六个新列：`name`、`age`、`active`、`score`、`profile` 和 `tags`：

```json
{"id":1,"name":"Alice","age":30,"active":true,"score":1,"profile":{"city":"SF"},"tags":["new"]}
{"id":2,"name":"Bob","age":null,"active":false,"score":1.5,"profile":{"city":"NYC"},"tags":["vip"]}
```

如果目标表只有 `id INT`，{{{ .lake }}} 会追加：

```text
name    VARCHAR   NULL
age     BIGINT    NULL
active  BOOLEAN   NULL
score   DOUBLE    NULL
profile VARIANT   NULL
tags    VARIANT   NULL
```

第二行中 `age = NULL`，这不会改变根据第一行推导出的 `BIGINT` 类型。`score` 同时包含整数型和 float，因此会变为 `DOUBLE`。`profile` 和 `tags` 分别是对象和数组，因此 Schema Evolution 会将它们作为 `VARIANT` 列追加。

### 第 4 步：验证结果 {#step-4-verify-results}

该表现在有三列。`city` 和 `score` 已自动添加：

```sql
DESC events;
```

```text
┌─────────────────────────────────────────────────────────┐
│ Field │     Type     │  Null  │ Default │    Extra     │
├───────┼──────────────┼────────┼─────────┼──────────────┤
│ id    │ INT          │ YES    │ NULL    │              │
│ city  │ VARCHAR      │ YES    │ NULL    │              │
│ score │ BIGINT       │ YES    │ NULL    │              │
└─────────────────────────────────────────────────────────┘
```

```sql
SELECT * FROM events ORDER BY id;
```

```text
┌────────────────────────────┐
│ id │ city │ score          │
├────┼──────┼────────────────┤
│  1 │ SF   │              9 │
│  2 │ NYC  │              8 │
│  3 │ NULL │              7 │
└────────────────────────────┘
```

如果采样未覆盖后续数据中出现的某个字段，加载会失败并返回该额外字段名。请增大 `SAMPLE_FILES`、`SAMPLE_RECORDS_PER_FILE` 或 `SAMPLE_TOTAL_RECORDS` 后重试。

## 列匹配模式 {#column-match-mode}

默认情况下，列名匹配不区分大小写。使用 `COLUMN_MATCH_MODE` 可进行大小写敏感匹配：

```sql
COPY INTO invoices
FROM @my_stage/
FILE_FORMAT = (TYPE = parquet MISSING_FIELD_AS = FIELD_DEFAULT)
COLUMN_MATCH_MODE = CASE_SENSITIVE;
```

## 限制 {#limitations}

- 当前支持 **Parquet** 和 **NDJSON** 文件。
- 新列会追加到表末尾，并且始终可为空。
- 如果同一列名在多个文件中出现且**数据类型不同**，加载会失败。
- 不支持自动类型提升，例如从 `INT` 到 `BIGINT`。
- 不支持通过 schema evolution 删除列或重命名列。
- NDJSON 依赖采样来推导 schema。如果采样未覆盖所有字段，请增大 `SCHEMA_EVOLUTION` 的采样选项。