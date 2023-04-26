---
title: Deploy a TiDB Cluster Using TiUP
summary: Learn how to easily deploy a TiDB cluster using TiUP.
---

# TiUPを使用して TiDBクラスタをデプロイ {#deploy-a-tidb-cluster-using-tiup}

[TiUP](https://github.com/pingcap/tiup)は、TiDB 4.0 で導入されたクラスター運用保守ツールです。 TiUP は、 Golangで記述されたクラスター管理コンポーネントである[TiUPクラスター](https://github.com/pingcap/tiup/tree/master/components/cluster)提供します。 TiUPクラスターを使用すると、TiDB クラスターのデプロイ、開始、停止、破棄、スケーリング、およびアップグレードを含む日常のデータベース操作を簡単に実行し、TiDB クラスターのパラメーターを管理できます。

TiUP は、TiDB、 TiFlash、TiDB Binlog、TiCDC、および監視システムの展開をサポートしています。このドキュメントでは、さまざまなトポロジの TiDB クラスターをデプロイする方法を紹介します。

## ステップ 1. 前提条件と事前チェック {#step-1-prerequisites-and-precheck}

次のドキュメントを読んだことを確認してください。

-   [ハードウェアとソフトウェアの要件](/hardware-and-software-requirements.md)
-   [環境とシステム構成の確認](/check-before-deployment.md)

## ステップ 2. 制御マシンにTiUPをデプロイ {#step-2-deploy-tiup-on-the-control-machine}

コントロール マシンにTiUP を展開するには、オンライン展開とオフライン展開の 2 つの方法があります。

### TiUPをオンラインでデプロイ {#deploy-tiup-online}

通常のユーザー アカウントを使用して制御マシンにログインします (例として`tidb`ユーザーを取り上げます)。以降のTiUP のインストールとクラスター管理は`tidb`ユーザーで実行できます。

1.  次のコマンドを実行してTiUPをインストールします。

    {{< copyable "" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2.  TiUP環境変数を設定します。

    1.  グローバル環境変数を再宣言します。

        {{< copyable "" >}}

        ```shell
        source .bash_profile
        ```

    2.  TiUPがインストールされているかどうかを確認します。

        {{< copyable "" >}}

        ```shell
        which tiup
        ```

3.  TiUPクラスターコンポーネントをインストールします。

    {{< copyable "" >}}

    ```shell
    tiup cluster
    ```

4.  TiUPが既にインストールされている場合は、 TiUPクラスターコンポーネントを最新バージョンに更新します。

    {{< copyable "" >}}

    ```shell
    tiup update --self && tiup update cluster
    ```

    `Update successfully!`が表示されれば、 TiUPクラスターは正常に更新されています。

5.  TiUPクラスターの現在のバージョンを確認します。

    {{< copyable "" >}}

    ```shell
    tiup --binary cluster
    ```

### TiUP をオフラインでデプロイ {#deploy-tiup-offline}

TiUPを使用して TiDB クラスターをオフラインでデプロイするには、このセクションの次の手順を実行します。

#### TiUPオフラインコンポーネントパッケージを準備する {#prepare-the-tiup-offline-component-package}

方法 1: [公式ダウンロードページ](https://www.pingcap.com/download/)で、対象の TiDB バージョンのオフライン ミラー パッケージ (TiUPオフライン パッケージが含まれる) を選択します。サーバーパッケージとツールキット パッケージを同時にダウンロードする必要があることに注意してください。

方法 2: `tiup mirror clone`を使用してオフラインコンポーネントパッケージを手動でパックします。詳細な手順は次のとおりです。

1.  TiUPパッケージ マネージャーをオンラインでインストールします。

    1.  TiUPツールをインストールします。

        {{< copyable "" >}}

        ```shell
        curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
        ```

    2.  グローバル環境変数を再宣言します。

        {{< copyable "" >}}

        ```shell
        source .bash_profile
        ```

    3.  TiUPがインストールされているかどうかを確認します。

        {{< copyable "" >}}

        ```shell
        which tiup
        ```

2.  TiUPを使用してミラーを引き出します。

    1.  インターネットにアクセスできるマシンで必要なコンポーネントをプルします。

        {{< copyable "" >}}

        ```shell
        tiup mirror clone tidb-community-server-${version}-linux-amd64 ${version} --os=linux --arch=amd64
        ```

        上記のコマンドは、現在のディレクトリに`tidb-community-server-${version}-linux-amd64`という名前のディレクトリを作成します。このディレクトリには、クラスターの起動に必要なコンポーネントパッケージが含まれています。

    2.  `tar`コマンドを使用してコンポーネントパッケージをパックし、隔離された環境のコントロール マシンにパッケージを送信します。

        {{< copyable "" >}}

        ```bash
        tar czvf tidb-community-server-${version}-linux-amd64.tar.gz tidb-community-server-${version}-linux-amd64
        ```

        `tidb-community-server-${version}-linux-amd64.tar.gz`は独立したオフライン環境パッケージです。

3.  オフライン ミラーをカスタマイズするか、既存のオフライン ミラーの内容を調整します。

    既存のオフライン ミラーを調整する (新しいバージョンのコンポーネントを追加するなど) 場合は、次の手順を実行します。

    1.  オフライン ミラーをプルする場合、コンポーネントやバージョン情報などのパラメータを介して特定の情報を指定することで、不完全なオフライン ミラーを取得できます。たとえば、次のコマンドを実行して、 TiUP v1.11.3 とTiUP クラスタ v1.11.3 のオフライン ミラーのみを含むオフライン ミラーをプルできます。

        {{< copyable "" >}}

        ```bash
        tiup mirror clone tiup-custom-mirror-v1.11.3 --tiup v1.11.3 --cluster v1.11.3
        ```

        特定のプラットフォーム用のコンポーネントのみが必要な場合は、 `--os`または`--arch`パラメーターを使用して指定できます。

    2.  「 TiUPを使用してミラーをプルする」の手順 2 を参照して、この不完全なオフライン ミラーを隔離環境の制御マシンに送信します。

    3.  隔離された環境の制御マシンで、現在のオフライン ミラーのパスを確認します。 TiUPツールが最近のバージョンの場合、次のコマンドを実行して現在のミラー アドレスを取得できます。

        {{< copyable "" >}}

        ```bash
        tiup mirror show
        ```

        上記のコマンドの出力が`show`コマンドが存在しないことを示している場合は、古いバージョンのTiUPを使用している可能性があります。この場合、現在のミラー アドレスは`$HOME/.tiup/tiup.toml`から取得できます。このミラー アドレスを記録します。次の手順では、このアドレスを参照するために`${base_mirror}`が使用されます。

    4.  不完全なオフライン ミラーを既存のオフライン ミラーにマージします。

        まず、現在のオフライン ミラーの`keys`ディレクトリを`$HOME/.tiup`ディレクトリにコピーします。

        {{< copyable "" >}}

        ```bash
        cp -r ${base_mirror}/keys $HOME/.tiup/
        ```

        次に、 TiUPコマンドを使用して、不完全なオフライン ミラーを使用中のミラーにマージします。

        {{< copyable "" >}}

        ```bash
        tiup mirror merge tiup-custom-mirror-v1.11.3
        ```

    5.  上記の手順が完了したら、 `tiup list`コマンドを実行して結果を確認します。このドキュメントの例では、 `tiup list tiup`と`tiup list cluster`の両方の出力が、 `v1.11.3`の対応するコンポーネントが利用可能であることを示しています。

#### オフラインTiUPコンポーネントをデプロイ {#deploy-the-offline-tiup-component}

パッケージをターゲット クラスタの制御マシンに送信した後、次のコマンドを実行してTiUPコンポーネントをインストールします。

{{< copyable "" >}}

```bash
tar xzvf tidb-community-server-${version}-linux-amd64.tar.gz && \
sh tidb-community-server-${version}-linux-amd64/local_install.sh && \
source /home/tidb/.bash_profile
```

`local_install.sh`スクリプトは`tiup mirror set tidb-community-server-${version}-linux-amd64`コマンドを自動的に実行して、現在のミラー アドレスを`tidb-community-server-${version}-linux-amd64`に設定します。

#### オフライン パッケージをマージする {#merge-offline-packages}

[公式ダウンロードページ](https://www.pingcap.com/download/)からオフライン パッケージをダウンロードする場合は、サーバーパッケージとツールキット パッケージをオフライン ミラーにマージする必要があります。 `tiup mirror clone`コマンドを使用してオフラインコンポーネントパッケージを手動でパッケージ化する場合は、この手順を省略できます。

次のコマンドを実行して、オフライン ツールキット パッケージをサーバーパッケージ ディレクトリにマージします。

```bash
tar xf tidb-community-toolkit-${version}-linux-amd64.tar.gz
ls -ld tidb-community-server-${version}-linux-amd64 tidb-community-toolkit-${version}-linux-amd64
cd tidb-community-server-${version}-linux-amd64/
cp -rp keys ~/.tiup/
tiup mirror merge ../tidb-community-toolkit-${version}-linux-amd64
```

ミラーを別のディレクトリに切り替えるには、 `tiup mirror set <mirror-dir>`コマンドを実行します。ミラーをオンライン環境に切り替えるには、 `tiup mirror set https://tiup-mirrors.pingcap.com`コマンドを実行します。

## 手順 3. クラスター トポロジ ファイルを初期化する {#step-3-initialize-cluster-topology-file}

次のコマンドを実行して、クラスター トポロジ ファイルを作成します。

{{< copyable "" >}}

```shell
tiup cluster template > topology.yaml
```

次の 2 つの一般的なシナリオでは、コマンドを実行して、推奨されるトポロジ テンプレートを生成できます。

-   ハイブリッド デプロイの場合: 複数のインスタンスが 1 台のマシンにデプロイされます。詳細については、 [ハイブリッド展開トポロジ](/hybrid-deployment-topology.md)を参照してください。

    {{< copyable "" >}}

    ```shell
    tiup cluster template --full > topology.yaml
    ```

-   地理的に分散した配置の場合: TiDB クラスターは、地理的に分散したデータ センターに配置されます。詳細については、 [地理的に分散された展開トポロジ](/geo-distributed-deployment-topology.md)を参照してください。

    {{< copyable "" >}}

    ```shell
    tiup cluster template --multi-dc > topology.yaml
    ```

`vi topology.yaml`を実行して、構成ファイルの内容を確認します。

{{< copyable "" >}}

```shell
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/tidb-deploy"
  data_dir: "/tidb-data"
server_configs: {}
pd_servers:
  - host: 10.0.1.4
  - host: 10.0.1.5
  - host: 10.0.1.6
tidb_servers:
  - host: 10.0.1.7
  - host: 10.0.1.8
  - host: 10.0.1.9
tikv_servers:
  - host: 10.0.1.1
  - host: 10.0.1.2
  - host: 10.0.1.3
monitoring_servers:
  - host: 10.0.1.4
grafana_servers:
  - host: 10.0.1.4
alertmanager_servers:
  - host: 10.0.1.4
```

次の例では、7 つの一般的なシナリオについて説明します。対応するリンクのトポロジの説明とテンプレートに従って、構成ファイル (名前は`topology.yaml` ) を変更する必要があります。その他のシナリオでは、それに応じて構成テンプレートを編集します。

| 応用                                                                    | コンフィグレーションタスク                                                  | コンフィグレーションファイルのテンプレート                                                                                                                                                                                                                                                                                                                                                                                    | トポロジの説明                                                                                                                                                           |
| :-------------------------------------------------------------------- | :------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| OLTP                                                                  | [最小限のトポロジをデプロイ](/minimal-deployment-topology.md)               | [シンプルな最小限の構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-mini.yaml) <br/> [完全な最小構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-mini.yaml)                                                                                                                                                                                                 | これは、tidb-server、tikv-server、および pd-server を含む基本的なクラスター トポロジです。                                                                                                    |
| HTAP                                                                  | [TiFlashトポロジをデプロイ](/tiflash-deployment-topology.md)            | [シンプルなTiFlash構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-tiflash.yaml) <br/> [完全なTiFlash構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-tiflash.yaml)                                                                                                                                                                                   | これは、最小限のクラスター トポロジと共にTiFlashをデプロイするためのものです。 TiFlashは柱状のstorageエンジンであり、徐々に標準のクラスター トポロジーになります。                                                                     |
| [TiCDC](/ticdc/ticdc-overview.md)を使用して増分データをレプリケートする                  | [TiCDC トポロジをデプロイ](/ticdc-deployment-topology.md)               | [シンプルな TiCDC 構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-cdc.yaml) <br/> [完全な TiCDC 構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-cdc.yaml)                                                                                                                                                                                           | これは、最小限のクラスター トポロジと共に TiCDC をデプロイすることです。 TiCDC は、TiDB、MySQL、MQ など、複数のダウンストリーム プラットフォームをサポートしています。                                                                 |
| [TiDBBinlog](/tidb-binlog/tidb-binlog-overview.md)を使用して増分データをレプリケートする | [TiDB Binlogトポロジをデプロイ](/tidb-binlog-deployment-topology.md)    | [シンプルな TiDB Binlog構成テンプレート (MySQL をダウンストリームとして)](https://github.com/pingcap/docs/blob/master/config-templates/simple-tidb-binlog.yaml) <br/> [シンプルな TiDB Binlog構成テンプレート (ダウンストリームとしてのファイル)](https://github.com/pingcap/docs/blob/master/config-templates/simple-file-binlog.yaml) <br/> [完全な TiDB Binlog構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-tidb-binlog.yaml) | これは、最小限のクラスター トポロジと共に TiDB Binlogをデプロイするためのものです。                                                                                                                  |
| Spark で OLAP を使用する                                                    | [TiSpark トポロジをデプロイ](/tispark-deployment-topology.md)           | [シンプルな TiSpark 構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-tispark.yaml) <br/> [完全な TiSpark 構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-tispark.yaml)                                                                                                                                                                               | これは、最小限のクラスター トポロジと共に TiSpark をデプロイするためのものです。 TiSpark は、TiDB/TiKV 上で Apache Spark を実行して OLAP クエリに応答するために構築されたコンポーネントです。現在、TiSpark に対するTiUPクラスターのサポートはまだ**実験的**です。 |
| 複数のインスタンスを 1 台のマシンにデプロイ                                               | [ハイブリッド トポロジをデプロイ](/hybrid-deployment-topology.md)             | [ハイブリッド展開用のシンプルな構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-multi-instance.yaml) <br/> [ハイブリッド展開用の完全な構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-multi-instance.yaml)                                                                                                                                                               | デプロイ トポロジは、ディレクトリ、ポート、リソース比率、およびラベルの構成を追加する必要がある場合にも適用されます。                                                                                                       |
| データセンター全体に TiDB クラスターをデプロイ                                            | [地理的に分散した展開トポロジをデプロイ](/geo-distributed-deployment-topology.md) | [地理的に分散した配置のコンフィグレーションテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/geo-redundancy-deployment.yaml)                                                                                                                                                                                                                                                                               | このトポロジは、例として 2 つの都市にある 3 つのデータ センターの典型的なアーキテクチャを取り上げています。地理的に分散したデプロイアーキテクチャと、注意が必要な主要な構成について説明します。                                                               |

> **ノート：**
>
> -   グローバルに有効なパラメーターについては、構成ファイルの`server_configs`セクションで、対応するコンポーネントのこれらのパラメーターを構成します。
> -   特定のノードで有効にする必要があるパラメーターについては、このノードの`config`でこれらのパラメーターを構成します。
> -   `.`を使用して、構成のサブカテゴリ`log.slow-threshold`など) を示します。その他の形式については、 [TiUP構成テンプレート](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml)を参照してください。
> -   ターゲット マシンに作成するユーザー グループ名を指定する必要がある場合は、 [この例](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml#L7)を参照してください。

構成の詳細については、次の構成例を参照してください。

-   [TiDB `config.toml.example`](https://github.com/pingcap/tidb/blob/master/config/config.toml.example)
-   [TiKV `config.toml.example`](https://github.com/tikv/tikv/blob/master/etc/config-template.toml)
-   [PD `config.toml.example`](https://github.com/pingcap/pd/blob/master/conf/config.toml)
-   [TiFlash `config.toml.example`](https://github.com/pingcap/tiflash/blob/master/etc/config-template.toml)

## ステップ 4. デプロイ コマンドを実行する {#step-4-run-the-deployment-command}

> **ノート：**
>
> TiUPを使用して TiDB をデプロイする場合、セキュリティ認証に秘密鍵または対話型パスワードを使用できます。
>
> -   秘密鍵を使用する場合は、鍵のパスを`-i`または`--identity_file`で指定します。
> -   パスワードを使用する場合は、 `-p`フラグを追加して、パスワード インタラクション ウィンドウに入ります。
> -   ターゲット マシンへのパスワードなしのログインが設定されている場合、認証は必要ありません。
>
> 一般に、 TiUP は、次の例外を除いて、ターゲット マシン上の`topology.yaml`ファイルで指定されたユーザーとグループを作成します。
>
> -   `topology.yaml`で構成されたユーザー名は、ターゲット マシンに既に存在します。
> -   コマンド ラインで`--skip-create-user`オプションを使用して、ユーザーを作成する手順を明示的にスキップしました。

`deploy`コマンドを実行する前に、 `check`および`check --apply`コマンドを使用して、クラスター内の潜在的なリスクを検出し、自動的に修復します。

1.  潜在的なリスクを確認します。

    {{< copyable "" >}}

    ```shell
    tiup cluster check ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

2.  自動修復を有効にします。

    {{< copyable "" >}}

    ```shell
    tiup cluster check ./topology.yaml --apply --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

3.  TiDB クラスターをデプロイ。

    {{< copyable "" >}}

    ```shell
    tiup cluster deploy tidb-test v6.5.2 ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

上記の`tiup cluster deploy`コマンドで:

-   `tidb-test`は、デプロイする TiDB クラスターの名前です。
-   `v6.5.2`は、デプロイする TiDB クラスターのバージョンです。 `tiup list tidb`を実行すると、サポートされている最新のバージョンを確認できます。
-   `topology.yaml`は初期設定ファイルです。
-   `--user root` 、ターゲット マシンに`root`ユーザーとしてログインして、クラスターの展開を完了することを示します。 `root`人のユーザーは、ターゲット マシンに対して`ssh`と`sudo`権限を持つことが期待されます。または、 `ssh`および`sudo`権限を持つ他のユーザーを使用して展開を完了することもできます。
-   `[-i]`と`[-p]`はオプションです。パスワードなしでターゲット マシンへのログインを設定した場合、これらのパラメータは必要ありません。そうでない場合は、2 つのパラメーターのいずれかを選択します。 `[-i]`は、ターゲット マシンにアクセスできる root ユーザー (または`--user`で指定された他のユーザー) の秘密鍵です。 `[-p]`は、対話的にユーザーパスワードを入力するために使用されます。

出力ログの最後に、 ``Deployed cluster `tidb-test` successfully``が表示されます。これは、デプロイが成功したことを示します。

## ステップ 5. TiUPによって管理されているクラスターを確認する {#step-5-check-the-clusters-managed-by-tiup}

{{< copyable "" >}}

```shell
tiup cluster list
```

TiUP は、複数の TiDB クラスターの管理をサポートしています。上記のコマンドは、現在TiUPによって管理されているすべてのクラスターの情報を出力します。これには、クラスター名、デプロイ ユーザー、バージョン、秘密鍵の情報が含まれます。

## ステップ 6. デプロイされた TiDB クラスターのステータスを確認する {#step-6-check-the-status-of-the-deployed-tidb-cluster}

たとえば、次のコマンドを実行して`tidb-test`クラスターのステータスを確認します。

{{< copyable "" >}}

```shell
tiup cluster display tidb-test
```

予想される出力には、インスタンス ID、ロール、ホスト、リスニング ポート、ステータス (クラスターがまだ開始されていないため、ステータスは`Down` / `inactive`です)、およびディレクトリ情報が含まれます。

## ステップ 7. TiDB クラスターを開始する {#step-7-start-a-tidb-cluster}

TiUP cluster v1.9.0以降、新しい起動方法としてセーフスタートが導入されました。この方法でデータベースを起動すると、データベースのセキュリティが向上します。この方法を使用することをお勧めします。

安全な起動後、 TiUP はTiDB root ユーザーのパスワードを自動的に生成し、コマンドライン インターフェイスでパスワードを返します。

> **ノート：**
>
> -   TiDB クラスターを安全に起動した後、パスワードなしで root ユーザーを使用して TiDB にログインすることはできません。したがって、今後のログインのために、コマンド出力で返されるパスワードを記録する必要があります。
>
> -   パスワードは一度だけ生成されます。記録していない場合や忘れてしまった場合は、 [`root`パスワードを忘れる](/user-account-management.md#forget-the-root-password)を参照してパスワードを変更してください。

方法 1: 安全なスタート

{{< copyable "" >}}

```shell
tiup cluster start tidb-test --init
```

出力が次のようになっていれば、開始は成功しています。

{{< copyable "" >}}

```shell
Started cluster `tidb-test` successfully.
The root password of TiDB database has been changed.
The new password is: 'y_+3Hwp=*AWz8971s6'.
Copy and record it to somewhere safe, it is only displayed once, and will not be stored.
The generated password can NOT be got again in future.
```

方法 2: 標準スタート

{{< copyable "" >}}

```shell
tiup cluster start tidb-test
```

出力ログに``Started cluster `tidb-test` successfully``が含まれていれば、開始は成功しています。標準起動後、パスワードなしで root ユーザーを使用してデータベースにログインできます。

## ステップ 8. TiDB クラスターの実行ステータスを確認する {#step-8-verify-the-running-status-of-the-tidb-cluster}

{{< copyable "" >}}

```shell
tiup cluster display tidb-test
```

出力ログに`Up`ステータスが表示されている場合、クラスターは正常に動作しています。

## こちらもご覧ください {#see-also}

[TiFlash](/tiflash/tiflash-overview.md) TiDB クラスターと共にデプロイした場合は、次のドキュメントを参照してください。

-   [TiFlashを使う](/tiflash/tiflash-overview.md#use-tiflash)
-   [TiFlashクラスタを管理](/tiflash/maintain-tiflash.md)
-   [TiFlashアラートのルールと解決策](/tiflash/tiflash-alert-rules.md)
-   [TiFlashのトラブルシューティング](/tiflash/troubleshoot-tiflash.md)

[TiCDC](/ticdc/ticdc-overview.md) TiDB クラスターと共にデプロイした場合は、次のドキュメントを参照してください。

-   [チェンジフィードの概要](/ticdc/ticdc-changefeed-overview.md)
-   [チェンジフィードの管理](/ticdc/ticdc-manage-changefeed.md)
-   [TiCDC のトラブルシューティング](/ticdc/troubleshoot-ticdc.md)
-   [TiCDC よくある質問](/ticdc/ticdc-faq.md)
