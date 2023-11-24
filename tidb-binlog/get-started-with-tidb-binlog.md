---
title: TiDB Binlog Tutorial
summary: Learn to deploy TiDB Binlog with a simple TiDB cluster.
---

# TiDBBinlogのチュートリアル {#tidb-binlog-tutorial}

このチュートリアルは、MariaDB サーバー インスタンスにデータをプッシュするように設定された、各コンポーネント(Placement Driver、TiKV Server、TiDB Server、 Pump、およびDrainer ) の単一ノードを備えた単純な TiDB Binlogデプロイメントから始まります。

このチュートリアルは、 [TiDBアーキテクチャ](/tidb-architecture.md)にある程度の知識があり、すでに TiDB クラスターをセットアップしている可能性があり (必須ではありません)、TiDB Binlogの実践的な経験を積みたいと考えているユーザーを対象としています。このチュートリアルは、TiDB Binlogを「試して」、そのアーキテクチャの概念に慣れるための良い方法です。

> **警告：**
>
> このチュートリアルの TiDB をデプロイする手順は、本番または開発設定で TiDB をデプロイするために使用し**ない**でください。

このチュートリアルは、x86-64 上の最新の Linux ディストリビューションを使用していることを前提としています。このチュートリアルでは例として、VMware で実行されている最小限の CentOS 7 インストールを使用します。既存の環境の癖の影響を受けないよう、クリーン インストールから始めることをお勧めします。ローカル仮想化を使用したくない場合は、クラウド サービスを使用して CentOS 7 VM を簡単に起動できます。

## TiDBBinlogの概要 {#tidb-binlog-overview}

TiDB Binlog は、 TiDB からバイナリ ログ データを収集し、リアルタイムのデータ バックアップとレプリケーションを提供するソリューションです。これは、増分データ更新を TiDB サーバー クラスターからダウンストリーム プラットフォームにプッシュします。

TiDB Binlog を増分バックアップに使用したり、ある TiDB クラスターから別の TiDB クラスターにデータをレプリケートしたり、Kafka を介して選択したダウンストリーム プラットフォームに TiDB 更新を送信したりできます。

TiDB Binlog は、MySQL または MariaDB から TiDB にデータを移行する場合に特に便利です。この場合、TiDB DM (データ移行) プラットフォームを使用して MySQL/MariaDB クラスターから TiDB にデータを取得し、TiDB Binlogを使用してTiDB クラスターと同期する別のダウンストリーム MySQL/MariaDB インスタンス/クラスター。 TiDB Binlog を使用すると、TiDB へのアプリケーション トラフィックをダウンストリームの MySQL または MariaDB インスタンス/クラスターにプッシュできるようになります。これにより、ダウンタイムやデータ損失なしにアプリケーションを MySQL または MariaDB に簡単に戻すことができるため、TiDB への移行のリスクが軽減されます。

詳細については[TiDBBinlogクラスタユーザー ガイド](/tidb-binlog/tidb-binlog-overview.md)参照してください。

## アーキテクチャ {#architecture}

TiDB Binlog は、**Pump**と**Drainerの**2 つのコンポーネントで構成されます。いくつかのPumpノードがポンプ クラスターを構成します。各Pumpノードは TiDB サーバー インスタンスに接続し、クラスター内の各 TiDB サーバー インスタンスに対して行われた更新を受け取ります。 Drainer は、 Pumpクラスターに接続し、受信した更新を特定のダウンストリーム宛先 (たとえば、Kafka、別の TiDBクラスタ、または MySQL/MariaDBサーバー)用の正しい形式に変換します。

![TiDB-Binlog architecture](/media/tidb-binlog-cluster-architecture.png)

Pumpのクラスター化アーキテクチャ、新しい TiDB サーバー インスタンスが TiDBクラスタに参加または TiDB クラスターから離脱したり、PumpノードがPumpクラスターに参加または離脱したりしても、更新が失われることはありません。

## インストール {#installation}

RHEL/CentOS 7 にはデフォルトのパッケージ リポジトリに MariaDB サーバーが含まれているため、この例では MySQL Server の代わりに MariaDB Server を使用しています。後で使用するためにサーバーだけでなくクライアントも必要になります。今すぐインストールしてみましょう:

