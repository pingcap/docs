---
title: ProxySQL Integration Guide
summary: Learn how to integrate TiDB Cloud and TiDB (self-hosted) with ProxySQL.
---

# TiDB を ProxySQL と統合する {#integrate-tidb-with-proxysql}

このドキュメントでは、ProxySQL の概要を説明し、 [開発環境](#development-environment)および[本番環境](#production-environment)で ProxySQL を TiDB と統合する方法を説明し、 [クエリ ルーティングのシナリオ](#typical-scenario)を通じて主な統合の利点を示します。

TiDB と ProxySQL について詳しく知りたい場合は、次のような便利なリンクを見つけることができます。

-   [TiDB Cloud](https://docs.pingcap.com/tidbcloud)
-   [TiDB 開発者ガイド](/develop/dev-guide-overview.md)
-   [ProxySQL ドキュメント](https://proxysql.com/documentation/)

## ProxySQL とは何ですか? {#what-is-proxysql}

[プロキシSQL](https://proxysql.com/)は、高パフォーマンスのオープン ソース SQL プロキシです。柔軟なアーキテクチャを備えており、さまざまな方法で展開できるため、さまざまなユース ケースに最適です。たとえば、ProxySQL を使用して、頻繁にアクセスされるデータをキャッシュすることでパフォーマンスを向上させることができます。

ProxySQL は、高速で効率的で使いやすいようにゼロから設計されています。 MySQL と完全に互換性があり、高品質の SQL プロキシに期待されるすべての機能をサポートしています。さらに、ProxySQL には多数の独自の機能が備わっているため、幅広いアプリケーションにとって理想的な選択肢となります。

## ProxySQL 統合の理由 {#why-proxysql-integration}

-   ProxySQL は、TiDB とやり取りする際のレイテンシーを短縮することで、アプリケーションのパフォーマンスを向上させるのに役立ちます。何を構築しているかに関係なく、Lambda のようなサーバーレス関数を使用するスケーラブルなアプリケーションでワークロードが非決定的でスパイクする可能性があるか、大量のデータをロードするクエリを実行するアプリケーションを構築しているかに関係なく. [接続プーリング](https://proxysql.com/documentation/detailed-answers-on-faq/)や[頻繁に使用されるクエリのキャッシュ](https://proxysql.com/documentation/query-cache/)などの ProxySQL の強力な機能を活用することで、アプリケーションはすぐにメリットを得ることができます。
-   ProxySQL は、ProxySQL で使用できる構成が簡単な機能[クエリ ルール](#query-rules)を利用して、SQL インジェクションなどの SQL の脆弱性に対するアプリケーション セキュリティ保護の追加レイヤーとして機能できます。
-   [プロキシSQL](https://github.com/sysown/proxysql)と[TiDB](https://github.com/pingcap/tidb)はどちらもオープンソース プロジェクトであるため、ベンダー ロックインがゼロのメリットを得ることができます。

## 導入アーキテクチャ {#deployment-architecture}

ProxySQL を TiDB と共に展開する最も明白な方法は、ProxySQL をアプリケーションレイヤーと TiDB の間のスタンドアロンの仲介として追加することです。ただし、スケーラビリティと耐障害性は保証されておらず、ネットワーク ホップによるレイテンシーも追加されます。これらの問題を回避するための代替デプロイメントアーキテクチャは、以下のように ProxySQL をサイドカーとしてデプロイすることです。

![proxysql-client-side-tidb-cloud](/media/develop/proxysql-client-side-tidb-cloud.png)

> **ノート：**
>
> 前の図は参考用です。実際の展開アーキテクチャに応じて調整する必要があります。

## 開発環境 {#development-environment}

このセクションでは、開発環境で TiDB を ProxySQL と統合する方法について説明します。 ProxySQL 統合を開始するには、TiDB クラスターの種類に応じて、 [前提条件](#prerequisite)のいずれかのオプションを選択できます。

-   オプション 1: [TiDB CloudをProxySQL と統合する](#option-1-integrate-tidb-cloud-with-proxysql)
-   オプション 2: [TiDB (自己ホスト型) を ProxySQL と統合する](#option-2-integrate-tidb-self-hosted-with-proxysql)

### 前提条件 {#prerequisites}

選択したオプションによっては、次のパッケージが必要になる場合があります。

-   [ギット](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
-   [ドッカー](https://docs.docker.com/get-docker/)
-   [パイソン3](https://www.python.org/downloads/)
-   [Docker Compose](https://docs.docker.com/compose/install/linux/)
-   [MySQL クライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)

以下のインストール手順に従ってください。

<SimpleTab groupId="os">

<div label="macOS" value="macOS">

1.  [ダウンロード](https://docs.docker.com/get-docker/)を入力して Docker を起動します (Docker Desktop には既に Docker Compose が含まれています)。
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

    1.  [Git Windows ダウンロード](https://git-scm.com/download/win)ページから**64 ビット Git for Windows セットアップ**パッケージをダウンロードします。
    2.  セットアップ ウィザードに従って Git パッケージをインストールします。 **[次へ] を**数回クリックして、デフォルトのインストール設定を使用できます。

        ![proxysql-windows-git-install](/media/develop/proxysql-windows-git-install.png)

-   MySQL Shell をダウンロードしてインストールします。

    1.  [MySQL コミュニティ サーバーのダウンロード](https://dev.mysql.com/downloads/mysql/)ページから MySQL Installer の ZIP ファイルをダウンロードします。
    2.  ファイルを解凍し、 `bin`フォルダー内の`mysql.exe`を見つけます。 `bin`フォルダーのパスをシステム変数に追加し、Git Bash で`PATH`変数に設定する必要があります。

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

    1.  [ドッカーのダウンロード](https://www.docker.com/products/docker-desktop/)ページから Docker Desktop インストーラーをダウンロードします。
    2.  インストーラーをダブルクリックして実行します。インストールが完了すると、再起動を求めるプロンプトが表示されます。

        ![proxysql-windows-docker-install](/media/develop/proxysql-windows-docker-install.png)

-   [Python ダウンロード](https://www.python.org/downloads/)ページから最新の Python 3 インストーラーをダウンロードして実行します。

</div>

</SimpleTab>

### オプション 1: TiDB CloudをProxySQL と統合する {#option-1-integrate-tidb-cloud-with-proxysql}

この統合では、TiDB Serverless Tierクラスターと共に[ProxySQL Docker イメージ](https://hub.docker.com/r/proxysql/proxysql)を使用します。次の手順では、ポート`16033`で ProxySQL をセットアップするため、このポートが使用可能であることを確認してください。

#### ステップ 1. TiDB Cloud Serverless Tierクラスターを作成する {#step-1-create-a-tidb-cloud-serverless-tier-cluster}

1.  [無料の TiDB Serverless Tierクラスターを作成する](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart#step-1-create-a-tidb-cluster) .クラスターに設定した root パスワードを覚えておいてください。
2.  後で使用するために、クラスターのホスト名、ポート、およびユーザー名を取得します。

    1.  [クラスター](https://tidbcloud.com/console/clusters)ページで、クラスター名をクリックして、クラスターの概要ページに移動します。
    2.  クラスターの概要ページで、 **[接続]**ペインを見つけて、 `Endpoint` 、 `Port` 、および`User`フィールドをコピーします`Endpoint`はクラスターのホスト名です。

#### ステップ 2. ProxySQL 構成ファイルを生成する {#step-2-generate-proxysql-configuration-files}

1.  TiDB と ProxySQL の[統合サンプル コード リポジトリ](https://github.com/pingcap-inc/tidb-proxysql-integration)を複製します。

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

    ```
    [Begin] generating configuration files..
    tidb-cloud-connect.cnf generated successfully.
    proxysql-prepare.sql generated successfully.
    proxysql-connect.py generated successfully.
    [End] all files generated successfully and placed in the current folder.
    ```

#### 手順 3.ProxySQL を構成する {#step-3-configure-proxysql}

1.  ドッカーを起動します。 Docker がすでに起動している場合は、この手順をスキップします。

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

2.  ProxySQL イメージをプルし、ProxySQL コンテナーをバックグラウンドで開始します。

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

3.  次のコマンドを実行して、ProxySQL と統合します。このコマンドは、 **ProxySQL Admin Interface**内で`proxysql-prepare.sql`を実行します。

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

    > **ノート：**
    >
    > `proxysql-prepare.sql`スクリプトは次のことを行います。
    >
    > 1.  クラスターのユーザー名とパスワードを使用してユーザーを追加します。
    > 2.  ユーザーを監視アカウントに割り当てます。
    > 3.  ホストのリストに TiDBServerless Tierクラスターを追加します。
    > 4.  ProxySQL と TiDB Serverless Tierクラスター間の安全な接続を有効にします。
    >
    > よりよく理解するために、 `proxysql-prepare.sql`のファイルを確認することを強くお勧めします。 ProxySQL 構成の詳細については、 [ProxySQL ドキュメント](https://proxysql.com/documentation/proxysql-configuration/)を参照してください。

    以下は出力例です。クラスターのホスト名が出力に表示されていることがわかります。これは、ProxySQL と TiDB Serverless Tierクラスター間の接続が確立されていることを意味します。

    ```
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
    ```

#### ステップ 4.ProxySQL を介して TiDB クラスターに接続する {#step-4-connect-to-your-tidb-cluster-through-proxysql}

1.  TiDB クラスターに接続するには、 `proxysql-connect.py`を実行します。スクリプトは自動的に MySQL クライアントを起動し、 [ステップ2](#step-2-generate-proxysql-configuration-files)で指定したユーザー名とパスワードを使用して接続します。

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

2.  TiDB クラスターに接続したら、次の SQL ステートメントを使用して接続を検証できます。

    ```sql
    SELECT VERSION();
    ```

    TiDB のバージョンが表示されている場合は、ProxySQL を介して TiDB Serverless Tierクラスターに正常に接続されています。いつでも MySQL クライアントを終了するには、 `quit`入力して<kbd>Enter</kbd>を押します。

    > **ノート：**
    >
    > ***デバッグの場合:***クラスターに接続できない場合は、ファイル`tidb-cloud-connect.cnf` 、 `proxysql-prepare.sql` 、および`proxysql-connect.py`を確認してください。指定したサーバー情報が使用可能であり、正しいことを確認してください。

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

### オプション 2: TiDB (自己ホスト型) を ProxySQL と統合する {#option-2-integrate-tidb-self-hosted-with-proxysql}

この統合では、 [TiDB](https://hub.docker.com/r/pingcap/tidb)と[プロキシSQL](https://hub.docker.com/r/proxysql/proxysql)の Docker イメージを使用して環境をセットアップします。ご自身の興味に合わせて[TiDB をインストールする他の方法 (自己ホスト型)](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb)を試してみることをお勧めします。

次の手順では、ポート`6033`と`4000`にそれぞれ ProxySQL と TiDB をセットアップするため、これらのポートが使用可能であることを確認してください。

1.  ドッカーを起動します。 Docker がすでに起動している場合は、この手順をスキップします。

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

2.  TiDB と ProxySQL の[統合サンプル コード リポジトリ](https://github.com/pingcap-inc/tidb-proxysql-integration)を複製します。

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

3.  ProxySQL と TiDB の最新のイメージをプルします。

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

4.  TiDB と ProxySQL の両方をコンテナーとして実行する統合環境を開始します。

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

    ProxySQL `6033`ポートにログインするには、ユーザー名`root`と空のパスワードを使用できます。

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

6.  TiDB クラスターに接続したら、次の SQL ステートメントを使用して接続を検証できます。

    ```sql
    SELECT VERSION();
    ```

    TiDB のバージョンが表示されている場合は、ProxySQL を介して TiDB コンテナーに正常に接続されています。

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

本番環境では、フル マネージド エクスペリエンスのために[TiDB Cloud](https://en.pingcap.com/tidb-cloud/)直接使用することをお勧めします。

### 前提条件 {#prerequisite}

MySQL クライアントをダウンロードしてインストールします。たとえば、 [MySQL シェル](https://dev.mysql.com/downloads/shell/)です。

### TiDB Cloudを CentOS 上の ProxySQL と統合する {#integrate-tidb-cloud-with-proxysql-on-centos}

ProxySQL は、さまざまなプラットフォームにインストールできます。以下は、CentOS を例に取っています。

サポートされているプラットフォームと対応するバージョン要件の完全なリストについては、 [ProxySQL ドキュメント](https://proxysql.com/documentation/installing-proxysql/)を参照してください。

#### ステップ 1.TiDB TiDB Cloud Dedicated Tierクラスターを作成する {#step-1-create-a-tidb-cloud-dedicated-tier-cluster}

詳細な手順については、 [TiDBクラスタを作成する](https://docs.pingcap.com/tidbcloud/create-tidb-cluster)を参照してください。

#### ステップ 2.ProxySQL をインストールする {#step-2-install-proxysql}

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

ProxySQL のサポートされているプラットフォームとそのインストールの詳細については、 [ProxySQL README](https://github.com/sysown/proxysql#installation)または[ProxySQL インストール ドキュメント](https://proxysql.com/documentation/installing-proxysql/)を参照してください。

#### 手順 3.ProxySQL を構成する {#step-3-configure-proxysql}

ProxySQL を TiDB のプロキシとして使用するには、ProxySQL を構成する必要があります。これを行うには、 [ProxySQL 管理インターフェイス内で SQL ステートメントを実行する](#option-1-configure-proxysql-using-the-admin-interface) (推奨) または[構成ファイル](#option-2-configure-proxysql-using-a-configuration-file)を使用できます。

> **ノート：**
>
> 次のセクションでは、ProxySQL の必須構成項目のみをリストします。構成の包括的なリストについては、 [ProxySQL ドキュメント](https://proxysql.com/documentation/proxysql-configuration/)を参照してください。

##### オプション 1: 管理インターフェイスを使用して ProxySQL を構成する {#option-1-configure-proxysql-using-the-admin-interface}

1.  標準の ProxySQL 管理インターフェイスを使用して ProxySQL の内部を再構成します。このインターフェイスは、任意の MySQL コマンド ライン クライアントからアクセスできます (ポート`6032`でデフォルトで利用可能)。

    ```bash
    mysql -u admin -padmin -h 127.0.0.1 -P6032 --prompt 'ProxySQL Admin> '
    ```

    上記の手順により、ProxySQL 管理プロンプトが表示されます。

2.  使用する TiDB クラスターを構成します。ここで、1 つまたは複数の TiDB クラスターを ProxySQL に追加できます。次のステートメントは、たとえば、1 つのTiDB Cloud Dedicated Tierクラスターを追加します。 `<tidb cloud dedicated cluster host>`と`<tidb cloud dedicated cluster port>` TiDB Cloudエンドポイントとポート (デフォルトのポートは`4000` ) に置き換える必要があります。

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

    > **ノート：**
    >
    > -   `hostgroup_id` : ホストグループの ID を指定します。 ProxySQL は、ホストグループを使用してクラスターを管理します。これらのクラスターに SQL トラフィックを均等に分散するために、負荷分散が必要な複数のクラスターを同じホストグループに構成できます。読み取り目的や書き込み目的などでクラスターを区別するために、異なるホストグループを使用するようにクラスターを構成できます。
    > -   `hostname` : TiDB クラスターのエンドポイント。
    > -   `port` : TiDB クラスターのポート。

3.  プロキシ ログイン ユーザーを構成して、ユーザーが TiDB クラスターに対する適切なアクセス許可を持っていることを確認します。次のステートメントでは、「 *tidb cloud dedicated cluster username* 」と「 <em>tidb cloud dedicated cluster password</em> 」をクラスターの実際のユーザー名とパスワードに置き換える必要があります。

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

    > **ノート：**
    >
    > -   `username` : TiDB ユーザー名。
    > -   `password` : TiDB パスワード。
    > -   `active` : ユーザーがアクティブかどうかを制御します。 `1`ユーザーが**アクティブで**ログインに使用できることを示し、 `0`ユーザーが非アクティブであることを示します。
    > -   `default_hostgroup` : ユーザーが使用するデフォルトのホストグループ。クエリ ルールが特定のホストグループへのトラフィックをオーバーライドしない限り、SQL トラフィックが分散されます。
    > -   `transaction_persistent` : `1`永続的なトランザクションを示します。ユーザーが接続内でトランザクションを開始すると、トランザクションがコミットまたはロールバックされるまで、すべてのクエリ ステートメントが同じホストグループにルーティングされます。

##### オプション 2: 構成ファイルを使用して ProxySQL を構成する {#option-2-configure-proxysql-using-a-configuration-file}

このオプションは、ProxySQL を構成するための代替方法としてのみ考慮してください。詳細については、 [構成ファイルによる ProxySQL の構成](https://github.com/sysown/proxysql#configuring-proxysql-through-the-config-file)を参照してください。

1.  既存の SQLite データベース (構成が内部に保存されている場所) を削除します。

    ```bash
    rm /var/lib/proxysql/proxysql.db
    ```

    > **警告：**
    >
    > SQLite データベース ファイルを削除すると、ProxySQL 管理インターフェイスを使用して行った構成の変更はすべて失われます。

2.  必要に応じて構成ファイル`/etc/proxysql.cnf`を変更します。例えば：

    ```
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
    ```

    前の例では:

    -   `address`および`port` : TiDB Cloudクラスターのエンドポイントとポートを指定します。
    -   `username`と`password` : TiDB Cloudクラスターのユーザー名とパスワードを指定します。

3.  ProxySQL を再起動します。

    ```bash
    systemctl restart proxysql
    ```

    再起動後、SQLite データベースが自動的に作成されます。

> **警告：**
>
> 本番でデフォルトの認証情報を使用して ProxySQL を実行しないでください。 `proxysql`サービスを開始する前に、 `admin_credentials`変数を変更して`/etc/proxysql.cnf`ファイルのデフォルトを変更できます。

## 典型的なシナリオ {#typical-scenario}

このセクションでは、クエリ ルーティングを例として取り上げ、ProxySQL と TiDB を統合することで利用できる利点のいくつかを示します。

### クエリ ルール {#query-rules}

データベースは、高トラフィック、欠陥のあるコード、または悪意のあるスパムによって過負荷になる可能性があります。 ProxySQL のクエリ ルールを使用すると、クエリを再ルーティング、書き換え、または拒否することで、これらの問題に迅速かつ効果的に対応できます。

![proxysql-client-side-rules](/media/develop/proxysql-client-side-rules.png)

> **ノート：**
>
> 次の手順では、TiDB と ProxySQL のコンテナー イメージを使用して、クエリ ルールを構成します。それらをプルしていない場合は、詳細な手順について[統合セクション](#option-2-integrate-tidb-self-hosted-with-proxysql)を確認できます。

1.  TiDB と ProxySQL の[統合サンプル コード リポジトリ](https://github.com/pingcap-inc/tidb-proxysql-integration)を複製します。前の手順ですでにクローンを作成している場合は、この手順をスキップしてください。

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

3.  次のコマンドを実行して、2 つの TiDB コンテナーと 1 つの ProxySQL コンテナーを開始します。

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

    すべてがうまくいけば、次のコンテナーが開始されます。

    -   ポート`4001` 、 `4002`を介して公開される TiDB クラスターの 2 つの Docker コンテナー
    -   ポート`6034`経由で公開される 1 つの ProxySQL Docker コンテナー。

4.  2 つの TiDB コンテナーで、 `mysql`を使用して同様のスキーマ定義を持つテーブルを作成し、異なるデータ ( `'tidb-server01-port-4001'` 、 `'tidb-server02-port-4002'` ) を挿入してこれらのコンテナーを識別します。

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

5.  次のコマンドを実行して ProxySQL を構成します。このコマンドは、ProxySQL 管理インターフェイス内で`proxysql-prepare.sql`実行し、TiDB コンテナーと ProxySQL 間のプロキシ接続を確立します。

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

    > **ノート：**
    >
    > `proxysql-prepare.sql`は次のことを行います。
    >
    > -   `hostgroup_id`を`0`および`1`として ProxySQL に TiDB クラスターを追加します。
    > -   空のパスワードでユーザー`root`を追加し、 `default_hostgroup`を`0`に設定します。
    > -   `rule_id`を`1`として、 `destination_hostgroup` `0`として、ルール`^SELECT.*FOR UPDATE$`を追加します。 SQL ステートメントがこのルールに一致する場合、リクエストは`hostgroup`を`0`として TiDB クラスターに転送されます。
    > -   `rule_id`を`2`として、 `destination_hostgroup` `1`として、ルール`^SELECT`を追加します。 SQL ステートメントがこのルールに一致する場合、リクエストは`hostgroup`を`1`として TiDB クラスターに転送されます。
    >
    > よりよく理解するために、 `proxysql-prepare.sql`のファイルを確認することを強くお勧めします。 ProxySQL 構成の詳細については、 [ProxySQL ドキュメント](https://proxysql.com/documentation/proxysql-configuration/)を参照してください。

    以下は、ProxySQL パターンがクエリ ルールに一致する方法に関する追加情報です。

    -   ProxySQL は、ルールを`rule_id`の昇順で 1 つずつ照合しようとします。
    -   `^`記号は SQL ステートメントの先頭に一致し、 `$`末尾に一致します。

    ProxySQL の正規表現とパターン マッチングの詳細については、ProxySQL ドキュメントの[mysql-query_processor_regex](https://proxysql.com/documentation/global-variables/mysql-variables/#mysql-query_processor_regex)を参照してください。

    パラメータの完全なリストについては、ProxySQL ドキュメントの[mysql_query_rules](https://proxysql.com/documentation/main-runtime/#mysql_query_rules)を参照してください。

6.  構成を確認し、クエリ ルールが機能するかどうかを確認します。

    1.  `root`人のユーザーとして ProxySQL MySQL Interface にログインします。

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

            このステートメントは rule_id `2`に一致し、ステートメントを`hostgroup 1`の TiDB クラスターに転送します。

        -   `SELECT ... FOR UPDATE`ステートメントを実行します。

            ```sql
            SELECT * FROM test.tidb_server FOR UPDATE;
            ```

            このステートメントは rule_id `1`に一致し、ステートメントを`hostgroup 0`の TiDB クラスターに転送します。

        -   トランザクションを開始します。

            ```sql
            BEGIN;
            INSERT INTO test.tidb_server (server_name) VALUES ('insert this and rollback later');
            SELECT * FROM test.tidb_server;
            ROLLBACK;
            ```

            このトランザクションでは、 `BEGIN`ステートメントはどのルールにも一致しません。デフォルトのホストグループ (この例では`hostgroup 0` ) を使用します。 ProxySQL はデフォルトでユーザー transaction_persistent を有効にし、同じホストグループ内の同じトランザクション内のすべてのステートメントを実行するため、 `INSERT`と`SELECT * FROM test.tidb_server;`ステートメントも TiDB クラスター`hostgroup 0`に転送されます。

        以下は出力例です。同様の出力が得られた場合、ProxySQL でクエリ ルールが正常に構成されています。

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

    3.  いつでも MySQL クライアントを終了するには、 `quit`入力して<kbd>Enter</kbd>を押します。

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
