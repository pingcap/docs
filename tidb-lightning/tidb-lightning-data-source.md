---
title: TiDB Lightning Data Sources
summary: TiDB Lightningでサポートされているすべてのデータ ソースについて説明します。
---

# TiDB Lightningデータソース {#tidb-lightning-data-sources}

TiDB Lightning は、CSV、SQL、Parquet ファイルなど、複数のデータ ソースから TiDB クラスターへのデータのインポートをサポートしています。

TiDB Lightningのデータ ソースを指定するには、次の構成を使用します。

```toml
[mydumper]
# Local source data directory or the URI of the external storage such as S3. For more information about the URI of the external storage, see https://docs.pingcap.com/tidb/v8.1/backup-and-restore-storages#uri-format.
data-source-dir = "/data/my_database"
```

TiDB Lightningが実行されると、 `data-source-dir`のパターンに一致するすべてのファイルが検索されます。

| ファイル     | タイプ                                                                                                                                                                                               | パターン                                                     |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| スキーマファイル | `CREATE TABLE` DDL文を含む                                                                                                                                                                            | `${db_name}.${table_name}-schema.sql`                    |
| スキーマファイル | `CREATE DATABASE` DDL文を含む                                                                                                                                                                         | `${db_name}-schema-create.sql`                           |
| データファイル  | データファイルにテーブル全体のデータが含まれている場合、ファイルは`${db_name}.${table_name}`という名前のテーブルにインポートされます。                                                                                                                  | `${db_name}.${table_name}.${csv|sql|parquet}`            |
| データファイル  | テーブルのデータが複数のデータファイルに分割されている場合、各データファイルのファイル名には数字の接尾辞を付ける必要があります。                                                                                                                                  | `${db_name}.${table_name}.001.${csv|sql|parquet}`        |
| 圧縮ファイル   | ファイルに`gzip` 、 `snappy` 、 `zstd`などの圧縮サフィックスが含まれている場合、 TiDB Lightning はインポートする前にファイルを解凍します。Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)である必要があります。その他の Snappy 圧縮形式はサポートされていません。 | `${db_name}.${table_name}.${csv|sql|parquet}.{compress}` |

TiDB Lightning は、可能な限りデータを並列処理します。ファイルは順番に読み取る必要があるため、データ処理の同時実行はファイル レベル ( `region-concurrency`で制御) になります。したがって、インポートされたファイルが大きい場合、インポートのパフォーマンスが低下します。最高のパフォーマンスを実現するには、インポートされたファイルのサイズを 256 MiB 以下に制限することをお勧めします。

## データベースとテーブルの名前を変更する {#rename-databases-and-tables}

TiDB Lightning はファイル名のパターンに従って、対応するデータベースとテーブルにデータをインポートします。データベース名またはテーブル名が変更された場合は、ファイル名を変更してからインポートするか、正規表現を使用してオンラインで名前を置き換えることができます。

### ファイルを一括で名前変更する {#rename-files-in-batch}

Red Hat Linux または Red Hat Linux ベースのディストリビューションを使用している場合は、 `rename`コマンドを使用して`data-source-dir`ディレクトリ内のファイルの名前を一括変更できます。

例えば：

```shell
rename srcdb. tgtdb. *.sql
```

データベース名を変更した後は、 `data-source-dir`ディレクトリから`CREATE DATABASE` DDL ステートメントを含む`${db_name}-schema-create.sql`ファイルを削除することをお勧めします。テーブル名も変更する場合は、 `CREATE TABLE` DDL ステートメントを含む`${db_name}.${table_name}-schema.sql`ファイル内のテーブル名も変更する必要があります。

### 正規表現を使用してオンラインで名前を置換する {#use-regular-expressions-to-replace-names-online}

