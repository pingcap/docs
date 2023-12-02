---
title: String types
summary: Learn about the string types supported in TiDB.
---

# 文字列型 {#string-types}

TiDB は、 `CHAR` 、 `VARCHAR` 、 `BINARY` 、 `VARBINARY` 、 `BLOB` 、 `TEXT` 、 `ENUM` 、 `SET`を含むすべての MySQL 文字列タイプをサポートします。詳細については、 [MySQL の文字列型](https://dev.mysql.com/doc/refman/8.0/en/string-types.html)参照してください。

## サポートされているタイプ {#supported-types}

### <code>CHAR</code>型 {#code-char-code-type}

`CHAR`は固定長の文字列です。 M は列の長さを文字数 (バイト数ではなく) で表します。 M の範囲は 0 ～ 255 です。タイプ`VARCHAR`とは異なり、データが`CHAR`列に挿入される場合、末尾のスペースは切り捨てられます。

```sql
[NATIONAL] CHAR[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>VARCHAR</code>型 {#code-varchar-code-type}

`VARCHAR`は可変長の文字列です。 M は列の最大長を文字数 (バイト数ではなく) で表します。 `VARCHAR`の最大サイズは 65,535 バイトを超えることはできません。行の最大長と使用されている文字セットによって`VARCHAR`さが決まります。

1 つの文字が占めるスペースは、文字セットによって異なる場合があります。次の表は、1 つの文字によって消費されるバイト数と、各文字セットの`VARCHAR`列の長さの範囲を示しています。

| キャラクターセット | 1 文字あたりのバイト数 | 最大`VARCHAR`カラム長の範囲 |
| --------- | ------------ | ------------------ |
| アスキー      | 1            | (0, 65535]         |
| ラテン語1     | 1            | (0, 65535]         |
| バイナリ      | 1            | (0, 65535]         |
| utf8      | 3            | (0, 21845]         |
| utf8mb4   | 4            | (0, 16383]         |

```sql
[NATIONAL] VARCHAR(M) [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>TEXT</code>タイプ {#code-text-code-type}

`TEXT`は可変長の文字列です。列の最大長は 65,535 バイトです。オプションの M 引数は文字単位であり、 `TEXT`列の最も適合するタイプを自動的に選択するために使用されます。たとえば`TEXT(60)` 、最大 255 バイトを保持できる`TINYTEXT`データ型を生成します。これは、1 文字あたり最大 4 バイトの 60 文字の UTF-8 文字列に適合します (4×60=240)。 M 引数の使用はお勧めできません。

```sql
TEXT[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>TINYTEXT</code>型 {#code-tinytext-code-type}

`TINYTEXT`タイプは[`TEXT`タイプ](#text-type)と似ています。違いは、 `TINYTEXT`の最大列長が 255 であることです。

```sql
TINYTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>MEDIUMTEXT</code>型 {#code-mediumtext-code-type}

<CustomContent platform="tidb">

`MEDIUMTEXT`タイプは[`TEXT`タイプ](#text-type)と似ています。違いは、 `MEDIUMTEXT`の最大列長が 16,777,215 であることです。ただし、 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50)の制限により、TiDB の単一行の最大storageサイズはデフォルトで 6 MiB ですが、構成を変更することで 120 MiB まで増やすことができます。

</CustomContent>
<CustomContent platform="tidb-cloud">

`MEDIUMTEXT`タイプは[`TEXT`タイプ](#text-type)と似ています。違いは、 `MEDIUMTEXT`の最大列長が 16,777,215 であることです。ただし、 [`txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v50)の制限により、TiDB の単一行の最大storageサイズはデフォルトで 6 MiB ですが、構成を変更することで 120 MiB まで増やすことができます。

</CustomContent>

```sql
MEDIUMTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>LONGTEXT</code>型 {#code-longtext-code-type}

<CustomContent platform="tidb">

`LONGTEXT`タイプは[`TEXT`タイプ](#text-type)と似ています。違いは、 `LONGTEXT`の最大列長が 4,294,967,295 であることです。ただし、 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50)の制限により、TiDB の単一行の最大storageサイズはデフォルトで 6 MiB ですが、構成を変更することで 120 MiB まで増やすことができます。

</CustomContent>
<CustomContent platform="tidb-cloud">

`LONGTEXT`タイプは[`TEXT`タイプ](#text-type)と似ています。違いは、 `LONGTEXT`の最大列長が 4,294,967,295 であることです。ただし、 [`txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v50)の制限により、TiDB の単一行の最大storageサイズはデフォルトで 6 MiB ですが、構成を変更することで 120 MiB まで増やすことができます。

</CustomContent>

```sql
LONGTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>BINARY</code>型 {#code-binary-code-type}

`BINARY`タイプは[`CHAR`型](#char-type)と似ています。違いは、 `BINARY`バイナリ バイト文字列を格納することです。

```sql
BINARY(M)
```

### <code>VARBINARY</code>型 {#code-varbinary-code-type}

`VARBINARY`タイプは[`VARCHAR`型](#varchar-type)と似ています。違いは、 `VARBINARY`バイナリ バイト文字列を格納することです。

```sql
VARBINARY(M)
```

### <code>BLOB</code>タイプ {#code-blob-code-type}

`BLOB`は大きなバイナリ ファイルです。 M は列の最大長をバイト単位で表し、範囲は 0 ～ 65,535 です。

```sql
BLOB[(M)]
```

### <code>TINYBLOB</code>型 {#code-tinyblob-code-type}

`TINYBLOB`タイプは[`BLOB`タイプ](#blob-type)と似ています。違いは、 `TINYBLOB`の最大列長が 255 であることです。

```sql
TINYBLOB
```

### <code>MEDIUMBLOB</code>タイプ {#code-mediumblob-code-type}

<CustomContent platform="tidb">

`MEDIUMBLOB`タイプは[`BLOB`タイプ](#blob-type)と似ています。違いは、 `MEDIUMBLOB`の最大列長が 16,777,215 であることです。ただし、 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50)の制限により、TiDB の単一行の最大storageサイズはデフォルトで 6 MiB ですが、構成を変更することで 120 MiB まで増やすことができます。

</CustomContent>
<CustomContent platform="tidb-cloud">

`MEDIUMBLOB`タイプは[`BLOB`タイプ](#blob-type)と似ています。違いは、 `MEDIUMBLOB`の最大列長が 16,777,215 であることです。ただし、 [`txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v50)の制限により、TiDB の単一行の最大storageサイズはデフォルトで 6 MiB ですが、構成を変更することで 120 MiB まで増やすことができます。

</CustomContent>

```sql
MEDIUMBLOB
```

### <code>LONGBLOB</code>型 {#code-longblob-code-type}

<CustomContent platform="tidb">

`LONGBLOB`タイプは[`BLOB`タイプ](#blob-type)と似ています。違いは、 `LONGBLOB`の最大列長が 4,294,967,295 であることです。ただし、 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50)の制限により、TiDB の単一行の最大storageサイズはデフォルトで 6 MiB ですが、構成を変更することで 120 MiB まで増やすことができます。

</CustomContent>
<CustomContent platform="tidb-cloud">

`LONGBLOB`タイプは[`BLOB`タイプ](#blob-type)と似ています。違いは、 `LONGBLOB`の最大列長が 4,294,967,295 であることです。ただし、 [`txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v50)の制限により、TiDB の単一行の最大storageサイズはデフォルトで 6 MiB ですが、構成を変更することで 120 MiB まで増やすことができます。

</CustomContent>

```sql
LONGBLOB
```

### <code>ENUM</code>タイプ {#code-enum-code-type}

`ENUM`は、テーブルの作成時に列仕様で明示的に列挙される許可された値のリストから選択された値を持つ文字列オブジェクトです。構文は次のとおりです。

```sql
ENUM('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]

# For example:
ENUM('apple', 'orange', 'pear')
```

`ENUM`データ型の値は数値として保存されます。各値は定義順序に従って数値に変換されます。前の例では、各文字列が数値にマップされます。

| 価値             | 番号 |
| -------------- | -- |
| ヌル             | ヌル |
| 」              | 0  |
| &#39;りんご&#39;  | 1  |
| &#39;オレンジ&#39; | 2  |
| &#39;梨&#39;    | 3  |

詳細については、 [MySQL の ENUM タイプ](https://dev.mysql.com/doc/refman/8.0/en/enum.html)を参照してください。

### <code>SET</code>タイプ {#code-set-code-type}

`SET`は、0 個以上の値を持つことができる文字列オブジェクトであり、それぞれの値は、テーブルの作成時に指定された許可される値のリストから選択する必要があります。構文は次のとおりです。

```sql
SET('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]

# For example:
SET('1', '2') NOT NULL
```

この例では、次のいずれかの値が有効です。

    ''
    '1'
    '2'
    '1,2'

TiDB では、 `SET`型の値は内部で`Int64`に変換されます。各要素の存在は、0 または 1 のバイナリを使用して表されます。 `SET('a','b','c','d')`として指定された列の場合、メンバーは次の 10 進値とバイナリ値を持ちます。

| メンバー | 10 進数値 | バイナリ値 |
| ---- | ------ | ----- |
| 「あ」  | 1      | 0001  |
| 「b」  | 2      | 0010  |
| 「c」  | 4      | 0100  |
| 「だ」  | 8      | 1000  |

この場合、要素が`('a', 'c')`の場合、2 進数では`0101`になります。

詳細については、 [MySQL の SET タイプ](https://dev.mysql.com/doc/refman/8.0/en/set.html)を参照してください。
