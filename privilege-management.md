---
title: Privilege Management
summary: 権限を管理する方法を学びます。
---

# 権限管理 {#privilege-management}

TiDBは、 MySQL 5.7の権限管理システム（構文と権限タイプを含む）をサポートしています。また、MySQL 8.0の以下の機能もサポートされています。

-   TiDB 3.0 以降の SQL ロール。
-   動的権限(TiDB 5.1 以降)。

このドキュメントでは、権限関連の TiDB 操作、TiDB 操作に必要な権限、および権限システムの実装について説明します。

## 特権関連の操作 {#privilege-related-operations}

### 権限を付与する {#grant-privileges}

[`GRANT`](/sql-statements/sql-statement-grant-privileges.md)ステートメントは、ユーザー アカウントに権限を付与します。

たとえば、次のステートメントを使用して、 `xxx`ユーザーに`test`データベースを読み取る権限を付与します。

```sql
GRANT SELECT ON test.* TO 'xxx'@'%';
```

次のステートメントを使用して、 `xxx`ユーザーにすべてのデータベースに対するすべての権限を付与します。

```sql
GRANT ALL PRIVILEGES ON *.* TO 'xxx'@'%';
```

デフォルトでは、指定されたユーザーが存在しない場合、 [`GRANT`](/sql-statements/sql-statement-grant-privileges.md)ステートメントはエラーを返します。この動作は、 [SQLモード](/system-variables.md#sql_mode) `NO_AUTO_CREATE_USER`が指定されているかどうかによって異なります。

```sql
SET sql_mode=DEFAULT;
```

    Query OK, 0 rows affected (0.00 sec)

```sql
SELECT @@sql_mode;
```

    +-------------------------------------------------------------------------------------------------------------------------------------------+
    | @@sql_mode                                                                                                                                |
    +-------------------------------------------------------------------------------------------------------------------------------------------+
    | ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
    +-------------------------------------------------------------------------------------------------------------------------------------------+
    1 row in set (0.00 sec)

```sql
SELECT * FROM mysql.user WHERE user='idontexist';
```

    Empty set (0.00 sec)

```sql
GRANT ALL PRIVILEGES ON test.* TO 'idontexist';
```

    ERROR 1105 (HY000): You are not allowed to create a user with GRANT

```sql
SELECT user,host,authentication_string FROM mysql.user WHERE user='idontexist';
```

    Empty set (0.00 sec)

以下の例では、SQLモード`NO_AUTO_CREATE_USER`設定されていないため、ユーザー`idontexist`空のパスワードで自動的に作成されます。これはセキュリティリスクを伴うため**推奨されません**。ユーザー名のスペルミスにより、空のパスワードで新規ユーザーが作成されます。

```sql
SET @@sql_mode='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
```

    Query OK, 0 rows affected (0.00 sec)

```sql
SELECT @@sql_mode;
```

    +-----------------------------------------------------------------------------------------------------------------------+
    | @@sql_mode                                                                                                            |
    +-----------------------------------------------------------------------------------------------------------------------+
    | ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION |
    +-----------------------------------------------------------------------------------------------------------------------+
    1 row in set (0.00 sec)

```sql
SELECT * FROM mysql.user WHERE user='idontexist';
```

    Empty set (0.00 sec)

```sql
GRANT ALL PRIVILEGES ON test.* TO 'idontexist';
```

    Query OK, 1 row affected (0.05 sec)

```sql
SELECT user,host,authentication_string FROM mysql.user WHERE user='idontexist';
```

    +------------+------+-----------------------+
    | user       | host | authentication_string |
    +------------+------+-----------------------+
    | idontexist | %    |                       |
    +------------+------+-----------------------+
    1 row in set (0.01 sec)

[`GRANT`](/sql-statements/sql-statement-grant-privileges.md)のあいまい一致を使用して、データベースに権限を付与できます。

```sql
GRANT ALL PRIVILEGES ON `te%`.* TO genius;
```

    Query OK, 0 rows affected (0.00 sec)

```sql
SELECT user,host,db FROM mysql.db WHERE user='genius';
```

    +--------|------|-----+
    | user   | host | db  |
    +--------|------|-----+
    | genius | %    | te% |
    +--------|------|-----+
    1 row in set (0.00 sec)

この例では、 `te%`の`%`により、 `te`で始まるすべてのデータベースに権限が付与されます。

### 権限を取り消す {#revoke-privileges}

[`REVOKE`](/sql-statements/sql-statement-revoke-privileges.md)ステートメントにより、システム管理者はユーザー アカウントから権限を取り消すことができます。

`REVOKE`ステートメントは`GRANT`ステートメントに対応しています。

```sql
REVOKE ALL PRIVILEGES ON `test`.* FROM 'genius'@'localhost';
```

> **注記：**
>
> 権限を取り消すには、完全に一致する文字列が必要です。一致する結果が見つからない場合は、エラーが表示されます。

```sql
REVOKE ALL PRIVILEGES ON `te%`.* FROM 'genius'@'%';
```

    ERROR 1141 (42000): There is no such grant defined for user 'genius' on host '%'

あいまい一致、エスケープ、文字列、識別子について:

```sql
GRANT ALL PRIVILEGES ON `te\%`.* TO 'genius'@'localhost';
```

    Query OK, 0 rows affected (0.00 sec)

この例では、完全一致を使用して`te%`という名前のデータベースを検索します。3 `%`エスケープ文字`\`使用されているため、 `%`ワイルドカードとして認識されないことに注意してください。

文字列は一重引用符（&#39;&#39;）で囲みますが、識別子はバッククォート（``）で囲みます。以下の違いをご確認ください。

```sql
GRANT ALL PRIVILEGES ON 'test'.* TO 'genius'@'localhost';
```

    ERROR 1064 (42000): You have an error in your SQL syntax; check the
    manual that corresponds to your MySQL server version for the right
    syntax to use near ''test'.* to 'genius'@'localhost'' at line 1

```sql
GRANT ALL PRIVILEGES ON `test`.* TO 'genius'@'localhost';
```

    Query OK, 0 rows affected (0.00 sec)

テーブル名に特別なキーワードを使用する場合は、それらをバッククォート (``) で囲みます。例:

```sql
CREATE TABLE `select` (id int);
```

    Query OK, 0 rows affected (0.27 sec)

### ユーザーに付与された権限を確認する {#check-privileges-granted-to-users}

`SHOW GRANTS`ステートメントを使用すると、ユーザーに付与されている権限を確認できます。例:

```sql
SHOW GRANTS; -- show grants for the current user
```

    +-------------------------------------------------------------+
    | Grants for User                                             |
    +-------------------------------------------------------------+
    | GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION |
    +-------------------------------------------------------------+

```sql
SHOW GRANTS FOR 'root'@'%'; -- show grants for a specific user
```

たとえば、ユーザー`rw_user@192.168.%`を作成し、そのユーザーに`test.write_table`テーブルへの書き込み権限とグローバル読み取り権限を付与します。

```sql
CREATE USER `rw_user`@`192.168.%`;
GRANT SELECT ON *.* TO `rw_user`@`192.168.%`;
GRANT INSERT, UPDATE ON `test`.`write_table` TO `rw_user`@`192.168.%`;
```

`rw_user@192.168.%`のユーザーに付与された権限を表示します:

```sql
SHOW GRANTS FOR `rw_user`@`192.168.%`;
```

    +------------------------------------------------------------------+
    | Grants for rw_user@192.168.%                                     |
    +------------------------------------------------------------------+
    | GRANT Select ON *.* TO 'rw_user'@'192.168.%'                     |
    | GRANT Insert,Update ON test.write_table TO 'rw_user'@'192.168.%' |
    +------------------------------------------------------------------+

### 動的権限 {#dynamic-privileges}

TiDB v5.1以降、MySQL 8.0から導入された動的権限がサポートされています。動的権限は、特定の操作に対するよりきめ細かなアクセス制御を実装することで、 `SUPER`権限を置き換えることを目的としています。例えば、動的権限を使用することで、システム管理者は`BACKUP`と`RESTORE`操作のみを実行できるユーザーアカウントを作成できます。

動的権限には次のものが含まれます。

-   `BACKUP_ADMIN`
-   `RESTORE_ADMIN`
-   `SYSTEM_USER`
-   `SYSTEM_VARIABLES_ADMIN`
-   `ROLE_ADMIN`
-   `CONNECTION_ADMIN`
-   `PLACEMENT_ADMIN`の場合、権限所有者は配置ポリシーを作成、変更、削除できます。
-   `DASHBOARD_CLIENT`権限所有者が TiDB ダッシュボードにログインすることを許可します。
-   `RESTRICTED_TABLES_ADMIN` 、SEM が有効な場合に権限所有者がシステム テーブルを表示できるようにします。
-   `RESTRICTED_STATUS_ADMIN` 、SEM が有効な場合に、権限所有者が[`SHOW [GLOBAL|SESSION] STATUS`](/sql-statements/sql-statement-show-status.md)のすべてのステータス変数を表示できるようにします。
-   `RESTRICTED_VARIABLES_ADMIN`場合、SEM が有効なときに権限所有者はすべてのシステム変数を表示できます。
-   `RESTRICTED_USER_ADMIN` 、SEM が有効な場合に、特権所有者のアクセスが SUPER ユーザーによって取り消されることを禁止します。
-   `RESTRICTED_CONNECTION_ADMIN`場合、権限所有者は`RESTRICTED_USER_ADMIN`ユーザーの接続を切断できます。この権限は`KILL`と`KILL TIDB`ステートメントに影響します。
-   `RESTRICTED_REPLICA_WRITER_ADMIN`では、TiDB クラスタで読み取り専用モードが有効になっている場合でも、権限所有者は影響を受けずに書き込みまたは更新操作を実行できます。詳細については、 [`tidb_restricted_read_only`](/system-variables.md#tidb_restricted_read_only-new-in-v520)参照してください。

動的権限の全セットを確認するには、 `SHOW PRIVILEGES`ステートメントを実行してください。プラグインは新しい権限を追加できるため、割り当て可能な権限のリストはTiDBのインストール状況によって異なる場合があります。

## <code>SUPER</code>特権 {#code-super-code-privilege}

-   `SUPER`権限を持つユーザーは、ほぼすべての操作を実行できます。デフォルトでは、この権限は`root`ユーザーにのみ付与されます。他のユーザーにこの権限を付与する場合は注意してください。
-   `SUPER`権限は[MySQL 8.0で非推奨](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#dynamic-privileges-migration-from-super)みなされ、よりきめ細かいアクセス制御を提供するために[動的権限](#dynamic-privileges)に置き換えることができます。

## TiDB操作に必要な権限 {#privileges-required-for-tidb-operations}

TiDBユーザーの権限は`INFORMATION_SCHEMA.USER_PRIVILEGES`テーブルで確認できます。例：

```sql
SELECT * FROM INFORMATION_SCHEMA.USER_PRIVILEGES WHERE grantee = "'root'@'%'";
```

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

### 変更 {#alter}

-   すべての`ALTER`ステートメントについて、ユーザーは対応するテーブルに対する`ALTER`権限を持っている必要があります。
-   `ALTER...DROP`と`ALTER...RENAME TO`以外のステートメントの場合、ユーザーは対応するテーブルに対して`INSERT`と`CREATE`権限を持っている必要があります。
-   `ALTER...DROP`ステートメントの場合、ユーザーは対応するテーブルに対する`DROP`権限を持っている必要があります。
-   `ALTER...RENAME TO`ステートメントの場合、ユーザーは名前変更前のテーブルに対して`DROP`権限を持っている必要があり、名前変更後のテーブルに対して`CREATE`権限と`INSERT`権限ている必要があります。

> **注記：**
>
> MySQL 5.7のドキュメントでは、テーブルに対して`ALTER`操作を実行するには権限`INSERT`と`CREATE`が必要であると記載されています。しかし、 MySQL 5.7では実際には、この場合`ALTER`権限のみが必要です。現在、TiDBにおける`ALTER`の権限は、MySQLの実際の動作と一致しています。

### バックアップ {#backup}

`SUPER`または`BACKUP_ADMIN`権限が必要です。

### インポートジョブをキャンセル {#cancel-import-job}

他のユーザーが作成したジョブをキャンセルするには、権限`SUPER`必要です。権限がない場合、現在のユーザーが作成したジョブのみをキャンセルできます。

### データベースの作成 {#create-database}

データベースに対して`CREATE`権限が必要です。

### インデックスの作成 {#create-index}

テーブルに対する`INDEX`権限が必要です。

### テーブルの作成 {#create-table}

テーブルに対する`CREATE`権限が必要です。

`CREATE TABLE...LIKE...`ステートメントを実行するには、テーブルに対する`SELECT`権限が必要です。

### ビューを作成 {#create-view}

`CREATE VIEW`権限が必要です。

> **注記：**
>
> 現在のユーザーがビューを作成したユーザーでない場合は、権限`CREATE VIEW`と`SUPER`両方が必要です。

### データベースの削除 {#drop-database}

データベースに対して`DROP`権限が必要です。

### インデックスの削除 {#drop-index}

テーブルに対する`INDEX`権限が必要です。

### テーブルを削除する {#drop-tables}

テーブルに対する`DROP`権限が必要です。

### インポート先 {#import-into}

対象テーブルに対して`SELECT` 、 `UPDATE` 、 `INSERT` 、 `DELETE` 、 `ALTER`権限が必要です。TiDBにローカルに保存されているファイルをインポートするには、 `FILE`権限も必要です。

### データをロード {#load-data}

テーブルに対する`INSERT`権限が必要です。 `REPLACE INTO`使用する場合は、 `DELETE`権限も必要です。

### テーブルを切り捨てる {#truncate-table}

テーブルに対する`DROP`権限が必要です。

### テーブル名の変更 {#rename-table}

名前を変更する前のテーブルに対して`ALTER`と`DROP`権限が必要であり、名前を変更した後のテーブルに対して`CREATE`と`INSERT`権限が必要です。

### テーブルを分析する {#analyze-table}

テーブルに対して`INSERT`および`SELECT`権限が必要です。

### ロック統計 {#lock-stats}

テーブルに対して`INSERT`および`SELECT`権限が必要です。

### 統計情報をアンロック {#unlock-stats}

テーブルに対して`INSERT`および`SELECT`権限が必要です。

### 見せる {#show}

`SHOW CREATE TABLE` 、テーブルに対する単一の権限が必要です。

`SHOW CREATE VIEW`は`SHOW VIEW`権限が必要です。

`SHOW GRANTS` `mysql`データベースに対する`SELECT`権限を必要とします。対象ユーザーが現在のユーザーである場合、 `SHOW GRANTS`権限を必要としません。

`SHOW PROCESSLIST`他のユーザーに属する接続を表示するには`PROCESS`権限が必要です。

`SHOW IMPORT JOB` 、他のユーザーの接続を表示するには`SUPER`権限が必要です。権限がない場合は、現在のユーザーが作成したジョブのみが表示されます。

`SHOW STATS_LOCKED` `mysql.stats_table_locked`テーブルに対する`SELECT`権限が必要です。

### ロール/ユーザーの作成 {#create-role-user}

`CREATE ROLE`は`CREATE ROLE`権限が必要です。

`CREATE USER`は`CREATE USER`権限が必要です。

### ロール/ユーザーの削除 {#drop-role-user}

`DROP ROLE`は`DROP ROLE`権限が必要です。

`DROP USER`は`CREATE USER`権限が必要です。

### ユーザーの変更 {#alter-user}

`CREATE USER`権限が必要です。

### 付与 {#grant}

`GRANT`によって付与される権限とともに`GRANT`権限が必要です。

ユーザーを暗黙的に作成するには、追加の権限が`CREATE USER`必要です。

`GRANT ROLE`は`SUPER`または`ROLE_ADMIN`権限が必要です。

### 取り消す {#revoke}

`GRANT`権限と`REVOKE`ステートメントの対象となる権限が必要です。

`REVOKE ROLE`は`SUPER`または`ROLE_ADMIN`権限が必要です。

### グローバル設定 {#set-global}

グローバル変数を設定するには、 `SUPER`または`SYSTEM_VARIABLES_ADMIN`権限が必要です。

### 管理者 {#admin}

`SUPER`権限が必要です。

### デフォルトロールの設定 {#set-default-role}

`SUPER`権限が必要です。

### 殺す {#kill}

他のユーザー セッションを終了するには、 `SUPER`または`CONNECTION_ADMIN`権限が必要です。

### リソースグループの作成 {#create-resource-group}

`SUPER`または`RESOURCE_GROUP_ADMIN`権限が必要です。

### リソースグループの変更 {#alter-resource-group}

`SUPER`または`RESOURCE_GROUP_ADMIN`権限が必要です。

### リソースグループの削除 {#drop-resource-group}

`SUPER`または`RESOURCE_GROUP_ADMIN`権限が必要です。

### リソースの調整 {#calibrate-resource}

`SUPER`または`RESOURCE_GROUP_ADMIN`権限が必要です。

### リソースグループの設定 {#set-resource-group}

システム変数[`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-new-in-v820) `ON`に設定されている場合、このステートメントを実行するには`SUPER` 、 `RESOURCE_GROUP_ADMIN` 、または`RESOURCE_GROUP_USER`権限が必要です。

