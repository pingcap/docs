---
title: Privilege Management
summary: Learn how to manage the privilege.
---

# 権限管理 {#privilege-management}

TiDBは、構文や特権タイプなど、MySQL5.7の特権管理システムをサポートしています。 MySQL8.0の次の機能もサポートされています。

-   TiDB3.0以降のSQLロール。
-   TiDB5.1以降の動的特権。

このドキュメントでは、特権関連のTiDB操作、TiDB操作に必要な特権、および特権システムの実装について説明します。

## 特権関連の操作 {#privilege-related-operations}

### 特権を付与する {#grant-privileges}

`GRANT`ステートメントは、ユーザーアカウントに特権を付与します。

たとえば、次のステートメントを使用して、 `xxx`人のユーザーに`test`のデータベースを読み取る権限を付与します。

```sql
GRANT SELECT ON test.* TO 'xxx'@'%';
```

次のステートメントを使用して、 `xxx`人のユーザーにすべてのデータベースに対するすべての特権を付与します。

```sql
GRANT ALL PRIVILEGES ON *.* TO 'xxx'@'%';
```

デフォルトでは、指定したユーザーが存在しない場合、 `GRANT`ステートメントはエラーを返します。この動作は、SQLモード`NO_AUTO_CREATE_USER`が指定されているかどうかによって異なります。

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

次の例では、SQLモード`NO_AUTO_CREATE_USER`が設定されていないため、ユーザー`idontexist`は空のパスワードで自動的に作成されます。これはセキュリティ上のリスクがあるため、**お勧めしません**。ユーザー名のスペルを間違えると、空のパスワードで新しいユーザーが作成されます。

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

`GRANT`のあいまい一致を使用して、データベースに特権を付与できます。

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

この例では、 `te%`分の`%`であるため、 `te`で始まるすべてのデータベースに特権が付与されます。

### 特権を取り消す {#revoke-privileges}

`REVOKE`ステートメントを使用すると、システム管理者はユーザーアカウントから特権を取り消すことができます。

`REVOKE`ステートメントは`REVOKE`ステートメントに対応します。

```sql
REVOKE ALL PRIVILEGES ON `test`.* FROM 'genius'@'localhost';
```

> **ノート：**
>
> 特権を取り消すには、完全に一致する必要があります。一致する結果が見つからない場合は、エラーが表示されます。

```sql
mysql> REVOKE ALL PRIVILEGES ON `te%`.* FROM 'genius'@'%';
ERROR 1141 (42000): There is no such grant defined for user 'genius' on host '%'
```

あいまい一致、エスケープ、文字列、および識別子について：

```sql
mysql> GRANT ALL PRIVILEGES ON `te\%`.* TO 'genius'@'localhost';
Query OK, 0 rows affected (0.00 sec)
```

この例では、完全一致を使用して`te%`という名前のデータベースを検索します。 `%`は`\`エスケープ文字を使用するため、 `%`はワイルドカードとは見なされないことに注意してください。

文字列は一重引用符（&#39;&#39;）で囲まれ、識別子はバッククォート（ ``）で囲まれます。以下の違いを参照してください。

```sql
mysql> GRANT ALL PRIVILEGES ON 'test'.* TO 'genius'@'localhost';
ERROR 1064 (42000): You have an error in your SQL syntax; check the
manual that corresponds to your MySQL server version for the right
syntax to use near ''test'.* to 'genius'@'localhost'' at line 1

mysql> GRANT ALL PRIVILEGES ON `test`.* TO 'genius'@'localhost';
Query OK, 0 rows affected (0.00 sec)
```

テーブル名として特別なキーワードを使用する場合は、それらをバッククォート（ ``）で囲みます。例えば：

```sql
mysql> CREATE TABLE `select` (id int);
Query OK, 0 rows affected (0.27 sec)
```

### ユーザーに付与されている権限を確認する {#check-privileges-granted-to-users}

`SHOW GRANTS`ステートメントを使用して、ユーザーに付与されている特権を確認できます。例えば：

```sql
SHOW GRANTS; -- show grants for the current user

