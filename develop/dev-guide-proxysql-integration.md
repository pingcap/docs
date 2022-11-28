---
title: Integrate TiDB with ProxySQL
summary: Introduce how to integrate TiDB with ProxySQL step by step.
aliases: ["/tidbcloud/dev-guide-proxysql-integration"]
---

# TiDB を ProxySQL と統合する {#integrate-tidb-with-proxysql}

このドキュメントでは、例として CentOS 7 を使用して**TiDB**と<strong>ProxySQL</strong>を統合する方法について説明します。他のシステムを使用して統合する場合は、 [試してみる](#4-try-out)セクションを参照してください。このセクションでは、 <strong>Docker</strong>および<strong>Docker Compose</strong>を使用してテスト統合環境をデプロイする方法を紹介しています。詳細については、次を参照してください。

-   [TiDB ドキュメント](/overview.md)
-   [TiDB 開発者ガイド](/develop/dev-guide-overview.md)
-   [ProxySQL ドキュメント](https://proxysql.com/documentation/)
-   [TiDB と ProxySQL の統合テスト](https://github.com/Icemap/tidb-proxysql-integration-test)

## 1.TiDBを起動 {#1-start-tidb}

### テスト環境 {#test-environment}

<SimpleTab groupId="startup-tidb">

<div label="TiDB Cloud" value="tidb-cloud">

[TiDB Cloud(サーバーレス層) で TiDB クラスターを構築する](/develop/dev-guide-build-cluster-in-cloud.md)を参照できます。

</div>

<div label="Source compilation" value="source-code">

1.  [TiDB](https://github.com/pingcap/tidb)のソースコードをダウンロードし、 `tidb-server`のフォルダに移動して`go build`のコマンドを実行します。

    ```shell
    git clone git@github.com:pingcap/tidb.git
    cd tidb/tidb-server
    go build
    ```

2.  構成ファイル[`tidb-config.toml`](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/tidb-config.toml)を使用して、TiDB を開始します。コマンドは次のとおりです。

    ```shell
    ${TIDB_SERVER_PATH} -config ./tidb-config.toml -store unistore -path "" -lease 0s > ${LOCAL_TIDB_LOG} 2>&1 &
    ```

    > **ノート：**
    >
    > -   上記のコマンドは、ストレージ エンジンとして`unistore`を使用します。これは、TiDB のテスト ストレージ エンジンです。テスト環境でのみ使用してください。
    > -   `TIDB_SERVER_PATH` : `go build`を使用したコンパイル済みバイナリのパス。たとえば、前のコマンドを`/usr/local`の下で実行すると、 `TIDB_SERVER_PATH`は`/usr/local/tidb/tidb-server/tidb-server`になります。
    > -   `LOCAL_TIDB_LOG` : TiDB のログ ファイル パス。

</div>

<div label="TiUP" value="tiup">

[TiUP](/tiup/tiup-overview.md)は、TiDB パッケージ マネージャーとして、TiDB、PD、TiKV など、TiDB エコシステム内のさまざまなクラスター コンポーネントの管理を容易にします。

1.  TiUP をインストールします。

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2.  テスト環境で TiDB を起動します。

    ```shell
    tiup playground
    ```

</div>

</SimpleTab>

### 本番環境 {#production-environment}

<SimpleTab groupId="startup-tidb">

<div label="TiDB Cloud" value="tidb-cloud">

TiDB サービスをホストする必要がある場合は、 [TiDB Cloud](https://en.pingcap.com/tidb-cloud/)を直接使用することをお勧めします (たとえば、自分で管理できない場合や、クラウドネイティブ環境が必要な場合など)。本番環境で TiDB クラスターを構築するには、 [TiDB クラスターを作成する](https://docs.pingcap.com/tidbcloud/create-tidb-cluster)を参照してください。

</div>

<div label="Deploy Locally" value="tiup">

本番環境では、テスト環境よりも多くの手順が必要です。オンプレミスの本番クラスターをデプロイするには、 [TiUP を使用して TiDB クラスターをデプロイする](/production-deployment-using-tiup.md)を参照して、ハードウェアの条件に基づいてデプロイすることをお勧めします。

</div>

</SimpleTab>

## 2.ProxySQL を開始します。 {#2-start-proxysql}

### ProxySQL を yum でインストールする {#install-proxysql-by-yum}

1.  ProxySQL リポジトリを追加します。

    ```shell
    cat > /etc/yum.repos.d/proxysql.repo << EOF
    [proxysql]
    name=ProxySQL YUM repository
    baseurl=https://repo.proxysql.com/ProxySQL/proxysql-2.4.x/centos/\$releasever
    gpgcheck=1
    gpgkey=https://repo.proxysql.com/ProxySQL/proxysql-2.4.x/repo_pub_key
    EOF
    ```

2.  ProxySQL をインストールします。

    ```shell
    yum install proxysql
    ```

3.  ProxySQL を開始します。

    ```shell
    systemctl start proxysql
    ```

### 他のインストール方法 {#other-installation-ways}

他の方法で ProxySQL をインストールするには、 [ProxySQL README](https://github.com/sysown/proxysql#installation)または[ProxySQL インストール ドキュメント](https://proxysql.com/documentation/)を参照してください。

## 3.ProxySQL を構成する {#3-configure-proxysql}

ProxySQL を TiDB のプロキシとして使用するには、ProxySQL を構成する必要があります。必要な構成項目は、次のセクションにリストされています。その他の構成項目の詳細については、 [ProxySQL の公式ドキュメント](https://proxysql.com/documentation/)を参照してください。

### 簡単な紹介 {#simple-introduction}

ProxySQL は、構成を管理するためのポート ( ***ProxySQL Admin インターフェイス***) と、プロキシへのポート ( <em><strong>ProxySQL MySQL Interface</strong></em> ) を使用します。

-   ***ProxySQL 管理インターフェイス***: 管理インターフェイスに接続するには、 `admin`ユーザーを使用して構成の読み取りと書き込みを行うか、 `stats`ユーザーを使用して統計の一部を読み取ることができます (構成の読み取りまたは書き込みはできません)。デフォルトの資格証明は`admin:admin`および`stats:stats`です。セキュリティ上の理由から、既定の資格情報を使用してローカルに接続できますが、リモートで接続するには、多くの場合`radmin`という名前の新しいユーザーを構成する必要があります。
-   ***ProxySQL MySQL Interface*** : SQL を設定済みのサービスに転送するためのプロキシとして使用されます。

![proxysql config flow](/media/develop/proxysql_config_flow.png)

ProxySQL 構成には、 `runtime` 、 `memory` 、および`disk`の 3 つのレイヤーがあります。 `memory`レイヤーの構成のみを変更できます。構成を変更した後、 `LOAD xxx TO runtime`を使用して構成を有効にするか、 `SAVE xxx TO DISK`を使用してディスクに保存し、構成の損失を防ぐことができます。

![proxysql config layer](/media/develop/proxysql_config_layer.png)

### TiDBサーバーの構成 {#configure-tidb-server}

ProxySQL に複数の TiDB サーバーを追加できます。 TiDB サーバーを追加するには、 ***ProxySQL 管理インターフェイス***で次の手順を実行します。

```sql
INSERT INTO mysql_servers(hostgroup_id, hostname, port) VALUES (0, '127.0.0.1', 4000);
LOAD mysql servers TO runtime;
SAVE mysql servers TO DISK;
```

フィールドの説明:

-   `hostgroup_id` : **ProxySQL**はホストグループによってサーバーを管理します。これらのサーバーに SQL を均等に分散するために、負荷分散が必要な複数のサーバーを同じホストグループに構成できます。読み取りと書き込みの分割など、サーバーを区別するために、それらを異なるホストグループに構成できます。
-   `hostname` : TiDBサーバーの IP またはドメイン。
-   `port` : TiDBサーバーのポート。

### プロキシ ログイン ユーザーの構成 {#configure-proxy-login-users}

TiDBサーバーユーザーを ProxySQL に追加すると、ProxySQL はこのユーザーが***ProxySQL MySQL Interface***にログインして TiDB との接続を作成できるようにします。ユーザーが TiDB で適切な権限を持っていることを確認してください。 TiDBサーバーユーザーを追加するには、 <em><strong>ProxySQL 管理インターフェイス</strong></em>で次の手順を実行します。

```sql
INSERT INTO mysql_users(username, password, active, default_hostgroup, transaction_persistent) VALUES ('root', '', 1, 0, 1);
LOAD mysql users TO runtime;
SAVE mysql users TO DISK;
```

フィールドの説明:

-   `username` : ユーザー名。
-   `password` : パスワード。
-   `active` : ユーザーがアクティブかどうかを制御します。 `1`がアクティブで、 `0`が非アクティブです。 `active`が`1`の場合のみ、ユーザーはログインできます。
-   `default_hostgroup` : ユーザーが使用する既定のホスト グループ。クエリ ルールがトラフィックを特定のホスト グループにルーティングしない限り、SQL が配布されます。
-   `transaction_persistent` : `1`は永続的なトランザクションを示します。つまり、ユーザーが接続でトランザクションを開始すると、トランザクションがコミットまたはロールバックされるまで、すべてのステートメントが同じホストグループにルーティングされます。

### 構成ファイルによる ProxySQL の構成 {#configure-proxysql-by-a-configuration-file}

***ProxySQL Admin インターフェイス***を使用して構成することに加えて、構成ファイルを使用して ProxySQL を構成することもできます。 [構成ファイルによる ProxySQL の構成](https://github.com/sysown/proxysql#configuring-proxysql-through-the-config-file)ドキュメントでは、構成ファイルは ProxySQL を初期化するための主要な方法ではなく、二次的な方法としてのみ考慮されるべきです。構成ファイルは、SQLite が作成されていない場合にのみ使用され、SQLite が作成された後は使用されません。構成ファイルを使用して ProxySQL を構成する場合は、最初に次のコマンドを使用して SQLite を削除する必要があります。ただし、これにより、 <em><strong>ProxySQL Admin インターフェイス</strong></em>での構成の変更が<strong>失わ</strong>れます。

```shell
rm /var/lib/proxysql/proxysql.db
```

または、 `LOAD xxx FROM CONFIG`コマンドを実行して現在の構成を上書きすることもできます。

構成ファイルのパスは`/etc/proxysql.cnf`です。構成ファイルを使用して、前のセクションで必要な構成項目を構成するには、次の例では`mysql_servers`と`mysql_users`を使用します。他の項目を変更するには、 `/etc/proxysql.cnf`を参照してください。

```
mysql_servers =
(
    {
        address="127.0.0.1"
        port=4000
        hostgroup=0
        max_connections=2000
    }
)

mysql_users:
(
    {
        username = "root"
        password = ""
        default_hostgroup = 0
        max_connections = 1000
        default_schema = "test"
        active = 1
        transaction_persistent = 1
    }
)
```

上記の変更を有効にするには、 `systemctl restart proxysql`コマンドを使用して ProxySQL を再起動します。その後、SQLite データベースが自動的に作成され、構成ファイルは無視されません。

### その他の設定項目 {#other-configuration-items}

上記の構成アイテムは必須です。オプションの設定項目については、 [グローバル変数](https://proxysql.com/documentation/global-variables/)を参照してください。

## 4. 試してみる {#4-try-out}

テスト環境をすばやく開始するには、Docker と Docker Compose を使用できます。ポート`4000`と`6033`が割り当てられていないことを確認します。

```shell
git clone https://github.com/Icemap/tidb-proxysql-integration-test.git
cd tidb-proxysql-integration-test && docker-compose pull # Get the latest Docker images
sudo setenforce 0 # Only on Linux
docker-compose up -d
```

> **警告：**
>
> 前述のコマンドを使用して本番環境で統合を作成し**ない**でください。

上記のコマンドは、TiDB と ProxySQL を統合した環境を開始し、2 つのコンテナーを実行します。 ProxySQL `6033`ポートにログインするには、ユーザー名`root`と空のパスワードを使用できます。コンテナーの構成の詳細については、 [`docker-compose.yaml`](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/docker-compose.yaml)を参照してください。 ProxySQL の構成の詳細については、 [`proxysql-docker.cnf`](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/proxysql-docker.cnf)を参照してください。

TiDB に接続するには、次のコマンドを実行します。

```shell
mysql -u root -h 127.0.0.1 -P 6033 -e "SELECT VERSION()"
```

結果の例は次のとおりです。

```sql
+--------------------+
| VERSION()          |
+--------------------+
| 5.7.25-TiDB-v6.1.2 |
+--------------------+
```

## 5.Configuration / コンフィグレーション例 {#5-configuration-examples}

依存関係:

-   ドッカー
-   Docker Compose
-   MySQL クライアント

サンプル コード リポジトリのクローンを作成し、サンプル ディレクトリに移動します。

```shell
git clone https://github.com/Icemap/tidb-proxysql-integration-test.git
cd tidb-proxysql-integration-test
```

次のセクションでは、ルート ディレクトリとして`tidb-proxysql-integration-test`を使用します。

### 管理インターフェイスを使用して負荷分散を構成する {#use-admin-interface-to-configure-load-balancing}

サンプル ディレクトリに移動します。

```shell
cd example/load-balance-admin-interface
```

#### スクリプトで実行 {#run-with-a-script}

***ProxySQL Admin Interface***を使用して負荷分散を構成するには、次のコマンドを使用して`test-load-balance.sh`スクリプトを実行します。

```shell
./test-load-balance.sh
```

#### ステップバイステップで実行 {#run-step-by-step}

前の`test-load-balance.sh`のスクリプトは、次のように段階的に実行できます。

1.  3 つの TiDB コンテナーと 1 つの ProxySQL インスタンスを開始します。

    ```shell
    docker-compose up -d
    ```

    -   `docker-compose`を使用して 3 つの TiDB コンテナーを開始します。コンテナ内のすべてのポートは`4000`で、ホスト ポートは`4001` 、 `4002` 、および`4003`です。
    -   TiDB コンテナーを開始すると、ProxySQL インスタンスが開始されます。コンテナー内の***ProxySQL MySQL Interface***のポートは`6033`で、ホスト ポートは`6034`です。
    -   ***ProxySQL Admin Interface***のポートはコンテナ内でしかアクセスできないため公開されていません。
    -   プロセスの詳細については、 [`docker-compose.yaml`](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/example/load-balance-admin-interface/docker-compose.yaml)を参照してください。

2.  3 つの TiDB コンテナーで、TiDB インスタンスを区別するために、異なるデータ ( `'tidb-0'` 、 `'tidb-1'` 、および`'tidb-2'` ) を使用して同じテーブル スキーマを作成します。

    ```shell
    mysql -u root -h 127.0.0.1 -P 4001 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-0');
    EOF

    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-1');
    EOF

    mysql -u root -h 127.0.0.1 -P 4003 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-2');
    EOF
    ```

3.  ***ProxySQL Admin Interface***で[`proxysql-prepare.sql`](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/example/load-balance-admin-interface/proxysql-prepare.sql)を実行するには、次のように`docker-compose exec`コマンドを実行します。

    ```shell
    docker-compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    上記の SQL ファイルが実行され、次の操作がトリガーされます。

    1.  3 つの TiDB サーバーのホストを追加し、すべて`hostgroup_id`を`0`に設定します。
    2.  TiDb サーバーの構成を有効にして、ディスクに保存します。
    3.  空のパスワードを持つ`root`ユーザーを追加し、 `default_hostgroup`を`0`として設定します。これは、前の`hostgroup_id`の TiDB サーバーに対応します。
    4.  ユーザーの構成を有効にし、ディスクに保存します。

4.  `root`のユーザーで***ProxySQL MySQL Interface***にログインし、次のステートメントを使用して 5 回クエリを実行します。予想される出力には、 `'tidb-0'` 、 `'tidb-1'` 、および`'tidb-2'`の 3 つの異なる値が含まれます。

    ```shell
    mysql -u root -h 127.0.0.1 -P 6034 -t << EOF
    SELECT * FROM test.test;
    SELECT * FROM test.test;
    SELECT * FROM test.test;
    SELECT * FROM test.test;
    SELECT * FROM test.test;
    EOF
    ```

5.  コンテナーとネットワークを停止して削除するには、次のコマンドを使用できます。

    ```shell
    docker-compose down
    ```

#### 期待される出力 {#expected-output}

予想される出力には 3 つの異なる結果 ( `'tidb-0'` 、 `'tidb-1'` 、および`'tidb-2'` ) がありますが、正確な順序は予想できません。以下は、予想される出力の 1 つです。

```
# ./test-load-balance.sh
Creating network "load-balance-admin-interface_default" with the default driver
Creating load-balance-admin-interface_tidb-1_1 ... done
Creating load-balance-admin-interface_tidb-2_1 ... done
Creating load-balance-admin-interface_tidb-0_1 ... done
Creating load-balance-admin-interface_proxysql_1 ... done
+--------+
| db     |
+--------+
| tidb-2 |
+--------+
+--------+
| db     |
+--------+
| tidb-0 |
+--------+
+--------+
| db     |
+--------+
| tidb-1 |
+--------+
+--------+
| db     |
+--------+
| tidb-1 |
+--------+
+--------+
| db     |
+--------+
| tidb-1 |
+--------+
Stopping load-balance-admin-interface_proxysql_1 ... done
Stopping load-balance-admin-interface_tidb-0_1   ... done
Stopping load-balance-admin-interface_tidb-2_1   ... done
Stopping load-balance-admin-interface_tidb-1_1   ... done
Removing load-balance-admin-interface_proxysql_1 ... done
Removing load-balance-admin-interface_tidb-0_1   ... done
Removing load-balance-admin-interface_tidb-2_1   ... done
Removing load-balance-admin-interface_tidb-1_1   ... done
Removing network load-balance-admin-interface_default
```

### 管理インターフェイスを使用してユーザー分割を構成する {#use-admin-interface-to-configure-user-split}

サンプル ディレクトリに移動します。

```shell
cd example/user-split-admin-interface
```

#### スクリプトで実行 {#run-with-a-script}

***ProxySQL Admin Interface***を使用してユーザー分割トラフィックを構成するには、次のコマンドを使用して`test-user-split.sh`スクリプトを実行します。

```shell
./test-user-split.sh
```

#### ステップバイステップで実行 {#run-step-by-step}

前の`test-user-split.sh`のスクリプトは、次のように段階的に実行できます。

1.  2 つの TiDB コンテナーと 1 つの ProxySQL インスタンスを開始します。

    ```shell
    docker-compose up -d
    ```

    -   `docker-compose`を使用して 2 つの TiDB コンテナーを開始します。コンテナー内のすべてのポートは`4000`で、ホスト ポートは`4001`と`4002`です。
    -   TiDB コンテナーを開始すると、ProxySQL インスタンスが開始されます。コンテナー内の***ProxySQL MySQL Interface***のポートは`6033`で、ホスト ポートは`6034`です。
    -   ***ProxySQL Admin Interface***のポートはコンテナ内でしかアクセスできないため公開されていません。
    -   プロセスの詳細については、 [`docker-compose.yaml`](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/example/user-split-admin-interface/docker-compose.yaml)を参照してください。

2.  2 つの TiDB コンテナーで、TiDB インスタンスを区別するために、異なるデータ ( `'tidb-0'`と`'tidb-1'` ) を使用して同じテーブル スキーマを作成します。

    ```shell
    mysql -u root -h 127.0.0.1 -P 4001 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-0');
    EOF

    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-1');
    EOF
    ```

3.  `tidb-1`つのインスタンスで ProxySQL の新しいユーザーを作成します。

    ```shell
    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    CREATE USER 'root1' IDENTIFIED BY '';
    GRANT ALL PRIVILEGES ON *.* TO 'root1'@'%';
    FLUSH PRIVILEGES;
    EOF
    ```

4.  ***ProxySQL Admin Interface***で[`proxysql-prepare.sql`](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/example/user-split-admin-interface/proxysql-prepare.sql)を実行するには、次のように`docker-compose exec`コマンドを実行します。

    ```shell
    docker-compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    上記の SQL ファイルが実行され、次の操作がトリガーされます。

    1.  2 つの TiDB サーバーのホストを追加します。 `hostgroup_id` of `tidb-0`は`0`で、 `hostgroup_id` of `tidb-1`は`1`です。
    2.  TiDb サーバーの構成を有効にして、ディスクに保存します。
    3.  空のパスワードで`root`ユーザーを追加し、 `default_hostgroup`を`0`に設定します。これは、SQL がデフォルトで`tidb-0`にルーティングされることを示しています。
    4.  空のパスワードでユーザー`root1`を追加し、 `default_hostgroup`を`1`に設定します。これは、SQL がデフォルトで`tidb-1`にルーティングされることを示しています。
    5.  ユーザーの構成を有効にし、ディスクに保存します。

5.  `root`ユーザーと`root1`ユーザーで***ProxySQL MySQL Interface***にログインします。予想される出力には、 `'tidb-0'`と`'tidb-1'`の 2 つの異なる値が含まれます。

    ```shell
    mysql -u root -h 127.0.0.1 -P 6034 -e "SELECT * FROM test.test;"
    mysql -u root1 -h 127.0.0.1 -P 6034 -e "SELECT * FROM test.test;"
    ```

6.  コンテナーとネットワークを停止して削除するには、次のコマンドを使用できます。

    ```shell
    docker-compose down
    ```

#### 期待される出力 {#expected-output}

以下は、予想される出力の 1 つです。

```
# ./test-user-split.sh
Creating network "user-split-admin-interface_default" with the default driver
Creating user-split-admin-interface_tidb-1_1 ... done
Creating user-split-admin-interface_tidb-0_1 ... done
Creating user-split-admin-interface_proxysql_1 ... done
+--------+
| db     |
+--------+
| tidb-0 |
+--------+
+--------+
| db     |
+--------+
| tidb-1 |
+--------+
Stopping user-split-admin-interface_proxysql_1 ... done
Stopping user-split-admin-interface_tidb-0_1   ... done
Stopping user-split-admin-interface_tidb-1_1   ... done
Removing user-split-admin-interface_proxysql_1 ... done
Removing user-split-admin-interface_tidb-0_1   ... done
Removing user-split-admin-interface_tidb-1_1   ... done
Removing network user-split-admin-interface_default
```

### 管理インターフェイスを使用してプロキシ ルールを構成する {#use-admin-interface-to-configure-proxy-rules}

サンプル ディレクトリに移動します。

```shell
cd example/proxy-rule-admin-interface
```

#### スクリプトで実行 {#run-with-script}

***ProxySQL Admin Interface***を使用して、異なる TiDB サーバーを使用して読み取りおよび書き込み SQL を実行する (一致しない場合は`default_hostgroup`を使用する) ようにプロキシ ルールを構成するには、次のコマンドを使用して`proxy-rule-split.sh`を実行します。

```shell
./proxy-rule-split.sh
```

#### ステップバイステップで実行 {#run-step-by-step}

前の`proxy-rule-split.sh`のスクリプトは、次のように段階的に実行できます。

1.  2 つの TiDB コンテナーと 1 つの ProxySQL インスタンスを開始します。

    ```shell
    docker-compose up -d
    ```

    -   `docker-compose`を使用して 2 つの TiDB コンテナーを開始します。コンテナー内のすべてのポートは`4000`で、ホスト ポートは`4001`と`4002`です。
    -   TiDB コンテナーを開始すると、ProxySQL インスタンスが開始されます。コンテナー内の***ProxySQL MySQL Interface***のポートは`6033`で、ホスト ポートは`6034`です。
    -   ***ProxySQL Admin Interface***のポートはコンテナ内でしかアクセスできないため公開されていません。
    -   プロセスの詳細については、 [`docker-compose.yaml`](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/example/proxy-rule-admin-interface/docker-compose.yaml)を参照してください。

2.  2 つの TiDB コンテナーで、TiDB インスタンスを区別するために、異なるデータ ( `'tidb-0'`と`'tidb-1'` ) を使用して同じテーブル スキーマを作成します。

    ```shell
    mysql -u root -h 127.0.0.1 -P 4001 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-0');
    EOF

    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    DROP TABLE IF EXISTS test.test;
    CREATE TABLE test.test (db VARCHAR(255));
    INSERT INTO test.test (db) VALUES ('tidb-1');
    EOF
    ```

3.  ***ProxySQL Admin Interface***で[`proxysql-prepare.sql`](https://github.com/Icemap/tidb-proxysql-integration-test/blob/main/example/proxy-rule-admin-interface/proxysql-prepare.sql)を実行するには、次のように`docker-compose exec`コマンドを実行します。

    ```shell
    docker-compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    上記の SQL ファイルが実行され、次の操作がトリガーされます。

    1.  2 つの TiDB サーバーのホストを追加します。 `hostgroup_id` of `tidb-0`は`0`で、 `hostgroup_id` of `tidb-1`は`1`です。

    2.  TiDB サーバーの構成を有効にして、ディスクに保存します。

    3.  空のパスワードでユーザー`root`を追加し、 `default_hostgroup`を`0`に設定します。これは、SQL がデフォルトで`tidb-0`にルーティングされることを示しています。

    4.  ユーザーの構成を有効にし、ディスクに保存します。

    5.  `rule_id`を`1`として、 `destination_hostgroup`を`0`として、ルール`^SELECT.*FOR UPDATE$`を追加します。 SQL ステートメントがこのルールに一致する場合、 `hostgroup`を`0`として TiDB サーバーを使用しました (このルールは、書き込まれたデータベースに`SELECT ... FOR UPDATE`を転送します)。

    6.  `rule_id`を`2`として、 `destination_hostgroup`を`1`として、ルール`^SELECT`を追加します。 SQL ステートメントがこのルールに一致する場合、 `hostgroup`を`1`として TiDB サーバーを使用します。

    7.  ルールの構成を有効にして、ディスクに保存します。

    > **ノート：**
    >
    > 一致ルールの詳細:
    >
    > -   ProxySQL は、最小から最大の順に`rule_id`つずつルールを照合しようとします。
    > -   `^`は SQL ステートメントの先頭に一致し、 `$`は末尾に一致します。
    > -   `match_digest`は、パラメーター化された SQL ステートメントに一致します。詳細については、 [query_processor_regex](https://proxysql.com/documentation/global-variables/mysql-variables/#mysql-query_processor_regex)を参照してください。
    > -   重要なパラメータ:
    >
    >     -   `digest` : パラメータ化されたハッシュ値と一致します。
    >     -   `match_pattern` : 生の SQL ステートメントに一致します。
    >     -   `negate_match_pattern` : 値を`1`に設定すると、 `match_digest`または`match_pattern`の一致が逆になります。
    >     -   `log` : クエリをログに記録するかどうか。
    >     -   `replace_pattern` : 空でない場合、これは一致したパターンを置き換えるパターンです。
    > -   完全なパラメーターについては、 [mysql_query_rules](https://proxysql.com/documentation/main-runtime/#mysql_query_rules)を参照してください。

4.  `root`ユーザーで***ProxySQL MySQL Interface***にログインします。

    ```shell
    mysql -u root -h 127.0.0.1 -P 6034
    ```

    次のステートメントを実行できます。

    -   `SELECT`ステートメント:

        ```sql
        SELECT * FROM test.test;
        ```

        ステートメントは、 `rule_id` of `2`でルールに一致し、 `hostgroup` of `1`でステートメントを TiDBサーバー`tidb-1`に転送することが期待されます。

    -   `SELECT ... FOR UPDATE`ステートメント:

        ```sql
        SELECT * FROM test.test for UPDATE;
        ```

        ステートメントは、 `rule_id` of `1`でルールに一致し、 `hostgroup` of `0`でステートメントを TiDBサーバー`tidb-0`に転送することが期待されます。

    -   取引：

        ```sql
        BEGIN;
        INSERT INTO test.test (db) VALUES ('insert this and rollback later');
        SELECT * FROM test.test;
        ROLLBACK;
        ```

        `BEGIN`ステートメントは、すべてのルールに一致しないことが予想されます。ユーザーの`default_hostgroup` (It is `0` ) を使用して、TiDBサーバー`tidb-0` ( `hostgroup` is `0` ) に転送します。また、ProxySQL はデフォルトでユーザー`transaction_persistent`を有効にします。これにより、同じトランザクション内のすべてのステートメントが同じ`hostgroup`で実行されます。したがって、 `INSERT`ステートメントと`SELECT * FROM test.test;`も TiDB サーバー`tidb-0`に転送されます ( `hostgroup`は`0`です)。

5.  コンテナーとネットワークを停止して削除するには、次のコマンドを使用できます。

    ```shell
    docker-compose down
    ```

#### 期待される出力 {#expected-output}

```
# ./proxy-rule-split.sh
Creating network "proxy-rule-admin-interface_default" with the default driver
Creating proxy-rule-admin-interface_tidb-1_1 ... done
Creating proxy-rule-admin-interface_tidb-0_1 ... done
Creating proxy-rule-admin-interface_proxysql_1 ... done
+--------+
| db     |
+--------+
| tidb-1 |
+--------+
+--------+
| db     |
+--------+
| tidb-0 |
+--------+
+--------------------------------+
| db                             |
+--------------------------------+
| tidb-0                         |
| insert this and rollback later |
+--------------------------------+
Stopping proxy-rule-admin-interface_proxysql_1 ... done
Stopping proxy-rule-admin-interface_tidb-0_1   ... done
Stopping proxy-rule-admin-interface_tidb-1_1   ... done
Removing proxy-rule-admin-interface_proxysql_1 ... done
Removing proxy-rule-admin-interface_tidb-0_1   ... done
Removing proxy-rule-admin-interface_tidb-1_1   ... done
Removing network proxy-rule-admin-interface_default
```

### 構成ファイルを使用して負荷分散を構成する {#use-the-configuration-file-to-configure-load-balancing}

構成ファイルを使用して負荷分散を構成するには、次のコマンドを使用して`test-load-balance.sh`を実行します。

```shell
cd example/load-balance-config-file
./test-load-balance.sh
```

期待される出力は[管理インターフェイスを使用して負荷分散を構成する](#use-the-configuration-file-to-configure-load-balancing)の出力と同じです。唯一の変更点は、構成ファイルを使用して ProxySQL 構成を初期化することです。

> **ノート：**
>
> -   ProxySQL の構成は SQLite に格納されます。構成ファイルは、SQLite が作成されていない場合にのみ使用されます。
> -   ***ProxySQL 管理インターフェイス***を介した構成では次の機能がサポートされているため、構成ファイルは初期化のみに使用し、構成アイテムの変更には使用しないことをお勧めします。
>
>     -   入力検証。
>     -   任意の MySQL クライアントによるリモート構成。
>     -   アップタイムを最大化するためのランタイム構成 (再起動する必要はありません)。
>     -   [ProxySQLクラスタ](https://proxysql.com/documentation/proxysql-cluster/)が構成されている場合、構成を他の ProxySQL ノードに伝搬します。
