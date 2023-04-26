---
title: TiDB Lightning Data Sources
summary: Learn all the data sources supported by TiDB Lightning.
---

# TiDB Lightningデータソース {#tidb-lightning-data-sources}

TiDB Lightning は、CSV、SQL、Parquet ファイルなど、複数のデータ ソースから TiDB クラスターへのデータのインポートをサポートしています。

TiDB Lightningのデータ ソースを指定するには、次の構成を使用します。

```toml
[mydumper]
# Local source data directory or the URL of the external storage such as S3.
data-source-dir = "/data/my_database"
```

TiDB Lightningの実行中は、パターン`data-source-dir`に一致するすべてのファイルが検索されます。

| ファイル      | タイプ                                                                                      | パターン                                                     |
| --------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| スキーマ ファイル | `CREATE TABLE` DDL ステートメントを含む                                                            | `${db_name}.${table_name}-schema.sql`                    |
| スキーマ ファイル | `CREATE DATABASE` DDL ステートメントを含む                                                         | `${db_name}-schema-create.sql`                           |
| データファイル   | データ ファイルにテーブル全体のデータが含まれている場合、ファイルは`${db_name}.${table_name}`という名前のテーブルにインポートされます。        | `${db_name}.${table_name}.${csv|sql|parquet}`            |
| データファイル   | テーブルのデータが複数のデータ ファイルに分割されている場合は、各データ ファイルのファイル名の末尾に数字を付ける必要があります。                        | `${db_name}.${table_name}.001.${csv|sql|parquet}`        |
| 圧縮ファイル    | ファイルに`gzip` 、 `snappy` 、または`zstd`などの圧縮接尾辞が含まれている場合、 TiDB Lightning はファイルをインポートする前に解凍します。 | `${db_name}.${table_name}.${csv|sql|parquet}.{compress}` |

TiDB Lightning はデータを可能な限り並行して処理します。ファイルは順番に読み取る必要があるため、データ処理の同時実行性はファイル レベル ( `region-concurrency`で制御) になります。そのため、インポートしたファイルが大きい場合、インポートのパフォーマンスが低下します。最高のパフォーマンスを実現するには、インポートするファイルのサイズを 256 MiB 以下に制限することをお勧めします。

## CSV {#csv}

### スキーマ {#schema}

CSV ファイルはスキーマレスです。 CSV ファイルを TiDB にインポートするには、テーブル スキーマを提供する必要があります。次のいずれかの方法でスキーマを提供できます。

-   DDL ステートメントを含む`${db_name}.${table_name}-schema.sql`および`${db_name}-schema-create.sql`という名前のファイルを作成します。
-   TiDB でテーブル スキーマを手動で作成します。

### コンフィグレーション {#configuration}