+-------------------------------------------------------------+
| Grants for User                                             |
+-------------------------------------------------------------+
| GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION |
+-------------------------------------------------------------+
SHOW GRANTS FOR 'root'@'%'; -- show grants for a specific user
```

たとえば、ユーザー`rw_user@192.168.%`を作成し、 `test.write_table`テーブルに対する書き込み権限とグローバル読み取り権限をユーザーに付与します。

```sql
CREATE USER `rw_user`@`192.168.%`;
GRANT SELECT ON *.* TO `rw_user`@`192.168.%`;
GRANT INSERT, UPDATE ON `test`.`write_table` TO `rw_user`@`192.168.%`;
```

`rw_user@192.168.%`人のユーザーに付与された特権を表示します。

```sql
SHOW GRANTS FOR `rw_user`@`192.168.%`;

+------------------------------------------------------------------+
| Grants for rw_user@192.168.%                                     |
+------------------------------------------------------------------+
| GRANT Select ON *.* TO 'rw_user'@'192.168.%'                     |
| GRANT Insert,Update ON test.write_table TO 'rw_user'@'192.168.%' |
+------------------------------------------------------------------+
```

### 動的特権 {#dynamic-privileges}

v5.1以降、TiDB機能は動的特権をサポートします。これはMySQL8.0から借用した機能です。動的特権は、特定の操作へのよりきめ細かいアクセスを実装することにより、 `SUPER`の特権を置き換えることを目的としています。たとえば、動的特権を使用して、システム管理者は`BACKUP`および`RESTORE`の操作のみを実行できるユーザーアカウントを作成できます。

動的特権には次のものがあります。

-   `BACKUP_ADMIN`
-   `RESTORE_ADMIN`
-   `ROLE_ADMIN`
-   `CONNECTION_ADMIN`
-   `SYSTEM_VARIABLES_ADMIN`
-   `RESTRICTED_REPLICA_WRITER_ADMIN`を使用すると、特権所有者は、TiDBクラスタで読み取り専用モードが有効になっている場合に影響を受けることなく書き込みまたは更新操作を実行できます。詳細については、 [`tidb_restricted_read_only`](/system-variables.md#tidb_restricted_read_only-new-in-v520)を参照してください。

動的特権の完全なセットを表示するには、 `SHOW PRIVILEGES`ステートメントを実行します。プラグインは新しい特権を追加することが許可されているため、割り当て可能な特権のリストは、TiDBのインストールによって異なる場合があります。

## TiDB操作に必要な権限 {#privileges-required-for-tidb-operations}

`INFORMATION_SCHEMA.USER_PRIVILEGES`の表でTiDBユーザーの権限を確認できます。例えば：

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

### ALTER {#alter}

-   `ALTER`のステートメントすべてについて、ユーザーは対応するテーブルに対して`ALTER`の特権を持っている必要があります。
-   `ALTER...DROP`と`ALTER...RENAME TO`を除くステートメントの場合、ユーザーは対応するテーブルに対して`INSERT`と`CREATE`の特権を持っている必要があります。
-   `ALTER...DROP`ステートメントの場合、ユーザーは対応するテーブルに対して`DROP`特権を持っている必要があります。
-   `ALTER...RENAME TO`ステートメントの場合、ユーザーは、名前を変更する前にテーブルに対して`DROP`の特権を持ち、名前を変更した後にテーブルに対して`CREATE`と`INSERT`の特権を持っている必要があります。

> **ノート：**
>
> MySQL 5.7のドキュメントでは、ユーザーはテーブルに対して`ALTER`の操作を実行するために`INSERT`と`CREATE`の特権が必要です。ただし、実際にはMySQL 5.7.25の場合、この場合は`ALTER`の特権のみが必要です。現在、TiDBの`ALTER`特権は、MySQLの実際の動作と一致しています。

### バックアップ {#backup}

`SUPER`または`BACKUP_ADMIN`の特権が必要です。

### データベースの作成 {#create-database}

データベースに`CREATE`の特権が必要です。

### インデックスの作成 {#create-index}

テーブルに`INDEX`の特権が必要です。

### CREATE TABLE {#create-table}

テーブルに`CREATE`の特権が必要です。

`CREATE TABLE...LIKE...`ステートメントを実行するには、テーブルに対する`SELECT`特権が必要です。

### ビューの作成 {#create-view}

`CREATE VIEW`の特権が必要です。

> **ノート：**
>
> 現在のユーザーがビューを作成したユーザーでない場合は、 `CREATE VIEW`と`SUPER`の両方の権限が必要です。

### ドロップデータベース {#drop-database}

テーブルに`DROP`の特権が必要です。

### ドロップインデックス {#drop-index}

テーブルに`INDEX`の特権が必要です。

### ドロップテーブル {#drop-tables}

テーブルに`DROP`の特権が必要です。

### データを読み込む {#load-data}

テーブルに`INSERT`の特権が必要です。

### 切り捨てテーブル {#truncate-table}

テーブルに`DROP`の特権が必要です。

### テーブルの名前を変更 {#rename-table}

名前を変更する前にテーブルに`ALTER`と`DROP`の特権が必要であり、名前を変更した後にテーブルに`CREATE`と`INSERT`の特権が必要です。

### テーブルの分析 {#analyze-table}

テーブルには`INSERT`と`SELECT`の権限が必要です。

### 見せる {#show}

`SHOW CREATE TABLE`には、テーブルに対する単一の特権が必要です。

`SHOW CREATE VIEW`には`SHOW VIEW`特権が必要です。

`SHOW GRANTS`には、 `mysql`データベースに対する`SELECT`特権が必要です。ターゲットユーザーが現在のユーザーである場合、 `SHOW GRANTS`は特権を必要としません。

`SHOW PROCESSLIST`は、他のユーザーに属する接続を表示するために`SUPER`を必要とします。

### 役割/ユーザーの作成 {#create-role-user}

`CREATE ROLE`には`CREATE ROLE`特権が必要です。

`CREATE USER`には`CREATE USER`特権が必要です。

### ドロップロール/ユーザー {#drop-role-user}

`DROP ROLE`には`DROP ROLE`特権が必要です。

`DROP USER`には`CREATE USER`特権が必要です。

### ALTER USER {#alter-user}

`CREATE USER`の特権が必要です。

### 許す {#grant}

`GRANT`によって付与された特権を持つ`GRANT`の特権が必要です。

暗黙的にユーザーを作成するには、追加の`CREATE USER`の特権が必要です。

`GRANT ROLE`には`SUPER`または`ROLE_ADMIN`の特権が必要です。

### 取り消す {#revoke}

`GRANT`の特権と`REVOKE`のステートメントの対象となる特権が必要です。

`REVOKE ROLE`には`SUPER`または`ROLE_ADMIN`の特権が必要です。

### グローバルに設定 {#set-global}

グローバル変数を設定するには、 `SUPER`つまたは`SYSTEM_VARIABLES_ADMIN`の特権が必要です。

### 管理者 {#admin}

`SUPER`の特権が必要です。

### デフォルトの役割を設定 {#set-default-role}

`SUPER`の特権が必要です。

### 殺す {#kill}

他のユーザーセッションを強制終了するには、 `SUPER`つまたは`CONNECTION_ADMIN`の特権が必要です。

## 特権システムの実装 {#implementation-of-the-privilege-system}

### 特権テーブル {#privilege-table}

次のシステムテーブルは、すべての特権関連データが格納されているため、特別です。

-   `mysql.user` （ユーザーアカウント、グローバル特権）
-   `mysql.db` （データベースレベルの特権）
-   `mysql.tables_priv` （テーブルレベルの特権）
-   `mysql.columns_priv` （列レベルの特権。現在はサポートされていません）

これらのテーブルには、データの有効範囲と特権情報が含まれています。たとえば、 `mysql.user`の表では次のようになります。

```sql
mysql> SELECT User,Host,Select_priv,Insert_priv FROM mysql.user LIMIT 1;
+------|------|-------------|-------------+
| User | Host | Select_priv | Insert_priv |
+------|------|-------------|-------------+
| root | %    | Y           | Y           |
+------|------|-------------|-------------+
1 row in set (0.00 sec)
```

このレコードでは、 `Host`と`User`は、任意のホスト（ `%` ）から`root`ユーザーによって送信された接続要求を受け入れることができることを決定します。 `Select_priv`と`Insert_priv`は、ユーザーがグローバル`Select`と`Insert`の特権を持っていることを意味します。 `mysql.user`表の有効射程はグローバルです。

`mysql.db`の`Host`と`User`は、ユーザーがアクセスできるデータベースを決定します。有効射程はデータベースです。

> **ノート：**
>
> `GRANT`などの提供された`DROP USER`を介してのみ特権テーブルを更新することをお勧めし`CREATE USER` 。基になる特権テーブルを直接編集しても、特権キャッシュは自動的に更新されないため、 `FLUSH PRIVILEGES`が実行されるまで予期しない動作が発生します。

### 接続検証 {#connection-verification}

クライアントが接続要求を送信すると、TiDBサーバーはログイン操作を確認します。 TiDBサーバーは最初に`mysql.user`のテーブルをチェックします。 `User`と`Host`のレコードが接続要求に一致する場合、TiDBサーバーは`authentication_string`を検証します。

ユーザーIDは、接続を開始するホストである`Host`とユーザー名である`User`の2つの情報に基づいています。ユーザー名が空でない場合、指定されたユーザーと完全に一致する必要があります。

`User` + `Host`は、 `user`のテーブルの複数の行に一致する場合があります。このシナリオに対処するために、 `user`テーブルの行がソートされます。クライアントが接続すると、テーブルの行が1つずつチェックされます。最初に一致した行が検証に使用されます。並べ替えの際、ホストはユーザーの前にランク付けされます。

### 確認をリクエストする {#request-verification}

接続が成功すると、要求検証プロセスは、操作に特権があるかどうかを確認します。

データベース関連の要求（ `INSERT` ）の場合、要求検証プロセスは最初に`UPDATE`テーブル内のユーザーのグローバル特権をチェックし`mysql.user` 。特権が付与されている場合は、直接アクセスできます。そうでない場合は、 `mysql.db`の表を確認してください。

`user`テーブルには、デフォルトのデータベースに関係なくグローバル権限があります。たとえば、 `user`の`DELETE`特権は、任意の行、テーブル、またはデータベースに適用できます。

`db`の表では、空のユーザーは匿名ユーザー名と一致します。 `User`列にワイルドカードを使用することはできません。 `Host`列と`Db`列の値は、パターンマッチングを使用できる`%`列と`_`列を使用できます。

`user`および`db`テーブルのデータも、メモリにロードされるときにソートされます。

`tables_priv`と`columns_priv`の`%`の使用法は似てい`Table_name`が、 `Db`の列の値に`Column_name`を含めることはできませ`%` 。ロード時の並べ替えも同様です。

### 効果の時間 {#time-of-effect}

TiDBが起動すると、いくつかの特権チェックテーブルがメモリにロードされ、キャッシュされたデータが特権の検証に使用されます。 `GRANT`などの`CREATE USER`管理ステートメントの実行はすぐに`DROP USER`になり`REVOKE` 。

`INSERT`などの`UPDATE`を使用して`mysql.user`などのテーブルを手動で編集しても、すぐには有効になりませ`DELETE` 。この動作はMySQLと互換性があり、特権キャッシュは次のステートメントで更新できます。

```sql
FLUSH PRIVILEGES;
```
