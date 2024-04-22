---
title: Privilege Management
summary: TiDBはMySQL 5.7の権限管理システムをサポートし、MySQL 8.0の機能もサポートしています。権限関連の操作には、GRANTステートメントを使用して権限を付与し、REVOKEステートメントを使用して権限を取り消します。動的権限はTiDB機能の一部であり、特定の操作に対するアクセスを制御します。権限はmysql.userおよびmysql.dbテーブルで管理され、FLUSH PRIVILEGESステートメントで更新できます。
---

# 権限管理 {#privilege-management}

TiDB は、構文や権限タイプを含むMySQL 5.7の権限管理システムをサポートしています。 MySQL 8.0 の次の機能もサポートされています。

-   TiDB 3.0 以降の SQL ロール。
-   TiDB 5.1 以降の動的権限。

このドキュメントでは、権限関連の TiDB 操作、TiDB 操作に必要な権限、および権限システムの実装について紹介します。

## 権限関連の操作 {#privilege-related-operations}

### 権限を付与する {#grant-privileges}

`GRANT`ステートメントは、ユーザー アカウントに権限を付与します。

たとえば、次のステートメントを使用して、 `xxx`人のユーザーに`test`データベースを読み取る権限を付与します。

```sql
GRANT SELECT ON test.* TO 'xxx'@'%';
```

次のステートメントを使用して、 `xxx`のユーザーにすべてのデータベースに対するすべての権限を付与します。

```sql
GRANT ALL PRIVILEGES ON *.* TO 'xxx'@'%';
```

デフォルトでは、指定したユーザーが存在しない場合、 `GRANT`ステートメントはエラーを返します。この動作は、SQL モード`NO_AUTO_CREATE_USER`が指定されているかどうかによって異なります。

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

次の例では、SQL モード`NO_AUTO_CREATE_USER`が設定されていないため、ユーザー`idontexist`は空のパスワードで自動的に作成されます。これはセキュリティ上のリスクがあるため**お勧めできません**。ユーザー名のスペルを間違えると、空のパスワードで新しいユーザーが作成されます。

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

`GRANT`ではあいまい一致を使用して、データベースに権限を付与できます。

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

> **注記：**
>
> 権限を取り消すには、完全に一致する必要があります。一致する結果が見つからない場合は、エラーが表示されます。

```sql
mysql> REVOKE ALL PRIVILEGES ON `te%`.* FROM 'genius'@'%';
ERROR 1141 (42000): There is no such grant defined for user 'genius' on host '%'
```

あいまい一致、エスケープ、文字列、識別子について:

```sql
mysql> GRANT ALL PRIVILEGES ON `te\%`.* TO 'genius'@'localhost';
Query OK, 0 rows affected (0.00 sec)
```

この例では、完全一致を使用して`te%`という名前のデータベースを検索します。 `%` `\`エスケープ文字が使用されているため、 `%`はワイルドカードとはみなされないことに注意してください。

文字列は一重引用符 (&#39;&#39;) で囲まれ、識別子はバッククォート (``) で囲まれます。以下の違いを参照してください。

```sql
mysql> GRANT ALL PRIVILEGES ON 'test'.* TO 'genius'@'localhost';
ERROR 1064 (42000): You have an error in your SQL syntax; check the
manual that corresponds to your MySQL server version for the right
syntax to use near ''test'.* to 'genius'@'localhost'' at line 1

mysql> GRANT ALL PRIVILEGES ON `test`.* TO 'genius'@'localhost';
Query OK, 0 rows affected (0.00 sec)
```

特別なキーワードをテーブル名として使用する場合は、キーワードをバッククォート (``) で囲みます。例えば：

```sql
mysql> CREATE TABLE `select` (id int);
Query OK, 0 rows affected (0.27 sec)
```

### ユーザーに付与された権限を確認する {#check-privileges-granted-to-users}

`SHOW GRANTS`ステートメントを使用すると、ユーザーに付与されている権限を確認できます。例えば：

```sql
SHOW GRANTS; -- show grants for the current user

+-------------------------------------------------------------+
| Grants for User                                             |
+-------------------------------------------------------------+
| GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION |
+-------------------------------------------------------------+
SHOW GRANTS FOR 'root'@'%'; -- show grants for a specific user
```

たとえば、ユーザー`rw_user@192.168.%`を作成し、そのユーザーにテーブル`test.write_table`に対する書き込み権限とグローバル読み取り権限を付与します。

```sql
CREATE USER `rw_user`@`192.168.%`;
GRANT SELECT ON *.* TO `rw_user`@`192.168.%`;
GRANT INSERT, UPDATE ON `test`.`write_table` TO `rw_user`@`192.168.%`;
```

`rw_user@192.168.%`人のユーザーに付与された権限を表示します。

```sql
SHOW GRANTS FOR `rw_user`@`192.168.%`;

