---
title: TiDB User Account Management
summary: TiDB ユーザー アカウントを管理する方法を学習します。
---

# TiDB ユーザーアカウント管理 {#tidb-user-account-management}

This document describes how to manage a TiDB user account.

## ユーザー名とパスワード {#user-names-and-passwords}

TiDBは、ユーザーアカウントをシステムテーブル[`mysql.user`](/mysql-schema/mysql-schema-user.md)に格納します。各アカウントはユーザー名とクライアントホストによって識別されます。各アカウントにはパスワードが設定されている場合があります。

MySQLクライアントを使用してTiDBサーバーに接続し、指定されたアカウントとパスワードでログインできます。ユーザー名は32文字以内である必要があります。

```shell
mysql --port 4000 --user xxx --password
```

または、コマンドラインパラメータの省略形を使用します。

```shell
mysql -P 4000 -u xxx -p
```

## ユーザーアカウントを追加する {#add-user-accounts}

You can create TiDB accounts in two ways:

-   アカウントを作成して権限を確立するための標準のアカウント管理 SQL ステートメント ( [`CREATE USER`](/sql-statements/sql-statement-create-user.md)や[`GRANT`](/sql-statements/sql-statement-grant-privileges.md)など) を使用します。
-   [`INSERT`](/sql-statements/sql-statement-insert.md)などのステートメントを使用して権限テーブルを直接操作し、 [`DELETE`](/sql-statements/sql-statement-delete.md) [`FLUSH PRIVILEGES`](/sql-statements/sql-statement-flush-privileges.md)実行します。この方法で[`UPDATE`](/sql-statements/sql-statement-update.md)更新が不完全になる可能性があるため、アカウントの作成または変更にはこの方法を使用しないことをお勧めします。

