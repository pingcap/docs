---
title: PostgreSQL 会话参数
summary: 了解如何在兼容 PostgreSQL 的 TiDB Cloud Starter 上查看和配置 PostgreSQL 会话参数。
---

# PostgreSQL 会话参数

兼容 PostgreSQL 的 {{{ .starter }}} 支持 PostgreSQL 兼容的会话参数，这些参数用于控制事务行为、数据库模式解析、时区、查询超时、输出格式以及其他会话设置。

## 设置和查看参数 {#set-and-view-parameters}

使用 `SET` 为当前会话更改参数：

```sql
SET statement_timeout = '120s';
```

使用 `SET LOCAL` 仅为当前事务更改参数：

```sql
BEGIN;

SET LOCAL statement_timeout = '30s';

SELECT *
FROM large_table;

COMMIT;
```

使用 `SHOW` 查看当前值：

```sql
SHOW statement_timeout;
```

列出所有已识别的参数：

```sql
SHOW ALL;
```

使用 `RESET` 将单个参数恢复为默认值：

```sql
RESET statement_timeout;
```

重置所有会话参数：

```sql
RESET ALL;
```

## 配置函数 {#configuration-functions}

使用 `current_setting()` 读取参数：

```sql
SELECT current_setting('statement_timeout');
```

使用 `set_config()` 更改参数：

```sql
SELECT set_config(
    'statement_timeout',
    '120s',
    false
);
```

第三个参数用于控制作用域：

- `false`：会话作用域。
- `true`：事务本地作用域。

## 常用的 PostgreSQL 兼容参数 {#common-postgresql-compatible-parameters}

支持以下常用参数：

| 参数 | 默认值 | 可变更 | 说明 |
| --- | --- | --- | --- |
| `application_name` | 空 | 是 | 与会话关联的应用程序名称。 |
| `bytea_output` | `hex` | 是 | `BYTEA` 值的输出格式。 |
| `client_encoding` | `UTF8` | 是 | 客户端字符编码。 |
| `client_min_messages` | `notice` | 是 | 发送给客户端的最低消息严重级别。 |
| `datestyle` | `ISO, MDY` | 否 | 日期显示格式。 |
| `default_transaction_isolation` | `read committed` | 是 | 新事务的默认隔离级别。 |
| `default_transaction_read_only` | `off` | 是 | 新事务默认是否为只读。 |
| `extra_float_digits` | `1` | 是 | 浮点数输出的额外精度。 |
| `search_path` | `$user, public` | 是 | 数据库模式搜索顺序。 |
| `server_encoding` | `UTF8` | 否 | 服务端字符编码。 |
| `standard_conforming_strings` | `on` | 否 | 在字符串常量中将反斜杠按字面值处理。 |
| `statement_timeout` | `60000ms` | 是 | 查询超时。设置为 `0` 表示无超时。 |
| `timezone` | `UTC` | 是 | 会话时区。 |
| `transaction_isolation` | `read committed` | 是 | 当前事务的隔离级别。 |
| `lock_timeout` | `0` | 是 | 获取锁的超时时间。 |
| `password_encryption` | `scram-sha-256` | 是 | 密码哈希算法。 |
| `max_identifier_length` | `63` | 否 | 报告 PostgreSQL 兼容的标识符长度为 63 字节。当前不会强制执行此限制。 |
| `lc_messages` | `C` | 是 | 用于服务器消息的区域设置。 |

`SHOW ALL` 是检查当前 PostgreSQL 兼容 {{{ .starter }}} 实例中可用完整参数集的最佳方式。

## 搜索路径 {#search-path}

`search_path` 参数控制数据库模式解析顺序。

查看当前搜索路径：

```sql
SHOW search_path;
```

为当前会话更改它：

```sql
SET search_path = app, public;
```

更改后，未限定名称会先在 `app` 中解析，再在 `public` 中解析。

## 时区 {#time-zone}

查看当前时区：

