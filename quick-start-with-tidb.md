---
title: Quick Start Guide for the TiDB Database Platform
summary: Learn how to quickly get started with the TiDB platform and see if TiDB is the right choice for you.
---

# TiDB データベース プラットフォームのクイック スタート ガイド {#quick-start-guide-for-the-tidb-database-platform}

このガイドでは、TiDB の使用を開始するための最も簡単な方法について説明します。非本番環境では、次のいずれかの方法で TiDB データベースをデプロイできます。

-   [ローカル テスト クラスターをデプロイ](#deploy-a-local-test-cluster) (macOS および Linux の場合)
-   [1 台のマシンで本番のデプロイをシミュレートする](#simulate-production-deployment-on-a-single-machine) (Linux のみ)

> **ノート：**
>
> このガイドで提供されているデプロイ方法は、本番**用ではなく**、クイック スタート<strong>専用</strong>です。
>
> -   オンプレミスの本番クラスターをデプロイするには、 [本番インストール ガイド](/production-deployment-using-tiup.md)を参照してください。
> -   TiDB を Kubernetes にデプロイするには、 [Kubernetes で TiDB を使い始める](https://docs.pingcap.com/tidb-in-kubernetes/stable/get-started)を参照してください。
> -   クラウドで TiDB を管理するには、 [TiDB Cloudクイック スタート](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart)を参照してください。

## ローカル テスト クラスターをデプロイ {#deploy-a-local-test-cluster}

-   シナリオ: 単一の macOS または Linuxサーバーを使用して、テスト用にローカル TiDB クラスターをすばやく展開します。このようなクラスターをデプロイすることで、TiDB の基本的なアーキテクチャと、TiDB、TiKV、PD、および監視コンポーネントなどのコンポーネントの操作を学習できます。

<SimpleTab>
<div label="macOS">

分散システムとして、基本的な TiDB テスト クラスターは通常、2 つの TiDB インスタンス、3 つの TiKV インスタンス、3 つの PD インスタンス、およびオプションのTiFlashインスタンスで構成されます。 TiUP Playground を使用すると、次の手順を実行して、テスト クラスターをすばやく構築できます。

1.  TiUPをダウンロードしてインストールします。

    {{< copyable "" >}}

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

    上記の出力のシェル プロファイル パスに注意してください。次のステップでパスを使用する必要があります。

2.  グローバル環境変数を宣言します。

    > **ノート：**
    >
    > インストール後、 TiUP は対応するシェル プロファイル ファイルの絶対パスを表示します。パスに応じて、次の`source`コマンドの`${your_shell_profile}`を変更する必要があります。この場合、ステップ 1 の出力から`${your_shell_profile}`は`/Users/user/.zshrc`です。

    {{< copyable "" >}}

    ```shell
    source ${your_shell_profile}
    ```

3.  現在のセッションでクラスターを開始します。

    -   1 つの TiDB インスタンス、1 つの TiKV インスタンス、1 つの PD インスタンス、および 1 つのTiFlashインスタンスで最新バージョンの TiDB クラスターを開始する場合は、次のコマンドを実行します。

        {{< copyable "" >}}

        ```shell
        tiup playground
        ```

    -   TiDB のバージョンと各コンポーネントのインスタンス数を指定する場合は、次のようなコマンドを実行します。

        {{< copyable "" >}}

        ```shell
        tiup playground v6.5.2 --db 2 --pd 3 --kv 3
        ```

        このコマンドは、v6.5.2 などのバージョン クラスターをローカル マシンにダウンロードして起動します。最新バージョンを表示するには、 `tiup list tidb`を実行します。

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

        > **ノート：**
        >
        > -   v5.2.0 以降、TiDB は Apple M1 チップを使用するマシンでの`tiup playground`実行をサポートしています。
        > -   このように運用されているプレイグラウンドの場合、テスト デプロイが終了した後、 TiUP は元のクラスター データをクリーンアップします。コマンドを再実行すると、新しいクラスターが取得されます。
        > -   データをstorageに保持する場合は、 `tiup --tag <your-tag> playground ...`を実行します。詳細は[TiUPリファレンスガイド](/tiup/tiup-reference.md#-t---tag)を参照してください。

4.  TiDB にアクセスするための新しいセッションを開始します。

    -   TiUPクライアントを使用して TiDB に接続します。

        {{< copyable "" >}}

        ```shell
        tiup client
        ```

    -   MySQL クライアントを使用して TiDB に接続することもできます。

        {{< copyable "" >}}

        ```shell
        mysql --host 127.0.0.1 --port 4000 -u root
        ```

5.  [http://127.0.0.1:9090](http://127.0.0.1:9090)で TiDB の Prometheus ダッシュボードにアクセスします。

6.  [TiDB ダッシュボード](/dashboard/dashboard-intro.md)の[http://127.0.0.1:2379/ダッシュボード](http://127.0.0.1:2379/dashboard)にアクセスします。デフォルトのユーザー名は`root`で、パスワードは空です。

7.  [http://127.0.0.1:3000](http://127.0.0.1:3000)から TiDB の Grafana ダッシュボードにアクセスします。デフォルトのユーザー名とパスワードはどちらも`admin`です。

8.  (オプション) 分析用に[データをTiFlashにロードする](/tiflash/tiflash-overview.md#use-tiflash) 。

9.  テスト デプロイ後にクラスターをクリーンアップします。

    1.  <kbd>Control+C</kbd>を押して、上記の TiDB サービスを停止します。

    2.  サービスが停止したら、次のコマンドを実行します。

        {{< copyable "" >}}

        ```shell
        tiup clean --all
        ```

> **ノート：**
>
> TiUP Playground はデフォルトで`127.0.0.1`をリッスンし、サービスはローカルでのみアクセス可能です。サービスを外部からアクセスできるようにする場合は、 `--host`パラメータを使用してリッスン アドレスを指定し、ネットワーク インターフェイス カード (NIC) を外部からアクセス可能な IP アドレスにバインドします。

</div>
<div label="Linux">

分散システムとして、基本的な TiDB テスト クラスターは通常、2 つの TiDB インスタンス、3 つの TiKV インスタンス、3 つの PD インスタンス、およびオプションのTiFlashインスタンスで構成されます。 TiUP Playground を使用すると、次の手順を実行して、テスト クラスターをすばやく構築できます。

1.  TiUPをダウンロードしてインストールします。

    {{< copyable "" >}}

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

    上記の出力のシェル プロファイル パスに注意してください。次のステップでパスを使用する必要があります。

2.  グローバル環境変数を宣言します。

    > **ノート：**
    >
    > インストール後、 TiUP は対応するシェル プロファイル ファイルの絶対パスを表示します。パスに応じて、次の`source`コマンドの`${your_shell_profile}`を変更する必要があります。

    {{< copyable "" >}}

    ```shell
    source ${your_shell_profile}
    ```

3.  現在のセッションでクラスターを開始します。

    -   1 つの TiDB インスタンス、1 つの TiKV インスタンス、1 つの PD インスタンス、および 1 つのTiFlashインスタンスで最新バージョンの TiDB クラスターを開始する場合は、次のコマンドを実行します。

        {{< copyable "" >}}

        ```shell
        tiup playground
        ```

    -   TiDB のバージョンと各コンポーネントのインスタンス数を指定する場合は、次のようなコマンドを実行します。

        {{< copyable "" >}}

        ```shell
        tiup playground v6.5.2 --db 2 --pd 3 --kv 3
        ```

        このコマンドは、v6.5.2 などのバージョン クラスターをローカル マシンにダウンロードして起動します。最新バージョンを表示するには、 `tiup list tidb`を実行します。

        このコマンドは、クラスターのアクセス方法を返します。

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
        > このように運用されているプレイグラウンドの場合、テスト デプロイが終了した後、 TiUP は元のクラスター データをクリーンアップします。コマンドを再実行すると、新しいクラスターが取得されます。データをstorageに保持する場合は、 `tiup --tag <your-tag> playground ...`を実行します。詳細は[TiUPリファレンスガイド](/tiup/tiup-reference.md#-t---tag)を参照してください。

4.  TiDB にアクセスするための新しいセッションを開始します。

    -   TiUPクライアントを使用して TiDB に接続します。

        {{< copyable "" >}}

        ```shell
        tiup client
        ```

    -   MySQL クライアントを使用して TiDB に接続することもできます。

        {{< copyable "" >}}

        ```shell
        mysql --host 127.0.0.1 --port 4000 -u root
        ```

5.  [http://127.0.0.1:9090](http://127.0.0.1:9090)で TiDB の Prometheus ダッシュボードにアクセスします。

6.  [TiDB ダッシュボード](/dashboard/dashboard-intro.md)の[http://127.0.0.1:2379/ダッシュボード](http://127.0.0.1:2379/dashboard)にアクセスします。デフォルトのユーザー名は`root`で、パスワードは空です。

7.  [http://127.0.0.1:3000](http://127.0.0.1:3000)から TiDB の Grafana ダッシュボードにアクセスします。デフォルトのユーザー名とパスワードはどちらも`admin`です。

8.  (オプション) 分析用に[データをTiFlashにロードする](/tiflash/tiflash-overview.md#use-tiflash) 。

9.  テスト デプロイ後にクラスターをクリーンアップします。

    1.  <kbd>Control+C</kbd>を押してプロセスを停止します。

    2.  サービスが停止したら、次のコマンドを実行します。

        {{< copyable "" >}}

        ```shell
        tiup clean --all
        ```

> **ノート：**
>
> TiUP Playground はデフォルトで`127.0.0.1`をリッスンし、サービスはローカルでのみアクセス可能です。サービスを外部からアクセスできるようにする場合は、 `--host`パラメータを使用してリッスン アドレスを指定し、ネットワーク インターフェイス カード (NIC) を外部からアクセス可能な IP アドレスにバインドします。

</div>
</SimpleTab>

## 1 台のマシンで本番のデプロイをシミュレートする {#simulate-production-deployment-on-a-single-machine}

-   シナリオ: 完全なトポロジーを備えた最小の TiDB クラスターを体験し、単一の Linuxサーバーで本番環境の展開手順をシミュレートします。

このセクションでは、 TiUPで最小のトポロジの YAML ファイルを使用して TiDB クラスターをデプロイする方法について説明します。

### 準備 {#prepare}

次の要件を満たすターゲット マシンを準備します。

-   CentOS 7.3 以降のバージョンがインストールされている
-   Linux OS はインターネットにアクセスできます。これは、TiDB および関連するソフトウェア インストール パッケージをダウンロードするために必要です。

最小の TiDB クラスター トポロジは次のとおりです。

> **ノート：**
>
> 次のインスタンスの IP アドレスは、IP の例としてのみ機能します。実際の展開では、IP を実際の IP に置き換える必要があります。

| 実例      | カウント | 知財                                   | コンフィグレーション                    |
| :------ | :--- | :----------------------------------- | :---------------------------- |
| TiKV    | 3    | 10.0.1.1<br/> 10.0.1.1<br/> 10.0.1.1 | ポートとディレクトリの競合を避ける             |
| TiDB    | 1    | 10.0.1.1                             | デフォルトのポート<br/>グローバル ディレクトリの構成 |
| PD      | 1    | 10.0.1.1                             | デフォルトのポート<br/>グローバル ディレクトリの構成 |
| TiFlash | 1    | 10.0.1.1                             | デフォルトのポート<br/>グローバル ディレクトリの構成 |
| モニター    | 1    | 10.0.1.1                             | デフォルトのポート<br/>グローバル ディレクトリの構成 |

ターゲット マシンのその他の要件:

-   `root`ユーザーとそのパスワードが必要です
-   [ターゲット マシンのファイアウォール サービスを停止します](/check-before-deployment.md#check-and-stop-the-firewall-service-of-target-machines) 、または TiDB クラスターノードが必要とするポートを開く
-   現在、 TiUPクラスターは、x86_64 (AMD64) および ARM アーキテクチャーでの TiDB のデプロイをサポートしています。

    -   AMD64 では CentOS 7.3 以降のバージョンを使用することをお勧めします
    -   ARM では CentOS 7.6 1810 を使用することをお勧めします

### デプロイ {#deploy}

> **ノート：**
>
> 通常のユーザーまたは`root`ユーザーとしてターゲット マシンにログインできます。次の手順では、例として`root`人のユーザーを使用します。

1.  TiUPをダウンロードしてインストールします。

    {{< copyable "" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2.  グローバル環境変数を宣言します。

    > **ノート：**
    >
    > インストール後、 TiUP は対応するシェル プロファイル ファイルの絶対パスを表示します。パスに応じて、次の`source`コマンドの`${your_shell_profile}`を変更する必要があります。

    {{< copyable "" >}}

    ```shell
    source ${your_shell_profile}
    ```

3.  TiUPのクラスターコンポーネントをインストールします。

    {{< copyable "" >}}

    ```shell
    tiup cluster
    ```

4.  TiUPクラスターが既にマシンにインストールされている場合は、ソフトウェア バージョンを更新します。

    {{< copyable "" >}}

    ```shell
    tiup update --self && tiup update cluster
    ```

5.  `sshd`サービスの接続制限を増やすには、root ユーザー権限を使用します。これは、 TiUP が複数のマシンで展開をシミュレートする必要があるためです。

    1.  `/etc/ssh/sshd_config`を変更し、 `MaxSessions`を`20`に設定します。
    2.  `sshd`サービスを再起動します。

        {{< copyable "" >}}

        ```shell
        service sshd restart
        ```

6.  クラスターを作成して開始します。

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

    -   `user: "tidb"` : `tidb`システム ユーザー (デプロイ時に自動的に作成される) を使用して、クラスターの内部管理を実行します。デフォルトでは、ポート 22 を使用して SSH 経由でターゲット マシンにログインします。
    -   `replication.enable-placement-rules` : この PD パラメータは、 TiFlash が正常に動作するように設定されています。
    -   `host` : ターゲット マシンの IP。

7.  クラスタ デプロイ コマンドを実行します。

    {{< copyable "" >}}

    ```shell
    tiup cluster deploy <cluster-name> <version> ./topo.yaml --user root -p
    ```

    -   `<cluster-name>` : クラスター名を設定します
    -   `<version>` : `v6.5.2`などの TiDB クラスターのバージョンを設定します。 `tiup list tidb`コマンドを実行すると、サポートされている TiDB のすべてのバージョンを確認できます。
    -   `-p` : ターゲット マシンへの接続に使用するパスワードを指定します。

        > **ノート：**
        >
        > 秘密鍵を使用する場合は、 `-i`で鍵のパスを指定できます。 `-i`と`-p`を同時に使用しないでください。

    「y」と`root`人のユーザーのパスワードを入力して、デプロイを完了します。

    ```log
    Do you want to continue? [y/N]:  y
    Input SSH password:
    ```

8.  クラスターを開始します。

    {{< copyable "" >}}

    ```shell
    tiup cluster start <cluster-name>
    ```

9.  クラスターにアクセスします。

    -   MySQL クライアントをインストールします。すでにインストールされている場合は、この手順をスキップしてください。

        {{< copyable "" >}}

        ```shell
        yum -y install mysql
        ```

    -   TiDB にアクセスします。パスワードが空です:

        {{< copyable "" >}}

        ```shell
        mysql -h 10.0.1.1 -P 4000 -u root
        ```

    -   [http://{grafana-ip}:3000](http://%7Bgrafana-ip%7D:3000)で Grafana 監視ダッシュボードにアクセスします。デフォルトのユーザー名とパスワードは両方とも`admin`です。

    -   [TiDB ダッシュボード](/dashboard/dashboard-intro.md)の[http://{pd-ip}:2379/ダッシュボード](http://%7Bpd-ip%7D:2379/dashboard)にアクセスします。デフォルトのユーザー名は`root`で、パスワードは空です。

    -   現在デプロイされているクラスターのリストを表示するには:

        {{< copyable "" >}}

        ```shell
        tiup cluster list
        ```

    -   クラスタのトポロジとステータスを表示するには:

        {{< copyable "" >}}

        ```shell
        tiup cluster display <cluster-name>
        ```

## 次は何ですか {#what-s-next}

-   ローカル テスト環境用に TiDB クラスターをデプロイしたばかりの場合:

    -   学ぶ[TiDB での基本的な SQL 操作](/basic-sql-operations.md)
    -   [データを TiDB に移行する](/migration-overview.md)

-   本番環境用に TiDB クラスターをデプロイする準備ができている場合:

    -   [TiUPを使用して TiDBをデプロイ](/production-deployment-using-tiup.md)
    -   [TiDB Operatorを使用して TiDB on Cloudをデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/stable)

-   TiFlashを使用した分析ソリューションをお探しの場合:

    -   [TiFlashを使用する](/tiflash/tiflash-overview.md#use-tiflash)
    -   [TiFlashの概要](/tiflash/tiflash-overview.md)
