---
title: SQL Mode
summary: 学习 SQL 模式。
---

# SQL 模式

TiDB 服务器可以在不同的 SQL 模式下运行，并且对不同的客户端应用这些模式的方式也不同。SQL 模式定义了 TiDB 支持的 SQL 语法以及要执行的数据校验类型，具体如下所述：

TiDB 启动后，你可以使用 `SET [ SESSION | GLOBAL ] sql_mode='modes'` 语句设置 SQL 模式。

- 当在 `GLOBAL` 级别设置 SQL 模式时，确保你拥有 `SUPER` 权限，并且该级别的设置只会影响之后新建立的连接。

- 在 `SESSION` 级别修改 SQL 模式只会影响当前客户端。

在该语句中，`modes` 是由逗号（','）分隔的一组模式。你可以使用 `SELECT @@sql_mode` 语句查看当前的 SQL 模式。SQL 模式的默认值为：`ONLY_FULL_GROUP_BY, STRICT_TRANS_TABLES, NO_ZERO_IN_DATE, NO_ZERO_DATE, ERROR_FOR_DIVISION_BY_ZERO, NO_AUTO_CREATE_USER, NO_ENGINE_SUBSTITUTION`。

## 重要的 `sql_mode` 值

* `ANSI`：该模式遵循标准 SQL。在此模式下，数据会被校验。如果数据不符合定义的类型或长度，数据类型会被调整或截断，并返回 `warning`。
* `STRICT_TRANS_TABLES`：严格模式，数据会被严格校验。如果有任何数据不正确，则无法插入表中，并返回错误。
* `TRADITIONAL`：在此模式下，TiDB 的行为类似于“传统”的 SQL 数据库系统。当向列中插入任何不正确的值时，会返回错误而不是警告。此时，`INSERT` 或 `UPDATE` 语句会立即停止。

## SQL 模式表

