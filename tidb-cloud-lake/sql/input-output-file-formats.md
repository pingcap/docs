---
title: 输入与输出文件格式
summary: "{{{ .lake }}} 支持多种文件格式，既可作为数据加载或卸载的源，也可作为目标。本文介绍支持的文件格式及其可用选项。"
---

# 输入与输出文件格式

{{{ .lake }}} 支持多种文件格式，既可作为数据加载或卸载的源，也可作为目标。本文介绍支持的文件格式及其可用选项。

## 语法 {#syntax}

要在语句中指定文件格式，请使用以下语法：

```sql
-- Specify a standard file format
... FILE_FORMAT = ( TYPE = { CSV | TSV | NDJSON | PARQUET | LANCE | ORC | AVRO } [ formatTypeOptions ] )

-- Specify a custom file format
... FILE_FORMAT = ( FORMAT_NAME = '<your-custom-format>' )
```

> **注意：**
>
> - 从 {{{ .lake }}} `v1.2.891-nightly` 开始，支持将 `TEXT` 作为 `TSV` 的别名。
> - 较旧版本的服务器可能会拒绝 `TYPE = TEXT`，因此本文在语法和示例中继续使用 `TSV` 以保持跨版本兼容性。
> - 如果你的目标环境仅为 {{{ .lake }}} `v1.2.891-nightly` 或更高版本，建议在新配置中优先使用 `TYPE = TEXT`。

{{{ .lake }}} 按以下优先级顺序确定 COPY 或 Select 语句使用的文件格式：

1. 首先，检查语句中是否显式指定了 FILE_FORMAT。
2. 如果操作中未指定 FILE_FORMAT，则使用创建 stage 时为该 stage 初始定义的文件格式。
3. 如果创建 stage 时未定义文件格式，{{{ .lake }}} 默认使用 PARQUET 格式。

> **注意：**
>
> - {{{ .lake }}} 当前仅支持将 ORC 和 AVRO 用作源。暂不支持将数据卸载到 ORC 或 AVRO 文件中。
> - {{{ .lake }}} 当前仅支持将 LANCE 用作卸载目标。`COPY INTO <location>` 写出的是 Lance 数据集目录，而不是单个独立文件，因此它适用于下游 Lance 工具链，而不是 stage-table 读取或 `COPY INTO <table>`。
> - 关于如何在 {{{ .lake }}} 中管理自定义文件格式，请参见 [文件格式](/tidb-cloud-lake/sql/file-format.md)。

### formatTypeOptions {#formattypeoptions}

`formatTypeOptions` 包含一个或多个选项，用于描述文件的其他格式细节。不同文件格式支持的选项不同。请参见下文各节，了解每种受支持文件格式的可用选项。

```sql
formatTypeOptions ::=
  RECORD_DELIMITER = '<character>'
  FIELD_DELIMITER = '<character>'
  SKIP_HEADER = <integer>
  QUOTE = '<character>'
  ESCAPE = '<character>'
  NAN_DISPLAY = '<string>'
  ROW_TAG = '<string>'
  COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | XZ | NONE
```

## CSV 选项 {#csv-options}