+------------------------------------------------------------------+
| Grants for rw_user@192.168.%                                     |
+------------------------------------------------------------------+
| GRANT Select ON *.* TO 'rw_user'@'192.168.%'                     |
| GRANT Insert,Update ON test.write_table TO 'rw_user'@'192.168.%' |
+------------------------------------------------------------------+
```

### 動的な権限 {#dynamic-privileges}

v5.1 以降、TiDB 機能は、MySQL 8.0 から借用した機能である動的権限をサポートしています。動的権限は、特定の操作に対するよりきめ細かいアクセスを実装することにより、 `SUPER`権限を置き換えることを目的としています。たとえば、システム管理者は、動的権限を使用して、 `BACKUP`と`RESTORE`操作のみを実行できるユーザー アカウントを作成できます。

動的権限には次のものが含まれます。

-   `BACKUP_ADMIN`
-   `RESTORE_ADMIN`
-   `SYSTEM_USER`
-   `SYSTEM_VARIABLES_ADMIN`
-   `ROLE_ADMIN`
-   `CONNECTION_ADMIN`
-   `PLACEMENT_ADMIN`指定すると、権限所有者は配置ポリシーを作成、変更、削除できます。
-   `DASHBOARD_CLIENT`では、特権所有者が TiDB ダッシュボードにログインできるようになります。
-   `RESTRICTED_TABLES_ADMIN`指定すると、SEM が有効な場合、権限所有者はシステム テーブルを表示できます。
-   `RESTRICTED_STATUS_ADMIN`指定すると、SEM が有効な場合、特権所有者は[`SHOW [GLOBAL|SESSION] STATUS`](/sql-statements/sql-statement-show-status.md)のすべてのステータス変数を表示できます。
-   `RESTRICTED_VARIABLES_ADMIN`指定すると、SEM が有効な場合、権限所有者はすべてのシステム変数を表示できます。
-   `RESTRICTED_USER_ADMIN` SEM が有効な場合、特権所有者が SUPER ユーザーによってアクセスを取り消されることを禁止します。
-   `RESTRICTED_CONNECTION_ADMIN`指定すると、特権所有者は`RESTRICTED_USER_ADMIN`人のユーザーの接続を強制終了できます。この権限はステートメント`KILL`とステートメント`KILL TIDB`に影響します。
-   `RESTRICTED_REPLICA_WRITER_ADMIN` TiDB クラスターで読み取り専用モードが有効になっている場合に、特権所有者は影響を受けることなく書き込みまたは更新操作を実行できます。詳細は[`tidb_restricted_read_only`](/system-variables.md#tidb_restricted_read_only-new-in-v520)を参照してください。

動的権限の完全なセットを表示するには、 `SHOW PRIVILEGES`ステートメントを実行します。プラグインは新しい権限を追加できるため、割り当て可能な権限のリストは TiDB インストールによって異なる場合があります。

## <code>SUPER</code>特典 {#code-super-code-privilege}

-   `SUPER`権限により、ユーザーはほぼすべての操作を実行できます。デフォルトでは、 `root`ユーザーのみにこの権限が付与されます。この権限を他のユーザーに付与する場合は注意してください。
-   `SUPER`権限は[MySQL 8.0 では非推奨になりました](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#dynamic-privileges-migration-from-super)とみなされ、よりきめ細かいアクセス制御を提供するために[動的権限](#dynamic-privileges)に置き換えることができます。

## TiDB 操作に必要な権限 {#privileges-required-for-tidb-operations}

TiDB ユーザーの権限は`INFORMATION_SCHEMA.USER_PRIVILEGES`表で確認できます。例えば：

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

### 変更 {#alter}

-   すべての`ALTER`ステートメントに対して、ユーザーは対応するテーブルに対する`ALTER`権限を持っている必要があります。
-   `ALTER...DROP`と`ALTER...RENAME TO`を除くステートメントの場合、ユーザーは対応するテーブルに対する`INSERT`と`CREATE`権限を持っている必要があります。
-   `ALTER...DROP`ステートメントの場合、ユーザーは対応するテーブルに対する`DROP`権限を持っている必要があります。
-   `ALTER...RENAME TO`ステートメントの場合、ユーザーは名前変更前にテーブルに対する`DROP`権限を持ち、名前変更後のテーブルに対して`CREATE`および`INSERT`権限を持っている必要があります。

> **注記：**
>
> MySQL 5.7 のドキュメントでは、ユーザーがテーブルに対して`ALTER`操作を実行するには`INSERT`と`CREATE`権限が必要です。しかし実際には、 MySQL 5.7.25 では、この場合に必要なのは`ALTER`権限のみです。現在、TiDB の`ALTER`権限は、MySQL の実際の動作と一致しています。

### バックアップ {#backup}

`SUPER`または`BACKUP_ADMIN`権限が必要です。

### インポートジョブのキャンセル {#cancel-import-job}

他のユーザーが作成したジョブをキャンセルするには`SUPER`権限が必要です。それ以外の場合、現在のユーザーが作成したジョブのみをキャンセルできます。

### データベースの作成 {#create-database}

データベースに対する`CREATE`権限が必要です。

### インデックスの作成 {#create-index}

テーブルに対する`INDEX`権限が必要です。

### テーブルの作成 {#create-table}

テーブルに対する`CREATE`権限が必要です。

`CREATE TABLE...LIKE...`ステートメントを実行するには、テーブルに対する`SELECT`権限が必要です。

### ビューの作成 {#create-view}

`CREATE VIEW`権限が必要です。

> **注記：**
>
> 現在のユーザーがビューを作成するユーザーではない場合は、 `CREATE VIEW`と`SUPER`の両方の権限が必要です。

### データベースを削除 {#drop-database}

テーブルに対する`DROP`権限が必要です。

### ドロップインデックス {#drop-index}

テーブルに対する`INDEX`権限が必要です。

### ドロップテーブル {#drop-tables}

テーブルに対する`DROP`権限が必要です。

### にインポート {#import-into}

ターゲットテーブルに対する`SELECT` 、 `UPDATE` 、 `INSERT` 、 `DELETE` 、および`ALTER`の権限が必要です。 TiDB にローカルに保存されているファイルをインポートするには、 `FILE`権限も必要です。

### データを読み込む {#load-data}

テーブルに対する`INSERT`権限が必要です。 `REPLACE INTO`使用する場合は、 `DELETE`権限も必要です。

### テーブルの切り捨て {#truncate-table}

テーブルに対する`DROP`権限が必要です。

### テーブルの名前を変更 {#rename-table}

名前変更前のテーブルには`ALTER`および`DROP`権限が必要で、名前変更後のテーブルには`CREATE`および`INSERT`権限が必要です。

### 分析テーブル {#analyze-table}

テーブルに対する`INSERT`および`SELECT`権限が必要です。

### ロック統計 {#lock-stats}

テーブルに対する`INSERT`および`SELECT`権限が必要です。

### ステータスのロックを解除する {#unlock-stats}

テーブルに対する`INSERT`および`SELECT`権限が必要です。

### 見せる {#show}

`SHOW CREATE TABLE`は、テーブルに対する任意の 1 つの権限が必要です。

`SHOW CREATE VIEW`は`SHOW VIEW`権限が必要です。

`SHOW GRANTS`は、 `mysql`データベースに対する`SELECT`権限が必要です。対象ユーザーが現在のユーザーの場合、 `SHOW GRANTS`は特権は必要ありません。

`SHOW PROCESSLIST`他のユーザーに属する接続を表示するには`SUPER`権限が必要です。

`SHOW IMPORT JOB`他のユーザーに属する接続を表示するには`SUPER`権限が必要です。それ以外の場合は、現在のユーザーが作成したジョブのみが表示されます。

`SHOW STATS_LOCKED`は、 `mysql.stats_table_locked`テーブルに対する`SELECT`特権が必要です。

### ロール/ユーザーの作成 {#create-role-user}

`CREATE ROLE`は`CREATE ROLE`権限が必要です。

`CREATE USER`は`CREATE USER`権限が必要です。

### ロール/ユーザーを削除 {#drop-role-user}

`DROP ROLE`は`DROP ROLE`権限が必要です。

`DROP USER`は`CREATE USER`権限が必要です。

### ユーザーの変更 {#alter-user}

`CREATE USER`権限が必要です。

### 付与 {#grant}

`GRANT`によって付与される権限とともに`GRANT`権限が必要です。

ユーザーを暗黙的に作成するには、追加の`CREATE USER`権限が必要です。

`GRANT ROLE`は`SUPER`または`ROLE_ADMIN`特権が必要です。

### 取り消す {#revoke}

`GRANT`権限と`REVOKE`ステートメントの対象となる権限が必要です。

`REVOKE ROLE`は`SUPER`または`ROLE_ADMIN`特権が必要です。

### グローバルに設定 {#set-global}

グローバル変数を設定するには`SUPER`または`SYSTEM_VARIABLES_ADMIN`権限が必要です。

### 管理者 {#admin}

`SUPER`権限が必要です。

### デフォルトの役割を設定 {#set-default-role}

`SUPER`権限が必要です。

### 殺す {#kill}

他のユーザーセッションを強制終了するには、 `SUPER`または`CONNECTION_ADMIN`権限が必要です。

### リソースグループの作成 {#create-resource-group}

`SUPER`または`RESOURCE_GROUP_ADMIN`権限が必要です。

### リソースグループの変更 {#alter-resource-group}

`SUPER`または`RESOURCE_GROUP_ADMIN`権限が必要です。

### リソースグループを削除 {#drop-resource-group}

`SUPER`または`RESOURCE_GROUP_ADMIN`権限が必要です。

### リソースの調整 {#calibrate-resource}

`SUPER`または`RESOURCE_GROUP_ADMIN`権限が必要です。

## 特権制度の導入 {#implementation-of-the-privilege-system}

### 特権テーブル {#privilege-table}

次のシステム テーブルは、すべての権限関連データが格納されるため、特別です。

-   `mysql.user` (ユーザーアカウント、グローバル権限)
-   `mysql.db` (データベースレベルの権限)
-   `mysql.tables_priv` (テーブルレベルの権限)
-   `mysql.columns_priv` (列レベルの権限。現在サポートされていません)

これらのテーブルには、データの有効範囲と権限情報が含まれています。たとえば、 `mysql.user`テーブルでは次のようになります。

```sql
mysql> SELECT User,Host,Select_priv,Insert_priv FROM mysql.user LIMIT 1;
+------|------|-------------|-------------+
| User | Host | Select_priv | Insert_priv |
+------|------|-------------|-------------+
| root | %    | Y           | Y           |
+------|------|-------------|-------------+
1 row in set (0.00 sec)
```

このレコードでは、 `Host`と`User`により、 `root`ユーザが任意のホスト（ `%` ）から送信した接続要求を受け付け可能であることが判断される。 `Select_priv`と`Insert_priv` 、ユーザーがグローバル`Select`と`Insert`権限を持っていることを意味します。表`mysql.user`の有効範囲はグローバルです。

`mysql.db`の`Host`と`User`によって、ユーザーがアクセスできるデータベースが決まります。有効範囲はデータベースです。

> **注記：**
>
> 特権テーブルは、 `GRANT` 、 `CREATE USER` 、 `DROP USER`などの指定された構文を使用してのみ更新することをお勧めします。基礎となる権限テーブルを直接編集しても、権限キャッシュは自動的に更新されないため、 `FLUSH PRIVILEGES`が実行されるまで予測できない動作が発生します。

### 接続の検証 {#connection-verification}

クライアントが接続リクエストを送信すると、TiDBサーバーはログイン操作を検証します。 TiDBサーバーは最初に`mysql.user`テーブルをチェックします。レコード`User`と`Host`接続リクエストと一致する場合、TiDBサーバーはレコード`authentication_string`を検証します。

ユーザー ID は 2 つの情報に基づいています。1 `Host`接続を開始するホスト、 `User`はユーザー名です。ユーザー名が空でない場合は、ユーザー名が完全に一致する必要があります。

`User` + `Host` `user`テーブルの複数の行に一致する可能性があります。このシナリオに対処するために、 `user`のテーブルの行が並べ替えられます。クライアントが接続すると、テーブルの行が 1 つずつチェックされます。最初に一致した行が検証に使用されます。並べ替える場合、ホストはユーザーよりも優先されます。

### 検証のリクエスト {#request-verification}

接続が成功すると、リクエスト検証プロセスによって、操作に権限があるかどうかがチェックされます。

データベース関連のリクエスト ( `INSERT` 、 `UPDATE` ) の場合、リクエスト検証プロセスは最初にテーブル`mysql.user`内のユーザーのグローバル権限をチェックします。権限が付与されている場合は、直接アクセスできます。そうでない場合は、 `mysql.db`表を確認してください。

`user`テーブルには、デフォルトのデータベースに関係なくグローバル権限があります。たとえば、 `user`の`DELETE`権限は、任意の行、テーブル、またはデータベースに適用できます。

`db`の表では、空のユーザーが匿名ユーザー名と一致します。 `User`列にはワイルドカードを使用できません。 `Host`と`Db`列の値には、パターン マッチングを使用できる`%`と`_`を使用できます。

テーブル`user`とテーブル`db`のデータも、メモリにロードされるときにソートされます。

`tables_priv`と`columns_priv`での`%`の使用は似ていますが、 `Db` 、 `Table_name` 、および`Column_name`の列値に`%`を含めることはできません。ロード時のソートも同様です。

### 効果時間 {#time-of-effect}

TiDB が起動すると、いくつかの権限チェック テーブルがメモリにロードされ、キャッシュされたデータを使用して権限が検証されます。 `GRANT` 、 `REVOKE` 、 `CREATE USER` 、 `DROP USER`などの権限管理ステートメントを実行すると、すぐに有効になります。

`mysql.user`などのテーブルを`INSERT` 、 `DELETE` 、 `UPDATE`などのステートメントで手動で編集しても、すぐには有効になりません。この動作は MySQL と互換性があり、権限キャッシュは次のステートメントで更新できます。

```sql
FLUSH PRIVILEGES;
```
