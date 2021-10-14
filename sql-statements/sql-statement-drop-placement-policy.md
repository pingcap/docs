---
title: DROP PLACEMENT POLICY
summary: The usage of ALTER PLACEMENT POLICY in TiDB.
---

# DROP PLACEMENT POLICY

`DROP PLACEMENT POLICY` 

## Synopsis

```ebnf+diagram
DropPolicyStmt ::=
    "DROP" "PLACEMENT" "POLICY" IfExists PolicyName

PolicyName ::=
	Identifier
```

## Examples

{{< copyable "sql" >}}

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
ALTER PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1,us-west-2" FOLLOWERS=4;
```

```
Query OK, 0 rows affected (0.08 sec)

Query OK, 0 rows affected (0.10 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [Placement Rules](/placement-rules.md)
* [SHOW PLACEMENT](/sql-statements/sql-statement-show-placement.md)
* [CREATE PLACEMENT POLICY](/sql-statements/sql-statement-create-placement-policy.md)
* [ALTER PLACEMENT POLICY](/sql-statements/sql-statement-alter-placement-policy.md)