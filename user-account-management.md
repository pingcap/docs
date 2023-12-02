---
title: TiDB User Account Management
summary: Learn how to manage a TiDB user account.
---

# TiDB ユーザーアカウント管理 {#tidb-user-account-management}

このドキュメントでは、TiDB ユーザー アカウントの管理方法について説明します。

## ユーザー名とパスワード {#user-names-and-passwords}

TiDB はユーザー アカウントを`mysql.user`システム データベースのテーブルに保存します。各アカウントはユーザー名とクライアント ホストによって識別されます。各アカウントにはパスワードがある場合があります。

MySQL クライアントを使用して TiDBサーバーに接続し、指定されたアカウントとパスワードを使用してログインできます。各ユーザー名が 32 文字以内であることを確認してください。

```shell
mysql --port 4000 --user xxx --password
```

または、コマンド ライン パラメーターの省略形を使用します。

```shell
mysql -P 4000 -u xxx -p
```

## ユーザーアカウントを追加する {#add-user-accounts}

TiDB アカウントは 2 つの方法で作成できます。

-   アカウントの作成とその権限の確立を目的とした標準のアカウント管理 SQL ステートメント ( `CREATE USER`や`GRANT`など) を使用します。
-   `INSERT` 、 `UPDATE` 、または`DELETE`などのステートメントを使用して権限テーブルを直接操作します。更新が不完全になる可能性があるため、この方法を使用してアカウントを作成することはお勧めできません。

サードパーティの GUI ツールを使用してアカウントを作成することもできます。

```sql
CREATE USER [IF NOT EXISTS] user [IDENTIFIED BY 'auth_string'];
```

パスワードを割り当てると、TiDB は`auth_string`暗号化して`mysql.user`テーブルに保存します。

```sql
CREATE USER 'test'@'127.0.0.1' IDENTIFIED BY 'xxx';
```

TiDB アカウントの名前は、ユーザー名とホスト名で構成されます。アカウント名の構文は、「user_name」@「host_name」です。

-   `user_name`では大文字と小文字が区別されます。

-   `host_name`はホスト名または IP アドレスで、ワイルドカード`%`または`_`をサポートします。たとえば、ホスト名`'%'`サブネット内のすべてのホストに一致し、ホスト名`'192.168.1.%'`サブネット内のすべてのホストに一致します。

ホストはあいまい一致をサポートしています。

```sql
CREATE USER 'test'@'192.168.10.%';
```

`test`人のユーザーは、 `192.168.10`サブネット上の任意のホストからログインできます。

ホストが指定されていない場合、ユーザーは任意の IP からのログインが許可されます。パスワードが指定されていない場合、デフォルトは空のパスワードです。

```sql
CREATE USER 'test';
```

に相当：

```sql
CREATE USER 'test'@'%' IDENTIFIED BY '';
```

指定されたユーザーが存在しない場合、ユーザーを自動的に作成する動作は`sql_mode`に依存します。 `sql_mode`に`NO_AUTO_CREATE_USER`が含まれる場合、 `GRANT`ステートメントはユーザーを作成せず、エラーが返されます。

たとえば、 `sql_mode`は`NO_AUTO_CREATE_USER`含まれておらず、次の`CREATE USER`および`GRANT`ステートメントを使用して 4 つのアカウントを作成するとします。

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

アカウントに付与された権限を確認するには、 `SHOW GRANTS`ステートメントを使用します。

```sql
SHOW GRANTS FOR 'admin'@'localhost';
```

    +-----------------------------------------------------+
    | Grants for admin@localhost                          |
    +-----------------------------------------------------+
    | GRANT RELOAD, PROCESS ON *.* TO 'admin'@'localhost' |
    +-----------------------------------------------------+

## ユーザーアカウントを削除する {#remove-user-accounts}

ユーザー アカウントを削除するには、 `DROP USER`ステートメントを使用します。

```sql
DROP USER 'test'@'localhost';
```

この操作により、 `mysql.user`テーブル内のユーザーのレコードと権限テーブル内の関連レコードがクリアされます。

