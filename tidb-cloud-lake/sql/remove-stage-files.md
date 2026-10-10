---
title: REMOVE STAGE FILES
summary: stage からファイルを削除します。
---

# REMOVE STAGE FILES

stage からファイルを削除します。

関連情報:

- [LIST STAGE FILES](/tidb-cloud-lake/sql/list-stage-files.md): stage 内のファイルを一覧表示します。
- [PRESIGN](/tidb-cloud-lake/sql/presign.md): {{{ .lake }}} では、Presigned URL 方式を使用してファイルを stage にアップロードすることを推奨しています。

## 構文 {#syntax}

```sql
REMOVE { userStage | internalStage | externalStage } [ PATTERN = '<regex_pattern>' ]
```

以下のとおりです。

### internalStage {#internalstage}

```sql
internalStage ::= @<internal_stage_name>[/<file>]
```

### externalStage {#externalstage}

```sql
externalStage ::= @<external_stage_name>[/<file>]
```

### PATTERN = 'regex_pattern' {#pattern-regex-pattern}

単一引用符で囲まれた正規表現パターン文字列で、削除する stage 上のファイルを絞り込みます。これは `@<stage_name>[/<path>]` の後のファイルパス部分に一致します。詳細は [PATTERN を使用した stage ファイルのフィルタリング](/tidb-cloud-lake/guides/stage-overview.md#filtering-staged-files-with-pattern) を参照してください。

## 例 {#examples}

次のコマンドは、*playground* という名前の stage から、名前が *'ontime.*'* パターンに一致するすべてのファイルを削除します。

```sql
REMOVE @playground PATTERN = 'ontime.*'
```