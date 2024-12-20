---
title: TiDB User Account Management
summary: TiDB ユーザー アカウントを管理する方法を学習します。
---

# TiDB ユーザーアカウント管理 {#tidb-user-account-management}

このドキュメントでは、TiDB ユーザー アカウントを管理する方法について説明します。

## ユーザー名とパスワード {#user-names-and-passwords}

TiDB は、ユーザー アカウントを[`mysql.user`](/mysql-schema/mysql-schema-user.md)システム テーブルのテーブルに保存します。各アカウントは、ユーザー名とクライアント ホストによって識別されます。各アカウントにはパスワードがある場合があります。

MySQL クライアントを使用して TiDBサーバーに接続し、指定されたアカウントとパスワードを使用してログインできます。各ユーザー名は、32 文字以下であることを確認してください。

```shell
mysql --port 4000 --user xxx --password
```

または、コマンドラインパラメータの省略形を使用します。

```shell
mysql -P 4000 -u xxx -p
```

## ユーザーアカウントを追加する {#add-user-accounts}

TiDB アカウントは次の 2 つの方法で作成できます。

-   [`CREATE USER`](/sql-statements/sql-statement-create-user.md)や[`GRANT`](/sql-statements/sql-statement-grant-privileges.md)など、アカウントを作成して権限を確立するための標準のアカウント管理 SQL ステートメントを使用します。
-   [`INSERT`](/sql-statements/sql-statement-insert.md) 、 [`UPDATE`](/sql-statements/sql-statement-update.md) 、 [`DELETE`](/sql-statements/sql-statement-delete.md)などのステートメントを使用して権限テーブルを直接操作し、 [`FLUSH PRIVILEGES`](/sql-statements/sql-statement-flush-privileges.md)実行します。この方法では更新が不完全になる可能性があるため、アカウントの作成または変更にはこの方法を使用しないことをお勧めします。