正規表現を使用してオンラインで名前を置き換えるには、 `[[mydumper.files]]`内の`pattern`構成を使用してファイル名を一致させ、 `schema`と`table`希望の名前に置き換えます。詳細については、 [カスタマイズされたファイルを一致させる](#match-customized-files)参照してください。

以下は、正規表現を使用してオンラインで名前を置き換える例です。この例では、

-   データファイル`pattern`の一致ルールは`^({schema_regrex})\.({table_regrex})\.({file_serial_regrex})\.(csv|parquet|sql)`です。
-   `schema` `'$1'`として指定します。これは、最初の正規表現`schema_regrex`の値が変更されないことを意味します。または、 `schema` `'tgtdb'`などの文字列として指定します。これは、固定のターゲット データベース名を意味します。
-   `table` `'$2'`として指定します。これは、2 番目の正規表現`table_regrex`の値が変更されないことを意味します。または、 `table` `'t1'`などの文字列として指定します。これは、固定のターゲット テーブル名を意味します。
-   `type` `'$3'`として指定します。これはデータ ファイルの種類`"schema-schema"` `type` `schema.sql` `"table-schema"` `schema-create.sql`表す) として指定できます。

```toml
[mydumper]
data-source-dir = "/some-subdir/some-database/"
[[mydumper.files]]
pattern = '^(srcdb)\.(.*?)-schema-create\.sql'
schema = 'tgtdb'
type = "schema-schema"
[[mydumper.files]]
pattern = '^(srcdb)\.(.*?)-schema\.sql'
schema = 'tgtdb'
table = '$2'
type = "table-schema"
[[mydumper.files]]
pattern = '^(srcdb)\.(.*?)\.(?:[0-9]+)\.(csv|parquet|sql)'
schema = 'tgtdb'
table = '$2'
type = '$3'
```

`gzip`使用してデータ ファイルをバックアップする場合は、それに応じて圧縮形式を構成する必要があります。データ ファイル`pattern`の一致ルールは`'^({schema_regrex})\.({table_regrex})\.({file_serial_regrex})\.(csv|parquet|sql)\.(gz)'`です。圧縮ファイル形式を表すには、 `compression` `'$4'`として指定できます。例:

```toml
[mydumper]
data-source-dir = "/some-subdir/some-database/"
[[mydumper.files]]
pattern = '^(srcdb)\.(.*?)-schema-create\.(sql)\.(gz)'
schema = 'tgtdb'
type = "schema-schema"
compression = '$4'
[[mydumper.files]]
pattern = '^(srcdb)\.(.*?)-schema\.(sql)\.(gz)'
schema = 'tgtdb'
table = '$2'
type = "table-schema"
compression = '$4'
[[mydumper.files]]
pattern = '^(srcdb)\.(.*?)\.(?:[0-9]+)\.(sql)\.(gz)'
schema = 'tgtdb'
table = '$2'
type = '$3'
compression = '$4'
```

## CSVファイル {#csv}

### スキーマ {#schema}

CSV ファイルにはスキーマがありません。CSV ファイルを TiDB にインポートするには、テーブル スキーマを提供する必要があります。スキーマは、次のいずれかの方法で提供できます。

-   DDL ステートメントを含む`${db_name}.${table_name}-schema.sql`および`${db_name}-schema-create.sql`という名前のファイルを作成します。
-   TiDB にテーブル スキーマを手動で作成します。

### コンフィグレーション {#configuration}

