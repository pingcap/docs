---
title: Privilege Management
summary: 特権を管理する方法を学びましょう。
---

# 権限管理 {#privilege-management}

TiDBは、構文や権限タイプを含め、 MySQL 5.7の権限管理システムをサポートしています。また、MySQL 8.0の以下の機能もサポートしています。

-   TiDB 3.0以降で利用可能になったSQLロール。
-   TiDB 5.1以降では、動的な権限が可能になりました。

このドキュメントでは、権限に関連するTiDB操作、TiDB操作に必要な権限、および権限システムの実装について説明します。

## 特権関連の操作 {#privilege-related-operations}

### 権限を付与する {#grant-privileges}

[`GRANT`](/sql-statements/sql-statement-grant-privileges.md)文は、ユーザーアカウントに権限を付与します。

例えば、次のステートメントを使用して、 `xxx`ユーザーに`test`データベースを読み取る権限を付与します。

```sql
GRANT SELECT ON test.* TO 'xxx'@'%';
```

`xxx`ユーザーにすべてのデータベースに対するすべての権限を付与するには、次のステートメントを使用します。

```sql
GRANT ALL PRIVILEGES ON *.* TO 'xxx'@'%';
```

バージョン8.5.6以降、TiDBはMySQL互換の列レベルの権限管理メカニズムをサポートしています。指定したテーブルの特定の列に対して、 `SELECT` 、 `INSERT` 、 `UPDATE` 、および`REFERENCES`権限を付与または取り消すことができます。詳細については、[列レベルの権限管理](/column-privilege-management.md)を参照してください。

