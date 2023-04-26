---
title: Privilege Management
summary: Learn how to manage the privilege.
---

# 権限管理 {#privilege-management}

TiDB は、 MySQL 5.7の権限管理システム (構文と権限タイプを含む) をサポートしています。 MySQL 8.0 の次の機能もサポートされています。

-   TiDB 3.0 以降の SQL ロール。
-   TiDB 5.1 以降の動的権限。

このドキュメントでは、権限関連の TiDB 操作、TiDB 操作に必要な権限、および権限システムの実装について紹介します。

## 特典関連の操作 {#privilege-related-operations}

### 権限の付与 {#grant-privileges}

`GRANT`ステートメントは、ユーザー アカウントに権限を付与します。

たとえば、次のステートメントを使用して、 `xxx`ユーザーに`test`データベースを読み取る権限を付与します。

```sql
GRANT SELECT ON test.* TO 'xxx'@'%';
```

次のステートメントを使用して、 `xxx`のユーザーにすべてのデータベースに対するすべての権限を付与します。

```sql
GRANT ALL PRIVILEGES ON *.* TO 'xxx'@'%';
```

デフォルトでは、指定されたユーザーが存在しない場合、 `GRANT`ステートメントはエラーを返します。この動作は、SQL モード`NO_AUTO_CREATE_USER`が指定されているかどうかによって異なります。

```sql
mysql> SET sql_mode=DEFAULT;
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT @@sql_mode;
+-------------------------------------------------------------------------------------------------------------------------------------------+
| @@sql_mode                                                                                                                                |
+-------------------------------------------------------------------------------------------------------------------------------------------+
| ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+-------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> SELECT * FROM mysql.user WHERE user='idontexist';
Empty set (0.00 sec)

mysql> GRANT ALL PRIVILEGES ON test.* TO 'idontexist';
ERROR 1105 (HY000): You are not allowed to create a user with GRANT

mysql> SELECT user,host,authentication_string FROM mysql.user WHERE user='idontexist';
Empty set (0.00 sec)
```

次の例では、SQL モード`NO_AUTO_CREATE_USER`が設定されていないため、空のパスワードでユーザー`idontexist`が自動的に作成されます。これはセキュリティ リスクがあるため**お勧めしません**。ユーザー名のスペルを間違えると、新しいユーザーが空のパスワードで作成されます。

```sql
mysql> SET @@sql_mode='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT @@sql_mode;
+-----------------------------------------------------------------------------------------------------------------------+
| @@sql_mode                                                                                                            |
+-----------------------------------------------------------------------------------------------------------------------+
| ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION |
+-----------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> SELECT * FROM mysql.user WHERE user='idontexist';
Empty set (0.00 sec)

mysql> GRANT ALL PRIVILEGES ON test.* TO 'idontexist';
Query OK, 1 row affected (0.05 sec)

mysql> SELECT user,host,authentication_string FROM mysql.user WHERE user='idontexist';
+------------+------+-----------------------+
| user       | host | authentication_string |
+------------+------+-----------------------+
| idontexist | %    |                       |
+------------+------+-----------------------+
1 row in set (0.01 sec)
```

あいまい一致 in `GRANT`を使用して、データベースに権限を付与できます。

```sql
mysql> GRANT ALL PRIVILEGES ON `te%`.* TO genius;
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT user,host,db FROM mysql.db WHERE user='genius';
+--------|------|-----+
| user   | host | db  |
+--------|------|-----+
| genius | %    | te% |
+--------|------|-----+
1 row in set (0.00 sec)
```

この例では、 `%` in `te%`のため、 `te`で始まるすべてのデータベースに権限が付与されます。

### 権限を取り消す {#revoke-privileges}

`REVOKE`ステートメントにより、システム管理者はユーザー アカウントから権限を取り消すことができます。

`REVOKE`ステートメントは`REVOKE`ステートメントに対応します。

```sql
REVOKE ALL PRIVILEGES ON `test`.* FROM 'genius'@'localhost';
```

> **ノート：**
>
> 権限を取り消すには、完全に一致する必要があります。一致する結果が見つからない場合、エラーが表示されます。

```sql
mysql> REVOKE ALL PRIVILEGES ON `te%`.* FROM 'genius'@'%';
ERROR 1141 (42000): There is no such grant defined for user 'genius' on host '%'
```

あいまい一致、エスケープ、文字列、および識別子について:

