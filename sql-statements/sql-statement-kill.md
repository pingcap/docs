---
title: KILL
summary: An overview of the usage of KILL for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-kill/','/docs/dev/reference/sql/statements/kill/']
---

# KILL

The statement `KILL TIDB` is used to terminate a connection in any TiDB instance in the current TiDB cluster.

## Synopsis

```ebnf+diagram
KillStmt ::= 'KILL' 'TIDB'? ( 'CONNECTION' | 'QUERY' )? CONNECTION_ID
```

## Examples

The following example shows how to query all active queries in the current cluster and terminate one of the connections.

{{< copyable "sql" >}}

```sql
SELECT ID, USER, INSTANCE, INFO FROM INFORMATION_SCHEMA.CLUSTER_PROCESSLIST;
```

```
+---------------------+------+-----------------+-----------------------------------------------------------------------------+
| ID                  | USER | INSTANCE        | INFO                                                                        |
+---------------------+------+-----------------+-----------------------------------------------------------------------------+
| 8306449708033769879 | root | 127.0.0.1:10082 | select sleep(30), 'foo'                                                     |
| 5857102839209263511 | root | 127.0.0.1:10080 | select sleep(50)                                                            |
| 5857102839209263513 | root | 127.0.0.1:10080 | SELECT ID, USER, INSTANCE, INFO FROM INFORMATION_SCHEMA.CLUSTER_PROCESSLIST |
+---------------------+------+-----------------+-----------------------------------------------------------------------------+
```

{{< copyable "sql" >}}

```sql
KILL 5857102839209263511;
```

```
Query OK, 0 rows affected (0.00 sec)
```

## MySQL compatibility

* By design, `KILL` is not compatible with MySQL by default. This helps prevent against a case of a connection being terminated on the wrong TiDB server, because it is common to place multiple TiDB servers behind a load balancer.
* DO NOT set [`compatible-kill-query = true`](/tidb-configuration-file.md#compatible-kill-query) in your configuration file UNLESS you are certain that clients will be always connected to the same TiDB node. This is because pressing <kbd>ctrl</kbd>+<kbd>c</kbd> in the default MySQL client opens a new connection in which `KILL` is executed. If there are proxies in between, the new connection might be routed to a different TiDB node, which possibly kills a different session.
* The `KILL TIDB` statement is a TiDB extension. The feature of this statement is similar to the MySQL `KILL [CONNECTION|QUERY]` command and the MySQL command-line <kbd>ctrl</kbd>+<kbd>c</kbd> feature. It is safe to use `KILL TIDB` on the same TiDB node.

## See also

* [SHOW \[FULL\] PROCESSLIST](/sql-statements/sql-statement-show-processlist.md)
* [CLUSTER_PROCESSLIST](/information-schema/information-schema-processlist.md#cluster_processlist)
