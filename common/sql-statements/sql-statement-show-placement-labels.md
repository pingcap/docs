---
title: SHOW PLACEMENT LABELS
summary: The usage of SHOW PLACEMENT LABELS in TiDB.
---

# SHOW PLACEMENT LABELS

`SHOW PLACEMENT LABELS` is used to summarize the labels and values that are available for Placement Rules.

## Synopsis

```ebnf+diagram
ShowStmt ::=
    "PLACEMENT" "LABELS"
```

## Examples

{{< copyable "sql" >}}

```sql
SHOW PLACEMENT LABELS;
```

```
+--------+----------------+
| Key    | Values         |
+--------+----------------+
| region | ["us-east-1"]  |
| zone   | ["us-east-1a"] |
+--------+----------------+
2 rows in set (0.00 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [Placement Rules in SQL](/placement-rules-in-sql.md)
* [SHOW PLACEMENT](/common/sql-statements/sql-statement-show-placement.md)
* [CREATE PLACEMENT POLICY](/common/sql-statements/sql-statement-create-placement-policy.md)