{{{ .lake }}} 的 CSV 实现符合 [RFC 4180](https://www.rfc-editor.org/rfc/rfc4180)，并受以下条件约束：

- 如果一个字符串包含 [QUOTE](#quote-load-only)、[ESCAPE](#escape)、[RECORD_DELIMITER](#record_delimiter) 或 [FIELD_DELIMITER](#field_delimiter) 中定义的字符，则该字符串必须使用引号包裹。
- 在带引号的字符串中，除 [QUOTE](#quote-load-only) 外，不会对任何字符进行转义。
- [FIELD_DELIMITER](#field_delimiter) 与 [QUOTE](#quote-load-only) 之间不应保留空格。

### RECORD_DELIMITER {#record-delimiter}

用于分隔文件中记录的分隔字符。

**可用值**：

- `\r\n`
- 单字节的非字母数字字符，例如 `#` 和 `|`。
- 带转义字符的字符：`\b`、`\f`、`\r`、`\n`、`\t`、`\0`、`\xHH`

**默认值**：`\n`

### FIELD_DELIMITER {#field-delimiter}

用于分隔一条记录中各字段的分隔字符。

**可用值**：

- 单字节的非字母数字字符，例如 `#` 和 `|`。
- 带转义字符的字符：`\b`、`\f`、`\r`、`\n`、`\t`、`\0`、`\xHH`

**默认值**：`,`（逗号）

### QUOTE (Load Only) {#quote-load-only}

用于包裹值的字符。

在加载数据时，除非字符串中包含 [QUOTE](#quote-load-only)、[ESCAPE](#escape)、[RECORD_DELIMITER](#record_delimiter) 或 [FIELD_DELIMITER](#field_delimiter) 中定义的字符，否则不需要使用引号。

**可用值**：`'\''`、`'"'` 或 ``'`'``（反引号）

**默认值**：`'"'`

### ESCAPE {#escape}

用于在带引号的值中对引号字符进行转义的字符，此外 [QUOTE](#quote-load-only) 本身也可用于转义。

在某些 CSV 变体中，引号是通过特殊的转义字符（如 `\`）进行转义的，而不是通过重复引号来转义。

**可用值**：`'\\'` 或 `''`（空，表示仅使用双引号转义）

**默认值**：`''`

### SKIP_HEADER (Load Only) {#skip-header-load-only}

从文件开头跳过的行数。

**默认值**：`0`

### TRIM_SPACE (Load Only) {#trim-space-load-only}

在类型转换之前，去除每个字段值前后的 ASCII 空白字符。

可去除的字符集合固定为 ASCII 空白字符：空格、tab、LF、CR、VT、FF。

对于 CSV，trim 操作发生在 csv-core 提取字段之后，因此带引号字段中的内容也会被去除首尾空白。

**默认值**：`false`

### OUTPUT_HEADER (Unload Only) {#output-header-unload-only}

包含带列名的表头行。

**默认值**：`false`

### QUOTE_STYLE (Unload Only) {#quote-style-unload-only}

控制输出时 CSV 值的加引号方式。

| 可用值 | 说明 |
|---------------------------|--------------------------------------------------------------|
| `QUOTE_NOT_NULL` (Default)| 对 CSV 输出中的每个非 NULL 字段都加引号。 |
| `QUOTE_MINIMAL`           | 仅在 CSV 输出格式要求时才对字段加引号。 |

**默认值**：`QUOTE_NOT_NULL`

### NAN_DISPLAY {#nan-display}

表示 "NaN"（Not-a-Number）的字符串。

**可用值**：必须是字面量 `'nan'` 或 `'null'`（不区分大小写）

**默认值**：`'NaN'`

### NULL_DISPLAY {#null-display}

表示 NULL 值的字符串。

加载数据时，未加引号且匹配的值始终会转换为 NULL；加引号且匹配的值仅在 `ALLOW_QUOTED_NULLS=true` 时才会转换为 NULL。

**默认值**：`'\N'`

### ALLOW_QUOTED_NULLS (Load Only) {#allow-quoted-nulls-load-only}

允许将带引号的字符串转换为 NULL 值。

只有当该标记为 true 时，与 `NULL_DISPLAY` 匹配的带引号字符串才会变为 NULL。未加引号且匹配的值无论此选项如何都会变为 NULL。

**默认值**：`false`

### ERROR_ON_COLUMN_COUNT_MISMATCH (Load Only) {#error-on-column-count-mismatch-load-only}

如果数据文件中的列数与目标表中的列数不匹配，则返回错误。

**默认值**：`true`

### EMPTY_FIELD_AS (Load Only) {#empty-field-as-load-only}

未加引号的空字段（即 `,,`）会被转换为的值。

| 可用值 | 转换为 |
|------------------|----------------------------------------------------------------------------------|
| `NULL`           | `NULL`。如果列不可为空，则报错。 |
| `STRING`         | 对于 String 列：`''`。<br/> 对于其他列：`NULL`。如果列不可为空，则报错。 |
| `FIELD_DEFAULT`  | 该列的默认值。 |

**默认值**：`NULL`

### QUOTED_EMPTY_FIELD_AS (Load Only) {#quoted-empty-field-as-load-only}

带引号的空字段（即 `,"",`）会被转换为的值。

**可用值**：与 [EMPTY_FIELD_AS](#empty_field_as-load-only) 相同

**默认值**：`STRING`

### BINARY_FORMAT {#binary-format}

`Binary` 列的编码格式。

**可用值**：`HEX` 或 `BASE64`

**默认值**：`HEX`

### GEOMETRY_FORMAT {#geometry-format}

`Geometry` 列的编码格式。

**可用值**：`EWKT`、`WKB`、`WKB`、`EWKB`、`GEOJSON`

**默认值**：`EWKT`

### ENCODING (Load Only) {#encoding-load-only}

源文件的字符集编码。设置为非 UTF-8 编码时，会先将文件内容转码为 UTF-8，再进行字段解析。

接受 [Encoding Standard](https://encoding.spec.whatwg.org/) 识别的任何标签（例如 `UTF-8`、`GBK`、`SHIFT_JIS`、`EUC-KR`、`ISO-8859-1`）。该标签会在创建文件格式 / stage 时进行校验。

**默认值**：`UTF-8`

### ENCODING_ERROR_MODE (Load Only) {#encoding-error-mode-load-only}

如何处理在声明编码下无效的字节（或者当编码为 `UTF-8` 时的无效 UTF-8 字节）。

| 可用值             | 说明                                                                 |
|--------------------|----------------------------------------------------------------------|
| `STRICT` (Default) | 在遇到第一个格式错误的字节序列时，报错并退出。                       |
| `REPLACE`          | 将每个格式错误的字节序列替换为 U+FFFD，然后继续处理。                |

**默认值**：`STRICT`

### COMPRESSION {#compression}

压缩算法。

| 可用值           | 说明                                                            |
|------------------|-----------------------------------------------------------------|
| `NONE`           | 表示文件未压缩。                                                |
| `AUTO`           | 通过文件扩展名自动检测压缩格式                                  |
| `GZIP`           |                                                                 |
| `BZ2`            |                                                                 |
| `BROTLI`         | 加载/导出 Brotli 压缩文件时必须显式指定。                       |
| `ZSTD`           | 支持 Zstandard v0.8（及更高版本）。                             |
| `DEFLATE`        | Deflate 压缩文件（带 zlib 头，RFC1950）。                       |
| `RAW_DEFLATE`    | Deflate 压缩文件（不带任何头，RFC1951）。                       |
| `XZ`             |                                                                 |

**默认值**：`NONE`

## TSV 选项 {#tsv-options}

{{{ .lake }}} TSV（在 `v1.2.891-nightly` 及之后版本中也称为 `TEXT`）在这两个名称下使用相同的格式和选项。为兼容旧版本服务器，本页仍以 `TSV` 作为主要术语。

{{{ .lake }}} TSV 需满足以下条件：

- [RECORD_DELIMITER](#record_delimiter-1)、[FIELD_DELIMITER](#field_delimiter-1) 使用 `\` 转义，以解决[分隔符冲突](https://en.wikipedia.org/wiki/Delimiter#Delimiter_collision)
- 除分隔符外，这些字符也会被转义：`\b`、`\f`、`\r`、`\n`、`\t`、`\0`、`\\`、`\'`。
- [QUOTE](#quote-load-only) 不是该格式的一部分。
- NULL 表示为 `\N`。

> **注意：**
>
> 1. 在 {{{ .lake }}} 中，TSV 与 CSV 的主要区别**不是**使用制表符而不是逗号作为字段分隔符（这可以通过选项修改），而是使用转义而不是引用来处理
> [分隔符冲突](https://en.wikipedia.org/wiki/Delimiter#Delimiter_collision)
> 2. 我们建议优先使用 CSV 作为存储格式，因为它有正式标准。
> 3. TSV 可用于加载以下系统生成的文件：
>     1. [Postgresql TEXT](https://www.postgresql.org/docs/current/sql-copy.html)。
>     2. [Clickhouse TSV](https://clickhouse.com/docs/integrations/data-formats/csv-tsv#tsv-tab-separated-files)
>     3. [MySQL TabSeparated](https://dev.mysql.com/doc/refman/8.4/en/mysqldump.html) MySQL `mysqldump --tab`。如果使用了 `--fields-enclosed-by` 或 `--fields-optionally-enclosed-by`，请改用 CSV。
>     4. 使用默认选项的 [Snowflake CSV](https://docs.snowflake.com/en/sql-reference/sql/create-file-format#type-csv)。如果指定了 `ESCAPE_UNENCLOSED_FIELD`，请改用 CSV。
>     5. Hive Textfile。

### RECORD_DELIMITER {#record-delimiter}

用于分隔文件中记录的分隔字符。

**可用值**：

- `\r\n`
- 任意字符，例如 `#` 和 `|`。
- 带转义字符的字符：`\b`、`\f`、`\r`、`\n`、`\t`、`\0`、`\xHH`

**默认值**：`\n`

### FIELD_DELIMITER {#field-delimiter}

用于分隔记录中字段的分隔字符。

**可用值**：

- 非字母数字字符，例如 `#` 和 `|`。
- 带转义字符的字符：`\b`、`\f`、`\r`、`\n`、`\t`、`\0`、`\xHH`

**默认值**：`\t`（TAB）

### SKIP_HEADER (Load Only) {#skip-header-load-only}

与 [CSV 的 SKIP_HEADER 选项](#skip_header-load-only)相同。

### TRIM_SPACE (Load Only) {#trim-space-load-only}

与 [CSV 的 TRIM_SPACE 选项](#trim_space-load-only)相同。

### OUTPUT_HEADER (Unload Only) {#output-header-unload-only}

与 [CSV 的 OUTPUT_HEADER 选项](#output_header-unload-only)相同。

### NAN_DISPLAY {#nan-display}

与 [CSV 的 NAN_DISPLAY 选项](#nan_display)相同。

### NULL_DISPLAY {#null-display}

与 [CSV 的 NULL_DISPLAY 选项](#null_display)相同。

### EMPTY_FIELD_AS (Load Only) {#empty-field-as-load-only}

与 [CSV 的 EMPTY_FIELD_AS 选项](#empty_field_as-load-only)相同。

注意：TSV 的默认值为 `FIELD_DEFAULT`（不同于 CSV，后者默认值为 `NULL`）。

**默认值**：`FIELD_DEFAULT`

### ERROR_ON_COLUMN_COUNT_MISMATCH (Load Only) {#error-on-column-count-mismatch-load-only}

与 [CSV 的 ERROR_ON_COLUMN_COUNT_MISMATCH 选项](#error_on_column_count_mismatch-load-only)相同。

### ENCODING (Load Only) {#encoding-load-only}

与 [CSV 的 ENCODING 选项](#encoding-load-only)相同。

### ENCODING_ERROR_MODE (Load Only) {#encoding-error-mode-load-only}

与 [CSV 的 ENCODING_ERROR_MODE 选项](#encoding_error_mode-load-only)相同。

### COMPRESSION {#compression}

与 [CSV 的 COMPRESSION 选项](#compression)相同。

## NDJSON 选项 {#ndjson-options}

### NULL_FIELD_AS (Load Only) {#null-field-as-load-only}

`null` 被转换成的值。

| 可用值                  | 转换为                                                   |
|-------------------------|----------------------------------------------------------|
| `NULL` (Default)        | 对可为空字段为 NULL；对非空字段报错。                    |
| `FIELD_DEFAULT`         | 该字段的默认值。                                         |

### MISSING_FIELD_AS (Load Only) {#missing-field-as-load-only}

缺失字段被转换成的值。

| 可用值           | 转换为                                                   |
|------------------|----------------------------------------------------------|
| `ERROR` (Default)| 报错。                                                   |
| `NULL`           | 对可为空字段为 NULL；对非空字段报错。                    |
| `FIELD_DEFAULT`  | 该字段的默认值。                                         |

### NULL_IF (Load Only) {#null-if-load-only}

一个字符串列表。当源文件中的字段值等于这些字符串之一时，会将其加载为 NULL。匹配必须完全一致且大小写敏感。

**语法**：`NULL_IF = ('value1', 'value2', ...)`

**默认值**：空（无额外 NULL 标记）

### COMPRESSION {#compression}

与 [CSV 的 COMPRESSION 选项](#compression)相同。

## PARQUET 选项 {#parquet-options}

### MISSING_FIELD_AS (Load Only) {#missing-field-as-load-only}

缺失字段被转换成的值。

| 可用值           | 转换为                                                   |
|------------------|----------------------------------------------------------|
| `ERROR` (Default)| 报错。                                                   |
| `FIELD_DEFAULT`  | 该字段的默认值。                                         |

### NULL_IF (Load Only) {#null-if-load-only}

与 [NDJSON 的 NULL_IF 选项](#null_if-load-only)相同。

### USE_LOGIC_TYPE (Load Only) {#use-logic-type-load-only}

启用后，加载时会使用 Parquet logical types（例如 DATE、TIMESTAMP、DECIMAL 注解）来确定目标列类型。禁用后，则只考虑物理存储类型。

**默认值**：`true`

### COMPRESSION (Unload Only) {#compression-unload-only}

parquet 文件内部块的压缩算法。

| 可用值           | 说明                                                                |
|------------------|---------------------------------------------------------------------|
| `ZSTD` (default) | 支持 Zstandard v0.8（及更高版本）。                                 |
| `SNAPPY`         | Snappy 是一种常用且快速的压缩算法，通常与 Parquet 一起使用。        |

## LANCE 选项 {#lance-options}

仅在使用 `COPY INTO <location>` 卸载时支持 `LANCE`。

与 CSV、TSV、NDJSON 和 Parquet 相比，Lance 导出**不会**生成一个或多个可由 {{{ .lake }}} 直接读回的独立文件。相反，{{{ .lake }}} 会写入一个数据集目录，其中包含 `.lance` 数据文件以及诸如 `_versions/` 之类的数据集元信息。

因此，Lance 更适合下游机器学习、向量以及基于 Arrow 的工作流，这些工作流会使用 Lance 工具（例如 Python `lance`（`pip install pylance`））来消费该数据集。

### 格式特定选项 {#format-specific-options}

Lance 没有格式特定选项。请使用：

```sql
FILE_FORMAT = (TYPE = LANCE)
```

### 行为差异 {#behavioral-differences}

| 项目 | LANCE 行为 |
|------|----------------|
| 支持的方向 | 仅卸载 |
| 在 {{{ .lake }}} stage 查询中读回 | 不支持 |
| `COPY INTO <table>` | 不支持 |
| 输出布局 | 包含 `.lance` 文件和元信息的数据集目录 |
| `SINGLE` copy 选项 | 不支持 |
| `PARTITION BY` | 不支持 |

## ORC 选项 {#orc-options}

### MISSING_FIELD_AS（仅加载） {#missing-field-as-load-only}

缺失字段会被转换成的值。

| 可用值 | 转换为 |
|------------------|----------------------------------------------------------|
| `ERROR` (Default)| 错误。                                                   |
| `FIELD_DEFAULT`  | 字段的默认值。                          |

## AVRO 选项 {#avro-options}

### MISSING_FIELD_AS（仅加载） {#missing-field-as-load-only}

缺失字段会被转换成的值。

| 可用值 | 转换为 |
|------------------|----------------------------------------------------------|
| `ERROR` (Default)| 错误。                                                   |
| `FIELD_DEFAULT`  | 字段的默认值。                          |

### NULL_IF（仅加载） {#null-if-load-only}

与 [NDJSON 的 NULL_IF 选项](#null_if-load-only) 相同。

### USE_LOGIC_TYPE（仅加载） {#use-logic-type-load-only}

启用后，Avro 逻辑类型（例如 date、timestamp-millis、decimal）将用于在加载期间确定目标列类型。禁用后，则只考虑底层 Avro 类型。

**默认值**：`true`