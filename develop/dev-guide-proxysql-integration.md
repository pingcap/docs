---
title: ProxySQL Integration Guide
summary: TiDB Cloudと TiDB (セルフホスト) を ProxySQL と統合する方法を学びます。
---

# TiDBとProxySQLを統合する {#integrate-tidb-with-proxysql}

このドキュメントでは、ProxySQL の概要を説明し、 [開発環境](#development-environment)および[本番環境](#production-environment)で ProxySQL を TiDB と統合する方法を説明し、 [クエリルーティングのシナリオ](#typical-scenario)を通じて主要な統合の利点を示します。

TiDB と ProxySQL についてさらに詳しく知りたい場合は、次のような役立つリンクがあります。

-   [TiDB Cloud](https://docs.pingcap.com/tidbcloud)
-   [TiDB 開発者ガイド](/develop/dev-guide-overview.md)
-   [ProxySQL ドキュメント](https://proxysql.com/documentation/)

## ProxySQL とは何ですか? {#what-is-proxysql}

[プロキシSQL](https://proxysql.com/)は、高性能なオープンソースSQLプロキシです。柔軟なアーキテクチャを備え、様々な方法で導入できるため、様々なユースケースに最適です。例えば、ProxySQLは、頻繁にアクセスされるデータをキャッシュすることでパフォーマンスを向上させることができます。

ProxySQLは、高速、効率的、そして使いやすさを念頭に設計されています。MySQLとの完全な互換性を備え、高品質なSQLプロキシに期待されるすべての機能を備えています。さらに、ProxySQLには独自の機能が多数搭載されており、幅広いアプリケーションに最適な選択肢となります。

## ProxySQL 統合の理由は何ですか? {#why-proxysql-integration}

-   ProxySQLは、TiDBとのやり取りにおけるレイテンシーを削減することで、アプリケーションのパフォーマンス向上に役立ちます。Lambdaなどのサーバーレス関数を使用したスケーラブルなアプリケーション（ワークロードが非決定的で急増する可能性がある）を構築する場合でも、大量[接続プール](https://proxysql.com/documentation/detailed-answers-on-faq/)データを読み込むクエリを実行するアプリケーションを構築する場合でも、構築するものは問いません。1や[頻繁に使用されるクエリのキャッシュ](https://proxysql.com/documentation/query-cache/)などのProxySQLの強力な機能を活用することで、アプリケーションはすぐにメリットを得ることができます。
-   ProxySQL は、ProxySQL で利用できる簡単に構成できる機能である[クエリルール](#query-rules)の助けを借りて、SQL インジェクションなどの SQL の脆弱性に対するアプリケーション セキュリティ保護の追加レイヤーとして機能します。
-   [プロキシSQL](https://github.com/sysown/proxysql)と[TiDB](https://github.com/pingcap/tidb)どちらもオープンソース プロジェクトであるため、ベンダー ロックインがないというメリットが得られます。

## デプロイメントアーキテクチャ {#deployment-architecture}

TiDBとProxySQLを併用する最も分かりやすい方法は、アプリケーションレイヤーとTiDBの間にProxySQLをスタンドアロンの仲介者として追加することです。しかし、スケーラビリティと耐障害性は保証されず、ネットワークホップによるレイテンシーも増加します。これらの問題を回避するための代替アーキテクチャとして、以下のようにProxySQLをサイドカーとして導入する方法があります。

![proxysql-client-side-tidb-cloud](/media/develop/proxysql-client-side-tidb-cloud.png)

> **注記：**
>
> 上記の図は参考用です。実際のデプロイメントアーキテクチャに合わせて調整する必要があります。

## 開発環境 {#development-environment}

このセクションでは、開発環境でTiDBとProxySQLを統合する方法について説明します。ProxySQLとの統合を開始するには、 [前提条件](#prerequisite)のすべての準備が完了したら、TiDBクラスタの種類に応じて以下のいずれかのオプションを選択してください。

-   オプション1: [TiDB Cloudと ProxySQL を統合する](#option-1-integrate-tidb-cloud-with-proxysql)
-   オプション2: [TiDB（セルフホスト）をProxySQLと統合する](#option-2-integrate-tidb-self-hosted-with-proxysql)

### 前提条件 {#prerequisites}

選択したオプションに応じて、次のパッケージが必要になる場合があります。

-   [ギット](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
-   [ドッカー](https://docs.docker.com/get-docker/)
-   [Python 3](https://www.python.org/downloads/)
-   [Dockerコンポーズ](https://docs.docker.com/compose/install/linux/)
-   [MySQLクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)

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
    2.  セットアップウィザードに従ってGitパッケージをインストールします。デフォルトのインストール設定を使用する場合は、 **「次へ」**を数回クリックします。

        ![proxysql-windows-git-install](/media/develop/proxysql-windows-git-install.png)

-   MySQL Shell をダウンロードしてインストールします。

    1.  [MySQLコミュニティサーバーのダウンロード](https://dev.mysql.com/downloads/mysql/)ページ目からMySQLインストーラーのZIPファイルをダウンロードします。
    2.  ファイルを解凍し、 `bin`フォルダ内の`mysql.exe`見つけます。5 フォルダ`bin`パスをシステム変数に追加し、Git Bash の`PATH`変数に設定します。

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

### オプション1: TiDB CloudとProxySQLを統合する {#option-1-integrate-tidb-cloud-with-proxysql}

この統合では、 [ProxySQL Docker イメージ](https://hub.docker.com/r/proxysql/proxysql)とTiDB Cloud Serverless クラスターを使用します。以下の手順ではポート`16033`に ProxySQL を設定するため、このポートが使用可能であることを確認してください。

#### ステップ1. TiDB Cloud Serverlessクラスターを作成する {#step-1-create-a-tidb-cloud-serverless-cluster}

1.  [無料のTiDB Cloud Serverlessクラスターを作成する](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart#step-1-create-a-tidb-cluster) 。クラスターに設定したルートパスワードを覚えておいてください。
2.  後で使用するために、クラスターのホスト名、ポート、およびユーザー名を取得します。

    1.  [クラスター](https://tidbcloud.com/project/clusters)ページで、クラスター名をクリックしてクラスターの概要ページに移動します。
    2.  クラスターの概要ページで、 **[接続]**ペインを見つけて、 `Endpoint` 、 `Port` 、 `User`フィールドをコピーします。ここで、 `Endpoint`クラスターのホスト名です。

#### ステップ2. ProxySQL構成ファイルを生成する {#step-2-generate-proxysql-configuration-files}

1.  TiDB および ProxySQL の[統合サンプルコードリポジトリ](https://github.com/pingcap-inc/tidb-proxysql-integration)クローンします。

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

    プロンプトが表示されたら、クラスターのエンドポイントを`Serverless Tier Host`に入力し、クラスターのユーザー名とパスワードを入力します。

    以下は出力例です。現在のフォルダ`tidb-cloud-connect`の下に 3 つの設定ファイルが生成されていることがわかります。

        [Begin] generating configuration files..
        tidb-cloud-connect.cnf generated successfully.
        proxysql-prepare.sql generated successfully.
        proxysql-connect.py generated successfully.
        [End] all files generated successfully and placed in the current folder.

#### ステップ3. ProxySQLを構成する {#step-3-configure-proxysql}

1.  Dockerを起動します。Dockerがすでに起動している場合は、この手順をスキップしてください。

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

3.  **ProxySQL 管理インターフェース**内で`proxysql-prepare.sql`実行する次のコマンドを実行して、ProxySQL と統合します。

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
    > 3.  TiDB Cloud Serverless クラスターをホストのリストに追加します。
    > 4.  ProxySQL とTiDB Cloud Serverless クラスター間の安全な接続を有効にします。
    >
    > より深く理解するために、 `proxysql-prepare.sql`ファイルを確認することを強くお勧めします。ProxySQL の設定の詳細については、 [ProxySQL ドキュメント](https://proxysql.com/documentation/proxysql-configuration/)参照してください。

    以下は出力例です。出力にクラスターのホスト名が表示されています。これは、ProxySQL とTiDB Cloud Serverless クラスター間の接続が確立されていることを意味します。

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

    TiDBのバージョンが表示されていれば、ProxySQL経由でTiDB Cloud Serverlessクラスターに正常に接続されています。MySQLクライアントを終了するには、 `quit`入力して<kbd>Enterキー</kbd>を押してください。

    > **注記：**
    >
    > ***デバッグ用：***クラスターに接続できない場合は、ファイル`tidb-cloud-connect.cnf` 、 `proxysql-prepare.sql` 、 `proxysql-connect.py`を確認してください。指定したサーバー情報が利用可能であり、正しいことを確認してください。

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

### オプション2: TiDB（セルフホスト）をProxySQLと統合する {#option-2-integrate-tidb-self-hosted-with-proxysql}

この統合では、 [TiDB](https://hub.docker.com/r/pingcap/tidb)と[プロキシSQL](https://hub.docker.com/r/proxysql/proxysql)のDockerイメージを使用して環境を構築します。興味があれば、 [TiDB をインストールする他の方法 (セルフホスト)](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb)試してみることをお勧めします。

次の手順では、それぞれポート`6033`と`4000`に ProxySQL と TiDB を設定するので、これらのポートが使用可能であることを確認してください。

1.  Dockerを起動します。Dockerがすでに起動している場合は、この手順をスキップしてください。

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

2.  TiDB および ProxySQL の[統合サンプルコードリポジトリ](https://github.com/pingcap-inc/tidb-proxysql-integration)クローンします。

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

## 生産環境 {#production-environment}

本番環境では、完全に管理されたエクスペリエンスを実現するために[TiDB Cloud専用](https://www.pingcap.com/tidb-cloud-dedicated/)直接使用することをお勧めします。

### 前提条件 {#prerequisite}

MySQLクライアントをダウンロードしてインストールします。例： [MySQLシェル](https://dev.mysql.com/downloads/shell/) 。

### CentOS でTiDB Cloudと ProxySQL を統合する {#integrate-tidb-cloud-with-proxysql-on-centos}

ProxySQLは様々なプラットフォームにインストールできます。以下ではCentOSを例に説明します。

サポートされているプラットフォームと対応するバージョン要件の完全なリストについては、 [ProxySQLドキュメント](https://proxysql.com/documentation/installing-proxysql/)参照してください。

#### ステップ1. TiDB Cloud専用クラスターを作成する {#step-1-create-a-tidb-cloud-dedicated-cluster}

詳細な手順については、 [TiDBクラスタを作成する](https://docs.pingcap.com/tidbcloud/create-tidb-cluster)参照してください。

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

3.  ProxySQLを起動します。

    ```bash
    systemctl start proxysql
    ```

ProxySQL がサポートするプラットフォームとそのインストールの詳細については、 [ProxySQL README](https://github.com/sysown/proxysql#installation)または[ProxySQL インストールドキュメント](https://proxysql.com/documentation/installing-proxysql/)参照してください。

#### ステップ3. ProxySQLを構成する {#step-3-configure-proxysql}

ProxySQLをTiDBのプロキシとして使用するには、ProxySQLを設定する必要があります。設定には、 [ProxySQL管理インターフェース内でSQL文を実行する](#option-1-configure-proxysql-using-the-admin-interface) （推奨）または[設定ファイル](#option-2-configure-proxysql-using-a-configuration-file)のいずれかを使用できます。

> **注記：**
>
> 以下のセクションでは、ProxySQL の必須設定項目のみを記載しています。設定項目の包括的なリストについては、 [ProxySQLドキュメント](https://proxysql.com/documentation/proxysql-configuration/)参照してください。

##### オプション 1: 管理インターフェースを使用して ProxySQL を構成する {#option-1-configure-proxysql-using-the-admin-interface}

1.  任意の MySQL コマンドライン クライアント (デフォルトではポート`6032`で使用可能) からアクセスできる標準の ProxySQL 管理インターフェイスを使用して、ProxySQL の内部を再構成します。

    ```bash
    mysql -u admin -padmin -h 127.0.0.1 -P6032 --prompt 'ProxySQL Admin> '
    ```

    上記の手順を実行すると、ProxySQL 管理者プロンプトが表示されます。

2.  使用するTiDBクラスターを設定します。ProxySQLに1つまたは複数のTiDBクラスターを追加できます。以下の文は、例えば1つのTiDB Cloud Dedicatedクラスターを追加します。1と`<tidb cloud dedicated cluster port>` `<tidb cloud dedicated cluster host>` TiDB Cloudのエンドポイントとポート番号（デフォルトは`4000` ）に置き換えてください。

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
    > -   `hostgroup_id` : ホストグループのIDを指定します。ProxySQLはホストグループを使用してクラスターを管理します。これらのクラスターへのSQLトラフィックを均等に分散するには、負荷分散が必要な複数のクラスターを同じホストグループに設定できます。読み取りと書き込みなど、クラスターを区別するために、異なるホストグループを使用するように設定することもできます。
    > -   `hostname` : TiDB クラスターのエンドポイント。
    > -   `port` : TiDB クラスターのポート。

3.  プロキシログインユーザーを設定し、ユーザーがTiDBクラスタに対して適切な権限を持っていることを確認してください。以下の文で、「 *tidb cloud dedicated cluster username* 」と「 *tidb cloud dedicated cluster password* 」を、実際のクラスタのユーザー名とパスワードに置き換えてください。

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
    > -   `active` : ユーザーがアクティブかどうかを制御します。2 `1`ユーザーが**アクティブ**でありログインに使用できることを示し、 `0`ユーザーが非アクティブであることを示します。
    > -   `default_hostgroup` : ユーザーが使用するデフォルトのホストグループ。クエリ ルールによって特定のホストグループへのトラフィックがオーバーライドされない限り、SQL トラフィックが分散されます。
    > -   `transaction_persistent` : `1`永続的なトランザクションを示します。ユーザーが接続内でトランザクションを開始すると、トランザクションがコミットまたはロールバックされるまで、すべてのクエリステートメントは同じホストグループにルーティングされます。

##### オプション2: 構成ファイルを使用してProxySQLを構成する {#option-2-configure-proxysql-using-a-configuration-file}

このオプションは、ProxySQLを設定するための代替方法としてのみご検討ください。詳細については、 [設定ファイルによるProxySQLの設定](https://github.com/sysown/proxysql#configuring-proxysql-through-the-config-file)参照してください。

1.  既存の SQLite データベース (構成が内部的に保存されている場所) を削除します。

    ```bash
    rm /var/lib/proxysql/proxysql.db
    ```

    > **警告：**
    >
    > SQLite データベース ファイルを削除すると、ProxySQL 管理インターフェイスを使用して行われた構成の変更はすべて失われます。

2.  必要に応じて設定ファイル`/etc/proxysql.cnf`を変更します。例：

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

    上記の例では、次のようになります。

    -   `address`と`port` : TiDB Cloudクラスターのエンドポイントとポートを指定します。
    -   `username`と`password` : TiDB Cloudクラスターのユーザー名とパスワードを指定します。

3.  ProxySQLを再起動します。

    ```bash
    systemctl restart proxysql
    ```

    再起動後、SQLite データベースが自動的に作成されます。

> **警告：**
>
> 本番本番では、デフォルトの認証情報でProxySQLを実行しないでください。1 サービスを開始する前に、 `proxysql`ファイル`/etc/proxysql.cnf` `admin_credentials`変数を変更することで、デフォルトを変更できます。

## 典型的なシナリオ {#typical-scenario}

このセクションでは、クエリ ルーティングを例に、ProxySQL と TiDB を統合することで得られる利点のいくつかを示します。

### クエリルール {#query-rules}

データベースは、大量のトラフィック、コードの不具合、悪意のあるスパムなどによって過負荷になる可能性があります。ProxySQLのクエリルールを使用すれば、クエリのルーティング、書き換え、または拒否を行うことで、これらの問題に迅速かつ効果的に対応できます。

![proxysql-client-side-rules](/media/develop/proxysql-client-side-rules.png)

> **注記：**
>
> 次の手順では、TiDBとProxySQLのコンテナイメージを使用してクエリルールを設定します。まだプルしていない場合は、詳細な手順については[統合セクション](#option-2-integrate-tidb-self-hosted-with-proxysql)ご覧ください。

1.  TiDBとProxySQL用の[統合サンプルコードリポジトリ](https://github.com/pingcap-inc/tidb-proxysql-integration)クローンします。前の手順で既にクローンしている場合は、この手順をスキップしてください。

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

4.  2 つの TiDB コンテナで、 `mysql`使用して同様のスキーマ定義を持つテーブルを作成し、 `'tidb-server02-port-4002'`データ ( `'tidb-server01-port-4001'` ) を挿入してこれらのコンテナを識別します。

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
    > `proxysql-prepare.sql`は次のことを行います。
    >
    > -   `hostgroup_id`の ProxySQL に TiDB クラスターを`0`および`1`として追加します。
    > -   空のパスワードを持つユーザー`root`追加し、 `default_hostgroup`を`0`に設定します。
    > -   ルール`^SELECT.*FOR UPDATE$`に、 `rule_id`を`1` 、 `destination_hostgroup`を`0`として追加します。SQL文がこのルールに一致する場合、リクエストは`hostgroup`を`0`としてTiDBクラスターに転送されます。
    > -   ルール`^SELECT`に、 `rule_id`を`2` 、 `destination_hostgroup`を`1`として追加します。SQL文がこのルールに一致する場合、リクエストは`hostgroup`を`1`としてTiDBクラスターに転送されます。
    >
    > より深く理解するために、 `proxysql-prepare.sql`ファイルを確認することを強くお勧めします。ProxySQL の設定の詳細については、 [ProxySQLドキュメント](https://proxysql.com/documentation/proxysql-configuration/)参照してください。

    以下は、ProxySQL パターンがクエリ ルールと一致する方法に関する追加情報です。

    -   ProxySQL は、 `rule_id`の昇順でルールを 1 つずつ照合しようとします。
    -   `^`記号は SQL ステートメントの先頭に一致し、 `$`末尾に一致します。

    ProxySQL の正規表現とパターン マッチングの詳細については、ProxySQL ドキュメントの[mysql-クエリプロセッサ正規表現](https://proxysql.com/documentation/global-variables/mysql-variables/#mysql-query_processor_regex)参照してください。

    パラメータの完全なリストについては、ProxySQL ドキュメントの[mysql_クエリルール](https://proxysql.com/documentation/main-runtime/#mysql_query_rules)参照してください。

6.  構成を確認し、クエリ ルールが機能するかどうかを確認します。

    1.  `root`ユーザーとして ProxySQL MySQL インターフェースにログインします。

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

            このトランザクションでは、 `BEGIN`ステートメントはどのルールにも一致しません。デフォルトのホストグループ（この例では`hostgroup 0` ）を使用します。ProxySQLはデフォルトでユーザーtransaction_persistentを有効にし、同じトランザクション内のすべてのステートメントを同じホストグループで実行するので、 `INSERT`と`SELECT * FROM test.tidb_server;`ステートメントもTiDBクラスター`hostgroup 0`に転送されます。

        以下は出力例です。同様の出力が表示されれば、ProxySQLでクエリルールが正常に設定されています。

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

    3.  いつでも MySQL クライアントを終了するには、 `quit`入力して<kbd>Enter キー</kbd>を押します。

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

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>
