---
title: ProxySQL Integration Guide
summary: Learn how to integrate TiDB Cloud and TiDB (self-hosted) with ProxySQL.
---

# TiDB と ProxySQL を統合する {#integrate-tidb-with-proxysql}

このドキュメントでは、ProxySQL の概要を説明し、 ProxySQL と TiDB を[開発環境](#development-environment)および[本番環境](#production-environment)で統合する方法を説明し、 [クエリルーティングのシナリオ](#typical-scenario)による主な統合の利点を示します。

TiDB と ProxySQL について詳しく知りたい場合は、次の便利なリンクを参照してください。

-   [TiDB Cloud](https://docs.pingcap.com/tidbcloud)
-   [TiDB 開発者ガイド](/develop/dev-guide-overview.md)
-   [ProxySQL ドキュメント](https://proxysql.com/documentation/)

## プロキシSQLとは何ですか? {#what-is-proxysql}

[プロキシSQL](https://proxysql.com/)は、高性能のオープンソース SQL プロキシです。柔軟なアーキテクチャを備えており、さまざまな方法で導入できるため、さまざまなユースケースに最適です。たとえば、ProxySQL を使用すると、頻繁にアクセスされるデータをキャッシュすることでパフォーマンスを向上できます。

ProxySQL は、高速かつ効率的で使いやすいように最初から設計されています。 MySQL と完全な互換性があり、高品質の SQL プロキシに期待されるすべての機能をサポートします。さらに、ProxySQL には、幅広いアプリケーションにとって理想的な選択肢となる、多数の独自の機能が備わっています。

## ProxySQL を統合する理由 {#why-proxysql-integration}

-   ProxySQL は、TiDB と対話する際のレイテンシーを短縮することで、アプリケーションのパフォーマンスを向上させるのに役立ちます。 Lambda などのサーバーレス関数を使用したスケーラブルなアプリケーションでワークロードが非決定的で急増する可能性がある場合や、大量のデータを読み込むクエリを実行するアプリケーションを構築している場合など、何を構築しているかに関係なく。 [接続プーリング](https://proxysql.com/documentation/detailed-answers-on-faq/)や[頻繁に使用されるクエリのキャッシュ](https://proxysql.com/documentation/query-cache/)などの ProxySQL の強力な機能を活用することで、アプリケーションはすぐにメリットを得ることができます。
-   ProxySQL は、ProxySQL で利用可能な構成が簡単な機能[クエリルール](#query-rules)を利用して、SQL インジェクションなどの SQL 脆弱性に対するアプリケーション セキュリティ保護の追加レイヤーとして機能します。
-   [プロキシSQL](https://github.com/sysown/proxysql)と[TiDB](https://github.com/pingcap/tidb)は両方ともオープンソース プロジェクトであるため、ベンダー ロックインがゼロのメリットを得ることができます。

## 導入アーキテクチャ {#deployment-architecture}

TiDB で ProxySQL をデプロイする最も明白な方法は、アプリケーションレイヤーと TiDB の間にスタンドアロンの仲介者として ProxySQL を追加することです。ただし、スケーラビリティと耐障害性は保証されておらず、ネットワーク ホップによるレイテンシーも追加されます。これらの問題を回避するための代替デプロイメントアーキテクチャは、次のように ProxySQL をサイドカーとしてデプロイすることです。

![proxysql-client-side-tidb-cloud](/media/develop/proxysql-client-side-tidb-cloud.png)

> **注記：**
>
> 前述の図は参考用です。実際の展開アーキテクチャに応じてこれを調整する必要があります。

## 開発環境 {#development-environment}

このセクションでは、開発環境で TiDB を ProxySQL と統合する方法について説明します。 ProxySQL 統合を開始するには、 [前提条件](#prerequisite)つをすべて準備した後、TiDB クラスターのタイプに応じて次のオプションのいずれかを選択できます。

-   オプション 1: [TiDB Cloudと ProxySQL を統合する](#option-1-integrate-tidb-cloud-with-proxysql)
-   オプション 2: [TiDB (セルフホスト型) を ProxySQL と統合する](#option-2-integrate-tidb-self-hosted-with-proxysql)

### 前提条件 {#prerequisites}

選択したオプションに応じて、次のパッケージが必要になる場合があります。

-   [ギット](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
-   [ドッカー](https://docs.docker.com/get-docker/)
-   [パイソン3](https://www.python.org/downloads/)
-   [Docker Compose](https://docs.docker.com/compose/install/linux/)
-   [MySQLクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)

以下のインストール手順に従ってください。

<SimpleTab groupId="os">

<div label="macOS" value="macOS">

1.  [ダウンロード](https://docs.docker.com/get-docker/)を選択して Docker を起動します (Docker デスクトップには既に Docker Compose が含まれています)。
2.  次のコマンドを実行して、Python と`mysql-client`をインストールします。

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

-   Git をダウンロードしてインストールします。

    1.  [Git Windowsのダウンロード](https://git-scm.com/download/win)ページから**64 ビット Git for Windows セットアップ**パッケージをダウンロードします。
    2.  セットアップ ウィザードに従って Git パッケージをインストールします。 **「次へ」を**数回クリックして、デフォルトのインストール設定を使用できます。

        ![proxysql-windows-git-install](/media/develop/proxysql-windows-git-install.png)

-   MySQL シェルをダウンロードしてインストールします。

    1.  [MySQL コミュニティ サーバーのダウンロード](https://dev.mysql.com/downloads/mysql/)ページからMySQLインストーラーのZIPファイルをダウンロードします。
    2.  ファイルを解凍し、 `bin`フォルダー内の`mysql.exe`を見つけます。 `bin`フォルダーのパスをシステム変数に追加し、それを Git Bash の`PATH`変数に設定する必要があります。

        ```bash
        echo 'export PATH="(your bin folder)":$PATH' >>~/.bash_profile
        source ~/.bash_profile
        ```

        例えば：

        ```bash
        echo 'export PATH="/c/Program Files (x86)/mysql-8.0.31-winx64/bin":$PATH' >>~/.bash_profile
        source ~/.bash_profile
        ```

-   Dockerをダウンロードしてインストールします。

    1.  [ドッカーのダウンロード](https://www.docker.com/products/docker-desktop/)ページからDocker Desktopインストーラーをダウンロードします。
    2.  インストーラーをダブルクリックして実行します。インストールが完了すると、再起動を求めるメッセージが表示されます。

        ![proxysql-windows-docker-install](/media/develop/proxysql-windows-docker-install.png)

-   [Pythonのダウンロード](https://www.python.org/downloads/)ページから最新の Python 3 インストーラーをダウンロードして実行します。

</div>

</SimpleTab>

### オプション 1: TiDB Cloudと ProxySQL を統合する {#option-1-integrate-tidb-cloud-with-proxysql}

この統合では、 [ProxySQL Docker イメージ](https://hub.docker.com/r/proxysql/proxysql) TiDB サーバーレス クラスターとともに使用します。次の手順では、ポート`16033`に ProxySQL をセットアップするため、このポートが使用可能であることを確認してください。

#### ステップ 1. TiDB サーバーレスクラスターを作成する {#step-1-create-a-tidb-serverless-cluster}

1.  [無料の TiDB サーバーレス クラスターを作成する](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart#step-1-create-a-tidb-cluster) 。クラスターに設定した root パスワードを覚えておいてください。
2.  後で使用するためにクラスターのホスト名、ポート、およびユーザー名を取得します。

    1.  [クラスター](https://tidbcloud.com/console/clusters)ページで、クラスター名をクリックしてクラスターの概要ページに移動します。
    2.  クラスターの概要ページで、 **[接続]**ペインを見つけて、 `Endpoint` 、 `Port` 、および`User`フィールドをコピーします。ここで、 `Endpoint`はクラスターのホスト名です。

#### ステップ 2. ProxySQL 構成ファイルを生成する {#step-2-generate-proxysql-configuration-files}

1.  TiDB と ProxySQL の[統合サンプルコードリポジトリ](https://github.com/pingcap-inc/tidb-proxysql-integration)をクローンします。

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

2.  `tidb-cloud-connect`フォルダーに変更します。

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

3.  `proxysql-config.py`を実行して ProxySQL 構成ファイルを生成します。

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

    プロンプトが表示されたら、クラスターのエンドポイントを`Serverless Tier Host`に入力し、クラスターのユーザー名とパスワードを入力します。

    以下は出力例です。現在の`tidb-cloud-connect`フォルダーの下に 3 つの構成ファイルが生成されていることがわかります。

        [Begin] generating configuration files..
        tidb-cloud-connect.cnf generated successfully.
        proxysql-prepare.sql generated successfully.
        proxysql-connect.py generated successfully.
        [End] all files generated successfully and placed in the current folder.

#### ステップ 3. ProxySQL を構成する {#step-3-configure-proxysql}

1.  Dockerを起動します。 Docker がすでに起動している場合は、この手順をスキップしてください。

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    インストールしたDockerのアイコンをダブルクリックして起動します。

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    systemctl start docker
    ```

    </div>

    <div label="Windows" value="Windows">

    インストールしたDockerのアイコンをダブルクリックして起動します。

    </div>

    </SimpleTab>

2.  ProxySQL イメージをプルし、バックグラウンドで ProxySQL コンテナを起動します。

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

3.  次のコマンドを実行して ProxySQL と統合します。これにより、 **ProxySQL Admin Interface**内で`proxysql-prepare.sql`が実行されます。

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
    > `proxysql-prepare.sql`スクリプトは次のことを行います。
    >
    > 1.  クラスターのユーザー名とパスワードを使用してユーザーを追加します。
    > 2.  ユーザーを監視アカウントに割り当てます。
    > 3.  TiDB サーバーレス クラスターをホストのリストに追加します。
    > 4.  ProxySQL と TiDB サーバーレス クラスター間の安全な接続を有効にします。
    >
    > より深く理解するには、 `proxysql-prepare.sql`ファイルを確認することを強くお勧めします。 ProxySQL 構成の詳細については、 [ProxySQL ドキュメント](https://proxysql.com/documentation/proxysql-configuration/)を参照してください。

    以下は出力例です。クラスターのホスト名が出力に表示されていることがわかります。これは、ProxySQL と TiDB サーバーレス クラスター間の接続が確立されていることを意味します。

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

#### ステップ 4. ProxySQL を介して TiDB クラスターに接続する {#step-4-connect-to-your-tidb-cluster-through-proxysql}

1.  TiDB クラスターに接続するには、 `proxysql-connect.py`を実行します。スクリプトは MySQL クライアントを自動的に起動し、 [ステップ2](#step-2-generate-proxysql-configuration-files)で指定したユーザー名とパスワードを接続に使用します。

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

2.  TiDB クラスターに接続した後、次の SQL ステートメントを使用して接続を検証できます。

    ```sql
    SELECT VERSION();
    ```

    TiDB バージョンが表示されたら、ProxySQL を介して TiDB サーバーレス クラスターに正常に接続されています。 MySQL クライアントをいつでも終了するには、 `quit`入力して<kbd>Enter</kbd>を押します。

    > **注記：**
    >
    > ***デバッグの場合:***クラスターに接続できない場合は、ファイル`tidb-cloud-connect.cnf` 、 `proxysql-prepare.sql` 、および`proxysql-connect.py`を確認してください。指定したサーバー情報が利用可能であり、正しいことを確認してください。

3.  コンテナを停止して削除し、前のディレクトリに移動するには、次のコマンドを実行します。

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

### オプション 2: TiDB (セルフホスト型) を ProxySQL と統合する {#option-2-integrate-tidb-self-hosted-with-proxysql}

この統合では、 [TiDB](https://hub.docker.com/r/pingcap/tidb)と[プロキシSQL](https://hub.docker.com/r/proxysql/proxysql)の Docker イメージを使用して環境をセットアップします。ご自身の興味に合わせて[TiDB をインストールするその他の方法 (セルフホスト型)](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb)を試してみることをお勧めします。

次の手順では、ProxySQL と TiDB をポート`6033`と`4000`にそれぞれセットアップするため、これらのポートが使用可能であることを確認してください。

1.  Dockerを起動します。 Docker がすでに起動している場合は、この手順をスキップしてください。

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    インストールしたDockerのアイコンをダブルクリックして起動します。

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    systemctl start docker
    ```

    </div>

    <div label="Windows" value="Windows">

    インストールしたDockerのアイコンをダブルクリックして起動します。

    </div>

    </SimpleTab>

2.  TiDB と ProxySQL の[統合サンプルコードリポジトリ](https://github.com/pingcap-inc/tidb-proxysql-integration)をクローンします。

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

3.  ProxySQL と TiDB の最新イメージをプルします。

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

4.  TiDB と ProxySQL の両方をコンテナーとして実行して、統合環境を開始します。

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

5.  ProxySQL 経由で TiDB に接続します。

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

6.  TiDB クラスターに接続した後、次の SQL ステートメントを使用して接続を検証できます。

    ```sql
    SELECT VERSION();
    ```

    TiDB バージョンが表示されたら、ProxySQL を介して TiDB コンテナに正常に接続されています。

7.  コンテナを停止して削除し、前のディレクトリに移動するには、次のコマンドを実行します。

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

## 本番環境 {#production-environment}

本番環境では、フルマネージド エクスペリエンスを得るために[TiDB Cloud](https://en.pingcap.com/tidb-cloud/)直接使用することをお勧めします。

### 前提条件 {#prerequisite}

MySQL クライアントをダウンロードしてインストールします。たとえば、 [MySQL シェル](https://dev.mysql.com/downloads/shell/) 。

### TiDB Cloudと CentOS 上の ProxySQL を統合する {#integrate-tidb-cloud-with-proxysql-on-centos}

ProxySQL はさまざまなプラットフォームにインストールできます。以下では CentOS を例に説明します。

サポートされているプラ​​ットフォームと対応するバージョン要件の完全なリストについては、 [ProxySQL ドキュメント](https://proxysql.com/documentation/installing-proxysql/)を参照してください。

#### ステップ 1. TiDB 専用クラスターを作成する {#step-1-create-a-tidb-dedicated-cluster}

詳細な手順については、 [TiDBクラスタを作成する](https://docs.pingcap.com/tidbcloud/create-tidb-cluster)を参照してください。

#### ステップ 2. ProxySQL をインストールする {#step-2-install-proxysql}

1.  ProxySQL を YUM リポジトリに追加します。

    ```bash
    cat > /etc/yum.repos.d/proxysql.repo << EOF
    [proxysql]
    name=ProxySQL YUM repository
    baseurl=https://repo.proxysql.com/ProxySQL/proxysql-2.4.x/centos/\$releasever
    gpgcheck=1
    gpgkey=https://repo.proxysql.com/ProxySQL/proxysql-2.4.x/repo_pub_key
    EOF
    ```

2.  ProxySQL をインストールします。

    ```bash
    yum install -y proxysql
    ```

3.  ProxySQL を開始します。

    ```bash
    systemctl start proxysql
    ```

ProxySQL のサポートされているプラ​​ットフォームとそのインストールの詳細については、 [ProxySQL の README](https://github.com/sysown/proxysql#installation)または[ProxySQL のインストールに関するドキュメント](https://proxysql.com/documentation/installing-proxysql/)を参照してください。

#### ステップ 3. ProxySQL を構成する {#step-3-configure-proxysql}

ProxySQL を TiDB のプロキシとして使用するには、ProxySQL を構成する必要があります。これを行うには、 [ProxySQL 管理インターフェイス内で SQL ステートメントを実行する](#option-1-configure-proxysql-using-the-admin-interface) (推奨) または[設定ファイル](#option-2-configure-proxysql-using-a-configuration-file)を使用します。

> **注記：**
>
> 次のセクションでは、ProxySQL の必要な構成項目のみをリストします。構成の包括的なリストについては、 [ProxySQL ドキュメント](https://proxysql.com/documentation/proxysql-configuration/)を参照してください。

##### オプション 1: 管理インターフェイスを使用して ProxySQL を構成する {#option-1-configure-proxysql-using-the-admin-interface}

1.  標準の ProxySQL 管理インターフェイスを使用して ProxySQL の内部を再構成します。これは、MySQL コマンド ライン クライアント (デフォルトでポート`6032`で利用可能) 経由でアクセスできます。

    ```bash
    mysql -u admin -padmin -h 127.0.0.1 -P6032 --prompt 'ProxySQL Admin> '
    ```

    上記の手順により、ProxySQL 管理プロンプトが表示されます。

2.  使用する TiDB クラスターを構成します。ここで、1 つまたは複数の TiDB クラスターを ProxySQL に追加できます。たとえば、次のステートメントは TiDB 専用クラスターを 1 つ追加します。 `<tidb cloud dedicated cluster host>`と`<tidb cloud dedicated cluster port>` TiDB Cloudエンドポイントとポートに置き換える必要があります (デフォルトのポートは`4000` )。

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
    > -   `hostgroup_id` : ホストグループのIDを指定します。 ProxySQL はホストグループを使用してクラスターを管理します。 SQL トラフィックをこれらのクラスターに均等に分散するには、同じホストグループへの負荷分散が必要な複数のクラスターを構成できます。読み取りおよび書き込み目的などでクラスターを区別するには、異なるホストグループを使用するようにクラスターを構成できます。
    > -   `hostname` : TiDB クラスターのエンドポイント。
    > -   `port` : TiDB クラスターのポート。

3.  プロキシ ログイン ユーザーを構成して、ユーザーが TiDB クラスターに対する適切な権限を持っていることを確認します。以下のステートメントでは、「 *tidb cloud dedicated Cluster username* 」と「 *tidb cloud dedicated clusta passwd* 」を、クラスターの実際のユーザー名とパスワードに置き換える必要があります。

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
    > -   `active` : ユーザーがアクティブかどうかを制御します。 `1`ユーザーが**アクティブで**ログインに使用できることを示し、 `0`ユーザーが非アクティブであることを示します。
    > -   `default_hostgroup` : ユーザーが使用するデフォルトのホストグループ。クエリ ルールによって特定のホストグループへのトラフィックがオーバーライドされない限り、SQL トラフィックが分散されます。
    > -   `transaction_persistent` : `1`永続的なトランザクションを示します。ユーザーが接続内でトランザクションを開始すると、トランザクションがコミットまたはロールバックされるまで、すべてのクエリ ステートメントが同じホストグループにルーティングされます。

##### オプション 2: 構成ファイルを使用して ProxySQL を構成する {#option-2-configure-proxysql-using-a-configuration-file}

このオプションは、ProxySQL を構成するための代替方法としてのみ考慮してください。詳細については、 [構成ファイルによる ProxySQL の構成](https://github.com/sysown/proxysql#configuring-proxysql-through-the-config-file)を参照してください。

1.  既存の SQLite データベース (構成が内部に保存されているデータベース) を削除します。

    ```bash
    rm /var/lib/proxysql/proxysql.db
    ```

    > **警告：**
    >
    > SQLite データベース ファイルを削除すると、ProxySQL 管理インターフェイスを使用して行われた構成の変更はすべて失われます。

2.  必要に応じて構成ファイル`/etc/proxysql.cnf`を変更します。例えば：

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

    前述の例では次のようになります。

    -   `address`および`port` : TiDB Cloudクラスターのエンドポイントとポートを指定します。
    -   `username`および`password` : TiDB Cloudクラスターのユーザー名とパスワードを指定します。

3.  ProxySQL を再起動します。

    ```bash
    systemctl restart proxysql
    ```

    再起動後、SQLite データベースが自動的に作成されます。

> **警告：**
>
> 本番では、デフォルトの資格情報を使用して ProxySQL を実行しないでください。 `proxysql`サービスを開始する前に、 `admin_credentials`変数を変更することで`/etc/proxysql.cnf`ファイルのデフォルトを変更できます。

## 典型的なシナリオ {#typical-scenario}

このセクションでは、クエリ ルーティングを例として、ProxySQL と TiDB を統合することで活用できる利点のいくつかを示します。

### クエリルール {#query-rules}

データベースは、高トラフィック、欠陥のあるコード、または悪意のあるスパムによって過負荷になる可能性があります。 ProxySQL のクエリ ルールを使用すると、クエリの再ルーティング、書き換え、または拒否により、これらの問題に迅速かつ効果的に対応できます。

![proxysql-client-side-rules](/media/develop/proxysql-client-side-rules.png)

> **注記：**
>
> 次の手順では、TiDB と ProxySQL のコンテナ イメージを使用してクエリ ルールを構成します。まだ引いていない場合は、 [統合セクション](#option-2-integrate-tidb-self-hosted-with-proxysql)参照して詳細な手順を確認してください。

1.  TiDB と ProxySQL の[統合サンプルコードリポジトリ](https://github.com/pingcap-inc/tidb-proxysql-integration)をクローンします。前の手順ですでにクローンを作成している場合は、この手順をスキップしてください。

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

2.  ProxySQL ルールのサンプル ディレクトリに移動します。

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

3.  次のコマンドを実行して、2 つの TiDB コンテナと 1 つの ProxySQL コンテナを起動します。

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

    すべてがうまくいけば、次のコンテナが開始されます。

    -   ポート`4001` 、 `4002`経由で公開される TiDB クラスターの 2 つの Docker コンテナー
    -   ポート`6034`経由で公開される 1 つの ProxySQL Docker コンテナ。

4.  2 つの TiDB コンテナーでは、 `mysql`を使用して同様のスキーマ定義を持つテーブルを作成し、異なるデータ ( `'tidb-server01-port-4001'` 、 `'tidb-server02-port-4002'` ) を挿入してこれらのコンテナーを識別します。

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

5.  次のコマンドを実行して ProxySQL を構成します。これにより、ProxySQL 管理インターフェイス内で`proxysql-prepare.sql`実行され、TiDB コンテナと ProxySQL の間にプロキシ接続が確立されます。

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
    > `proxysql-prepare.sql`は次のことを行います。
    >
    > -   ProxySQL に TiDB クラスターを`hostgroup_id`を`0`および`1`として追加します。
    > -   空のパスワードを持つユーザー`root`を追加し、 `default_hostgroup`を`0`に設定します。
    > -   ルール`^SELECT.*FOR UPDATE$`を`rule_id`を`1`として、 `destination_hostgroup` `0`として追加します。 SQL ステートメントがこのルールに一致する場合、リクエストは`hostgroup`を`0`として TiDB クラスターに転送されます。
    > -   ルール`^SELECT`を`rule_id`を`2`として、 `destination_hostgroup` `1`として追加します。 SQL ステートメントがこのルールに一致する場合、リクエストは`hostgroup`を`1`として TiDB クラスターに転送されます。
    >
    > より深く理解するには、 `proxysql-prepare.sql`ファイルを確認することを強くお勧めします。 ProxySQL 構成の詳細については、 [ProxySQL ドキュメント](https://proxysql.com/documentation/proxysql-configuration/)を参照してください。

    以下は、ProxySQL パターンがクエリ ルールとどのように一致するかに関する追加情報です。

    -   ProxySQL は、 `rule_id`の昇順でルールを 1 つずつ照合しようとします。
    -   `^`記号は SQL ステートメントの先頭に一致し、 `$`最後に一致します。

    ProxySQL の正規表現とパターン マッチングの詳細については、ProxySQL ドキュメントの[mysql-query_processor_regex](https://proxysql.com/documentation/global-variables/mysql-variables/#mysql-query_processor_regex)を参照してください。

    パラメータの完全なリストについては、ProxySQL ドキュメントの[mysql_query_rules](https://proxysql.com/documentation/main-runtime/#mysql_query_rules)を参照してください。

6.  構成を検証し、クエリ ルールが機能するかどうかを確認します。

    1.  ProxySQL MySQL インターフェイスに`root`ユーザーとしてログインします。

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

    2.  次の SQL ステートメントを実行します。

        -   `SELECT`ステートメントを実行します。

            ```sql
            SELECT * FROM test.tidb_server;
            ```

            このステートメントは、rule_id `2`と一致し、ステートメントを`hostgroup 1`の TiDB クラスターに転送します。

        -   `SELECT ... FOR UPDATE`ステートメントを実行します。

            ```sql
            SELECT * FROM test.tidb_server FOR UPDATE;
            ```

            このステートメントは、rule_id `1`と一致し、ステートメントを`hostgroup 0`の TiDB クラスターに転送します。

        -   トランザクションを開始します。

            ```sql
            BEGIN;
            INSERT INTO test.tidb_server (server_name) VALUES ('insert this and rollback later');
            SELECT * FROM test.tidb_server;
            ROLLBACK;
            ```

            このトランザクションでは、 `BEGIN`ステートメントはどのルールにも一致しません。デフォルトのホストグループ (この例では`hostgroup 0` ) が使用されます。 ProxySQL はデフォルトでユーザーtransaction_persistent を有効にし、同じホストグループ内の同じトランザクション内のすべてのステートメントを実行するため、 `INSERT`および`SELECT * FROM test.tidb_server;`ステートメントも TiDB クラスター`hostgroup 0`に転送されます。

        以下は出力例です。同様の出力が得られた場合は、ProxySQL を使用してクエリ ルールが正常に構成されています。

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

    3.  MySQL クライアントをいつでも終了するには、 `quit`入力して<kbd>Enter</kbd>を押します。

7.  コンテナを停止して削除し、前のディレクトリに移動するには、次のコマンドを実行します。

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
