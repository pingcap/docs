---
title: ADMIN [SET|SHOW|UNSET] BDR ROLE
summary: TiDB データベースの ADMIN [SET|SHOW|UNSET] BDR ROLE の使用法の概要。
---

# 管理者 [設定|表示|設定解除] BDR ロール {#admin-set-show-unset-bdr-role}

-   クラスターのBDRロールを設定するには、 `ADMIN SET BDR ROLE`使用します。現在、TiDBクラスターには`PRIMARY`と`SECONDARY` BDRロールを設定できます。BDRロールの詳細については、 [TiCDC 双方向レプリケーションにおける DDL 同期](/ticdc/ticdc-bidirectional-replication.md#ddl-replication)参照してください。
-   クラスターの BDR ロールを表示するには、 `ADMIN SHOW BDR ROLE`使用します。
-   クラスターの BDR ロールを設定解除するには、 `ADMIN UNSET BDR ROLE`使用します。

## 概要 {#synopsis}

```ebnf+diagram
AdminShowBDRRoleStmt ::=
    'ADMIN' 'SHOW' 'BDR' 'ROLE'

AdminSetBDRRoleStmt ::=
    'ADMIN' 'SET' 'BDR' 'ROLE' ('PRIMARY' | 'SECONDARY')

AdminUnsetBDRRoleStmt ::=
    'ADMIN' 'UNSET' 'BDR' 'ROLE'
```

## 例 {#examples}

デフォルトでは、TiDB クラスターには BDR ロールがありません。クラスターの BDR ロールを表示するには、次のコマンドを実行します。

```sql
ADMIN SHOW BDR ROLE;
```

```sql
+------------+
| BDR_ROLE   |
+------------+
|            |
+------------+
1 row in set (0.01 sec)
```

次のコマンドを実行して、BDR ロールを`PRIMARY`に設定します。

```sql
ADMIN SET BDR ROLE PRIMARY;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

```sql
ADMIN SHOW BDR ROLE;
+----------+
| BDR_ROLE |
+----------+
| primary  |
+----------+
1 row in set (0.00 sec)
```

クラスターの BDR ロールを設定解除するには、次のコマンドを実行します。

```sql
ADMIN UNSET BDR ROLE;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

```sql
ADMIN SHOW BDR ROLE;
+----------+
| BDR_ROLE |
+----------+
|          |
+----------+
1 row in set (0.01 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。
