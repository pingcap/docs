---
title: RENAME USER
summary: An overview of the usage of RENAME USER for the TiDB database.
---

# ユーザーの名前を変更 {#rename-user}

`RANAME USER`は、既存のユーザーの名前を変更するために使用されます。

## あらすじ {#synopsis}

```ebnf+diagram
RenameUserStmt ::=
    'RENAME' 'USER' UserToUser ( ',' UserToUser )*
UserToUser ::=
    Username 'TO' Username
Username ::=
    StringName ('@' StringName | singleAtIdentifier)? | 'CURRENT_USER' OptionalBraces
```

## 例 {#examples}

```sql
CREATE USER 'newuser' IDENTIFIED BY 'mypassword';
```

```sql
Query OK, 1 row affected (0.02 sec)
```

```sql
SHOW GRANTS FOR 'newuser';
```

```sql
+-------------------------------------+
| Grants for newuser@%                |
+-------------------------------------+
| GRANT USAGE ON *.* TO 'newuser'@'%' |
+-------------------------------------+
1 row in set (0.00 sec)
```

```sql
RENAME USER 'newuser' TO 'testuser';
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

```sql
SHOW GRANTS FOR 'testuser';
```

```sql
+--------------------------------------+
| Grants for testuser@%                |
+--------------------------------------+
| GRANT USAGE ON *.* TO 'testuser'@'%' |
+--------------------------------------+
1 row in set (0.00 sec)
```

```sql
SHOW GRANTS FOR 'newuser';
```

```sql
ERROR 1141 (42000): There is no such grant defined for user 'newuser' on host '%'
```

## MySQLの互換性 {#mysql-compatibility}

`RENAME USER`は MySQL と完全な互換性があることが期待されています。互換性の違いが見つかった場合は、 [バグを報告](https://docs.pingcap.com/tidb/stable/support)を行うことができます。

## こちらも参照 {#see-also}

-   [ユーザーを作成](/sql-statements/sql-statement-create-user.md)
-   [助成金を表示する](/sql-statements/sql-statement-show-grants.md)
-   [ユーザーを削除する](/sql-statements/sql-statement-drop-user.md)