## 特権制度の導入 {#implementation-of-the-privilege-system}

### 権限テーブル {#privilege-table}

次の[`mysql`システムテーブル](/mysql-schema/mysql-schema.md) 、権限に関連するすべてのデータが格納されているため特別です。

-   `mysql.user` (ユーザーアカウント、グローバル権限)
-   `mysql.db` （データベースレベルの権限）
-   `mysql.tables_priv` （テーブルレベルの権限）
-   `mysql.columns_priv` (列レベルの権限。現在はサポートされていません)

これらのテーブルには、データの有効範囲と権限情報が含まれています。例えば、テーブル`mysql.user`では次のようになります。

```sql
SELECT User,Host,Select_priv,Insert_priv FROM mysql.user LIMIT 1;
```

    +------|------|-------------|-------------+
    | User | Host | Select_priv | Insert_priv |
    +------|------|-------------|-------------+
    | root | %    | Y           | Y           |
    +------|------|-------------|-------------+
    1 row in set (0.00 sec)

このレコードでは、 `Host`と`User` 、 `root`ユーザーが任意のホスト（ `%` ）から送信した接続要求を受け入れることができることを示しています。9と`Insert_priv` `Select_priv`ユーザーがグローバル権限`Select`と`Insert`持っていることを意味します。17 `mysql.user`テーブルにおける有効範囲はグローバルです。

