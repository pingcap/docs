---
title: REMOVE STAGE FILES
summary: 从 stage 中移除文件。
---

# REMOVE STAGE FILES

从 stage 中移除文件。

另请参阅：

- [LIST STAGE FILES](/tidb-cloud-lake/sql/list-stage-files.md)：列出 stage 中的文件。
- [PRESIGN](/tidb-cloud-lake/sql/presign.md)：{{{ .lake }}} 建议使用 Presigned URL 方法将文件上传到 stage。

## 语法 {#syntax}

```sql
REMOVE { userStage | internalStage | externalStage } [ PATTERN = '<regex_pattern>' ]
```

其中：

### internalStage {#internalstage}

```sql
internalStage ::= @<internal_stage_name>[/<file>]
```

### externalStage {#externalstage}

```sql
externalStage ::= @<external_stage_name>[/<file>]
```

### PATTERN = 'regex_pattern' {#pattern-regex-pattern}

用单引号括起来的正则表达式模式字符串，用于筛选要移除的 stage 文件。它匹配 `@<stage_name>[/<path>]` 之后的文件路径部分。参见 [使用 PATTERN 过滤 stage 文件](/tidb-cloud-lake/guides/stage-overview.md#filtering-staged-files-with-pattern)。

## 示例 {#examples}

以下命令会从名为 *playground* 的 stage 中移除所有名称匹配模式 *'ontime.*'* 的文件：

```sql
REMOVE @playground PATTERN = 'ontime.*'
```