## 予約済みユーザーアカウント {#reserved-user-accounts}

TiDB は、データベースの初期化中に`'root'@'%'`デフォルト アカウントを作成します。

## アカウントのリソース制限を設定する {#set-account-resource-limits}

現在、TiDB はアカウントのリソース制限の設定をサポートしていません。

## アカウントのパスワードを割り当てる {#assign-account-passwords}

TiDB はパスワードを`mysql.user`システム データベースに保存します。パスワードを割り当てるまたは更新する操作は、 `CREATE USER`権限、または`mysql`データベースに対する権限(新しいアカウントを作成する`INSERT`権限、既存のアカウントを更新する`UPDATE`権限) を持つユーザーにのみ許可されます。

-   新しいアカウントの作成時にパスワードを割り当てるには、 `CREATE USER`を使用し、 `IDENTIFIED BY`句を含めます。

    ```sql
    CREATE USER 'test'@'localhost' IDENTIFIED BY 'mypass';
    ```

-   既存のアカウントのパスワードを割り当てるか変更するには、 `SET PASSWORD FOR`または`ALTER USER`を使用します。

    ```sql
    SET PASSWORD FOR 'root'@'%' = 'xxx';
    ```

    または：

    ```sql
    ALTER USER 'test'@'localhost' IDENTIFIED BY 'mypass';
    ```

## <code>root</code>パスワードを忘れた場合 {#forget-the-code-root-code-password}

1.  構成ファイルを変更します。

    1.  tidb-server インスタンスの 1 つが配置されているマシンにログインします。
    2.  TiDB ノード展開ディレクトリの下の`conf`ディレクトリに入り、 `tidb.toml`構成ファイルを見つけます。
    3.  構成ファイルの`security`セクションに構成項目`skip-grant-table`を追加します。 `security`セクションがない場合は、次の 2 行を tidb.toml 構成ファイルの最後に追加します。

            [security]
            skip-grant-table = true

2.  tidb-server プロセスを停止します。

    1.  tidb-server プロセスをビュー。

        ```bash
        ps aux | grep tidb-server
        ```

    2.  tidb-server に対応するプロセス ID (PID) を見つけ、 `kill`コマンドを使用してプロセスを停止します。

        ```bash
        kill -9 <pid>
        ```

3.  変更した構成を使用して TiDB を起動します。

    > **注記：**
    >
    > TiDB プロセスを開始する前に`skip-grant-table`を設定すると、オペレーティング システム ユーザーのチェックが開始されます。オペレーティング システムの`root`ユーザーのみが TiDB プロセスを開始できます。

    1.  TiDB ノード展開ディレクトリの下にある`scripts`ディレクトリを入力します。
    2.  オペレーティング システムの`root`アカウントに切り替えます。
    3.  フォアグラウンドのディレクトリで`run_tidb.sh`スクリプトを実行します。
    4.  新しいターミナル ウィンドウに`root`としてログインし、パスワードを変更します。

        ```bash
        mysql -h 127.0.0.1 -P 4000 -u root
        ```

4.  `run_tidb.sh`スクリプトの実行を停止し、ステップ 1 で TiDB 構成ファイルに追加した内容を削除し、tidb-server が自動的に起動するまで待ちます。

## <code>FLUSH PRIVILEGES</code> {#code-flush-privileges-code}

ユーザーと権限に関連する情報は TiKVサーバーに保存され、TiDB はこの情報をプロセス内にキャッシュします。一般に、 `CREATE USER` 、 `GRANT` 、およびその他のステートメントによる関連情報の変更は、クラスター全体ですぐに有効になります。ネットワークが一時的に利用できないなどの何らかの要因によって操作が影響を受けた場合、TiDB はキャッシュ情報を定期的に再ロードするため、変更は約 15 分で有効になります。

権限テーブルを直接変更した場合は、次のコマンドを実行して変更をすぐに適用します。

```sql
FLUSH PRIVILEGES;
```

詳細は[権限管理](/privilege-management.md)を参照してください。
