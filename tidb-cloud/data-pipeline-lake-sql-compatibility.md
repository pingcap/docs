---
title: TiDB Cloud Lake 的 Data Pipeline SQL 兼容性
summary: TiDB Cloud Data Pipeline 中 DDL、DML 以及 TiDB 到 TiDB Cloud Lake 类型映射行为的参考。
---

# TiDB Cloud Lake 的 Data Pipeline SQL 兼容性

本文档介绍了 TiDB Cloud Data Pipeline 在将数据复制到 TiDB Cloud Lake 时，对 DDL、DML 和列类型的支持情况。你可以使用本文档来规划 pipeline、验证 schema 兼容性，或排查类型转换问题。

> **注意：**
>
> 支持的行为取决于所使用的 TiCDC 和 TiDB Cloud Lake 版本。如果你观察到不同的行为，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

## DDL 支持概览 {#ddl-support-summary}

| DDL 操作 | 状态 | 说明 |
| -------------------- | -----: | ----- |
| `CREATE TABLE` | ✅ |  |
| `ADD COLUMN` | ✅ |  |
| `ADD COLUMN ... NOT NULL DEFAULT ...` | ✅ |  |
| `DROP COLUMN` | ✅ |  |
| `RENAME COLUMN` | ✅ |  |
| `MODIFY COLUMN` | ⚠️ 部分支持 | 仅支持下方列出的 schema evolution 场景。其他转换不作保证，并且可能会阻塞下游消费。 |

### 支持的 `MODIFY COLUMN` 转换 {#supported-modify-column-conversions}

| 从 | 到 | 说明 |
| ---- | -- | ----- |
| `VARCHAR` | `TEXT` | schema evolution 期间常见的扩宽转换。 |
| `TINYINT` | `INT` | 提升整数型存储宽度。 |
| `INT` | `BIGINT` | schema evolution 期间常见的扩宽转换。 |
| `INT` | `VARCHAR` / `TEXT` | 当目标类型被转换为字符串表示时使用。 |

此处未列出的 DDL 操作不会由 pipeline 处理，并且可能会阻塞受影响表后续的数据消费。此外，单条 `ALTER TABLE` 语句中组合多个变更的方式不受支持。

## DML 支持概览 {#dml-support-summary}

| DML 操作 | 状态 |
| ------------ | -----: |
| `INSERT` | ✅ |
| `UPDATE` | ✅ |
| `DELETE` | ✅ |

此处未列出的 DML 操作不会传播到目标端。

## 类型映射参考 {#type-mapping-reference}

### 整数类型 {#integer-types}

| TiDB 类型 | TiDB Cloud Lake 类型 |
| --------- | -------------------- |
| `TINYINT` | `INT8` |
| `TINYINT UNSIGNED` | `UINT8` |
| `SMALLINT` | `INT16` |
| `SMALLINT UNSIGNED` | `UINT16` |
| `MEDIUMINT` | `INT32` |
| `INT` / `INTEGER` | `INT32` |
| `MEDIUMINT UNSIGNED` / `INT UNSIGNED` / `INTEGER UNSIGNED` | `UINT32` |
| `BIGINT` | `INT64` |
| `BIGINT UNSIGNED` | `UINT64` |

### 浮点类型 {#floating-point-types}

| TiDB 类型 | TiDB Cloud Lake 类型 |
| --------- | -------------------- |
| `FLOAT` | `FLOAT32` |
| `DOUBLE` / `REAL` | `FLOAT64` |

### 精确数值类型 {#exact-numeric-types}

| TiDB 类型 | TiDB Cloud Lake 类型 | 说明 |
| --------- | -------------------- | ----- |
| `DECIMAL(P,S)` | `DECIMAL(P,S)` | 精度和扩展会被精确保留。`NUMERIC(P,S)` 也是如此。 |
| `DECIMAL`（无精度） | `DECIMAL(76,30)` | 会自动扩宽到最大有效精度，以避免静默截断。 |
| `NUMERIC`（无精度） | `DECIMAL(76,30)` | 同上。 |

### 日期和时间类型 {#date-and-time-types}

| TiDB 类型 | TiDB Cloud Lake 类型 | 说明 |
| --------- | -------------------- | ----- |
| `DATE` | `DATE` |  |
| `DATETIME` / `DATETIME(n)` | `TIMESTAMP` | 支持小数秒精度。 |
| `TIMESTAMP` / `TIMESTAMP(n)` | `TIMESTAMP` | 支持小数秒精度。 |
| `TIME` | `VARCHAR` | TiDB Cloud Lake 没有独立的 `TIME` 类型，因此会以文本形式存储。 |
| `YEAR` | `INT16` | 映射为整数型，而不是时间类型。 |

### 字符串类型 {#string-types}

| TiDB 类型 | TiDB Cloud Lake 类型 | 说明 |
| --------- | -------------------- | ----- |
| `CHAR` / `VARCHAR` | `VARCHAR` | 长度不会被保留。 |
| `TINYTEXT` / `TEXT` / `MEDIUMTEXT` / `LONGTEXT` | `VARCHAR` |  |
| `ENUM` | `VARCHAR` | 需要使用 `content-compatible=true` 的 changefeed 才能保留 enum 文本。 |
| `SET` | `VARCHAR` | 需要使用 `content-compatible=true` 的 changefeed 才能保留元素文本。 |

### 二进制类型 {#binary-types}

| TiDB 类型 | TiDB Cloud Lake 类型 |
| --------- | -------------------- |
| `BINARY` / `VARBINARY` | `BINARY` |
| `TINYBLOB` / `BLOB` / `MEDIUMBLOB` / `LONGBLOB` | `BINARY` |

### 其他类型 {#other-types}

| TiDB 类型 | TiDB Cloud Lake 类型 | 说明 |
| --------- | -------------------- | ----- |
| `BOOLEAN` / `BOOL` | `BOOLEAN` |  |
| `BIT` | `UINT64` | 始终映射为无符号类型。全为 1 的 `BIT(64)` 会超出有符号 `INT64` 的范围。 |
| `JSON` | `VARIANT` |  |
| 未知 / 未列出的类型 | `VARCHAR` | 回退映射；会丢失类型语义。 |