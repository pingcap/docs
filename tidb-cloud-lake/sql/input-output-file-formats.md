---
title: 入出力ファイル形式
summary: "{{{ .lake }}} は、データのロードやアンロードのソースおよびターゲットとして、さまざまなファイル形式を受け入れます。このページでは、サポートされているファイル形式と利用可能なオプションについて説明します。"
---

# 入出力ファイル形式

{{{ .lake }}} は、データのロードやアンロードのソースおよびターゲットとして、さまざまなファイル形式を受け入れます。このページでは、サポートされているファイル形式と利用可能なオプションについて説明します。

## 構文 {#syntax}

ステートメントでファイル形式を指定するには、次の構文を使用します。

```sql
-- Specify a standard file format
... FILE_FORMAT = ( TYPE = { CSV | TSV | NDJSON | PARQUET | LANCE | ORC | AVRO } [ formatTypeOptions ] )

-- Specify a custom file format
... FILE_FORMAT = ( FORMAT_NAME = '<your-custom-format>' )
```

> **Note:**
>
> - {{{ .lake }}} `v1.2.891-nightly` 以降では、`TEXT` が `TSV` のエイリアスとしてサポートされています。
> - 古いサーバーでは `TYPE = TEXT` が拒否される場合があるため、このページではバージョン間の互換性を考慮して、引き続き構文と例で `TSV` を使用しています。
> - {{{ .lake }}} `v1.2.891-nightly` 以降のみを対象とする場合は、新しい設定では `TYPE = TEXT` を使用することを推奨します。

{{{ .lake }}} は、COPY または Select ステートメントで使用するファイル形式を、次の優先順位で決定します。

1. まず、ステートメント内で FILE_FORMAT が明示的に指定されているかを確認します。
2. 操作で FILE_FORMAT が指定されていない場合は、stage 作成時にその stage に対して最初に定義されたファイル形式を使用します。
3. stage 作成時にファイル形式が定義されていない場合、{{{ .lake }}} はデフォルトで PARQUET 形式を使用します。

> **Note:**
>
> - {{{ .lake }}} は現在、ORC と AVRO をソースとしてのみサポートしています。データを ORC または AVRO ファイルにアンロードすることはまだサポートされていません。
> - {{{ .lake }}} は現在、LANCE をアンロード先としてのみサポートしています。`COPY INTO <location>` は単一ファイルではなく Lance データセットディレクトリを書き込むため、stage テーブル読み取りや `COPY INTO <table>` ではなく、下流の Lance ツール向けです。
> - {{{ .lake }}} でカスタムファイル形式を管理する方法については、[ファイル形式](/tidb-cloud-lake/sql/file-format.md) を参照してください。

### formatTypeOptions {#formattypeoptions}

`formatTypeOptions` には、ファイルに関するその他の形式の詳細を記述するための 1 つ以上のオプションが含まれます。オプションはファイル形式によって異なります。サポートされている各ファイル形式で利用可能なオプションについては、以下のセクションを参照してください。

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

## CSV オプション {#csv-options}

