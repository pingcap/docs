---
title: SQL Mode
summary: 学习 SQL 模式。
---

# SQL 模式

TiDB 服务器在不同的 SQL 模式下运行，并对不同的客户端应用这些模式。SQL 模式定义了 TiDB 支持的 SQL 语法以及要执行的数据验证检查类型，具体如下所述：

在 TiDB 启动后，你可以使用 `SET [ SESSION | GLOBAL ] sql_mode='modes'` 语句来设置 SQL 模式。

- 在 `GLOBAL` 级别设置 SQL 模式时，确保你具有 `SUPER` 权限，并且你在此级别的设置只影响之后建立的连接。

- 在 `SESSION` 级别对 SQL 模式的更改只影响当前客户端。

在此语句中，`modes` 是由逗号（','）分隔的一组模式。你可以使用 `SELECT @@sql_mode` 语句来检查当前的 SQL 模式。SQL 模式的默认值为：`ONLY_FULL_GROUP_BY, STRICT_TRANS_TABLES, NO_ZERO_IN_DATE, NO_ZERO_DATE, ERROR_FOR_DIVISION_BY_ZERO, NO_AUTO_CREATE_USER, NO_ENGINE_SUBSTITUTION`。

## 重要的 `sql_mode` 值

* `ANSI`：此模式符合标准 SQL。在此模式下，系统会检查数据。如果数据不符合定义的类型或长度，会调整数据类型或修剪，并返回 `warning`。
* `STRICT_TRANS_TABLES`：严格模式，数据会被严格检查。如果任何数据不正确，不能插入表中，并返回错误。
* `TRADITIONAL`：在此模式下，TiDB 行为类似于“传统” SQL 数据库系统。当向列中插入不正确的值时，会返回错误而非警告。然后，`INSERT` 或 `UPDATE` 语句会立即停止。

## SQL 模式表

