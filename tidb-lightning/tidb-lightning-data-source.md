---
title: TiDB Lightning Data Sources
summary: TiDB Lightningでサポートされているすべてのデータ ソースについて説明します。
---

# TiDB Lightningデータソース {#tidb-lightning-data-sources}

TiDB Lightning は、CSV、SQL、Parquet ファイルなど、複数のデータ ソースから TiDB クラスターへのデータのインポートをサポートしています。

TiDB Lightningのデータ ソースを指定するには、次の構成を使用します。

```toml
[mydumper]
# Local source data directory or the URI of the external storage such as S3. For more information about the URI of the external storage, see https://docs.pingcap.com/tidb/dev/backup-and-restore-storages#uri-format.
data-source-dir = "/data/my_database"
```

TiDB Lightningが実行されると、 `data-source-dir`パターンに一致するすべてのファイルが検索されます。

| ファイル     | タイプ                                                                                                                                                                                               | パターン                                                     |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| スキーマファイル | `CREATE TABLE` DDL文が含まれています                                                                                                                                                                       | `${db_name}.${table_name}-schema.sql`                    |
| スキーマファイル | `CREATE DATABASE` DDL文が含まれています                                                                                                                                                                    | `${db_name}-schema-create.sql`                           |
| データファイル  | データファイルにテーブル全体のデータが含まれている場合、ファイルは`${db_name}.${table_name}`名前のテーブルにインポートされます。                                                                                                                     | `${db_name}.${table_name}.${csv|sql|parquet}`            |
| データファイル  | テーブルのデータが複数のデータファイルに分割されている場合、各データファイルのファイル名に数字を付ける必要がある。                                                                                                                                         | `${db_name}.${table_name}.001.${csv|sql|parquet}`        |
| 圧縮ファイル   | ファイルに`gzip` 、 `snappy` 、 `zstd`などの圧縮サフィックスが含まれている場合、 TiDB Lightning はインポート前にファイルを解凍します。Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)形式である必要があります。その他の Snappy 圧縮形式はサポートされていません。 | `${db_name}.${table_name}.${csv|sql|parquet}.{compress}` |

TiDB Lightningは、可能な限り並列でデータを処理します。ファイルは順番に読み取る必要があるため、データ処理の同時実行性はファイルレベル（ `region-concurrency`で制御）で制御されます。そのため、インポートするファイルのサイズが大きい場合、インポートのパフォーマンスが低下します。最適なパフォーマンスを得るには、インポートするファイルのサイズを256MiB以下に制限することをお勧めします。

## データベースとテーブルの名前を変更する {#rename-databases-and-tables}

TiDB Lightningは、ファイル名のパターンに従って、対応するデータベースとテーブルにデータをインポートします。データベース名またはテーブル名が変更された場合は、ファイル名を変更してからインポートするか、正規表現を使用してオンラインで名前を置換することができます。

### ファイルを一括で名前変更 {#rename-files-in-batch}

Red Hat Linux または Red Hat Linux ベースのディストリビューションを使用している場合は、 `rename`コマンドを使用して、 `data-source-dir`ディレクトリ内のファイルの名前を一括変更することができます。

例えば：

```shell
rename srcdb. tgtdb. *.sql
```

データベース名を変更した後は、 `data-source-dir`ディレクトリから`CREATE DATABASE` DDL ステートメントを含む`${db_name}-schema-create.sql`ファイルを削除することをお勧めします。テーブル名も変更する場合は、 `CREATE TABLE` DDL ステートメントを含む`${db_name}.${table_name}-schema.sql`ファイル内のテーブル名も変更する必要があります。

### 正規表現を使用してオンラインで名前を置換する {#use-regular-expressions-to-replace-names-online}

