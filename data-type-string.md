---
title: String types
summary: Learn about the string types supported in TiDB.
---

# 文字列型 {#string-types}

TiDB は、 `CHAR` 、 `VARCHAR` 、 `BINARY` 、 `VARBINARY` 、 `BLOB` 、 `TEXT` 、 `ENUM` 、および`SET`を含むすべての MySQL 文字列型をサポートします。詳細については、 [MySQL の文字列型](https://dev.mysql.com/doc/refman/5.7/en/string-types.html)参照してください。

## サポートされているタイプ {#supported-types}

### <code>CHAR</code>型 {#code-char-code-type}

`CHAR`は固定長の文字列です。 M は列の長さを文字 (バイトではなく) で表します。 M の範囲は 0 ～ 255 です。2 型と`VARCHAR`異なり、データが`CHAR`列に挿入されると、末尾のスペースが切り捨てられます。

```sql
[NATIONAL] CHAR[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>VARCHAR</code>型 {#code-varchar-code-type}

`VARCHAR`は可変長の文字列です。 M は、列の最大長を文字 (バイトではなく) で表します。 `VARCHAR`の最大サイズは 65,535 バイトを超えることはできません。 `VARCHAR`行の長さは、最大行長と使用されている文字セットによって決まります。

1 つの文字が占めるスペースは、文字セットによって異なる場合があります。次の表は、1 文字で消費されるバイト数と、各文字セットの`VARCHAR`列の長さの範囲を示しています。

| キャラクターセット | 文字あたりのバイト数 | `VARCHAR`カラムの最大長の範囲 |
| --------- | ---------- | ------------------- |
| アスキー      | 1          | (0, 65535]          |
| ラテン語1     | 1          | (0, 65535]          |
| バイナリ      | 1          | (0, 65535]          |
| utf8      | 3          | (0, 21845]          |
| utf8mb4   | 4          | (0, 16383]          |

```sql
[NATIONAL] VARCHAR(M) [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>TEXT</code>タイプ {#code-text-code-type}

`TEXT`は可変長の文字列です。列の最大長は 65,535 バイトです。オプションの M 引数は文字数で、 `TEXT`列の最も適切なタイプを自動的に選択するために使用されます。たとえば`TEXT(60)` 、最大 255 バイトを保持できる`TINYTEXT`データ型を生成します。これは、1 文字あたり最大 4 バイト (4×60=240) の 60 文字の UTF-8 文字列に適合します。 M 引数の使用はお勧めしません。

```sql
TEXT[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>TINYTEXT</code>タイプ {#code-tinytext-code-type}

`TINYTEXT`タイプは[`TEXT`タイプ](#text-type)に似ています。違いは、 `TINYTEXT`の最大列長が 255 であることです。

```sql
TINYTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>MEDIUMTEXT</code>タイプ {#code-mediumtext-code-type}

`MEDIUMTEXT`タイプは[`TEXT`タイプ](#text-type)に似ています。違いは、 `MEDIUMTEXT`の最大列長が 16,777,215 であることです。ただし、 [TiDB での単一列の制限](/tidb-limitations.md#limitation-on-a-single-column)のため、TiDB の 1 つの列の最大storageサイズはデフォルトで 6 MiB であり、構成を変更することで 120 MiB に増やすことができます。

```sql
MEDIUMTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>LONGTEXT</code>タイプ {#code-longtext-code-type}

`LONGTEXT`タイプは[`TEXT`タイプ](#text-type)に似ています。違いは、 `LONGTEXT`の最大列長が 4,294,967,295 であることです。ただし、 [TiDB での単一列の制限](/tidb-limitations.md#limitation-on-a-single-column)のため、TiDB の 1 つの列の最大storageサイズはデフォルトで 6 MiB であり、構成を変更することで 120 MiB に増やすことができます。

```sql
LONGTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>BINARY</code>型 {#code-binary-code-type}

`BINARY`タイプは[`CHAR`型](#char-type)に似ています。違いは、 `BINARY`バイナリ バイト文字列を格納することです。

```sql
BINARY(M)
```

### <code>VARBINARY</code>型 {#code-varbinary-code-type}

`VARBINARY`タイプは[`VARCHAR`型](#varchar-type)に似ています。違いは、 `VARBINARY`バイナリ バイト文字列を格納することです。

```sql
VARBINARY(M)
```

### <code>BLOB</code>型 {#code-blob-code-type}

`BLOB`は大きなバイナリ ファイルです。 M は、0 から 65,535 の範囲の最大列長をバイト単位で表します。

```sql
BLOB[(M)]
```

### <code>TINYBLOB</code>型 {#code-tinyblob-code-type}

`TINYBLOB`タイプは[`BLOB`型](#blob-type)に似ています。違いは、 `TINYBLOB`の最大列長が 255 であることです。

```sql
TINYBLOB
```

### <code>MEDIUMBLOB</code>タイプ {#code-mediumblob-code-type}

`MEDIUMBLOB`タイプは[`BLOB`型](#blob-type)に似ています。違いは、 `MEDIUMBLOB`の最大列長が 16,777,215 であることです。ただし、 [TiDB での単一列の制限](/tidb-limitations.md#limitation-on-a-single-column)のため、TiDB の 1 つの列の最大storageサイズはデフォルトで 6 MiB であり、構成を変更することで 120 MiB に増やすことができます。

```sql
MEDIUMBLOB
```

### <code>LONGBLOB</code>型 {#code-longblob-code-type}

`LONGBLOB`タイプは[`BLOB`型](#blob-type)に似ています。違いは、 `LONGBLOB`の最大列長が 4,294,967,295 であることです。ただし、 [TiDB での単一列の制限](/tidb-limitations.md#limitation-on-a-single-column)のため、TiDB の 1 つの列の最大storageサイズはデフォルトで 6 MiB であり、構成を変更することで 120 MiB に増やすことができます。

```sql
LONGBLOB
```

### <code>ENUM</code>型 {#code-enum-code-type}

`ENUM`は、テーブルの作成時に列の指定で明示的に列挙された許可された値のリストから選択された値を持つ文字列オブジェクトです。構文は次のとおりです。

```sql
ENUM('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]

# For example:
ENUM('apple', 'orange', 'pear')
```

`ENUM`データ型の値は数値として格納されます。各値は、定義順序に従って数値に変換されます。前の例では、各文字列が数値にマップされています。

| 価値             | 番号 |
| -------------- | -- |
| ヌル             | ヌル |
| &#39;&#39;     | 0  |
| &#39;りんご&#39;  | 1  |
| &#39;オレンジ&#39; | 2  |
| &#39;梨&#39;    | 3  |

詳細については、 [MySQL の ENUM 型](https://dev.mysql.com/doc/refman/5.7/en/enum.html)を参照してください。

### <code>SET</code>タイプ {#code-set-code-type}

`SET`は、0 個以上の値を持つことができる文字列オブジェクトです。各値は、テーブルの作成時に指定された許可された値のリストから選択する必要があります。構文は次のとおりです。

```sql
SET('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]

# For example:
SET('1', '2') NOT NULL
```

この例では、次の値のいずれかが有効です。

```
''
'1'
'2'
'1,2'
```

TiDB では、 `SET`型の値は内部で`Int64`に変換されます。各要素の存在は、バイナリを使用して表されます: 0 または 1. `SET('a','b','c','d')`として指定された列の場合、メンバーは次の 10 進数値とバイナリ値を持ちます。

| メンバー        | 小数値 | バイナリ値 |
| ----------- | --- | ----- |
| 「あ」         | 1   | 0001  |
| &#39;b&#39; | 2   | 0010  |
| &#39;c&#39; | 4   | 0100  |
| &#39;d&#39; | 8   | 1000  |

この場合、要素が`('a', 'c')`の場合、2 進数では`0101`になります。

詳細については、 [MySQL の SET タイプ](https://dev.mysql.com/doc/refman/5.7/en/set.html)を参照してください。