デフォルトでは、 [`GRANT`](/sql-statements/sql-statement-grant-privileges.md)ステートメントは、指定されたユーザーが存在しない場合にエラーを返します。この動作は、 [SQLモード](/system-variables.md#sql_mode)`NO_AUTO_CREATE_USER`が指定されているかどうかによって異なります。

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

次の例では、SQL モード`idontexist` `NO_AUTO_CREATE_USER`が空のパスワードで自動的に作成されます。これはセキュリティ上のリスクとなるため**推奨されません**。ユーザー名のスペルミスがあると、空のパスワードで新しいユーザーが作成されてしまいます。

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

[`GRANT`](/sql-statements/sql-statement-grant-privileges.md)コマンドでは、あいまい一致を使用してデータベースに権限を付与できます。

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

この例では、 `%`内の`te%`により、 `te`で始まるすべてのデータベースに権限が付与されます。

### 権限を取り消す {#revoke-privileges}

[`REVOKE`](/sql-statements/sql-statement-revoke-privileges.md)ステートメントを使用すると、システム管理者はユーザーアカウントから権限を取り消すことができます。

`REVOKE`ステートメントは`GRANT`ステートメントに対応します。

```sql
REVOKE ALL PRIVILEGES ON `test`.* FROM 'genius'@'localhost';
```

> **注記：**
>
> 権限を取り消すには、完全一致が必要です。一致する結果が見つからない場合は、エラーが表示されます。

```sql
REVOKE ALL PRIVILEGES ON `te%`.* FROM 'genius'@'%';
```

    ERROR 1141 (42000): There is no such grant defined for user 'genius' on host '%'

あいまい一致、エスケープシーケンス、文字列、識別子について：

```sql
GRANT ALL PRIVILEGES ON `te\%`.* TO 'genius'@'localhost';
```

    Query OK, 0 rows affected (0.00 sec)

この例では、完全一致を使用して`te%`という名前のデータベースを検索します。 `%`は`\`エスケープ文字を使用しているため、 `%`はワイルドカードとして扱われません。

文字列はシングルクォーテーションマーク（&#39;&#39;）で囲み、識別子はバッククォート（``）で囲みます。違いは以下のとおりです。

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

テーブル名として特別なキーワードを使用する場合は、バッククォート（``）で囲みます。例：

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

例えば、ユーザー`rw_user@192.168.%`を作成し、そのユーザーに`test.write_table`テーブルへの書き込み権限とグローバルな読み取り権限を付与します。

```sql
CREATE USER `rw_user`@`192.168.%`;
GRANT SELECT ON *.* TO `rw_user`@`192.168.%`;
GRANT INSERT, UPDATE ON `test`.`write_table` TO `rw_user`@`192.168.%`;
```

`rw_user@192.168.%`ユーザーに付与された権限を表示します。

```sql
SHOW GRANTS FOR `rw_user`@`192.168.%`;
```

    +------------------------------------------------------------------+
    | Grants for rw_user@192.168.%                                     |
    +------------------------------------------------------------------+
    | GRANT Select ON *.* TO 'rw_user'@'192.168.%'                     |
    | GRANT Insert,Update ON test.write_table TO 'rw_user'@'192.168.%' |
    +------------------------------------------------------------------+

### 動的な権限 {#dynamic-privileges}

バージョン5.1以降、TiDBはMySQL 8.0から取り入れた動的権限をサポートしています。動的権限は、特定の操作に対するよりきめ細かなアクセスを実装することで、 `SUPER`権限を置き換えることを目的としています。たとえば、動的権限を使用すると、システム管理者は`BACKUP`と`RESTORE`操作のみを実行できるユーザーアカウントを作成できます。

動的権限には以下が含まれます。

-   `BACKUP_ADMIN`
-   `RESTORE_ADMIN`
-   `SYSTEM_USER`
-   `SYSTEM_VARIABLES_ADMIN`
-   `ROLE_ADMIN`
-   `CONNECTION_ADMIN`
-   `PLACEMENT_ADMIN`は、権限所有者が配置ポリシーを作成、変更、削除できるようにします。
-   `DASHBOARD_CLIENT`は、権限所有者が TiDB ダッシュボードにログインできるようにします。
-   `RESTRICTED_TABLES_ADMIN`は、SEM が有効になっている場合に、権限所有者がシステム テーブルを表示できるようにします。
-   `RESTRICTED_STATUS_ADMIN`を使用すると、SEM が有効になっているときに、権限所有者は[`SHOW [GLOBAL|SESSION] STATUS`](/sql-statements/sql-statement-show-status.md)ですべてのステータス変数を表示できます。
-   `RESTRICTED_VARIABLES_ADMIN`は、SEM が有効になっている場合に、権限所有者がすべてのシステム変数を表示できるようにします。
-   `RESTRICTED_USER_ADMIN` SEM が有効になっている場合、特権所有者が SUPER ユーザーによってアクセス権を取り消されることを禁止します。
-   `RESTRICTED_CONNECTION_ADMIN`権限所有者が`RESTRICTED_USER_ADMIN`ユーザーの接続を強制終了することを許可します。この権限は`KILL`および`KILL TIDB`ステートメントに影響します。
-   `RESTRICTED_REPLICA_WRITER_ADMIN`使用すると、TiDB クラスタで読み取り専用モードが有効になっている場合でも、権限所有者は影響を受けることなく書き込みまたは更新操作を実行できます。詳細については、 [`tidb_restricted_read_only`](/system-variables.md#tidb_restricted_read_only-new-in-v520)参照してください。

動的権限の全セットを確認するには、 `SHOW PRIVILEGES`ステートメントを実行してください。プラグインは新しい権限を追加できるため、割り当て可能な権限のリストは、TiDB のインストール環境によって異なる場合があります。

## <code>SUPER</code>特権 {#code-super-code-privilege}

-   `SUPER`権限は、ユーザーがほぼすべての操作を実行できるようにします。デフォルトでは、 `root`ユーザーのみにこの権限が付与されています。他のユーザーにこの権限を付与する際は注意してください。
-   `SUPER`権限は[MySQL 8.0で非推奨になりました](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#dynamic-privileges-migration-from-super)推奨になりました。よりきめ細かいアクセス制御を提供するために[動的権限](#dynamic-privileges)に置き換えることができます。

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

### 変更する {#alter}

-   `ALTER`ステートメントすべてにおいて、ユーザーは対応するテーブルに対する`ALTER`権限を持っている必要があります。
-   `ALTER...DROP`および`ALTER...RENAME TO`以外のステートメントについては、ユーザーは対応するテーブルに対して`INSERT`および`CREATE`の権限を持っている必要があります。
-   `ALTER...DROP`ステートメントを使用するには、ユーザーは対応するテーブルに対して`DROP`権限を持っている必要があります。
-   `ALTER...RENAME TO`ステートメントを実行するには、ユーザーは名前変更前にテーブルに対する`DROP`権限を持ち、名前変更後にテーブルに対する`CREATE`および`INSERT`権限ている必要があります。

> **注記：**
>
> MySQL 5.7のドキュメントでは、テーブルに対して`INSERT`操作を実行するには、 `CREATE`および`ALTER`の権限であるとされています。しかし、実際にはMySQL 5.7では、この場合`ALTER`権限のみが必要です。現在、TiDB の`ALTER`権限は、MySQL の実際の動作と一致しています。

### バックアップ {#backup}

`SUPER`または`BACKUP_ADMIN`の権限が必要です。

### インポートジョブをキャンセルする {#cancel-import-job}

他のユーザーが作成したジョブをキャンセルするには`SUPER`権限が必要です。それ以外の場合は、現在のユーザーが作成したジョブのみキャンセルできます。

### データベースの作成 {#create-database}

データベースに対する`CREATE`権限が必要です。

### インデックスを作成する {#create-index}

テーブルに対する`INDEX`権限が必要です。

### テーブルを作成する {#create-table}

テーブルに対する`CREATE`権限が必要です。

`CREATE TABLE...LIKE...`ステートメントを実行するには、テーブルに対する`SELECT`権限が必要です。

### ビューの作成 {#create-view}

`CREATE VIEW`権限が必要です。

> **注記：**
>
> 現在のユーザーがビューを作成したユーザーでない場合、 `CREATE VIEW`と`SUPER`の両方の権限が必要です。

### データベースの削除 {#drop-database}

データベースに対する`DROP`権限が必要です。

### インデックスを削除 {#drop-index}

テーブルに対する`INDEX`権限が必要です。

### テーブルを削除する {#drop-tables}

テーブルに対する`DROP`権限が必要です。

### インポート先 {#import-into}

対象テーブルに対して`SELECT` 、 `UPDATE` 、 `INSERT` 、 `DELETE` 、および`ALTER`の権限が必要です。TiDBにローカルに保存されているファイルをインポートするには、 `FILE`権限も必要です。

### データの読み込み {#load-data}

テーブルに対して`INSERT`権限が必要です。 `REPLACE INTO`を使用する場合は、 `DELETE`権限も必要です。

### テーブルを切り捨てる {#truncate-table}

テーブルに対する`DROP`権限が必要です。

### テーブル名の変更 {#rename-table}

テーブル名を変更する前に、 `ALTER`および`DROP`の権限が必要であり、テーブル名を変更する後には`CREATE`および`INSERT`の権限。

### 表の分析 {#analyze-table}

テーブルに対する`INSERT`および`SELECT`の権限が必要です。

### ロック統計 {#lock-stats}

テーブルに対する`INSERT`および`SELECT`の権限が必要です。

### 統計情報をアンロックする {#unlock-stats}

テーブルに対する`INSERT`および`SELECT`の権限が必要です。

### 見せる {#show}

`SHOW CREATE TABLE`テーブルに対する単一の権限を必要とします。

`SHOW CREATE VIEW`には`SHOW VIEW`の権限が必要です。

`SHOW GRANTS`は`SELECT`データベースへの`mysql`権限を必要とします。対象ユーザーが現在のユーザーである場合、 `SHOW GRANTS`権限を必要としません。

`SHOW PROCESSLIST`は、他のユーザーに属する接続を表示するために`PROCESS`の権限を必要とします。

`SHOW IMPORT JOB`は、他のユーザーに属する接続を表示するために`SUPER`権限を必要とします。権限がない場合は、現在のユーザーが作成したジョブのみが表示されます。

`SHOW STATS_LOCKED`は`SELECT` `mysql.stats_table_locked` }} テーブルに対する権限を必要とします。

### ロール/ユーザーの作成 {#create-role-user}

`CREATE ROLE`には`CREATE ROLE`の権限が必要です。

`CREATE USER`には`CREATE USER`の権限が必要です。

### ロール/ユーザーを削除する {#drop-role-user}

`DROP ROLE`には`DROP ROLE`の権限が必要です。

`DROP USER`には`CREATE USER`の権限が必要です。

### ユーザーの変更 {#alter-user}

`CREATE USER`権限が必要です。

### 付与 {#grant}

`GRANT`によって付与された権限を持つ`GRANT`権限が必要です。

ユーザーを暗黙的に作成するには、追加の`CREATE USER`権限が必要です。

`GRANT ROLE`には`SUPER`または`ROLE_ADMIN`権限が必要です。

### 取り消す {#revoke}

`GRANT`権限と、 `REVOKE`ステートメントで指定されている権限が必要です。

`REVOKE ROLE`には`SUPER`または`ROLE_ADMIN`権限が必要です。

### グローバル設定 {#set-global}

グローバル変数を設定するには、 `SUPER`または`SYSTEM_VARIABLES_ADMIN`の権限が必要です。

### 管理者 {#admin}

`SUPER`の権限が必要です。

### デフォルトロールを設定する {#set-default-role}

`SUPER`の権限が必要です。

### 殺す {#kill}

他のユーザーセッションを終了するには、 `SUPER`または`CONNECTION_ADMIN`の権限が必要です。

### リソースグループを作成する {#create-resource-group}

`SUPER`または`RESOURCE_GROUP_ADMIN`の権限が必要です。

### アルター・リソース・グループ {#alter-resource-group}

`SUPER`または`RESOURCE_GROUP_ADMIN`の権限が必要です。

### リソースグループを削除する {#drop-resource-group}

`SUPER`または`RESOURCE_GROUP_ADMIN`の権限が必要です。

### リソースの校正 {#calibrate-resource}

`SUPER`または`RESOURCE_GROUP_ADMIN`の権限が必要です。

### リソースグループを設定する {#set-resource-group}

システム変数[`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-new-in-v820) `ON`に設定されている場合、このステートメントを実行するには`SUPER`または`RESOURCE_GROUP_ADMIN`または`RESOURCE_GROUP_USER`の権限が必要です。

