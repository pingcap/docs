---
title: LIST_STAGE
summary: stage 内のファイルを一覧表示します。これにより、拡張子に基づいて stage 内のファイルをフィルタリングし、各ファイルの詳細情報を取得できます。この関数は DDL コマンド LIST STAGE FILES に似ていますが、すべてのファイル情報ではなく、ファイル名、サイズ、MD5 ハッシュ、最終更新タイムスタンプ、作成者などの特定のファイル情報を SELECT 文で柔軟に取得できます。
---

# LIST_STAGE

stage 内のファイルを一覧表示します。これにより、拡張子に基づいて stage 内のファイルをフィルタリングし、各ファイルの詳細情報を取得できます。この関数は DDL コマンド [LIST STAGE FILES](/tidb-cloud-lake/sql/list-stage.md) に似ていますが、すべてのファイル情報ではなく、ファイル名、サイズ、MD5 ハッシュ、最終更新タイムスタンプ、作成者などの特定のファイル情報を SELECT 文で柔軟に取得できます。

## 構文 {#syntax}

```sql
LIST_STAGE(
  LOCATION => '{ internalStage | externalStage | userStage }'
  [ PATTERN => '<regex_pattern>']
)
```

以下のとおりです。

### internalStage {#internalstage}

```sql
internalStage ::= @<internal_stage_name>[/<path>]
```

### externalStage {#externalstage}

```sql
externalStage ::= @<external_stage_name>[/<path>]
```

### userStage {#userstage}

```sql
userStage ::= @~[/<path>]
```

### PATTERN {#pattern}

正規表現を使用して stage 内のファイルをフィルタリングします。`@<stage_name>[/<path>]` の後のファイルパス部分にマッチします。詳細は、[PATTERN を使用した stage ファイルのフィルタリング](/tidb-cloud-lake/guides/stage-overview.md#filtering-staged-files-with-pattern) を参照してください。

## 例 {#examples}

```sql
SELECT * FROM list_stage(location => '@my_stage/', pattern => '.*[.]log');
+----------------+------+------------------------------------+-------------------------------+---------+
|      name      | size |                md5                 |         last_modified         | creator |
+----------------+------+------------------------------------+-------------------------------+---------+
| 2023/meta.log  |  475 | "4208ff530b252236e14b3cd797abdfbd" | 2023-04-19 20:23:24.000 +0000 | NULL    |
| 2023/query.log | 1348 | "1c6654b207472c277fc8c6207c035e18" | 2023-04-19 20:23:24.000 +0000 | NULL    |
+----------------+------+------------------------------------+-------------------------------+---------+

-- Equivalent to the following statement:
LIST @my_stage PATTERN = '.*[.]log';
```