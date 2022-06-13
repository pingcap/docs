---
title: Connect to TiDB
summary: Learn how to connect to TiDB.
---

# TiDBに接続する {#connect-to-tidb}

TiDBは、MySQL5.7プロトコルと高い互換性があります。クライアントリンクパラメータの完全なリストについては、 [MySQLクライアントオプション](https://dev.mysql.com/doc/refman/5.7/en/mysql-command-options.html)を参照してください。

TiDBは[MySQLクライアント/サーバープロトコル](https://dev.mysql.com/doc/internals/en/client-server-protocol.html)をサポートします。これにより、ほとんどのクライアントドライバーとORMフレームワークがMySQLに接続するのと同じようにTiDBに接続できます。

## MySQLシェル {#mysql-shell}

TiDBのコマンドラインツールとして使用できるMySQLシェルを使用してTiDBに接続できます。 MySQL Shellをインストールするには、 [MySQLシェルのドキュメント](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.html)の手順に従います。インストール後、次のコマンドを使用してTiDBに接続できます。

{{< copyable "" >}}

```shell
mysql --host <tidb_server_host> --port 4000 -u root -p --comments
```

> **ノート：**
>
> バージョン5.7.7より前のMySQLシェルは、デフォルトで[オプティマイザーのヒント](/optimizer-hints.md#optimizer-hints)をクリアします。以前のMySQLShellバージョンでヒント構文を使用する必要がある場合は、クライアントの起動時に`--comments`オプションを追加します。

## JDBC {#jdbc}

[JDBC](https://dev.mysql.com/doc/connector-j/8.0/en/)のドライバーを使用してTiDBに接続できます。これを行うには、 `MysqlDataSource`または`MysqlConnectionPoolDataSource`オブジェクト（両方のオブジェクトが`DataSource`インターフェイスをサポート）を作成してから、 `setURL`関数を使用して接続文字列を設定する必要があります。

例えば：

{{< copyable "" >}}

```java
MysqlDataSource mysqlDataSource = new MysqlDataSource();
mysqlDataSource.setURL("jdbc:mysql://{host}:{port}/{database}?user={username}&password={password}");
```

JDBC接続の詳細については、 [JDBCドキュメント](https://dev.mysql.com/doc/connector-j/8.0/en/)を参照してください。

### 接続パラメータ {#connection-parameters}

|    パラメータ名    |                              説明                             |
| :----------: | :---------------------------------------------------------: |
| `{username}` |    TiDBクラスタに接続するための[SQLユーザー](/user-account-management.md)   |
| `{password}` |                        SQLユーザーのパスワード                        |
|   `{host}`   | TiDBノードの[ホスト](https://en.wikipedia.org/wiki/Host_(network)) |
|   `{port}`   |                     TiDBノードがリッスンしているポート                     |
| `{database}` |                         既存のデータベースの名前                        |

## Hibernate {#hibernate}

[Hibernate ORM](https://hibernate.org/orm/)を使用してTiDBに接続できます。これを行うには、Hibernate構成ファイルの`hibernate.connection.url`を有効なTiDB接続文字列に設定する必要があります。

たとえば、 `hibernate.cfg.xml`の構成ファイルを使用する場合は、次のように`hibernate.connection.url`を設定します。

{{< copyable "" >}}

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

構成が完了したら、次のコマンドを使用して構成ファイルを読み取り、 `SessionFactory`のオブジェクトを取得できます。

{{< copyable "" >}}

```java
SessionFactory sessionFactory = new Configuration().configure("hibernate.cfg.xml").buildSessionFactory();
```

次の点に注意してください。

-   `hibernate.cfg.xml`の構成ファイルはXML形式であり、 `&`はXMLの特殊文字であるため、ファイルを構成するときに`&`を`&amp;`に変更する必要があります。たとえば、接続文字列`hibernate.connection.url`を`jdbc:mysql://{host}:{port}/{database}?user={user}&password={password}`から`jdbc:mysql://{host}:{ port}/{database}?user={user}&amp;password={password}`に変更する必要があります。
-   `hibernate.dialect`から`org.hibernate.dialect.TiDBDialect`に設定して、 `TiDB`方言を使用することをお勧めします。
-   Hibernateは`6.0.0.Beta2`から始まるTiDBダイアレクトをサポートしているため、 `6.0.0.Beta2`への接続にはHibernate3以降のバージョンを使用することをお勧めします。

Hibernate接続パラメーターの詳細については、 [Hibernateドキュメント](https://hibernate.org/orm/documentation)を参照してください。

### 接続パラメータ {#connection-parameters}

|    パラメータ名    |                              説明                             |
| :----------: | :---------------------------------------------------------: |
| `{username}` |    TiDBクラスタに接続するための[SQLユーザー](/user-account-management.md)   |
| `{password}` |                        SQLユーザーのパスワード                        |
|   `{host}`   | TiDBノードの[ホスト](https://en.wikipedia.org/wiki/Host_(network)) |
|   `{port}`   |                     TiDBノードがリッスンしているポート                     |
| `{database}` |                         既存のデータベースの名前                        |
