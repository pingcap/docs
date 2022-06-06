---
title: TiDB Lightning CSV Support and Restrictions
summary: Learn how to import CSV files via TiDB Lightning.
---

# TiDBLightningCSVのサポートと制限 {#tidb-lightning-csv-support-and-restrictions}

このドキュメントでは、TiDBLightningを使用してCSVファイルからTiDBにデータを移行する方法について説明します。 MySQLからCSVファイルを生成する方法については、 [Dumplingを使用してCSVファイルにエクスポート](/dumpling-overview.md#export-to-csv-files)を参照してください。

TiDB Lightningは、CSV（カンマ区切り値）データソース、およびTSV（タブ区切り値）などの他の区切り形式の読み取りをサポートしています。

## ファイル名 {#file-name}

テーブル全体を表すCSVファイルには`db_name.table_name.csv`という名前を付ける必要があります。これは、データベース`db_name`内のテーブル`table_name`として復元されます。

テーブルが複数のCSVファイルにまたがる場合は、 `db_name.table_name.003.csv`のように名前を付ける必要があります。数字の部分は連続している必要はありませんが、増加してゼロが埋め込まれている必要があります。

コンテンツがコンマで区切られていない場合でも、ファイル拡張子は`*.csv`でなければなりません。

## スキーマ {#schema}

CSVファイルはスキーマレスです。それらをTiDBにインポートするには、テーブルスキーマを提供する必要があります。これは、次のいずれかによって実行できます。

-   `CREATE TABLE`のDDLステートメントを含む`db_name.table_name-schema.sql`という名前のファイルと、 `CREATE DATABASE`のDDLステートメントを含む`db_name-schema-create.sql`という名前のファイルを提供します。
-   そもそもTiDBで直接空のテーブルを作成し、次に`tidb-lightning.toml`の`[mydumper] no-schema = true`を設定します。

## Configuration / コンフィグレーション {#configuration}

CSV形式は、 `[mydumper.csv]`セクションの`tidb-lightning.toml`で構成できます。ほとんどの設定には、 [`LOAD DATA`]ステートメントに対応するオプションがあります。

```toml
[mydumper.csv]
# Separator between fields. Must be ASCII characters. It is not recommended to use the default ','. It is recommended to use '\|+\|' or other uncommon character combinations.
separator = ','
# Quoting delimiter. Empty value means no quoting.
delimiter = '"'
# Line terminator. Empty value means both "\n" (LF) and "\r\n" (CRLF) are line terminators.
terminator = ''
# Whether the CSV files contain a header.
# If `header` is true, the first line will be skipped.
header = true
# Whether the CSV contains any NULL value.
# If `not-null` is true, all columns from CSV cannot be NULL.
not-null = false
# When `not-null` is false (that is, CSV can contain NULL),
# fields equal to this value will be treated as NULL.
null = '\N'
# Whether to interpret backslash escapes inside fields.
backslash-escape = true
# If a line ends with a separator, remove it.
trim-last-separator = false
```

`separator`などのすべての文字列フィールドで、入力に特殊文字が含まれている場合は、円記号のエスケープシーケンスを使用して、それらを*二重引用符で囲まれ*`"…"` `delimiter`で表すことができ`terminator` 。たとえば、 `separator = "\u001f"`は、ASCII文字0x1Fを区切り文字として使用することを意味します。

さらに、*一重引用符で囲まれ*た文字列（ `'…'` ）を使用して、バックスラッシュのエスケープを抑制することができます。たとえば、 `terminator = '\n'`は、2文字の文字列を使用することを意味します。つまり、円記号の後に文字「n」をターミネータとして使用します。

詳細については、 [TOML v1.0.0 specification]を参照してください。

[`LOAD DATA`]: https://dev.mysql.com/doc/refman/8.0/en/load-data.html

[TOML v1.0.0 specification]: https://toml.io/en/v1.0.0#string

### <code>separator</code> {#code-separator-code}

-   フィールドセパレータを定義します。

-   複数の文字にすることができますが、空にすることはできません。

-   一般的な値：

    -   CSVの場合は`','` （カンマ区切り値）
    -   TSVの場合は`"\t"` （タブ区切り値）
    -   `"\u0001"`はASCII文字0x01を区切り文字として使用します

-   LOADDATAステートメントの`FIELDS TERMINATED BY`オプションに対応します。

### <code>delimiter</code> {#code-delimiter-code}

-   引用に使用される区切り文字を定義します。

-   `delimiter`が空の場合、すべてのフィールドは引用符で囲まれていません。

-   一般的な値：

    -   [RFC 4180]と同じ、二重引用符付きの`'"'`引用符フィールド
    -   `''`引用を無効にする

-   `LOAD DATA`ステートメントの`FIELDS ENCLOSED BY`オプションに対応します。

[RFC 4180]: https://tools.ietf.org/html/rfc4180

### <code>terminator</code> {#code-terminator-code}

-   ラインターミネータを定義します。
-   `terminator`が空の場合、 `"\r"` （U + 000Dキャリッジリターン）と`"\n"` （U + 000Aラインフィード）の両方がターミネータとして使用されます。
-   `LOAD DATA`ステートメントの`LINES TERMINATED BY`オプションに対応します。

### <code>header</code> {#code-header-code}

-   *すべての*CSVファイルにヘッダー行が含まれているかどうか。
-   `header`が真の場合、最初の行が*列名*として使用されます。 `header`がfalseの場合、最初の行は特別ではなく、通常のデータ行として扱われます。

### <code>not-null</code>および<code>null</code> {#code-not-null-code-and-code-null-code}

-   `not-null`の設定は、すべてのフィールドがnull許容でないかどうかを制御します。
-   `not-null`がfalseの場合、 `null`で指定された文字列は、具体的な値ではなくSQLNULLに変換されます。
-   引用は、フィールドがnullであるかどうかには影響しません。

    たとえば、CSVファイルの場合：

    ```csv
    A,B,C
    \N,"\N",
    ```

    デフォルト設定（ `not-null = false; null = '\N'` ）では、TiDBにインポートした後、列`A`と`B`の両方がNULLに変換されます。列`C`は単に空の文字列`''`ですが、NULLではありません。

### <code>backslash-escape</code> {#code-backslash-escape-code}

-   フィールド内のバックスラッシュエスケープを解釈するかどうか。

-   `backslash-escape`が真の場合、次のシーケンスが認識され、変換されます。

    | 順序   | に変換                   |
    | ---- | --------------------- |
    | `\0` | ヌル文字（U + 0000）        |
    | `\b` | バックスペース（U + 0008）     |
    | `\n` | ラインフィード（U + 000A）     |
    | `\r` | キャリッジリターン（U + 000D）   |
    | `\t` | タブ（U + 0009）          |
    | `\Z` | Windows EOF（U + 001A） |

    他のすべての場合（たとえば、 `\"` ）は、バックスラッシュが単純に削除され、フィールドに次の文字（ `"` ）が残ります。左の文字には特別な役割（区切り文字など）はなく、通常の文字です。

-   引用は、円記号のエスケープが解釈されるかどうかには影響しません。

-   `LOAD DATA`ステートメントの`FIELDS ESCAPED BY '\'`オプションに対応します。

### <code>trim-last-separator</code> {#code-trim-last-separator-code}

-   フィールド`separator`をターミネータとして扱い、末尾の区切り文字をすべて削除します。

    たとえば、CSVファイルの場合：

    ```csv
    A,,B,,
    ```

-   `trim-last-separator = false`の場合、これは5つのフィールド`('A', '', 'B', '', '')`の行として解釈されます。

-   `trim-last-separator = true`の場合、これは3つのフィールド`('A', '', 'B')`の行として解釈されます。

-   複数の末尾の区切り文字を使用した動作は直感的ではないため、このオプションは非推奨です。代わりに`terminator`オプションを使用してください。古い構成が

    ```toml
    separator = ','
    trim-last-separator = true
    ```

    これをに変更することをお勧めします

    ```toml
    separator = ','
    terminator = ",\n"
    ```

### 構成不可能なオプション {#non-configurable-options}

TiDB Lightningは、 `LOAD DATA`ステートメントでサポートされるすべてのオプションをサポートしているわけではありません。いくつかの例：

-   行プレフィックス（ `LINES STARTING BY` ）は使用できません。
-   ヘッダーを単純にスキップすることはできません（ `IGNORE n LINES` ）。存在する場合は、有効な列名である必要があります。

## 厳密なフォーマット {#strict-format}

Lightningは、入力ファイルのサイズが約256MBで均一な場合に最適に機能します。入力が単一の巨大なCSVファイルである場合、Lightningはそれを処理するために1つのスレッドしか使用できないため、インポート速度が大幅に低下します。

これは、最初にCSVを複数のファイルに分割することで修正できます。一般的なCSV形式の場合、ファイル全体を読み取らずに行の開始と終了をすばやく識別する方法はありません。したがって、LightningはデフォルトではCSVファイルを自動的に分割しませ*ん*。ただし、CSV入力が特定の制限に準拠していることが確実な場合は、 `strict-format`設定を有効にして、Lightningがファイルを複数の256MBサイズのチャンクに分割して並列処理できるようにすることができます。

```toml
[mydumper]
strict-format = true
```

現在、厳密なCSVファイルは、すべてのフィールドが1行のみを占めることを意味します。つまり、次のいずれかが当てはまる必要があります。

-   区切り文字が空、または
-   すべてのフィールドにターミネータ自体が含まれているわけではありません。デフォルトの構成では、これはすべてのフィールドにCR（ `\r` ）またはLF（ `\n` ）が含まれていないことを意味します。

CSVファイルが厳密ではないが、 `strict-format`が誤って`true`に設定されている場合、複数行にまたがるフィールドが2つのチャンクに半分にカットされ、解析が失敗したり、さらに悪いことに、破損したデータを静かにインポートしたりする可能性があります。

## 一般的な構成 {#common-configurations}

### CSV {#csv}

デフォルト設定は、RFC4180に従ってCSV用にすでに調整されています。

```toml
[mydumper.csv]
separator = ',' # It is not recommended to use the default ‘,’. It is recommended to use ‘\|+\|‘ or other uncommon character combinations.
delimiter = '"'
header = true
not-null = false
null = '\N'
backslash-escape = true
```

内容の例：

```
ID,Region,Count
1,"East",32
2,"South",\N
3,"West",10
4,"North",39
```

### TSV {#tsv}

```toml
[mydumper.csv]
separator = "\t"
delimiter = ''
header = true
not-null = false
null = 'NULL'
backslash-escape = false
```

内容の例：

```
ID    Region    Count
1     East      32
2     South     NULL
3     West      10
4     North     39
```

### TPC-H DBGEN {#tpc-h-dbgen}

```toml
[mydumper.csv]
separator = '|'
delimiter = ''
terminator = "|\n"
header = false
not-null = true
backslash-escape = false
```

内容の例：

```
1|East|32|
2|South|0|
3|West|10|
4|North|39|
```
