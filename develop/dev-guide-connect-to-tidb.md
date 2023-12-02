---
title: Connect to TiDB
summary: Learn how to connect to TiDB.
---

# TiDB に接続する {#connect-to-tidb}

TiDB は MySQL プロトコルと高い互換性があります。クライアント リンク パラメータの完全なリストについては、 [MySQL クライアントのオプション](https://dev.mysql.com/doc/refman/8.0/en/mysql-command-options.html)を参照してください。

TiDB は[MySQL クライアント/サーバー プロトコル](https://dev.mysql.com/doc/dev/mysql-server/latest/PAGE_PROTOCOL.html)サポートしており、ほとんどのクライアント ドライバーと ORM フレームワークが MySQL に接続するのと同じように TiDB に接続できるようになります。

## MySQL {#mysql}

個人の好みに基づいて、MySQL クライアントまたは MySQL シェルの使用を選択できます。

<SimpleTab>

<div label="MySQL Client">

TiDB のコマンドライン ツールとして使用できる MySQL クライアントを使用して TiDB に接続できます。 MySQL クライアントをインストールするには、YUM ベースの Linux ディストリビューションの以下の手順に従ってください。

```shell
sudo yum install mysql
```

インストール後、次のコマンドを使用して TiDB に接続できます。

```shell
mysql --host <tidb_server_host> --port 4000 -u root -p --comments
```

</div>

<div label="MySQL Shell">

TiDB のコマンドライン ツールとして使用できる MySQL Shell を使用して TiDB に接続できます。 MySQL Shell をインストールするには、 [MySQL シェルのドキュメント](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.html)の手順に従ってください。インストール後、次のコマンドを使用して TiDB に接続できます。

```shell
mysqlsh --sql mysql://root@<tidb_server_host>:4000
```

</div>

</SimpleTab>

## JDBC {#jdbc}

[JDBC](https://dev.mysql.com/doc/connector-j/en/)ドライバーを使用して TiDB に接続できます。これを行うには、 `MysqlDataSource`または`MysqlConnectionPoolDataSource`オブジェクト (どちらのオブジェクトも`DataSource`インターフェイスをサポートします) を作成し、 `setURL`関数を使用して接続文字列を設定する必要があります。

例えば：

```java
MysqlDataSource mysqlDataSource = new MysqlDataSource();
mysqlDataSource.setURL("jdbc:mysql://{host}:{port}/{database}?user={username}&password={password}");
```

JDBC 接続の詳細については、 [JDBC ドキュメント](https://dev.mysql.com/doc/connector-j/en/)を参照してください。

### 接続パラメータ {#connection-parameters}

|    パラメータ名    |                              説明                              |
| :----------: | :----------------------------------------------------------: |
| `{username}` |                  TiDB クラスターに接続するための SQL ユーザー                 |
| `{password}` |                        SQL ユーザーのパスワード                        |
|   `{host}`   | TiDB ノードの[ホスト](https://en.wikipedia.org/wiki/Host_(network)) |
|   `{port}`   |                     TiDB ノードがリッスンしているポート                     |
| `{database}` |                         既存のデータベースの名前                         |

<CustomContent platform="tidb">

TiDB SQLユーザーの詳細については、 [TiDB ユーザーアカウント管理](/user-account-management.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB SQLユーザーの詳細については、 [TiDB ユーザーアカウント管理](https://docs.pingcap.com/tidb/stable/user-account-management)を参照してください。

</CustomContent>

## 休止状態 {#hibernate}

[休止状態 ORM](https://hibernate.org/orm/)を使用して TiDB に接続できます。これを行うには、Hibernate 構成ファイルの`hibernate.connection.url`正当な TiDB 接続文字列に設定する必要があります。

たとえば、 `hibernate.cfg.xml`設定ファイルを使用する場合は、次のように`hibernate.connection.url`を設定します。

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

構成が完了したら、次のコマンドを使用して構成ファイルを読み取り、 `SessionFactory`オブジェクトを取得できます。

```java
SessionFactory sessionFactory = new Configuration().configure("hibernate.cfg.xml").buildSessionFactory();
```

次の点に注意してください。

-   `hibernate.cfg.xml`設定ファイルは XML 形式であり、 `&`は XML の特殊文字であるため、ファイルを設定するときに`&`を`&amp;`に変更する必要があります。たとえば、接続文字列`hibernate.connection.url` `jdbc:mysql://{host}:{port}/{database}?user={user}&password={password}`から`jdbc:mysql://{host}:{ port}/{database}?user={user}&amp;password={password}`に変更する必要があります。
-   `TiDB`方言を`hibernate.dialect` ～ `org.hibernate.dialect.TiDBDialect`に設定して使用することをお勧めします。
-   Hibernate は`6.0.0.Beta2`から始まる TiDB ダイアレクトをサポートしているため、TiDB への接続には Hibernate `6.0.0.Beta2`以降のバージョンを使用することをお勧めします。

Hibernate 接続パラメータの詳細については、 [Hibernate のドキュメント](https://hibernate.org/orm/documentation)を参照してください。

### 接続パラメータ {#connection-parameters}

|    パラメータ名    |                              説明                              |
| :----------: | :----------------------------------------------------------: |
| `{username}` |                  TiDB クラスターに接続するための SQL ユーザー                 |
| `{password}` |                        SQL ユーザーのパスワード                        |
|   `{host}`   | TiDB ノードの[ホスト](https://en.wikipedia.org/wiki/Host_(network)) |
|   `{port}`   |                     TiDB ノードがリッスンしているポート                     |
| `{database}` |                         既存のデータベースの名前                         |

<CustomContent platform="tidb">

TiDB SQLユーザーの詳細については、 [TiDB ユーザーアカウント管理](/user-account-management.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB SQLユーザーの詳細については、 [TiDB ユーザーアカウント管理](https://docs.pingcap.com/tidb/stable/user-account-management)を参照してください。

</CustomContent>
