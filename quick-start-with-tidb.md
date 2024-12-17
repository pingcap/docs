---
title: Quick Start Guide for the TiDB Database Platform
summary: TiDB プラットフォームをすぐに使い始める方法を学び、TiDB が最適な選択であるかどうかを確認します。
---

# TiDB データベース プラットフォームのクイック スタート ガイド {#quick-start-guide-for-the-tidb-database-platform}

このガイドでは、TiDB を使い始めるための最も簡単な方法を紹介します。非本番環境では、次のいずれかの方法で TiDB データベースをデプロイできます。

-   [ローカルテストクラスタをデプロイ](#deploy-a-local-test-cluster) (macOS および Linux の場合)
-   [単一のマシンで本番の展開をシミュレートする](#simulate-production-deployment-on-a-single-machine) (Linuxのみ)

さらに、 [TiDB プレイグラウンド](https://play.tidbcloud.com/?utm_source=docs&#x26;utm_medium=tidb_quick_start)で TiDB の機能を試すこともできます。

> **注記：**
>
> このガイドで提供されるデプロイメント方法は、クイック スタート**のみを目的と**しており、本番や包括的な機能および安定性のテスト**には使用できません**。
>
> -   セルフホスト型の本番クラスターをデプロイするには、 [本番インストールガイド](/production-deployment-using-tiup.md)を参照してください。
> -   Kubernetes に TiDB をデプロイするには、 [Kubernetes で TiDB を使い始める](https://docs.pingcap.com/tidb-in-kubernetes/stable/get-started)参照してください。
> -   クラウドで TiDB を管理するには、 [TiDB Cloudクイック スタート](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart)参照してください。

## ローカルテストクラスタをデプロイ {#deploy-a-local-test-cluster}

-   シナリオ: 単一の macOS または Linuxサーバーを使用して、テスト用のローカル TiDB クラスターを迅速にデプロイします。このようなクラスターをデプロイすることで、TiDB の基本的なアーキテクチャと、TiDB、TiKV、PD、監視コンポーネントなどのコンポーネントの操作を学習できます。

<SimpleTab>
<div label="macOS">

分散システムとして、基本的なTiUPテスト クラスターは通常、2 つの TiDB インスタンス、3 つの TiKV インスタンス、3 つの PD インスタンス、およびオプションのTiFlashインスタンスで構成されます。TiUP Playground を使用すると、次の手順に従ってテスト クラスターをすばやく構築できます。

1.  TiUPをダウンロードしてインストールします:

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

    上記の出力の Shell プロファイル パスをメモします。次の手順でこのパスを使用する必要があります。

2.  グローバル環境変数を宣言します。

    > **注記：**
    >
    > インストール後、 TiUP は対応するシェル プロファイル ファイルの絶対パスを表示します。パスに応じて、次の`source`のコマンドの`${your_shell_profile}`変更する必要があります。この場合、 `${your_shell_profile}`手順 1 の出力の`/Users/user/.zshrc`になります。

    ```shell
    source ${your_shell_profile}
    ```

3.  現在のセッションでクラスターを起動します。

    > **注記：**
    >
    > -   以下のように操作したプレイグラウンドでは、デプロイとテストが終了した後、 TiUPクラスターデータが自動的にクリーンアップされます。コマンドを再実行すると、新しいクラスターが取得されます。
    > -   storageにデータを保持する場合は、クラスターの起動時に`--tag`フラグを追加します。詳細については、 [TiDBクラスタを起動するときにデータを保存するタグを指定します](/tiup/tiup-playground.md#specify-a-tag-when-starting-the-tidb-cluster-to-store-the-data)参照してください。
    >
    >     ```shell
    >     tiup playground --tag ${tag_name}
    >     ```

    -   1 つの TiDB インスタンス、1 つの TiKV インスタンス、1 つの PD インスタンス、および 1 つのTiFlashインスタンスを含む最新バージョンの TiDB クラスターを起動するには、次のコマンドを実行します。

        ```shell
        tiup playground
        ```

    -   TiDB のバージョンと各コンポーネントのインスタンスの数を指定するには、次のようなコマンドを実行します。

        ```shell
        tiup playground v8.1.1 --db 2 --pd 3 --kv 3
        ```

        このコマンドは、バージョン クラスター (v8.1.1 など) をローカル マシンにダウンロードして起動します。最新バージョンを表示するには、 `tiup list tidb`実行します。

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
        > v5.2.0 以降、TiDB は Apple M1 チップを使用するマシン上で`tiup playground`実行をサポートします。

4.  TiDB にアクセスするには、新しいセッションを開始します。

    -   TiUPクライアントを使用して TiDB に接続します。

        ```shell
        tiup client
        ```

    -   あるいは、MySQL クライアントを使用して TiDB に接続することもできます。

        ```shell
        mysql --host 127.0.0.1 --port 4000 -u root
        ```

5.  [http://127.0.0.1:9090](http://127.0.0.1:9090)で TiDB の Prometheus ダッシュボードにアクセスします。

6.  [http://127.0.0.1:2379/ダッシュボード](http://127.0.0.1:2379/dashboard)の[TiDBダッシュボード](/dashboard/dashboard-intro.md)にアクセスします。デフォルトのユーザー名は`root` 、パスワードは空です。

7.  [http://127.0.0.1:3000](http://127.0.0.1:3000)から TiDB の Grafana ダッシュボードにアクセスします。デフォルトのユーザー名とパスワードはどちらも`admin`です。

8.  (オプション) 分析用に[TiFlashにデータをロードする](/tiflash/tiflash-overview.md#use-tiflash) 。

9.  テストデプロイ後にクラスターをクリーンアップします。

    1.  <kbd>Control+C</kbd>を押して上記の TiDB サービスを停止します。

    2.  サービスが停止したら、次のコマンドを実行します。

        ```shell
        tiup clean --all
        ```

> **注記：**
>
> TiUP Playground はデフォルトで`127.0.0.1`でリッスンし、サービスはローカルでのみアクセスできます。サービスを外部からアクセス可能にする場合は、 `--host`パラメータを使用してリッスン アドレスを指定し、ネットワーク インターフェイス カード (NIC) を外部からアクセス可能な IP アドレスにバインドします。

</div>
<div label="Linux">

分散システムとして、基本的なTiUPテスト クラスターは通常、2 つの TiDB インスタンス、3 つの TiKV インスタンス、3 つの PD インスタンス、およびオプションのTiFlashインスタンスで構成されます。TiUP Playground を使用すると、次の手順に従ってテスト クラスターをすばやく構築できます。

1.  TiUPをダウンロードしてインストールします:

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

    上記の出力の Shell プロファイル パスをメモします。次の手順でこのパスを使用する必要があります。

2.  グローバル環境変数を宣言します。

    > **注記：**
    >
    > インストール後、 TiUP は対応するシェル プロファイル ファイルの絶対パスを表示します。パスに応じて、次の`source`のコマンドの`${your_shell_profile}`変更する必要があります。

    ```shell
    source ${your_shell_profile}
    ```

3.  現在のセッションでクラスターを起動します。

    > **注記：**
    >
    > -   以下のように操作したプレイグラウンドでは、デプロイとテストが終了した後、 TiUPクラスターデータが自動的にクリーンアップされます。コマンドを再実行すると、新しいクラスターが取得されます。
    > -   storageにデータを保持する場合は、クラスターの起動時に`--tag`フラグを追加します。詳細については、 [TiDBクラスタを起動するときにデータを保存するタグを指定します](/tiup/tiup-playground.md#specify-a-tag-when-starting-the-tidb-cluster-to-store-the-data)参照してください。
    >
    >     ```shell
    >     tiup playground --tag ${tag_name}
    >     ```

    -   1 つの TiDB インスタンス、1 つの TiKV インスタンス、1 つの PD インスタンス、および 1 つのTiFlashインスタンスを含む最新バージョンの TiDB クラスターを起動するには、次のコマンドを実行します。

        ```shell
        tiup playground
        ```

    -   TiDB のバージョンと各コンポーネントのインスタンスの数を指定するには、次のようなコマンドを実行します。

        ```shell
        tiup playground v8.1.1 --db 2 --pd 3 --kv 3
        ```

        このコマンドは、バージョン クラスター (v8.1.1 など) をローカル マシンにダウンロードして起動します。最新バージョンを表示するには、 `tiup list tidb`実行します。

        このコマンドは、クラスターのアクセス方法を返します。

        ```log
        CLUSTER START SUCCESSFULLY, Enjoy it ^-^
        To connect TiDB: mysql --host 127.0.0.1 --port 4000 -u root -p (no password) --comments
        To view the dashboard: http://127.0.0.1:2379/dashboard
        PD client endpoints: [127.0.0.1:2379]
        To view the Prometheus: http://127.0.0.1:9090
        To view the Grafana: http://127.0.0.1:3000
        ```

4.  TiDB にアクセスするには、新しいセッションを開始します。

    -   TiUPクライアントを使用して TiDB に接続します。

        ```shell
        tiup client
        ```

    -   あるいは、MySQL クライアントを使用して TiDB に接続することもできます。

        ```shell
        mysql --host 127.0.0.1 --port 4000 -u root
        ```

5.  [http://127.0.0.1:9090](http://127.0.0.1:9090)で TiDB の Prometheus ダッシュボードにアクセスします。

6.  [http://127.0.0.1:2379/ダッシュボード](http://127.0.0.1:2379/dashboard)の[TiDBダッシュボード](/dashboard/dashboard-intro.md)にアクセスします。デフォルトのユーザー名は`root` 、パスワードは空です。

7.  [http://127.0.0.1:3000](http://127.0.0.1:3000)から TiDB の Grafana ダッシュボードにアクセスします。デフォルトのユーザー名とパスワードはどちらも`admin`です。

8.  (オプション) 分析用に[TiFlashにデータをロードする](/tiflash/tiflash-overview.md#use-tiflash) 。

9.  テストデプロイ後にクラスターをクリーンアップします。

    1.  <kbd>Control+C を</kbd>押してプロセスを停止します。

    2.  サービスが停止したら、次のコマンドを実行します。

        ```shell
        tiup clean --all
        ```

> **注記：**
>
> TiUP Playground はデフォルトで`127.0.0.1`でリッスンし、サービスはローカルでのみアクセスできます。サービスを外部からアクセス可能にする場合は、 `--host`パラメータを使用してリッスン アドレスを指定し、ネットワーク インターフェイス カード (NIC) を外部からアクセス可能な IP アドレスにバインドします。

</div>
</SimpleTab>

## 単一のマシンで本番の展開をシミュレートする {#simulate-production-deployment-on-a-single-machine}

-   シナリオ: 完全なトポロジを備えた最小の TiDB クラスターを体験し、単一の Linuxサーバー上で本番展開手順をシミュレートします。

このセクションでは、 TiUPで最小トポロジの YAML ファイルを使用して TiDB クラスターをデプロイする方法について説明します。

### 準備する {#prepare}

TiDB クラスターを展開する前に、ターゲット マシンが次の要件を満たしていることを確認してください。

-   CentOS 7.3以降のバージョンがインストールされています。
-   Linux OS はインターネットにアクセスでき、TiDB および関連ソフトウェアのインストール パッケージをダウンロードするために必要です。

最小の TiDB クラスター トポロジは、次のインスタンスで構成されます。

> **注記：**
>
> インスタンスの IP アドレスは例としてのみ提供されています。実際の展開では、IP アドレスを実際の IP アドレスに置き換えてください。

| 実例      | カウント | IP                                   | コンフィグレーション                 |
| :------ | :--- | :----------------------------------- | :------------------------- |
| ティクヴ    | 3    | 10.0.1.1<br/> 10.0.1.1<br/> 10.0.1.1 | ポートとディレクトリ間の競合を避ける         |
| ティビ     | 1    | 10.0.1.1                             | デフォルトポート<br/>グローバルディレクトリ構成 |
| PD      | 1    | 10.0.1.1                             | デフォルトポート<br/>グローバルディレクトリ構成 |
| TiFlash | 1    | 10.0.1.1                             | デフォルトポート<br/>グローバルディレクトリ構成 |
| モニター    | 1    | 10.0.1.1                             | デフォルトポート<br/>グローバルディレクトリ構成 |

ターゲット マシンのその他の要件は次のとおりです。

-   `root`のユーザーとそのパスワードが必要です
-   [対象マシンのファイアウォールサービスを停止します](/check-before-deployment.md#check-and-stop-the-firewall-service-of-target-machines) 、またはTiDBクラスタノードに必要なポートを開く
-   現在、 TiUPクラスターは、x86_64 (AMD64) および ARM アーキテクチャでの TiDB のデプロイをサポートしています。

    -   AMD64 では CentOS 7.3 以降のバージョンを使用することをお勧めします。
    -   ARM では CentOS 7.6 1810 を使用することをお勧めします。

### デプロイ {#deploy}

> **注記：**
>
> 対象マシンには、通常のユーザーまたは`root`ユーザーとしてログインできます。次の手順では、 `root`ユーザーを例として使用します。

1.  TiUPをダウンロードしてインストールします:

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2.  グローバル環境変数を宣言します。

    > **注記：**
    >
    > インストール後、 TiUP は対応するシェル プロファイル ファイルの絶対パスを表示します。パスに応じて、次の`source`のコマンドの`${your_shell_profile}`変更する必要があります。

    ```shell
    source ${your_shell_profile}
    ```

3.  TiUPのクラスターコンポーネントをインストールします。

    ```shell
    tiup cluster
    ```

4.  TiUPクラスターがすでにマシンにインストールされている場合は、ソフトウェア バージョンを更新します。

    ```shell
    tiup update --self && tiup update cluster
    ```

5.  ルート ユーザー権限を使用して、 `sshd`サービスの接続制限を増やします。これは、 TiUP が複数のマシンへの展開をシミュレートする必要があるためです。

    1.  `/etc/ssh/sshd_config`変更し、 `MaxSessions` `20`に設定します。
    2.  `sshd`サービスを再起動します。

        ```shell
        service sshd restart
        ```

6.  クラスターを作成して起動します。

    次のテンプレートに従って設定ファイルを編集し、名前を`topo.yaml`にします。

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

    -   `user: "tidb"` : `tidb`システム ユーザー (デプロイメント中に自動的に作成) を使用して、クラスターの内部管理を実行します。デフォルトでは、ポート 22 を使用して SSH 経由でターゲット マシンにログインします。
    -   `replication.enable-placement-rules` : この PD パラメータは、 TiFlash が正常に実行されるように設定されます。
    -   `host` : ターゲットマシンの IP。

7.  クラスター デプロイメント コマンドを実行します。

    ```shell
    tiup cluster deploy <cluster-name> <version> ./topo.yaml --user root -p
    ```

    -   `<cluster-name>` : クラスター名を設定する
    -   `<version>` : TiDBクラスタバージョンを設定します（例： `v8.1.1` ）。4 `tiup list tidb`を実行すると、サポートされているすべてのTiDBバージョンを確認できます。
    -   `-p` : ターゲットマシンに接続するために使用するパスワードを指定します。

        > **注記：**
        >
        > 秘密鍵を使用する場合は、 `-i`で鍵のパスを指定できます。 `-i`と`-p`同時に使用しないでください。

    展開を完了するには、「y」と`root`のユーザーのパスワードを入力します。

    ```log
    Do you want to continue? [y/N]:  y
    Input SSH password:
    ```

8.  クラスターを起動します。

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

    -   [http://{grafana-ip}:3000](http://%7Bgrafana-ip%7D:3000)で Grafana 監視ダッシュボードにアクセスします。デフォルトのユーザー名とパスワードはどちらも`admin`です。

    -   [http://{pd-ip}:2379/ダッシュボード](http://%7Bpd-ip%7D:2379/dashboard)の[TiDBダッシュボード](/dashboard/dashboard-intro.md)にアクセスします。デフォルトのユーザー名は`root` 、パスワードは空です。

    -   現在デプロイされているクラスターのリストを表示するには:

        ```shell
        tiup cluster list
        ```

    -   クラスターのトポロジとステータスを表示するには:

        ```shell
        tiup cluster display <cluster-name>
        ```

## 次は何か {#what-s-next}

ローカル テスト環境用に TiDB クラスターをデプロイしたばかりの場合は、次の手順に従います。

-   [TiDB における基本的な SQL 操作](/basic-sql-operations.md)を参照して、TiDB での基本的な SQL 操作について学習します。
-   [データをTiDBに移行する](/migration-overview.md)を参照して TiDB にデータを移行することもできます。

本番環境用に TiDB クラスターをデプロイする準備ができたら、次の手順に従います。

-   [TiUP を使用して TiDB をデプロイ](/production-deployment-using-tiup.md)
-   あるいは、 [Kubernetes 上の TiDB](https://docs.pingcap.com/tidb-in-kubernetes/stable)ドキュメントを参照して、 TiDB Operator を使用してクラウドに TiDB をデプロイすることもできます。

TiFlashを使用した分析ソリューションをお探しの場合は、次の手順に従ってください。

-   [TiFlashを使用する](/tiflash/tiflash-overview.md#use-tiflash)
-   [TiFlashの概要](/tiflash/tiflash-overview.md)
