---
title: LIST_STAGE
summary: 列出 stage 中的文件。你可以根据文件扩展名筛选 stage 中的文件，并获取每个文件的详细信息。该函数类似于 DDL 命令 [LIST STAGE FILES](/tidb-cloud-lake/sql/list-stage.md)，但它允许你通过 SELECT 语句灵活地获取特定文件信息，例如文件名、大小、MD5 哈希、最后修改时间戳和创建者，而不是返回所有文件信息。
---

# LIST_STAGE

列出 stage 中的文件。你可以根据文件扩展名筛选 stage 中的文件，并获取每个文件的详细信息。该函数类似于 DDL 命令 [LIST STAGE FILES](/tidb-cloud-lake/sql/list-stage.md)，但它允许你通过 SELECT 语句灵活地获取特定文件信息，例如文件名、大小、MD5 哈希、最后修改时间戳和创建者，而不是返回所有文件信息。

## 语法 {#syntax}

```sql
LIST_STAGE(
  LOCATION => '{ internalStage | externalStage | userStage }'
  [ PATTERN => '<regex_pattern>']
)
```

其中：

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

使用正则表达式筛选 staged 文件。它匹配 `@<stage_name>[/<path>]` 之后的文件路径部分。参见[使用 PATTERN 筛选 staged 文件](/tidb-cloud-lake/guides/stage-overview.md#filtering-staged-files-with-pattern)。

## 示例 {#examples}

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