```bash
sudo yum install -y mariadb-server
```

```bash
curl -L https://download.pingcap.org/tidb-community-server-v7.1.2-linux-amd64.tar.gz | tar xzf -
cd tidb-latest-linux-amd64
```

期待される出力:

    [kolbe@localhost ~]$ curl -LO https://download.pingcap.org/tidb-latest-linux-amd64.tar.gz | tar xzf -
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100  368M  100  368M    0     0  8394k      0  0:00:44  0:00:44 --:--:-- 11.1M
    [kolbe@localhost ~]$ cd tidb-latest-linux-amd64
    [kolbe@localhost tidb-latest-linux-amd64]$

## コンフィグレーション {#configuration}

次に、 `pd-server` 、 `tikv-server` 、および`tidb-server`のそれぞれに 1 つのインスタンスを持つ単純な TiDB クラスターを開始します。

以下を使用して構成ファイルを設定します。

```bash
printf > pd.toml %s\\n 'log-file="pd.log"' 'data-dir="pd.data"'
printf > tikv.toml %s\\n 'log-file="tikv.log"' '[storage]' 'data-dir="tikv.data"' '[pd]' 'endpoints=["127.0.0.1:2379"]' '[rocksdb]' max-open-files=1024 '[raftdb]' max-open-files=1024
printf > pump.toml %s\\n 'log-file="pump.log"' 'data-dir="pump.data"' 'addr="127.0.0.1:8250"' 'advertise-addr="127.0.0.1:8250"' 'pd-urls="http://127.0.0.1:2379"'
printf > tidb.toml %s\\n 'store="tikv"' 'path="127.0.0.1:2379"' '[log.file]' 'filename="tidb.log"' '[binlog]' 'enable=true'
printf > drainer.toml %s\\n 'log-file="drainer.log"' '[syncer]' 'db-type="mysql"' '[syncer.to]' 'host="127.0.0.1"' 'user="root"' 'password=""' 'port=3306'
```

構成の詳細を確認するには、次のコマンドを使用します。

```bash
for f in *.toml; do echo "$f:"; cat "$f"; echo; done
```

期待される出力:

    drainer.toml:
    log-file="drainer.log"
    [syncer]
    db-type="mysql"
    [syncer.to]
    host="127.0.0.1"
    user="root"
    password=""
    port=3306

    pd.toml:
    log-file="pd.log"
    data-dir="pd.data"

    pump.toml:
    log-file="pump.log"
    data-dir="pump.data"
    addr="127.0.0.1:8250"
    advertise-addr="127.0.0.1:8250"
    pd-urls="http://127.0.0.1:2379"

    tidb.toml:
    store="tikv"
    path="127.0.0.1:2379"
    [log.file]
    filename="tidb.log"
    [binlog]
    enable=true

    tikv.toml:
    log-file="tikv.log"
    [storage]
    data-dir="tikv.data"
    [pd]
    endpoints=["127.0.0.1:2379"]
    [rocksdb]
    max-open-files=1024
    [raftdb]
    max-open-files=1024

## ブートストラッピング {#bootstrapping}

これで、各コンポーネントを開始できるようになりました。これは特定の順序で実行するのが最適です。最初に配置Driver(PD)、次に TiKV サーバー、次にPump(TiDB はバイナリ ログを送信するためにPumpサービスに接続する必要があるため)、最後に TiDB サーバーです。

以下を使用してすべてのサービスを開始します。

```bash
./bin/pd-server --config=pd.toml &>pd.out &
./bin/tikv-server --config=tikv.toml &>tikv.out &
./pump --config=pump.toml &>pump.out &
sleep 3
./bin/tidb-server --config=tidb.toml &>tidb.out &
```

期待される出力:

    [kolbe@localhost tidb-latest-linux-amd64]$ ./bin/pd-server --config=pd.toml &>pd.out &
    [1] 20935
    [kolbe@localhost tidb-latest-linux-amd64]$ ./bin/tikv-server --config=tikv.toml &>tikv.out &
    [2] 20944
    [kolbe@localhost tidb-latest-linux-amd64]$ ./pump --config=pump.toml &>pump.out &
    [3] 21050
    [kolbe@localhost tidb-latest-linux-amd64]$ sleep 3
    [kolbe@localhost tidb-latest-linux-amd64]$ ./bin/tidb-server --config=tidb.toml &>tidb.out &
    [4] 21058

