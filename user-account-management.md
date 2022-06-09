---
title: TiDB User Account Management
summary: Learn how to manage a TiDB user account.
---

# TiDBユーザーアカウント管理 {#tidb-user-account-management}

このドキュメントでは、TiDBユーザーアカウントを管理する方法について説明します。

## ユーザー名とパスワード {#user-names-and-passwords}

TiDBは、ユーザーアカウントを`mysql.user`のシステムデータベースのテーブルに保存します。各アカウントは、ユーザー名とクライアントホストによって識別されます。各アカウントにはパスワードがあります。

MySQLクライアントを使用してTiDBサーバーに接続し、指定されたアカウントとパスワードを使用してログインできます。

```sql
shell> mysql --port 4000 --user xxx --password
```

または、コマンドラインパラメータの略語を使用します。

```sql
shell> mysql -P 4000 -u xxx -p
```

## ユーザーアカウントを追加する {#add-user-accounts}

TiDBアカウントは、次の2つの方法で作成できます。

-   アカウントを作成し、 `CREATE USER`や`GRANT`などの特権を確立することを目的とした標準のアカウント管理SQLステートメントを使用する。
-   `INSERT`などの`UPDATE`を使用して`DELETE`テーブルを直接操作する。

特権テーブルを直接操作すると更新が不完全になる可能性があるため、アカウント管理ステートメントを使用することをお勧めします。サードパーティのGUIツールを使用してアカウントを作成することもできます。

{{< copyable "" >}}

```sql
CREATE USER [IF NOT EXISTS] user [IDENTIFIED BY 'auth_string'];
```

パスワードを割り当てた後、TiDBは`auth_string`を暗号化して`mysql.user`テーブルに保存します。

{{< copyable "" >}}

```sql
CREATE USER 'test'@'127.0.0.1' IDENTIFIED BY 'xxx';
```

TiDBアカウントの名前は、ユーザー名とホスト名で構成されます。アカウント名の構文は「user_name」@「host_name」です。

-   `user_name`では大文字と小文字が区別されます。

-   `host_name`は、ワイルドカード`%`または`_`をサポートするホスト名またはIPアドレスです。たとえば、ホスト名`'%'`はすべてのホストと一致し、ホスト名`'192.168.1.%'`はサブネット内のすべてのホストと一致します。

ホストはあいまいマッチングをサポートしています。

{{< copyable "" >}}

```sql
CREATE USER 'test'@'192.168.10.%';
```

`test`人のユーザーは、 `192.168.10`のサブネット上の任意のホストからログインできます。

ホストが指定されていない場合、ユーザーは任意のIPからログインできます。パスワードが指定されていない場合、デフォルトは空のパスワードです。

{{< copyable "" >}}

```sql
CREATE USER 'test';
```

に相当：

{{< copyable "" >}}

```sql
CREATE USER 'test'@'%' IDENTIFIED BY '';
```

指定されたユーザーが存在しない場合、ユーザーを自動的に作成する動作は`sql_mode`に依存します。 `sql_mode`に`NO_AUTO_CREATE_USER`が含まれている場合、 `GRANT`ステートメントはエラーが返されたユーザーを作成しません。

たとえば、 `sql_mode`に`NO_AUTO_CREATE_USER`が含まれておらず、次の`CREATE USER`および`GRANT`ステートメントを使用して4つのアカウントを作成するとします。

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

アカウントに付与されている権限を確認するには、次の`SHOW GRANTS`のステートメントを使用します。

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

## ユーザーアカウントを削除する {#remove-user-accounts}

ユーザーアカウントを削除するには、次の`DROP USER`のステートメントを使用します。

{{< copyable "" >}}

```sql
DROP USER 'test'@'localhost';
```

この操作により、 `mysql.user`テーブルのユーザーのレコードと特権テーブルの関連レコードがクリアされます。

## 予約済みのユーザーアカウント {#reserved-user-accounts}

TiDBは、データベースの初期化中に`'root'@'%'`のデフォルトアカウントを作成します。

## アカウントのリソース制限を設定する {#set-account-resource-limits}

現在、TiDBはアカウントリソース制限の設定をサポートしていません。

## アカウントのパスワードを割り当てる {#assign-account-passwords}

TiDBは、 `mysql.user`のシステムデータベースにパスワードを保存します。パスワードを割り当てまたは更新する操作は、 `CREATE USER`の特権、または`mysql`のデータベースに対する特権（新しいアカウントを作成するための`INSERT`の特権、既存のアカウントを更新するための`UPDATE`の特権）を持つユーザーにのみ許可されます。

-   新しいアカウントを作成するときにパスワードを割り当てるには、 `CREATE USER`を使用し、 `IDENTIFIED BY`句を含めます。

    ```sql
    CREATE USER 'test'@'localhost' IDENTIFIED BY 'mypass';
    ```

-   既存のアカウントのパスワードを割り当てたり変更したりするには、 `SET PASSWORD FOR`または`ALTER USER`を使用します。

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

2.  構成を変更してTiDBを起動します。 `root`を使用してログインし、パスワードを変更します。

    ```bash
    mysql -h 127.0.0.1 -P 4000 -u root
    ```

`skip-grant-table`が設定されている場合、TiDBプロセスを開始すると、ユーザーがオペレーティングシステムの管理者であるかどうかが確認され、オペレーティングシステムの`root`のユーザーのみがTiDBプロセスを開始できます。

## <code>FLUSH PRIVILEGES</code> {#code-flush-privileges-code}

ユーザーと特権に関連する情報はTiKVサーバーに保存され、TiDBはこの情報をプロセス内にキャッシュします。一般に、 `CREATE USER` 、およびその他のステートメントによる関連情報の変更は、クラスタ全体で迅速に有効になり`GRANT` 。一時的に利用できないネットワークなどの要因により運用が影響を受ける場合、TiDBは定期的にキャッシュ情報をリロードするため、変更は約15分で有効になります。

特権テーブルを直接変更した場合は、次のコマンドを実行して変更をすぐに適用します。

```sql
FLUSH PRIVILEGES;
```

詳細については、 [権限管理](/privilege-management.md)を参照してください。
