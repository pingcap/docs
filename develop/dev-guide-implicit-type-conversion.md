---
title: Avoid Implicit Type Conversions
summary: Introduces the possible consequences of implicit type conversions in TiDB and ways to avoid them.
---

# Avoid Implicit Type Conversions

This page introduces the possible consequences of implicit type conversions in TiDB and ways to avoid them.

## Conversion rules

When the data types on both sides of a predicate in SQL do not match, TiDB will implicitly convert the data types on one or both sides to a compatible data type for predicate operations.

The rules for implicit type conversion in TiDB are as follows:

- If one or both arguments are `NULL`, the result of the comparison is `NULL` (except for the NULL-safe `<=>` equivalent comparison operator, which results in `true` for NULL `<=>` NULL and does not require conversion).
- If both arguments in the comparison operation are strings, they are compared as strings.
- If both arguments are integers, they are compared as integers.
- If no comparison is made with numbers, the hexadecimal value is treated as a binary string.
- If one of the arguments is a decimal value, the comparison depends on the other argument. If the other parameter is a decimal or integer value, the parameter is compared to the decimal value, and if the other parameter is a floating-point value, the parameter is compared to the floating-point value.
- If one of the parameters is a `TIMESTAMP` or `DATETIME` column and the other parameter is a constant, the constant is converted to a timestamp before performing the comparison.
- In all other cases, the parameters are compared as floating-point numbers (`DOUBLE` type).

## Consequences caused by implicit type conversion

Implicit type conversions increase the ease of human-computer interaction, but we should try to avoid them in application code, due to the fact that they can lead to:

- Index invalidity
- Loss of precision

### Index invalidity

In the following case, `account_id` is the primary key and its data type is `varchar`. As you can see from the execution plan, this SQL has an implicit type conversion and cannot use the index.

{{< copyable "sql" >}}

```sql
DESC SELECT * FROM `account` WHERE `account_id`=6010000000009801;
+-------------------------+----------------+-----------+---------------+------------------------------------------------------------+
| id                      | estRows        | task      | access object | operator info                                              |
+-------------------------+----------------+-----------+---------------+------------------------------------------------------------+
| TableReader_7           | 8000628000.00  | root      |               | data:Selection_6                                           |
| └─Selection_6           | 8000628000.00  | cop[tikv] |               | eq(cast(findpt.account.account_id), 6.010000000009801e+15) |
|   └─TableFullScan_5     | 10000785000.00 | cop[tikv] | table:account | keep order:false                                           |
+-------------------------+----------------+-----------+---------------+------------------------------------------------------------+
3 rows in set (0.00 sec)
```

**Brief description of run results**: From the above execution plan, the `Cast` operator is visible.

### Loss of precision

In the following case, the data type of field a is `decimal(32,0)`. From the execution plan, we know that there is an implicit type conversion, and both the decimal field and the string constant are converted to double type, but the precision of `double` type is not as high as `decimal`, so there is a loss of precision, and in this case, it causes the error of filtering the result set out of range.

{{< copyable "sql" >}}

```sql
DESC SELECT * FROM `t1` WHERE `a` BETWEEN '12123123' AND '1111222211111111200000';
+-------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------+
| id                      | estRows | task      | access object | operator info                                                                       |
+-------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------+
| TableReader_7           | 0.80    | root      |               | data:Selection_6                                                                    |
| └─Selection_6           | 0.80    | cop[tikv] |               | ge(cast(findpt.t1.a), 1.2123123e+07), le(cast(findpt.t1.a), 1.1112222111111112e+21) |
|   └─TableFullScan_5     | 1.00    | cop[tikv] | table:t1      | keep order:false, stats:pseudo                                                      |
+-------------------------+---------+-----------+---------------+-------------------------------------------------------------------------------------+
3 rows in set (0.00 sec)
```

**Brief description of run results**: From the above execution plan, the `Cast` operator is visible.

{{< copyable "sql" >}}

```sql
SELECT * FROM `t1` WHERE `a` BETWEEN '12123123' AND '1111222211111111200000';
+------------------------+
| a                      |
+------------------------+
| 1111222211111111222211 |
+------------------------+
1 row in set (0.01 sec)

```

**Brief description of run results**: The above execution gives an error result.