`jobs`を実行すると、実行中のデーモンのリストが表示されます。

    [kolbe@localhost tidb-latest-linux-amd64]$ jobs
    [1]   Running                 ./bin/pd-server --config=pd.toml &>pd.out &
    [2]   Running                 ./bin/tikv-server --config=tikv.toml &>tikv.out &
    [3]-  Running                 ./pump --config=pump.toml &>pump.out &
    [4]+  Running                 ./bin/tidb-server --config=tidb.toml &>tidb.out &

いずれかのサービスの開始に失敗した場合 (たとえば、「 `Running` 」ではなく「 `Exit 1` 」が表示された場合)、その個別のサービスを再起動してみてください。

## 接続中 {#connecting}

これで TiDBクラスタの 4 つのコンポーネントがすべて実行され、MariaDB/MySQL コマンドライン クライアントを使用してポート 4000 で TiDB サーバーに接続できるようになりました。

```bash
mysql -h 127.0.0.1 -P 4000 -u root -e 'select tidb_version()\G'
```

期待される出力:

    [kolbe@localhost tidb-latest-linux-amd64]$ mysql -h 127.0.0.1 -P 4000 -u root -e 'select tidb_version()\G'
    *************************** 1. row ***************************
    tidb_version(): Release Version: v3.0.0-beta.1-154-gd5afff70c
    Git Commit Hash: d5afff70cdd825d5fab125c8e52e686cc5fb9a6e
    Git Branch: master
    UTC Build Time: 2019-04-24 03:10:00
    GoVersion: go version go1.12 linux/amd64
    Race Enabled: false
    TiKV Min Version: 2.1.0-alpha.1-ff3dd160846b7d1aed9079c389fc188f7f5ea13e
    Check Table Before Drop: false

この時点で、TiDBクラスタが実行されており、クラスターから`pump`ログを読み取り、データ ディレクトリにリレー ログとして保存しています。次のステップは、 `drainer`可能な MariaDBサーバーを起動することです。

以下を使用して`drainer`を開始します。

```bash
sudo systemctl start mariadb
./drainer --config=drainer.toml &>drainer.out &
```

MySQLサーバーのインストールが容易なオペレーティング システムを使用している場合でも、それは問題ありません。ポート 3306 でリッスンしていること、および空のパスワードを使用してユーザー「root」として接続できること、または必要に応じてdrainer.toml を調整できることを確認してください。

```bash
mysql -h 127.0.0.1 -P 3306 -u root
```

```sql
show databases;
```

期待される出力:

    [kolbe@localhost ~]$ mysql -h 127.0.0.1 -P 3306 -u root
    Welcome to the MariaDB monitor.  Commands end with ; or \g.
    Your MariaDB connection id is 20
    Server version: 5.5.60-MariaDB MariaDB Server

    Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    MariaDB [(none)]> show databases;
    +--------------------+
    | Database           |
    +--------------------+
    | information_schema |
    | mysql              |
    | performance_schema |
    | test               |
    | tidb_binlog        |
    +--------------------+
    5 rows in set (0.01 sec)

ここではすでに`tidb_binlog`データベースが確認できます。このデータベースには、TiDB クラスターからのバイナリ ログが適用された時点までを記録するために`drainer`によって使用される`checkpoint`テーブルが含まれています。

```sql
MariaDB [tidb_binlog]> use tidb_binlog;
Database changed
MariaDB [tidb_binlog]> select * from checkpoint;
+---------------------+---------------------------------------------+
| clusterID           | checkPoint                                  |
+---------------------+---------------------------------------------+
| 6678715361817107733 | {"commitTS":407637466476445697,"ts-map":{}} |
+---------------------+---------------------------------------------+
1 row in set (0.00 sec)
```

ここで、TiDBサーバーへの別のクライアント接続を開いて、テーブルを作成してそこにいくつかの行を挿入しましょう。 (複数のクライアントを同時に開いたままにできるように、GNU 画面でこれを実行することをお勧めします。)

