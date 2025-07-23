---
title: String types
summary: 了解 TiDB 支持的字符串类型。
---

# String Types

TiDB 支持所有 MySQL 的字符串类型，包括 `CHAR`、`VARCHAR`、`BINARY`、`VARBINARY`、`BLOB`、`TEXT`、`ENUM` 和 `SET`。更多信息请参见 [String Types in MySQL](https://dev.mysql.com/doc/refman/8.0/en/string-types.html)。

## 支持的类型

### `CHAR` 类型

`CHAR` 是固定长度字符串。M 表示列的长度（以字符为单位，而非字节）。M 的取值范围为 0 到 255。与 `VARCHAR` 类型不同，当数据插入到 `CHAR` 列时，尾部空格会被截断。

```sql
[NATIONAL] CHAR[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `VARCHAR` 类型

`VARCHAR` 是可变长度字符串。M 表示最大列长度（以字符为单位，而非字节）。`VARCHAR` 的最大尺寸不能超过 65,535 字节。最大行长度和所使用的字符集共同决定 `VARCHAR` 的长度。

不同字符集的单个字符占用的字节数可能不同。下表显示了每个字符集中的单个字符所占的字节数，以及每个字符集中的 `VARCHAR` 列长度范围：

| 字符集 | 每个字符的字节数 | 最大 `VARCHAR` 列长度范围 |
| ----- | ---- | ---- |
| ascii | 1 | (0, 65535] |
| latin1 | 1 | (0, 65535] |
| binary | 1 | (0, 65535] |
| utf8 | 3 | (0, 21845] |
| utf8mb4 | 4 | (0, 16383] |

```sql
[NATIONAL] VARCHAR(M) [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `TEXT` 类型

`TEXT` 是可变长度字符串。最大列长度为 65,535 字节。可选的 M 参数以字符为单位，用于自动选择最合适的 `TEXT` 类型。例如 `TEXT(60)` 会生成一个 `TINYTEXT` 类型，最多可存储 255 字节，适合存储最多 60 个字符（每个字符最多 4 字节，4×60=240）。不建议使用 M 参数。

```sql
TEXT[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `TINYTEXT` 类型

`TINYTEXT` 类型类似于 [`TEXT` 类型](#text-type)。区别在于 `TINYTEXT` 的最大列长度为 255。

```sql
TINYTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `MEDIUMTEXT` 类型

<CustomContent platform="tidb">

`MEDIUMTEXT` 类型类似于 [`TEXT` 类型](#text-type)。区别在于 `MEDIUMTEXT` 的最大列长度为 16,777,215。但由于 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500) 的限制，TiDB 中单行的最大存储大小默认为 6 MiB，可以通过修改配置将其提高到 120 MiB。

</CustomContent>
<CustomContent platform="tidb-cloud">

`MEDIUMTEXT` 类型类似于 [`TEXT` 类型](#text-type)。区别在于 `MEDIUMTEXT` 的最大列长度为 16,777,215。但由于 [`txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v4010-and-v500) 的限制，TiDB 中单行的最大存储大小默认为 6 MiB，可以通过修改配置将其提高到 120 MiB。

</CustomContent>

```sql
MEDIUMTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `LONGTEXT` 类型

<CustomContent platform="tidb">

`LONGTEXT` 类型类似于 [`TEXT` 类型](#text-type)。区别在于 `LONGTEXT` 的最大列长度为 4,294,967,295。但由于 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500) 的限制，TiDB 中单行的最大存储大小默认为 6 MiB，可以通过修改配置将其提高到 120 MiB。

</CustomContent>
<CustomContent platform="tidb-cloud">

`LONGTEXT` 类型类似于 [`TEXT` 类型](#text-type)。区别在于 `LONGTEXT` 的最大列长度为 4,294,967,295。但由于 [`txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v4010-and-v500) 的限制，TiDB 中单行的最大存储大小默认为 6 MiB，可以通过修改配置将其提高到 120 MiB。

</CustomContent>

```sql
LONGTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

### `BINARY` 类型

`BINARY` 类型类似于 [`CHAR` 类型](#char-type)。区别在于 `BINARY` 存储二进制字节字符串。

```sql
BINARY(M)
```

### `VARBINARY` 类型

`VARBINARY` 类型类似于 [`VARCHAR` 类型](#varchar-type)。区别在于 `VARBINARY` 存储二进制字节字符串。

```sql
VARBINARY(M)
```

### `BLOB` 类型

`BLOB` 是大型二进制文件。M 表示最大列长度（以字节为单位），范围为 0 到 65,535。

```sql
BLOB[(M)]
```

### `TINYBLOB` 类型

`TINYBLOB` 类型类似于 [`BLOB` 类型](#blob-type)。区别在于 `TINYBLOB` 的最大列长度为 255。

```sql
TINYBLOB
```

### `MEDIUMBLOB` 类型

<CustomContent platform="tidb">

`MEDIUMBLOB` 类型类似于 [`BLOB` 类型](#blob-type)。区别在于 `MEDIUMBLOB` 的最大列长度为 16,777,215。但由于 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500) 的限制，TiDB 中单行的最大存储大小默认为 6 MiB，可以通过修改配置将其提高到 120 MiB。

</CustomContent>
<CustomContent platform="tidb-cloud">

`MEDIUMBLOB` 类型类似于 [`BLOB` 类型](#blob-type)。区别在于 `MEDIUMBLOB` 的最大列长度为 16,777,215。但由于 [`txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v4010-and-v500) 的限制，TiDB 中单行的最大存储大小默认为 6 MiB，可以通过修改配置将其提高到 120 MiB。

</CustomContent>

```sql
MEDIUMBLOB
```

### `LONGBLOB` 类型

<CustomContent platform="tidb">

`LONGBLOB` 类型类似于 [`BLOB` 类型](#blob-type)。区别在于 `LONGBLOB` 的最大列长度为 4,294,967,295。但由于 [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500) 的限制，TiDB 中单行的最大存储大小默认为 6 MiB，可以通过修改配置将其提高到 120 MiB。

</CustomContent>
<CustomContent platform="tidb-cloud">

`LONGBLOB` 类型类似于 [`BLOB` 类型](#blob-type)。区别在于 `LONGBLOB` 的最大列长度为 4,294,967,295。但由于 [`txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v4010-and-v500) 的限制，TiDB 中单行的最大存储大小默认为 6 MiB，可以通过修改配置将其提高到 120 MiB。

</CustomContent>

```sql
LONGBLOB
```

### `ENUM` 类型

`ENUM` 是一种字符串对象，其值从在创建表时显式列出允许值的列表中选择。语法如下：

```sql
ENUM('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]

# 例如：
ENUM('apple', 'orange', 'pear')
```

`ENUM` 数据类型的值以数字存储。每个值根据定义顺序转换为数字。在前述示例中，每个字符串映射为一个数字：

| 值 | 数字 |
| ---- | ---- |
| NULL | NULL |
| '' | 0 |
| 'apple' | 1 |
| 'orange' | 2 |
| 'pear' | 3 |

更多信息请参见 [the ENUM type in MySQL](https://dev.mysql.com/doc/refman/8.0/en/enum.html)。

### `SET` 类型

`SET` 是一种字符串对象，可以包含零个或多个值，每个值必须从在创建表时指定的允许值列表中选择。语法如下：

```sql
SET('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]

# 例如：
SET('1', '2') NOT NULL
```

在示例中，以下任意值都可以是有效的：

```
''
'1'
'2'
'1,2'
```

在 TiDB 中，`SET` 类型的值会被内部转换为 `Int64`。每个元素的存在用二进制表示：0 或 1。对于指定为 `SET('a','b','c','d')` 的列，其成员对应的十进制和二进制值如下：

| 成员 | 十进制值 | 二进制值 |
| ---- | ---- | ------ |
| 'a' | 1 | 0001 |
| 'b' | 2 | 0010 |
| 'c' | 4 | 0100 |
| 'd' | 8 | 1000 |

在这种情况下，元素 `('a', 'c')` 的二进制表示为 `0101`。

更多信息请参见 [the SET type in MySQL](https://dev.mysql.com/doc/refman/8.0/en/set.html)。