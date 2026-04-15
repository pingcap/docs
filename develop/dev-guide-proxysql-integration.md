---
title: Integrate TiDB with ProxySQL
summary: TiDB CloudとTiDB（セルフホスト型）をProxySQLと統合する方法を学びましょう。
aliases: ['/ja/tidb/stable/dev-guide-proxysql-integration/','/ja/tidb/dev/dev-guide-proxysql-integration/','/ja/tidbcloud/dev-guide-proxysql-integration/']
---

# TiDBとProxySQLを統合する {#integrate-tidb-with-proxysql}

このドキュメントでは、ProxySQL の概要を説明し、[開発環境](#development-environment)および[本番環境](#production-environment)で ProxySQL を TiDB と統合する方法を説明し、[クエリルーティングのシナリオ](#typical-scenario)を通じて統合の主な利点を示します。

TiDBとProxySQLについてさらに詳しく知りたい場合は、以下のリンクが参考になります。

-   [TiDB Cloud](https://docs.pingcap.com/tidbcloud)
-   [TiDB開発者ガイド](https://docs.pingcap.com/developer/)
-   [ProxySQLドキュメント](https://proxysql.com/documentation/)

## ProxySQLとは何ですか？ {#what-is-proxysql}

[ProxySQL](https://proxysql.com/)は、高性能なオープンソースのSQLプロキシです。柔軟なアーキテクチャを備え、様々な方法で導入できるため、多様なユースケースに最適です。例えば、ProxySQLは、頻繁にアクセスされるデータをキャッシュすることでパフォーマンスを向上させるために使用できます。

ProxySQLは、高速性、効率性、使いやすさを追求してゼロから設計されています。MySQLとの完全な互換性を持ち、高品質なSQLプロキシに期待されるすべての機能をサポートしています。さらに、ProxySQLには独自の機能が多数搭載されており、幅広いアプリケーションに最適な選択肢となっています。

## ProxySQLとの連携の理由とは？ {#why-proxysql-integration}

-   ProxySQL は、TiDB と対話する際のレイテンシーを短縮することで、アプリケーションのパフォーマンスを向上させるのに役立ちます。 Lambda などのサーバーレス関数を使用したスケーラブルなアプリケーションでワークロードが非決定的で急増する可能性がある場合や、大量のデータを読み込むクエリを実行するアプリケーションを構築している場合など、何を構築しているかに関係なく。 [接続プーリング](https://proxysql.com/documentation/detailed-answers-on-faq/)や[頻繁に使用されるクエリをキャッシュする](https://proxysql.com/documentation/query-cache/)可能性をキャッシュするなどの ProxySQL の強力な機能を活用することで、アプリケーションはすぐにメリットを得ることができます。
-   ProxySQL は、ProxySQL で利用できる簡単に設定できる機能である[クエリルール](#query-rules)利用することで、SQL インジェクションなどの SQL 脆弱性に対するアプリケーション セキュリティ保護の追加レイヤーとして機能します。
-   [ProxySQL](https://github.com/sysown/proxysql)と[TiDB](https://github.com/pingcap/tidb)どちらもオープンソースプロジェクトであるため、ベンダーロックインの心配がないというメリットを享受できます。

## デプロイメントアーキテクチャ {#deployment-architecture}

TiDB と ProxySQL を連携させる最も一般的な方法は、アプリケーションレイヤーと TiDB の間に ProxySQL をスタンドアロンの中間層として追加することです。しかし、この方法ではスケーラビリティと耐障害性が保証されず、ネットワークホップによるレイテンシーも増加します。これらの問題を回避するために、以下のように ProxySQL をサイドカーとしてデプロイする代替のデプロイアーキテクチャがあります。

![proxysql-client-side-tidb-cloud](/media/develop/proxysql-client-side-tidb-cloud.png)

> **注記：**
>
> 上記の図はあくまで参考用です。実際の導入アーキテクチャに合わせて適宜修正してください。

## 開発環境 {#development-environment}

このセクションでは、開発環境で TiDB と ProxySQL を統合する方法について説明します。ProxySQL 統合を開始するには、すべての[前提条件](#prerequisite)完了後。

-   オプション 1: [TiDB CloudとProxySQLを統合する](#option-1-integrate-tidb-cloud-with-proxysql)
-   オプション 2: [TiDB Self-ManagedをProxySQLと統合する](#option-2-integrate-tidb-self-managed-with-proxysql)

### 前提条件 {#prerequisites}

選択するオプションによっては、以下のパッケージが必要になる場合があります。

-   [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
-   [ドッカー](https://docs.docker.com/get-docker/)
-   [Python 3](https://www.python.org/downloads/)
-   [Docker Compose](https://docs.docker.com/compose/install/linux/)
-   [MySQLクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)

以下のインストール手順に従ってください。

<SimpleTab groupId="os">

<div label="macOS" value="macOS">

1.  Docker[ダウンロード](https://docs.docker.com/get-docker/)して起動します (Docker デスクトップには既に Docker Compose が含まれています)。
2.  Pythonと`mysql-client`をインストールするには、次のコマンドを実行してください。

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    brew install python mysql-client
    ```

</div>

<div label="CentOS" value="CentOS">

```bash
curl -fsSL https://get.docker.com | bash -s docker
yum install -y git python39 docker-ce docker-ce-cli containerd.io docker-compose-plugin mysql
systemctl start docker
```

</div>

<div label="Windows" value="Windows">

-   Gitをダウンロードしてインストールしてください。

    1.  [Git Windows ダウンロード](https://git-scm.com/download/win)ページから**64 ビット Git for Windows セットアップ**パッケージをダウンロードします。
    2.  セットアップウィザードの手順に従ってGitパッケージをインストールしてください。デフォルトのインストール設定を使用する場合は、 **「次へ」を**数回クリックしてください。

        ![proxysql-windows-git-install](/media/develop/proxysql-windows-git-install.png)

-   MySQL Shellをダウンロードしてインストールしてください。

    1.  [MySQL Community Server のダウンロード](https://dev.mysql.com/downloads/mysql/)ページから MySQL インストーラーの ZIP ファイルをダウンロードします。
    2.  ファイルを解凍し、 `mysql.exe`フォルダ内の`bin` } を探します。Git Bash で`bin`フォルダのパスをシステム変数に追加し、 `PATH`変数に設定する必要があります。

        ```bash
        echo 'export PATH="(your bin folder)":$PATH' >>~/.bash_profile
        source ~/.bash_profile
        ```

        例えば：

        ```bash
        echo 'export PATH="/c/Program Files (x86)/mysql-8.0.31-winx64/bin":$PATH' >>~/.bash_profile
        source ~/.bash_profile
        ```

-   Dockerをダウンロードしてインストールしてください。

    1.  [Dockerのダウンロード](https://www.docker.com/products/docker-desktop/)ページからDocker Desktopインストーラーをダウンロードします。
    2.  インストーラーをダブルクリックして実行してください。インストールが完了すると、再起動を促すメッセージが表示されます。

        ![proxysql-windows-docker-install](/media/develop/proxysql-windows-docker-install.png)

-   [Pythonのダウンロード](https://www.python.org/downloads/)ページから最新の Python 3 インストーラーをダウンロードして実行します。

</div>

</SimpleTab>

### オプション1： TiDB CloudとProxySQLを統合する {#option-1-integrate-tidb-cloud-with-proxysql}

この統合では、 [ProxySQLのDockerイメージ](https://hub.docker.com/r/proxysql/proxysql)イメージとTiDB Cloud Starterインスタンスを使用します。以下の手順でProxySQLをポート`16033`にセットアップしますので、このポートが利用可能であることを確認してください。

#### ステップ1. TiDB Cloud Starterインスタンスを作成する {#step-1-create-a-tidb-cloud-starter-instance}

1.  [無料のTiDB Cloud Starterインスタンスを作成します。](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart#step-1-create-a-starter-instance) TiDB Cloud Starterインスタンスに設定した root パスワードを覚えておいてください。
2.  後で使用するために、 TiDB Cloud Starterインスタンスのホスト名、ポート番号、およびユーザー名を取得してください。

    1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページで、対象のTiDB Cloud Starterインスタンスの名前をクリックすると、その概要ページに移動します。
    2.  概要ページで、 **[接続]**ペインを見つけて、 `Endpoint` 、 `Port` 、および`User`フィールドをコピーします。ここで`Endpoint`はTiDB Cloud Starterインスタンスのホスト名です。

#### ステップ2. ProxySQL構成ファイルを生成する {#step-2-generate-proxysql-configuration-files}

1.  TiDB および ProxySQL 用の[統合例のコードリポジトリ](https://github.com/pingcap-inc/tidb-proxysql-integration)クローンを作成します。

     <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

     </SimpleTab>

2.  `tidb-cloud-connect`フォルダに移動します。

     <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    cd tidb-proxysql-integration/example/tidb-cloud-connect
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    cd tidb-proxysql-integration/example/tidb-cloud-connect
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    cd tidb-proxysql-integration/example/tidb-cloud-connect
    ```

    </div>

     </SimpleTab>

3.  `proxysql-config.py`を実行してProxySQL構成ファイルを生成します。

     <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    python3 proxysql-config.py
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    python3 proxysql-config.py
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    python proxysql-config.py
    ```

    </div>

     </SimpleTab>

    プロンプトが表示されたら、 `Serverless Tier Host`のTiDB Cloud Starterインスタンスのエンドポイントを入力し、次にTiDB Cloud Starterインスタンスのユーザー名とパスワードを入力します。

    以下は出力例です。現在の`tidb-cloud-connect`フォルダーの下に 3 つの設定ファイルが生成されていることがわかります。

        [Begin] generating configuration files..
        tidb-cloud-connect.cnf generated successfully.
        proxysql-prepare.sql generated successfully.
        proxysql-connect.py generated successfully.
        [End] all files generated successfully and placed in the current folder.

#### ステップ3. ProxySQLの設定 {#step-3-configure-proxysql}

1.  Dockerを起動します。Dockerが既に起動している場合は、この手順をスキップしてください。

     <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    インストール済みのDockerのアイコンをダブルクリックして起動してください。

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    systemctl start docker
    ```

    </div>

    <div label="Windows" value="Windows">

    インストール済みのDockerのアイコンをダブルクリックして起動してください。

    </div>

     </SimpleTab>

2.  ProxySQLイメージをプルし、バックグラウンドでProxySQLコンテナを起動します。

     <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose up -d
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose up -d
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose up -d
    ```

    </div>

     </SimpleTab>

3.  ProxySQL と統合するには、次のコマンドを実行します。このコマンドは、 **ProxySQL 管理インターフェース**内で`proxysql-prepare.sql`を実行します。

     <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    </div>

     </SimpleTab>

    > **注記：**
    >
    > `proxysql-prepare.sql`スクリプトは、以下の処理を実行します。
    >
    > 1.  TiDB Cloud Starterインスタンスのユーザー名とパスワードを使用してユーザーを追加します。
    > 2.  ユーザーを監視アカウントに割り当てます。
    > 3.  TiDB Cloud Starterインスタンスをホストリストに追加します。
    > 4.  ProxySQLとTiDB Cloud Starterインスタンス間の安全な接続を有効にします。
    >
    > より深く理解するには、 `proxysql-prepare.sql`ファイルを確認することを強くお勧めします。 ProxySQL 構成の詳細については、 [ProxySQLのドキュメント](https://proxysql.com/documentation/proxysql-configuration/)参照してください。

    以下は出力例です。出力にTiDB Cloud Starterインスタンスのホスト名が表示されていることがわかります。これは、ProxySQLとTiDB Cloud Starterインスタンス間の接続が確立されていることを意味します。

        *************************** 1. row ***************************
            hostgroup_id: 0
                hostname: gateway01.us-west-2.prod.aws.tidbcloud.com
                    port: 4000
                gtid_port: 0
                    status: ONLINE
                    weight: 1
                compression: 0
            max_connections: 1000
        max_replication_lag: 0
                    use_ssl: 1
            max_latency_ms: 0
                    comment:

#### ステップ4. ProxySQL経由でTiDBに接続する {#step-4-connect-to-tidb-through-proxysql}

1.  TiDB Cloud Starterインスタンスに接続するには、 `proxysql-connect.py`を実行します。スクリプトは自動的に MySQL クライアントを起動し、 [ステップ2](#step-2-generate-proxysql-configuration-files)で指定したユーザー名とパスワードを使用して接続します。

     <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    python3 proxysql-connect.py
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    python3 proxysql-connect.py
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    python proxysql-connect.py
    ```

    </div>

     </SimpleTab>

2.  TiDB Cloud Starterインスタンスに接続した後、次のSQL文を使用して接続を検証できます。

    ```sql
    SELECT VERSION();
    ```

    TiDB のバージョンが表示されていれば、ProxySQL を介してTiDB Cloud Starterインスタンスに正常に接続されています。MySQL クライアントを終了するには、 `quit`と入力して<kbd>Enter キー</kbd>を押します。

    > **注記：**
    >
    > ***デバッグの場合：*** TiDB Cloud Starterインスタンスに接続できない場合は、ファイル`tidb-cloud-connect.cnf` 、 `proxysql-prepare.sql` 、および`proxysql-connect.py`確認してください。提供したサーバー情報が利用可能で正しいことを確認してください。

3.  コンテナを停止して削除し、前のディレクトリに戻るには、次のコマンドを実行します。

     <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose down
    cd -
    ```

    </div>

     </SimpleTab>

### オプション2：TiDB Self-ManagedをProxySQLと統合する {#option-2-integrate-tidb-self-managed-with-proxysql}

この統合では、 [TiDB](https://hub.docker.com/r/pingcap/tidb)と[ProxySQL](https://hub.docker.com/r/proxysql/proxysql)の Docker イメージを使用して環境をセットアップします。 [TiDB Self-Managedをインストールするその他の方法](/quick-start-with-tidb.md)ご自身の興味に応じて試してみることをお勧めします。

以下の手順では、ProxySQL と TiDB をそれぞれポート`6033`と`4000`にセットアップしますので、これらのポートが使用可能であることを確認してください。

1.  Dockerを起動します。Dockerが既に起動している場合は、この手順をスキップしてください。

     <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    インストール済みのDockerのアイコンをダブルクリックして起動してください。

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    systemctl start docker
    ```

    </div>

    <div label="Windows" value="Windows">

    インストール済みのDockerのアイコンをダブルクリックして起動してください。

    </div>

     </SimpleTab>

2.  TiDB および ProxySQL 用の[統合例のコードリポジトリ](https://github.com/pingcap-inc/tidb-proxysql-integration)クローンを作成します。

     <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

     </SimpleTab>

3.  ProxySQLとTiDBの最新イメージを取得します。

     <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    cd tidb-proxysql-integration && docker compose pull
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    cd tidb-proxysql-integration && docker compose pull
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    cd tidb-proxysql-integration && docker compose pull
    ```

    </div>

     </SimpleTab>

4.  TiDBとProxySQLの両方をコンテナとして実行する統合環境を起動します。

     <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose up -d
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose up -d
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose up -d
    ```

    </div>

     </SimpleTab>

    ProxySQL `6033`ポートにログインするには、 `root`ユーザー名と空のパスワードを使用できます。

5.  ProxySQL経由でTiDBに接続する：

     <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    mysql -u root -h 127.0.0.1 -P 6033
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    mysql -u root -h 127.0.0.1 -P 6033
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    mysql -u root -h 127.0.0.1 -P 6033
    ```

    </div>

     </SimpleTab>

6.  TiDBセルフマネージドクラスタに接続した後、次のSQLステートメントを使用して接続を検証できます。

    ```sql
    SELECT VERSION();
    ```

    TiDBのバージョンが表示されていれば、ProxySQL経由でTiDBコンテナへの接続は成功しています。

7.  コンテナを停止して削除し、前のディレクトリに戻るには、次のコマンドを実行します。

     <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose down
    cd -
    ```

    </div>

     </SimpleTab>

## 生産環境 {#production-environment}

本番環境では、完全マネージド型のサービスを受けるために、 [TiDB Cloud Dedicated](https://www.pingcap.com/tidb-cloud-dedicated/)直接利用することをお勧めします。

### 前提条件 {#prerequisite}

MySQL クライアントをダウンロードしてインストールします。たとえば、 [MySQLシェル](https://dev.mysql.com/downloads/shell/)。

### CentOS上でTiDB CloudとProxySQLを統合する {#integrate-tidb-cloud-with-proxysql-on-centos}

ProxySQLは様々なプラットフォームにインストールできます。以下ではCentOSを例として説明します。

サポートされているプラ​​ットフォームと対応するバージョン要件の完全なリストについては、 [ProxySQLのドキュメント](https://proxysql.com/documentation/installing-proxysql/)参照してください。

#### ステップ1. TiDB Cloud Dedicatedクラスタを作成する {#step-1-create-a-tidb-cloud-dedicated-cluster}

詳細な手順については、 [TiDB Cloud Dedicatedクラスターを作成する](https://docs.pingcap.com/tidbcloud/create-tidb-cluster)参照してください。

#### ステップ2. ProxySQLをインストールする {#step-2-install-proxysql}

1.  YUMリポジトリにProxySQLを追加する：

    ```bash
    cat > /etc/yum.repos.d/proxysql.repo << EOF
    [proxysql]
    name=ProxySQL YUM repository
    baseurl=https://repo.proxysql.com/ProxySQL/proxysql-2.4.x/centos/\$releasever
    gpgcheck=1
    gpgkey=https://repo.proxysql.com/ProxySQL/proxysql-2.4.x/repo_pub_key
    EOF
    ```

2.  ProxySQLをインストールします。

    ```bash
    yum install -y proxysql
    ```

3.  ProxySQLを起動します。

    ```bash
    systemctl start proxysql
    ```

ProxySQL のサポートされているプラ​​ットフォームとそのインストールの詳細については、 [ProxySQL README](https://github.com/sysown/proxysql#installation)または[ProxySQLのインストール手順書](https://proxysql.com/documentation/installing-proxysql/)を参照してください。

#### ステップ3. ProxySQLの設定 {#step-3-configure-proxysql}

ProxySQL を TiDB のプロキシとして使用するには、ProxySQL を構成する必要があります。これを行うには、 [ProxySQL管理インターフェース内でSQLステートメントを実行する](#option-1-configure-proxysql-using-the-admin-interface)(推奨) か、 [設定ファイル](#option-2-configure-proxysql-using-a-configuration-file)を使用します。

> **注記：**
>
> 次のセクションでは、ProxySQL の必要な構成項目のみをリストします。構成の包括的なリストについては、 [ProxySQLのドキュメント](https://proxysql.com/documentation/proxysql-configuration/)参照してください。

##### オプション1：管理インターフェースを使用してProxySQLを設定する {#option-1-configure-proxysql-using-the-admin-interface}

1.  ProxySQLの内部設定を再構成するには、任意のMySQLコマンドラインクライアントからアクセスできる標準のProxySQL管理インターフェースを使用します（デフォルトではポート`6032`で利用可能です）。

    ```bash
    mysql -u admin -padmin -h 127.0.0.1 -P6032 --prompt 'ProxySQL Admin> '
    ```

    上記の手順を実行すると、ProxySQLの管理画面が表示されます。

2.  使用するTiDB Cloud Dedicatedクラスターを構成します。ProxySQL に 1 つまたは複数のTiDB Cloud Dedicatedクラスターを追加できます。たとえば、次のステートメントは 1 つのTiDB Cloud Dedicatedクラスターを追加します。 `<tidb cloud dedicated cluster host>`と`<tidb cloud dedicated cluster port>`を、ご使用のTiDB Cloud Dedicatedエンドポイントとポートに置き換える必要があります (デフォルトのポートは`4000`です)。

    ```sql
    INSERT INTO mysql_servers(hostgroup_id, hostname, port) 
    VALUES 
      (
        0,
        '<tidb cloud dedicated cluster host>', 
        <tidb cloud dedicated cluster port>
      );
    LOAD mysql servers TO runtime;
    SAVE mysql servers TO DISK;
    ```

    > **注記：**
    >
    > -   `hostgroup_id` : ホストグループの ID を指定します。ProxySQL はホストグループを使用してクラスタを管理します。SQL トラフィックをこれらのクラスタに均等に分散するには、負荷分散が必要な複数のクラスタを同じホストグループに構成できます。読み取りと書き込みなどの目的でクラスタを区別するには、異なるホストグループを使用するように構成できます。
    > -   `hostname` : TiDB Cloud Dedicatedクラスターのエンドポイント。
    > -   `port` : TiDB Cloud Dedicatedクラスターのポート。

3.  プロキシログインユーザーを設定して、ユーザーがTiDB Cloud Dedicatedクラスタに対して適切な権限を持っていることを確認してください。以下のステートメントでは、「 *tidb cloud dedicated cluster username* 」と「 *tidb cloud dedicated cluster password* 」を、実際のTiDB Cloud Dedicatedクラスタのユーザー名とパスワードに置き換えてください。

    ```sql
    INSERT INTO mysql_users(
      username, password, active, default_hostgroup, 
      transaction_persistent
    ) 
    VALUES 
      (
        '<tidb cloud dedicated cluster username>', 
        '<tidb cloud dedicated cluster password>', 
        1, 0, 1
      );
    LOAD mysql users TO runtime;
    SAVE mysql users TO DISK;
    ```

    > **注記：**
    >
    > -   `username` : TiDB ユーザー名。
    > -   `password` : TiDB パスワード。
    > -   `active` : ユーザーがアクティブかどうかを制御します。 `1`ユーザーが**アクティブ**でログインに使用できることを示し、 `0`はユーザーが非アクティブであることを示します。
    > -   `default_hostgroup` : ユーザーが使用するデフォルトのホストグループ。クエリ ルールがトラフィックを特定のホストグループに上書きしない限り、SQL トラフィックはこのホストグループに分散されます。
    > -   `transaction_persistent` : `1`は、永続的なトランザクションを示します。ユーザーが接続内でトランザクションを開始すると、トランザクションがコミットまたはロールバックされるまで、すべてのクエリ ステートメントは同じホスト グループにルーティングされます。

##### オプション2：設定ファイルを使用してProxySQLを設定する {#option-2-configure-proxysql-using-a-configuration-file}

このオプションは、ProxySQL を構成するための代替方法としてのみ考慮してください。詳細については、 [設定ファイルによるProxySQLの設定](https://github.com/sysown/proxysql#configuring-proxysql-through-the-config-file)参照してください。

1.  既存のSQLiteデータベース（設定が内部的に保存されている場所）をすべて削除します。

    ```bash
    rm /var/lib/proxysql/proxysql.db
    ```

    > **警告：**
    >
    > SQLiteデータベースファイルを削除すると、ProxySQL管理インターフェースを使用して行った設定変更はすべて失われます。

2.  必要に応じて設定ファイル`/etc/proxysql.cnf`を変更してください。例:

        mysql_servers:
        (
            {
                address="<tidb cloud dedicated cluster host>"
                port=<tidb cloud dedicated cluster port>
                hostgroup=0
                max_connections=2000
            }
        )

        mysql_users:
        (
            {
                username = "<tidb cloud dedicated cluster username>"
                password = "<tidb cloud dedicated cluster password>"
                default_hostgroup = 0
                max_connections = 1000
                default_schema = "test"
                active = 1
                transaction_persistent = 1
            }
        )

    前述の例では：

    -   `address`および`port` : TiDB Cloud Dedicatedクラスターのエンドポイントとポートを指定します。
    -   `username`および`password` : TiDB Cloud Dedicatedクラスターのユーザー名とパスワードを指定します。

3.  ProxySQLを再起動してください。

    ```bash
    systemctl restart proxysql
    ```

    再起動後、SQLiteデータベースは自動的に作成されます。

> **警告：**
>
> 本番環境では、本番の認証情報を使用して ProxySQL を実行しないでください。 `proxysql`サービスを開始する前に、 `/etc/proxysql.cnf`ファイル内の`admin_credentials`変数を変更することで、デフォルト値を変更できます。

## 典型的なシナリオ {#typical-scenario}

このセクションでは、クエリルーティングを例にとり、ProxySQLをTiDBと統合することで得られるメリットの一部を紹介します。

### クエリルール {#query-rules}

データベースは、トラフィックの増加、コードの不具合、悪意のあるスパムなどによって過負荷状態になることがあります。ProxySQLのクエリルールを使用すれば、クエリのルーティング変更、書き換え、拒否などによって、これらの問題に迅速かつ効果的に対応できます。

![proxysql-client-side-rules](/media/develop/proxysql-client-side-rules.png)

> **注記：**
>
> 以下の手順では、TiDBとProxySQLのコンテナイメージを使用してクエリルールを設定します。まだプルしていない場合は、 を参照してください[統合セクション](#option-2-integrate-tidb-self-managed-with-proxysql)詳細な手順については、こちらをご覧ください。

1.  TiDB および ProxySQL 用の[統合例のコードリポジトリ](https://github.com/pingcap-inc/tidb-proxysql-integration)クローンを作成します。前の手順ですでにクローンを作成している場合は、この手順をスキップしてください。

     <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    git clone https://github.com/pingcap-inc/tidb-proxysql-integration.git
    ```

    </div>

     </SimpleTab>

2.  ProxySQLルールのサンプルディレクトリに移動します。

     <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    cd tidb-proxysql-integration/example/proxy-rule-admin-interface
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    cd tidb-proxysql-integration/example/proxy-rule-admin-interface
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    cd tidb-proxysql-integration/example/proxy-rule-admin-interface
    ```

    </div>

     </SimpleTab>

3.  以下のコマンドを実行して、2つのTiDBコンテナと1つのProxySQLコンテナを起動します。

     <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose up -d
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose up -d
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose up -d
    ```

    </div>

     </SimpleTab>

    全てが順調に進めば、以下のコンテナが起動されます。

    -   ポート`4001`および`4002`を介して公開される TiDB クラスタの 2 つの Docker コンテナ
    -   ポート`6034`を介して公開される ProxySQL Docker コンテナが 1 つあります。

4.  2 つの TiDB コンテナでは、 `mysql`を使用して同様のスキーマ定義を持つテーブルを作成し、次に異なるデータ ( `'tidb-server01-port-4001'` 、 `'tidb-server02-port-4002'` ) を挿入してこれらのコンテナを識別します。

     <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    mysql -u root -h 127.0.0.1 -P 4001 << EOF
    DROP TABLE IF EXISTS test.tidb_server;
    CREATE TABLE test.tidb_server (server_name VARCHAR(255));
    INSERT INTO test.tidb_server (server_name) VALUES ('tidb-server01-port-4001');
    EOF

    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    DROP TABLE IF EXISTS test.tidb_server;
    CREATE TABLE test.tidb_server (server_name VARCHAR(255));
    INSERT INTO test.tidb_server (server_name) VALUES ('tidb-server02-port-4002');
    EOF
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    mysql -u root -h 127.0.0.1 -P 4001 << EOF
    DROP TABLE IF EXISTS test.tidb_server;
    CREATE TABLE test.tidb_server (server_name VARCHAR(255));
    INSERT INTO test.tidb_server (server_name) VALUES ('tidb-server01-port-4001');
    EOF

    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    DROP TABLE IF EXISTS test.tidb_server;
    CREATE TABLE test.tidb_server (server_name VARCHAR(255));
    INSERT INTO test.tidb_server (server_name) VALUES ('tidb-server02-port-4002');
    EOF
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    mysql -u root -h 127.0.0.1 -P 4001 << EOF
    DROP TABLE IF EXISTS test.tidb_server;
    CREATE TABLE test.tidb_server (server_name VARCHAR(255));
    INSERT INTO test.tidb_server (server_name) VALUES ('tidb-server01-port-4001');
    EOF

    mysql -u root -h 127.0.0.1 -P 4002 << EOF
    DROP TABLE IF EXISTS test.tidb_server;
    CREATE TABLE test.tidb_server (server_name VARCHAR(255));
    INSERT INTO test.tidb_server (server_name) VALUES ('tidb-server02-port-4002');
    EOF
    ```

    </div>

     </SimpleTab>

5.  ProxySQL を構成するには、次のコマンドを実行します。このコマンドは、ProxySQL 管理インターフェイス内で`proxysql-prepare.sql`を実行し、TiDB コンテナと ProxySQL 間のプロキシ接続を確立します。

     <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose exec proxysql sh -c "mysql -uadmin -padmin -h127.0.0.1 -P6032 < ./proxysql-prepare.sql"
    ```

    </div>

     </SimpleTab>

    > **注記：**
    >
    > `proxysql-prepare.sql`は以下のことを行います。
    >
    > -   `hostgroup_id`を持つ TiDB クラスタを`0`および`1`として ProxySQL に追加します。
    > -   空のパスワードを持つユーザー`root`を追加し、 `default_hostgroup`を`0`に設定します。
    > -   `^SELECT.*FOR UPDATE$`ルールを追加し、 `rule_id`を`1`として、 `destination_hostgroup`を`0`として追加します。SQL ステートメントがこのルールに一致する場合、リクエストは`hostgroup`を`0`として TiDB クラスタに転送されます。
    > -   `^SELECT`ルールを追加し、 `rule_id`を`2`として、 `destination_hostgroup`を`1`として追加します。SQL ステートメントがこのルールに一致する場合、リクエストは`hostgroup`を`1`として TiDB クラスタに転送されます。
    >
    > より深く理解するには、 `proxysql-prepare.sql`ファイルを確認することを強くお勧めします。 ProxySQL 構成の詳細については、 [ProxySQLのドキュメント](https://proxysql.com/documentation/proxysql-configuration/)参照してください。

    ProxySQLパターンがクエリルールとどのように一致するかについての追加情報は以下のとおりです。

    -   ProxySQL は`rule_id`の昇順でルールを 1 つずつ照合しようとします。
    -   `^`記号は SQL ステートメントの開始と一致し、 `$`終了と一致します。

    ProxySQLの正規表現とパターンマッチングの詳細については、ProxySQLドキュメントの[mysql-query_processor_regex](https://proxysql.com/documentation/global-variables/mysql-variables/#mysql-query_processor_regex)参照してください。

    パラメータの完全なリストについては、ProxySQLドキュメントの[mysql_query_rules](https://proxysql.com/documentation/main-runtime/#mysql_query_rules)参照してください。

6.  設定を確認し、クエリルールが正しく機能するかどうかをチェックしてください。

    1.  `root`ユーザーとしてProxySQL MySQLインターフェースにログインしてください。

         <SimpleTab groupId="os">

        <div label="macOS" value="macOS">

        ```bash
        mysql -u root -h 127.0.0.1 -P 6034
        ```

        </div>

        <div label="CentOS" value="CentOS">

        ```bash
        mysql -u root -h 127.0.0.1 -P 6034
        ```

        </div>

        <div label="Windows (Git Bash)" value="Windows">

        ```bash
        mysql -u root -h 127.0.0.1 -P 6034
        ```

        </div>

         </SimpleTab>

    2.  以下のSQL文を実行してください。

        -   `SELECT`ステートメントを実行します。

            ```sql
            SELECT * FROM test.tidb_server;
            ```

            このステートメントは、ルールID `2`に一致し、ステートメントを`hostgroup 1`上の TiDB クラスタに転送します。

        -   `SELECT ... FOR UPDATE`ステートメントを実行します。

            ```sql
            SELECT * FROM test.tidb_server FOR UPDATE;
            ```

            このステートメントは、ルールID `1`に一致し、ステートメントを`hostgroup 0`上の TiDB クラスタに転送します。

        -   取引を開始する:

            ```sql
            BEGIN;
            INSERT INTO test.tidb_server (server_name) VALUES ('insert this and rollback later');
            SELECT * FROM test.tidb_server;
            ROLLBACK;
            ```

            このトランザクションでは、 `BEGIN`ステートメントはどのルールにも一致しません。デフォルトのホストグループ (この例では`hostgroup 0`が使用されます。ProxySQL はデフォルトでユーザー transaction_persistent を有効にしており、同じホストグループ内で同じトランザクション内のすべてのステートメントを実行するため、 `INSERT`および`SELECT * FROM test.tidb_server;`ステートメントも TiDB クラスタ`hostgroup 0`に転送されます。

        以下は出力例です。同様の出力が得られれば、ProxySQLによるクエリルールの設定は正常に完了しています。

        ```sql
        +-------------------------+
        | server_name             |
        +-------------------------+
        | tidb-server02-port-4002 |
        +-------------------------+
        +-------------------------+
        | server_name             |
        +-------------------------+
        | tidb-server01-port-4001 |
        +-------------------------+
        +--------------------------------+
        | server_name                    |
        +--------------------------------+
        | tidb-server01-port-4001        |
        | insert this and rollback later |
        +--------------------------------+
        ```

    3.  MySQLクライアントをいつでも終了するには、 `quit`と入力して<kbd>Enterキー</kbd>を押してください。

7.  コンテナを停止して削除し、前のディレクトリに戻るには、次のコマンドを実行します。

     <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    docker compose down
    cd -
    ```

    </div>

    <div label="Windows (Git Bash)" value="Windows">

    ```bash
    docker compose down
    cd -
    ```

    </div>

     </SimpleTab>

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