```bash
mysql -h 127.0.0.1 -P 4000 --prompt='TiDB [\d]> ' -u root
```

```sql
create database tidbtest;
use tidbtest;
create table t1 (id int unsigned not null AUTO_INCREMENT primary key);
insert into t1 () values (),(),(),(),();
select * from t1;
```

期待される出力:

    TiDB [(none)]> create database tidbtest;
    Query OK, 0 rows affected (0.12 sec)

    TiDB [(none)]> use tidbtest;
    Database changed
    TiDB [tidbtest]> create table t1 (id int unsigned not null AUTO_INCREMENT primary key);
    Query OK, 0 rows affected (0.11 sec)

    TiDB [tidbtest]> insert into t1 () values (),(),(),(),();
    Query OK, 5 rows affected (0.01 sec)
    Records: 5  Duplicates: 0  Warnings: 0

    TiDB [tidbtest]> select * from t1;
    +----+
    | id |
    +----+
    |  1 |
    |  2 |
    |  3 |
    |  4 |
    |  5 |
    +----+
    5 rows in set (0.00 sec)

MariaDB クライアントに戻ると、新しいデータベース、新しいテーブル、および新しく挿入された行が見つかるはずです。

```sql
use tidbtest;
show tables;
select * from t1;
```

期待される出力:

    MariaDB [(none)]> use tidbtest;
    Reading table information for completion of table and column names
    You can turn off this feature to get a quicker startup with -A

    Database changed
    MariaDB [tidbtest]> show tables;
    +--------------------+
    | Tables_in_tidbtest |
    +--------------------+
    | t1                 |
    +--------------------+
    1 row in set (0.00 sec)

    MariaDB [tidbtest]> select * from t1;
    +----+
    | id |
    +----+
    |  1 |
    |  2 |
    |  3 |
    |  4 |
    |  5 |
    +----+
    5 rows in set (0.00 sec)

MariaDBサーバーにクエリを実行するときに、TiDB に挿入したのと同じ行が表示されるはずです。おめでとう！ TiDB Binlog のセットアップが完了しました。

## binlogctl {#binlogctl}

クラスターに参加したポンプとドレーナーの情報は PD に保存されます。 binlogctl ツールのクエリを使用して、それらの状態に関する情報を操作できます。詳細については[binlogctl ガイド](/tidb-binlog/binlog-control.md)参照してください。

クラスター内のポンプとドレイナーの現在のステータスを表示するには、 `binlogctl`を使用します。

```bash
./binlogctl -cmd drainers
./binlogctl -cmd pumps
```

期待される出力:

    [kolbe@localhost tidb-latest-linux-amd64]$ ./binlogctl -cmd drainers
    [2019/04/11 17:44:10.861 -04:00] [INFO] [nodes.go:47] ["query node"] [type=drainer] [node="{NodeID: localhost.localdomain:8249, Addr: 192.168.236.128:8249, State: online, MaxCommitTS: 407638907719778305, UpdateTime: 2019-04-11 17:44:10 -0400 EDT}"]

    [kolbe@localhost tidb-latest-linux-amd64]$ ./binlogctl -cmd pumps
    [2019/04/11 17:44:13.904 -04:00] [INFO] [nodes.go:47] ["query node"] [type=pump] [node="{NodeID: localhost.localdomain:8250, Addr: 192.168.236.128:8250, State: online, MaxCommitTS: 407638914024079361, UpdateTime: 2019-04-11 17:44:13 -0400 EDT}"]

Drainer を強制終了すると、クラスターはその Drainer を「一時停止」状態にします。これは、クラスターが Drainer の再参加を期待していることを意味します。

```bash
pkill drainer
./binlogctl -cmd drainers
```

期待される出力:

    [kolbe@localhost tidb-latest-linux-amd64]$ pkill drainer
    [kolbe@localhost tidb-latest-linux-amd64]$ ./binlogctl -cmd drainers
    [2019/04/11 17:44:22.640 -04:00] [INFO] [nodes.go:47] ["query node"] [type=drainer] [node="{NodeID: localhost.localdomain:8249, Addr: 192.168.236.128:8249, State: paused, MaxCommitTS: 407638915597467649, UpdateTime: 2019-04-11 17:44:18 -0400 EDT}"]