{{{ .lake }}} の CSV は [RFC 4180](https://www.rfc-editor.org/rfc/rfc4180) に準拠しており、次の条件に従います。

- 文字列に [QUOTE](#quote-load-only)、[ESCAPE](#escape)、[RECORD_DELIMITER](#record_delimiter)、または [FIELD_DELIMITER](#field_delimiter) の文字が含まれる場合、その文字列は引用符で囲む必要があります。
- 引用符で囲まれた文字列内では、[QUOTE](#quote-load-only) を除き、どの文字もエスケープされません。
- [FIELD_DELIMITER](#field_delimiter) と [QUOTE](#quote-load-only) の間に空白を入れてはいけません。

### RECORD_DELIMITER {#record-delimiter}

ファイル内でレコードを区切る区切り文字です。

**利用可能な値**:

- `\r\n`
- `#` や `|` などの、1 バイトの非英数字文字
- エスケープ文字付きの文字: `\b`, `\f`, `\r`, `\n`, `\t`, `\0`, `\xHH`

**デフォルト**: `\n`

### FIELD_DELIMITER {#field-delimiter}

レコード内でフィールドを区切る区切り文字です。

**利用可能な値**:

- `#` や `|` などの、1 バイトの非英数字文字
- エスケープ文字付きの文字: `\b`, `\f`, `\r`, `\n`, `\t`, `\0`, `\xHH`

**デフォルト**: `,` (カンマ)

### QUOTE (Load Only) {#quote-load-only}

値を引用符で囲むために使用する文字です。

データのロードでは、文字列に [QUOTE](#quote-load-only)、[ESCAPE](#escape)、[RECORD_DELIMITER](#record_delimiter)、または [FIELD_DELIMITER](#field_delimiter) の文字が含まれていない限り、引用符は必須ではありません。

**利用可能な値**: `'\''`, `'"'`, または ``'`'``(バッククォート)

**デフォルト**: `'"'`

### ESCAPE {#escape}

[QUOTE](#quote-load-only) 自体に加えて、引用符で囲まれた値の中で引用符文字をエスケープするために使用する文字です。

CSV の一部のバリアントでは、引用符を二重にしてエスケープする代わりに、`\` のような特別なエスケープ文字を使って引用符をエスケープします。

**利用可能な値**: `'\\'` または `''` (空。二重引用のみを使用することを意味します)

**デフォルト**: `''`

### SKIP_HEADER (Load Only) {#skip-header-load-only}

ファイルの先頭からスキップする行数です。

**デフォルト**: `0`

### TRIM_SPACE (Load Only) {#trim-space-load-only}

型変換の前に、各フィールド値の先頭および末尾から ASCII 空白文字を削除します。

削除対象の文字セットは ASCII 空白文字に固定されており、space、tab、LF、CR、VT、FF が含まれます。

CSV では、csv-core がフィールドを抽出した後にトリミングが行われるため、引用符で囲まれたフィールド内容もトリミングされます。

**デフォルト**: `false`

### OUTPUT_HEADER (Unload Only) {#output-header-unload-only}

カラム名を含むヘッダー行を出力に含めます。

**デフォルト**: `false`

### QUOTE_STYLE (Unload Only) {#quote-style-unload-only}

出力時に CSV の値をどのように引用符で囲むかを制御します。

| 利用可能な値 | 説明 |
|---------------------------|--------------------------------------------------------------|
| `QUOTE_NOT_NULL` (Default)| CSV 出力内の NULL 以外のすべてのフィールドを引用符で囲みます。 |
| `QUOTE_MINIMAL`           | CSV 出力形式で必要な場合にのみフィールドを引用符で囲みます。 |

**デフォルト**: `QUOTE_NOT_NULL`

### NAN_DISPLAY {#nan-display}

"NaN" (Not-a-Number) を表す文字列です。

**利用可能な値**: リテラル `'nan'` または `'null'` のみ (大文字小文字は区別されません)

**デフォルト**: `'NaN'`

### NULL_DISPLAY {#null-display}

NULL 値を表す文字列です。

データのロード時、引用符なしで一致した値は常に NULL になります。引用符付きで一致した値は、`ALLOW_QUOTED_NULLS=true` の場合にのみ NULL に変換されます。

**デフォルト**: `'\N'`

### ALLOW_QUOTED_NULLS (Load Only) {#allow-quoted-nulls-load-only}

引用符付き文字列を NULL 値に変換できるようにします。

`NULL_DISPLAY` に一致する引用符付き文字列は、このフラグが true の場合にのみ NULL になります。引用符なしで一致した値は、このオプションに関係なく NULL になります。

**デフォルト**: `false`

### ERROR_ON_COLUMN_COUNT_MISMATCH (Load Only) {#error-on-column-count-mismatch-load-only}

データファイル内のカラム数が宛先テーブルのカラム数と一致しない場合にエラーを返します。

**デフォルト**: `true`

### EMPTY_FIELD_AS (Load Only) {#empty-field-as-load-only}

引用符なしの空フィールド (つまり `,,`) を変換する値です。

| 利用可能な値 | 変換先 |
|------------------|----------------------------------------------------------------------------------|
| `NULL`           | `NULL`。カラムが NULL 許可でない場合はエラーになります。 |
| `STRING`         | 文字列カラムの場合: `''`。<br/> その他のカラムの場合: `NULL`。NULL 許可でない場合はエラーになります。 |
| `FIELD_DEFAULT`  | そのカラムのデフォルト値。 |

**デフォルト**: `NULL`

### QUOTED_EMPTY_FIELD_AS (Load Only) {#quoted-empty-field-as-load-only}

引用符付きの空フィールド (つまり `,"",`) を変換する値です。

**利用可能な値**: [EMPTY_FIELD_AS](#empty_field_as-load-only) と同じ

**デフォルト**: `STRING`

### BINARY_FORMAT {#binary-format}

`Binary` カラムのエンコード形式です。

**利用可能な値**: `HEX` または `BASE64`

**デフォルト**: `HEX`

### GEOMETRY_FORMAT {#geometry-format}

`Geometry` カラムのエンコード形式です。

**Available Values**: `EWKT`, `WKB`, `WKB`, `EWKB`, `GEOJSON`

**Default**: `EWKT`

### ENCODING (Load Only) {#encoding-load-only}

ソースファイルの文字セットエンコーディングです。UTF-8 以外のエンコーディングに設定した場合、フィールド解析の前にファイル内容は UTF-8 に変換されます。

[Encoding Standard](https://encoding.spec.whatwg.org/) で認識される任意のラベルを使用できます（例: `UTF-8`, `GBK`, `SHIFT_JIS`, `EUC-KR`, `ISO-8859-1`）。このラベルは、ファイル形式 / stage の作成時に検証されます。

**Default**: `UTF-8`

### ENCODING_ERROR_MODE (Load Only) {#encoding-error-mode-load-only}

宣言されたエンコーディングで無効なバイト列（または encoding が `UTF-8` の場合は無効な UTF-8）をどのように処理するかを指定します。

| Available Values   | 説明                                                                 |
|--------------------|----------------------------------------------------------------------|
| `STRICT` (Default) | 最初の不正なバイト列でエラーを返して中止します。                     |
| `REPLACE`          | 各不正バイト列を U+FFFD に置き換えて処理を続行します。               |

**Default**: `STRICT`

### COMPRESSION {#compression}

圧縮アルゴリズムです。

| Available Values | 説明                                                            |
|------------------|-----------------------------------------------------------------|
| `NONE`           | ファイルが圧縮されていないことを示します。                      |
| `AUTO`           | ファイル拡張子から圧縮形式を自動検出します                      |
| `GZIP`           |                                                                 |
| `BZ2`            |                                                                 |
| `BROTLI`         | Brotli 圧縮ファイルをロード/アンロードする場合は指定が必要です。 |
| `ZSTD`           | Zstandard v0.8 以降をサポートします。                            |
| `DEFLATE`        | Deflate 圧縮ファイル（zlib ヘッダー付き、RFC1950）。             |
| `RAW_DEFLATE`    | Deflate 圧縮ファイル（ヘッダーなし、RFC1951）。                  |
| `XZ`             |                                                                 |

**Default**: `NONE`

## TSV Options {#tsv-options}

{{{ .lake }}} TSV（`v1.2.891-nightly` 以降では `TEXT` とも呼ばれます）は、どちらの名前でも同じ形式とオプションを使用します。このページでは、古いサーバーバージョンとの互換性のため、主要な用語として `TSV` を使用します。

{{{ .lake }}} TSV には次の条件があります。

- [RECORD_DELIMITER](#record_delimiter-1)、[FIELD_DELIMITER](#field_delimiter-1) は、[delimiter collision](https://en.wikipedia.org/wiki/Delimiter#Delimiter_collision) を解決するために `\` でエスケープされます
- 区切り文字に加えて、次の文字もエスケープされます: `\b`, `\f`, `\r`, `\n`, `\t`, `\0`, `\\`, `\'`。
- [QUOTE](#quote-load-only) は形式の一部ではありません。
- NULL は `\N` として表されます。

> **Note:**
>
> 1. {{{ .lake }}} では、TSV と CSV の主な違いは、フィールド区切り文字としてカンマの代わりにタブを使うこと（これはオプションで変更可能）ではなく、[delimiter collision](https://en.wikipedia.org/wiki/Delimiter#Delimiter_collision) の処理に引用符ではなくエスケープを使うことです
> 2. CSV には正式な標準があるため、保存形式としては TSV より CSV を推奨します。
> 3. TSV は、次のものによって生成されたファイルのロードに使用できます。
>     1. [Postgresql TEXT](https://www.postgresql.org/docs/current/sql-copy.html)。
>     2. [Clickhouse TSV](https://clickhouse.com/docs/integrations/data-formats/csv-tsv#tsv-tab-separated-files)
>     3. [MySQL TabSeparated](https://dev.mysql.com/doc/refman/8.4/en/mysqldump.html) MySQL `mysqldump --tab`。`--fields-enclosed-by` または `--fields-optionally-enclosed-by` を使用する場合は、代わりに CSV を使用してください。
>     4. デフォルトオプションの [Snowflake CSV](https://docs.snowflake.com/en/sql-reference/sql/create-file-format#type-csv)。`ESCAPE_UNENCLOSED_FIELD` が指定されている場合は、代わりに CSV を使用してください。
>     5. Hive Textfile。

### RECORD_DELIMITER {#record-delimiter}

ファイル内でレコードを区切る文字です。

**Available Values**:

- `\r\n`
- `#` や `|` などの任意の文字。
- エスケープ文字付きの文字: `\b`, `\f`, `\r`, `\n`, `\t`, `\0`, `\xHH`

**Default**: `\n`

### FIELD_DELIMITER {#field-delimiter}

レコード内でフィールドを区切る文字です。

**Available Values**:

- `#` や `|` などの英数字以外の文字。
- エスケープ文字付きの文字: `\b`, `\f`, `\r`, `\n`, `\t`, `\0`, `\xHH`

**Default**: `\t` (TAB)

### SKIP_HEADER (Load Only) {#skip-header-load-only}

[CSV の SKIP_HEADER オプション](#skip_header-load-only)と同じです。

### TRIM_SPACE (Load Only) {#trim-space-load-only}

[CSV の TRIM_SPACE オプション](#trim_space-load-only)と同じです。

### OUTPUT_HEADER (Unload Only) {#output-header-unload-only}

[CSV の OUTPUT_HEADER オプション](#output_header-unload-only)と同じです。

### NAN_DISPLAY {#nan-display}

[CSV の NAN_DISPLAY オプション](#nan_display)と同じです。

### NULL_DISPLAY {#null-display}

[CSV の NULL_DISPLAY オプション](#null_display)と同じです。

### EMPTY_FIELD_AS (Load Only) {#empty-field-as-load-only}

[CSV の EMPTY_FIELD_AS オプション](#empty_field_as-load-only)と同じです。

Note: TSV のデフォルトは `FIELD_DEFAULT` です（デフォルトが `NULL` の CSV とは異なります）。

**Default**: `FIELD_DEFAULT`

### ERROR_ON_COLUMN_COUNT_MISMATCH (Load Only) {#error-on-column-count-mismatch-load-only}

[CSV の ERROR_ON_COLUMN_COUNT_MISMATCH オプション](#error_on_column_count_mismatch-load-only)と同じです。

### ENCODING (Load Only) {#encoding-load-only}

[CSV の ENCODING オプション](#encoding-load-only)と同じです。

### ENCODING_ERROR_MODE (Load Only) {#encoding-error-mode-load-only}

[CSV の ENCODING_ERROR_MODE オプション](#encoding_error_mode-load-only)と同じです。

### COMPRESSION {#compression}

[CSV の COMPRESSION オプション](#compression)と同じです。

## NDJSON Options {#ndjson-options}

### NULL_FIELD_AS (Load Only) {#null-field-as-load-only}

`null` を変換する値です。

| Available Values        | 変換先                                                   |
|-------------------------|----------------------------------------------------------|
| `NULL` (Default)        | NULL 許容フィールドでは NULL。NULL 非許容フィールドではエラー。 |
| `FIELD_DEFAULT`         | フィールドのデフォルト値。                               |

### MISSING_FIELD_AS (Load Only) {#missing-field-as-load-only}

欠落しているフィールドを変換する値です。

| Available Values | 変換先                                                   |
|------------------|----------------------------------------------------------|
| `ERROR` (Default)| エラー。                                                 |
| `NULL`           | NULL 許容フィールドでは NULL。NULL 非許容フィールドではエラー。 |
| `FIELD_DEFAULT`  | フィールドのデフォルト値。                               |

### NULL_IF (Load Only) {#null-if-load-only}

文字列のリストです。ソースファイル内のフィールド値がこれらの文字列のいずれかと一致する場合、その値は NULL としてロードされます。一致は完全一致かつ大文字小文字を区別します。

**Syntax**: `NULL_IF = ('value1', 'value2', ...)`

**Default**: empty (追加の NULL マーカーなし)

### COMPRESSION {#compression}

[CSV の COMPRESSION オプション](#compression)と同じです。

## PARQUET Options {#parquet-options}

### MISSING_FIELD_AS (Load Only) {#missing-field-as-load-only}

欠落しているフィールドを変換する値です。

| Available Values | 変換先                     |
|------------------|----------------------------|
| `ERROR` (Default)| エラー。                   |
| `FIELD_DEFAULT`  | フィールドのデフォルト値。 |

### NULL_IF (Load Only) {#null-if-load-only}

[NDJSON の NULL_IF オプション](#null_if-load-only)と同じです。

### USE_LOGIC_TYPE (Load Only) {#use-logic-type-load-only}

有効にすると、ロード時に Parquet の論理型（例: DATE、TIMESTAMP、DECIMAL annotations）を使用して対象カラム型を決定します。無効にすると、物理ストレージ型のみが考慮されます。

**Default**: `true`

### COMPRESSION (Unload Only) {#compression-unload-only}

parquet ファイル内部ブロックの圧縮アルゴリズムです。

| Available Values | 説明                                                                    |
|------------------|-------------------------------------------------------------------------|
| `ZSTD` (default) | Zstandard v0.8 以降をサポートします。                                   |
| `SNAPPY`         | Snappy は、Parquet でよく使用される一般的で高速な圧縮アルゴリズムです。 |

## LANCE オプション {#lance-options}

`LANCE` は、`COPY INTO <location>` を使用したアンロードでのみサポートされます。

CSV、TSV、NDJSON、Parquet と比較すると、Lance エクスポートでは、{{{ .lake }}} が直接読み戻せる単独ファイルは 1 つも、または複数も生成されません。代わりに、{{{ .lake }}} は `.lance` データファイルと、`_versions/` などのデータセットメタデータを含むデータセットディレクトリを書き込みます。

このため、Lance は、Python `lance` (`pip install pylance`) などの Lance ツールを使ってデータセットを利用する、下流の機械学習、ベクトル、Arrow ベースのワークフローにより適しています。

### フォーマット固有のオプション {#format-specific-options}

Lance にはフォーマット固有のオプションはありません。次を使用します。

```sql
FILE_FORMAT = (TYPE = LANCE)
```

### 動作上の違い {#behavioral-differences}

| 項目 | LANCE の動作 |
|------|----------------|
| サポートされる方向 | アンロードのみ |
| {{{ .lake }}} stage クエリでの読み戻し | サポートされません |
| `COPY INTO <table>` | サポートされません |
| 出力レイアウト | `.lance` ファイルとメタデータを含むデータセットディレクトリ |
| `SINGLE` copy オプション | サポートされません |
| `PARTITION BY` | サポートされません |

## ORC オプション {#orc-options}

### MISSING_FIELD_AS (ロードのみ) {#missing-field-as-load-only}

欠落しているフィールドが変換される値です。

| 利用可能な値 | 変換先 |
|------------------|----------------------------------------------------------|
| `ERROR` (Default)| エラー。 |
| `FIELD_DEFAULT`  | フィールドのデフォルト値。 |

## AVRO オプション {#avro-options}

### MISSING_FIELD_AS (ロードのみ) {#missing-field-as-load-only}

欠落しているフィールドが変換される値です。

| 利用可能な値 | 変換先 |
|------------------|----------------------------------------------------------|
| `ERROR` (Default)| エラー。 |
| `FIELD_DEFAULT`  | フィールドのデフォルト値。 |

### NULL_IF (ロードのみ) {#null-if-load-only}

[NDJSON の NULL_IF オプション](#null_if-load-only)と同じです。

### USE_LOGIC_TYPE (ロードのみ) {#use-logic-type-load-only}

有効にすると、ロード時に対象カラム型を決定するために Avro の論理型（例: date、timestamp-millis、decimal）が使用されます。無効にすると、基になる Avro 型のみが考慮されます。

**Default**: `true`