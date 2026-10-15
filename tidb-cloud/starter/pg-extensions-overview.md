---
title: PostgreSQL 扩展
summary: 了解 PostgreSQL-compatible TiDB Cloud Starter 支持的 PostgreSQL 扩展和内置能力。
---

# PostgreSQL 扩展

PostgreSQL-compatible {{{ .starter }}} 提供一组预定义的 PostgreSQL 扩展和内置能力，用于向量搜索、全文搜索、数据导入、集成以及常见的 PostgreSQL 开发工作流。

> **Note:**
>
> PostgreSQL-compatible {{{ .starter }}} 当前处于公测阶段。扩展的可用性和功能在预览期间可能会发生变化。

## 支持的扩展和能力 {#supported-extensions-and-capabilities}

当前支持以下扩展和能力：

| 扩展或能力 | 描述 | 启用方式 |
| --- | --- | --- |
| `vector` | 提供与 pgvector 兼容的 `VECTOR` 类型、距离运算符、相似性搜索和 HNSW 索引。 | 内置。可使用 `CREATE EXTENSION vector` 注册扩展元信息。 |
| `embedding` | 提供服务端文本向量嵌入函数，例如 `embedding()` 和 `embed_text()`。 | 运行 `CREATE EXTENSION embedding`。 |
| 全文搜索 | 提供与 PostgreSQL 兼容的全文搜索，使用 `tsvector`、`tsquery`、排序函数和 GIN 索引。 | 内置。 |
| 中文分词（与 `zhparser` 兼容） | 为全文搜索提供中文分词。 | 内置且始终可用。 |
| `parquet` | 支持从受支持的 URL 查询和导入 Parquet 数据。 | 运行 `CREATE EXTENSION parquet`。 |
| `http` | 支持直接从 SQL 发起 HTTP 请求。无需注册扩展即可使用 HTTP 函数。 | 内置。 |
| `uuid-ossp` | 提供常用的 UUID 生成功能，例如 `uuid_generate_v4()`。 | 内置。可使用 `CREATE EXTENSION "uuid-ossp"` 注册扩展元信息。 |

## 启用扩展 {#enable-an-extension}

某些扩展会自动可用，而其他扩展则必须通过 `CREATE EXTENSION` 显式启用。

例如：

```sql
CREATE EXTENSION IF NOT EXISTS embedding;
CREATE EXTENSION IF NOT EXISTS parquet;
```

`vector` 类型和向量运算符是内置的。你也可以运行以下语句，在 `pg_extension` 中注册 `vector`，以兼容会检查扩展元信息的工具和 ORM：

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

要查看当前数据库中已注册的扩展，请运行：

```sql
SELECT *
FROM pg_extension;
```

## 限制 {#limitations}

以下限制适用：

- 仅支持 TiDB Cloud 明确提供的扩展和内置能力。
- 你不能安装任意自定义或第三方 PostgreSQL 扩展。
- 某些受支持的扩展仅提供上游 PostgreSQL 或相应开源扩展中的部分行为。
- 在公测期间，扩展的可用性和行为可能会发生变化。
- 公测期间不支持 `pg_cron` 作业调度。尽管 `CREATE EXTENSION pg_cron` 可能会成功，但 `cron.schedule()` 等调度函数不可用，且无法执行已调度的作业。查询 `cron.job` 可能会返回空结果，但这并不表示 `pg_cron` 已正常运行。