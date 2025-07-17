---
title: Operators
summary: 了解运算符的优先级、比较函数和运算符、逻辑运算符以及赋值运算符。
---

# Operators

本文档描述了运算符的优先级、比较函数和运算符、逻辑运算符以及赋值运算符。

- [Operator precedence](#operator-precedence)
- [Comparison functions and operators](#comparison-functions-and-operators)
- [Logical operators](#logical-operators)
- [Assignment operators](#assignment-operators)

| Name | Description |
| ---------------------------------------- | ---------------------------------------- |
| [AND, &&](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_and) | 逻辑与 |
| [=](https://dev.mysql.com/doc/refman/8.0/en/assignment-operators.html#operator_assign-equal) | 赋值（作为 [`SET`](https://dev.mysql.com/doc/refman/8.0/en/set-variable.html) 语句的一部分，或作为 [`UPDATE`](https://dev.mysql.com/doc/refman/8.0/en/update.html) 语句中的 `SET` 子句的一部分） |
| [:=](https://dev.mysql.com/doc/refman/8.0/en/assignment-operators.html#operator_assign-value) | 赋值 |
| [BETWEEN ... AND ...](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_between) | 检查一个值是否在某个范围内 |
| [BINARY](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#operator_binary) | 将字符串转换为二进制字符串 |
| &[https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-and] | 位与 |
| [~](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-invert) | 位取反 |
| [\|](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-or) | 位或 |
| [^](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_bitwise-xor) | 位异或 |
| [CASE](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#operator_case) | 条件表达式 |
| [DIV](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_div) | 整数除法 |
| [/](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_divide) | 除法运算符 |
| [=](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal) | 等于运算符 |
| [`<=>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal-to) | NULL 安全相等运算符 |
| [>](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than) | 大于运算符 |
| [>=](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than-or-equal) | 大于等于运算符 |
| [IS](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is) | 测试值是否为布尔值 |
| [IS NOT](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-not) | 测试值是否为布尔值 |
| [IS NOT NULL](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-not-null) | NOT NULL 值测试 |
| [IS NULL](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-null) | NULL 值测试 |
| [->](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_json-column-path) | 评估路径后返回 JSON 列的值；等同于 `JSON_EXTRACT()` |
| [->>](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_json-inline-path) | 评估路径后返回 JSON 列的值并去除引号；等同于 `JSON_UNQUOTE(JSON_EXTRACT())` |
| [<<](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_left-shift) | 左移 |
| [<](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than) | 小于运算符 |
| [<=](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than-or-equal) | 小于等于运算符 |
| [LIKE](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_like) | 简单模式匹配 |
| [ILIKE](https://www.postgresql.org/docs/current/functions-matching.html) | 支持大小写不敏感的简单模式匹配（在 TiDB 中支持，但在 MySQL 中不支持） |
| [-](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_minus) | 减法运算符 |
| [%, MOD](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_mod) | 取模运算符 |
| [NOT, !](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_not) | 取反值 |
| [NOT BETWEEN ... AND ...](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-between) | 检查一个值是否不在某个范围内 |
| [!=, `<>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-equal) | 不等于运算符 |
| [NOT LIKE](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_not-like) | 不匹配简单模式的否定 |
| [NOT REGEXP](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_not-regexp) | REGEXP 的否定 |
| [\|\|, OR](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_or) | 逻辑或 |
| [+](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_plus) | 加法运算符 |
| [REGEXP](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_regexp) | 使用正则表达式进行模式匹配 |
| [>>](https://dev.mysql.com/doc/refman/8.0/en/bit-functions.html#operator_right-shift) | 右移 |
| [RLIKE](https://dev.mysql.com/doc/refman/8.0/en/regexp.html#operator_regexp) | REGEXP 的同义词 |
| [*](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_times) | 乘法运算符 |
| [-](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_unary-minus) | 改变参数的符号 |
| [XOR](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_xor) | 逻辑异或 |

## Unsupported operators

* [`SOUNDS LIKE`](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#operator_sounds-like)

## Operator precedence

运算符优先级由高到低列出。同行显示的运算符具有相同的优先级。

```sql
INTERVAL
BINARY, COLLATE
!
- (一元减号), ~ (一元位取反)
^
*, /, DIV, %, MOD
-, +
<<, >>
&
|
= (比较), <=>, >=, >, <=, <, <>, !=, IS, LIKE, REGEXP, IN
BETWEEN, CASE, WHEN, THEN, ELSE
NOT
AND, &&
XOR
OR, ||
= (赋值), :=
```

详细信息请参见 [Operator Precedence](https://dev.mysql.com/doc/refman/8.0/en/operator-precedence.html)。

## Comparison functions and operators

| Name | Description |
| ---------------------------------------- | ---------------------------------------- |
| [BETWEEN ... AND ...](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_between) | 检查一个值是否在某个范围内 |
| [COALESCE()](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_coalesce) | 返回第一个非 NULL 的参数 |
| [=](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal) | 等于运算符 |
| [`<=>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal-to) | NULL 安全相等运算符 |
| [>](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than) | 大于运算符 |
| [>=](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than-or-equal) | 大于等于运算符 |
| [GREATEST()](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_greatest) | 返回最大值 |
| [IN()](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_in) | 检查一个值是否在某个集合内 |
| [INTERVAL()](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_interval) | 返回第一个参数小于的索引值 |
| [IS](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is) | 测试值是否为布尔值 |
| [IS NOT](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-not) | 测试值是否为布尔值 |
| [IS NOT NULL](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-not-null) | NOT NULL 值测试 |
| [IS NULL](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-null) | NULL 值测试 |
| [ISNULL()](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_isnull) | 测试参数是否为 NULL |
| [LEAST()](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_least) | 返回最小值 |
| [<](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than) | 小于运算符 |
| [<=](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than-or-equal) | 小于等于运算符 |
| [LIKE](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_like) | 简单模式匹配 |
| [ILIKE](https://www.postgresql.org/docs/current/functions-matching.html) | 支持大小写不敏感的简单模式匹配（在 TiDB 中支持，但在 MySQL 中不支持） |
| [NOT BETWEEN ... AND ...](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-between) | 检查一个值是否不在某个范围内 |
| [!=, `<>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-equal) | 不等于运算符 |
| [NOT IN()](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-in) | 检查一个值是否不在某个集合内 |
| [NOT LIKE](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#operator_not-like) | 不匹配简单模式的否定 |
| [STRCMP()](https://dev.mysql.com/doc/refman/8.0/en/string-comparison-functions.html#function_strcmp) | 比较两个字符串 |

详细信息请参见 [Comparison Functions and Operators](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html)。

## Logical operators

| Name | Description |
| ---------------------------------------- | ------------- |
| [AND, &&](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_and) | 逻辑与 |
| [NOT, !](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_not) | 取反值 |
| [\|\|, OR](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_or) | 逻辑或 |
| [XOR](https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html#operator_xor) | 逻辑异或 |

详细信息请参见 [MySQL Handling of GROUP BY](https://dev.mysql.com/doc/refman/8.0/en/group-by-handling.html)。

## Assignment operators

| Name | Description |
| ---------------------------------------- | ---------------------------------------- |
| [=](https://dev.mysql.com/doc/refman/8.0/en/assignment-operators.html#operator_assign-equal) | 赋值（作为 [`SET`](https://dev.mysql.com/doc/refman/8.0/en/set-variable.html) 语句的一部分，或作为 [`UPDATE`](https://dev.mysql.com/doc/refman/8.0/en/update.html) 语句中的 `SET` 子句的一部分） |
| [:=](https://dev.mysql.com/doc/refman/8.0/en/assignment-operators.html#operator_assign-value) | 赋值 |

详细信息请参见 [Detection of Functional Dependence](https://dev.mysql.com/doc/refman/8.0/en/group-by-functional-dependence.html)。

## MySQL compatibility

* MySQL 不支持 `ILIKE` 运算符。