| 名称 | 描述 |
| :--- | :--- |
| `PIPES_AS_CONCAT` | 将 "\|\|" 视为字符串连接运算符 (`+`)（与 `CONCAT()` 相同），而不是 `OR`（完全支持） |
| `ANSI_QUOTES` | 将 `"` 视为标识符。如果启用 `ANSI_QUOTES`，则只有单引号被视为字符串字面量，双引号被视为标识符。因此，不能用双引号引用字符串。（完全支持）|
| `IGNORE_SPACE` | 如果启用此模式，系统会忽略空格。例如："user" 和 "user " 被视为相同。（完全支持）|
| `ONLY_FULL_GROUP_BY` | 如果 `SELECT`、`HAVING` 或 `ORDER BY` 中引用的列既未聚合也未包含在 `GROUP BY` 子句中，则 SQL 语句无效。因为在查询结果中显示此类列是不正常的。此设置受系统变量 [`tidb_enable_new_only_full_group_by_check`](/system-variables.md#tidb_enable_new_only_full_group_by_check-new-in-v610) 影响。（完全支持）|
| `NO_UNSIGNED_SUBTRACTION` | 在减法操作中，如果操作数没有符号，不会将结果标记为 `UNSIGNED`。（完全支持）|
| `NO_DIR_IN_CREATE` | 在创建表时忽略所有 `INDEX DIRECTORY` 和 `DATA DIRECTORY` 指令。此选项仅对二级复制服务器有用（仅支持语法） |
| `NO_KEY_OPTIONS` | 使用 `SHOW CREATE TABLE` 语句时，不导出 MySQL 特有的语法，如 `ENGINE`。在使用 mysqldump 迁移不同数据库类型时考虑此选项。（仅支持语法）|
| `NO_FIELD_OPTIONS` | 使用 `SHOW CREATE TABLE` 语句时，不导出 MySQL 特有的语法，如 `ENGINE`。在使用 mysqldump 迁移不同数据库类型时考虑此选项。（仅支持语法） |
| `NO_TABLE_OPTIONS` | 使用 `SHOW CREATE TABLE` 语句时，不导出 MySQL 特有的语法，如 `ENGINE`。在使用 mysqldump 迁移不同数据库类型时考虑此选项。（仅支持语法）|
| `NO_AUTO_VALUE_ON_ZERO` | 如果启用此模式，当传入 [`AUTO_INCREMENT`](/auto-increment.md) 列的值为 `0` 或特定值时，系统会直接写入此值到该列。当传入 `NULL` 时，系统会自动生成下一个序列号。（完全支持）|
| `NO_BACKSLASH_ESCAPES` | 如果启用此模式，`\` 反斜杠符号只代表其自身。（完全支持）|
| `STRICT_TRANS_TABLES` | 为事务存储引擎启用严格模式，在插入非法值后回滚整个语句。（完全支持） |
| `STRICT_ALL_TABLES` | 对于事务表，在插入非法值后回滚整个事务语句。（完全支持） |
| `NO_ZERO_IN_DATE` | 严格模式，不接受月份或日期部分为 `0` 的日期。如果使用 `IGNORE` 选项，TiDB 会插入 `'0000-00-00'` 作为类似日期。在非严格模式下，此日期被接受，但会返回警告。（完全支持）|
| `NO_ZERO_DATE` | 在严格模式下，不允许 `'0000-00-00'` 作为合法日期。你仍然可以使用 `IGNORE` 选项插入零日期。在非严格模式下，此日期被接受，但会返回警告。（完全支持）|
| `ALLOW_INVALID_DATES` | 在此模式下，系统不会检查所有日期的有效性，只会检查月份值是否在 `1` 到 `12` 之间，日期值是否在 `1` 到 `31` 之间。此模式仅适用于 `DATE` 和 `DATATIME` 列。所有 `TIMESTAMP` 列仍需进行完整的有效性检查。（完全支持） |
| `ERROR_FOR_DIVISION_BY_ZERO` | 如果启用此模式，处理除以 `0` 的数据变更操作（`INSERT` 或 `UPDATE`）时，系统会返回错误。<br/>如果未启用此模式，系统会返回警告，并使用 `NULL` 代替。（完全支持） |
| `NO_AUTO_CREATE_USER` | 阻止 `GRANT` 自动创建新用户，除非指定密码（完全支持）|
| `HIGH_NOT_PRECEDENCE` | NOT 运算符的优先级使得表达式如 `NOT a BETWEEN b AND c` 被解析为 `NOT (a BETWEEN b AND c)`。在某些旧版本的 MySQL 中，此表达式被解析为 `(NOT a) BETWEEN b AND c`。（完全支持） |
| `NO_ENGINE_SUBSTITUTION` | 阻止在所需存储引擎被禁用或未编译时自动替换存储引擎。（仅支持语法）|
| `PAD_CHAR_TO_FULL_LENGTH` | 如果启用此模式，系统不会修剪 `CHAR` 类型的尾随空格。（仅支持语法。此模式已在 [MySQL 8.0 中弃用](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_pad_char_to_full_length)。） |
| `REAL_AS_FLOAT` | 将 `REAL` 视为 `FLOAT` 的同义词，而非 `DOUBLE` 的同义词（完全支持）|
| `POSTGRESQL` | 等同于 `PIPES_AS_CONCAT`、`ANSI_QUOTES`、`IGNORE_SPACE`、`NO_KEY_OPTIONS`、`NO_TABLE_OPTIONS`、`NO_FIELD_OPTIONS`（仅支持语法）|
| `MSSQL` | 等同于 `PIPES_AS_CONCAT`、`ANSI_QUOTES`、`IGNORE_SPACE`、`NO_KEY_OPTIONS`、`NO_TABLE_OPTIONS`、`NO_FIELD_OPTIONS`（仅支持语法）|
| `DB2` | 等同于 `PIPES_AS_CONCAT`、`ANSI_QUOTES`、`IGNORE_SPACE`、`NO_KEY_OPTIONS`、`NO_TABLE_OPTIONS`、`NO_FIELD_OPTIONS`（仅支持语法）|
| `MAXDB` | 等同于 `PIPES_AS_CONCAT`、`ANSI_QUOTES`、`IGNORE_SPACE`、`NO_KEY_OPTIONS`、`NO_TABLE_OPTIONS`、`NO_FIELD_OPTIONS`、`NO_AUTO_CREATE_USER`（完全支持）|
| `MySQL323` | 等同于 `NO_FIELD_OPTIONS`、`HIGH_NOT_PRECEDENCE`（仅支持语法）|
| `MYSQL40` | 等同于 `NO_FIELD_OPTIONS`、`HIGH_NOT_PRECEDENCE`（仅支持语法）|
| `ANSI` | 等同于 `REAL_AS_FLOAT`、`PIPES_AS_CONCAT`、`ANSI_QUOTES`、`IGNORE_SPACE`（仅支持语法）|
| `TRADITIONAL` | 等同于 `STRICT_TRANS_TABLES`、`STRICT_ALL_TABLES`、`NO_ZERO_IN_DATE`、`NO_ZERO_DATE`、`ERROR_FOR_DIVISION_BY_ZERO`、`NO_AUTO_CREATE_USER`（仅支持语法） |
| `ORACLE` | 等同于 `PIPES_AS_CONCAT`、`ANSI_QUOTES`、`IGNORE_SPACE`、`NO_KEY_OPTIONS`、`NO_TABLE_OPTIONS`、`NO_FIELD_OPTIONS`、`NO_AUTO_CREATE_USER`（仅支持语法）|