```sql
mysql> GRANT ALL PRIVILEGES ON `te\%`.* TO 'genius'@'localhost';
Query OK, 0 rows affected (0.00 sec)
```

この例では、完全一致を使用して`te%`という名前のデータベースを見つけます。 `%` `\`エスケープ文字を使用するため、 `%`はワイルドカードとは見なされないことに注意してください。

文字列は一重引用符 (&#39;&#39;) で囲み、識別子はバックティック (``) で囲みます。以下の違いを参照してください。

```sql
mysql> GRANT ALL PRIVILEGES ON 'test'.* TO 'genius'@'localhost';
ERROR 1064 (42000): You have an error in your SQL syntax; check the
manual that corresponds to your MySQL server version for the right
syntax to use near ''test'.* to 'genius'@'localhost'' at line 1

mysql> GRANT ALL PRIVILEGES ON `test`.* TO 'genius'@'localhost';
Query OK, 0 rows affected (0.00 sec)
```

テーブル名として特別なキーワードを使用する場合は、それらをバッククォート (``) で囲みます。例えば：

```sql
mysql> CREATE TABLE `select` (id int);
Query OK, 0 rows affected (0.27 sec)
```

### ユーザーに付与された権限を確認する {#check-privileges-granted-to-users}

`SHOW GRANTS`ステートメントを使用して、ユーザーに付与されている権限を確認できます。例えば：

```sql
SHOW GRANTS; -- show grants for the current user

+-------------------------------------------------------------+
| Grants for User                                             |
+-------------------------------------------------------------+
| GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION |
+-------------------------------------------------------------+
SHOW GRANTS FOR 'root'@'%'; -- show grants for a specific user
```

たとえば、ユーザー`rw_user@192.168.%`を作成し、そのユーザーに`test.write_table`テーブルに対する書き込み権限とグローバル読み取り権限を付与します。

```sql
CREATE USER `rw_user`@`192.168.%`;
GRANT SELECT ON *.* TO `rw_user`@`192.168.%`;
GRANT INSERT, UPDATE ON `test`.`write_table` TO `rw_user`@`192.168.%`;
```

`rw_user@192.168.%`人のユーザーに付与された権限を表示:

```sql
SHOW GRANTS FOR `rw_user`@`192.168.%`;