`mysql.db`の`Host`と`User` 、ユーザーがアクセスできるデータベースを決定します。有効範囲はデータベースです。

> **注記：**
>
> 権限テーブルの更新は、 `GRANT` 、 `CREATE USER` 、 `DROP USER`などの指定構文のみで行うことをお勧めします。基盤となる権限テーブルを直接編集しても権限キャッシュは自動的に更新されず、 `FLUSH PRIVILEGES`が実行されるまで予期しない動作が発生します。

### 接続検証 {#connection-verification}

クライアントが接続要求を送信すると、TiDBサーバーはログイン操作を検証します。TiDBサーバーはまず`mysql.user`テーブルをチェックします。3 `User`と`Host`のレコードが接続要求と一致する場合、TiDBサーバーは`authentication_string`レコードを検証します。

ユーザーIDは、2つの情報に基づいています。1 `Host`は接続を開始するホスト、もう`User`はユーザー名です。ユーザー名が空でない場合、ユーザー名は必ず一致する必要があります。

`User` + `Host`テーブル`user`の複数の行に一致する可能性があります。このシナリオに対処するため、テーブル`user`の行はソートされます。クライアントが接続すると、テーブルの行が1つずつチェックされ、最初に一致した行が検証に使用されます。ソートの際、Host は User よりも上位にランク付けされます。

