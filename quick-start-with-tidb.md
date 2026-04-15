---
title: Quick Start with TiDB Self-Managed
summary: TiUPプレイグラウンドを使ってTiDBセルフマネージドを素早く使い始める方法を学び、TiDBがあなたにとって最適な選択肢かどうかを確認しましょう。
---

# TiDBセルフマネージドのクイックスタート {#quick-start-with-tidb-self-managed}

このガイドでは、TiDB Self-Managed を最も迅速に使い始める方法を説明します。非本番環境では、以下のいずれかの方法で TiDB データベースをデプロイできます。

-   [ローカルテストクラスターをデプロイ](#deploy-a-local-test-cluster)(macOSおよびLinux用)
-   [単一のマシン上で本番本番への展開をシミュレーションする](#simulate-production-deployment-on-a-single-machine)(Linux のみ)

さらに、 [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&#x26;utm_medium=tidb_quick_start)でTiDBの機能を試すこともできます。

> **注記：**
>
> このガイドで説明する導入方法は、クイックスタート**のみを目的として**おり、本番や包括的な機能・安定性テスト**には適していません**。
>
> -   セルフホスト型実本番クラスターをデプロイするには、[本番インストールガイド](/production-deployment-using-tiup.md)ガイドを参照してください。
> -   TiDB を Kubernetes にデプロイするには、 [Kubernetes 上で TiDB を使い始める](https://docs.pingcap.com/tidb-in-kubernetes/stable/get-started)を参照してください。
> -   クラウドで TiDB を管理するには、 [TiDB Cloudクイックスタート](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart)を参照してください。

## ローカルテストクラスターをデプロイ {#deploy-a-local-test-cluster}

このセクションでは、単一のmacOSまたはLinuxサーバー上でテスト用のローカルTiDBクラスタを迅速にデプロイする方法について説明します。このようなクラスタをデプロイすることで、TiDBデータベースの基本的なアーキテクチャと、TiDB、TiKV、PD、監視コンポーネントなどの各コンポーネントの動作を習得できます。

<SimpleTab>
<div label="macOS">

分散システムである基本的なTiDBテストクラスタは、通常、2つのTiDBインスタンス、3つのTiKVインスタンス、3つのPDインスタンス、およびオプションのTiFlashインスタンスで構成されます。TiUP Playgroundを使用すると、以下の手順に従ってテストクラスタをすばやくセットアップできます。

1.  TiUPをダウンロードしてインストールしてください：

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

    以下のメッセージが表示された場合、 TiUPのインストールは正常に完了しています。

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

    上記の出力に表示されているシェルプロファイルのパスをメモしておいてください。次のステップでこのパスを使用する必要があります。

    > **注記：**
    >
    > TiDBはv5.2.0以降、Appleシリコンチップを使用するマシン上で`tiup playground`を実行することをサポートしています。

2.  グローバル環境変数を宣言します。

    > **注記：**
    >
    > インストール後、 TiUP は対応するシェルプロファイルファイルの絶対パスを表示します。次の`${your_shell_profile}`コマンドの`source`をパスに合わせて変更する必要があります。この場合、 `${your_shell_profile}`はステップ 1 の出力の`/Users/user/.zshrc`です。

    ```shell
    source ${your_shell_profile}
    ```

3.  現在のセッションでクラスターを起動します。

    > **注記：**
    >
    > -   以下の方法で運用されるプレイグラウンドの場合、デプロイとテストが完了すると、 TiUPは自動的にクラスタデータをクリーンアップします。コマンドを再実行すると、新しいクラスタが作成されます。
    > -   データをstorageに保持する場合は、クラスターの起動時に`--tag`フラグを追加します。詳細については、 [TiDBクラスタの起動時に、データを保存するタグを指定します。](/tiup/tiup-playground.md#specify-a-tag-when-starting-the-tidb-cluster-to-store-the-data)参照してください。
    >
    >     ```shell
    >     tiup playground --tag ${tag_name}
    >     ```

    -   最新バージョンの TiDB クラスタを、TiDB インスタンス 1 つ、TiKV インスタンス 1 つ、PD インスタンス 1 つ、 TiFlashインスタンス 1 つで起動するには、次のコマンドを実行します。

        ```shell
        tiup playground
        ```

        このコマンドを初めて実行する場合、 TiUPは最新バージョンのTiDBをダウンロードし、クラスタを起動します。

        出力には、クラスターのエンドポイントのリストが表示されます。

        ```log
        🎉 TiDB Playground Cluster is started, enjoy!

        Connect TiDB:    mysql --comments --host 127.0.0.1 --port 4000 -u root
        TiDB Dashboard:  http://127.0.0.1:2379/dashboard
        Grafana:         http://127.0.0.1:3000
        ```

    -   TiDBのバージョンと各コンポーネントのインスタンス数を指定するには、次のようなコマンドを実行します。

        ```shell
        tiup playground v8.5.4 --db 2 --pd 3 --kv 3
        ```

        このコマンドは、少なくとも10GiBのメモリと4つのCPUコアを搭載したマシンで実行することをお勧めします。リソースが不足している場合、システムがクラッシュする可能性があります。

        利用可能なすべてのバージョンを表示するには、 `tiup list tidb`を実行してください。

4.  TiDBクラスタのエンドポイントにアクセスするには、新しいセッションを開始してください。

    -   TiDBデータベースに接続します。

        -   TiUPクライアントを使用してTiDBに接続してください。

            ```shell
            tiup client
            ```

        -   あるいは、MySQLクライアントを使用してTiDBに接続することもできます。

            ```shell
            mysql --host 127.0.0.1 --port 4000 -u root
            ```

    -   プロメテウス: [http://127.0.0.1:9090](http://127.0.0.1:9090) 。

    -   [TiDBダッシュボード](/dashboard/dashboard-intro.md): [http://127.0.0.1:2379/dashboard](http://127.0.0.1:2379/dashboard) 。デフォルトのユーザー名は`root`で、パスワードは空です。

    -   Grafana: [http://127.0.0.1:3000](http://127.0.0.1:3000) 。デフォルトのユーザー名とパスワードはどちらも`admin`です。

5.  (オプション) 分析用に[TiFlashにデータをロードする](/tiflash/tiflash-overview.md#use-tiflash)。

6.  テスト後にクラスターをクリーンアップしてください。

    1.  上記のTiDBサービスを停止するには、 <kbd>Control</kbd> + <kbd>C</kbd>を押してください。

    2.  サービス停止後、以下のコマンドを実行してください。

        ```shell
        tiup clean --all
        ```

> **注記：**
>
> TiUP Playgroundはデフォルトでは`127.0.0.1`でリッスンし、サービスはローカルでのみアクセス可能です。サービスを外部からアクセス可能にするには、 `--host`パラメーターを使用してリッスンアドレスを指定し、ネットワークインターフェイスカード（NIC）を外部からアクセス可能なIPアドレスにバインドしてください。

</div>
<div label="Linux">

分散システムである基本的なTiDBテストクラスタは、通常、2つのTiDBインスタンス、3つのTiKVインスタンス、3つのPDインスタンス、およびオプションのTiFlashインスタンスで構成されます。TiUP Playgroundを使用すると、以下の手順に従ってテストクラスタをすばやくセットアップできます。

1.  TiUPをダウンロードしてインストールしてください：

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

    以下のメッセージが表示された場合、 TiUPのインストールは正常に完了しています。

    ```log
    Successfully set mirror to https://tiup-mirrors.pingcap.com
    Detected shell: bash
    Shell profile:  /home/user/.bashrc
    /home/user/.bashrc has been modified to add tiup to PATH
    open a new terminal or source /home/user/.bashrc to use it
    Installed path: /home/user/.tiup/bin/tiup
    ===============================================
    Have a try:     tiup playground
    ===============================================
    ```

    上記の出力に表示されているシェルプロファイルのパスをメモしておいてください。次のステップでこのパスを使用する必要があります。

2.  グローバル環境変数を宣言します。

    > **注記：**
    >
    > インストール後、 TiUPは対応するシェルプロファイルファイルの絶対パスを表示します。パスに応じて、以下の`${your_shell_profile}`コマンドの`source`する必要があります。

    ```shell
    source ${your_shell_profile}
    ```

3.  現在のセッションでクラスターを起動します。

    > **注記：**
    >
    > -   以下の方法で運用されるプレイグラウンドの場合、デプロイとテストが完了すると、 TiUPは自動的にクラスタデータをクリーンアップします。コマンドを再実行すると、新しいクラスタが作成されます。
    > -   データをstorageに保持する場合は、クラスターの起動時に`--tag`フラグを追加します。詳細については、 [TiDBクラスタの起動時に、データを保存するタグを指定します。](/tiup/tiup-playground.md#specify-a-tag-when-starting-the-tidb-cluster-to-store-the-data)参照してください。
    >
    >     ```shell
    >     tiup playground --tag ${tag_name}
    >     ```

    -   最新バージョンの TiDB クラスタを、TiDB インスタンス 1 つ、TiKV インスタンス 1 つ、PD インスタンス 1 つ、 TiFlashインスタンス 1 つで起動するには、次のコマンドを実行します。

        ```shell
        tiup playground
        ```

        このコマンドを初めて実行する場合、 TiUPは最新バージョンのTiDBをダウンロードし、クラスタを起動します。

        出力には、クラスターのエンドポイントのリストが表示されます。

        ```log
        🎉 TiDB Playground Cluster is started, enjoy!

        Connect TiDB:    mysql --comments --host 127.0.0.1 --port 4000 -u root
        TiDB Dashboard:  http://127.0.0.1:2379/dashboard
        Grafana:         http://127.0.0.1:3000
        ```

    -   TiDBのバージョンと各コンポーネントのインスタンス数を指定するには、次のようなコマンドを実行します。

        ```shell
        tiup playground v8.5.4 --db 2 --pd 3 --kv 3
        ```

        利用可能なすべてのバージョンを表示するには、 `tiup list tidb`を実行してください。

4.  TiDBクラスタのエンドポイントにアクセスするには、新しいセッションを開始してください。

    -   TiDBデータベースに接続します。

        -   TiUPクライアントを使用してTiDBに接続してください。

            ```shell
            tiup client
            ```

        -   あるいは、MySQLクライアントを使用してTiDBに接続することもできます。

            ```shell
            mysql --host 127.0.0.1 --port 4000 -u root
            ```

    -   プロメテウス: [http://127.0.0.1:9090](http://127.0.0.1:9090) 。

    -   [TiDBダッシュボード](/dashboard/dashboard-intro.md): [http://127.0.0.1:2379/dashboard](http://127.0.0.1:2379/dashboard) 。デフォルトのユーザー名は`root`で、パスワードは空です。

    -   Grafana: [http://127.0.0.1:3000](http://127.0.0.1:3000) 。デフォルトのユーザー名とパスワードはどちらも`admin`です。

5.  (オプション) 分析用に[TiFlashにデータをロードする](/tiflash/tiflash-overview.md#use-tiflash)。

6.  テスト後にクラスターをクリーンアップしてください。

    1.  <kbd>Ctrl</kbd> + <kbd>C</kbd>を押してプロセスを停止します。

    2.  サービス停止後、以下のコマンドを実行してください。

        ```shell
        tiup clean --all
        ```

> **注記：**
>
> TiUP Playgroundはデフォルトでは`127.0.0.1`でリッスンし、サービスはローカルでのみアクセス可能です。サービスを外部からアクセス可能にするには、 `--host`パラメーターを使用してリッスンアドレスを指定し、ネットワークインターフェイスカード（NIC）を外部からアクセス可能なIPアドレスにバインドしてください。

</div>
</SimpleTab>

## 単一のマシン上で本番本番への展開をシミュレーションする {#simulate-production-deployment-on-a-single-machine}

このセクションでは、完全なトポロジーを持つ最小のTiDBクラスタをセットアップし、単一のLinuxサーバー上で本番へのデプロイ手順をシミュレートする方法について説明します。

以下では、 TiUPの最小トポロジーの YAML ファイルを使用して TiDB クラスタをデプロイする方法について説明します。

### 準備する {#prepare}

TiDBクラスタをデプロイする前に、ターゲットマシンが以下の要件を満たしていることを確認してください。

-   CentOS 7.3以降のバージョンがインストールされています。
-   Linux OSはインターネットにアクセスできる環境にあり、TiDBおよび関連ソフトウェアのインストールパッケージをダウンロードするにはインターネット接続が必要です。

TiDBクラスタの最小トポロジーは、以下のインスタンスで構成されます。

| 実例      | カウント | IP       | コンフィグレーション                     |
| :------ | :--- | :------- | :----------------------------- |
| ティクヴ    | 3    | 10.0.1.1 | 競合を避けるために、ポート番号は増分番号を使用してください。 |
| TiDB    | 1    | 10.0.1.1 | デフォルトのポートおよびその他の設定を使用する        |
| PD      | 1    | 10.0.1.1 | デフォルトのポートおよびその他の設定を使用する        |
| TiFlash | 1    | 10.0.1.1 | デフォルトのポートおよびその他の設定を使用する        |
| モニター    | 1    | 10.0.1.1 | デフォルトのポートおよびその他の設定を使用する        |

> **注記：**
>
> インスタンスのIPアドレスはあくまで例です。実際のデプロイメントでは、これらのIPアドレスを実際のIPアドレスに置き換えてください。

対象マシンに対するその他の要件は以下のとおりです。

-   `root`ユーザーとそのパスワードが必要です。
-   [対象マシンのファイアウォールサービスを停止します。](/check-before-deployment.md#check-the-firewall-service-of-target-machines) 、または、TiDB クラスターノードに必要なポートを開きます。
-   現在、 TiUPクラスタは、x86_64（AMD64）およびARMアーキテクチャへのTiDBのデプロイをサポートしています。

    -   AMD64アーキテクチャでは、CentOS 7.3以降のバージョンを使用することをお勧めします。
    -   ARMアーキテクチャではCentOS 7.6（1810）を使用することをお勧めします。

### デプロイ {#deploy}

> **注記：**
>
> 対象マシンには、通常のユーザーまたは`root`ユーザーとしてログインできます。以下の手順で`root`ユーザーを例として使用します。

1.  TiUPをダウンロードしてインストールしてください：

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2.  グローバル環境変数を宣言します。

    > **注記：**
    >
    > インストール後、 TiUPは対応するシェルプロファイルファイルの絶対パスを表示します。パスに応じて、以下の`${your_shell_profile}`コマンドの`source`する必要があります。

    ```shell
    source ${your_shell_profile}
    ```

3.  TiUPのクラスタコンポーネントをインストールします。

    ```shell
    tiup cluster
    ```

4.  TiUPクラスタが既にマシンにインストールされている場合は、ソフトウェアバージョンを更新してください。

    ```shell
    tiup update --self && tiup update cluster
    ```

5.  ルートユーザー権限を使用して、 `sshd`サービスの接続制限を増やしてください。これは、 TiUP が複数のマシンへの展開をシミュレートする必要があるためです。

    1.  `/etc/ssh/sshd_config`を変更し、 `MaxSessions`を`20`に設定します。
    2.  `sshd`サービスを再起動してください。

        ```shell
        service sshd restart
        ```

6.  クラスターを作成して起動します。

    次のテンプレートに従って[トポロジー構成ファイル](/tiup/tiup-cluster-topology-reference.md)を作成および編集し、 `topo.yaml`という名前を付けます。

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

    -   `user: "tidb"` : `tidb`システムユーザー (デプロイ時に自動的に作成されます) を使用して、クラスタの内部管理を実行します。デフォルトでは、ポート 22 を使用して SSH 経由でターゲット マシンにログインします。
    -   `replication.enable-placement-rules` : このPDパラメータは、 TiFlashが正常に動作するように設定されます。
    -   `host` : ターゲットマシンのIPアドレス。

7.  クラスター展開コマンドを実行します。

    ```shell
    tiup cluster deploy <cluster-name> <version> ./topo.yaml --user root -p
    ```

    -   `<cluster-name>` : クラスター名を設定します。
    -   `<version>` : TiDB クラスタのバージョンを設定します (例`v8.5.4` 。サポートされているすべての TiDB バージョンは`tiup list tidb`コマンドを実行することで確認できます。
    -   `--user` : 環境を初期化するユーザーを指定します。
    -   `-p` : ターゲットマシンへの接続に使用するパスワードを指定します。

        > **注記：**
        >
        > 秘密鍵を使用する場合は、 `-i`を使用して鍵のパスを指定できます。 `-i`と`-p`同時に使用しないでください。

    デプロイメントを完了するには、「y」と`root`ユーザーのパスワードを入力してください。

    ```log
    Do you want to continue? [y/N]:  y
    Input SSH password:
    ```

8.  クラスターを起動します。

    ```shell
    tiup cluster start <cluster-name>
    ```

9.  クラスタエンドポイントにアクセスします。

    -   MySQLクライアントをインストールしてください。既にインストール済みの場合は、この手順をスキップしてください。

        ```shell
        yum -y install mysql
        ```

    -   MySQLクライアントを使用してTiDBデータベースに接続します。パスワードは空欄です。

        ```shell
        mysql -h 10.0.1.1 -P 4000 -u root
        ```

    -   Grafana: [http://{grafana-ip}:3000](http://%7Bgrafana-ip%7D:3000) 。デフォルトのユーザー名とパスワードはどちらも`admin`です。

    -   TiDB [http://{pd-ip}:2379/dashboard](http://%7Bpd-ip%7D:2379/dashboard) [TiDBダッシュボード](/dashboard/dashboard-intro.md)。デフォルトのユーザー名は`root`で、パスワードは空です。

10. （オプション）クラスタ一覧とトポロジーをビュー。

    -   クラスター一覧を表示するには：

        ```shell
        tiup cluster list
        ```

    -   クラスターのトポロジーとステータスを表示するには：

        ```shell
        tiup cluster display <cluster-name>
        ```

    `tiup cluster`コマンドの詳細については、 [TiUPクラスタコマンド](/tiup/tiup-component-cluster.md)参照してください。

11. テスト後にクラスターをクリーンアップしてください。

    1.  上記のTiDBサービスを停止するには、 <kbd>Control</kbd> + <kbd>C</kbd>を押してください。

    2.  サービス停止後、以下のコマンドを実行してください。

        ```shell
        tiup clean --all
        ```

## 次は？ {#what-s-next}

ローカルテスト環境用にTiDBクラスタをデプロイしたばかりの場合は、次の手順を実行してください。

-   TiDB における基本的な SQL 操作については、 [TiDBにおける基本的なSQL操作](/basic-sql-operations.md)参照してください。
-   データをTiDBに移行するを参照して、TiDBにデータを[データをTiDBに移行する](/migration-overview.md)することもできます。
-   TiUPを使用して TiDB クラスターを管理する方法について詳しくは、 [TiUPの概要](/tiup/tiup-overview.md)を参照してください。

本番環境にTiDBクラスタをデプロイする準備が整ったら、次の手順に進んでください。

-   [TiUPを使用してTiDBをデプロイ](/production-deployment-using-tiup.md)
-   あるいは、 [Kubernetes 上の TiDB](https://docs.pingcap.com/tidb-in-kubernetes/stable)ドキュメントを参照して、 TiDB Operator を使用してクラウド上に TiDB をデプロイすることもできます。

あなたがアプリケーション開発者で、TiDBを使用してアプリケーションを迅速に構築したい場合は、以下の手順に従ってください。

-   [開発者ガイドの概要](https://docs.pingcap.com/developer/)
-   [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)
-   [応用例](/develop/dev-guide-sample-application-java-jdbc.md)

TiFlashを使った分析ソリューションをお探しの場合は、以下の手順に従ってください。

-   [TiFlashの概要](/tiflash/tiflash-overview.md)
-   [TiFlashを使用する](/tiflash/tiflash-overview.md#use-tiflash)