+------------------------------------------------------------------+
| Grants for rw_user@192.168.%                                     |
+------------------------------------------------------------------+
| GRANT Select ON *.* TO 'rw_user'@'192.168.%'                     |
| GRANT Insert,Update ON test.write_table TO 'rw_user'@'192.168.%' |
+------------------------------------------------------------------+
```

### 動的権限 {#dynamic-privileges}

v5.1 以降、TiDB の機能は、MySQL 8.0 から借用した機能である動的権限をサポートしています。動的権限は、特定の操作へのよりきめ細かいアクセスを実装することにより、 `SUPER`特権を置き換えることを目的としています。たとえば、動的権限を使用して、システム管理者は`BACKUP`つと`RESTORE`の操作しか実行できないユーザー アカウントを作成できます。

動的権限には次のものがあります。

-   `BACKUP_ADMIN`
-   `RESTORE_ADMIN`
-   `SYSTEM_USER`
-   `SYSTEM_VARIABLES_ADMIN`
-   `ROLE_ADMIN`
-   `CONNECTION_ADMIN`
-   `PLACEMENT_ADMIN`を指定すると、権限の所有者は配置ポリシーを作成、変更、および削除できます。
-   `DASHBOARD_CLIENT`特権所有者が TiDB ダッシュボードにログインできるようにします。
-   `RESTRICTED_TABLES_ADMIN`指定すると、権限の所有者は、SEM が有効な場合にシステム テーブルを表示できます。
-   `RESTRICTED_STATUS_ADMIN`指定すると、権限の所有者は、SEM が有効になっている場合に[`SHOW [GLOBAL|SESSION] STATUS`](/sql-statements/sql-statement-show-status.md)のすべてのステータス変数を表示できます。
-   `RESTRICTED_VARIABLES_ADMIN`指定すると、権限の所有者は、SEM が有効になっている場合にすべてのシステム変数を表示できます。
-   `RESTRICTED_USER_ADMIN`権限所有者が、SEM が有効になっているときに SUPER ユーザーによってアクセス権が取り消されることを禁止します。
-   `RESTRICTED_CONNECTION_ADMIN`は、特権所有者が`RESTRICTED_USER_ADMIN`人のユーザーの接続を切断できるようにします。この特権は、 `KILL`と`KILL TIDB`ステートメントに影響します。
-   `RESTRICTED_REPLICA_WRITER_ADMIN`指定すると、権限の所有者は、TiDB クラスターで読み取り専用モードが有効になっている場合に影響を受けることなく、書き込み操作または更新操作を実行できます。詳細については、 [`tidb_restricted_read_only`](/system-variables.md#tidb_restricted_read_only-new-in-v520)を参照してください。

動的権限の完全なセットを表示するには、 `SHOW PRIVILEGES`ステートメントを実行します。プラグインは新しい権限を追加できるため、割り当て可能な権限のリストは、TiDB のインストールによって異なる場合があります。

## <code>SUPER</code>特典 {#code-super-code-privilege}

-   `SUPER`特権により、ユーザーはほとんどすべての操作を実行できます。デフォルトでは、この権限は`root`ユーザーのみに付与されます。この権限を他のユーザーに付与する場合は注意してください。
-   `SUPER`特権は[MySQL 8.0 で非推奨](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#dynamic-privileges-migration-from-super)と見なされ、よりきめ細かいアクセス制御を提供するために[動的権限](#dynamic-privileges)に置き換えることができます。

## TiDB 操作に必要な権限 {#privileges-required-for-tidb-operations}

`INFORMATION_SCHEMA.USER_PRIVILEGES`テーブルで TiDB ユーザーの権限を確認できます。例えば：

```sql
mysql> SELECT * FROM INFORMATION_SCHEMA.USER_PRIVILEGES WHERE grantee = "'root'@'%'";
+------------+---------------+-------------------------+--------------+
| GRANTEE    | TABLE_CATALOG | PRIVILEGE_TYPE          | IS_GRANTABLE |
+------------+---------------+-------------------------+--------------+
| 'root'@'%' | def           | Select                  | YES          |
| 'root'@'%' | def           | Insert                  | YES          |
| 'root'@'%' | def           | Update                  | YES          |
| 'root'@'%' | def           | Delete                  | YES          |
| 'root'@'%' | def           | Create                  | YES          |
| 'root'@'%' | def           | Drop                    | YES          |
| 'root'@'%' | def           | Process                 | YES          |
| 'root'@'%' | def           | References              | YES          |
| 'root'@'%' | def           | Alter                   | YES          |
| 'root'@'%' | def           | Show Databases          | YES          |
| 'root'@'%' | def           | Super                   | YES          |
| 'root'@'%' | def           | Execute                 | YES          |
| 'root'@'%' | def           | Index                   | YES          |
| 'root'@'%' | def           | Create User             | YES          |
| 'root'@'%' | def           | Create Tablespace       | YES          |
| 'root'@'%' | def           | Trigger                 | YES          |
| 'root'@'%' | def           | Create View             | YES          |
| 'root'@'%' | def           | Show View               | YES          |
| 'root'@'%' | def           | Create Role             | YES          |
| 'root'@'%' | def           | Drop Role               | YES          |
| 'root'@'%' | def           | CREATE TEMPORARY TABLES | YES          |
| 'root'@'%' | def           | LOCK TABLES             | YES          |
| 'root'@'%' | def           | CREATE ROUTINE          | YES          |
| 'root'@'%' | def           | ALTER ROUTINE           | YES          |
| 'root'@'%' | def           | EVENT                   | YES          |
| 'root'@'%' | def           | SHUTDOWN                | YES          |
| 'root'@'%' | def           | RELOAD                  | YES          |
| 'root'@'%' | def           | FILE                    | YES          |
| 'root'@'%' | def           | CONFIG                  | YES          |
| 'root'@'%' | def           | REPLICATION CLIENT      | YES          |
| 'root'@'%' | def           | REPLICATION SLAVE       | YES          |
+------------+---------------+-------------------------+--------------+
31 rows in set (0.00 sec)
```

### 変更する {#alter}

-   すべての`ALTER`ステートメントについて、ユーザーは対応するテーブルに対する`ALTER`特権を持っている必要があります。
-   `ALTER...DROP`と`ALTER...RENAME TO`以外のステートメントの場合、ユーザーは対応するテーブルに対する`INSERT`と`CREATE`権限を持っている必要があります。
-   `ALTER...DROP`ステートメントの場合、ユーザーは対応するテーブルに対する`DROP`特権を持っている必要があります。
-   `ALTER...RENAME TO`ステートメントの場合、ユーザーは、名前変更前のテーブルに対する`DROP`権限と、名前変更後のテーブルに対する`CREATE`および`INSERT`権限を持っている必要があります。

> **ノート：**
>
> MySQL 5.7 のドキュメントでは、ユーザーがテーブルに対して`ALTER`操作を実行するには、 `INSERT`と`CREATE`権限が必要です。しかし実際には、 MySQL 5.7.25 の場合、この場合は`ALTER`特権のみが必要です。現在、TiDB の`ALTER`権限は、MySQL の実際の動作と一致しています。

### バックアップ {#backup}

`SUPER`または`BACKUP_ADMIN`特権が必要です。

### データベースの作成 {#create-database}

データベースに対する`CREATE`特権が必要です。

### インデックスを作成 {#create-index}

テーブルに対する`INDEX`特権が必要です。

### テーブルを作成 {#create-table}

テーブルに対する`CREATE`特権が必要です。

`CREATE TABLE...LIKE...`ステートメントを実行するには、テーブルに対する`SELECT`特権が必要です。

### ビューを作成 {#create-view}

`CREATE VIEW`特権が必要です。

> **ノート：**
>
> 現在のユーザーがビューを作成したユーザーでない場合は、 `CREATE VIEW`と`SUPER`の両方の権限が必要です。

### データベースをドロップ {#drop-database}

テーブルに対する`DROP`特権が必要です。

### ドロップインデックス {#drop-index}

テーブルに対する`INDEX`特権が必要です。

### ドロップテーブル {#drop-tables}

テーブルに対する`DROP`特権が必要です。

### データを読み込む {#load-data}

テーブルに対する`INSERT`特権が必要です。 `REPLACE INTO`使用する場合は、 `DELETE`特権も必要です。

### テーブルの切り捨て {#truncate-table}

テーブルに対する`DROP`特権が必要です。

### テーブル名の変更 {#rename-table}

名前を変更する前にテーブルに対して`ALTER`および`DROP`権限が必要であり、名前を変更した後にテーブルに対して`CREATE`および`INSERT`権限が必要です。

### テーブルを分析 {#analyze-table}

テーブルに対する`INSERT`および`SELECT`権限が必要です。

### 見せる {#show}

`SHOW CREATE TABLE`には、テーブルに対する単一の特権が必要です。

`SHOW CREATE VIEW`には`SHOW VIEW`特権が必要です。

`SHOW GRANTS`は、 `mysql`データベースに対する`SELECT`特権が必要です。ターゲット ユーザーが現在のユーザーの場合、 `SHOW GRANTS`は権限は必要ありません。

`SHOW PROCESSLIST`他のユーザーに属する接続を表示するには`SUPER`が必要です。

### ロール/ユーザーの作成 {#create-role-user}

`CREATE ROLE`には`CREATE ROLE`特権が必要です。

`CREATE USER`には`CREATE USER`特権が必要です。

### ロール/ユーザーのドロップ {#drop-role-user}

`DROP ROLE`には`DROP ROLE`特権が必要です。

`DROP USER`には`CREATE USER`特権が必要です。

### ユーザーの変更 {#alter-user}

`CREATE USER`特権が必要です。

### 許す {#grant}

`GRANT`によって付与される権限を持つ`GRANT`権限が必要です。

ユーザーを暗黙的に作成するには、追加の`CREATE USER`特権が必要です。

`GRANT ROLE`は`SUPER`または`ROLE_ADMIN`特権が必要です。

### 取り消す {#revoke}

`GRANT`特権と、 `REVOKE`ステートメントの対象となる権限が必要です。

`REVOKE ROLE`は`SUPER`または`ROLE_ADMIN`特権が必要です。

### グローバル設定 {#set-global}

グローバル変数を設定するには、 `SUPER`または`SYSTEM_VARIABLES_ADMIN`特権が必要です。

### 管理者 {#admin}

`SUPER`特権が必要です。

### デフォルトの役割を設定 {#set-default-role}

`SUPER`特権が必要です。

### 殺す {#kill}

他のユーザー セッションを強制終了するには、 `SUPER`または`CONNECTION_ADMIN`特権が必要です。

## 特典システムの実装 {#implementation-of-the-privilege-system}

### 特典テーブル {#privilege-table}

次のシステム テーブルは、権限に関連するすべてのデータが格納されているため、特別です。

-   `mysql.user` (ユーザー アカウント、グローバル権限)
-   `mysql.db` (データベースレベルの権限)
-   `mysql.tables_priv` (テーブルレベルの権限)
-   `mysql.columns_priv` (列レベルの特権。現在サポートされていません)

これらのテーブルには、データの有効範囲と特権情報が含まれています。たとえば、 `mysql.user`テーブルでは次のようになります。

```sql
mysql> SELECT User,Host,Select_priv,Insert_priv FROM mysql.user LIMIT 1;
+------|------|-------------|-------------+
| User | Host | Select_priv | Insert_priv |
+------|------|-------------|-------------+
| root | %    | Y           | Y           |
+------|------|-------------|-------------+
1 row in set (0.00 sec)
```

このレコードで、 `Host`と`User` 、 `root`ユーザーが任意のホスト ( `%` ) から送信した接続要求を受け入れることができると判断します。 `Select_priv`および`Insert_priv`ユーザーがグローバル`Select`および`Insert`権限を持っていることを意味します。 `mysql.user`テーブルの有効範囲はグローバルです。

`mysql.db`分の`Host`と`User` 、ユーザーがアクセスできるデータベースを決定します。有効範囲はデータベースです。

> **ノート：**
>
> `GRANT` 、 `CREATE USER` 、 `DROP USER`などの指定された構文を使用してのみ権限テーブルを更新することをお勧めします。基礎となる特権テーブルを直接編集しても、特権キャッシュが自動的に更新されないため、 `FLUSH PRIVILEGES`が実行されるまで予期しない動作が発生します。

### 接続確認 {#connection-verification}

クライアントが接続要求を送信すると、TiDBサーバーはログイン操作を検証します。 TiDBサーバーは最初に`mysql.user`テーブルをチェックします。 `User`と`Host`のレコードが接続要求と一致する場合、TiDBサーバーは`authentication_string`を検証します。

ユーザー ID は、2 つの情報に基づいています`Host`は接続を開始するホスト、 `User`はユーザー名です。ユーザー名が空でない場合は、指定されたユーザーと完全に一致する必要があります。

`User` + `Host` 、 `user`テーブルの複数の行に一致する場合があります。このシナリオに対処するために、 `user`テーブルの行が並べ替えられます。クライアントが接続すると、テーブルの行が 1 つずつチェックされます。最初に一致した行が検証に使用されます。並べ替えると、ホストがユーザーよりも前にランク付けされます。

### 確認をリクエストする {#request-verification}

接続が成功すると、リクエスト検証プロセスで、操作に権限があるかどうかがチェックされます。

データベース関連の要求 ( `INSERT` 、 `UPDATE` ) の場合、要求検証プロセスは最初に`mysql.user`テーブルでユーザーのグローバル権限をチェックします。権限が付与されている場合は、直接アクセスできます。そうでない場合は、 `mysql.db`テーブルを確認してください。

`user`テーブルには、デフォルトのデータベースに関係なくグローバル権限があります。たとえば、 `user`の`DELETE`特権は、任意の行、テーブル、またはデータベースに適用できます。

`db`テーブルでは、空のユーザーが匿名ユーザー名と一致します。 `User`列目にワイルドカードは使用できません。 `Host`と`Db`列の値には、パターン マッチングを使用できる`%`と`_`を使用できます。

`user`と`db`テーブルのデータも、メモリにロードされるときに並べ替えられます。

`tables_priv`と`columns_priv`での`%`の使用は似ていますが、 `Db` 、 `Table_name` 、および`Column_name`の列の値に`%`を含めることはできません。ロード時のソートも同様です。

### 効果時間 {#time-of-effect}

TiDB が起動すると、いくつかの権限チェック テーブルがメモリに読み込まれ、キャッシュされたデータを使用して権限が検証されます。 `GRANT` 、 `REVOKE` 、 `CREATE USER` 、 `DROP USER`などの権限管理ステートメントを実行すると、すぐに有効になります。

`mysql.user`などのテーブルを`INSERT` 、 `DELETE` 、 `UPDATE`などのステートメントで手動で編集しても、すぐには反映されません。この動作は MySQL と互換性があり、特権キャッシュは次のステートメントで更新できます。

```sql
FLUSH PRIVILEGES;
```
