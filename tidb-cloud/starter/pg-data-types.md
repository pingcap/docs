---
title: PostgreSQL 数据类型
summary: 了解 PostgreSQL-compatible TiDB Cloud Starter 支持的 PostgreSQL 兼容数据类型。
---

# PostgreSQL 数据类型

PostgreSQL-compatible {{{ .starter }}} 支持常见的 PostgreSQL 数据类型，适用于数值、文本、二进制、日期和时间、JSON、数组、向量以及全文搜索工作负载。

## 支持的数据类型 {#supported-data-types}

支持以下数据类型：

| 数据类型 | 别名 | 描述 |
| --- | --- | --- |
| `BOOLEAN` | `BOOL` | 布尔值。 |
| `INTEGER` | `INT`, `INT4` | 4 字节有符号整数。 |
| `BIGINT` | `INT8` | 8 字节有符号整数。 |
| `DOUBLE PRECISION` | `FLOAT8` | 8 字节 IEEE 754 浮点数。 |
| `NUMERIC` | `NUMERIC(p,s)`, `DECIMAL` | 具有 96 位系数且最多支持 28 位小数的精确数值。 |
| `TEXT` | - | 可变长度 UTF-8 文本。 |
| `VARCHAR(n)` | `CHARACTER VARYING(n)` | 最大长度为 `n` 个字符的可变长度文本。 |
| `BYTEA` | - | 二进制数据。 |
| `TIMESTAMP` | `TIMESTAMP WITHOUT TIME ZONE` | 不带时区的日期和时间。 |
| `TIMESTAMPTZ` | `TIMESTAMP WITH TIME ZONE` | 具有时区语义的日期和时间。 |
| `DATE` | - | 日历日期。 |
| `TIME` | `TIME WITHOUT TIME ZONE` | 一天中的时间。 |
| `INTERVAL` | - | 时间间隔。 |
| `UUID` | - | 128 位 UUID 值。 |
| `INET` | - | IPv4 或 IPv6 主机或网络地址。 |
| `JSON` | - | 保留输入文本表示形式的 JSON 数据。 |
| `JSONB` | - | 以规范化表示形式存储的 JSON 数据。 |
| `SERIAL` | - | 由序列支持的自增 4 字节整数。 |
| `BIGSERIAL` | - | 由序列支持的自增 8 字节整数。 |
| `type[]` | - | 支持的数据类型组成的数组。 |
| `VECTOR(n)` | - | 用于向量搜索的固定维度稠密向量。 |
| `TSVECTOR` | - | 全文搜索文档表示。 |
| `TSQUERY` | - | 全文搜索查询表示。 |
| `NAME` | - | 系统目录使用的 PostgreSQL 兼容标识符类型。 |

以下 PostgreSQL 数据类型可以接受，但存在兼容性差异：

- `SMALLINT` 和 `INT2`：内部按 `INTEGER` 存储。不强制执行 PostgreSQL `SMALLINT` 的取值范围。
- `REAL` 和 `FLOAT4`：内部按 `DOUBLE PRECISION` 存储，不具备 PostgreSQL 单精度浮点语义。
- `CHAR(n)` 和 `CHARACTER(n)`：内部按 `VARCHAR` 存储，不具备 PostgreSQL 定长空格填充语义。

## 数值类型 {#numeric-types}

对整数值使用 `INTEGER` 或 `BIGINT`：

```sql
CREATE TABLE counters (
    id BIGSERIAL PRIMARY KEY,
    count INTEGER NOT NULL,
    total BIGINT
);
```

在需要精确十进制值时，使用 `NUMERIC`：

```sql
CREATE TABLE products (
    id BIGSERIAL PRIMARY KEY,
    price NUMERIC(10, 2)
);
```

PostgreSQL-compatible {{{ .starter }}} 使用 96 位系数存储 `NUMERIC` 值，可容纳大约 28–29 位有效十进制数字。通过调整小数点位置，最多可支持 28 位小数。