## 特権システムの導入 {#implementation-of-the-privilege-system}

### 権限テーブル {#privilege-table}

次の[`mysql`システムテーブル](/mysql-schema/mysql-schema.md)すべての権限関連データが保存されているため、特別です。

-   `mysql.user` （ユーザーアカウント、グローバル権限）
-   `mysql.db` （データベースレベルの権限）
-   `mysql.tables_priv` （テーブルレベルの権限）
-   `mysql.columns_priv` （列レベルの権限。v8.5.6以降でサポート）

これらのテーブルには、データの有効範囲と権限情報が含まれています。たとえば、 `mysql.user`テーブルでは次のようになります。

```sql
SELECT User,Host,Select_priv,Insert_priv FROM mysql.user LIMIT 1;
```

    +------|------|-------------|-------------+
    | User | Host | Select_priv | Insert_priv |
    +------|------|-------------|-------------+
    | root | %    | Y           | Y           |
    +------|------|-------------|-------------+
    1 row in set (0.00 sec)

このレコードでは、 `Host`と`User`は`root`ユーザーから任意のホスト ( `%` ) から送信された接続要求を受け入れることができると判断します。 `Select_priv`と`Insert_priv`は、ユーザーがグローバルな`Select`および`Insert`権限を持っていることを意味します。 `mysql.user`テーブルの有効範囲はグローバルです。