CSV 形式は、 `tidb-lightning.toml`ファイルの`[mydumper.csv]`セクションで設定できます。ほとんどの設定には、MySQL の[`LOAD DATA`](https://dev.mysql.com/doc/refman/8.0/en/load-data.html)ステートメントに対応するオプションがあります。

```toml
[mydumper.csv]
# The field separator. Can be one or multiple characters. The default is ','.
# If the data might contain commas, it is recommended to use '|+|' or other uncommon
# character combinations as a separator.
separator = ','
# Quoting delimiter. Empty value means no quoting.
delimiter = '"'
# Line terminator. Can be one or multiple characters. Empty value (default) means
# both "\n" (LF) and "\r\n" (CRLF) are line terminators.
terminator = ''
# Whether the CSV file contains a header.
# If `header` is true, the first line is skipped and mapped
# to the table columns.
header = true
# Whether the CSV file contains any NULL value.
# If `not-null` is true, all columns from CSV cannot be parsed as NULL.
not-null = false
# When `not-null` is false (that is, CSV can contain NULL),
# fields equal to this value will be treated as NULL.
null = '\N'
# Whether to parse backslash as escape character.
backslash-escape = true
# Whether to treat `separator` as the line terminator and trim all trailing separators.
trim-last-separator = false
```

`separator` 、 `delimiter` 、 `terminator`などの文字列フィールドの入力に特殊文字が含まれる場合は、バックスラッシュを使用して特殊文字をエスケープできます。エスケープ シーケンスは*二重引用符で囲まれた*文字列 ( `"…"` ) である必要があります。たとえば、 `separator = "\u001f"`区切り文字として ASCII 文字`0X1F`使用することを意味します。

*一重引用符で囲まれた*文字列 ( `'…'` ) を使用すると、バックスラッシュのエスケープを抑制できます。たとえば、 `terminator = '\n'` 、 LF `\n`ではなく、バックスラッシュ ( `\` ) と文字`n`の 2 文字の文字列を終端として使用することを意味します。

詳細については[TOML v1.0.0仕様](https://toml.io/en/v1.0.0#string)参照してください。

#### <code>separator</code> {#code-separator-code}

-   フィールド区切り文字を定義します。

-   1 文字または複数文字を指定できますが、空にすることはできません。

-   共通の値:

    -   CSV（カンマ区切り値）の場合は`','` 。
    -   TSV (タブ区切り値)の場合は`"\t"` 。
    -   `"\u0001"` ASCII 文字`0x01`を使用します。

-   LOAD DATA ステートメントの`FIELDS TERMINATED BY`オプションに対応します。

#### <code>delimiter</code> {#code-delimiter-code}

-   引用符に使用する区切り文字を定義します。

-   `delimiter`が空の場合、すべてのフィールドは引用符で囲まれません。

-   共通の値:

    -   `'"'`フィールドを二重引用符で囲みます。 [RFC 4180](https://tools.ietf.org/html/rfc4180)と同じです。
    -   `''`引用を無効にします。

-   `LOAD DATA`ステートメントの`FIELDS ENCLOSED BY`オプションに対応します。

#### <code>terminator</code> {#code-terminator-code}

-   行末記号を定義します。
-   `terminator`が空の場合、 `"\n"` (改行) と`"\r\n"` (復帰 + 改行) の両方が行末文字として使用されます。
-   `LOAD DATA`ステートメントの`LINES TERMINATED BY`オプションに対応します。

#### <code>header</code> {#code-header-code}

-   *すべての*CSV ファイルにヘッダー行が含まれているかどうか。
-   `header`が`true`場合、最初の行は*列名*として使用されます。 `header`が`false`場合、最初の行は通常のデータ行として扱われます。

#### <code>not-null</code>と<code>null</code> {#code-not-null-code-and-code-null-code}

-   `not-null`設定は、すべてのフィールドが null 不可であるかどうかを制御します。
-   `not-null`が`false`の場合、 `null`で指定された文字列は特定の値ではなく SQL NULL に変換されます。
-   引用符はフィールドが null であるかどうかには影響しません。

    たとえば、次の CSV ファイルの場合:

    ```csv
    A,B,C
    \N,"\N",
    ```

    デフォルト設定（ `not-null = false; null = '\N'` ）では、列`A`と`B` TiDBにインポートされた後、両方ともNULLに変換されます。列`C`は空の文字列`''`ですが、NULLではありません。

#### <code>backslash-escape</code> {#code-backslash-escape-code}

-   フィールド内のバックスラッシュをエスケープ文字として解析するかどうか。

-   `backslash-escape`が真の場合、次のシーケンスが認識され、変換されます。

    | シーケンス | 変換された                  |
    | ----- | ---------------------- |
    | `\0`  | ヌル文字 ( `U+0000` )      |
    | `\b`  | バックスペース ( `U+0008` )   |
    | `\n`  | 改行 ( `U+000A` )        |
    | `\r`  | キャリッジリターン ( `U+000D` ) |
    | `\t`  | タブ ( `U+0009` )        |
    | `\Z`  | ウィンドウズEOF ( `U+001A` ) |

    その他の場合（たとえば、 `\"` ）は、バックスラッシュが削除され、フィールドに次の文字（ `"` ）が残ります。残った文字には特別な役割（たとえば、区切り文字）はなく、通常の文字です。

-   引用符で囲んでも、バックスラッシュがエスケープ文字として解析されるかどうかには影響しません。

-   `LOAD DATA`ステートメントの`FIELDS ESCAPED BY '\'`オプションに対応します。

#### <code>trim-last-separator</code> {#code-trim-last-separator-code}

-   `separator`行末文字として扱い、すべての末尾の区切り文字を削除するかどうか。

    たとえば、次の CSV ファイルの場合:

    ```csv
    A,,B,,
    ```

    -   `trim-last-separator = false`の場合、これは 5 つのフィールド`('A', '', 'B', '', '')`の行として解釈されます。
    -   `trim-last-separator = true`の場合、これは 3 つのフィールド`('A', '', 'B')`の行として解釈されます。

-   このオプションは非推奨です。代わりに`terminator`オプションを使用してください。

    既存の構成が次の場合:

    ```toml
    separator = ','
    trim-last-separator = true
    ```

    構成を次のように変更することをお勧めします。

    ```toml
    separator = ','
    terminator = ",\n" # Use ",\n" or ",'\r\n" according to your actual file.
    ```

#### 設定できないオプション {#non-configurable-options}

TiDB Lightning は、 `LOAD DATA`ステートメントでサポートされているすべてのオプションをサポートしているわけではありません。例:

-   行頭文字（ `LINES STARTING BY` ）は使用できません。
-   ヘッダーはスキップできません（ `IGNORE n LINES` ）。有効な列名である必要があります。

### 厳格なフォーマット {#strict-format}

TiDB Lightning は、入力ファイルのサイズが 256 MiB 前後の均一な場合に最適に機能します。入力が 1 つの巨大な CSV ファイルである場合、 TiDB Lightning は1 つのスレッドでしかファイルを処理できないため、インポート速度が低下します。

これは、最初に CSV を複数のファイルに分割することで修正できます。一般的な CSV 形式では、ファイル全体を読み取らずに行の開始位置や終了位置をすばやく特定する方法はありません。そのため、 TiDB Lightning はデフォルトで CSV ファイルを自動的に分割しませ*ん*。ただし、CSV 入力が特定の制限に準拠していることが確実な場合は、 `strict-format`設定を有効にして、 TiDB Lightning がファイルを複数の 256 MiB サイズのチャンクに分割し、並列処理できるようにすることができます。

```toml
[mydumper]
strict-format = true
```

厳密な CSV ファイルでは、各フィールドは 1 行のみを占めます。つまり、次のいずれかが当てはまる必要があります。

-   区切り文字が空です。
-   各フィールドにはターミネータ自体は含まれません。デフォルト設定では、各フィールドに CR ( `\r` ) または LF ( `\n` ) が含まれないことを意味します。

CSV ファイルが厳密ではなく、 `strict-format`が誤って`true`に設定されている場合、複数行にまたがるフィールドが 2 つのチャンクに分割され、解析エラーが発生したり、破損したデータが黙ってインポートされたりする可能性があります。

### 一般的な構成例 {#common-configuration-examples}

#### CSVファイル {#csv}

デフォルト設定は、RFC 4180 に従って CSV 用にすでに調整されています。

```toml
[mydumper.csv]
separator = ',' # If the data might contain a comma (','), it is recommended to use '|+|' or other uncommon character combinations as the separator.
delimiter = '"'
header = true
not-null = false
null = '\N'
backslash-escape = true
```

コンテンツの例:

    ID,Region,Count
    1,"East",32
    2,"South",\N
    3,"West",10
    4,"North",39

#### TSSV {#tsv}

```toml
[mydumper.csv]
separator = "\t"
delimiter = ''
header = true
not-null = false
null = 'NULL'
backslash-escape = false
```

コンテンツの例:

    ID    Region    Count
    1     East      32
    2     South     NULL
    3     West      10
    4     North     39

#### TPC-H DBGEN {#tpc-h-dbgen}

```toml
[mydumper.csv]
separator = '|'
delimiter = ''
terminator = "|\n"
header = false
not-null = true
backslash-escape = false
```

コンテンツの例:

    1|East|32|
    2|South|0|
    3|West|10|
    4|North|39|

## 構文 {#sql}

TiDB Lightning がTiDB Lightningファイルを処理する場合、単一の SQL ファイルをすばやく分割できないため、同時実行性を高めて単一ファイルのインポート速度を向上させることはできません。したがって、SQL ファイルからデータをインポートする場合は、単一の巨大な SQL ファイルを避けてください。TiDB TiDB Lightning は、入力ファイルのサイズが 256 MiB 前後で均一である場合に最も効果的に機能します。

## 寄木細工 {#parquet}

TiDB Lightning は現在、Amazon Aurora、Apache Hive、Snowflake によって生成された Parquet ファイルのみをサポートしています。S3 内のファイル構造を識別するには、次の設定を使用してすべてのデータ ファイルを一致させます。

    [[mydumper.files]]
    # The expression needed for parsing Amazon Aurora parquet files
    pattern = '(?i)^(?:[^/]*/)*([a-z0-9\-_]+).([a-z0-9\-_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'
    schema = '$1'
    table = '$2'
    type = '$3'

この設定は、 Auroraスナップショットによってエクスポートされた parquet ファイルを一致させる方法のみを示していることに注意してください。スキーマ ファイルを個別にエクスポートして処理する必要があります。

`mydumper.files`の詳細については[カスタマイズされたファイルと一致](#match-customized-files)を参照してください。

## 圧縮ファイル {#compressed-files}

TiDB Lightning は現在、 Dumplingによってエクスポートされた圧縮ファイル、または命名規則に従う圧縮ファイルをサポートしています。現在、 TiDB Lightning は次の圧縮アルゴリズムをサポートしています: `gzip` 、 `snappy` 、および`zstd` 。ファイル名が命名規則に従っている場合、 TiDB Lightning は自動的に圧縮アルゴリズムを識別し、追加の構成なしでストリーミング解凍後にファイルをインポートします。

> **注記：**
>
> -   TiDB Lightning は1 つの大きな圧縮ファイルを同時に解凍できないため、圧縮ファイルのサイズがインポート速度に影響します。解凍後のソース ファイルは 256 MiB 以下にすることをお勧めします。
> -   TiDB Lightning は個別に圧縮されたデータ ファイルのみをインポートし、複数のデータ ファイルが含まれる単一の圧縮ファイルのインポートはサポートしていません。
> -   TiDB Lightning は、 `db.table.parquet.snappy`などの別の圧縮ツールで圧縮された`parquet`ファイルをサポートしていません。 `parquet`ファイルを圧縮する場合は、 `parquet`ファイル ライターの圧縮形式を設定できます。
> -   TiDB Lightning v6.4.0 以降のバージョンでは、次の圧縮データ ファイルのみがサポートされています: `gzip` 、 `snappy` 、および`zstd` 。その他の種類のファイルではエラーが発生します。ソース データ ファイルが保存されているディレクトリにサポートされていない圧縮ファイルが存在する場合、タスクによってエラーが報告されます。このようなエラーを回避するには、サポートされていないファイルをインポート データ ディレクトリから移動します。
> -   Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)である必要があります。Snappy 圧縮の他のバリエーションはサポートされていません。

## カスタマイズされたファイルを一致させる {#match-customized-files}

TiDB Lightning は、命名パターンに従うデータ ファイルのみを認識します。場合によっては、データ ファイルが命名パターンに従っていないことがあり、その場合はファイルをインポートせずにデータのインポートが短時間で完了します。

この問題を解決するには、カスタマイズした式でデータ ファイルを一致させるために`[[mydumper.files]]`使用します。

S3 にエクスポートされたAuroraスナップショットを例に挙げます。Parquet ファイルの完全なパスは`S3://some-bucket/some-subdir/some-database/some-database.some-table/part-00000-c5a881bb-58ff-4ee6-1111-b41ecff340a3-c000.gz.parquet`です。

通常、 `some-database`データベースをインポートするには、 `data-source-dir` `S3://some-bucket/some-subdir/some-database/`に設定します。

前述の Parquet ファイル パスに基づいて、 `(?i)^(?:[^/]*/)*([a-z0-9\-_]+).([a-z0-9\-_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$`ような正規表現を記述してファイルを一致させることができます。一致グループでは、 `index=1`は`some-database` 、 `index=2`は`some-table` 、 `index=3`は`parquet`です。

デフォルトの命名規則に従わないデータ ファイルをTiDB Lightning が認識できるように、正規表現と対応するインデックスに従って構成ファイルを記述できます。例:

```toml
[[mydumper.files]]
# The expression needed for parsing the Amazon Aurora parquet file
pattern = '(?i)^(?:[^/]*/)*([a-z0-9\-_]+).([a-z0-9\-_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'
schema = '$1'
table = '$2'
type = '$3'
```

-   **schema** : ターゲット データベースの名前。値は次のとおりです。
    -   正規表現を使用して取得されたグループ インデックス (例: `$1` )。
    -   インポートするデータベースの名前 (例: `db1` )。一致したすべてのファイルは`db1`にインポートされます。
-   **table** : 対象テーブルの名前。値は次のとおりです。
    -   正規表現を使用して取得されたグループ インデックス (例: `$2` )。
    -   インポートするテーブルの名前 (例: `table1` )。一致したすべてのファイルは`table1`にインポートされます。
-   **type** : ファイルの種類。 `sql` 、 `parquet` 、 `csv`をサポートします。値は次のとおりです。
    -   正規表現を使用して取得されたグループ インデックス (例: `$3` )。
-   **key** : ファイル番号（例: `${db_name}.${table_name}.001.csv`の`001`など）。
    -   正規表現を使用して取得されたグループ インデックス (例: `$4` )。

## Amazon S3からデータをインポートする {#import-data-from-amazon-s3}

次の例は、 TiDB Lightning を使用して Amazon S3 からデータをインポートする方法を示しています。詳細なパラメータ設定については、 [外部ストレージサービスの URI 形式](/external-storage-uri.md)参照してください。

-   ローカルに設定された権限を使用して S3 データにアクセスします。

    ```bash
    tiup tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/sql-backup'
    ```

-   パス形式のリクエストを使用して S3 データにアクセスします。

    ```bash
    tiup tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/sql-backup?force-path-style=true&endpoint=http://10.154.10.132:8088'
    ```

-   特定の AWS IAMロール ARN を使用して S3 データにアクセスします。

    ```bash
    tiup tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/test-data?role-arn=arn:aws:iam::888888888888:role/my-role'
    ```

<!---->

-   AWS IAMユーザーのアクセスキーを使用して S3 データにアクセスします。

    ```bash
    tiup tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/test-data?access_key={my_access_key}&secret_access_key={my_secret_access_key}'
    ```

-   AWS IAMロールアクセスキーとセッショントークンの組み合わせを使用して、S3 データにアクセスします。

    ```bash
    tiup tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/test-data?access_key={my_access_key}&secret_access_key={my_secret_access_key}&session-token={my_session_token}'
    ```

## その他のリソース {#more-resources}

-   [Dumplingを使用してCSVファイルにエクスポートする](/dumpling-overview.md#export-to-csv-files)
-   [`LOAD DATA`](https://dev.mysql.com/doc/refman/8.0/en/load-data.html)
