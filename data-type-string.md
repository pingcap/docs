---
title: String types
summary: Learn about the string types supported in TiDB.
---

# 文字列型 {#string-types}

`VARCHAR`は、 `CHAR` 、 `TEXT` `BINARY`を`ENUM`すべての`BLOB`文字列型を`SET`し`VARBINARY` 。詳細については、 [MySQLの文字列型](https://dev.mysql.com/doc/refman/5.7/en/string-types.html)を参照してください。

## サポートされているタイプ {#supported-types}

### <code>CHAR</code>タイプ {#code-char-code-type}

`CHAR`は固定長の文字列です。 Mは、列の長さを文字数（バイトではなく）で表します。 Mの範囲は0〜255です`VARCHAR`タイプとは異なり、データが`CHAR`列に挿入されると、末尾のスペースが切り捨てられます。

```sql
[NATIONAL] CHAR[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>VARCHAR</code>タイプ {#code-varchar-code-type}

`VARCHAR`は可変長の文字列です。 Mは、列の最大長を文字数（バイトではなく）で表します。 `VARCHAR`の最大サイズは65,535バイトを超えることはできません。行の最大長と使用されている文字セットによって、 `VARCHAR`の長さが決まります。

1つの文字が占めるスペースは、文字セットによって異なる場合があります。次の表は、1文字で消費されるバイト数と、各文字セットの`VARCHAR`列の長さの範囲を示しています。

| キャラクターセット | 文字あたりのバイト数 | 最大`VARCHAR`列の長さの範囲 |
| --------- | ---------- | ------------------ |
| アスキー      | 1          | （0、65535]          |
| latin1    | 1          | （0、65535]          |
| バイナリ      | 1          | （0、65535]          |
| utf8      | 3          | （0、21845]          |
| utf8mb4   | 4          | （0、16383]          |

```sql
[NATIONAL] VARCHAR(M) [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>TEXT</code>タイプ {#code-text-code-type}

`TEXT`は可変長の文字列です。 Mは、0〜65,535の範囲の最大列長を文字数で表します。行の最大長と使用されている文字セットによって、 `TEXT`の長さが決まります。

```sql
TEXT[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>TINYTEXT</code>タイプ {#code-tinytext-code-type}

`TINYTEXT`タイプは[`TEXT`タイプ](#text-type)に似ています。違いは、 `TINYTEXT`の最大列長が255であるということです。

```sql
TINYTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>MEDIUMTEXT</code>タイプ {#code-mediumtext-code-type}

`MEDIUMTEXT`タイプは[`TEXT`タイプ](#text-type)に似ています。違いは、 `MEDIUMTEXT`の最大列長が16,777,215であるということです。

```sql
MEDIUMTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>LONGTEXT</code>タイプ {#code-longtext-code-type}

`LONGTEXT`タイプは[`TEXT`タイプ](#text-type)に似ています。違いは、 `LONGTEXT`の最大列長が4,294,967,295であるということです。

```sql
LONGTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### <code>BINARY</code>タイプ {#code-binary-code-type}

`BINARY`タイプは[`CHAR`タイプ](#char-type)に似ています。違いは、 `BINARY`がバイナリバイト文字列を格納することです。

```sql
BINARY(M)
```

### <code>VARBINARY</code>タイプ {#code-varbinary-code-type}

`VARBINARY`タイプは[`VARCHAR`タイプ](#varchar-type)に似ています。違いは、 `VARBINARY`がバイナリバイト文字列を格納することです。

```sql
VARBINARY(M)
```

### <code>BLOB</code>タイプ {#code-blob-code-type}

`BLOB`は大きなバイナリファイルです。 Mは、0〜65,535の範囲の最大列長をバイト単位で表します。

```sql
BLOB[(M)]
```

### <code>TINYBLOB</code>タイプ {#code-tinyblob-code-type}

`TINYBLOB`タイプは[`BLOB`タイプ](#blob-type)に似ています。違いは、 `TINYBLOB`の最大列長が255であるということです。

```sql
TINYBLOB
```

### <code>MEDIUMBLOB</code>タイプ {#code-mediumblob-code-type}

`MEDIUMBLOB`タイプは[`BLOB`タイプ](#blob-type)に似ています。違いは、 `MEDIUMBLOB`の最大列長が16,777,215であるということです。

```sql
MEDIUMBLOB
```

### <code>LONGBLOB</code>タイプ {#code-longblob-code-type}

`LONGBLOB`タイプは[`BLOB`タイプ](#blob-type)に似ています。違いは、 `LONGBLOB`の最大列長が4,294,967,295であるということです。

```sql
LONGBLOB
```

### <code>ENUM</code>タイプ {#code-enum-code-type}

`ENUM`は、テーブルの作成時に列仕様に明示的に列挙される許可された値のリストから選択された値を持つ文字列オブジェクトです。構文は次のとおりです。

```sql
ENUM('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]

# For example:
ENUM('apple', 'orange', 'pear')
```

`ENUM`データ型の値は数値として格納されます。各値は、定義順に数値に変換されます。前の例では、各文字列は数値にマップされています。

| 価値             | 番号 |
| -------------- | -- |
| ヌル             | ヌル |
| &#39;&#39;     | 0  |
| &#39;りんご&#39;  | 1  |
| &#39;オレンジ&#39; | 2  |
| &#39;梨&#39;    | 3  |

詳細については、 [MySQLのENUMタイプ](https://dev.mysql.com/doc/refman/5.7/en/enum.html)を参照してください。

### <code>SET</code>タイプ {#code-set-code-type}

`SET`は、0個以上の値を持つことができる文字列オブジェクトであり、各値は、テーブルの作成時に指定された許可された値のリストから選択する必要があります。構文は次のとおりです。

```sql
SET('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]

# For example:
SET('1', '2') NOT NULL
```

この例では、次の値のいずれかが有効である可能性があります。

```
''
'1'
'2'
'1,2'
```

TiDBでは、 `SET`タイプの値は内部で`Int64`に変換されます。各要素の存在は、0または1の2進数を使用して表されます`SET('a','b','c','d')`として指定された列の場合、メンバーには次の10進数値と2進数値があります。

| メンバー        | 10進値 | バイナリ値 |
| ----------- | ---- | ----- |
| &#39;a&#39; | 1    | 0001  |
| &#39;b&#39; | 2    | 0010  |
| &#39;c&#39; | 4    | 0100  |
| &#39;d&#39; | 8    | 1000  |

この場合、 `('a', 'c')`の要素の場合、バイナリでは`0101`になります。

詳細については、 [MySQLのSETタイプ](https://dev.mysql.com/doc/refman/5.7/en/set.html)を参照してください。