| 名称 | 描述 |
| :--- | :--- |
| `PIPES_AS_CONCAT` | 将 "\|\|" 视为字符串连接运算符（`+`，与 `CONCAT()` 相同），而不是 `OR`（完全支持） |
| `ANSI_QUOTES` | 将 `"` 视为标识符。如果启用 `ANSI_QUOTES`，只有单引号被视为字符串字面量，双引号被视为标识符。因此，双引号不能用于引用字符串。（完全支持）|
| `IGNORE_SPACE` | 启用该模式后，系统会忽略空格。例如："user" 和 "user " 被视为相同。（完全支持）|
| `ONLY_FULL_GROUP_BY` | 如果 SQL 语句在 `SELECT`、`HAVING` 或 `ORDER BY` 中引用了既未聚合也未包含在 `GROUP BY` 子句中的列，则该语句无效。因为在查询结果中显示此类列是不正常的。此设置受 [`tidb_enable_new_only_full_group_by_check`](/system-variables.md#tidb_enable_new_only_full_group_by_check-new-in-v610) 系统变量影响。（完全支持）|
| `NO_UNSIGNED_SUBTRACTION` | 如果减法操作数没有符号，则结果不标记为 `UNSIGNED`。（完全支持）|
| `NO_DIR_IN_CREATE` | 创建表时忽略所有 `INDEX DIRECTORY` 和 `DATA DIRECTORY` 指令。该选项仅对二级复制服务器有用（仅语法支持） |
| `NO_KEY_OPTIONS` | 使用 `SHOW CREATE TABLE` 语句时，不导出 MySQL 特有的语法如 `ENGINE`。在使用 mysqldump 跨数据库类型迁移时可考虑此选项。（仅语法支持）|
| `NO_FIELD_OPTIONS` | 使用 `SHOW CREATE TABLE` 语句时，不导出 MySQL 特有的语法如 `ENGINE`。在使用 mysqldump 跨数据库类型迁移时可考虑此选项。（仅语法支持） |
| `NO_TABLE_OPTIONS` | 使用 `SHOW CREATE TABLE` 语句时，不导出 MySQL 特有的语法如 `ENGINE`。在使用 mysqldump 跨数据库类型迁移时可考虑此选项。（仅语法支持）|
| `NO_AUTO_VALUE_ON_ZERO` | 启用该模式后，当 [`AUTO_INCREMENT`](/auto-increment.md) 列传入的值为 `0` 或指定值时，系统会直接将该值写入该列。当传入 `NULL` 时，系统会自动生成下一个序列号。（完全支持）|
| `NO_BACKSLASH_ESCAPES` | 启用该模式后，`\` 反斜杠符号仅表示其本身。（完全支持）|
| `STRICT_TRANS_TABLES` | 为事务存储引擎启用严格模式，在插入无效值后回滚整个语句。（完全支持） |
| `STRICT_ALL_TABLES` | 对于事务表，在插入无效值后回滚整个事务语句。（完全支持） |
| `NO_ZERO_IN_DATE` | 严格模式，不接受月份或日期部分为 `0` 的日期。如果使用 `IGNORE` 选项，TiDB 会为类似日期插入 '0000-00-00'。在非严格模式下，接受此类日期但会返回警告。（完全支持）|
| `NO_ZERO_DATE` | 在严格模式下，不将 '0000-00-00' 作为合法日期使用。你仍然可以通过 `IGNORE` 选项插入零日期。在非严格模式下，接受此类日期但会返回警告。（完全支持）|
| `ALLOW_INVALID_DATES` | 启用该模式后，系统不会校验所有日期的合法性。只校验月份值在 `1` 到 `12` 之间，日期值在 `1` 到 `31` 之间。该模式仅适用于 `DATE` 和 `DATATIME` 列。所有 `TIMESTAMP` 列都需要完整的合法性校验。（完全支持） |
| `ERROR_FOR_DIVISION_BY_ZERO` | 启用该模式后，在数据变更操作（`INSERT` 或 `UPDATE`）中遇到除以 `0` 时，系统返回错误。<br/> 如果未启用该模式，系统返回警告并使用 `NULL` 代替。（完全支持） |
| `NO_AUTO_CREATE_USER` | 阻止 `GRANT` 自动创建新用户，除非指定了密码（完全支持）|
| `HIGH_NOT_PRECEDENCE` | NOT 运算符的优先级使得诸如 `NOT a BETWEEN b AND c` 的表达式被解析为 `NOT (a BETWEEN b AND c)`。在某些旧版本 MySQL 中，该表达式被解析为 `(NOT a) BETWEEN b AND c`。（完全支持） |
| `NO_ENGINE_SUBSTITUTION` | 如果所需存储引擎被禁用或未编译，阻止自动替换存储引擎。（仅语法支持）|
| `PAD_CHAR_TO_FULL_LENGTH` | 启用该模式后，系统不会去除 `CHAR` 类型的尾部空格。（仅语法支持。该模式已在 [MySQL 8.0 中废弃](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_pad_char_to_full_length)。） |
| `REAL_AS_FLOAT` | 将 `REAL` 视为 `FLOAT` 的同义词，而不是 `DOUBLE` 的同义词（完全支持）|
| `POSTGRESQL` | 等价于 `PIPES_AS_CONCAT`、`ANSI_QUOTES`、`IGNORE_SPACE`、`NO_KEY_OPTIONS`、`NO_TABLE_OPTIONS`、`NO_FIELD_OPTIONS`（仅语法支持）|
| `MSSQL` | 等价于 `PIPES_AS_CONCAT`、`ANSI_QUOTES`、`IGNORE_SPACE`、`NO_KEY_OPTIONS`、`NO_TABLE_OPTIONS`、`NO_FIELD_OPTIONS`（仅语法支持）|
| `DB2` | 等价于 `PIPES_AS_CONCAT`、`ANSI_QUOTES`、`IGNORE_SPACE`、`NO_KEY_OPTIONS`、`NO_TABLE_OPTIONS`、`NO_FIELD_OPTIONS`（仅语法支持）|
| `MAXDB` | 等价于 `PIPES_AS_CONCAT`、`ANSI_QUOTES`、`IGNORE_SPACE`、`NO_KEY_OPTIONS`、`NO_TABLE_OPTIONS`、`NO_FIELD_OPTIONS`、`NO_AUTO_CREATE_USER`（完全支持）|
| `MySQL323` | 等价于 `NO_FIELD_OPTIONS`、`HIGH_NOT_PRECEDENCE`（仅语法支持）|
| `MYSQL40` | 等价于 `NO_FIELD_OPTIONS`、`HIGH_NOT_PRECEDENCE`（仅语法支持）|
| `ANSI` | 等价于 `REAL_AS_FLOAT`、`PIPES_AS_CONCAT`、`ANSI_QUOTES`、`IGNORE_SPACE`（仅语法支持）|
| `TRADITIONAL` | 等价于 `STRICT_TRANS_TABLES`、`STRICT_ALL_TABLES`、`NO_ZERO_IN_DATE`、`NO_ZERO_DATE`、`ERROR_FOR_DIVISION_BY_ZERO`、`NO_AUTO_CREATE_USER`（仅语法支持） |
| `ORACLE` | 等价于 `PIPES_AS_CONCAT`、`ANSI_QUOTES`、`IGNORE_SPACE`、`NO_KEY_OPTIONS`、`NO_TABLE_OPTIONS`、`NO_FIELD_OPTIONS`、`NO_AUTO_CREATE_USER`（仅语法支持）|