正規表現を使ってオンラインで名前を置換するには、 `[[mydumper.files]]`内の`pattern`設定を使ってファイル名を一致させ、 `schema`と`table`希望の名前に置き換えます。詳細については、 [カスタマイズされたファイルを一致させる](#match-customized-files)参照してください。

以下は、正規表現を使用してオンラインで名前を置換する例です。この例では、

-   データファイル`pattern`の一致ルールは`^({schema_regrex})\.({table_regrex})\.({file_serial_regrex})\.(csv|parquet|sql)`です。
-   `schema`を`'$1'`と指定すると、最初の正規表現の値`schema_regrex`は変更されません。または、 `schema` `'tgtdb'`などの文字列として指定すると、固定のターゲットデータベース名になります。
-   `table`を`'$2'`と指定すると、2番目の正規表現の値`table_regrex`は変更されません。または、 `table` `'t1'`などの文字列として指定すると、固定のターゲットテーブル名になります。
-   `type` `'$3'` （データファイルの種類）として指定します。5 `type` `"table-schema"` （ `schema.sql`ファイル）または`"schema-schema"` （ `schema-create.sql`ファイル）として指定できます。

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

`gzip`使用してデータファイルをバックアップする場合は、それに応じて圧縮形式を設定する必要があります。データファイル`pattern`のマッチングルールは`'^({schema_regrex})\.({table_regrex})\.({file_serial_regrex})\.(csv|parquet|sql)\.(gz)'`です。圧縮ファイル形式を表すために、 `compression` `'$4'`として指定できます。例：

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

## CSV {#csv}

### スキーマ {#schema}

CSVファイルはスキーマレスです。CSVファイルをTiDBにインポートするには、テーブルスキーマを提供する必要があります。スキーマは、以下のいずれかの方法で提供できます。

-   DDL ステートメントを含む`${db_name}.${table_name}-schema.sql`および`${db_name}-schema-create.sql`名前のファイルを作成します。
-   TiDB にテーブル スキーマを手動で作成します。

### コンフィグレーション {#configuration}

CSV形式は、 `tidb-lightning.toml`ファイルの`[mydumper.csv]`セクションで設定できます。ほとんどの設定には、MySQLの[`LOAD DATA`](https://dev.mysql.com/doc/refman/8.0/en/load-data.html)ステートメントに対応するオプションがあります。

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

`separator` 、 `delimiter` 、 `terminator`などの文字列フィールドに特殊文字を入力する場合、バックスラッシュを使用して特殊文字をエスケープできます。エスケープシーケンスは*二重引用符で囲まれた*文字列（ `"…"` ）である必要があります。例えば、 `separator = "\u001f"` ASCII文字`0X1F`区切り文字として使用することを意味します。

*シングルクォーテーションで囲まれた*文字列 ( `'…'` ) を使用すると、バックスラッシュによるエスケープを抑制できます。例えば、 `terminator = '\n'` 、LF `\n`ではなく、バックスラッシュ ( `\` ) と文字`n`の2文字の文字列を終端として使用することを意味します。

詳細については[TOML v1.0.0仕様](https://toml.io/en/v1.0.0#string)参照してください。

#### <code>separator</code> {#code-separator-code}

-   フィールドセパレーターを定義します。

-   1 文字または複数文字を使用できますが、空にすることはできません。

-   共通の値:

    -   CSV (カンマ区切り値)の場合は`','` 。
    -   TSV (タブ区切り値)の場合は`"\t"` 。
    -   `"\u0001"`指定すると ASCII 文字`0x01`使用されます。

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
-   `terminator`が空の場合、行末文字として`"\n"` (改行) と`"\r\n"` (復帰 + 改行) の両方が使用されます。
-   `LOAD DATA`ステートメントの`LINES TERMINATED BY`オプションに対応します。

#### <code>header</code> {#code-header-code}

-   *すべての*CSV ファイルにヘッダー行が含まれているかどうか。
-   `header`が`true`場合、最初の行は*列名*として使用されます。7 が`header` `false`場合、最初の行は通常のデータ行として扱われます。

#### <code>not-null</code>と<code>null</code> {#code-not-null-code-and-code-null-code}

-   `not-null`設定は、すべてのフィールドが null 不可かどうかを制御します。
-   `not-null`が`false`の場合、 `null`で指定された文字列は特定の値ではなく SQL NULL に変換されます。
-   引用符で囲んでも、フィールドが null かどうかには影響しません。

    たとえば、次の CSV ファイルでは、

    ```csv
    A,B,C
    \N,"\N",
    ```

    デフォルト設定（ `not-null = false; null = '\N'` ）では、列`A`と`B` TiDBにインポートされた後、両方ともNULLに変換されます。列`C`空文字列`''`ですが、NULLではありません。

#### <code>backslash-escape</code> {#code-backslash-escape-code}

-   フィールド内のバックスラッシュをエスケープ文字として解析するかどうか。

-   `backslash-escape`が真の場合、次のシーケンスが認識され、変換されます。

    | シーケンス | 変換された                    |
    | ----- | ------------------------ |
    | `\0`  | ヌル文字（ `U+0000` ）         |
    | `\b`  | バックスペース ( `U+0008` )     |
    | `\n`  | 改行（ `U+000A` ）           |
    | `\r`  | キャリッジリターン（ `U+000D` ）    |
    | `\t`  | タブ ( `U+0009` )          |
    | `\Z`  | Windows EOF ( `U+001A` ) |

    それ以外の場合（例えば`\"` ）、バックスラッシュは削除され、次の文字（ `"` ）がフィールドに残ります。残された文字は特別な役割（例えば区切り文字）を持たず、通常の文字として扱われます。

-   引用符で囲んでも、バックスラッシュがエスケープ文字として解析されるかどうかには影響しません。

-   `LOAD DATA`ステートメントの`FIELDS ESCAPED BY '\'`オプションに対応します。

#### <code>trim-last-separator</code> {#code-trim-last-separator-code}

-   `separator`行末文字として扱い、すべての末尾の区切り文字を削除するかどうか。

    たとえば、次の CSV ファイルでは、

    ```csv
    A,,B,,
    ```

    -   `trim-last-separator = false`場合、これは 5 つのフィールド`('A', '', 'B', '', '')`の行として解釈されます。
    -   `trim-last-separator = true`場合、これは 3 つのフィールド`('A', '', 'B')`の行として解釈されます。

-   このオプションは非推奨です。代わりにオプション`terminator`使用してください。

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

TiDB Lightningは、 `LOAD DATA`文でサポートされているすべてのオプションをサポートしているわけではありません。例えば：

-   行頭語( `LINES STARTING BY` )は使用できません。
-   ヘッダーはスキップできません（ `IGNORE n LINES` ）、有効な列名である必要があります。

### 厳格なフォーマット {#strict-format}

TiDB Lightningは、入力ファイルのサイズが256MiB程度に均一である場合に最も効果的に機能します。入力が単一の巨大なCSVファイルである場合、 TiDB Lightningはファイルを1つのスレッドでしか処理できないため、インポート速度が低下します。

これは、CSVをまず複数のファイルに分割することで解決できます。一般的なCSV形式では、ファイル全体を読み込まなければ行の開始位置と終了位置を素早く特定する方法がありません。そのため、 TiDB LightningはデフォルトではCSVファイルを自動的に分割し*ません*。ただし、CSV入力が特定の制限に準拠していることが確実な場合は、 `strict-format`設定を有効にすると、 TiDB Lightningがファイルを256MiBサイズの複数のチャンクに分割して並列処理できるようになります。

```toml
[mydumper]
strict-format = true
```

厳密なCSVファイルでは、各フィールドは1行のみに収まります。つまり、次のいずれかの条件を満たす必要があります。

-   区切り文字が空です。
-   各フィールドにはターミネータ自体が含まれません。デフォルト設定では、これは各フィールドに CR ( `\r` ) または LF ( `\n` ) が含まれないことを意味します。

CSV ファイルが厳密ではなく、 `strict-format`が誤って`true`に設定されている場合、複数行にまたがるフィールドが 2 つのチャンクに分割され、解析が失敗したり、破損したデータが暗黙的にインポートされたりする可能性があります。

### 一般的な構成例 {#common-configuration-examples}

#### CSV {#csv}

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

#### TSV {#tsv}

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

## SQL {#sql}

TiDB Lightning TiDB LightningはSQLファイルを処理する際に、単一のSQLファイルを迅速に分割できないため、同時実行性を高めて単一ファイルのインポート速度を向上させることができません。そのため、SQLファイルからデータをインポートする際は、巨大なSQLファイルを1つだけ使用することは避けてください。TiDB TiDB Lightningは、入力ファイルのサイズが256MiB程度に均一である場合に最も効果的に動作します。

## 寄木細工 {#parquet}

TiDB Lightningは現在、Amazon Aurora、Apache Hive、Snowflakeによって生成されたParquetファイルのみをサポートしています。S3内のファイル構造を識別するには、以下の設定を使用してすべてのデータファイルを一致させてください。

    [[mydumper.files]]
    # The expression needed for parsing Amazon Aurora parquet files
    pattern = '(?i)^(?:[^/]*/)*([a-z0-9\-_]+).([a-z0-9\-_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'
    schema = '$1'
    table = '$2'
    type = '$3'

この設定は、 Auroraスナップショットによってエクスポートされた parquet ファイルを一致させる方法のみを示しています。スキーマファイルは別途エクスポートして処理する必要があります。

`mydumper.files`詳細については[カスタマイズされたファイルに一致](#match-customized-files)を参照してください。

## 圧縮ファイル {#compressed-files}

TiDB Lightningは現在、 Dumplingでエクスポートされた圧縮ファイル、または命名規則に従った圧縮ファイルをサポートしています。現在、 TiDB Lightningは`gzip` `snappy`圧縮アルゴリズムをサポートしています。ファイル名が命名規則に従っている場合、 TiDB Lightningは`zstd`に圧縮アルゴリズムを識別し、追加の設定なしでストリーミング解凍後にファイルをインポートします。

> **注記：**
>
> -   TiDB Lightningは単一の大きな圧縮ファイルを同時に解凍できないため、圧縮ファイルのサイズはインポート速度に影響します。解凍後のソースファイルは256MiB以下にすることをお勧めします。
> -   TiDB Lightning は個別に圧縮されたデータ ファイルのみをインポートし、複数のデータ ファイルが含まれる単一の圧縮ファイルのインポートはサポートしていません。
> -   TiDB Lightningは、 `db.table.parquet.snappy`などの他の圧縮ツールで圧縮された`parquet`ファイル`parquet` `parquet`ライターの圧縮形式を設定できます。
> -   TiDB Lightning v6.4.0以降のバージョンでは、 `gzip` `snappy`圧縮データファイルのみがサポートされています。その他の種類のファイルはエラーの原因となります。ソースデータファイルが保存されているディレクトリにサポートされていない圧縮ファイルが存在する場合、タスク`zstd`エラーを報告します。このようなエラーを回避するには、サポートされていないファイルをインポートデータディレクトリから移動してください。
> -   Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)である必要があります。その他の Snappy 圧縮形式はサポートされていません。

## カスタマイズされたファイルを一致させる {#match-customized-files}

TiDB Lightningは、命名パターンに従ったデータファイルのみを認識します。場合によっては、データファイルが命名パターンに従っていない可能性があり、その場合、ファイルのインポートなしでデータのインポートが短時間で完了します。

この問題を解決するには、カスタマイズした式でデータ ファイルを一致させるために`[[mydumper.files]]`使用します。

S3にエクスポートされたAuroraスナップショットを例に挙げます。Parquetファイルの完全パスは`S3://some-bucket/some-subdir/some-database/some-database.some-table/part-00000-c5a881bb-58ff-4ee6-1111-b41ecff340a3-c000.gz.parquet`です。

通常、 `some-database`データベースをインポートするには、 `data-source-dir` `S3://some-bucket/some-subdir/some-database/`に設定します。

上記のParquetファイルパスに基づいて、 `(?i)^(?:[^/]*/)*([a-z0-9\-_]+).([a-z0-9\-_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$`ような正規表現を記述することでファイルに一致させることができます。一致グループでは、 `index=1`は`some-database` `index=2` `some-table`は`index=3` `parquet`なります。

デフォルトの命名規則に従わないデータファイルをTiDB Lightningが認識できるように、正規表現と対応するインデックスに従って設定ファイルを記述することができます。例：

```toml
[[mydumper.files]]
# The expression needed for parsing the Amazon Aurora parquet file
pattern = '(?i)^(?:[^/]*/)*([a-z0-9\-_]+).([a-z0-9\-_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'
schema = '$1'
table = '$2'
type = '$3'
```

-   **schema** : 対象データベースの名前。値は次のいずれかです。
    -   正規表現を使用して取得されたグループ インデックス (例: `$1` )。
    -   インポートするデータベースの名前（例： `db1` ）。一致したすべてのファイルは`db1`にインポートされます。
-   **table** : 対象テーブルの名前。値は次のいずれかです。
    -   正規表現を使用して取得されたグループ インデックス (例: `$2` )。
    -   インポートするテーブルの名前（例： `table1` ）。一致したすべてのファイルは`table1`にインポートされます。
-   **type** : ファイルの種類`sql` `parquet`サポートします。値は`csv`のとおりです。
    -   正規表現を使用して取得されたグループ インデックス (例: `$3` )。
-   **key** : ファイル番号 (例: `${db_name}.${table_name}.001.csv`の場合は`001` 。
    -   正規表現を使用して取得されたグループ インデックス (例: `$4` )。

## Amazon S3からデータをインポートする {#import-data-from-amazon-s3}

以下の例は、TiDB Lightningを使用して Amazon S3 からデータをインポートする方法を示しています。詳細なパラメータ設定については、 [外部ストレージサービスのURI形式](/external-storage-uri.md)参照してください。

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
