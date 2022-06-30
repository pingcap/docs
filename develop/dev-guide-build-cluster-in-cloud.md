---
title: Build a TiDB Cluster in TiDB Cloud (DevTier)
summary: Learn how to build a TiDB cluster in TiDB Cloud (Developer Tier) and connect to a TiDB Cloud cluster.
---

<!-- markdownlint-disable MD029 -->

# TiDB CloudでTiDBクラスタを構築する（DevTier） {#build-a-tidb-cluster-in-tidb-cloud-devtier}

このドキュメントでは、TiDBの使用を開始する最も簡単な方法について説明します。 [TiDB Cloud](https://en.pingcap.com/tidb-cloud)を使用して、無料のTiDBクラスタを作成し、それに接続して、サンプルアプリケーションを実行します。

ローカルマシンでTiDBを実行する必要がある場合は、 [TiDBをローカルで起動する](/quick-start-with-tidb.md)を参照してください。

## 手順1.無料のクラスタを作成する {#step-1-create-a-free-cluster}

1.  TiDB Cloudアカウントをお持ちでない場合は、 [TiDB Cloud](https://tidbcloud.com/free-trial)をクリックしてアカウントにサインアップしてください。

2.  TiDB Cloudアカウントで[ログイン](https://tidbcloud.com/) 。

3.  1年間無料で開発者層クラスタを作成するには、 [プランページ](https://tidbcloud.com/console/plans)で**開発者層**プランを選択するか、 [クラスターの作成（開発層）](https://tidbcloud.com/console/create-cluster?tier=dev)をクリックします。

4.  [**クラスターの作成（開発者層）]**ページで、クラスタ名、パスワード、クラウドプロバイダー（現時点では、AWSのみが開発者層で利用可能）、およびリージョン（近くのリージョンが推奨されます）を設定します。次に、[<strong>作成</strong>]をクリックしてクラスタを作成します。

5.  TiDB Cloudクラスタは約5〜15分で作成されます。作成の進行状況は[アクティブクラスター](https://tidbcloud.com/console/clusters)で確認できます。

6.  クラスタを作成した後、[**アクティブクラスター**]ページで、新しく作成したクラスタの名前をクリックして、クラスタのコントロールパネルに移動します。

    ![active clusters](/media/develop/IMG_20220331-232643794.png)

7.  [**接続**]をクリックして、トラフィックフィルター（TiDB接続で許可されているクライアントIPのリスト）を作成します。

    ![connect](/media/develop/IMG_20220331-232726165.png)

8.  ポップアップウィンドウで、[**現在のIPアドレスを追加**]をクリックして現在のIPアドレスを入力し、[<strong>フィルター</strong>の作成]をクリックしてトラフィックフィルターを作成します。

9.  文字列をコピーして、後で使用するためにSQLクライアントに接続します。

    ![SQL string](/media/develop/IMG_20220331-232800929.png)

## ステップ2.クラスタに接続する {#step-2-connect-to-a-cluster}

1.  MySQLクライアントがインストールされていない場合は、オペレーティングシステムを選択し、以下の手順に従ってインストールします。

<SimpleTab>

<div label="macOS">

[自作](https://brew.sh/index)がない場合はインストールし、次のコマンドを実行してMySQLクライアントをインストールします。

{{< copyable "" >}}

```shell
brew install mysql-client
```

出力は次のとおりです。

```
mysql-client is keg-only, which means it was not symlinked into /opt/homebrew,
because it conflicts with mysql (which contains client libraries).

If you need to have mysql-client first in your PATH, run:
  echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc

For compilers to find mysql-client you may need to set:
  export LDFLAGS="-L/opt/homebrew/opt/mysql-client/lib"
  export CPPFLAGS="-I/opt/homebrew/opt/mysql-client/include"
```

MySQLクライアントをPATHに追加するには、上記の出力で次のコマンドを見つけ（出力がドキュメントの上記の出力と矛盾する場合は、代わりに出力で対応するコマンドを使用します）、実行します。

{{< copyable "" >}}

```shell
echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc
```

次に、 `source`コマンドでグローバル環境変数を宣言し、MySQLクライアントが正常にインストールされていることを確認します。

{{< copyable "" >}}

```shell
source ~/.zshrc
mysql --version
```

期待される出力の例：

```
mysql  Ver 8.0.28 for macos12.0 on arm64 (Homebrew)
```

</div>

<div label="Linux">

例としてCentOS7を取り上げます。

{{< copyable "" >}}

```shell
yum install mysql
```

次に、MySQLクライアントが正常にインストールされていることを確認します。

{{< copyable "" >}}

```shell
mysql --version
```

期待される出力の例：

```
mysql  Ver 15.1 Distrib 5.5.68-MariaDB, for Linux (x86_64) using readline 5.1
```

</div>

</SimpleTab>

2.  [ステップ1](#step-1-create-a-free-cluster)で取得した接続文字列を実行します。

{{< copyable "" >}}

```shell
mysql --connect-timeout 15 -u root -h <host> -P 4000 -p
```

3.  サインインするにはパスワードを入力してください。

## ステップ3.サンプルアプリケーションを実行します {#step-3-run-the-sample-application}

1.  `tidb-example-java`のプロジェクトのクローンを作成します。

{{< copyable "" >}}

```shell
git clone https://github.com/pingcap-inc/tidb-example-java.git
```

2.  接続パラメータを変更します。

<SimpleTab>

<div label="Local default cluster">

変更は必要ありません。

</div>

<div label="Non-local default cluster, TiDB Cloud, or other remote cluster">

`plain-java-jdbc/src/main/java/com/pingcap/JDBCExample.java`で、ホスト、ポート、ユーザー、およびパスワードのパラメーターを変更します。

{{< copyable "" >}}

```java
mysqlDataSource.setServerName("localhost");
mysqlDataSource.setPortNumber(4000);
mysqlDataSource.setDatabaseName("test");
mysqlDataSource.setUser("root");
mysqlDataSource.setPassword("");
```

設定したパスワードが`123456`で、 TiDB Cloudから取得した接続文字列が次のとおりであるとします。

{{< copyable "" >}}

```shell
mysql --connect-timeout 15 -u root -h xxx.tidbcloud.com -P 4000 -p
```

この場合、次のようにパラメータを変更できます。

{{< copyable "" >}}

```java
mysqlDataSource.setServerName("xxx.tidbcloud.com");
mysqlDataSource.setPortNumber(4000);
mysqlDataSource.setDatabaseName("test");
mysqlDataSource.setUser("root");
mysqlDataSource.setPassword("123456");
```

</div>

</SimpleTab>

3.  `make plain-java-jdbc`を実行します。

これが[期待される出力](https://github.com/pingcap-inc/tidb-example-java/blob/main/Expected-Output.md#plain-java-jdbc)の例です。
