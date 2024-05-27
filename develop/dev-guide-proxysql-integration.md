---
title: ProxySQL Integration Guide
summary: TiDB Cloudと TiDB (セルフホスト) を ProxySQL と統合する方法を学びます。
---

# TiDB と ProxySQL を統合する {#integrate-tidb-with-proxysql}

このドキュメントでは、ProxySQL の概要を説明し、 [開発環境](#development-environment)および[本番環境](#production-environment)で ProxySQL を TiDB と統合する方法を説明し、 [クエリルーティングのシナリオ](#typical-scenario)を通じて主要な統合の利点を示します。

TiDB と ProxySQL についてさらに詳しく知りたい場合は、次のような役立つリンクがあります。

-   [TiDB Cloud](https://docs.pingcap.com/tidbcloud)
-   [TiDB 開発者ガイド](/develop/dev-guide-overview.md)
-   [ProxySQL ドキュメント](https://proxysql.com/documentation/)

## ProxySQL とは何ですか? {#what-is-proxysql}

[プロキシSQL](https://proxysql.com/)は、高性能なオープンソースの SQL プロキシです。柔軟なアーキテクチャを備え、さまざまな方法で導入できるため、さまざまなユースケースに最適です。たとえば、ProxySQL を使用すると、頻繁にアクセスされるデータをキャッシュしてパフォーマンスを向上させることができます。

ProxySQL は、高速、効率的、そして使いやすいように徹底的に設計されています。MySQL と完全に互換性があり、高品質の SQL プロキシに期待されるすべての機能をサポートしています。さらに、ProxySQL には、さまざまなアプリケーションに最適な選択肢となる独自の機能が多数搭載されています。

## ProxySQL 統合の理由は何ですか? {#why-proxysql-integration}

-   ProxySQL は、TiDB とのやり取り時のレイテンシーを削減することで、アプリケーションのパフォーマンスを向上させることができます。構築するものが何であっても、つまり、ワークロードが非決定的で急増する可能性のある Lambda などのサーバーレス関数を使用するスケーラブルなアプリケーションであっても、大量のデータをロードするクエリを実行するアプリケーションを構築している場合でも、ProxySQL の[接続プーリング](https://proxysql.com/documentation/detailed-answers-on-faq/)や[頻繁に使用されるクエリをキャッシュする](https://proxysql.com/documentation/query-cache/)などの強力な機能を活用することで、アプリケーションはすぐにメリットを得ることができます。
-   ProxySQL は、ProxySQL で利用できる簡単に構成できる機能である[クエリルール](#query-rules)の助けを借りて、SQL インジェクションなどの SQL 脆弱性に対するアプリケーション セキュリティ保護の追加レイヤーとして機能します。
-   [プロキシSQL](https://github.com/sysown/proxysql)と[ティビ](https://github.com/pingcap/tidb)どちらもオープンソース プロジェクトなので、ベンダー ロックインがゼロになるというメリットが得られます。

## デプロイメントアーキテクチャ {#deployment-architecture}

ProxySQL を TiDB とともにデプロイする最も明白な方法は、アプリケーションレイヤーと TiDB の間に ProxySQL をスタンドアロンの仲介者として追加することです。ただし、スケーラビリティと障害耐性は保証されず、ネットワーク ホップによるレイテンシーも追加されます。これらの問題を回避するための代替のデプロイアーキテクチャは、次のように ProxySQL をサイドカーとしてデプロイすることです。

![proxysql-client-side-tidb-cloud](/media/develop/proxysql-client-side-tidb-cloud.png)

> **注記：**
>
> 上記の図は参考用です。実際の展開アーキテクチャに合わせて調整する必要があります。

## 開発環境 {#development-environment}

このセクションでは、開発環境で TiDB を ProxySQL と統合する方法について説明します。ProxySQL 統合を開始するには、 [前提条件](#prerequisite)をすべて準備した後、TiDB クラスターの種類に応じて次のいずれかのオプションを選択できます。

-   オプション1: [TiDB Cloudと ProxySQL を統合する](#option-1-integrate-tidb-cloud-with-proxysql)
-   オプション2: [TiDB（セルフホスト）をProxySQLと統合する](#option-2-integrate-tidb-self-hosted-with-proxysql)

### 前提条件 {#prerequisites}

選択したオプションに応じて、次のパッケージが必要になる場合があります。

-   [ギット](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
-   [ドッカー](https://docs.docker.com/get-docker/)
-   [Python3 について](https://www.python.org/downloads/)
-   [Docker の作成](https://docs.docker.com/compose/install/linux/)
-   [MySQL クライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)

以下のインストール手順に従ってください。

<SimpleTab groupId="os">

<div label="macOS" value="macOS">

1.  [ダウンロード](https://docs.docker.com/get-docker/)インストールして Docker を起動します (Docker Desktop にはすでに Docker Compose が含まれています)。
2.  次のコマンドを実行して、Python と`mysql-client`インストールします。

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

    1.  [Git Windows ダウンロード](https://git-scm.com/download/win)ページから**64 ビット Git for Windows セットアップ**パッケージをダウンロードします。
    2.  セットアップ ウィザードに従って Git パッケージをインストールします。デフォルトのインストール設定を使用するには、 **[次へ]**を数回クリックします。

        ![proxysql-windows-git-install](/media/develop/proxysql-windows-git-install.png)

-   MySQL Shell をダウンロードしてインストールします。

    1.  [MySQL コミュニティ サーバーのダウンロード](https://dev.mysql.com/downloads/mysql/)ページ目からMySQLインストーラーのZIPファイルをダウンロードします。
    2.  ファイル`bin`解凍し、 `bin`フォルダ内の`mysql.exe`を見つけます。5 フォルダのパスをシステム変数に追加し、Git Bash の`PATH`変数に設定する必要があります。

        ```bash
        echo 'export PATH="(your bin folder)":$PATH' >>~/.bash_profile
        source ~/.bash_profile
        ```

        例えば：

        ```bash
        echo 'export PATH="/c/Program Files (x86)/mysql-8.0.31-winx64/bin":$PATH' >>~/.bash_profile
        source ~/.bash_profile
        ```

-   Docker をダウンロードしてインストールします。

    1.  [Docker ダウンロード](https://www.docker.com/products/docker-desktop/)ページ目から Docker Desktop インストーラーをダウンロードします。
    2.  インストーラーをダブルクリックして実行します。インストールが完了すると、再起動を求めるメッセージが表示されます。

        ![proxysql-windows-docker-install](/media/develop/proxysql-windows-docker-install.png)

-   [Python ダウンロード](https://www.python.org/downloads/)ページから最新の Python 3 インストーラーをダウンロードして実行します。

</div>

</SimpleTab>

### オプション 1: TiDB Cloudを ProxySQL と統合する {#option-1-integrate-tidb-cloud-with-proxysql}

この統合では、 [ProxySQL Docker イメージ](https://hub.docker.com/r/proxysql/proxysql) TiDB Serverless クラスターとともに使用します。次の手順では、ポート`16033`に ProxySQL を設定するので、このポートが使用可能であることを確認してください。

#### ステップ1. TiDBサーバーレスクラスターを作成する {#step-1-create-a-tidb-serverless-cluster}

1.  [無料のTiDBサーバーレスクラスターを作成する](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart#step-1-create-a-tidb-cluster) 。クラスターに設定したルートパスワードを覚えておいてください。
2.  後で使用するために、クラスターのホスト名、ポート、およびユーザー名を取得します。

    1.  [クラスター](https://tidbcloud.com/console/clusters)ページで、クラスター名をクリックしてクラスターの概要ページに移動します。
    2.  クラスターの概要ページで、 **[接続]**ペインを見つけて、 `Endpoint` 、 `Port` 、および`User`フィールドをコピーします。ここで、 `Endpoint`はクラスターのホスト名です。

#### ステップ2. ProxySQL構成ファイルを生成する {#step-2-generate-proxysql-configuration-files}

1.  TiDB および ProxySQL の[統合サンプルコードリポジトリ](https://github.com/pingcap-inc/tidb-proxysql-integration)をクローンします。

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

2.  `tidb-cloud-connect`フォルダに変更します:

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

3.  `proxysql-config.py`実行して ProxySQL 構成ファイルを生成します。

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

    プロンプトが表示されたら、 `Serverless Tier Host`にクラスターのエンドポイントを入力し、クラスターのユーザー名とパスワードを入力します。

    以下は出力例です。現在の`tidb-cloud-connect`フォルダーの下に 3 つの構成ファイルが生成されていることがわかります。

        [Begin] generating configuration files..
        tidb-cloud-connect.cnf generated successfully.
        proxysql-prepare.sql generated successfully.
        proxysql-connect.py generated successfully.
        [End] all files generated successfully and placed in the current folder.

#### ステップ3. ProxySQLを構成する {#step-3-configure-proxysql}

1.  Docker を起動します。Docker がすでに起動している場合は、この手順をスキップしてください。

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    インストールした Docker のアイコンをダブルクリックして起動します。

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    systemctl start docker
    ```

    </div>

    <div label="Windows" value="Windows">

    インストールした Docker のアイコンをダブルクリックして起動します。

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

3.  次のコマンドを実行して ProxySQL と統合します。このコマンドは、 **ProxySQL 管理インターフェース**内で`proxysql-prepare.sql`実行します。

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
    > `proxysql-prepare.sql`スクリプトは次のことを実行します。
    >
    > 1.  クラスターのユーザー名とパスワードを使用してユーザーを追加します。
    > 2.  ユーザーを監視アカウントに割り当てます。
    > 3.  TiDB Serverless クラスターをホストのリストに追加します。
    > 4.  ProxySQL と TiDB Serverless クラスター間の安全な接続を有効にします。
    >
    > より深く理解するために、 `proxysql-prepare.sql`ファイルを確認することを強くお勧めします。ProxySQL 構成の詳細については、 [ProxySQL ドキュメント](https://proxysql.com/documentation/proxysql-configuration/)を参照してください。

    以下は出力例です。出力にクラスターのホスト名が表示されています。これは、ProxySQL と TiDB Serverless クラスター間の接続が確立されていることを意味します。

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

#### ステップ4. ProxySQL経由でTiDBクラスターに接続する {#step-4-connect-to-your-tidb-cluster-through-proxysql}

1.  TiDB クラスターに接続するには、 `proxysql-connect.py`実行します。スクリプトは自動的に MySQL クライアントを起動し、 [ステップ2](#step-2-generate-proxysql-configuration-files)で指定したユーザー名とパスワードを使用して接続します。

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

    TiDB のバージョンが表示されている場合は、ProxySQL を介して TiDB Serverless クラスターに正常に接続されています。MySQL クライアントをいつでも終了するには、 `quit`入力して<kbd>Enter キー</kbd>を押します。

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

### オプション 2: TiDB (セルフホスト) を ProxySQL と統合する {#option-2-integrate-tidb-self-hosted-with-proxysql}

この統合では、 [ティビ](https://hub.docker.com/r/pingcap/tidb)と[プロキシSQL](https://hub.docker.com/r/proxysql/proxysql)の Docker イメージを使用して環境をセットアップします。興味があれば[TiDB をインストールする他の方法 (セルフホスト)](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb)を試してみることをお勧めします。

次の手順では、それぞれポート`6033`と`4000`に ProxySQL と TiDB を設定するので、これらのポートが使用可能であることを確認してください。

1.  Docker を起動します。Docker がすでに起動している場合は、この手順をスキップしてください。

    <SimpleTab groupId="os">

    <div label="macOS" value="macOS">

    インストールした Docker のアイコンをダブルクリックして起動します。

    </div>

    <div label="CentOS" value="CentOS">

    ```bash
    systemctl start docker
    ```

    </div>

    <div label="Windows" value="Windows">

    インストールした Docker のアイコンをダブルクリックして起動します。

    </div>

    </SimpleTab>

2.  TiDB および ProxySQL の[統合サンプルコードリポジトリ](https://github.com/pingcap-inc/tidb-proxysql-integration)をクローンします。

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

3.  ProxySQL と TiDB の最新イメージを取得します。

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

4.  コンテナとして実行される TiDB と ProxySQL の両方を使用して統合環境を開始します。

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

    ProxySQL `6033`ポートにログインするには、空のパスワードを持つ`root`ユーザー名を使用できます。

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

    TiDB バージョンが表示されている場合は、ProxySQL を介して TiDB コンテナーに正常に接続されています。

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

本番環境では、完全に管理されたエクスペリエンスを実現するために[TiDB Cloud](https://en.pingcap.com/tidb-cloud/)直接使用することをお勧めします。

### 前提条件 {#prerequisite}

MySQL クライアントをダウンロードしてインストールします。たとえば、 [MySQL シェル](https://dev.mysql.com/downloads/shell/) 。

### CentOS 上の ProxySQL とTiDB Cloudを統合する {#integrate-tidb-cloud-with-proxysql-on-centos}

ProxySQL はさまざまなプラットフォームにインストールできます。以下では CentOS を例に説明します。

サポートされているプラ​​ットフォームと対応するバージョン要件の完全なリストについては、 [ProxySQL ドキュメント](https://proxysql.com/documentation/installing-proxysql/)参照してください。

#### ステップ1. TiDB専用クラスターを作成する {#step-1-create-a-tidb-dedicated-cluster}

詳細な手順については[TiDBクラスタを作成する](https://docs.pingcap.com/tidbcloud/create-tidb-cluster)参照してください。

#### ステップ2. ProxySQLをインストールする {#step-2-install-proxysql}

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

3.  ProxySQLを起動します:

    ```bash
    systemctl start proxysql
    ```

ProxySQL のサポートされているプラ​​ットフォームとそのインストールの詳細については、 [ProxySQL README](https://github.com/sysown/proxysql#installation)または[ProxySQL インストール ドキュメント](https://proxysql.com/documentation/installing-proxysql/)を参照してください。

#### ステップ3. ProxySQLを構成する {#step-3-configure-proxysql}

ProxySQL を TiDB のプロキシとして使用するには、ProxySQL を構成する必要があります。これを行うには、 [ProxySQL管理インターフェース内でSQL文を実行する](#option-1-configure-proxysql-using-the-admin-interface) (推奨) または[設定ファイル](#option-2-configure-proxysql-using-a-configuration-file)を使用します。

> **注記：**
>
> 以下のセクションでは、ProxySQL の必須構成項目のみをリストします。構成の包括的なリストについては、 [ProxySQL ドキュメント](https://proxysql.com/documentation/proxysql-configuration/)を参照してください。

##### オプション 1: 管理インターフェースを使用して ProxySQL を構成する {#option-1-configure-proxysql-using-the-admin-interface}

1.  任意の MySQL コマンドライン クライアント (デフォルトではポート`6032`で使用可能) からアクセスできる標準の ProxySQL 管理インターフェイスを使用して、ProxySQL の内部を再構成します。

    ```bash
    mysql -u admin -padmin -h 127.0.0.1 -P6032 --prompt 'ProxySQL Admin> '
    ```

    上記の手順を実行すると、ProxySQL 管理者プロンプトが表示されます。

2.  使用する TiDB クラスターを構成します。ここでは、1 つまたは複数の TiDB クラスターを ProxySQL に追加できます。次のステートメントは、たとえば`<tidb cloud dedicated cluster host>`つの TiDB 専用クラスターを追加します。1 と`<tidb cloud dedicated cluster port>` TiDB Cloudエンドポイントとポートに置き換える必要があります (デフォルトのポートは`4000`です)。

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
    > -   `hostgroup_id` : ホストグループの ID を指定します。ProxySQL はホストグループを使用してクラスターを管理します。これらのクラスターに SQL トラフィックを均等に分散するには、同じホストグループに負荷分散する必要がある複数のクラスターを構成できます。読み取りや書き込みなどの目的でクラスターを区別するには、異なるホストグループを使用するようにクラスターを構成できます。
    > -   `hostname` : TiDB クラスターのエンドポイント。
    > -   `port` : TiDB クラスターのポート。

3.  プロキシ ログイン ユーザーを構成して、ユーザーが TiDB クラスターに対して適切な権限を持っていることを確認します。次のステートメントでは、「 *tidb cloud 専用クラスター ユーザー名*」と「 *tidb クラウド 専用クラスター パスワード*」をクラスターの実際のユーザー名とパスワードに置き換える必要があります。

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
    > -   `active` : ユーザーがアクティブかどうかを制御します。2 `1`ユーザーが**アクティブ**でログインに使用できることを示し、 `0`ユーザーが非アクティブであることを示します。
    > -   `default_hostgroup` : ユーザーが使用するデフォルトのホストグループ。クエリ ルールによって特定のホストグループへのトラフィックがオーバーライドされない限り、SQL トラフィックが分散されます。
    > -   `transaction_persistent` : `1`永続的なトランザクションを示します。ユーザーが接続内でトランザクションを開始すると、トランザクションがコミットまたはロールバックされるまで、すべてのクエリ ステートメントは同じホスト グループにルーティングされます。

##### オプション 2: 構成ファイルを使用して ProxySQL を構成する {#option-2-configure-proxysql-using-a-configuration-file}

このオプションは、ProxySQL を構成するための代替方法としてのみ検討してください。詳細については、 [設定ファイルによるProxySQLの設定](https://github.com/sysown/proxysql#configuring-proxysql-through-the-config-file)を参照してください。

1.  既存の SQLite データベース (構成が内部に保存されている場所) を削除します。

    ```bash
    rm /var/lib/proxysql/proxysql.db
    ```

    > **警告：**
    >
    > SQLite データベース ファイルを削除すると、ProxySQL 管理インターフェイスを使用して行われた構成の変更はすべて失われます。

2.  必要に応じて設定ファイル`/etc/proxysql.cnf`を変更します。例:

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

    上記の例では、

    -   `address`および`port` : TiDB Cloudクラスターのエンドポイントとポートを指定します。
    -   `username`および`password` : TiDB Cloudクラスターのユーザー名とパスワードを指定します。

3.  ProxySQLを再起動します。

    ```bash
    systemctl restart proxysql
    ```

    再起動後、SQLite データベースが自動的に作成されます。

> **警告：**
>
> 本番では、デフォルトの資格情報を使用して ProxySQL を実行しないでください。1 サービスを開始する前に、 `proxysql`変数`admin_credentials`変更して`/etc/proxysql.cnf`ファイルのデフォルトを変更できます。

## 典型的なシナリオ {#typical-scenario}

このセクションでは、クエリ ルーティングを例に、ProxySQL と TiDB を統合することで得られる利点のいくつかを示します。

### クエリルール {#query-rules}

データベースは、高トラフィック、欠陥のあるコード、または悪意のあるスパムによって過負荷になる可能性があります。ProxySQL のクエリ ルールを使用すると、クエリを再ルーティング、書き換え、または拒否することで、これらの問題に迅速かつ効果的に対応できます。

![proxysql-client-side-rules](/media/develop/proxysql-client-side-rules.png)

> **注記：**
>
> 次の手順では、TiDB と ProxySQL のコンテナ イメージを使用してクエリ ルールを構成します。まだ取得していない場合は、詳細な手順については[統合セクション](#option-2-integrate-tidb-self-hosted-with-proxysql)参照してください。

1.  TiDB および ProxySQL の[統合サンプルコードリポジトリ](https://github.com/pingcap-inc/tidb-proxysql-integration)クローンします。前の手順ですでにクローンしている場合は、この手順をスキップします。

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

2.  ProxySQL ルールのサンプル ディレクトリに変更します。

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

    すべてがうまくいけば、次のコンテナが起動します。

    -   ポート`4001` `4002`で公開される TiDB クラスターの 2 つの Docker コンテナ
    -   ポート`6034`経由で公開される 1 つの ProxySQL Docker コンテナー。

4.  2 つの TiDB コンテナで、 `mysql`を使用して同様のスキーマ定義を持つテーブルを作成し、 `'tidb-server02-port-4002'`データ ( `'tidb-server01-port-4001'` ) を挿入してこれらのコンテナを識別します。

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

5.  次のコマンドを実行して ProxySQL を構成します。このコマンドは、ProxySQL 管理インターフェイス内で`proxysql-prepare.sql`実行し、TiDB コンテナーと ProxySQL の間にプロキシ接続を確立します。

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
    > `proxysql-prepare.sql`次のことを行います。
    >
    > -   `hostgroup_id` ProxySQL に TiDB クラスターを`0`および`1`として追加します。
    > -   空のパスワードを持つユーザー`root`追加し、 `default_hostgroup`を`0`に設定します。
    > -   `rule_id`を`1` 、 `destination_hostgroup`を`0`とするルール`^SELECT.*FOR UPDATE$`を追加します。SQL ステートメントがこのルールに一致する場合、リクエストは`hostgroup`を`0`として TiDB クラスターに転送されます。
    > -   `rule_id`を`2` 、 `destination_hostgroup`を`1`とするルール`^SELECT`を追加します。SQL ステートメントがこのルールに一致する場合、リクエストは`hostgroup`を`1`として TiDB クラスターに転送されます。
    >
    > より深く理解するために、 `proxysql-prepare.sql`ファイルを確認することを強くお勧めします。ProxySQL 構成の詳細については、 [ProxySQL ドキュメント](https://proxysql.com/documentation/proxysql-configuration/)を参照してください。

    以下は、ProxySQL パターンがクエリ ルールと一致する方法に関する追加情報です。

    -   ProxySQL は、 `rule_id`の昇順でルールを 1 つずつ照合しようとします。
    -   `^`記号は SQL ステートメントの先頭に一致し、 `$`末尾に一致します。

    ProxySQL の正規表現とパターン マッチングの詳細については、ProxySQL ドキュメントの[mysql クエリプロセッサ正規表現](https://proxysql.com/documentation/global-variables/mysql-variables/#mysql-query_processor_regex)参照してください。

    パラメータの完全なリストについては、ProxySQL ドキュメントの[mysql_クエリルール](https://proxysql.com/documentation/main-runtime/#mysql_query_rules)参照してください。

6.  構成を確認し、クエリ ルールが機能するかどうかを確認します。

    1.  `root`のユーザーとして ProxySQL MySQL インターフェイスにログインします。

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

        -   取引を開始します:

            ```sql
            BEGIN;
            INSERT INTO test.tidb_server (server_name) VALUES ('insert this and rollback later');
            SELECT * FROM test.tidb_server;
            ROLLBACK;
            ```

            このトランザクションでは、 `BEGIN`ステートメントはどのルールにも一致しません。デフォルトのホストグループ (この例では`hostgroup 0` ) を使用します。ProxySQL はデフォルトでユーザー transaction_persistent を有効にし、同じホストグループ内の同じトランザクション内のすべてのステートメントを実行するため、 `INSERT`および`SELECT * FROM test.tidb_server;`ステートメントも TiDB クラスター`hostgroup 0`に転送されます。

        以下は出力例です。同様の出力が表示された場合、ProxySQL でクエリ ルールが正常に構成されています。

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

    3.  いつでも MySQL クライアントを終了するには、 `quit`入力して<kbd>Enter</kbd>キーを押します。

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
