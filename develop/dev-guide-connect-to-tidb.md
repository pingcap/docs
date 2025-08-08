---
title: Connect to TiDB
summary: TiDB に接続する方法を学習します。
---

# TiDBに接続する {#connect-to-tidb}

TiDBはMySQLプロトコルと高い互換性があります。クライアントリンクパラメータの完全なリストについては、 [MySQLクライアントオプション](https://dev.mysql.com/doc/refman/8.0/en/mysql-command-options.html)参照してください。

TiDB は[MySQL クライアント/サーバー プロトコル](https://dev.mysql.com/doc/dev/mysql-server/latest/PAGE_PROTOCOL.html)サポートしており、これにより、ほとんどのクライアント ドライバーと ORM フレームワークが MySQL に接続するのと同じように TiDB に接続できるようになります。

## MySQL {#mysql}

個人の好みに応じて、MySQL クライアントまたは MySQL シェルの使用を選択できます。

<SimpleTab>

<div label="MySQL Client">

TiDB には、MySQL クライアントを使用して接続できます。MySQL クライアントは、TiDB のコマンドラインツールとして使用できます。MySQL クライアントをインストールするには、YUM ベースの Linux ディストリビューションの以下の手順に従ってください。

```shell
sudo yum install mysql
```

インストール後、次のコマンドを使用して TiDB に接続できます。

```shell
mysql --host <tidb_server_host> --port 4000 -u root -p --comments
```

macOS上のMySQL v9.0クライアントはプラグイン`mysql_native_password`を正しくロードできないため、TiDBへの接続時にエラー`ERROR 2059 (HY000): Authentication plugin 'mysql_native_password' cannot be loaded`発生します。この問題を解決するには、MySQL v8.0クライアントをインストールしてTiDBに接続することをお勧めします。インストールするには、以下のコマンドを実行してください。

```shell
brew install mysql-client@8.0
brew unlink mysql
brew link mysql-client@8.0
```

それでもエラーが発生する場合は、MySQL v8.0クライアントのインストールパスを指定してTiDBに接続してください。以下のコマンドを実行してください。

```shell
/opt/homebrew/opt/mysql-client@8.0/bin/mysql --comments --host ${YOUR_IP_ADDRESS} --port ${YOUR_PORT_NUMBER} -u ${your_user_name} -p
```

上記のコマンドの`/opt/homebrew/opt/mysql-client@8.0/bin/mysql` 、実際の環境の MySQL v8.0 クライアントのインストール パスに置き換えます。

</div>

<div label="MySQL Shell">

TiDB には、MySQL Shell を使用して接続できます。MySQL Shell は、TiDB のコマンドラインツールとして使用できます。MySQL Shell をインストールするには、 [MySQL Shell ドキュメント](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.html)の手順に従ってください。インストール後、以下のコマンドで TiDB に接続できます。

```shell
mysqlsh --sql mysql://root@<tidb_server_host>:4000
```

</div>

</SimpleTab>

## JDBC {#jdbc}

[JDBC](https://dev.mysql.com/doc/connector-j/en/)ドライバを使用して TiDB に接続できます。そのためには、 `MysqlDataSource`または`MysqlConnectionPoolDataSource`オブジェクト（どちらのオブジェクトも`DataSource`インターフェースをサポートしています）を作成し、 `setURL`関数を使用して接続文字列を設定する必要があります。

例えば：

```java
MysqlDataSource mysqlDataSource = new MysqlDataSource();
mysqlDataSource.setURL("jdbc:mysql://{host}:{port}/{database}?user={username}&password={password}");
```

JDBC接続の詳細については、 [JDBCドキュメント](https://dev.mysql.com/doc/connector-j/en/)参照してください。

### 接続パラメータ {#connection-parameters}

|    パラメータ名    |                              説明                             |
| :----------: | :---------------------------------------------------------: |
| `{username}` |                 TiDB クラスターに接続するための SQL ユーザー                 |
| `{password}` |                        SQLユーザーのパスワード                        |
|   `{host}`   | TiDBノードの[ホスト](https://en.wikipedia.org/wiki/Host_(network)) |
|   `{port}`   |                     TiDBノードがリッスンしているポート                     |
| `{database}` |                         既存のデータベースの名前                        |

<CustomContent platform="tidb">

TiDB SQLユーザーの詳細については、 [TiDB ユーザーアカウント管理](/user-account-management.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB SQLユーザーの詳細については、 [TiDB ユーザーアカウント管理](https://docs.pingcap.com/tidb/stable/user-account-management)参照してください。

</CustomContent>

## 休止状態 {#hibernate}

[ハイバネートORM](https://hibernate.org/orm/)使用して TiDB に接続できます。そのためには、Hibernate 設定ファイルで`hibernate.connection.url`有効な TiDB 接続文字列に設定する必要があります。

たとえば、 `hibernate.cfg.xml`構成ファイルを使用する場合は、 `hibernate.connection.url`次のように設定します。

```xml
<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE hibernate-configuration PUBLIC
        "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
        "http://www.hibernate.org/dtd/hibernate-configuration-3.0.dtd">
<hibernate-configuration>
    <session-factory>
        <property name="hibernate.connection.driver_class">com.mysql.cj.jdbc.Driver</property>
        <property name="hibernate.dialect">org.hibernate.dialect.TiDBDialect</property>
        <property name="hibernate.connection.url">jdbc:mysql://{host}:{port}/{database}?user={user}&amp;password={password}</property>
    </session-factory>
</hibernate-configuration>
```

設定が完了したら、次のコマンドを使用して設定ファイルを読み取り、 `SessionFactory`オブジェクトを取得できます。

```java
SessionFactory sessionFactory = new Configuration().configure("hibernate.cfg.xml").buildSessionFactory();
```

次の点に注意してください。

-   `hibernate.cfg.xml`構成ファイルはXML形式であり、 `&` XMLでは特殊文字であるため、ファイルを構成する際には`&`を`&amp;`に変更する必要があります。例えば、接続文字列`hibernate.connection.url` `jdbc:mysql://{host}:{port}/{database}?user={user}&password={password}`から`jdbc:mysql://{host}:{ port}/{database}?user={user}&amp;password={password}`に変更する必要があります。
-   `hibernate.dialect` 〜 `org.hibernate.dialect.TiDBDialect`に設定して`TiDB`方言を使用することをお勧めします。
-   Hibernate は`6.0.0.Beta2`以降の TiDB 方言をサポートしているため、TiDB に接続するには Hibernate `6.0.0.Beta2`以降のバージョンを使用することをお勧めします。

Hibernate 接続パラメータの詳細については、 [Hibernateのドキュメント](https://hibernate.org/orm/documentation)参照してください。

### 接続パラメータ {#connection-parameters}

|    パラメータ名    |                              説明                             |
| :----------: | :---------------------------------------------------------: |
| `{username}` |                 TiDB クラスターに接続するための SQL ユーザー                 |
| `{password}` |                        SQLユーザーのパスワード                        |
|   `{host}`   | TiDBノードの[ホスト](https://en.wikipedia.org/wiki/Host_(network)) |
|   `{port}`   |                     TiDBノードがリッスンしているポート                     |
| `{database}` |                         既存のデータベースの名前                        |

<CustomContent platform="tidb">

TiDB SQLユーザーの詳細については、 [TiDB ユーザーアカウント管理](/user-account-management.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB SQLユーザーの詳細については、 [TiDB ユーザーアカウント管理](https://docs.pingcap.com/tidb/stable/user-account-management)参照してください。

</CustomContent>

## ヘルプが必要ですか? {#need-help}

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。
