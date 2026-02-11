---
title: TiDB 数据类型
summary: 了解 TiDB 中数据类型的默认值。
---

# 默认值

在数据类型规范中，`DEFAULT` 值子句用于指定列的默认值。

你可以为所有数据类型设置默认值。通常，默认值必须是常数，不能是函数或表达式，但也有一些例外情况：

- 对于时间类型，你可以使用 `NOW`、`CURRENT_TIMESTAMP`、`LOCALTIME` 和 `LOCALTIMESTAMP` 函数作为 `TIMESTAMP` 和 `DATETIME` 列的默认值。
- 对于整数型，你可以使用 `NEXT VALUE FOR` 函数将序列的下一个值设置为列的默认值，并使用 [`RAND()`](/functions-and-operators/numeric-functions-and-operators.md) 函数生成一个随机 float 值作为列的默认值。
- 对于字符串类型，你可以使用 [`UUID()`](/functions-and-operators/miscellaneous-functions.md) 函数生成一个 [通用唯一标识符（UUID）](/best-practices/uuid.md) 作为列的默认值。
- 对于二进制类型，你可以使用 [`UUID_TO_BIN()`](/functions-and-operators/miscellaneous-functions.md) 函数将 UUID 转换为二进制格式，并将转换后的值设置为列的默认值。
- 从 v8.0.0 开始，TiDB 还支持为 [`BLOB`](/data-type-string.md#blob-type)、[`TEXT`](/data-type-string.md#text-type) 和 [`JSON`](/data-type-json.md#json-data-type) 数据类型 [指定默认值](#specify-expressions-as-default-values)，但你只能使用表达式为它们设置 [默认值](#default-values)。

如果列定义中没有显式的 `DEFAULT` 值，TiDB 会按如下方式确定默认值：

- 如果该列可以取 `NULL` 值，则该列会被定义为显式的 `DEFAULT NULL` 子句。
- 如果该列不能取 `NULL` 值，TiDB 会为该列定义时不加显式的 `DEFAULT` 子句。

对于没有显式 `DEFAULT` 子句的 `NOT NULL` 列，在向该列插入数据时，如果 `INSERT` 或 `REPLACE` 语句未为该列提供值，TiDB 会根据当时生效的 SQL 模式进行处理：

- 如果启用了严格 SQL 模式，对于事务表会报错并回滚该语句。对于非事务表也会报错。
- 如果未启用严格模式，TiDB 会将该列设置为该数据类型的隐式默认值。

隐式默认值定义如下：

- 对于数值类型，默认值为 0。如果声明了 `AUTO_INCREMENT` 属性，则默认值为序列中的下一个值。
- 对于除 `TIMESTAMP` 以外的日期和时间类型，默认值为该类型的合适 “零” 值。对于 `TIMESTAMP`，默认值为当前日期和时间。
- 对于除 `ENUM` 以外的字符串类型，默认值为空字符串。对于 `ENUM`，默认值为第一个枚举值。

## 指定表达式作为默认值

从 8.0.13 版本开始，MySQL 支持在 `DEFAULT` 子句中指定表达式作为默认值。更多信息请参见 [MySQL 8.0.13 起的显式默认值处理](https://dev.mysql.com/doc/refman/8.0/en/data-type-defaults.html#data-type-defaults-explicit)。

TiDB 支持在 `DEFAULT` 子句中指定以下表达式作为默认值。

* `UPPER(SUBSTRING_INDEX(USER(), '@', 1))`
* `REPLACE(UPPER(UUID()), '-', '')`
* 以下格式的 `DATE_FORMAT` 表达式：
    * `DATE_FORMAT(NOW(), '%Y-%m')`
    * `DATE_FORMAT(NOW(), '%Y-%m-%d')`
    * `DATE_FORMAT(NOW(), '%Y-%m-%d %H.%i.%s')`
    * `DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%s')`
* `STR_TO_DATE('1980-01-01', '%Y-%m-%d')`
* [`CURRENT_TIMESTAMP()`](/functions-and-operators/date-and-time-functions.md)、[`CURRENT_DATE()`](/functions-and-operators/date-and-time-functions.md)：两者都使用默认的小数秒精度（fsp）
* [`JSON_OBJECT()`](/functions-and-operators/json-functions.md)、[`JSON_ARRAY()`](/functions-and-operators/json-functions.md)、[`JSON_QUOTE()`](/functions-and-operators/json-functions.md)
* [`NEXTVAL()`](/functions-and-operators/sequence-functions.md#nextval)
* [`RAND()`](/functions-and-operators/numeric-functions-and-operators.md)
* [`UUID()`](/functions-and-operators/miscellaneous-functions.md#uuid)、[`UUID_TO_BIN()`](/functions-and-operators/miscellaneous-functions.md#uuid_to_bin)
* [`VEC_FROM_TEXT()`](/ai/reference/vector-search-functions-and-operators.md#vec_from_text)

TiDB 支持为 `BLOB`、`TEXT` 和 `JSON` 数据类型分配默认值。但你只能使用表达式，而不能使用字面量，为这些数据类型定义默认值。以下是 `BLOB` 的示例：

```sql
CREATE TABLE t2 (
  b BLOB DEFAULT (RAND())
);
```

使用 UUID 的示例：

```sql
CREATE TABLE t3 (
  uuid BINARY(16) DEFAULT (UUID_TO_BIN(UUID())),
  name VARCHAR(255)
);
```

关于如何使用 UUID 的更多信息，请参见 [使用 UUID 作为主键的最佳实践](/best-practices/uuid.md)。

使用 `JSON` 的示例：

```sql
CREATE TABLE t4 (
  id bigint AUTO_RANDOM PRIMARY KEY,
  j json DEFAULT (JSON_OBJECT("a", 1, "b", 2))
);
```

不允许的 `JSON` 示例：

```sql
CREATE TABLE t5 (
  id bigint AUTO_RANDOM PRIMARY KEY,
  j json DEFAULT ('{"a": 1, "b": 2}')
);
```

最后两个示例展示了类似的默认值，但只有第一个是合法的，因为它使用了表达式而不是字面量。