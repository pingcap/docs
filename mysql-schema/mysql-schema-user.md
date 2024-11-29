---
title: mysql.user
summary: mysql` スキーマの `user` テーブルについて学習します。
---

# <code>mysql.user</code> {#code-mysql-user-code}

`mysql.user`表には、ユーザー アカウントとその権限に関する情報が示されています。

`mysql.user`の構造を表示するには、次の SQL ステートメントを使用します。

```sql
DESC mysql.user;
```

出力は次のようになります。

    +------------------------+----------------------+------+------+-------------------+-------+
    | Field                  | Type                 | Null | Key  | Default           | Extra |
    +------------------------+----------------------+------+------+-------------------+-------+
    | Host                   | char(255)            | NO   | PRI  | NULL              |       |
    | User                   | char(32)             | NO   | PRI  | NULL              |       |
    | authentication_string  | text                 | YES  |      | NULL              |       |
    | plugin                 | char(64)             | YES  |      | NULL              |       |
    | Select_priv            | enum('N','Y')        | NO   |      | N                 |       |
    | Insert_priv            | enum('N','Y')        | NO   |      | N                 |       |
    | Update_priv            | enum('N','Y')        | NO   |      | N                 |       |
    | Delete_priv            | enum('N','Y')        | NO   |      | N                 |       |
    | Create_priv            | enum('N','Y')        | NO   |      | N                 |       |
    | Drop_priv              | enum('N','Y')        | NO   |      | N                 |       |
    | Process_priv           | enum('N','Y')        | NO   |      | N                 |       |
    | Grant_priv             | enum('N','Y')        | NO   |      | N                 |       |
    | References_priv        | enum('N','Y')        | NO   |      | N                 |       |
    | Alter_priv             | enum('N','Y')        | NO   |      | N                 |       |
    | Show_db_priv           | enum('N','Y')        | NO   |      | N                 |       |
    | Super_priv             | enum('N','Y')        | NO   |      | N                 |       |
    | Create_tmp_table_priv  | enum('N','Y')        | NO   |      | N                 |       |
    | Lock_tables_priv       | enum('N','Y')        | NO   |      | N                 |       |
    | Execute_priv           | enum('N','Y')        | NO   |      | N                 |       |
    | Create_view_priv       | enum('N','Y')        | NO   |      | N                 |       |
    | Show_view_priv         | enum('N','Y')        | NO   |      | N                 |       |
    | Create_routine_priv    | enum('N','Y')        | NO   |      | N                 |       |
    | Alter_routine_priv     | enum('N','Y')        | NO   |      | N                 |       |
    | Index_priv             | enum('N','Y')        | NO   |      | N                 |       |
    | Create_user_priv       | enum('N','Y')        | NO   |      | N                 |       |
    | Event_priv             | enum('N','Y')        | NO   |      | N                 |       |
    | Repl_slave_priv        | enum('N','Y')        | NO   |      | N                 |       |
    | Repl_client_priv       | enum('N','Y')        | NO   |      | N                 |       |
    | Trigger_priv           | enum('N','Y')        | NO   |      | N                 |       |
    | Create_role_priv       | enum('N','Y')        | NO   |      | N                 |       |
    | Drop_role_priv         | enum('N','Y')        | NO   |      | N                 |       |
    | Account_locked         | enum('N','Y')        | NO   |      | N                 |       |
    | Shutdown_priv          | enum('N','Y')        | NO   |      | N                 |       |
    | Reload_priv            | enum('N','Y')        | NO   |      | N                 |       |
    | FILE_priv              | enum('N','Y')        | NO   |      | N                 |       |
    | Config_priv            | enum('N','Y')        | NO   |      | N                 |       |
    | Create_Tablespace_Priv | enum('N','Y')        | NO   |      | N                 |       |
    | Password_reuse_history | smallint(5) unsigned | YES  |      | NULL              |       |
    | Password_reuse_time    | smallint(5) unsigned | YES  |      | NULL              |       |
    | User_attributes        | json                 | YES  |      | NULL              |       |
    | Token_issuer           | varchar(255)         | YES  |      | NULL              |       |
    | Password_expired       | enum('N','Y')        | NO   |      | N                 |       |
    | Password_last_changed  | timestamp            | YES  |      | CURRENT_TIMESTAMP |       |
    | Password_lifetime      | smallint(5) unsigned | YES  |      | NULL              |       |
    +------------------------+----------------------+------+------+-------------------+-------+
    44 rows in set (0.00 sec)

`mysql.user`テーブルには、次の 3 つのグループに分類できる複数のフィールドが含まれています。

<CustomContent platform="tidb">

-   範囲：
    -   `Host` : TiDB アカウントのホスト名を指定します。
    -   `User` : TiDB アカウントのユーザー名を指定します。

-   特権：

    `_priv`または`_Priv`で終わるフィールドは、ユーザー アカウントに付与される権限を定義します。たとえば、 `Select_priv` 、ユーザーがグローバル`Select`権限を持っていることを意味します。詳細については、 [TiDB操作に必要な権限](/privilege-management.md#privileges-required-for-tidb-operations)参照してください。

-   Security：
    -   `authentication_string`および`plugin` : `authentication_string`には、ユーザー アカウントの資格情報が保存されます。資格情報は、 `plugin`フィールドで指定された認証プラグインに基づいて解釈されます。
    -   `Account_locked` : ユーザー アカウントがロックされているかどうかを示します。
    -   `Password_reuse_history`と`Password_reuse_time` : [パスワード再利用ポリシー](/password-management.md#password-reuse-policy)に使用されます。
    -   `User_attributes` : ユーザーのコメントとユーザー属性に関する情報を提供します。
    -   `Token_issuer` : [`tidb_auth_token`](/security-compatibility-with-mysql.md#tidb_auth_token)認証プラグインに使用されます。
    -   `Password_expired` 、 `Password_last_changed` 、 `Password_lifetime` : [パスワード有効期限ポリシー](/password-management.md#password-expiration-policy)に使用されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   範囲：
    -   `Host` : TiDB アカウントのホスト名を指定します。
    -   `User` : TiDB アカウントのユーザー名を指定します。

-   特権：

    `_priv`または`_Priv`で終わるフィールドは、ユーザー アカウントに付与される権限を定義します。たとえば、 `Select_priv` 、ユーザーがグローバル`Select`権限を持っていることを意味します。詳細については、 [TiDB操作に必要な権限](https://docs.pingcap.com/tidb/stable/privilege-management#privileges-required-for-tidb-operations)参照してください。

-   Security：
    -   `authentication_string`および`plugin` : `authentication_string`には、ユーザー アカウントの資格情報が保存されます。資格情報は、 `plugin`フィールドで指定された認証プラグインに基づいて解釈されます。
    -   `Account_locked` : ユーザー アカウントがロックされているかどうかを示します。
    -   `Password_reuse_history`と`Password_reuse_time` : [パスワード再利用ポリシー](https://docs.pingcap.com/tidb/stable/password-management#password-reuse-policy)に使用されます。
    -   `User_attributes` : ユーザーのコメントとユーザー属性に関する情報を提供します。
    -   `Token_issuer` : [`tidb_auth_token`](https://docs.pingcap.com/tidb/stable/security-compatibility-with-mysql#tidb_auth_token)認証プラグインに使用されます。
    -   `Password_expired` 、 `Password_last_changed` 、 `Password_lifetime` : [パスワード有効期限ポリシー](https://docs.pingcap.com/tidb/stable/password-management#password-expiration-policy)に使用されます。

</CustomContent>

TiDB `mysql.user`テーブルのフィールドのほとんどは MySQL `mysql.user`テーブルにも存在しますが、 `Token_issuer`フィールドは TiDB に固有です。
