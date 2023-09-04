---
title: Quick Start Guide for the TiDB Database Platform
summary: Learn how to quickly get started with the TiDB platform and see if TiDB is the right choice for you.
---

# TiDB データベース プラットフォームのクイック スタート ガイド {#quick-start-guide-for-the-tidb-database-platform}

このガイドは、TiDB を始めるための最も簡単な方法を提供します。非実稼働環境の場合は、次のいずれかの方法を使用して TiDB データベースをデプロイできます。

-   [ローカルテストクラスターをデプロイ](#deploy-a-local-test-cluster) (macOS および Linux の場合)
-   [単一マシン上で本番デプロイメントをシミュレートする](#simulate-production-deployment-on-a-single-machine) (Linux のみ)

さらに、TiDB の機能を[TiDB プレイグラウンド](https://play.tidbcloud.com/?utm_source=docs&#x26;utm_medium=tidb_quick_start)で試すことができます。

> **注記：**
>
> このガイドで提供されるデプロイメント方法は、クイック スタート**のみを目的として**おり、本番**向けではありません**。
>
> -   セルフホスト型本番クラスタを展開するには、 [本番インストールガイド](/production-deployment-using-tiup.md)を参照してください。
> -   TiDB を Kubernetes にデプロイするには、 [Kubernetes で TiDB を使ってみる](https://docs.pingcap.com/tidb-in-kubernetes/stable/get-started)を参照してください。
> -   クラウドで TiDB を管理するには、 [TiDB Cloudクイック スタート](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart)を参照してください。

## ローカルテストクラスターをデプロイ {#deploy-a-local-test-cluster}

-   シナリオ: 単一の macOS または Linuxサーバーを使用して、テスト用にローカル TiDB クラスターを迅速にデプロイします。このようなクラスターをデプロイすることで、TiDB の基本的なアーキテクチャと、TiDB、TiKV、PD、モニタリング コンポーネントなどのそのコンポーネントの操作を学ぶことができます。

<SimpleTab>
  <div label="macOS">
    分散システムとして、基本的な TiDB テスト クラスターは通常、2 つの TiDB インスタンス、3 つの TiKV インスタンス、3 つの PD インスタンス、およびオプションのTiFlashインスタンスで構成されます。 TiUP Playground を使用すると、次の手順に従ってテスト クラスターを迅速に構築できます。

    1.  TiUPをダウンロードしてインストールします。

        ```shell
        curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
        ```

        次のメッセージが表示されたら、 TiUP は正常にインストールされています。

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

        上記の出力のシェル プロファイル パスに注目してください。次のステップでそのパスを使用する必要があります。

    2.  グローバル環境変数を宣言します。

        > **注記：**
        >
        > インストール後、 TiUP は対応するシェル プロファイル ファイルの絶対パスを表示します。以下の`source`コマンドの`${your_shell_profile}`パスに合わせて変更する必要があります。この場合、 `${your_shell_profile}`ステップ 1 の出力からの`/Users/user/.zshrc`です。

        ```shell
        source ${your_shell_profile}
        ```

    3.  現在のセッションでクラスターを開始します。

        -   1 つの TiDB インスタンス、1 つの TiKV インスタンス、1 つの PD インスタンス、および 1 つのTiFlashインスタンスを含む最新バージョンの TiDB クラスターを起動するには、次のコマンドを実行します。

            ```shell
            tiup playground
            ```

        -   TiDB バージョンと各コンポーネントのインスタンス数を指定するには、次のようなコマンドを実行します。

            ```shell
            tiup playground v7.1.1 --db 2 --pd 3 --kv 3
            ```

            このコマンドは、v7.1.1 などのバージョン クラスターをローカル マシンにダウンロードして起動します。最新バージョンを表示するには、 `tiup list tidb`を実行します。

            このコマンドは、クラスターのアクセス方法を返します。

            ```log
            CLUSTER START SUCCESSFULLY, Enjoy it ^-^
            To connect TiDB: mysql --comments --host 127.0.0.1 --port 4001 -u root -p (no password)
            To connect TiDB: mysql --comments --host 127.0.0.1 --port 4000 -u root -p (no password)
            To view the dashboard: http://127.0.0.1:2379/dashboard
            PD client endpoints: [127.0.0.1:2379 127.0.0.1:2382 127.0.0.1:2384]
            To view Prometheus: http://127.0.0.1:9090
            To view Grafana: http://127.0.0.1:3000
            ```

            > **注記：**
            >
            > -   v5.2.0 以降、TiDB は Apple M1 チップを使用するマシンでの`tiup playground`の実行をサポートします。
            > -   この方法で操作されたプレイグラウンドの場合、テスト デプロイメントが完了した後、 TiUP は元のクラスター データをクリーンアップします。コマンドを再実行すると、新しいクラスターが取得されます。
            > -   データをstorage上に保持したい場合は、 `tiup --tag <your-tag> playground ...`を実行します。詳細については、 [TiUPリファレンス](/tiup/tiup-reference.md#-t---tag)ガイドを参照してください。

    4.  新しいセッションを開始して TiDB にアクセスします。

        -   TiUPクライアントを使用して TiDB に接続します。

            ```shell
            tiup client
            ```

        -   あるいは、MySQL クライアントを使用して TiDB に接続することもできます。

            ```shell
            mysql --host 127.0.0.1 --port 4000 -u root
            ```

    5.  [http://127.0.0.1:9090](http://127.0.0.1:9090)で TiDB の Prometheus ダッシュボードにアクセスします。

    6.  [http://127.0.0.1:2379/ダッシュボード](http://127.0.0.1:2379/dashboard)で[TiDB ダッシュボード](/dashboard/dashboard-intro.md)にアクセスします。デフォルトのユーザー名は`root`で、パスワードは空です。

    7.  [http://127.0.0.1:3000](http://127.0.0.1:3000)を通じて TiDB の Grafana ダッシュボードにアクセスします。デフォルトのユーザー名とパスワードは両方とも`admin`です。

    8.  (オプション) 分析用に[データをTiFlashにロードする](/tiflash/tiflash-overview.md#use-tiflash) 。

    9.  テスト展開後にクラスターをクリーンアップします。

        1.  <kbd>Control+C</kbd>を押して、上記の TiDB サービスを停止します。

        2.  サービスを停止した後、次のコマンドを実行します。

            ```shell
            tiup clean --all
            ```

    > **注記：**
    >
    > TiUP Playground はデフォルトで`127.0.0.1`をリッスンし、サービスはローカルでのみアクセス可能です。サービスに外部からアクセスできるようにする場合は、 `--host`パラメータを使用してリスニング アドレスを指定し、ネットワーク インターフェイス カード (NIC) を外部からアクセス可能な IP アドレスにバインドします。
  </div>

  <div label="Linux">
    分散システムとして、基本的な TiDB テスト クラスターは通常、2 つの TiDB インスタンス、3 つの TiKV インスタンス、3 つの PD インスタンス、およびオプションのTiFlashインスタンスで構成されます。 TiUP Playground を使用すると、次の手順に従ってテスト クラスターを迅速に構築できます。

    1.  TiUPをダウンロードしてインストールします。

        ```shell
        curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
        ```

        次のメッセージが表示されたら、 TiUP は正常にインストールされています。

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

        上記の出力のシェル プロファイル パスに注目してください。次のステップでそのパスを使用する必要があります。

    2.  グローバル環境変数を宣言します。

        > **注記：**
        >
        > インストール後、 TiUP は対応するシェル プロファイル ファイルの絶対パスを表示します。以下の`source`コマンドの`${your_shell_profile}`パスに合わせて変更する必要があります。

        ```shell
        source ${your_shell_profile}
        ```

    3.  現在のセッションでクラスターを開始します。

        -   1 つの TiDB インスタンス、1 つの TiKV インスタンス、1 つの PD インスタンス、および 1 つのTiFlashインスタンスを含む最新バージョンの TiDB クラスターを起動するには、次のコマンドを実行します。

            ```shell
            tiup playground
            ```

        -   TiDB バージョンと各コンポーネントのインスタンス数を指定するには、次のようなコマンドを実行します。

            ```shell
            tiup playground v7.1.1 --db 2 --pd 3 --kv 3
            ```

            このコマンドは、v7.1.1 などのバージョン クラスターをローカル マシンにダウンロードして起動します。最新バージョンを表示するには、 `tiup list tidb`を実行します。

            このコマンドは、クラスターのアクセス方法を返します。

            ```log
            CLUSTER START SUCCESSFULLY, Enjoy it ^-^
            To connect TiDB: mysql --host 127.0.0.1 --port 4000 -u root -p (no password) --comments
            To view the dashboard: http://127.0.0.1:2379/dashboard
            PD client endpoints: [127.0.0.1:2379]
            To view the Prometheus: http://127.0.0.1:9090
            To view the Grafana: http://127.0.0.1:3000
            ```

            > **注記：**
            >
            > この方法で操作されたプレイグラウンドの場合、テスト デプロイメントが完了した後、 TiUP は元のクラスター データをクリーンアップします。コマンドを再実行すると、新しいクラスターが取得されます。データをstorage上に保持したい場合は、 `tiup --tag <your-tag> playground ...`を実行します。詳細については、 [TiUPリファレンス](/tiup/tiup-reference.md#-t---tag)ガイドを参照してください。

    4.  新しいセッションを開始して TiDB にアクセスします。

        -   TiUPクライアントを使用して TiDB に接続します。

            ```shell
            tiup client
            ```

        -   あるいは、MySQL クライアントを使用して TiDB に接続することもできます。

            ```shell
            mysql --host 127.0.0.1 --port 4000 -u root
            ```

    5.  [http://127.0.0.1:9090](http://127.0.0.1:9090)で TiDB の Prometheus ダッシュボードにアクセスします。

    6.  [http://127.0.0.1:2379/ダッシュボード](http://127.0.0.1:2379/dashboard)で[TiDB ダッシュボード](/dashboard/dashboard-intro.md)にアクセスします。デフォルトのユーザー名は`root`で、パスワードは空です。

    7.  [http://127.0.0.1:3000](http://127.0.0.1:3000)を通じて TiDB の Grafana ダッシュボードにアクセスします。デフォルトのユーザー名とパスワードは両方とも`admin`です。

    8.  (オプション) 分析用に[データをTiFlashにロードする](/tiflash/tiflash-overview.md#use-tiflash) 。

    9.  テスト展開後にクラスターをクリーンアップします。

        1.  <kbd>Control+C</kbd>を押してプロセスを停止します。

        2.  サービスを停止した後、次のコマンドを実行します。

            ```shell
            tiup clean --all
            ```

    > **注記：**
    >
    > TiUP Playground はデフォルトで`127.0.0.1`をリッスンし、サービスはローカルでのみアクセス可能です。サービスに外部からアクセスできるようにする場合は、 `--host`パラメータを使用してリスニング アドレスを指定し、ネットワーク インターフェイス カード (NIC) を外部からアクセス可能な IP アドレスにバインドします。
  </div>
</SimpleTab>

## 単一マシン上で本番デプロイメントをシミュレートする {#simulate-production-deployment-on-a-single-machine}

-   シナリオ: 完全なトポロジーを備えた最小の TiDB クラスターを体験し、単一の Linuxサーバー上での本番デプロイメント・ステップをシミュレートします。

このセクションでは、 TiUPで最小のトポロジの YAML ファイルを使用して TiDB クラスターをデプロイする方法について説明します。

### 準備する {#prepare}

TiDB クラスターをデプロイする前に、ターゲット マシンが次の要件を満たしていることを確認してください。

-   CentOS 7.3以降がインストールされていること。
-   Linux OS はインターネットにアクセスできます。これは、TiDB および関連ソフトウェア インストール パッケージをダウンロードするために必要です。

最小の TiDB クラスター トポロジは、次のインスタンスで構成されます。

> **注記：**
>
> インスタンスの IP アドレスは例としてのみ示されています。実際の展開では、IP アドレスを実際の IP アドレスに置き換えます。

| 実例      | カウント | IP                                   | コンフィグレーション                  |
| :------ | :--- | :----------------------------------- | :-------------------------- |
| TiKV    | 3    | 10.0.1.1<br/> 10.0.1.1<br/> 10.0.1.1 | ポートとディレクトリ間の競合を回避する         |
| TiDB    | 1    | 10.0.1.1                             | デフォルトのポート<br/>グローバルディレクトリ構成 |
| PD      | 1    | 10.0.1.1                             | デフォルトのポート<br/>グローバルディレクトリ構成 |
| TiFlash | 1    | 10.0.1.1                             | デフォルトのポート<br/>グローバルディレクトリ構成 |
| モニター    | 1    | 10.0.1.1                             | デフォルトのポート<br/>グローバルディレクトリ構成 |

ターゲット マシンのその他の要件は次のとおりです。

-   `root`ユーザーとそのパスワードが必要です
-   [ターゲットマシンのファイアウォールサービスを停止します](/check-before-deployment.md#check-and-stop-the-firewall-service-of-target-machines) 、または TiDB クラスターノードに必要なポートを開きます
-   現在、 TiUPクラスターは、x86_64 (AMD64) および ARM アーキテクチャでの TiDB のデプロイをサポートしています。

    -   AMD64 では CentOS 7.3 以降のバージョンを使用することをお勧めします。
    -   ARM では CentOS 7.6 1810 を使用することをお勧めします。

### デプロイ {#deploy}

> **注記：**
>
> 対象マシンには通常ユーザーまたは`root`ユーザーとしてログインできます。次の手順では、例として`root`ユーザーを使用します。

1.  TiUPをダウンロードしてインストールします。

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2.  グローバル環境変数を宣言します。

    > **注記：**
    >
    > インストール後、 TiUP は対応するシェル プロファイル ファイルの絶対パスを表示します。以下の`source`コマンドの`${your_shell_profile}`パスに合わせて変更する必要があります。

    ```shell
    source ${your_shell_profile}
    ```

3.  TiUPのクラスターコンポーネントをインストールします。

    ```shell
    tiup cluster
    ```

4.  TiUPクラスターが既にマシンにインストールされている場合は、ソフトウェア バージョンを更新します。

    ```shell
    tiup update --self && tiup update cluster
    ```

5.  root ユーザー権限を使用して、 `sshd`サービスの接続制限を増やします。これは、 TiUP が複数のマシンでの展開をシミュレートする必要があるためです。

    1.  `/etc/ssh/sshd_config`を変更し、 `MaxSessions` ～ `20`を設定します。
    2.  `sshd`サービスを再起動します。

        ```shell
        service sshd restart
        ```

6.  クラスターを作成して起動します。

    次のテンプレートに従って構成ファイルを編集し、 `topo.yaml`という名前を付けます。

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
       instance.tidb_slow_log_threshold: 300
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

    -   `user: "tidb"` : `tidb`システム ユーザー (展開中に自動的に作成される) を使用して、クラスターの内部管理を実行します。デフォルトでは、ポート 22 を使用して SSH 経由でターゲット マシンにログインします。
    -   `replication.enable-placement-rules` : この PD パラメータは、 TiFlash が正常に動作することを保証するために設定されます。
    -   `host` : ターゲットマシンのIP。

7.  クラスター展開コマンドを実行します。

    ```shell
    tiup cluster deploy <cluster-name> <version> ./topo.yaml --user root -p
    ```

    -   `<cluster-name>` : クラスター名を設定します
    -   `<version>` : TiDB クラスターのバージョンを設定します ( `v7.1.1`など)。 `tiup list tidb`コマンドを実行すると、サポートされているすべての TiDB バージョンを確認できます。
    -   `-p` : ターゲットマシンへの接続に使用するパスワードを指定します。

        > **注記：**
        >
        > 秘密キーを使用する場合は、 `-i`までのキーのパスを指定できます。 `-i`と`-p`を同時に使用しないでください。

    「y」と`root`ユーザーのパスワードを入力して、展開を完了します。

    ```log
    Do you want to continue? [y/N]:  y
    Input SSH password:
    ```

8.  クラスターを開始します。

    ```shell
    tiup cluster start <cluster-name>
    ```

9.  クラスターにアクセスします。

    -   MySQL クライアントをインストールします。すでにインストールされている場合は、この手順をスキップしてください。

        ```shell
        yum -y install mysql
        ```

    -   TiDB にアクセスします。パスワードが空です:

        ```shell
        mysql -h 10.0.1.1 -P 4000 -u root
        ```

    -   [http://{グラファナ-ip}:3000](http://%7Bgrafana-ip%7D:3000)から Grafana 監視ダッシュボードにアクセスします。デフォルトのユーザー名とパスワードは両方とも`admin`です。

    -   [http://{pd-ip}:2379/ダッシュボード](http://%7Bpd-ip%7D:2379/dashboard)で[TiDB ダッシュボード](/dashboard/dashboard-intro.md)にアクセスします。デフォルトのユーザー名は`root`で、パスワードは空です。

    -   現在デプロイされているクラスターのリストを表示するには、次の手順を実行します。

        ```shell
        tiup cluster list
        ```

    -   クラスターのトポロジーとステータスを表示するには、次の手順を実行します。

        ```shell
        tiup cluster display <cluster-name>
        ```

## 次は何ですか {#what-s-next}

ローカル テスト環境に TiDB クラスターをデプロイしたばかりの場合は、次の手順を実行します。

-   TiDB の基本的な SQL 操作については、 [TiDB の基本的な SQL 操作](/basic-sql-operations.md)を参照してください。
-   [データを TiDB に移行する](/migration-overview.md)を参照してデータを TiDB に移行することもできます。

TiDB クラスターを本番環境にデプロイする準備ができている場合は、次の手順を実行します。

-   [TiUPを使用して TiDBをデプロイ](/production-deployment-using-tiup.md)
-   または、ドキュメント[Kubernetes 上の TiDB](https://docs.pingcap.com/tidb-in-kubernetes/stable)を参照して、 TiDB Operatorを使用して TiDB をクラウドにデプロイすることもできます。

TiFlashを使用した分析ソリューションをお探しの場合は、次の手順を実行してください。

-   [TiFlashを使用する](/tiflash/tiflash-overview.md#use-tiflash)
-   [TiFlashの概要](/tiflash/tiflash-overview.md)
