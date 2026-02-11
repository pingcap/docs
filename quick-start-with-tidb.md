---
title: Quick Start with TiDB Self-Managed
summary: TiUPプレイグラウンドを使用して TiDB Self-Managed をすぐに開始する方法を学び、TiDB が最適な選択であるかどうかを確認します。
---

# TiDBセルフマネージドのクイックスタート {#quick-start-with-tidb-self-managed}

このガイドでは、TiDBセルフマネージドを使い始めるための最も簡単な方法を紹介します。非本番環境では、以下のいずれかの方法でTiDBデータベースをデプロイできます。

-   [ローカルテストクラスタをデプロイ](#deploy-a-local-test-cluster) (macOSおよびLinux用)
-   [単一のマシンで本番の展開をシミュレートする](#simulate-production-deployment-on-a-single-machine) (Linuxのみ)

さらに、 [TiDB プレイグラウンド](https://play.tidbcloud.com/?utm_source=docs&#x26;utm_medium=tidb_quick_start)で TiDB の機能を試すこともできます。

> **注記：**
>
> このガイドで提供されるデプロイメント方法は、クイック スタート**のみを目的として**おり、本番や包括的な機能および安定性のテスト**には使用できません**。
>
> -   セルフホスト型の本番本番クラスターをデプロイするには、 [本番インストールガイド](/production-deployment-using-tiup.md)を参照してください。
> -   Kubernetes に TiDB をデプロイするには、 [Kubernetes で TiDB を使い始める](https://docs.pingcap.com/tidb-in-kubernetes/stable/get-started)参照してください。
> -   クラウドで TiDB を管理するには、 [TiDB Cloudクイックスタート](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart)参照してください。

## ローカルテストクラスタをデプロイ {#deploy-a-local-test-cluster}

このセクションでは、単一のmacOSまたはLinuxサーバー上でテスト用のローカルTiDBクラスターを迅速に展開する方法について説明します。このようなクラスターを展開することで、TiDBデータベースの基本アーキテクチャと、TiDB、TiKV、PD、監視コンポーネントなどのコンポーネントの動作を学習できます。

<SimpleTab>
<div label="macOS">

分散システムであるTiDBテストクラスタは、通常、2つのTiDBインスタンス、3つのTiKVインスタンス、3つのPDインスタンス、そしてオプションのTiFlashインスタンスで構成されます。TiUP Playgroundを使用すると、以下の手順で簡単にテストクラスタをセットアップできます。

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

    上記の出力にあるシェルプロファイルのパスをメモしてください。このパスは次の手順で使用します。

    > **注記：**
    >
    > v5.2.0 以降、TiDB は Apple Silicon チップを使用するマシン上で`tiup playground`実行をサポートします。

2.  グローバル環境変数を宣言します。

    > **注記：**
    >
    > インストール後、 TiUP は対応するシェルプロファイルファイルの絶対パスを表示します。次の`source`コマンドの`${your_shell_profile}`パスに合わせて変更する必要があります。この場合、 `${your_shell_profile}`は手順 1 の出力の`/Users/user/.zshrc`になります。

    ```shell
    source ${your_shell_profile}
    ```

3.  現在のセッションでクラスターを起動します。

    > **注記：**
    >
    > -   以下の方法で操作されたプレイグラウンドでは、デプロイとテストが完了すると、 TiUPクラスターデータが自動的にクリーンアップされます。コマンドを再実行すると、新しいクラスターが作成されます。
    > -   storageにデータを永続化したい場合は、クラスターの起動時にフラグ`--tag`を追加してください。詳細は[TiDBクラスタを起動するときにデータを保存するタグを指定します](/tiup/tiup-playground.md#specify-a-tag-when-starting-the-tidb-cluster-to-store-the-data)参照してください。
    >
    >     ```shell
    >     tiup playground --tag ${tag_name}
    >     ```

    -   1 つの TiDB インスタンス、1 つの TiKV インスタンス、1 つの PD インスタンス、および 1 つのTiFlashインスタンスを含む最新バージョンの TiDB クラスターを起動するには、次のコマンドを実行します。

        ```shell
        tiup playground
        ```

        このコマンドを初めて実行する場合、 TiUP は最新バージョンの TiDB をダウンロードし、クラスターを起動します。

        出力にはクラスターのエンドポイントのリストが表示されます。

        ```log
        🎉 TiDB Playground Cluster is started, enjoy!

        Connect TiDB:    mysql --comments --host 127.0.0.1 --port 4000 -u root
        TiDB Dashboard:  http://127.0.0.1:2379/dashboard
        Grafana:         http://127.0.0.1:3000
        ```

    -   TiDB のバージョンと各コンポーネントのインスタンスの数を指定するには、次のようなコマンドを実行します。

        ```shell
        tiup playground v8.5.5 --db 2 --pd 3 --kv 3
        ```

        このコマンドは、少なくとも10GiBのメモリと4つのCPUコアを搭載したマシンで実行することをお勧めします。リソースが不足すると、システムがクラッシュする可能性があります。

        利用可能なすべてのバージョンを表示するには、 `tiup list tidb`を実行します。

4.  TiDB クラスターのエンドポイントにアクセスするための新しいセッションを開始します。

    -   TiDB データベースに接続します。

        -   TiUPクライアントを使用して TiDB に接続します。

            ```shell
            tiup client
            ```

        -   あるいは、MySQL クライアントを使用して TiDB に接続することもできます。

            ```shell
            mysql --host 127.0.0.1 --port 4000 -u root
            ```

    -   プロメテウス: [http://127.0.0.1:9090](http://127.0.0.1:9090) .

    -   [TiDBダッシュボード](/dashboard/dashboard-intro.md) : [http://127.0.0.1:2379/ダッシュボード](http://127.0.0.1:2379/dashboard) 。デフォルトのユーザー名は`root` 、パスワードは空です。

    -   Grafana: [http://127.0.0.1:3000](http://127.0.0.1:3000) 。デフォルトのユーザー名とパスワードはどちらも`admin`です。

5.  (オプション) 分析用に[TiFlashにデータをロードする](/tiflash/tiflash-overview.md#use-tiflash) 。

6.  テスト後にクラスターをクリーンアップします。

    1.  <kbd>Control</kbd> + <kbd>C</kbd>を押して上記の TiDB サービスを停止します。

    2.  サービスを停止した後、次のコマンドを実行します。

        ```shell
        tiup clean --all
        ```

> **注記：**
>
> TiUP Playgroundはデフォルトで`127.0.0.1`リッスンしており、サービスはローカルでのみアクセス可能です。サービスを外部からアクセス可能にしたい場合は、 `--host`パラメータを使用してリッスンアドレスを指定し、ネットワークインターフェースカード（NIC）を外部からアクセス可能なIPアドレスにバインドします。

</div>
<div label="Linux">

分散システムであるTiDBテストクラスタは、通常、2つのTiDBインスタンス、3つのTiKVインスタンス、3つのPDインスタンス、そしてオプションのTiFlashインスタンスで構成されます。TiUP Playgroundを使用すると、以下の手順で簡単にテストクラスタをセットアップできます。

1.  TiUPをダウンロードしてインストールします:

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

    次のメッセージが表示されたら、 TiUP は正常にインストールされています。

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

    上記の出力にあるシェルプロファイルのパスをメモしてください。このパスは次の手順で使用します。

2.  グローバル環境変数を宣言します。

    > **注記：**
    >
    > インストール後、 TiUP は対応するシェルプロファイルファイルの絶対パスを表示します。以下の`source`コマンドの`${your_shell_profile}`パスに合わせて変更する必要があります。

    ```shell
    source ${your_shell_profile}
    ```

3.  現在のセッションでクラスターを起動します。

    > **注記：**
    >
    > -   以下の方法で操作されたプレイグラウンドでは、デプロイとテストが完了すると、 TiUPクラスターデータが自動的にクリーンアップされます。コマンドを再実行すると、新しいクラスターが作成されます。
    > -   storageにデータを永続化したい場合は、クラスターの起動時にフラグ`--tag`を追加してください。詳細は[TiDBクラスタを起動するときにデータを保存するタグを指定します](/tiup/tiup-playground.md#specify-a-tag-when-starting-the-tidb-cluster-to-store-the-data)参照してください。
    >
    >     ```shell
    >     tiup playground --tag ${tag_name}
    >     ```

    -   1 つの TiDB インスタンス、1 つの TiKV インスタンス、1 つの PD インスタンス、および 1 つのTiFlashインスタンスを含む最新バージョンの TiDB クラスターを起動するには、次のコマンドを実行します。

        ```shell
        tiup playground
        ```

        このコマンドを初めて実行する場合、 TiUP は最新バージョンの TiDB をダウンロードし、クラスターを起動します。

        出力にはクラスターのエンドポイントのリストが表示されます。

        ```log
        🎉 TiDB Playground Cluster is started, enjoy!

        Connect TiDB:    mysql --comments --host 127.0.0.1 --port 4000 -u root
        TiDB Dashboard:  http://127.0.0.1:2379/dashboard
        Grafana:         http://127.0.0.1:3000
        ```

    -   TiDB のバージョンと各コンポーネントのインスタンスの数を指定するには、次のようなコマンドを実行します。

        ```shell
        tiup playground v8.5.5 --db 2 --pd 3 --kv 3
        ```

        利用可能なすべてのバージョンを表示するには、 `tiup list tidb`を実行します。

4.  TiDB クラスターのエンドポイントにアクセスするための新しいセッションを開始します。

    -   TiDB データベースに接続します。

        -   TiUPクライアントを使用して TiDB に接続します。

            ```shell
            tiup client
            ```

        -   あるいは、MySQL クライアントを使用して TiDB に接続することもできます。

            ```shell
            mysql --host 127.0.0.1 --port 4000 -u root
            ```

    -   プロメテウス: [http://127.0.0.1:9090](http://127.0.0.1:9090) .

    -   [TiDBダッシュボード](/dashboard/dashboard-intro.md) : [http://127.0.0.1:2379/ダッシュボード](http://127.0.0.1:2379/dashboard) 。デフォルトのユーザー名は`root` 、パスワードは空です。

    -   Grafana: [http://127.0.0.1:3000](http://127.0.0.1:3000) 。デフォルトのユーザー名とパスワードはどちらも`admin`です。

5.  (オプション) 分析用に[TiFlashにデータをロードする](/tiflash/tiflash-overview.md#use-tiflash) 。

6.  テスト後にクラスターをクリーンアップします。

    1.  <kbd>Control</kbd> + <kbd>C</kbd>を押してプロセスを停止します。

    2.  サービスを停止した後、次のコマンドを実行します。

        ```shell
        tiup clean --all
        ```

> **注記：**
>
> TiUP Playgroundはデフォルトで`127.0.0.1`リッスンしており、サービスはローカルでのみアクセス可能です。サービスを外部からアクセス可能にしたい場合は、 `--host`パラメータを使用してリッスンアドレスを指定し、ネットワークインターフェースカード（NIC）を外部からアクセス可能なIPアドレスにバインドします。

</div>
</SimpleTab>

## 単一のマシンで本番の展開をシミュレートする {#simulate-production-deployment-on-a-single-machine}

このセクションでは、完全なトポロジを持つ最小の TiDB クラスターを設定し、単一の Linuxサーバー上で本番の展開手順をシミュレートする方法について説明します。

以下では、 TiUPで最小トポロジの YAML ファイルを使用して TiDB クラスターをデプロイする方法について説明します。

### 準備する {#prepare}

TiDB クラスターを展開する前に、ターゲット マシンが次の要件を満たしていることを確認してください。

-   CentOS 7.3 以降のバージョンがインストールされています。
-   Linux OS はインターネットにアクセスできるため、TiDB および関連ソフトウェアのインストール パッケージをダウンロードする必要があります。

最小の TiDB クラスター トポロジは、次のインスタンスで構成されます。

| 実例      | カウント | IP       | コンフィグレーション            |
| :------ | :--- | :------- | :-------------------- |
| ティクブ    | 3    | 10.0.1.1 | 競合を避けるために増分ポート番号を使用する |
| ティドブ    | 1    | 10.0.1.1 | デフォルトのポートとその他の設定を使用する |
| PD      | 1    | 10.0.1.1 | デフォルトのポートとその他の設定を使用する |
| TiFlash | 1    | 10.0.1.1 | デフォルトのポートとその他の設定を使用する |
| モニター    | 1    | 10.0.1.1 | デフォルトのポートとその他の設定を使用する |

> **注記：**
>
> インスタンスのIPアドレスは例としてのみ提供されています。実際の導入では、IPアドレスを実際のIPアドレスに置き換えてください。

ターゲット マシンのその他の要件は次のとおりです。

-   `root`のユーザーとそのパスワードが必要です。
-   [対象マシンのファイアウォールサービスを停止します](/check-before-deployment.md#check-the-firewall-service-of-target-machines) 、または TiDB クラスター ノードに必要なポートを開きます。
-   現在、 TiUPクラスターは、x86_64 (AMD64) および ARM アーキテクチャでの TiDB のデプロイをサポートしています。

    -   AMD64アーキテクチャでは CentOS 7.3 以降のバージョンを使用することをお勧めします。
    -   ARMアーキテクチャでは CentOS 7.6 (1810) を使用することをお勧めします。

### デプロイ {#deploy}

> **注記：**
>
> 対象マシンには、通常のユーザーまたはユーザー`root`としてログインできます。以下の手順では、ユーザー`root`を例に説明します。

1.  TiUPをダウンロードしてインストールします:

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2.  グローバル環境変数を宣言します。

    > **注記：**
    >
    > インストール後、 TiUP は対応するシェルプロファイルファイルの絶対パスを表示します。以下の`source`コマンドの`${your_shell_profile}`パスに合わせて変更する必要があります。

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

5.  ルートユーザー権限を使用して、 `sshd`サービスへの接続制限を増やします。これは、 TiUPが複数のマシンへの展開をシミュレートする必要があるためです。

    1.  `/etc/ssh/sshd_config`を変更し、 `MaxSessions`を`20`に設定します。
    2.  `sshd`サービスを再起動します。

        ```shell
        service sshd restart
        ```

6.  クラスターを作成して起動します。

    次のテンプレートに従って[トポロジ構成ファイル](/tiup/tiup-cluster-topology-reference.md)作成および編集し、 `topo.yaml`という名前を付けます。

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

    -   `user: "tidb"` : クラスターの内部管理には、デプロイメント中に自動作成されるシステムユーザー`tidb`を使用します。デフォルトでは、ポート22を使用してSSH経由でターゲットマシンにログインします。
    -   `replication.enable-placement-rules` : この PD パラメータは、 TiFlashが正常に実行されるように設定されます。
    -   `host` : ターゲットマシンの IP。

7.  クラスター デプロイメント コマンドを実行します。

    ```shell
    tiup cluster deploy <cluster-name> <version> ./topo.yaml --user root -p
    ```

    -   `<cluster-name>` : クラスター名を設定します。
    -   `<version>` : TiDBクラスターのバージョンを設定します（例： `v8.5.5` ） `tiup list tidb`コマンドを実行すると、サポートされているすべてのTiDBバージョンを確認できます。
    -   `--user` : 環境を初期化するユーザーを指定します。
    -   `-p` : ターゲット マシンに接続するために使用するパスワードを指定します。

        > **注記：**
        >
        > 秘密鍵を使用する場合は、 `-i`で鍵のパスを指定できます。3と`-i` `-p`同時に使用しないでください。

    展開を完了するには、「y」と`root`のユーザーのパスワードを入力します。

    ```log
    Do you want to continue? [y/N]:  y
    Input SSH password:
    ```

8.  クラスターを起動します。

    ```shell
    tiup cluster start <cluster-name>
    ```

9.  クラスターのエンドポイントにアクセスします。

    -   MySQLクライアントをインストールします。すでにインストールされている場合は、この手順をスキップしてください。

        ```shell
        yum -y install mysql
        ```

    -   MySQLクライアントを使用してTiDBデータベースに接続します。パスワードは空です。

        ```shell
        mysql -h 10.0.1.1 -P 4000 -u root
        ```

    -   Grafana: [http://{grafana-ip}:3000](http://%7Bgrafana-ip%7D:3000) 。デフォルトのユーザー名とパスワードはどちらも`admin`です。

    -   [TiDBダッシュボード](/dashboard/dashboard-intro.md) : [http://{pd-ip}:2379/ダッシュボード](http://%7Bpd-ip%7D:2379/dashboard) 。デフォルトのユーザー名は`root` 、パスワードは空です。

10. (オプション) クラスターのリストとトポロジをビュー。

    -   クラスター リストを表示するには:

        ```shell
        tiup cluster list
        ```

    -   クラスターのトポロジとステータスを表示するには:

        ```shell
        tiup cluster display <cluster-name>
        ```

    `tiup cluster`コマンドの詳細については、 [TiUPクラスタコマンド](/tiup/tiup-component-cluster.md)参照してください。

11. テスト後にクラスターをクリーンアップします。

    1.  <kbd>Control</kbd> + <kbd>C</kbd>を押して上記の TiDB サービスを停止します。

    2.  サービスを停止した後、次のコマンドを実行します。

        ```shell
        tiup clean --all
        ```

## 次は何か {#what-s-next}

ローカル テスト環境用に TiDB クラスターをデプロイしたばかりの場合は、次の手順に従います。

-   [TiDBにおける基本的なSQL操作](/basic-sql-operations.md)を参照して、TiDB での基本的な SQL 操作について学習します。
-   [TiDBへのデータの移行](/migration-overview.md)を参照して TiDB にデータを移行することもできます。
-   TiUPを使用して TiDB クラスターを管理する方法の詳細については、 [TiUPの概要](/tiup/tiup-overview.md)を参照してください。

本番環境用に TiDB クラスターをデプロイする準備ができたら、次の手順に従います。

-   [TiUPを使用してTiDBをデプロイ](/production-deployment-using-tiup.md)
-   あるいは、 [Kubernetes 上の TiDB](https://docs.pingcap.com/tidb-in-kubernetes/stable)ドキュメントを参照して、 TiDB Operator を使用してクラウドに TiDB をデプロイすることもできます。

アプリケーション開発者であり、TiDB を使用してアプリケーションを迅速に構築したい場合は、次の手順に従ってください。

-   [開発者ガイドの概要](https://docs.pingcap.com/developer/)
-   [TiDB Cloudスタータークラスタを作成する](/develop/dev-guide-build-cluster-in-cloud.md)
-   [アプリケーション例](/develop/dev-guide-sample-application-java-jdbc.md)

TiFlashを使用した分析ソリューションをお探しの場合は、次の手順に従ってください。

-   [TiFlashの概要](/tiflash/tiflash-overview.md)
-   [TiFlashを使用する](/tiflash/tiflash-overview.md#use-tiflash)