[サードパーティのGUIツール](/develop/dev-guide-third-party-support.md#gui)使用してアカウントを作成することもできます。

```sql
CREATE USER [IF NOT EXISTS] user [IDENTIFIED BY 'auth_string'];
```

パスワードを割り当てると、TiDB は`auth_string`ハッシュして[`mysql.user`](/mysql-schema/mysql-schema-user.md)テーブルに保存します。

```sql
CREATE USER 'test'@'127.0.0.1' IDENTIFIED BY 'xxx';
```

TiDBアカウント名はユーザー名とホスト名で構成されます。アカウント名の構文は「user_name@host_name」です。

-   `user_name`は大文字と小文字が区別されます。

-   `host_name`はホスト名またはIPアドレスで、ワイルドカード`%`または`_`サポートします。例えば、ホスト名`'%'`すべてのホストに一致し、ホスト名`'192.168.1.%'`サブネット内のすべてのホストに一致します。

ホストはあいまい一致をサポートします:

```sql
CREATE USER 'test'@'192.168.10.%';
```

`test`ユーザーは、 `192.168.10`サブネット上の任意のホストからログインできます。

ホストが指定されていない場合、ユーザーはどのIPアドレスからでもログインできます。パスワードが指定されていない場合、デフォルトは空のパスワードです。

```sql
CREATE USER 'test';
```

以下と同等:

```sql
CREATE USER 'test'@'%' IDENTIFIED BY '';
```

指定されたユーザーが存在しない場合、ユーザーの自動作成の動作は[`sql_mode`](/system-variables.md#sql_mode)に依存します。 `sql_mode`に`NO_AUTO_CREATE_USER`含まれる場合、 `GRANT`ステートメントはユーザーを作成せず、エラーが返されます。

For example, assume that the `sql_mode` does not include `NO_AUTO_CREATE_USER`, and you use the following `CREATE USER` and `GRANT` statements to create four accounts:

```sql
CREATE USER 'finley'@'localhost' IDENTIFIED BY 'some_pass';
```

```sql
GRANT ALL PRIVILEGES ON *.* TO 'finley'@'localhost' WITH GRANT OPTION;
```

```sql
CREATE USER 'finley'@'%' IDENTIFIED BY 'some_pass';
```

```sql
GRANT ALL PRIVILEGES ON *.* TO 'finley'@'%' WITH GRANT OPTION;
```

```sql
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin_pass';
```

```sql
GRANT RELOAD,PROCESS ON *.* TO 'admin'@'localhost';
```

```sql
CREATE USER 'dummy'@'localhost';
```

アカウントに付与された権限を確認するには、次の[`SHOW GRANTS`](/sql-statements/sql-statement-show-grants.md)ステートメントを使用します。

```sql
SHOW GRANTS FOR 'admin'@'localhost';
```

    +-----------------------------------------------------+
    | Grants for admin@localhost                          |
    +-----------------------------------------------------+
    | GRANT RELOAD, PROCESS ON *.* TO 'admin'@'localhost' |
    +-----------------------------------------------------+

To see the account definition for an account, use the [`SHOW CREATE USER`](/sql-statements/sql-statement-show-create-user.md) statement:

```sql
SHOW CREATE USER 'admin'@'localhost';
```

    +--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | CREATE USER for admin@localhost                                                                                                                                                                                                      |
    +--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | CREATE USER 'admin'@'localhost' IDENTIFIED WITH 'mysql_native_password' AS '*14E65567ABDB5135D0CFD9A70B3032C179A49EE7' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK PASSWORD HISTORY DEFAULT PASSWORD REUSE INTERVAL DEFAULT  |
    +--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    1 row in set (0.00 sec)

## ユーザーアカウントを削除する {#remove-user-accounts}

ユーザー アカウントを削除するには、次[`DROP USER`](/sql-statements/sql-statement-drop-user.md)ステートメントを使用します。

```sql
DROP USER 'test'@'localhost';
```

この操作により、 [`mysql.user`](/mysql-schema/mysql-schema-user.md)テーブル内のユーザーのレコードと権限テーブル内の関連レコードがクリアされます。

## 予約済みユーザーアカウント {#reserved-user-accounts}

TiDB は、データベースの初期化中に`'root'@'%'`デフォルト アカウントを作成します。

## アカウントのリソース制限を設定する {#set-account-resource-limits}

TiDBは、リソースグループを使用してユーザーが消費するリソースを制限できます。詳細については、 [リソース制御を使用してリソースグループの制限とフロー制御を実現する](/tidb-resource-control-ru-groups.md)参照してください。

## アカウントパスワードの割り当て {#assign-account-passwords}

TiDBはパスワードを[`mysql.user`](/mysql-schema/mysql-schema-user.md)システムテーブルに保存します。パスワードの割り当てまたは更新操作は、 `CREATE USER`権限、または`mysql`データベース権限（新規アカウント作成の`INSERT`権限、既存アカウント更新の`UPDATE`権限）を持つユーザーのみに許可されます。

-   新しいアカウントを作成するときにパスワードを割り当てるには、 [`CREATE USER`](/sql-statements/sql-statement-create-user.md)使用し、 `IDENTIFIED BY`句を含めます。

    ```sql
    CREATE USER 'test'@'localhost' IDENTIFIED BY 'mypass';
    ```

-   To assign or change a password for an existing account, use [`SET PASSWORD FOR`](/sql-statements/sql-statement-set-password.md) or [`ALTER USER`](/sql-statements/sql-statement-alter-user.md):

    ```sql
    SET PASSWORD FOR 'root'@'%' = 'xxx';
    ```

    または：

    ```sql
    ALTER USER 'test'@'localhost' IDENTIFIED BY 'mypass';
    ```

## <code>root</code>パスワードを忘れた {#forget-the-code-root-code-password}

1.  設定ファイルを変更します。

    1.  tidb-server インスタンスの 1 つが配置されているマシンにログインします。
    2.  TiDB ノードのデプロイメント ディレクトリの下の`conf`ディレクトリに入り、 `tidb.toml`構成ファイルを見つけます。
    3.  設定ファイルの[`security`](/tidb-configuration-file.md#security)セクションに設定項目[`skip-grant-table`](/tidb-configuration-file.md)追加します。5 `security`がない場合は、 `tidb.toml`設定ファイルの末尾に次の2行を追加します。

            [security]
            skip-grant-table = true

2.  tidb-server プロセスを停止します。

    1.  tidb-server プロセスをビュー。

        ```bash
        ps aux | grep tidb-server
        ```

    2.  tidb-server に対応するプロセス ID (PID) を見つけて、 `kill`コマンドを使用してプロセスを停止します。

        ```bash
        kill -9 <pid>
        ```

3.  変更した構成を使用して TiDB を起動します。

    > **注記：**
    >
    > TiDBプロセスを開始する前に`skip-grant-table`設定すると、オペレーティングシステムのユーザーチェックが開始されます。オペレーティングシステムの`root`ユーザーのみがTiDBプロセスを開始できます。

    1.  TiDB ノードのデプロイメント ディレクトリの下の`scripts`ディレクトリを入力します。
    2.  Switch to the `root` account of the operating system.
    3.  ディレクトリ内の`run_tidb.sh`スクリプトをフォアグラウンドで実行します。
    4.  新しいターミナル ウィンドウで`root`としてログインし、パスワードを変更します。

        ```bash
        mysql -h 127.0.0.1 -P 4000 -u root
        ```

4.  `run_tidb.sh`スクリプトの実行を停止し、手順 1 で TiDB 構成ファイルに追加された内容を削除し、tidb-server が自動的に起動するのを待ちます。

## <code>FLUSH PRIVILEGES</code> {#code-flush-privileges-code}

ユーザーと権限に関する情報はTiKVサーバーに保存され、TiDBはこれらの情報をプロセス内にキャッシュします。通常、 [`CREATE USER`](/sql-statements/sql-statement-create-user.md) 、その他[`GRANT`](/sql-statements/sql-statement-grant-privileges.md)ステートメントによる関連情報の変更は、クラスター全体に迅速に反映されます。一時的なネットワーク利用不可などの要因によって操作が影響を受ける場合、TiDBは定期的にキャッシュ情報を再読み込みするため、変更は約15分後に反映されます。

権限テーブルを直接変更した場合は、 [`FLUSH PRIVILEGES`](/sql-statements/sql-statement-flush-privileges.md)実行して変更をすぐに適用します。

詳細は[権限管理](/privilege-management.md)参照。