「NodeID」に`binlogctl`を指定すると、個々のノードを制御できます。この場合、drainerの NodeID は「localhost.localdomain:8249」、Pumpの NodeID は「localhost.localdomain:8250」です。

このチュートリアルでの`binlogctl`の主な使用は、クラスターの再起動の場合に行われる可能性があります。 TiDB クラスター内のすべてのプロセスを終了し、(ダウンストリームの MySQL/MariaDBサーバーまたはDrainerを除く) 再起動しようとすると、 PumpはDrainerに接続できず、 Drainerがまだ「オンライン」であると信じているため、起動を拒否します。

この問題には 3 つの解決策があります。

-   プロセスを強制終了する代わりに`binlogctl`を使用してDrainerを停止します。

        ./binlogctl --pd-urls=http://127.0.0.1:2379 --cmd=drainers
        ./binlogctl --pd-urls=http://127.0.0.1:2379 --cmd=offline-drainer --node-id=localhost.localdomain:8249

-   Pumpを始動する*前に*Drainerを始動してください。

-   PD の開始後 (ただし、 DrainerとPumpの開始前) に`binlogctl`を使用して、一時停止したDrainerの状態を更新します。

        ./binlogctl --pd-urls=http://127.0.0.1:2379 --cmd=update-drainer --node-id=localhost.localdomain:8249 --state=offline

## 掃除 {#cleanup}

TiDB クラスターおよび TiDB Binlogプロセスを停止するには、クラスターを形成するすべてのプロセス (pd-server、tikv-server、pump、tidb-server、 drainer) を開始したシェルで`pkill -P $$`を実行します。各コンポーネントを正常にシャットダウンするのに十分な時間を与えるには、特定の順序でコンポーネントを停止すると便利です。

```bash
for p in tidb-server drainer pump tikv-server pd-server; do pkill "$p"; sleep 1; done
```

期待される出力:

    kolbe@localhost tidb-latest-linux-amd64]$ for p in tidb-server drainer pump tikv-server pd-server; do pkill "$p"; sleep 1; done
    [4]-  Done                    ./bin/tidb-server --config=tidb.toml &>tidb.out
    [5]+  Done                    ./drainer --config=drainer.toml &>drainer.out
    [3]+  Done                    ./pump --config=pump.toml &>pump.out
    [2]+  Done                    ./bin/tikv-server --config=tikv.toml &>tikv.out
    [1]+  Done                    ./bin/pd-server --config=pd.toml &>pd.out

すべてのサービスが終了した後にクラスターを再起動する場合は、最初にサービスを開始するために実行したのと同じコマンドを使用します。上記の[`binlogctl`](#binlogctl)セクションで説明したように、 `pump`の前に`drainer`開始し、 `tidb-server`の前に`pump`を開始する必要があります。

```bash
./bin/pd-server --config=pd.toml &>pd.out &
./bin/tikv-server --config=tikv.toml &>tikv.out &
./drainer --config=drainer.toml &>drainer.out &
sleep 3
./pump --config=pump.toml &>pump.out &
sleep 3
./bin/tidb-server --config=tidb.toml &>tidb.out &
```

いずれかのコンポーネントの起動に失敗した場合は、失敗した個々のコンポーネントを再起動してみてください。

## 結論 {#conclusion}

このチュートリアルでは、単一のPumpと単一のDrainerを持つクラスターを使用して、TiDB クラスターからダウンストリームの MariaDBサーバーにレプリケートするように TiDB Binlogをセットアップしました。これまで見てきたように、TiDB Binlog は、TiDB クラスターへの変更をキャプチャして処理するための包括的なプラットフォームです。

より堅牢な開発、テスト、または本番環境では、高可用性とスケーリングを目的として複数の TiDB サーバーを使用し、複数のPumpインスタンスを使用して、TiDBサーバーインスタンスへのアプリケーション トラフィックがPumpの問題の影響を受けないようにします。集まる。追加のDrainerインスタンスを使用して、更新を別のダウンストリーム プラットフォームにプッシュしたり、増分バックアップを実装したりすることもできます。
