---
title: Quick Start Guide for the TiDB Database Platform
summary: Learn how to quickly get started with the TiDB platform and see if TiDB is the right choice for you.
---

# TiDBデータベースプラットフォームのクイックスタートガイド {#quick-start-guide-for-the-tidb-database-platform}

このガイドでは、TiDBの使用を開始する最も簡単な方法について説明します。非実稼働環境の場合、次のいずれかの方法でTiDBデータベースをデプロイできます。

-   [ローカルテストクラスタをデプロイする](#deploy-a-local-test-cluster) （macOSおよびLinuxの場合）
-   [単一のマシンでの実稼働展開をシミュレートする](#simulate-production-deployment-on-a-single-machine) （Linuxのみ）

> **ノート：**
>
> -   TiDB、TiUP、およびTiDBダッシュボードは、使用法の詳細をPingCAPと共有して、製品を改善する方法を理解するのに役立ちます。共有される内容と共有を無効にする方法の詳細については、 [テレメトリー](/telemetry.md)を参照してください。
>
> -   このガイドで提供されている展開方法は、クイックスタート**のみ**を目的としており、本番環境向けではあり<strong>ません</strong>。
>
>     -   オンプレミスの本番クラスタをデプロイするには、 [本番インストールガイド](/production-deployment-using-tiup.md)を参照してください。
>     -   KubernetesにTiDBをデプロイするには、 [KubernetesでTiDBを使い始める](https://docs.pingcap.com/tidb-in-kubernetes/stable/get-started)を参照してください。
>     -   クラウドでTiDBを管理するには、 [TiDB Cloudクイックスタート](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart)を参照してください。

## ローカルテストクラスタをデプロイする {#deploy-a-local-test-cluster}

-   シナリオ：単一のmacOSまたはLinuxサーバーを使用してテストするために、ローカルTiDBクラスタをすばやくデプロイします。このようなクラスタをデプロイすることにより、TiDBの基本アーキテクチャと、TiDB、TiKV、PD、および監視コンポーネントなどのコンポーネントの操作を学習できます。

<SimpleTab>
<div label="macOS">

分散システムとして、基本的なTiDBテストクラスタは通常、2つのTiDBインスタンス、3つのTiKVインスタンス、3つのPDインスタンス、およびオプションのTiFlashインスタンスで構成されます。 TiUP Playgroundを使用すると、次の手順を実行してテストクラスタをすばやく構築できます。

1.  TiUPをダウンロードしてインストールします。

    {{< copyable "" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

    次のメッセージが表示された場合は、TiUPが正常にインストールされています。

    ```log
    Successfully set mirror to https://tiup-mirrors.pingcap.com
    Detected shell: zsh
    Shell profile:  /Users/user/.zshrc
    /Users/user/.zshrc has been modified to add tiup to PATH
    open a new terminal or source /Users/user/.zshrc to use it
    Installed path: /Users/user/.tiup/bin/tiup
    ===============================================
    Have a try:     tiup playground
    ===============================================
    ```

    上記の出力のシェルプロファイルパスに注意してください。次のステップでパスを使用する必要があります。

2.  グローバル環境変数を宣言します。

    > **ノート：**
    >
    > インストール後、TiUPは対応するシェルプロファイルファイルの絶対パスを表示します。パスに応じて、次の`source`のコマンドで`${your_shell_profile}`を変更する必要があります。この場合、 `${your_shell_profile}`はステップ1の出力からの`/Users/user/.zshrc`です。

    {{< copyable "" >}}

    ```shell
    source ${your_shell_profile}
    ```

3.  現在のセッションでクラスタを開始します。

    -   1つのTiDBインスタンス、1つのTiKVインスタンス、1つのPDインスタンス、および1つのTiFlashインスタンスを使用して最新バージョンのTiDBクラスタを起動する場合は、次のコマンドを実行します。

        {{< copyable "" >}}

        ```shell
        tiup playground
        ```

    -   TiDBのバージョンと各コンポーネントのインスタンス数を指定する場合は、次のようなコマンドを実行します。

        {{< copyable "" >}}

        ```shell
        tiup playground v6.1.0 --db 2 --pd 3 --kv 3
        ```

        このコマンドは、バージョンクラスタをローカルマシンにダウンロードして、v6.1.0などで起動します。最新バージョンを表示するには、 `tiup list tidb`を実行します。

        このコマンドは、クラスタのアクセスメソッドを返します。

        ```log
        CLUSTER START SUCCESSFULLY, Enjoy it ^-^
        To connect TiDB: mysql --comments --host 127.0.0.1 --port 4001 -u root -p (no password)
        To connect TiDB: mysql --comments --host 127.0.0.1 --port 4000 -u root -p (no password)
        To view the dashboard: http://127.0.0.1:2379/dashboard
        PD client endpoints: [127.0.0.1:2379 127.0.0.1:2382 127.0.0.1:2384]
        To view Prometheus: http://127.0.0.1:9090
        To view Grafana: http://127.0.0.1:3000
        ```

        > **ノート：**
        >
        > -   v5.2.0以降、TiDBはAppleM1チップを使用するマシンでの`tiup playground`の実行をサポートします。
        > -   このように操作された遊び場の場合、テスト展開が終了した後、TiUPは元のクラスタデータをクリーンアップします。コマンドを再実行すると、新しいクラスタが作成されます。
        > -   データをストレージに永続化する場合は、 `tiup --tag <your-tag> playground ...`を実行します。詳しくは[TiUPリファレンスガイド](/tiup/tiup-reference.md#-t---tag)をご覧ください。

4.  TiDBにアクセスするための新しいセッションを開始します。

    -   TiUPクライアントを使用してTiDBに接続します。

        {{< copyable "" >}}

        ```shell
        tiup client
        ```

    -   MySQLクライアントを使用してTiDBに接続することもできます。

        {{< copyable "" >}}

        ```shell
        mysql --host 127.0.0.1 --port 4000 -u root
        ```

5.  [http://127.0.0.1:9090](http://127.0.0.1:9090)でTiDBのPrometheusダッシュボードにアクセスします。

6.  [http://127.0.0.1:2379/dashboard](http://127.0.0.1:2379/dashboard)にアクセスし[TiDBダッシュボード](/dashboard/dashboard-intro.md) 。デフォルトのユーザー名は`root`で、パスワードは空です。

7.  [http://127.0.0.1:3000](http://127.0.0.1:3000)を介してTiDBのGrafanaダッシュボードにアクセスします。デフォルトのユーザー名とパスワードはどちらも`admin`です。

8.  （オプション）分析用に[TiFlashにデータをロードする](/tiflash/tiflash-overview.md#use-tiflash) 。

9.  テスト展開後にクラスタをクリーンアップします。

    1.  <kbd>Control + C</kbd>を押して、上記のTiDBサービスを停止します。

    2.  サービスが停止した後、次のコマンドを実行します。

        {{< copyable "" >}}

        ```shell
        tiup clean --all
        ```

> **ノート：**
>
> TiUP Playgroundはデフォルトで`127.0.0.1`をリッスンし、サービスはローカルでのみアクセス可能です。サービスを外部からアクセスできるようにする場合は、 `--host`パラメーターを使用してリスニングアドレスを指定し、ネットワークインターフェイスカード（NIC）を外部からアクセス可能なIPアドレスにバインドします。

</div>
<div label="Linux">

分散システムとして、基本的なTiDBテストクラスタは通常、2つのTiDBインスタンス、3つのTiKVインスタンス、3つのPDインスタンス、およびオプションのTiFlashインスタンスで構成されます。 TiUP Playgroundを使用すると、次の手順を実行してテストクラスタをすばやく構築できます。

1.  TiUPをダウンロードしてインストールします。

    {{< copyable "" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

    次のメッセージが表示された場合は、TiUPが正常にインストールされています。

    ```log
    Successfully set mirror to https://tiup-mirrors.pingcap.com
    Detected shell: zsh
    Shell profile:  /Users/user/.zshrc
    /Users/user/.zshrc has been modified to add tiup to PATH
    open a new terminal or source /Users/user/.zshrc to use it
    Installed path: /Users/user/.tiup/bin/tiup
    ===============================================
    Have a try:     tiup playground
    ===============================================
    ```

    上記の出力のシェルプロファイルパスに注意してください。次のステップでパスを使用する必要があります。

2.  グローバル環境変数を宣言します。

    > **ノート：**
    >
    > インストール後、TiUPは対応するシェルプロファイルファイルの絶対パスを表示します。パスに応じて、次の`source`のコマンドで`${your_shell_profile}`を変更する必要があります。

    {{< copyable "" >}}

    ```shell
    source ${your_shell_profile}
    ```

3.  現在のセッションでクラスタを開始します。

    -   1つのTiDBインスタンス、1つのTiKVインスタンス、1つのPDインスタンス、および1つのTiFlashインスタンスを使用して最新バージョンのTiDBクラスタを起動する場合は、次のコマンドを実行します。

        {{< copyable "" >}}

        ```shell
        tiup playground
        ```

    -   TiDBのバージョンと各コンポーネントのインスタンス数を指定する場合は、次のようなコマンドを実行します。

        {{< copyable "" >}}

        ```shell
        tiup playground v6.1.0 --db 2 --pd 3 --kv 3
        ```

        このコマンドは、バージョンクラスタをローカルマシンにダウンロードして、v6.1.0などで起動します。最新バージョンを表示するには、 `tiup list tidb`を実行します。

        このコマンドは、クラスタのアクセスメソッドを返します。

        ```log
        CLUSTER START SUCCESSFULLY, Enjoy it ^-^
        To connect TiDB: mysql --host 127.0.0.1 --port 4000 -u root -p (no password) --comments
        To view the dashboard: http://127.0.0.1:2379/dashboard
        PD client endpoints: [127.0.0.1:2379]
        To view the Prometheus: http://127.0.0.1:9090
        To view the Grafana: http://127.0.0.1:3000
        ```

        > **ノート：**
        >
        > このように操作された遊び場の場合、テスト展開が終了した後、TiUPは元のクラスタデータをクリーンアップします。コマンドを再実行すると、新しいクラスタが作成されます。データをストレージに永続化する場合は、 `tiup --tag <your-tag> playground ...`を実行します。詳しくは[TiUPリファレンスガイド](/tiup/tiup-reference.md#-t---tag)をご覧ください。

4.  TiDBにアクセスするための新しいセッションを開始します。

    -   TiUPクライアントを使用してTiDBに接続します。

        {{< copyable "" >}}

        ```shell
        tiup client
        ```

    -   MySQLクライアントを使用してTiDBに接続することもできます。

        {{< copyable "" >}}

        ```shell
        mysql --host 127.0.0.1 --port 4000 -u root
        ```

5.  [http://127.0.0.1:9090](http://127.0.0.1:9090)でTiDBのPrometheusダッシュボードにアクセスします。

6.  [http://127.0.0.1:2379/dashboard](http://127.0.0.1:2379/dashboard)にアクセスし[TiDBダッシュボード](/dashboard/dashboard-intro.md) 。デフォルトのユーザー名は`root`で、パスワードは空です。

7.  [http://127.0.0.1:3000](http://127.0.0.1:3000)を介してTiDBのGrafanaダッシュボードにアクセスします。デフォルトのユーザー名とパスワードはどちらも`admin`です。

8.  （オプション）分析用に[TiFlashにデータをロードする](/tiflash/tiflash-overview.md#use-tiflash) 。

9.  テスト展開後にクラスタをクリーンアップします。

    1.  <kbd>Control+C</kbd>を押してプロセスを停止します。

    2.  サービスが停止した後、次のコマンドを実行します。

        {{< copyable "" >}}

        ```shell
        tiup clean --all
        ```

> **ノート：**
>
> TiUP Playgroundはデフォルトで`127.0.0.1`をリッスンし、サービスはローカルでのみアクセス可能です。サービスを外部からアクセスできるようにする場合は、 `--host`パラメーターを使用してリスニングアドレスを指定し、ネットワークインターフェイスカード（NIC）を外部からアクセス可能なIPアドレスにバインドします。

</div>
</SimpleTab>

## 単一のマシンでの実稼働展開をシミュレートする {#simulate-production-deployment-on-a-single-machine}

-   シナリオ：完全なトポロジを備えた最小のTiDBクラスタを体験し、単一のLinuxサーバーでの運用展開手順をシミュレートします。

このセクションでは、TiUPで最小のトポロジのYAMLファイルを使用してTiDBクラスタをデプロイする方法について説明します。

### 準備 {#prepare}

次の要件を満たすターゲットマシンを準備します。

-   CentOS7.3以降のバージョンがインストールされている
-   Linux OSはインターネットにアクセスできます。インターネットは、TiDBおよび関連するソフトウェアインストールパッケージをダウンロードするために必要です。

最小のTiDBクラスタトポロジは次のとおりです。

> **ノート：**
>
> 次のインスタンスのIPアドレスは、IPの例としてのみ機能します。実際の展開では、IPを実際のIPに置き換える必要があります。

| 実例      | カウント | IP                                   | Configuration / コンフィグレーション  |
| :------ | :--- | :----------------------------------- | :-------------------------- |
| TiKV    | 3    | 10.0.1.1<br/> 10.0.1.1<br/> 10.0.1.1 | ポートとディレクトリ間の競合を回避する         |
| TiDB    | 1    | 10.0.1.1                             | デフォルトのポート<br/>グローバルディレクトリ構成 |
| PD      | 1    | 10.0.1.1                             | デフォルトのポート<br/>グローバルディレクトリ構成 |
| TiFlash | 1    | 10.0.1.1                             | デフォルトのポート<br/>グローバルディレクトリ構成 |
| モニター    | 1    | 10.0.1.1                             | デフォルトのポート<br/>グローバルディレクトリ構成 |

ターゲットマシンのその他の要件：

-   `root`人のユーザーとそのパスワードが必要です
-   [ターゲットマシンのファイアウォールサービスを停止します](/check-before-deployment.md#check-and-stop-the-firewall-service-of-target-machines) 、またはTiDBクラスタノードに必要なポートを開きます
-   現在、TiUPクラスタはx86_64（AMD64）およびARMアーキテクチャーへのTiDBのデプロイをサポートしています。

    -   AMD64ではCentOS7.3以降のバージョンを使用することをお勧めします
    -   ARMではCentOS7.61810を使用することをお勧めします

### デプロイ {#deploy}

> **ノート：**
>
> 通常のユーザーまたは`root`人のユーザーとしてターゲットマシンにログインできます。次の手順では、例として`root`ユーザーを使用します。

1.  TiUPをダウンロードしてインストールします。

    {{< copyable "" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2.  グローバル環境変数を宣言します。

    > **ノート：**
    >
    > インストール後、TiUPは対応するシェルプロファイルファイルの絶対パスを表示します。パスに応じて、次の`source`のコマンドで`${your_shell_profile}`を変更する必要があります。

    {{< copyable "" >}}

    ```shell
    source ${your_shell_profile}
    ```

3.  TiUPのクラスタコンポーネントをインストールします。

    {{< copyable "" >}}

    ```shell
    tiup cluster
    ```

4.  TiUPクラスタがすでにマシンにインストールされている場合は、ソフトウェアバージョンを更新します。

    {{< copyable "" >}}

    ```shell
    tiup update --self && tiup update cluster
    ```

5.  rootユーザー特権を使用して、 `sshd`のサービスの接続制限を増やします。これは、TiUPが複数のマシンでの展開をシミュレートする必要があるためです。

    1.  `/etc/ssh/sshd_config`を変更し、 `MaxSessions`を`20`に設定します。
    2.  `sshd`のサービスを再起動します。

        {{< copyable "" >}}

        ```shell
        service sshd restart
        ```

6.  クラスタを作成して開始します。

    次のテンプレートに従って構成ファイルを編集し、 `topo.yaml`という名前を付けます。

    {{< copyable "" >}}

    ```yaml
    # # Global variables are applied to all deployments and used as the default value of
    # # the deployments if a specific deployment value is missing.
    global:
     user: "tidb"
     ssh_port: 22
     deploy_dir: "/tidb-deploy"
     data_dir: "/tidb-data"

    # # Monitored variables are applied to all the machines.
    monitored:
     node_exporter_port: 9100
     blackbox_exporter_port: 9115

    server_configs:
     tidb:
       log.slow-threshold: 300
     tikv:
       readpool.storage.use-unified-pool: false
       readpool.coprocessor.use-unified-pool: true
     pd:
       replication.enable-placement-rules: true
       replication.location-labels: ["host"]
     tiflash:
       logger.level: "info"

    pd_servers:
     - host: 10.0.1.1

    tidb_servers:
     - host: 10.0.1.1

    tikv_servers:
     - host: 10.0.1.1
       port: 20160
       status_port: 20180
       config:
         server.labels: { host: "logic-host-1" }

     - host: 10.0.1.1
       port: 20161
       status_port: 20181
       config:
         server.labels: { host: "logic-host-2" }

     - host: 10.0.1.1
       port: 20162
       status_port: 20182
       config:
         server.labels: { host: "logic-host-3" }

    tiflash_servers:
     - host: 10.0.1.1

    monitoring_servers:
     - host: 10.0.1.1

    grafana_servers:
     - host: 10.0.1.1
    ```

    -   `user: "tidb"` ： `tidb`システムユーザー（展開時に自動的に作成されます）を使用して、クラスタの内部管理を実行します。デフォルトでは、ポート22を使用してSSH経由でターゲットマシンにログインします。
    -   `replication.enable-placement-rules` ：このPDパラメータは、TiFlashが正常に動作することを保証するために設定されます。
    -   `host` ：ターゲットマシンのIP。

7.  clusterdeploymentコマンドを実行しクラスタ。

    {{< copyable "" >}}

    ```shell
    tiup cluster deploy <cluster-name> <tidb-version> ./topo.yaml --user root -p
    ```

    -   `<cluster-name>` ：クラスタ名を設定します
    -   `<tidb-version>` ：TiDBクラスタのバージョンを設定します。 `tiup list tidb`コマンドを実行すると、サポートされているすべてのTiDBバージョンを確認できます。
    -   `-p` ：ターゲットマシンへの接続に使用するパスワードを指定します。

        > **ノート：**
        >
        > 秘密鍵を使用する場合は、 `-i`を介して鍵のパスを指定できます。 `-i`と`-p`を同時に使用しないでください。

    「y」と`root`人のユーザーのパスワードを入力して、展開を完了します。

    ```log
    Do you want to continue? [y/N]:  y
    Input SSH password:
    ```

8.  クラスタを開始します：

    {{< copyable "" >}}

    ```shell
    tiup cluster start <cluster-name>
    ```

9.  クラスタにアクセスします。

    -   MySQLクライアントをインストールします。すでにインストールされている場合は、この手順をスキップしてください。

        {{< copyable "" >}}

        ```shell
        yum -y install mysql
        ```

    -   TiDBにアクセスします。パスワードは空です：

        {{< copyable "" >}}

        ```shell
        mysql -h 10.0.1.1 -P 4000 -u root
        ```

    -   [http：// {grafana-ip}：3000](http://%7Bgrafana-ip%7D:3000)でGrafanaモニタリングダッシュボードにアクセスします。デフォルトのユーザー名とパスワードはどちらも`admin`です。

    -   [http：// {pd-ip}：2379 / dashboard](http://%7Bpd-ip%7D:2379/dashboard)にアクセスし[TiDBダッシュボード](/dashboard/dashboard-intro.md) 。デフォルトのユーザー名は`root`で、パスワードは空です。

    -   現在デプロイされているクラスタリストを表示するには：

        {{< copyable "" >}}

        ```shell
        tiup cluster list
        ```

    -   クラスタのトポロジとステータスを表示するには：

        {{< copyable "" >}}

        ```shell
        tiup cluster display <cluster-name>
        ```

## 次は何ですか {#what-s-next}

-   ローカルテスト環境にTiDBクラスタをデプロイしたばかりの場合：

    -   学ぶ[TiDBでの基本的なSQL操作](/basic-sql-operations.md)
    -   [データをTiDBに移行する](/migration-overview.md)

-   実稼働環境にTiDBクラスタをデプロイする準備ができている場合：

    -   [TiUPを使用してTiDBをデプロイ](/production-deployment-using-tiup.md)
    -   [TiDB Operatorを使用してクラウドにTiDBをデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/stable)

-   TiFlashを使用した分析ソリューションをお探しの場合：

    -   [TiFlashを使用する](/tiflash/tiflash-overview.md#use-tiflash)
    -   [TiFlashの概要](/tiflash/tiflash-overview.md)