即使声明了更大的精度或小数位数，仍然适用以下限制：

- `NUMERIC(38,0)` 不支持存储 38 位整数。支持的最大整数为 `79228162514264337593543950335`；更大的整数无法存储。
- 声明的小数位数大于 28 时，也无法保留超过 28 位小数。例如，将 `0.12345678901234567890123456789012345` 存储到 `NUMERIC(60,35)` 列中时，会被舍入为 `0.1234567890123456789012345679`。

在从 PostgreSQL 迁移数据之前，请验证你的数值是否在支持的范围内。

对浮点值使用 `DOUBLE PRECISION`：

```sql
CREATE TABLE measurements (
    id BIGSERIAL PRIMARY KEY,
    value DOUBLE PRECISION
);
```

## 字符和二进制类型 {#character-and-binary-types}

对可变长度文本使用 `TEXT`：

```sql
CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    title TEXT,
    body TEXT
);
```

当你希望限制最大字符长度时，使用 `VARCHAR(n)`：

```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(64) NOT NULL
);
```

使用 `BYTEA` 存储二进制数据：

```sql
CREATE TABLE files (
    id BIGSERIAL PRIMARY KEY,
    content BYTEA
);
```

## 日期和时间类型 {#date-and-time-types}

PostgreSQL-compatible {{{ .starter }}} 支持 `DATE`、`TIME`、`TIMESTAMP`、`TIMESTAMPTZ` 和 `INTERVAL`。

例如：

```sql
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    event_date DATE,
    start_time TIME,
    created_at TIMESTAMP,
    published_at TIMESTAMPTZ,
    duration INTERVAL
);
```

在需要时，使用 PostgreSQL 类型化字面量：

```sql
SELECT
    DATE '2026-09-19',
    TIME '15:30:00',
    TIMESTAMP '2026-09-19 15:30:00',
    TIMESTAMPTZ '2026-09-19 15:30:00+00',
    INTERVAL '2 hours';
```

### 时间戳精度 {#timestamp-precision}

时间戳以微秒精度存储。

类型语法中接受 0 到 6 的精度参数，但它们不会截断已存储的小数秒。

例如，`TIMESTAMP(3)` 仍然可以保留 6 位小数。

## Interval 运算 {#interval-operations}

`INTERVAL` 会分别保留基于月份和不足一个月的组成部分，从而支持具备日历感知能力的日期运算。

你可以对 `INTERVAL` 进行加、减、乘、除运算：

```sql
SELECT
    INTERVAL '1 day' * 2 AS two_days,
    2 * INTERVAL '1 day' AS two_days_again,
    INTERVAL '1 day' / 2 AS half_day,
    INTERVAL '1 day' + INTERVAL '1 hour' AS day_and_hour,
    INTERVAL '3 days' - INTERVAL '1 day' AS two_days,
    INTERVAL '0 day' - INTERVAL '1 day' AS negative_day,
    NOW() - 7 * INTERVAL '1 day' AS one_week_ago;
```

## UUID {#uuid}

使用 `UUID` 存储 128 位 UUID 值：

```sql
CREATE TABLE sessions (
    id UUID PRIMARY KEY,
    user_id BIGINT NOT NULL
);
```

## INET {#inet}

使用 `INET` 存储 IPv4 或 IPv6 主机或网络地址：

```sql
CREATE TABLE access_log (
    id BIGSERIAL PRIMARY KEY,
    client_ip INET
);
```

例如：

```sql
INSERT INTO access_log (client_ip)
VALUES
    ('192.168.1.10'),
    ('10.0.0.0/8'),
    ('::1');
```

支持相等比较和排序比较。某些 PostgreSQL 网络运算符和函数暂不支持。参见[PostgreSQL 兼容性](/tidb-cloud/starter/postgresql-compatibility.md)。

## JSON and JSONB {#json-and-jsonb}