`tidb-lightning.toml`ファイルの`[mydumper.csv]`セクションで CSV 形式を設定できます。ほとんどの設定には、MySQL の[`LOAD DATA`](https://dev.mysql.com/doc/refman/8.0/en/load-data.html)ステートメントに対応するオプションがあります。

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

`separator` 、 `delimiter` 、または`terminator`などの文字列フィールドの入力に特殊文字が含まれる場合、バックスラッシュを使用して特殊文字をエスケープできます。エスケープ シーケンスは、*二重引用*符で囲まれた文字列 ( `"…"` ) である必要があります。たとえば、 `separator = "\u001f"` ASCII 文字`0X1F`セパレータとして使用することを意味します。

*単一引用*符で囲まれた文字列 ( `'…'` ) を使用して、バックスラッシュのエスケープを抑制することができます。たとえば、 `terminator = '\n'` 、LF `\n`ではなく、バックスラッシュ ( `\` ) の後に文字`n`が続く 2 文字の文字列をターミネータとして使用することを意味します。

詳細については、 [TOML v1.0.0 仕様](https://toml.io/en/v1.0.0#string)参照してください。

#### <code>separator</code> {#code-separator-code}

-   フィールド区切りを定義します。

-   1 つまたは複数の文字を指定できますが、空にすることはできません。

-   一般的な値:

    -   CSV (コンマ区切り値) の場合は`','` 。
    -   TSV (タブ区切り値) の場合は`"\t"` 。
    -   `"\u0001"`は ASCII 文字を使用します`0x01` .

-   LOAD DATA ステートメントの`FIELDS TERMINATED BY`オプションに対応します。

#### <code>delimiter</code> {#code-delimiter-code}

-   引用に使用する区切り文字を定義します。

-   `delimiter`が空の場合、すべてのフィールドは引用符で囲まれていません。

-   一般的な値:

    -   `'"'`二重引用符でフィールドを引用します。 [RFC4180](https://tools.ietf.org/html/rfc4180)と同じ。
    -   `''`引用を無効にします。

-   `LOAD DATA`ステートメントの`FIELDS ENCLOSED BY`オプションに対応します。

#### <code>terminator</code> {#code-terminator-code}

-   行末記号を定義します。
-   `terminator`が空の場合、 `"\n"` (ライン フィード) と`"\r\n"` (キャリッジ リターン + ライン フィード) の両方が行末記号として使用されます。
-   `LOAD DATA`ステートメントの`LINES TERMINATED BY`オプションに対応します。

#### <code>header</code> {#code-header-code}

-   *すべての*CSV ファイルにヘッダー行が含まれているかどうか。
-   `header`が`true`の場合、最初の行が*列名*として使用されます。 `header`が`false`の場合、最初の行は通常のデータ行として扱われます。

#### <code>not-null</code>および<code>null</code> {#code-not-null-code-and-code-null-code}

-   `not-null`設定は、すべてのフィールドが null 非許容であるかどうかを制御します。
-   `not-null`が`false`の場合、 `null`で指定された文字列は、特定の値ではなく SQL NULL に変換されます。
-   引用符は、フィールドが null であるかどうかには影響しません。

    たとえば、次の CSV ファイルでは次のようになります。

    ```csv
    A,B,C
    \N,"\N",
    ```

    デフォルト設定 ( `not-null = false; null = '\N'` ) では、列`A`と`B`は両方とも、TiDB にインポートされた後に NULL に変換されます。列`C`は空の文字列`''`ですが、NULL ではありません。

#### <code>backslash-escape</code> {#code-backslash-escape-code}

-   フィールド内のバックスラッシュをエスケープ文字として解析するかどうか。

-   `backslash-escape`が true の場合、次のシーケンスが認識され、変換されます。

    | シーケンス | に変換                      |
    | ----- | ------------------------ |
    | `\0`  | 空文字 ( `U+0000` )         |
    | `\b`  | バックスペース ( `U+0008` )     |
    | `\n`  | 改行 ( `U+000A` )          |
    | `\r`  | キャリッジリターン ( `U+000D` )   |
    | `\t`  | タブ ( `U+0009` )          |
    | `\Z`  | Windows EOF ( `U+001A` ) |

    他のすべての場合 (たとえば、 `\"` ) では、バックスラッシュが取り除かれ、フィールドに次の文字 ( `"` ) が残ります。左の文字には特別な役割 (区切り文字など) はなく、単なる通常の文字です。

-   引用符は、バックスラッシュがエスケープ文字として解析されるかどうかには影響しません。

-   `LOAD DATA`ステートメントの`FIELDS ESCAPED BY '\'`オプションに対応します。

#### <code>trim-last-separator</code> {#code-trim-last-separator-code}

-   `separator`行終端記号として扱い、末尾の区切り文字をすべて削除するかどうか。

    たとえば、次の CSV ファイルでは次のようになります。

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

#### 構成不可能なオプション {#non-configurable-options}

TiDB Lightning は、 `LOAD DATA`ステートメントでサポートされているすべてのオプションをサポートしているわけではありません。例えば：

-   行のプレフィックス ( `LINES STARTING BY` ) は使用できません。
-   ヘッダーはスキップできず ( `IGNORE n LINES` )、有効な列名でなければなりません。

### 厳密な形式 {#strict-format}

TiDB Lightning は、入力ファイルが約 256 MiB の均一なサイズである場合に最適に機能します。入力が単一の巨大な CSV ファイルの場合、 TiDB Lightning は1 つのスレッドでしかファイルを処理できないため、インポート速度が遅くなります。

これは、最初に CSV を複数のファイルに分割することで修正できます。一般的な CSV 形式の場合、ファイル全体を読み取らずに行の開始位置と終了位置をすばやく特定する方法はありません。したがって、デフォルトでは、 TiDB Lightning はCSV ファイルを自動的に分割しませ*ん*。ただし、CSV 入力が特定の制限に準拠していることが確実な場合は、 `strict-format`設定を有効にして、 TiDB Lightning がファイルを複数の 256 MiB サイズのチャンクに分割して並列処理できるようにすることができます。

```toml
[mydumper]
strict-format = true
```

厳密な CSV ファイルでは、すべてのフィールドが 1 行だけを占めます。つまり、次のいずれかに該当する必要があります。

-   区切り文字が空です。
-   すべてのフィールドにターミネータ自体が含まれているわけではありません。デフォルトの構成では、これはすべてのフィールドに CR ( `\r` ) または LF ( `\n` ) が含まれていないことを意味します。

CSV ファイルが厳密ではなく、 `strict-format`誤って`true`に設定されている場合、複数行にまたがるフィールドが半分に分割されて 2 つのチャンクになり、解析が失敗したり、破損したデータが静かにインポートされたりすることさえあります。

### 一般的な構成例 {#common-configuration-examples}

#### CSV {#csv}

デフォルト設定は、RFC 4180 に従って CSV 用に調整済みです。

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

```
ID,Region,Count
1,"East",32
2,"South",\N
3,"West",10
4,"North",39
```

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

```
ID    Region    Count
1     East      32
2     South     NULL
3     West      10
4     North     39
```

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

```
1|East|32|
2|South|0|
3|West|10|
4|North|39|
```

## SQL {#sql}

TiDB Lightning がSQL ファイルを処理するとき、 TiDB Lightning は単一の SQL ファイルをすばやく分割できないため、同時実行性を高めて単一ファイルのインポート速度を向上させることはできません。したがって、SQL ファイルからデータをインポートする場合は、単一の巨大な SQL ファイルを避けてください。 TiDB Lightning は、入力ファイルが約 256 MiB の均一なサイズである場合に最適に機能します。

## 寄木細工 {#parquet}

TiDB Lightning は現在、Amazon Auroraまたは Apache Hive によって生成された Parquet ファイルのみをサポートしています。 S3 のファイル構造を識別するには、次の構成を使用してすべてのデータ ファイルを照合します。

```
[[mydumper.files]]
# The expression needed for parsing Amazon Aurora parquet files
pattern = '(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'
schema = '$1'
table = '$2'
type = '$3'
```

この設定は、 Auroraスナップショットによってエクスポートされた寄木細工のファイルを一致させる方法のみを示していることに注意してください。スキーマ ファイルを個別にエクスポートして処理する必要があります。

`mydumper.files`の詳細については、 [カスタマイズされたファイルに一致](#match-customized-files)を参照してください。

## 圧縮ファイル {#compressed-files}

TiDB Lightning は現在、 Dumplingによってエクスポートされた圧縮ファイル、または命名規則に従う圧縮ファイルをサポートしています。現在、 TiDB Lightning は次の圧縮アルゴリズムをサポートしています: `gzip` 、 `snappy` 、および`zstd` 。ファイル名が命名規則に従っている場合、 TiDB Lightning は圧縮アルゴリズムを自動的に識別し、追加の構成を行わなくても、ストリーミング解凍後にファイルをインポートします。

> **ノート：**
>
> -   TiDB Lightning は単一の大きな圧縮ファイルを同時に解凍できないため、圧縮ファイルのサイズはインポート速度に影響します。ソース ファイルは、解凍後に 256 MiB を超えないようにすることをお勧めします。
> -   TiDB Lightning は個別に圧縮されたデータ ファイルのみをインポートし、複数のデータ ファイルが含まれる単一の圧縮ファイルのインポートはサポートしていません。
> -   TiDB Lightning は、 `db.table.parquet.snappy`などの別の圧縮ツールで圧縮された`parquet`ファイルをサポートしていません。 `parquet`ファイルを圧縮する場合は、 `parquet`ファイル ライターの圧縮形式を構成できます。
> -   TiDB Lightning v6.4.0 以降のバージョンでは、 `.bak`ファイルと次の圧縮データ ファイルのみがサポートされます: `gzip` 、 `snappy` 、および`zstd` 。他のタイプのファイルはエラーの原因になります。サポートされていないファイルについては、事前にファイル名を変更するか、これらのファイルをインポート データ ディレクトリから移動して、このようなエラーを回避する必要があります。

## カスタマイズされたファイルを一致させる {#match-customized-files}

TiDB Lightning は、命名パターンに従うデータ ファイルのみを認識します。場合によっては、データ ファイルが命名パターンに従っていない可能性があるため、データ インポートはファイルをインポートせずに短時間で完了します。

この問題を解決するには、 `[[mydumper.files]]`を使用して、カスタマイズした式でデータ ファイルを一致させることができます。

例として、S3 にエクスポートされたAuroraスナップショットを取り上げます。 Parquet ファイルの完全なパスは`S3://some-bucket/some-subdir/some-database/some-database.some-table/part-00000-c5a881bb-58ff-4ee6-1111-b41ecff340a3-c000.gz.parquet`です。

通常、 `some-database`データベースをインポートするには、 `data-source-dir`を`S3://some-bucket/some-subdir/some-database/`に設定します。

前述の Parquet ファイル パスに基づいて、 `(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$`のような正規表現を記述してファイルを一致させることができます。一致グループでは、 `index=1`は`some-database` 、 `index=2`は`some-table` 、 `index=3`は`parquet`です。

デフォルトの命名規則に従わないデータ ファイルをTiDB Lightning が認識できるように、正規表現と対応するインデックスに従って構成ファイルを作成できます。例えば：

```toml
[[mydumper.files]]
# The expression needed for parsing the Amazon Aurora parquet file
pattern = '(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'
schema = '$1'
table = '$2'
type = '$3'
```

-   **schema** : ターゲット データベースの名前。値は次のとおりです。
    -   `$1`などの正規表現を使用して取得したグループ インデックス。
    -   `db1`など、インポートするデータベースの名前。一致したすべてのファイルが`db1`にインポートされます。
-   **table** : ターゲット テーブルの名前。値は次のとおりです。
    -   `$2`などの正規表現を使用して取得したグループ インデックス。
    -   `table1`など、インポートするテーブルの名前。一致したすべてのファイルが`table1`にインポートされます。
-   **type** : ファイルの種類。 `sql` 、 `parquet` 、および`csv`をサポートします。値は次のとおりです。
    -   `$3`などの正規表現を使用して取得したグループ インデックス。
-   **key** : `001` in `${db_name}.${table_name}.001.csv`などのファイル番号。
    -   `$4`などの正規表現を使用して取得したグループ インデックス。

## Amazon S3 からデータをインポートする {#import-data-from-amazon-s3}

次の例は、 TiDB Lightningを使用して Amazon S3 からデータをインポートする方法を示しています。その他のパラメーター構成については、 [外部storageURL](/br/backup-and-restore-storages.md#url-format)を参照してください。

-   TiDB Lightning を使用して S3 からデータをインポートします。

    ```bash
    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/sql-backup'
    ```

-   TiDB Lightningを使用して S3 からデータをインポートします (パス スタイルのリクエストを使用)。

    ```bash
    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/sql-backup?force-path-style=true&endpoint=http://10.154.10.132:8088'
    ```

-   TiDB Lightningを使用して S3 からデータをインポートします (特定のIAMロールを使用して S3 データにアクセスします)。

    ```bash
    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/test-data?role-arn=arn:aws:iam::888888888888:role/my-role'
    ```

## その他のリソース {#more-resources}

-   [Dumplingを使用して CSV ファイルにエクスポートする](/dumpling-overview.md#export-to-csv-files)
-   [`LOAD DATA`](https://dev.mysql.com/doc/refman/8.0/en/load-data.html)
