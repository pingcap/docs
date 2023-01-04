---
title: TiDB User Account Management
summary: Learn how to manage a TiDB user account.
---

# TiDB ユーザー アカウント管理 {#tidb-user-account-management}

このドキュメントでは、TiDB ユーザー アカウントを管理する方法について説明します。

## ユーザー名とパスワード {#user-names-and-passwords}

TiDB は、ユーザー アカウントを`mysql.user`システム データベースのテーブルに格納します。各アカウントは、ユーザー名とクライアント ホストによって識別されます。各アカウントにはパスワードが設定されている場合があります。

MySQL クライアントを使用して TiDBサーバーに接続し、指定したアカウントとパスワードを使用してログインできます。各ユーザー名は、32 文字以内である必要があります。

```shell
mysql --port 4000 --user xxx --password
```

または、コマンド ライン パラメータの省略形を使用します。

```shell
mysql -P 4000 -u xxx -p
```

## ユーザー アカウントを追加する {#add-user-accounts}

TiDB アカウントは次の 2 つの方法で作成できます。

-   `CREATE USER`や`GRANT`など、アカウントの作成と権限の確立を目的とした標準のアカウント管理 SQL ステートメントを使用する。
-   `INSERT` 、 `UPDATE` 、または`DELETE`などのステートメントを使用して特権テーブルを直接操作する。この方法を使用してアカウントを作成することはお勧めしません。更新が不完全になる可能性があるためです。

サードパーティの GUI ツールを使用してアカウントを作成することもできます。

{{< copyable "" >}}

```sql
CREATE USER [IF NOT EXISTS] user [IDENTIFIED BY 'auth_string'];
```

パスワードを割り当てた後、TiDB は`auth_string`を暗号化して`mysql.user`テーブルに格納します。

{{< copyable "" >}}

```sql
CREATE USER 'test'@'127.0.0.1' IDENTIFIED BY 'xxx';
```

TiDB アカウントの名前は、ユーザー名とホスト名で構成されます。アカウント名の構文は、&#39;user_name&#39;@&#39;host_name&#39; です。

-   `user_name`は大文字と小文字が区別されます。

-   `host_name`は、ワイルドカード`%`または`_`をサポートするホスト名または IP アドレスです。たとえば、ホスト名`'%'`はすべてのホストに一致し、ホスト名`'192.168.1.%'`はサブネット内のすべてのホストに一致します。

ホストはあいまい一致をサポートしています。

{{< copyable "" >}}

```sql
CREATE USER 'test'@'192.168.10.%';
```

`test`ユーザーは、 `192.168.10`サブネット上の任意のホストからログインできます。

ホストが指定されていない場合、ユーザーは任意の IP からログインできます。パスワードが指定されていない場合、デフォルトは空のパスワードです。

{{< copyable "" >}}

```sql
CREATE USER 'test';
```

に相当：

{{< copyable "" >}}

```sql
CREATE USER 'test'@'%' IDENTIFIED BY '';
```

指定されたユーザーが存在しない場合、ユーザーの自動作成の動作は`sql_mode`に依存します。 `sql_mode`に`NO_AUTO_CREATE_USER`が含まれている場合、 `GRANT`ステートメントはユーザーを作成せず、エラーが返されます。

たとえば、 `sql_mode`に`NO_AUTO_CREATE_USER`が含まれず、次の`CREATE USER`および`GRANT`ステートメントを使用して 4 つのアカウントを作成するとします。

{{< copyable "" >}}

```sql
CREATE USER 'finley'@'localhost' IDENTIFIED BY 'some_pass';
```

{{< copyable "" >}}

```sql
GRANT ALL PRIVILEGES ON *.* TO 'finley'@'localhost' WITH GRANT OPTION;
```

{{< copyable "" >}}

```sql
CREATE USER 'finley'@'%' IDENTIFIED BY 'some_pass';
```

{{< copyable "" >}}

```sql
GRANT ALL PRIVILEGES ON *.* TO 'finley'@'%' WITH GRANT OPTION;
```

{{< copyable "" >}}

```sql
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin_pass';
```

{{< copyable "" >}}

```sql
GRANT RELOAD,PROCESS ON *.* TO 'admin'@'localhost';
```

{{< copyable "" >}}

```sql
CREATE USER 'dummy'@'localhost';
```

アカウントに付与された権限を確認するには、次の`SHOW GRANTS`ステートメントを使用します。

{{< copyable "" >}}

```sql
SHOW GRANTS FOR 'admin'@'localhost';
```

```
+-----------------------------------------------------+
| Grants for admin@localhost                          |
+-----------------------------------------------------+
| GRANT RELOAD, PROCESS ON *.* TO 'admin'@'localhost' |
+-----------------------------------------------------+
```

## ユーザー アカウントを削除する {#remove-user-accounts}

ユーザー アカウントを削除するには、次の`DROP USER`ステートメントを使用します。

{{< copyable "" >}}

```sql
DROP USER 'test'@'localhost';
```

この操作により、 `mysql.user`テーブル内のユーザーのレコードと権限テーブル内の関連レコードがクリアされます。

## 予約済みユーザー アカウント {#reserved-user-accounts}

TiDB は、データベースの初期化中に`'root'@'%'`のデフォルト アカウントを作成します。

## アカウントのリソース制限を設定する {#set-account-resource-limits}

現在、TiDB はアカウント リソース制限の設定をサポートしていません。

## アカウントのパスワードを割り当てる {#assign-account-passwords}

TiDB はパスワードを`mysql.user`システム データベースに格納します。パスワードを割り当てたり更新したりする操作は、 `CREATE USER`の権限、または`mysql`データベースの権限( `INSERT`の新しいアカウントを作成する権限、 `UPDATE`の既存のアカウントを更新する権限) を持つユーザーにのみ許可されます。

-   新しいアカウントを作成するときにパスワードを割り当てるには、 `CREATE USER`を使用し、 `IDENTIFIED BY`句を含めます。

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

## <code>root</code>パスワードを忘れる {#forget-the-code-root-code-password}

1.  `security`の部分に`skip-grant-table`を追加して、構成ファイルを変更します。

    ```
    [security]
    skip-grant-table = true
    ```

2.  変更した構成で TiDB を起動します。 `root`を使用してログインし、パスワードを変更します。

    ```bash
    mysql -h 127.0.0.1 -P 4000 -u root
    ```

`skip-grant-table`が設定されている場合、TiDB プロセスを開始すると、ユーザーがオペレーティング システムの管理者であるかどうかがチェックされ、オペレーティング システムの`root`ユーザーのみが TiDB プロセスを開始できます。

## <code>FLUSH PRIVILEGES</code> {#code-flush-privileges-code}

ユーザーと権限に関連する情報は TiKVサーバーに保存され、TiDB はこの情報をプロセス内にキャッシュします。一般に、 `CREATE USER` 、 `GRANT` 、およびその他のステートメントによる関連情報の変更は、クラスター全体ですぐに反映されます。ネットワークが一時的に利用できないなどの影響があった場合は、TiDB が定期的にキャッシュ情報をリロードするため、約 15 分で変更が反映されます。

特権テーブルを直接変更した場合は、次のコマンドを実行して変更をすぐに適用します。

```sql
FLUSH PRIVILEGES;
```

詳細については、 [権限管理](/privilege-management.md)を参照してください。
