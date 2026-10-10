---
title: CREATE PIPE
summary: "{{{ .lake }}} の取り込みパイプラインで CREATE PIPE コマンドを使用する方法を学びます。"
---

# CREATE PIPE

`COPY INTO <table>` ステートメントを基盤とする pipe を作成します。

## 構文 {#syntax}

```sql
CREATE PIPE [ IF NOT EXISTS ] <name>
    [ AUTO_INGEST = TRUE ]
    [ COMMENT = '<comment>' | COMMENTS = '<comment>' ]
AS
COPY INTO <table> ...
```

## パラメータ {#parameters}

| パラメータ | 説明 |
|-----------|-------------|
| `IF NOT EXISTS` | オプション。pipe がすでに存在する場合は、変更を加えずに成功します。 |
| `AUTO_INGEST = TRUE` | オプション。自動取り込みを有効にします。 |
| `COMMENT` / `COMMENTS` | オプションの pipe コメントです。 |
| `AS COPY INTO ...` | pipe によって実行される `COPY INTO <table>` ステートメントです。 |

## 例 {#example}

```sql
CREATE PIPE IF NOT EXISTS my_pipe
AUTO_INGEST = TRUE
COMMENTS = 'load staged files into target table'
AS
COPY INTO my_table
FROM @my_stage;
```