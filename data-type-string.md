---
title: String types
summary: TiDB でサポートされている文字列型について学習します。
---

# 文字列型 {#string-types}

TiDB は`CHAR` 、 `VARCHAR` 、 `BINARY` 、 `VARBINARY` 、 `BLOB` 、 `TEXT` 、 `ENUM` 、 `SET`を含むすべての MySQL 文字列型をサポートしています。詳細については、 [MySQL の文字列型](https://dev.mysql.com/doc/refman/8.0/en/string-types.html)参照してください。

## サポートされているタイプ {#supported-types}

### <code>CHAR</code>型 {#code-char-code-type}

`CHAR`は固定長文字列です。M は列の長さを文字数 (バイト数ではありません) で表します。M の範囲は 0 ～ 255 です。2 タイプとは異なり、 `VARCHAR`列にデータを挿入すると、末尾のスペースは`CHAR`られます。

```sql
[NATIONAL] CHAR[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>VARCHAR</code>型 {#code-varchar-code-type}

`VARCHAR`可変長の文字列です。M は文字数 (バイト数ではありません) での最大列長を表します`VARCHAR`の最大サイズは 65,535 バイトを超えることはできません。最大行長と使用されている文字セットによって`VARCHAR`さが決まります。

1 つの文字が占めるスペースは、文字セットによって異なる場合があります。次の表は、1 つの文字が消費するバイト数と、各文字セットの`VARCHAR`列の長さの範囲を示しています。

| 文字セット   | 1文字あたりのバイト数 | `VARCHAR`カラムの最大長の範囲 |
| ------- | ----------- | ------------------- |
| アスキー    | 1           | (0, 65535]          |
| ラテン1    | 1           | (0, 65535]          |
| バイナリ    | 1           | (0, 65535]          |
| utf8    | 3           | (0, 21845]          |
| utf8mb4 | 4           | (0, 16383]          |

```sql
[NATIONAL] VARCHAR(M) [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>TEXT</code>タイプ {#code-text-code-type}

`TEXT`可変長の文字列です。列の最大長は 65,535 バイトです。オプションの M 引数は文字数で、 `TEXT`列の最適な型を自動的に選択するために使用されます。たとえば、 `TEXT(60)`最大 255 バイトを保持できる`TINYTEXT`データ型を生成し、これは 1 文字あたり最大 4 バイト (4×60=240) の 60 文字の UTF-8 文字列に適合します。M 引数の使用は推奨されません。

```sql
TEXT[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>TINYTEXT</code>タイプ {#code-tinytext-code-type}

`TINYTEXT`タイプは[`TEXT`タイプ](#text-type)と似ていますが、違いは`TINYTEXT`の最大列長が 255 であることです。

```sql
TINYTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>MEDIUMTEXT</code>タイプ {#code-mediumtext-code-type}

<CustomContent platform="tidb">

`MEDIUMTEXT`タイプは[`TEXT`タイプ](#text-type)と似ています。違いは、 `MEDIUMTEXT`の最大列長が 16,777,215 であることです。ただし、 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500)の制限により、TiDB の単一行の最大storageサイズはデフォルトで 6 MiB であり、構成を変更することで 120 MiB まで増やすことができます。

</CustomContent>
<CustomContent platform="tidb-cloud">

`MEDIUMTEXT`タイプは[`TEXT`タイプ](#text-type)と似ています。違いは、 `MEDIUMTEXT`の最大列長が 16,777,215 であることです。ただし、 [`txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v4010-and-v500)の制限により、TiDB の単一行の最大storageサイズはデフォルトで 6 MiB であり、構成を変更することで 120 MiB まで増やすことができます。

</CustomContent>

```sql
MEDIUMTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>LONGTEXT</code>型 {#code-longtext-code-type}

<CustomContent platform="tidb">

`LONGTEXT`型は[`TEXT`タイプ](#text-type)と似ています。違いは、 `LONGTEXT`の最大列長が 4,294,967,295 であることです。ただし、 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500)の制限により、TiDB の単一行の最大storageサイズはデフォルトで 6 MiB であり、構成を変更することで 120 MiB まで増やすことができます。

</CustomContent>
<CustomContent platform="tidb-cloud">

`LONGTEXT`型は[`TEXT`タイプ](#text-type)と似ています。違いは、 `LONGTEXT`の最大列長が 4,294,967,295 であることです。ただし、 [`txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v4010-and-v500)の制限により、TiDB の単一行の最大storageサイズはデフォルトで 6 MiB であり、構成を変更することで 120 MiB まで増やすことができます。

</CustomContent>

```sql
LONGTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>BINARY</code>型 {#code-binary-code-type}

`BINARY`型は[`CHAR`型](#char-type)と似ています。違いは、 `BINARY`バイナリ バイト文字列を格納することです。

```sql
BINARY(M)
```

### <code>VARBINARY</code>型 {#code-varbinary-code-type}

`VARBINARY`型は[`VARCHAR`型](#varchar-type)と似ています。違いは、 `VARBINARY`バイナリ バイト文字列を格納することです。

```sql
VARBINARY(M)
```

### <code>BLOB</code>型 {#code-blob-code-type}

`BLOB`大きなバイナリ ファイルです。M は、0 から 65,535 までの最大列長をバイト単位で表します。

```sql
BLOB[(M)]
```

### <code>TINYBLOB</code>型 {#code-tinyblob-code-type}

`TINYBLOB`タイプは[`BLOB`型](#blob-type)と似ていますが、違いは`TINYBLOB`の最大列長が 255 であることです。

```sql
TINYBLOB
```

### <code>MEDIUMBLOB</code>型 {#code-mediumblob-code-type}

<CustomContent platform="tidb">

`MEDIUMBLOB`タイプは[`BLOB`型](#blob-type)と似ています。違いは、 `MEDIUMBLOB`の最大列長が 16,777,215 であることです。ただし、 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500)の制限により、TiDB の単一行の最大storageサイズはデフォルトで 6 MiB であり、構成を変更することで 120 MiB まで増やすことができます。

</CustomContent>
<CustomContent platform="tidb-cloud">

`MEDIUMBLOB`タイプは[`BLOB`型](#blob-type)と似ています。違いは、 `MEDIUMBLOB`の最大列長が 16,777,215 であることです。ただし、 [`txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v4010-and-v500)の制限により、TiDB の単一行の最大storageサイズはデフォルトで 6 MiB であり、構成を変更することで 120 MiB まで増やすことができます。

</CustomContent>

```sql
MEDIUMBLOB
```

### <code>LONGBLOB</code>型 {#code-longblob-code-type}

<CustomContent platform="tidb">

`LONGBLOB`型は[`BLOB`型](#blob-type)と似ています。違いは、 `LONGBLOB`の最大列長が 4,294,967,295 であることです。ただし、 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500)の制限により、TiDB の単一行の最大storageサイズはデフォルトで 6 MiB であり、構成を変更することで 120 MiB まで増やすことができます。

</CustomContent>
<CustomContent platform="tidb-cloud">

`LONGBLOB`型は[`BLOB`型](#blob-type)と似ています。違いは、 `LONGBLOB`の最大列長が 4,294,967,295 であることです。ただし、 [`txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v4010-and-v500)の制限により、TiDB の単一行の最大storageサイズはデフォルトで 6 MiB であり、構成を変更することで 120 MiB まで増やすことができます。

</CustomContent>

```sql
LONGBLOB
```

### <code>ENUM</code>型 {#code-enum-code-type}

`ENUM`は、テーブルの作成時に列仕様で明示的に列挙される許可された値のリストから選択された値を持つ文字列オブジェクトです。構文は次のとおりです。

```sql
ENUM('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]

# For example:
ENUM('apple', 'orange', 'pear')
```

`ENUM`データ型の値は数値として保存されます。各値は定義順序に従って数値に変換されます。前の例では、各文字列が数値にマッピングされています。

| 価値             | 番号   |
| -------------- | ---- |
| NULL           | NULL |
| &#39;&#39;     | 0    |
| &#39;りんご&#39;  | 1    |
| &#39;オレンジ&#39; | 2    |
| &#39;梨&#39;    | 3    |

詳細については[MySQLのENUM型](https://dev.mysql.com/doc/refman/8.0/en/enum.html)参照してください。

### <code>SET</code>型 {#code-set-code-type}

`SET` 0 個以上の値を持つことができる文字列オブジェクトであり、各値はテーブルの作成時に指定された許可された値のリストから選択する必要があります。構文は次のとおりです。

```sql
SET('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]

# For example:
SET('1', '2') NOT NULL
```

この例では、次のいずれかの値が有効になります。

    ''
    '1'
    '2'
    '1,2'

TiDB では、 `SET`型の値は内部的に`Int64`に変換されます。各要素の存在は、0 または 1 のバイナリを使用して表されます。 `SET('a','b','c','d')`として指定された列の場合、メンバーは次の 10 進値と 2 進値を持ちます。

| メンバー        | 小数値 | バイナリ値 |
| ----------- | --- | ----- |
| &#39;あ&#39; | 1   | 0001  |
| &#39;ブ&#39; | 2   | 0010  |
| &#39;ハ&#39; | 4   | 0100  |
| &#39;d&#39; | 8   | 1000  |

この場合、 `('a', 'c')`の要素は 2 進数では`0101`なります。

詳細については[MySQLのSET型](https://dev.mysql.com/doc/refman/8.0/en/set.html)参照してください。