当保留原始 JSON 文本表示很重要时，请使用 `JSON`。当需要规范化表示以及 JSON 包含等操作时，请使用 `JSONB`。

例如：

```sql
CREATE TABLE profiles (
    id BIGSERIAL PRIMARY KEY,
    settings JSONB
);

INSERT INTO profiles (settings)
VALUES ('{"theme":"dark","notifications":true}');

SELECT *
FROM profiles
WHERE settings @> '{"theme":"dark"}';
```

## Arrays {#arrays}

使用 `type[]` 定义数组：

```sql
CREATE TABLE articles (
    id BIGSERIAL PRIMARY KEY,
    tags TEXT[]
);
```

插入并访问数组值：

```sql
INSERT INTO articles (tags)
VALUES (ARRAY['database', 'cloud', 'postgresql']);

SELECT tags[1]
FROM articles;
```

## Vector and full-text search types {#vector-and-full-text-search-types}

`VECTOR(n)` 可用于向量搜索：

```sql
CREATE TABLE embeddings (
    id BIGSERIAL PRIMARY KEY,
    embedding VECTOR(3)
);
```

有关向量运算符和 HNSW 索引的信息，参见[向量搜索](/tidb-cloud/starter/pg-vector-search.md)。

`TSVECTOR` 和 `TSQUERY` 可用于兼容 PostgreSQL 的全文搜索：

```sql
SELECT
    to_tsvector('simple', 'PostgreSQL full text search')
    @@ plainto_tsquery('simple', 'PostgreSQL');
```

更多信息，参见[全文搜索](/tidb-cloud/starter/pg-full-text-search.md)。

## Type coercion {#type-coercion}

兼容 PostgreSQL 的 {{{ .starter }}} 在常见 SQL 上下文中支持 PostgreSQL 风格的类型强制转换。

### `UNION`, `CASE`, `COALESCE`, and `VALUES` {#union-case-coalesce-and-values}

当文本与另一种已确定类型的值组合时，该表达式可以解析为文本类型。

例如：

```sql
SELECT 1
UNION
SELECT 'a';
```

### Comparisons {#comparisons}

当文本字面量与已确定类型的值进行比较时，如果可能，文本字面量会被强制转换为另一个操作数的类型。

例如：

```sql
CREATE TABLE example (
    id INTEGER PRIMARY KEY
);

SELECT *
FROM example
WHERE id = '42';
```

在此示例中，`'42'` 会被强制转换为 `INTEGER`。

### Numeric type promotion {#numeric-type-promotion}

当数值类型组合使用时，结果会按照以下一般优先级进行提升：

```text
INTEGER -> BIGINT -> DOUBLE PRECISION -> NUMERIC
```

与 PostgreSQL 不同，组合 `DOUBLE PRECISION` 和 `NUMERIC` 会产生 `NUMERIC` 结果。例如：

```sql
SELECT pg_typeof(1::double precision + 2::numeric);
```

此查询返回 `numeric`。

如果你的应用需要 `DOUBLE PRECISION` 结果，请将 `NUMERIC` 操作数显式转换为 `DOUBLE PRECISION`。

### Temporal type promotion {#temporal-type-promotion}

常见时间类型表达式的提升规则如下：

| 表达式类型 | 结果类型 |
| --- | --- |
| `DATE` 和 `TIMESTAMP` | `TIMESTAMP` |
| `TIMESTAMP` 和 `TIMESTAMPTZ` | `TIMESTAMPTZ` |
| `DATE` 和 `TIMESTAMPTZ` | `TIMESTAMPTZ` |

## Type casts {#type-casts}

可以使用任一 PostgreSQL 类型转换语法：

```sql
SELECT CAST('42' AS INTEGER);
SELECT '42'::INTEGER;
```

显式类型转换比赋值转换和隐式类型转换更宽松。例如，显式类型转换可以执行某些 `INSERT` 或 `UPDATE` 赋值会拒绝的转换。