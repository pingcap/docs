---
title: 表函数
summary: 本页提供 {{{ .lake }}} 中表函数的参考信息。表函数返回一组行（类似于表），并且可以在查询的 FROM 子句中使用。
---

# 表函数

本页提供 {{{ .lake }}} 中表函数的参考信息。表函数返回一组行（类似于表），并且可以在查询的 FROM 子句中使用。

## 数据 schema 与文件检查 {#data-schema-file-inspection}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [INFER_SCHEMA](/tidb-cloud-lake/sql/infer-schema.md) | 检测文件元信息 schema 并获取列定义 | `SELECT * FROM INFER_SCHEMA(LOCATION => '@mystage/data/')` |
| [INSPECT_PARQUET](/tidb-cloud-lake/sql/inspect-parquet.md) | 检查 Parquet 文件的结构 | `SELECT * FROM INSPECT_PARQUET(LOCATION => '@mystage/data.parquet')` |

## stage 与查询管理 {#stage-query-management}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [LIST_STAGE](/tidb-cloud-lake/sql/list-stage.md) | 列出 stage 中的文件 | `SELECT * FROM LIST_STAGE(LOCATION => '@mystage/data/')` |
| [RESULT_SCAN](/tidb-cloud-lake/sql/result-scan.md) | 获取先前查询的结果集 | `SELECT * FROM RESULT_SCAN(LAST_QUERY_ID())` |

## 数据生成 {#data-generation}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [GENERATE_SERIES](/tidb-cloud-lake/sql/generate-series.md) | 生成一系列值 | `SELECT * FROM GENERATE_SERIES(1, 10, 2)` |

## 数据转换与展开 {#data-transformation-expansion}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [FLATTEN](/tidb-cloud-lake/sql/flatten.md) | 将嵌套的 JSON 或数组数据转换为表格格式 | `SELECT * FROM FLATTEN(INPUT => parse_json('[1,2,3]'))` |

## 系统信息与管理 {#system-information-management}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [SHOW_GRANTS](/tidb-cloud-lake/sql/show-grants.md) | 显示已授予的权限 | `SELECT * FROM SHOW_GRANTS()` |
| [SHOW_VARIABLES](/tidb-cloud-lake/sql/show-variables.md) | 显示系统变量 | `SELECT * FROM SHOW_VARIABLES()` |
| [STREAM_STATUS](/tidb-cloud-lake/sql/stream-status.md) | 显示流状态信息 | `SELECT * FROM STREAM_STATUS('mystream')` |
| [TASK_HISTROY](/tidb-cloud-lake/sql/task-history.md) | 显示任务执行历史 | `SELECT * FROM TASK_HISTROY('mytask')` |
| [POLICY_REFERENCES](/tidb-cloud-lake/sql/policy-references.md) | 返回安全策略与表/视图之间的关联关系 | `SELECT * FROM POLICY_REFERENCES(POLICY_NAME => 'mypolicy')` |
| [TAG_REFERENCES](/tidb-cloud-lake/sql/tag-references.md) | 返回分配给数据库对象的标签 | `SELECT * FROM TAG_REFERENCES('mydb.mytable', 'TABLE')` |
| [GET_LINEAGE](/tidb-cloud-lake/sql/get-lineage.md) | 返回上游或下游对象及列血缘关系 | `SELECT * FROM GET_LINEAGE('mydb.mytable', 'TABLE', 'UPSTREAM')` |

## 存储引擎函数 {#storage-engine-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [FUSE_VACUUM_TEMPORARY_TABLE](/tidb-cloud-lake/sql/fuse-vacuum-temporary-table.md) | 清理临时表 | `SELECT * FROM FUSE_VACUUM_TEMPORARY_TABLE()` |
| [FUSE_AMEND](/tidb-cloud-lake/sql/system-fuse-amend.md) | 管理数据修正 | `SELECT * FROM FUSE_AMEND()` |

## Iceberg 集成 {#iceberg-integration}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [ICEBERG_MANIFEST](/tidb-cloud-lake/sql/iceberg-manifest.md) | 显示 Iceberg 表的 manifest 信息 | `SELECT * FROM ICEBERG_MANIFEST('mytable')` |
| [ICEBERG_SNAPSHOT](/tidb-cloud-lake/sql/iceberg-snapshot.md) | 显示 Iceberg 表的快照信息 | `SELECT * FROM ICEBERG_SNAPSHOT('mytable')` |

## 匿名化 {#anonymization}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [OBFUSCATE](/tidb-cloud-lake/sql/obfuscate.md) | 数据集匿名化 | `SELECT * FROM OBFUSCATE(users)` |