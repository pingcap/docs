---
title: Build a TiDB Cluster in TiDB Cloud (DevTier)
summary: Learn how to build a TiDB cluster in TiDB Cloud (Developer Tier) and connect to a TiDB Cloud cluster.
---

<!-- markdownlint-disable MD029 -->

# TiDB Cloud (DevTier) で TiDBクラスタを構築する {#build-a-tidb-cluster-in-tidb-cloud-devtier}

このドキュメントでは、TiDB を開始するための最も簡単な方法について説明します。 [TiDB Cloud](https://en.pingcap.com/tidb-cloud)を使用して、無料の TiDBクラスタを作成し、それに接続して、サンプル アプリケーションを実行します。

ローカル マシンで TiDB を実行する必要がある場合は、 [TiDB をローカルで起動する](/quick-start-with-tidb.md)を参照してください。

## ステップ 1.無料のクラスタを作成する {#step-1-create-a-free-cluster}

1.  TiDB Cloudアカウントを持っていない場合は、 [TiDB Cloud](https://tidbcloud.com/free-trial)をクリックしてアカウントにサインアップします。

2.  [ログイン](https://tidbcloud.com/)をTiDB Cloudアカウントで。

3.  Developer Tierクラスタを 1 年間無料で作成するには、 [プランページ](https://tidbcloud.com/console/plans)で**Developer Tier**プランを選択するか、 [クラスターの作成](https://tidbcloud.com/console/clusters)をクリックして [<strong>クラスターの作成</strong>] ページで<strong>Developer Tier</strong>を選択します。

4.  [**クラスターの作成]**ページで、クラスタ名、クラウド プロバイダー (現時点では、開発者層で使用できるのは AWS のみ)、およびリージョン (近くのリージョンをお勧めします) を設定します。次に、[<strong>作成</strong>] をクリックしてクラスタを作成します。

5.  TiDB Cloudクラスタは、約 5 ～ 15 分で作成されます。 [アクティブなクラスター](https://tidbcloud.com/console/clusters)で作成の進行状況を確認できます。

6.  クラスタを作成したら、[**アクティブなクラスター**] ページで、新しく作成したクラスタの名前をクリックして、クラスタコントロール パネルに移動します。

    ![active clusters](/media/develop/IMG_20220331-232643794.png)

7.  [**接続**] をクリックして、トラフィック フィルター (TiDB 接続に許可されているクライアント IP のリスト) を作成します。

    ![connect](/media/develop/IMG_20220331-232726165.png)

8.  ポップアップ ウィンドウで、[**現在の IP アドレスを追加**] をクリックして現在の IP アドレスを入力し、[<strong>フィルター</strong>の作成] をクリックしてトラフィック フィルターを作成します。

9.  後で使用するために、文字列をコピーして SQL クライアントに接続します。

    ![SQL string](/media/develop/IMG_20220331-232800929.png)

## ステップ 2.クラスタに接続する {#step-2-connect-to-a-cluster}

1.  MySQL クライアントがインストールされていない場合は、オペレーティング システムを選択し、以下の手順に従ってインストールします。

<SimpleTab>

<div label="macOS">

macOS の場合、 [自作](https://brew.sh/index)がない場合はインストールしてから、次のコマンドを実行して MySQL クライアントをインストールします。

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

MySQL クライアントを PATH に追加するには、上記の出力で次のコマンドを見つけて (出力がドキュメントの上記の出力と一致しない場合は、代わりに出力で対応するコマンドを使用してください)、それを実行します。

{{< copyable "" >}}

```shell
echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc
```

次に、 `source`コマンドでグローバル環境変数を宣言し、MySQL クライアントが正常にインストールされていることを確認します。

{{< copyable "" >}}

```shell
source ~/.zshrc
mysql --version
```

予想される出力の例:

```
mysql  Ver 8.0.28 for macos12.0 on arm64 (Homebrew)
```

</div>

<div label="Linux">

Linux の場合、次の例では CentOS 7 を使用しています。

{{< copyable "" >}}

```shell
yum install mysql
```

次に、MySQL クライアントが正常にインストールされたことを確認します。

{{< copyable "" >}}

```shell
mysql --version
```

予想される出力の例:

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

3.  パスワードを入力してサインインします。

## ステップ 3. サンプル アプリケーションを実行する {#step-3-run-the-sample-application}

1.  `tidb-example-java`のプロジェクトを複製します。

{{< copyable "" >}}

```shell
git clone https://github.com/pingcap-inc/tidb-example-java.git
```

2.  接続パラメーターを変更します。

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

[期待される出力](https://github.com/pingcap-inc/tidb-example-java/blob/main/Expected-Output.md#plain-java-jdbc)の例を次に示します。
