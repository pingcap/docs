---
title: 查询与转换
summary: "{{{ .lake }}} 支持直接查询已暂存的文件，而无需先将数据加载到表中。你可以查询任意 stage 类型（user、internal、external）中的文件，也可以直接查询对象存储和 HTTPS URL 中的文件。它非常适合在加载前后进行数据检查、验证和转换。"
---

# 查询与转换

{{{ .lake }}} 支持直接查询已暂存的文件，而无需先将数据加载到表中。你可以查询任意 stage 类型（user、internal、external）中的文件，也可以直接查询对象存储和 HTTPS URL 中的文件。它非常适合在加载前后进行数据检查、验证和转换。

## 语法 {#syntax}

仅查询

```sql
SELECT {
    [<alias>.]<column> [, [<alias>.]<column> ...] -- Query columns by name
  | [<alias>.]$<col_position> [, [<alias>.]$<col_position> ...] -- Query columns by position
  | [<alias>.]$1[:<column>] [, [<alias>.]$1[:<column>]  ...] -- Query rows as Variants
}
FROM {@<stage_name>[/<path>] | '<uri>'}  -- stage table function
  [( -- stage table function parameters
    [<connection_parameters>],
    [ PATTERN => '<regex_pattern>'],
    [ FILE_FORMAT => 'CSV | TSV | NDJSON | PARQUET | ORC | Avro | <custom_format_name>'],
    [ FILES => ( '<file_name>' [ , '<file_name>' ... ])],
    [ CASE_SENSITIVE => true | false ]
  )]
  [<alias>]
```

带转换的复制

```sql
COPY INTO [<database_name>.]<table_name> [ ( <col_name> [ , <col_name> ... ] ) ]
     FROM (
        SELECT {
            [<alias>.]<column> [, [<alias>.]<column> ...] -- Query columns by name
            | [<alias>.]$<col_position> [, [<alias>.]$<col_position> ...] -- Query columns by position
            | [<alias>.]$1[:<column>] [, [<alias>.]$1[:<column>]  ...] -- Query rows as Variants
            } ]
        FROM {@<stage_name>[/<path>] | '<uri>'}
    )
[ FILES = ( '<file_name>' [ , '<file_name>' ] [ , ... ] ) ]
[ PATTERN = '<regex_pattern>' ]
[ FILE_FORMAT = (
         FORMAT_NAME = '<your-custom-format>'
         | TYPE = { CSV | TSV | NDJSON | PARQUET | ORC | AVRO } [ formatTypeOptions ]
       ) ]
[ copyOptions ]
```

> **注意：**
>
> 对比这两种语法：
>
> - `Select List` 相同
> - `FROM {@<stage_name>[/<path>] | '<uri>'}` 相同
> - 参数不同：
>     - 查询使用 `table function parameters`，即 `(<key> => <value>, ...)`
>     - 转换使用位于末尾的选项，参见 [Copy into table](/tidb-cloud-lake/sql/copy-into-table.md)

## FROM 子句 {#from-clause}

`FROM` 子句使用与 `Table Function` 类似的语法。与普通表一样，在与其他表进行 join 时也可以使用表 `alias`。

table function 参数：

| 参数               | 描述                                             |
|-------------------------|---------------------------------------------------------|
| `FILE_FORMAT`           | 文件格式类型（CSV、TSV、NDJSON、PARQUET、ORC、Avro） |
| `PATTERN`               | 用于过滤文件的正则表达式模式                           |
| `FILES`                 | 要查询的文件显式列表                                   |
| `CASE_SENSITIVE`        | 列名是否区分大小写（仅 Parquet）                       |
| `connection_parameters` | 外部存储连接详情                                       |

## 查询文件数据 {#query-file-data}

select 列表支持三种语法；一次只能使用其中一种，不能混用。

### 将行作为 Variants 查询 {#query-rows-as-variants}

- 支持的文件格式：NDJSON、AVRO、Parquet、ORC

> **注意：**
>
> 当前对于 Parquet 和 ORC，`Query rows as Variants` 比 `Query columns by name` 更慢，并且这两种方法不能混用。

语法：

```sql
SELECT [<alias>.]$1[:<column>] [, [<alias>.]$1[:<column>]  ...] <FROM Clause>
```

- 示例：`SELECT $1:id, $1:name FROM ...`
- 表结构：($1: Variant)。即只有一列，类型为 Variant Object，每个 Variant 表示完整的一行
- 说明：
    - 像 `$1:column` 这样的路径表达式的类型也是 Variant，在表达式中使用或加载到目标表列时可以自动转换为原生类型。有时你可能希望在执行特定类型操作前手动进行类型转换（例如 `CAST($1:id AS INT)`），以使语义更加明确。

### 按名称查询列 {#query-columns-by-name}

- 支持的文件格式：NDJSON、AVRO、Parquet、ORC

```sql
SELECT [<alias>.]<column> [, [<alias>.]<column>  ...] <FROM Clause>
```

- 示例：`SELECT id, name FROM ...`
- 表结构：从 Parquet 或 ORC 文件 schema 映射得到的列
- 说明：
    - 所有文件都必须具有相同的 Parquet/ORC schema；否则会返回错误

### 按位置查询列 {#query-columns-by-position}

- 支持的文件格式：CSV、TSV

```sql
SELECT [<alias>.]$<col_position>[, [<alias>.]$<col_position>,  ...] <FROM Clause>
```

- 示例：`SELECT $1, $2 FROM ...`
- 表结构：类型为 `VARCHAR NULL` 的列
- 说明
    - `<col_position>` 从 1 开始

## 查询元信息 {#query-metadata}

你还可以在查询中包含文件元信息，这对于跟踪数据血缘和调试非常有用：

```sql
SELECT METADATA$FILENAME, METADATA$FILE_ROW_NUMBER, $1, <FROM Clause>
(
    FILE_FORMAT => 'ndjson_query_format',
    PATTERN => '.*[.]ndjson'
);
```

以下是支持的文件格式可用的文件级元信息字段：

| 文件元信息              | 类型    | 描述                                      |
| -------------------------- | ------- |--------------------------------------------------|
| `METADATA$FILENAME`        | VARCHAR | 读取该行所在文件的路径 |
| `METADATA$FILE_ROW_NUMBER` | INT     | 该行在文件中的行号（从 0 开始） |

**使用场景：**

- **数据血缘**：跟踪每条记录来自哪个源文件
- **调试**：通过文件和行号定位有问题的记录
- **增量处理**：仅处理特定文件或文件中的特定范围

## 按文件格式分类的教程 {#tutorials-by-file-formats}

- [在 Stage 中查询 Parquet 文件](/tidb-cloud-lake/guides/query-parquet-files-in-stage.md)
- [在 Stage 中查询 ORC 文件](/tidb-cloud-lake/guides/query-staged-orc-files-in-stage.md)
- [在 Stage 中查询 NDJSON 文件](/tidb-cloud-lake/guides/query-ndjson-files-in-stage.md)
- [在 Stage 中查询 Avro 文件](/tidb-cloud-lake/guides/query-avro-files-in-stage.md)
- [在 Stage 中查询 CSV 文件](/tidb-cloud-lake/guides/query-csv-files-in-stage.md)
- [在 Stage 中查询 TSV 文件](/tidb-cloud-lake/guides/query-tsv-files-in-stage.md)

## Schema Evolution {#schema-evolution}

- [Schema Evolution](/tidb-cloud-lake/guides/schema-evolution.md)：在加载表结构持续演进的 Parquet 文件时，自动向表中添加新列。