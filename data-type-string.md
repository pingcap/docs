---
title: String types
summary: TiDB でサポートされている文字列型について学習します。
---

# 文字列型 {#string-types}

TiDBは、 `CHAR` 、 `VARCHAR` 、 `BINARY` 、 `VARBINARY` 、 `BLOB` 、 `TEXT` 、 `ENUM` 、 `SET`を含むすべてのMySQL文字列型をサポートしています。詳細については、 [MySQLの文字列型](https://dev.mysql.com/doc/refman/8.0/en/string-types.html)参照してください。

## サポートされているタイプ {#supported-types}

### <code>CHAR</code>型 {#code-char-code-type}

`CHAR`は固定長文字列です。Mは列の長さを文字数（バイト数ではありません）で表します。Mの範囲は0から255です。2とは異なり、 `VARCHAR`列にデータを挿入する場合、末尾のスペース`CHAR`切り捨てられます。

```sql
[NATIONAL] CHAR[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>VARCHAR</code>型 {#code-varchar-code-type}

`VARCHAR`は可変長の文字列です。Mは列の最大長（バイト数ではありません）を文字数で表します。2 `VARCHAR`最大サイズは65,535バイトを超えることはできません。4 `VARCHAR`長さは、行の最大長と使用されている文字セットによって決まります。

1文字が占めるスペースは、文字セットによって異なります。次の表は、1文字が消費するバイト数と、各文字セットにおける`VARCHAR`列目の長さの範囲を示しています。

| 文字セット   | 文字あたりのバイト数 | `VARCHAR`カラムの最大長の範囲 |
| ------- | ---------- | ------------------- |
| アスキー    | 1          | （0, 65535）          |
| ラテン1    | 1          | （0, 65535）          |
| バイナリ    | 1          | （0, 65535）          |
| UTF8    | 3          | （0, 21845]          |
| utf8mb4 | 4          | （0, 16383）          |

```sql
[NATIONAL] VARCHAR(M) [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>TEXT</code>タイプ {#code-text-code-type}

`TEXT`は可変長の文字列です。列の最大長は65,535バイトです。オプションのM引数は文字数で、 `TEXT`列の最適な型を自動的に選択するために使用されます。例えば`TEXT(60)`指定すると、最大255バイトを保持できる`TINYTEXT`データ型が生成され、1文字あたり最大4バイト（4×60=240）の60文字のUTF-8文字列に適合します。M引数の使用は推奨されません。

```sql
TEXT[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>TINYTEXT</code>型 {#code-tinytext-code-type}

`TINYTEXT`型は[`TEXT`タイプ](#text-type)と似ていますが、 `TINYTEXT`の最大列長が255である点が異なります。

```sql
TINYTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>MEDIUMTEXT</code>タイプ {#code-mediumtext-code-type}

<CustomContent platform="tidb">

`MEDIUMTEXT`型は[`TEXT`タイプ](#text-type)と似ています。違いは、 `MEDIUMTEXT`の最大列長が16,777,215である点です。ただし、 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500)の制限により、TiDBの1行の最大storageサイズはデフォルトで6MiBですが、設定を変更することで120MiBまで増やすことができます。

</CustomContent>
<CustomContent platform="tidb-cloud">

`MEDIUMTEXT`型は[`TEXT`タイプ](#text-type)と似ています。違いは、 `MEDIUMTEXT`の最大列長が16,777,215である点です。ただし、 [`txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v4010-and-v500)の制限により、TiDBの1行の最大storageサイズはデフォルトで6MiBですが、設定を変更することで120MiBまで増やすことができます。

</CustomContent>

```sql
MEDIUMTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>LONGTEXT</code>型 {#code-longtext-code-type}

<CustomContent platform="tidb">

`LONGTEXT`型は[`TEXT`タイプ](#text-type)型と似ています。違いは、 `LONGTEXT`の最大列長が 4,294,967,295 である点です。ただし、 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500)の制限により、TiDB の単一行の最大storageサイズはデフォルトで 6 MiB となり、設定を変更することで 120 MiB まで増やすことができます。

</CustomContent>
<CustomContent platform="tidb-cloud">

`LONGTEXT`型は[`TEXT`タイプ](#text-type)型と似ています。違いは、 `LONGTEXT`の最大列長が 4,294,967,295 である点です。ただし、 [`txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v4010-and-v500)の制限により、TiDB の単一行の最大storageサイズはデフォルトで 6 MiB となり、設定を変更することで 120 MiB まで増やすことができます。

</CustomContent>

```sql
LONGTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>BINARY</code>型 {#code-binary-code-type}

`BINARY`型は[`CHAR`型](#char-type)と似ています。違いは、 `BINARY`バイナリバイト文字列を格納することです。

```sql
BINARY(M)
```

### <code>VARBINARY</code>型 {#code-varbinary-code-type}

`VARBINARY`型は[`VARCHAR`型](#varchar-type)と似ています。違いは、 `VARBINARY`バイナリバイト文字列を格納するという点です。

```sql
VARBINARY(M)
```

### <code>BLOB</code>型 {#code-blob-code-type}

`BLOB`は大きなバイナリファイルです。M は列の最大長（バイト単位）を表し、範囲は 0 から 65,535 です。

```sql
BLOB[(M)]
```

### <code>TINYBLOB</code>型 {#code-tinyblob-code-type}

`TINYBLOB`型は[`BLOB`型](#blob-type)と似ていますが、 `TINYBLOB`の最大列長が255である点が異なります。

```sql
TINYBLOB
```

### <code>MEDIUMBLOB</code>型 {#code-mediumblob-code-type}

<CustomContent platform="tidb">

`MEDIUMBLOB`型は[`BLOB`型](#blob-type)と似ています。違いは、 `MEDIUMBLOB`の最大列長が16,777,215である点です。ただし、 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500)の制限により、TiDBの1行の最大storageサイズはデフォルトで6MiBですが、設定を変更することで120MiBまで増やすことができます。

</CustomContent>
<CustomContent platform="tidb-cloud">

`MEDIUMBLOB`型は[`BLOB`型](#blob-type)と似ています。違いは、 `MEDIUMBLOB`の最大列長が16,777,215である点です。ただし、 [`txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v4010-and-v500)の制限により、TiDBの1行の最大storageサイズはデフォルトで6MiBですが、設定を変更することで120MiBまで増やすことができます。

</CustomContent>

```sql
MEDIUMBLOB
```

### <code>LONGBLOB</code>型 {#code-longblob-code-type}

<CustomContent platform="tidb">

`LONGBLOB`型は[`BLOB`型](#blob-type)型と似ています。違いは、 `LONGBLOB`の最大列長が 4,294,967,295 である点です。ただし、 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500)の制限により、TiDB の単一行の最大storageサイズはデフォルトで 6 MiB となり、設定を変更することで 120 MiB まで増やすことができます。

</CustomContent>
<CustomContent platform="tidb-cloud">

`LONGBLOB`型は[`BLOB`型](#blob-type)型と似ています。違いは、 `LONGBLOB`の最大列長が 4,294,967,295 である点です。ただし、 [`txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v4010-and-v500)の制限により、TiDB の単一行の最大storageサイズはデフォルトで 6 MiB となり、設定を変更することで 120 MiB まで増やすことができます。

</CustomContent>

```sql
LONGBLOB
```

### <code>ENUM</code>型 {#code-enum-code-type}

`ENUM`は、テーブル作成時に列指定で明示的に列挙された許容値のリストから選択された値を持つ文字列オブジェクトです。構文は次のとおりです。

```sql
ENUM('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]

# For example:
ENUM('apple', 'orange', 'pear')
```

`ENUM`データ型の値は数値として保存されます。各値は定義順序に従って数値に変換されます。前の例では、各文字列が数値にマッピングされています。

| 価値             | 番号 |
| -------------- | -- |
| ヌル             | ヌル |
| &#39;&#39;     | 0  |
| &#39;りんご&#39;  | 1  |
| &#39;オレンジ&#39; | 2  |
| &#39;梨&#39;    | 3  |

詳細については[MySQLのENUM型](https://dev.mysql.com/doc/refman/8.0/en/enum.html)参照してください。

### <code>SET</code>型 {#code-set-code-type}

`SET` 、0 個以上の値を持つことができる文字列オブジェクトです。各値は、テーブルの作成時に指定された許可された値のリストから選択する必要があります。構文は次のとおりです。

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

TiDBでは、 `SET`型の値は内部的に`Int64`に変換されます。各要素の存在は、0または1の2進数で表されます`SET('a','b','c','d')`と指定された列の場合、各要素は以下の10進数と2進数の値を持ちます。

| メンバー        | 小数値 | バイナリ値 |
| ----------- | --- | ----- |
| 「あ」         | 1   | 0001  |
| 「b」         | 2   | 0010  |
| &#39;c&#39; | 4   | 0100  |
| 「d」         | 8   | 1000  |

この場合、 `('a', 'c')`の要素は 2 進数では`0101`になります。

詳細については[MySQLのSET型](https://dev.mysql.com/doc/refman/8.0/en/set.html)参照してください。