[サードパーティのGUIツール](/develop/dev-guide-third-party-support.md#gui)使用してアカウントを作成することもできます。

```sql
CREATE USER [IF NOT EXISTS] user [IDENTIFIED BY 'auth_string'];
```

パスワードを割り当てると、TiDB は`auth_string`をハッシュして[`mysql.user`](/mysql-schema/mysql-schema-user.md)テーブルに保存します。

```sql
CREATE USER 'test'@'127.0.0.1' IDENTIFIED BY 'xxx';
```

TiDB アカウントの名前は、ユーザー名とホスト名で構成されます。アカウント名の構文は、「user_name」@「host_name」です。

-   `user_name`大文字と小文字が区別されます。

-   `host_name`はホスト名または IP アドレスであり、ワイルドカード`%`または`_`サポートします。たとえば、ホスト名`'%'`すべてのホストに一致し、ホスト名`'192.168.1.%'`サブネット内のすべてのホストに一致します。

ホストはファジーマッチングをサポートしています:

```sql
CREATE USER 'test'@'192.168.10.%';
```

`test`ユーザーは、 `192.168.10`サブネット上の任意のホストからログインできます。

ホストが指定されていない場合、ユーザーはどの IP からでもログインできます。パスワードが指定されていない場合、デフォルトは空のパスワードです。

```sql
CREATE USER 'test';
```

以下と同等:

```sql
CREATE USER 'test'@'%' IDENTIFIED BY '';
```

指定されたユーザーが存在しない場合、ユーザーを自動的に作成する動作は[`sql_mode`](/system-variables.md#sql_mode)によって異なります。 `sql_mode`に`NO_AUTO_CREATE_USER`含まれている場合、 `GRANT`ステートメントはユーザーを作成せず、エラーが返されます。

たとえば、 `sql_mode`に`NO_AUTO_CREATE_USER`含まれず、次の`CREATE USER`と`GRANT`ステートメントを使用して 4 つのアカウントを作成するとします。

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

アカウントのアカウント定義を表示するには、次の[`SHOW CREATE USER`](/sql-statements/sql-statement-show-create-user.md)ステートメントを使用します。

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

ユーザー アカウントを削除するには、次の[`DROP USER`](/sql-statements/sql-statement-drop-user.md)ステートメントを使用します。

```sql
DROP USER 'test'@'localhost';
```

この操作により、 [`mysql.user`](/mysql-schema/mysql-schema-user.md)テーブル内のユーザーのレコードと権限テーブル内の関連レコードがクリアされます。

## 予約済みユーザーアカウント {#reserved-user-accounts}

TiDB は、データベースの初期化中に`'root'@'%'`デフォルト アカウントを作成します。

## アカウントのリソース制限を設定する {#set-account-resource-limits}

TiDB は、リソース グループを使用してユーザーが消費するリソースを制限できます。詳細については、 [リソース制御を使用してリソースの分離を実現する](/tidb-resource-control.md)参照してください。

## アカウントパスワードの割り当て {#assign-account-passwords}

TiDB は、パスワードを[`mysql.user`](/mysql-schema/mysql-schema-user.md)システム テーブルに保存します。パスワードの割り当てまたは更新の操作は、 `CREATE USER`権限、または`mysql`データベースの権限(新しいアカウントを作成する`INSERT`権限、既存のアカウントを更新する`UPDATE`権限) を持つユーザーのみに許可されます。

-   新しいアカウントを作成するときにパスワードを割り当てるには、 [`CREATE USER`](/sql-statements/sql-statement-create-user.md)使用し、 `IDENTIFIED BY`句を含めます。

    ```sql
    CREATE USER 'test'@'localhost' IDENTIFIED BY 'mypass';
    ```

-   既存のアカウントのパスワードを割り当てたり変更したりするには、 [`SET PASSWORD FOR`](/sql-statements/sql-statement-set-password.md)または[`ALTER USER`](/sql-statements/sql-statement-alter-user.md)使用します。

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
    3.  構成ファイルの[`security`](/tidb-configuration-file.md#security)セクションに設定項目[`skip-grant-table`](/tidb-configuration-file.md)を追加します。 `security`セクションがない場合は、 `tidb.toml`構成ファイルの末尾に次の 2 行を追加します。

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
    > TiDB プロセスを開始する前に`skip-grant-table`設定すると、オペレーティング システム ユーザーのチェックが開始されます。オペレーティング システムの`root`ユーザーのみが TiDB プロセスを開始できます。

    1.  TiDB ノードのデプロイメント ディレクトリの下の`scripts`ディレクトリを入力します。
    2.  オペレーティング システムの`root`アカウントに切り替えます。
    3.  ディレクトリ内の`run_tidb.sh`スクリプトをフォアグラウンドで実行します。
    4.  新しいターミナル ウィンドウで`root`としてログインし、パスワードを変更します。

        ```bash
        mysql -h 127.0.0.1 -P 4000 -u root
        ```

4.  `run_tidb.sh`スクリプトの実行を停止し、手順 1 で TiDB 構成ファイルに追加されたコンテンツを削除し、tidb-server が自動的に起動するのを待ちます。

## <code>FLUSH PRIVILEGES</code> {#code-flush-privileges-code}

ユーザーや権限に関する情報は TiKVサーバーに保存され、TiDB はプロセス内にこの情報をキャッシュします。通常、 [`CREATE USER`](/sql-statements/sql-statement-create-user.md)などのステートメントによる関連情報の[`GRANT`](/sql-statements/sql-statement-grant-privileges.md)は、クラスター全体にすぐに反映されます。一時的にネットワークが利用できなくなるなどの要因によって操作が影響を受ける場合は、TiDB が定期的にキャッシュ情報を再読み込みするため、変更は約 15 分後に反映されます。

権限テーブルを直接変更した場合は、 [`FLUSH PRIVILEGES`](/sql-statements/sql-statement-flush-privileges.md)を実行して変更をすぐに適用します。

詳細は[権限管理](/privilege-management.md)参照。
