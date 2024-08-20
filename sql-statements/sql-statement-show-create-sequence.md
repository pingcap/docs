---
title: SHOW CREATE SEQUENCE
summary: An overview of the usage of SHOW CREATE SEQUENCE for the TiDB database.
---

# SHOW CREATE SEQUENCE

The `SHOW CREATE SEQUENCE` shows the detailed information of a sequence, which is similar to `SHOW CREATE TABLE`.

## Synopsis

```ebnf+diagram
ShowCreateSequenceStmt ::=
    "SHOW" "CREATE" "SEQUENCE" ( SchemaName "." )? TableName
```

## Examples

```sql
CREATE SEQUENCE seq;
```

```
Query OK, 0 rows affected (0.03 sec)
```

```sql
SHOW CREATE SEQUENCE seq;
```

```
+-------+----------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                               |
+-------+----------------------------------------------------------------------------------------------------------------------------+
| seq   | CREATE SEQUENCE `seq` start with 1 minvalue 1 maxvalue 9223372036854775806 increment by 1 cache 1000 nocycle ENGINE=InnoDB |
+-------+----------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL compatibility

This statement is a TiDB extension. The implementation is modeled on sequences available in MariaDB.

## See also

* [CREATE SEQUENCE](/sql-statements/sql-statement-create-sequence.md)
* [ALTER SEQUENCE](/sql-statements/sql-statement-alter-sequence.md)
* [DROP SEQUENCE](/sql-statements/sql-statement-drop-sequence.md)
