---
title: TiDB Lightning CSV Support and Restrictions
summary: Learn how to import CSV files via TiDB Lightning.
---

# TiDB Lightning CSV のサポートと制限 {#tidb-lightning-csv-support-and-restrictions}

このドキュメントでは、 TiDB Lightningを使用して CSV ファイルから TiDB にデータを移行する方法について説明します。 MySQL から CSV ファイルを生成する方法については、 [Dumplingを使用して CSV ファイルにエクスポートする](/dumpling-overview.md#export-to-csv-files)を参照してください。

TiDB Lightning は、 CSV (カンマ区切り値) データ ソースの読み取りと、TSV (タブ区切り値) などの他の区切り形式をサポートしています。

## ファイル名 {#file-name}

テーブル全体を表す CSV ファイルには`db_name.table_name.csv`という名前を付ける必要があります。これは、データベース`db_name`内のテーブル`table_name`として復元されます。

テーブルが複数の CSV ファイルにまたがる場合は、 `db_name.table_name.003.csv`のように名前を付ける必要があります。数値部分は連続している必要はありませんが、増加し、ゼロが埋め込まれている必要があります。

コンテンツがコンマで区切られていない場合でも、ファイル拡張子は`*.csv`でなければなりません。

## スキーマ {#schema}

CSV ファイルはスキーマレスです。それらを TiDB にインポートするには、テーブル スキーマを提供する必要があります。これは、次のいずれかで実行できます。

-   `CREATE TABLE` DDL ステートメントを含む`db_name.table_name-schema.sql`という名前のファイルと、 `CREATE DATABASE` DDL ステートメントを含む`db_name-schema-create.sql`という名前のファイルを提供します。
-   TiDB でテーブル スキーマを手動で作成します。

## コンフィグレーション {#configuration}

CSV 形式は、 `[mydumper.csv]`セクションの`tidb-lightning.toml`で構成できます。ほとんどの設定には、MySQL [`LOAD DATA`]ステートメントに対応するオプションがあります。

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

`separator` 、 `delimiter` 、 `terminator`などのすべての文字列フィールドで、入力に特殊文字が含まれている場合は、バックスラッシュ エスケープ シーケンスを使用して、それらを*二重引用*符で囲まれた文字列 ( `"…"` ) で表すことができます。たとえば、 `separator = "\u001f"` ASCII 文字 0x1F をセパレータとして使用することを意味します。

さらに、*単一引用*符で囲まれた文字列 ( `'…'` ) を使用して、バックスラッシュのエスケープを抑制することができます。たとえば、 `terminator = '\n'` 2 文字の文字列を使用することを意味します: バックスラッシュの後に文字 &quot;n&quot; がターミネータとして続きます。

詳細は[TOML v1.0.0 specification]を参照してください。

[`LOAD DATA`]: https://dev.mysql.com/doc/refman/8.0/en/load-data.html

[TOML v1.0.0 specification]: https://toml.io/en/v1.0.0#string

### <code>separator</code> {#code-separator-code}

-   フィールド区切りを定義します。

-   複数の文字を指定できますが、空にすることはできません。

-   一般的な値:

    -   CSV (カンマ区切り値) の場合は`','`
    -   TSV (タブ区切り値) の場合は`"\t"`
    -   ASCII 文字 0x01 をセパレータとして使用する場合は`"\u0001"`

-   LOAD DATA ステートメントの`FIELDS TERMINATED BY`オプションに対応します。

### <code>delimiter</code> {#code-delimiter-code}

-   引用に使用する区切り文字を定義します。

-   `delimiter`が空の場合、すべてのフィールドは引用符で囲まれていません。

-   一般的な値:

    -   二重引用符で囲まれた`'"'`引用フィールド、 [RFC 4180]と同じ
    -   `''`引用を無効にする

-   `LOAD DATA`ステートメントの`FIELDS ENCLOSED BY`オプションに対応します。

[RFC 4180]: https://tools.ietf.org/html/rfc4180

### <code>terminator</code> {#code-terminator-code}

-   行末記号を定義します。
-   `terminator`が空の場合、 `"\r"` (U+000D キャリッジ リターン) と`"\n"` (U+000A ライン フィード) の両方がターミネータとして使用されます。
-   `LOAD DATA`ステートメントの`LINES TERMINATED BY`オプションに対応します。

### <code>header</code> {#code-header-code}

-   *すべての*CSV ファイルにヘッダー行が含まれているかどうか。
-   `header`が true の場合、最初の行が*列名*として使用されます。 `header`が false の場合、最初の行は特別ではなく、通常のデータ行として扱われます。

### <code>not-null</code>および<code>null</code> {#code-not-null-code-and-code-null-code}

-   `not-null`設定は、すべてのフィールドが null 非許容であるかどうかを制御します。
-   `not-null`が false の場合、 `null`で指定された文字列は、具体的な値ではなく SQL NULL に変換されます。
-   引用符は、フィールドが null であるかどうかには影響しません。

    たとえば、CSV ファイルの場合:

    ```csv
    A,B,C
    \N,"\N",
    ```

    デフォルト設定 ( `not-null = false; null = '\N'` ) では、列`A`と`B`は両方とも、TiDB へのインポート後に NULL に変換されます。列`C`は単に空の文字列`''`ですが、NULL ではありません。

### <code>backslash-escape</code> {#code-backslash-escape-code}

-   フィールド内のバックスラッシュ エスケープを解釈するかどうか。

-   `backslash-escape`が true の場合、次のシーケンスが認識され、変換されます。

    | シーケンス | に変換                  |
    | ----- | -------------------- |
    | `\0`  | 空文字 (U+0000)         |
    | `\b`  | バックスペース (U+0008)     |
    | `\n`  | 改行 (U+000A)          |
    | `\r`  | キャリッジ リターン (U+000D)  |
    | `\t`  | タブ (U+0009)          |
    | `\Z`  | Windows EOF (U+001A) |

    他のすべての場合 (たとえば、 `\"` ) では、バックスラッシュは単純に取り除かれ、次の文字 ( `"` ) がフィールドに残ります。左の文字には特別な役割 (区切り文字など) はなく、単なる通常の文字です。

-   引用符は、バックスラッシュ エスケープが解釈されるかどうかには影響しません。

-   `LOAD DATA`ステートメントの`FIELDS ESCAPED BY '\'`オプションに対応します。

### <code>trim-last-separator</code> {#code-trim-last-separator-code}

-   フィールド`separator`ターミネータとして扱い、末尾のセパレータをすべて削除します。

    たとえば、CSV ファイルの場合:

    ```csv
    A,,B,,
    ```

-   `trim-last-separator = false`の場合、これは 5 つのフィールド`('A', '', 'B', '', '')`の行として解釈されます。

-   `trim-last-separator = true`の場合、これは 3 つのフィールド`('A', '', 'B')`の行として解釈されます。

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

TiDB Lightning は、 `LOAD DATA`ステートメントでサポートされているすべてのオプションをサポートしているわけではありません。いくつかの例：

-   行のプレフィックス ( `LINES STARTING BY` ) は使用できません。
-   ヘッダーを単純にスキップすることはできません ( `IGNORE n LINES` )。存在する場合は、有効な列名でなければなりません。

## 厳密な形式 {#strict-format}

入力ファイルのサイズが 256 MB 前後で一定の場合、Lightning は最適に機能します。入力が単一の巨大な CSV ファイルの場合、Lightning はそれを処理するために 1 つのスレッドしか使用できないため、インポート速度が大幅に低下します。

これは、最初に CSV を複数のファイルに分割することで修正できます。一般的な CSV 形式の場合、ファイル全体を読み取らずに行の開始時刻と終了時刻をすばやく識別する方法はありません。したがって、デフォルトでは、Lightning は CSV ファイルを自動的に分割しませ*ん*。ただし、CSV 入力が特定の制限に準拠していることが確実な場合は、 `strict-format`設定を有効にして、Lightning がファイルを複数の 256 MB サイズのチャンクに分割して並列処理できるようにすることができます。

```toml
[mydumper]
strict-format = true
```

現在、厳密な CSV ファイルは、すべてのフィールドが 1 行のみを占めることを意味します。つまり、次のいずれかに該当する必要があります。

-   区切り文字が空であるか、または
-   すべてのフィールドにターミネータ自体が含まれているわけではありません。デフォルトの構成では、これはすべてのフィールドに CR ( `\r` ) または LF ( `\n` ) が含まれていないことを意味します。

CSV ファイルが厳密ではなく、 `strict-format`誤って`true`に設定されている場合、複数行にまたがるフィールドが半分に分割されて 2 つのチャンクになり、解析が失敗するか、さらに悪いことに、破損したデータが静かにインポートされる可能性があります。

## 一般的な構成 {#common-configurations}

### CSV {#csv}

デフォルト設定は、RFC 4180 に従って CSV 用に調整済みです。

```toml
[mydumper.csv]
separator = ',' # It is not recommended to use the default ','. It is recommended to use '\|+\|' or other uncommon character combinations.
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

コンテンツの例:

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

コンテンツの例:

```
1|East|32|
2|South|0|
3|West|10|
4|North|39|
```
