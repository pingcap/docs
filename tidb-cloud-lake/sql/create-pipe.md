---
title: CREATE PIPE
summary: "了解如何在 {{{ .lake }}} 中使用 CREATE PIPE 命令创建摄取管道。"
---

# CREATE PIPE

创建一个由 `COPY INTO <table>` 语句支持的 pipe。

## 语法 {#syntax}

```sql
CREATE PIPE [ IF NOT EXISTS ] <name>
    [ AUTO_INGEST = TRUE ]
    [ COMMENT = '<comment>' | COMMENTS = '<comment>' ]
AS
COPY INTO <table> ...
```

## 参数 {#parameters}

| 参数 | 描述 |
|-----------|-------------|
| `IF NOT EXISTS` | 可选。如果 pipe 已存在，则成功返回且不做任何更改。 |
| `AUTO_INGEST = TRUE` | 可选。启用自动摄取。 |
| `COMMENT` / `COMMENTS` | 可选的 pipe 注释。 |
| `AS COPY INTO ...` | 由 pipe 执行的 `COPY INTO <table>` 语句。 |

## 示例 {#example}

```sql
CREATE PIPE IF NOT EXISTS my_pipe
AUTO_INGEST = TRUE
COMMENTS = 'load staged files into target table'
AS
COPY INTO my_table
FROM @my_stage;
```