### 確認をリクエストする {#request-verification}

接続が成功すると、要求検証プロセスによって、操作に権限があるかどうかがチェックされます。

データベース関連のリクエスト（ `INSERT` `UPDATE`の場合、リクエスト検証プロセスはまず`mysql.user`テーブルでユーザーのグローバル権限を確認します。権限が付与されている場合は直接アクセスできます。権限が付与されていない場合は、 `mysql.db`テーブルを確認します。

`user`テーブルは、デフォルトのデータベースに関係なく、グローバル権限を持ちます。例えば、 `user`のテーブルの`DELETE`権限は、任意の行、テーブル、またはデータベースに適用できます。

`db`番目のテーブルでは、空のユーザーが匿名ユーザー名と一致します。3 `User`の列ではワイルドカードは使用できません。5 `Host`と`Db`番目の列の値には、パターンマッチングが可能な`%`と`_`使用できます。

テーブル`user`と`db`のデータも、メモリにロードされるときにソートされます。

`tables_priv`と`columns_priv`における`%`の使用法は似ていますが、 `Db` 、 `Table_name` 、 `Column_name`列値には`%`含めることはできません。ロード時のソートも同様です。

### 効果時間 {#time-of-effect}

TiDBが起動すると、いくつかの権限チェックテーブルがメモリにロードされ、キャッシュされたデータ`GRANT`使用して権限が検証されます。1、3、5、7 `REVOKE`の権限管理ステートメント`CREATE USER`実行すると、すぐに有効`DROP USER`なります。

`mysql.user`のようなテーブルを`INSERT` 、 `DELETE` 、 `UPDATE`ようなステートメントで手動で編集しても、すぐには反映されません。この動作はMySQLと互換性があり、権限キャッシュは[`FLUSH PRIVILEGES`](/sql-statements/sql-statement-flush-privileges.md)なステートメントで更新できます。