`Host`内の`User`と`mysql.db`は、ユーザーがアクセスできるデータベースを決定します。有効な範囲はデータベースです。

> **注記：**
>
> `GRANT` 、 `CREATE USER` }}、 `DROP USER` `FLUSH PRIVILEGES`が実行されるまで予期しない動作が発生する可能性があります。

### 接続確認 {#connection-verification}

クライアントが接続要求を送信すると、TiDBサーバーはログイン操作を検証します。TiDBサーバーは最初に`mysql.user`テーブルをチェックします。 `User`と`Host`のレコードが接続要求と一致する場合、TiDBサーバーは`authentication_string`を検証します。

ユーザーの識別は、接続を開始するホスト`Host`とユーザー名`User`の2つの情報に基づいています。ユーザー名が空でない場合、指定されたユーザー名と完全に一致する必要があります。

`User` + `Host` `user`テーブルの複数の行に一致する可能性があります。このシナリオに対処するため、 `user`テーブルの行はソートされます。クライアントが接続すると、テーブルの行が 1 つずつチェックされ、最初に一致した行が検証に使用されます。ソート時には、ホストがユーザーよりも優先されます。

### リクエストの確認 {#request-verification}

接続が成功すると、要求検証プロセスによって、その操作に権限があるかどうかがチェックされます。

データベース関連のリクエスト（ `INSERT` 、 `UPDATE` ）の場合、リクエスト検証プロセスではまず`mysql.user`テーブルでユーザーのグローバル権限を確認します。権限が付与されている場合は、直接アクセスできます。付与されていない場合は、 `mysql.db`テーブルを確認します。

`user`テーブルは、デフォルトのデータベースに関係なく、グローバルな権限を持ちます。たとえば、 `DELETE`の`user`権限は、任意の行、テーブル、またはデータベースに適用できます。

`db`テーブルでは、空のユーザーは匿名ユーザー名に一致します。 `User`列ではワイルドカードは使用できません。 `Host`列と`Db`列の値には、パターンマッチングを使用できる`%`と`_`を使用できます。

`user`および`db`テーブルのデータも、メモリにロードされるときにソートされます。

`%`と`tables_priv`における`columns_priv`の使用方法は似ていますが、 `Db` 、 `Table_name` 、 `Column_name`の列値には`%`を含めることはできません。読み込み時のソートも同様です。

### 有効期間 {#time-of-effect}

TiDB が起動すると、いくつかの権限チェックテーブルがメモリにロードされ、キャッシュされたデータを使用して権限が検証されます。 `GRANT` 、 `REVOKE` 、 `CREATE USER` 、 `DROP USER`権限管理ステートメントを実行すると、すぐに反映されます。

`mysql.user`などのテーブルを`INSERT` 、 `DELETE` 、 `UPDATE`手動で編集しても、すぐに反映されません。この動作は MySQL と互換性があり、権限キャッシュは[`FLUSH PRIVILEGES`](/sql-statements/sql-statement-flush-privileges.md)ステートメントで更新できます。