```sql
SHOW timezone;
```

设置会话时区：

```sql
SET timezone = 'America/Los_Angeles';
```

或者：

```sql
SET TIME ZONE 'UTC';
```

会话时区会影响 `TIMESTAMPTZ` 值的显示和解释方式。

## 语句超时 {#statement-timeout}

默认语句超时时间为 60 秒。

对于长时间运行的操作，可以增大超时时间：

```sql
SET statement_timeout = '180s';
```

为当前会话禁用语句超时：

```sql
SET statement_timeout = 0;
```

对于索引创建或大规模数据迁移等操作，请谨慎使用较大的超时时间。

## 事务参数 {#transaction-parameters}

为后续事务设置默认隔离级别：

```sql
SET default_transaction_isolation = 'repeatable read';
```

使新事务默认以只读方式运行：

```sql
SET default_transaction_read_only = on;
```

查看当前事务设置：

```sql
SHOW transaction_isolation;
SHOW transaction_read_only;
```

## 其他可接受的 PostgreSQL 参数 {#other-accepted-postgresql-parameters}

以下 PostgreSQL 兼容参数也会被识别：

- `default_table_access_method`
- `default_tablespace`
- `default_text_search_config`
- `default_transaction_deferrable`
- `idle_in_transaction_session_timeout`
- `in_hot_standby`
- `integer_datetimes`
- `intervalstyle`
- `lc_monetary`
- `lc_numeric`
- `lc_time`
- `max_index_keys`
- `row_security`
- `xmloption`

以下附加参数可通过 `SHOW` 读取：

- `is_superuser`
- `listen_addresses`
- `max_connections`
- `port`
- `role`
- `server_version`
- `server_version_num`
- `session_authorization`
- `transaction_deferrable`
- `transaction_read_only`

某些值是为了兼容 PostgreSQL 客户端和工具而暴露的，这并不意味着对应的上游 PostgreSQL 服务器功能都可用。

## 仅用于兼容性的参数 {#compatibility-only-parameters}

某些 PostgreSQL 参数会被接受，以便 PostgreSQL 客户端和框架能够成功初始化会话，但修改它们不会改变查询行为。

### `work_mem` {#work-mem}

`work_mem` 会被接受，并且其会话值可以被修改：

```sql
SET work_mem = '64MB';
SHOW work_mem;
```

在 PostgreSQL 兼容的 {{{ .starter }}} 中，所配置的值不会控制查询执行内存。

### `check_function_bodies` {#check-function-bodies}

`check_function_bodies` 会被接受，但它不会像 PostgreSQL 那样控制函数体校验。

PL/pgSQL 函数体中的 SQL 语句可能仅在调用该函数时才会被校验。请在创建函数后对其进行测试。

## `session_replication_role` {#session-replication-role}

不支持 `session_replication_role = 'replica'`。

以下语句会被拒绝：

```sql
SET session_replication_role = 'replica';
```

触发器将继续以正常的 `origin` 行为执行。

不要依赖 `session_replication_role` 在批量加载期间抑制触发器。

## 全文搜索参数 {#full-text-search-parameter}

`default_text_search_config` 参数用于控制默认的全文搜索配置。

查看当前值：

```sql
SHOW default_text_search_config;
```

为当前会话设置该参数：

```sql
SET default_text_search_config = 'simple';
```

## 向量搜索参数 {#vector-search-parameter}

`hnsw.ef_search` 参数用于控制当前会话的 HNSW 候选列表大小。

查看该参数：

```sql
SHOW hnsw.ef_search;
```

设置该参数：

```sql
SET hnsw.ef_search = 100;
```

默认值为 `40`。更高的值可以提高召回率，但代价是增加额外的查询延时。

## 向量嵌入参数 {#embedding-parameter}

启用 `embedding` 扩展后，`embedding.dimensions` 参数用于控制受支持的服务端嵌入函数所使用的输出维度。

例如：

```sql
SET embedding.dimensions = 512;
```