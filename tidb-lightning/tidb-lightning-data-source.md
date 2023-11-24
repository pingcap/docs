---
title: TiDB Lightning Data Sources
summary: Learn all the data sources supported by TiDB Lightning.
---

# TiDB Lightningデータ ソース {#tidb-lightning-data-sources}

TiDB Lightning は、CSV、SQL、Parquet ファイルなど、複数のデータ ソースから TiDB クラスターへのデータのインポートをサポートします。

TiDB Lightningのデータ ソースを指定するには、次の構成を使用します。

```toml
[mydumper]
# Local source data directory or the URI of the external storage such as S3. For more information about the URI of the external storage, see https://docs.pingcap.com/tidb/v6.6/backup-and-restore-storages#uri-format.
data-source-dir = "/data/my_database"
```

TiDB Lightningの実行中は、 `data-source-dir`のパターンに一致するすべてのファイルを検索します。

| ファイル     | タイプ                                                                                                                                                                                                                  | パターン                                                     |
| -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| スキーマファイル | `CREATE TABLE` DDL ステートメントが含まれます                                                                                                                                                                                     | `${db_name}.${table_name}-schema.sql`                    |
| スキーマファイル | `CREATE DATABASE` DDL ステートメントが含まれます                                                                                                                                                                                  | `${db_name}-schema-create.sql`                           |
| データファイル  | データ ファイルにテーブル全体のデータが含まれている場合、ファイルは`${db_name}.${table_name}`という名前のテーブルにインポートされます。                                                                                                                                    | `${db_name}.${table_name}.${csv|sql|parquet}`            |
| データファイル  | テーブルのデータが複数のデータ ファイルに分割されている場合、各データ ファイルのファイル名の末尾に番号を付ける必要があります。                                                                                                                                                     | `${db_name}.${table_name}.001.${csv|sql|parquet}`        |
| 圧縮ファイル   | ファイルに`gzip` 、 `snappy` 、または`zstd`などの圧縮接尾辞が含まれている場合、 TiDB Lightning はファイルをインポートする前にファイルを解凍します。 Snappy 圧縮ファイルは[公式の Snappy フォーマット](https://github.com/google/snappy)にある必要があることに注意してください。 Snappy 圧縮の他のバリアントはサポートされていません。 | `${db_name}.${table_name}.${csv|sql|parquet}.{compress}` |

TiDB Lightning は、データを可能な限り並行して処理します。ファイルは順番に読み取る必要があるため、データ処理の同時実行性はファイル レベル ( `region-concurrency`で制御) になります。したがって、インポートされるファイルが大きい場合、インポートのパフォーマンスが低下します。最高のパフォーマンスを実現するには、インポートされるファイルのサイズを 256 MiB 以下に制限することをお勧めします。

## CSV {#csv}

### スキーマ {#schema}

CSV ファイルにはスキーマがありません。 CSV ファイルを TiDB にインポートするには、テーブル スキーマを提供する必要があります。次のいずれかの方法でスキーマを提供できます。

-   DDL ステートメントを含む`${db_name}.${table_name}-schema.sql`および`${db_name}-schema-create.sql`という名前のファイルを作成します。
-   TiDB にテーブル スキーマを手動で作成します。

### コンフィグレーション {#configuration}

CSV形式は、 `tidb-lightning.toml`ファイルの`[mydumper.csv]`セクションで設定できます。ほとんどの設定には、MySQL の[`LOAD DATA`](https://dev.mysql.com/doc/refman/8.0/en/load-data.html)ステートメントに対応するオプションがあります。

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

`separator` 、 `delimiter` 、または`terminator`などの文字列フィールドの入力に特殊文字が含まれる場合は、バックスラッシュを使用して特殊文字をエスケープできます。エスケープ シーケンスは*二重引用*符で囲まれた文字列 ( `"…"` ) である必要があります。たとえば、 `separator = "\u001f"` 、ASCII 文字`0X1F`区切り文字として使用することを意味します。

*一重引用*符で囲まれた文字列 ( `'…'` ) を使用すると、バックスラッシュのエスケープを抑制できます。たとえば、 `terminator = '\n'` 、LF `\n`ではなく、バックスラッシュ ( `\` ) とその後に文字`n`が続いた 2 文字の文字列をターミネータとして使用することを意味します。

詳細については、 [TOML v1.0.0 仕様](https://toml.io/en/v1.0.0#string)を参照してください。

#### <code>separator</code> {#code-separator-code}

-   フィールド区切り文字を定義します。

-   1 つまたは複数の文字を指定できますが、空にすることはできません。

-   一般的な値:

    -   CSV (カンマ区切り値) の場合は`','` 。
    -   TSV の場合は`"\t"` (タブ区切り値)。
    -   ASCII 文字を使用する場合は`"\u0001"` `0x01` 。

-   LOAD DATA ステートメントの`FIELDS TERMINATED BY`オプションに対応します。

#### <code>delimiter</code> {#code-delimiter-code}

-   引用符で使用する区切り文字を定義します。

-   `delimiter`が空の場合、すべてのフィールドは引用符で囲まれません。

-   一般的な値:

    -   `'"'`フィールドを二重引用符で囲みます。 [RFC 4180](https://tools.ietf.org/html/rfc4180)と同じ。
    -   `''`引用を無効にします。

-   `LOAD DATA`ステートメントの`FIELDS ENCLOSED BY`オプションに対応します。

#### <code>terminator</code> {#code-terminator-code}

-   行末文字を定義します。
-   `terminator`が空の場合、 `"\n"` (改行) と`"\r\n"` (復帰 + 改行) の両方が行終端文字として使用されます。
-   `LOAD DATA`ステートメントの`LINES TERMINATED BY`オプションに対応します。

#### <code>header</code> {#code-header-code}

-   *すべての*CSV ファイルにヘッダー行が含まれるかどうか。
-   `header`が`true`の場合、最初の行が*列名*として使用されます。 `header`が`false`の場合、最初の行は通常のデータ行として扱われます。

#### <code>not-null</code>と<code>null</code> {#code-not-null-code-and-code-null-code}

-   `not-null`設定は、すべてのフィールドが NULL 不可であるかどうかを制御します。
-   `not-null`が`false`の場合、 `null`で指定された文字列は、特定の値ではなく SQL NULL に変換されます。
-   引用符は、フィールドが null かどうかには影響しません。

    たとえば、次の CSV ファイルでは:

    ```csv
    A,B,C
    \N,"\N",
    ```

    デフォルト設定 ( `not-null = false; null = '\N'` ) では、列`A`と列`B`は両方とも TiDB にインポートされた後に NULL に変換されます。列`C`は空の文字列`''`ですが、NULL ではありません。

#### <code>backslash-escape</code> {#code-backslash-escape-code}

-   フィールド内のバックスラッシュをエスケープ文字として解析するかどうか。

-   `backslash-escape`が true の場合、次のシーケンスが認識され、変換されます。

    | シーケンス | に変換                      |
    | ----- | ------------------------ |
    | `\0`  | ヌル文字 ( `U+0000` )        |
    | `\b`  | バックスペース ( `U+0008` )     |
    | `\n`  | 改行 ( `U+000A` )          |
    | `\r`  | キャリッジリターン ( `U+000D` )   |
    | `\t`  | タブ ( `U+0009` )          |
    | `\Z`  | Windows EOF ( `U+001A` ) |

    他のすべての場合 (たとえば、 `\"` )、バックスラッシュは取り除かれ、次の文字 ( `"` ) がフィールドに残ります。左側の文字には特別な役割 (デリミタなど) はなく、単なる通常の文字です。

-   引用符は、バックスラッシュがエスケープ文字として解析されるかどうかには影響しません。

-   `LOAD DATA`ステートメントの`FIELDS ESCAPED BY '\'`オプションに対応します。

#### <code>trim-last-separator</code> {#code-trim-last-separator-code}

-   `separator`行末記号として扱い、末尾の区切り文字をすべてトリミングするかどうか。

    たとえば、次の CSV ファイルでは:

    ```csv
    A,,B,,
    ```

    -   `trim-last-separator = false`の場合、これは 5 つのフィールドの行として解釈されます`('A', '', 'B', '', '')` 。
    -   `trim-last-separator = true`の場合、これは 3 つのフィールドの行として解釈されます`('A', '', 'B')` 。

-   このオプションは廃止されました。代わりに`terminator`オプションを使用してください。

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

TiDB Lightning は、 `LOAD DATA`ステートメントでサポートされるすべてのオプションをサポートするわけではありません。例えば：

-   行プレフィックス ( `LINES STARTING BY` ) は使用できません。
-   ヘッダーはスキップできません ( `IGNORE n LINES` )。有効な列名である必要があります。

### 厳密な形式 {#strict-format}

TiDB Lightning は、入力ファイルのサイズが約 256 MiB の均一な場合に最適に機能します。入力が単一の巨大な CSV ファイルである場合、 TiDB Lightning はファイルを 1 つのスレッドでしか処理できないため、インポート速度が遅くなります。

この問題は、最初に CSV を複数のファイルに分割することで修正できます。一般的な CSV 形式の場合、ファイル全体を読み込まずに行の開始位置と終了位置をすばやく特定する方法はありません。したがって、 TiDB Lightning はデフォルトで CSV ファイルを自動的に分割しませ*ん*。ただし、CSV 入力が特定の制限に従っていることが確実な場合は、 `strict-format`設定を有効にして、 TiDB Lightning がファイルを複数の 256 MiB サイズのチャンクに分割して並列処理できるようにすることができます。

```toml
[mydumper]
strict-format = true
```

厳密な CSV ファイルでは、各フィールドは 1 行のみを占めます。つまり、次のいずれかが当てはまらなければなりません。

-   区切り文字が空です。
-   どのフィールドにもターミネータ自体は含まれません。デフォルト設定では、これはすべてのフィールドに CR ( `\r` ) または LF ( `\n` ) が含まれていないことを意味します。

CSV ファイルが厳密ではなく、誤って`strict-format`が`true`に設定されている場合、複数行にまたがるフィールドが半分の 2 つのチャンクに分割され、解析エラーが発生したり、破損したデータが静かにインポートされたりする可能性があります。

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

TiDB Lightning がSQL ファイルを処理する場合、 TiDB Lightning は単一の SQL ファイルを迅速に分割できないため、同時実行性を高めて単一ファイルのインポート速度を向上させることはできません。したがって、SQL ファイルからデータをインポートする場合は、単一の巨大な SQL ファイルを避けてください。 TiDB Lightning は、入力ファイルのサイズが約 256 MiB の均一な場合に最適に機能します。

## 寄木細工 {#parquet}

TiDB Lightning は現在、Amazon Auroraまたは Apache Hive によって生成された Parquet ファイルのみをサポートしています。 S3 のファイル構造を識別するには、次の構成を使用してすべてのデータ ファイルを照合します。

    [[mydumper.files]]
    # The expression needed for parsing Amazon Aurora parquet files
    pattern = '(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'
    schema = '$1'
    table = '$2'
    type = '$3'

この設定は、 Auroraスナップショットによってエクスポートされた寄木細工のファイルを照合する方法のみを示していることに注意してください。スキーマ ファイルを個別にエクスポートして処理する必要があります。

`mydumper.files`の詳細については、 [カスタマイズされたファイルと一致する](#match-customized-files)を参照してください。

## 圧縮ファイル {#compressed-files}

TiDB Lightning は現在、 Dumplingによってエクスポートされた圧縮ファイル、または命名規則に従った圧縮ファイルをサポートしています。現在、 TiDB Lightning は次の圧縮アルゴリズムをサポートしています: `gzip` 、 `snappy` 、および`zstd` 。ファイル名が命名規則に従っている場合、 TiDB Lightning は圧縮アルゴリズムを自動的に識別し、ストリーミング解凍後に追加の構成を行わずにファイルをインポートします。

> **注記：**
>
> -   TiDB Lightning は単一の大きな圧縮ファイルを同時に解凍できないため、圧縮ファイルのサイズはインポート速度に影響します。解凍後のソース ファイルのサイズは 256 MiB 以下であることをお勧めします。
> -   TiDB Lightning は、個別に圧縮されたデータ ファイルのみをインポートし、複数のデータ ファイルが含まれる単一の圧縮ファイルのインポートをサポートしません。
> -   TiDB Lightning は、 `parquet`などの別の圧縮ツールで圧縮されたファイルをサポートしていません`db.table.parquet.snappy` 。 `parquet`ファイルを圧縮する場合は、 `parquet`ファイル ライターの圧縮形式を設定できます。
> -   TiDB Lightning v6.4.0 以降のバージョンは、圧縮データ ファイル`gzip` 、 `snappy` 、および`zstd`のみをサポートします。他の種類のファイルではエラーが発生します。ソース データ ファイルが保存されているディレクトリにサポートされていない圧縮ファイルが存在する場合、タスクはエラーを報告します。このようなエラーを回避するには、サポートされていないファイルをインポート データ ディレクトリから移動します。
> -   Snappy 圧縮ファイルは[公式の Snappy フォーマット](https://github.com/google/snappy)に存在する必要があります。 Snappy 圧縮の他のバリアントはサポートされていません。

## カスタマイズされたファイルと一致する {#match-customized-files}

TiDB Lightning は、命名パターンに従ったデータ ファイルのみを認識します。場合によっては、データ ファイルが命名パターンに従っていない可能性があるため、ファイルをインポートせずにデータのインポートが短時間で完了します。

この問題を解決するには、カスタマイズした式で`[[mydumper.files]]`​​を使用してデータ ファイルを照合します。

S3 にエクスポートされたAuroraスナップショットを例に挙げます。 Parquet ファイルの完全なパスは`S3://some-bucket/some-subdir/some-database/some-database.some-table/part-00000-c5a881bb-58ff-4ee6-1111-b41ecff340a3-c000.gz.parquet`です。

通常、 `some-database`データベースをインポートするには、 `data-source-dir`を`S3://some-bucket/some-subdir/some-database/`に設定します。

前述の Parquet ファイル パスに基づいて、ファイルに一致する`(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$`のような正規表現を作成できます。一致グループでは、 `index=1`は`some-database` 、 `index=2`は`some-table` 、 `index=3`は`parquet`です。

正規表現と対応するインデックスに従って構成ファイルを作成すると、 TiDB Lightning がデフォルトの命名規則に従っていないデータ ファイルを認識できるようになります。例えば：

```toml
[[mydumper.files]]
# The expression needed for parsing the Amazon Aurora parquet file
pattern = '(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'
schema = '$1'
table = '$2'
type = '$3'
```

-   **schema** : ターゲットデータベースの名前。値は次のとおりです。
    -   `$1`などの正規表現を使用して取得されるグループ インデックス。
    -   インポートするデータベースの名前 ( `db1`など)。一致したすべてのファイルが`db1`にインポートされます。
-   **table** : ターゲットテーブルの名前。値は次のとおりです。
    -   `$2`などの正規表現を使用して取得されるグループ インデックス。
    -   インポートするテーブルの名前 ( `table1`など)。一致したすべてのファイルが`table1`にインポートされます。
-   **type** : ファイルの種類。 `sql` 、 `parquet` 、および`csv`をサポートします。値は次のとおりです。
    -   `$3`などの正規表現を使用して取得されるグループ インデックス。
-   **key** : ファイル番号 ( `001` in `${db_name}.${table_name}.001.csv`など)。
    -   `$4`などの正規表現を使用して取得されるグループ インデックス。

## Amazon S3 からデータをインポートする {#import-data-from-amazon-s3}

次の例は、 TiDB Lightningを使用して Amazon S3 からデータをインポートする方法を示しています。パラメータ設定の詳細については、 [外部ストレージ サービスの URI 形式](/external-storage-uri.md)を参照してください。

-   ローカルに設定された権限を使用して S3 データにアクセスします。

    ```bash
    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/sql-backup'
    ```

-   パス形式のリクエストを使用して S3 データにアクセスします。

    ```bash
    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/sql-backup?force-path-style=true&endpoint=http://10.154.10.132:8088'
    ```

-   特定の AWS IAMロール ARN を使用して S3 データにアクセスします。

    ```bash
    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/test-data?role-arn=arn:aws:iam::888888888888:role/my-role'
    ```

<!---->

-   AWS IAMユーザーのアクセス キーを使用して S3 データにアクセスします。

    ```bash
    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/test-data?access_key={my_access_key}&secret_access_key={my_secret_access_key}'
    ```

-   AWS IAMロールのアクセス キーとセッション トークンの組み合わせを使用して、S3 データにアクセスします。

    ```bash
    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/test-data?access_key={my_access_key}&secret_access_key={my_secret_access_key}&session-token={my_session_token}'
    ```

## その他のリソース {#more-resources}

-   [Dumplingを使用して CSV ファイルにエクスポートする](/dumpling-overview.md#export-to-csv-files)
-   [`LOAD DATA`](https://dev.mysql.com/doc/refman/8.0/en/load-data.html)
