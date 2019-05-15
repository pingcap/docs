---
title: String types
summary: Learn about the data types supported in TiDB.
category: reference
---

# String types

## Overview

TiDB supports all the MySQL string types, including `CHAR`, `VARCHAR`, `BINARY`, `VARBINARY`, `BLOB`, `TEXT`, `ENUM`, and `SET`. For more information, [String Types in MySQL](https://dev.mysql.com/doc/refman/5.7/en/string-types.html).

### `CHAR` Type

```sql
[NATIONAL] CHAR[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```
A fixed-length string. If stored as CHAR, it is right-padded with spaces to the specified length. M represents the column length in characters. The range of M is 0 to 255.

### `VARCHAR` Type

```sql
[NATIONAL] VARCHAR(M) [CHARACTER SET charset_name] [COLLATE collation_name]
```
A variable-length string. M represents the maximum column length in characters. The range of M is 0 to 65,535. The effective maximum length of a VARCHAR is subject to the maximum row size (65,535 bytes, which is shared among all columns) and the character set used.

### `TINYTEXT` Type

```sql
TINYTEXT[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```

A TEXT column with a maximum length of 255 characters.

### `TEXT` Type

```sql
TEXT[(M)] [CHARACTER SET charset_name] [COLLATE collation_name]
```

A TEXT column. M represents the maximum column length ranging from 0 to 65,535. The maximum length of TEXT is based on the size of the longest row and the character set.

### `MEDIUMTEXT` Type

```sql
MEDIUMTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```

A TEXT column with a maximum length of 16,777,215 characters.


### `LONGTEXT` Type

```sql
LONGTEXT [CHARACTER SET charset_name] [COLLATE collation_name]
```
A TEXT column with a maximum length of 4,294,967,295 characters.

### `BINARY` Type

```sql
BINARY(M)
```
The BINARY type is similar to the CHAR type, but stores binary byte strings rather than nonbinary character strings.

### `VARBINARY` Type

```sql
VARBINARY(M)
```
The VARBINARY type is similar to the VARCHAR type, but stores binary byte strings rather than nonbinary character strings.

### `TINYBLOB` Type

```sql
TINYBLOB
```
A BLOB column with a maximum length of 255 bytes.

### `BLOB` Type

```sql
BLOB[(M)]
```
A BLOB column with a maximum length of 65,535 bytes. M represents the maximum column length.

### `MEDIUMBLOB` Type

```sql
MEDIUMBLOB
```
A BLOB column with a maximum length of 16,777,215 bytes.

### `LONGBLOB` Type

```sql
LONGBLOB
```
A BLOB column with a maximum length of 4,294,967,295 bytes.

### `ENUM` Type

An ENUM is a string object with a value chosen from a list of permitted values that are enumerated explicitly in the column specification when the table is created. The syntax is:

```sql
ENUM('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]

# For example:
ENUM('apple', 'orange', 'pear')
```

The value of the ENUM data type is stored as numbers. Each value is converted to a number according the definition order. In the previous example, each string is mapped to a number:

| Value | Number |
| ---- | ---- |
| NULL | NULL |
| '' | 0 |
| 'apple' | 1 |
| 'orange' | 2 |
| 'pear' | 3 |

For more information, see [the ENUM type in MySQL](https://dev.mysql.com/doc/refman/5.7/en/enum.html).

### `SET` Type

A SET is a string object that can have zero or more values, each of which must be chosen from a list of permitted values specified when the table is created. The syntax is:

```sql
SET('value1','value2',...) [CHARACTER SET charset_name] [COLLATE collation_name]

# For example:
SET('1', '2') NOT NULL
```
In the example, any of the following values can be valid:

```
''
'1'
'2'
'1,2'
```
In TiDB, the values of the SET type is internally converted to Int64. The existence of each element is represented using a binary: 0 or 1. For a column specified as `SET('a','b','c','d')`, the members have the following decimal and binary values.

| Member | Decimal Value | Binary Value |
| ---- | ---- | ------ |
| 'a' | 1 | 0001 |
| 'b' | 2 | 0010 |
| 'c' | 4 | 0100 |
| 'd' | 8 | 1000 |

In this case, for an element of `('a', 'c')`, it is 0101 in binary.

For more information, see [the SET type in MySQL](https://dev.mysql.com/doc/refman/5.7/en/set.html).
