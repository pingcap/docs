---
title: Deploy a TiDB Cluster Using TiUP
summary: Learn how to easily deploy a TiDB cluster using TiUP.
---

# TiUPを使用した TiDBクラスタのデプロイ {#deploy-a-tidb-cluster-using-tiup}

[TiUP](https://github.com/pingcap/tiup)は、TiDB 4.0 で導入されたクラスターの運用および保守ツールです。 TiUP は、 Golangで書かれたクラスター管理コンポーネント[TiUPクラスター](https://github.com/pingcap/tiup/tree/master/components/cluster)を提供します。 TiUPクラスターを使用すると、TiDB クラスターのデプロイ、開始、停止、破棄、スケーリング、アップグレードなどの日常的なデータベース操作を簡単に実行し、TiDB クラスターのパラメーターを管理できます。

TiUP は、TiDB、 TiFlash、TiDB Binlog、TiCDC、および監視システムの導入をサポートしています。このドキュメントでは、さまざまなトポロジーの TiDB クラスターをデプロイする方法を紹介します。

## ステップ 1. 前提条件と事前チェック {#step-1-prerequisites-and-precheck}

次の文書を必ず読んでください。

-   [ハードウェアとソフトウェアの要件](/hardware-and-software-requirements.md)
-   [環境およびシステム構成の確認](/check-before-deployment.md)

## ステップ 2. 制御マシンにTiUPをデプロイ {#step-2-deploy-tiup-on-the-control-machine}

TiUP は、オンライン展開とオフライン展開の 2 つの方法のいずれかで制御マシンに展開できます。

### TiUPをオンラインでデプロイ {#deploy-tiup-online}

通常のユーザー アカウントを使用して制御マシンにログインします (例として`tidb`ユーザーを取り上げます)。以降のTiUP のインストールとクラスター管理は`tidb`ユーザーが実行できます。

1.  次のコマンドを実行してTiUPをインストールします。

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2.  TiUP環境変数を設定します。

    1.  グローバル環境変数を再宣言します。

        ```shell
        source .bash_profile
        ```

    2.  TiUPがインストールされているかどうかを確認します。

        ```shell
        which tiup
        ```

3.  TiUPクラスターコンポーネントをインストールします。

    ```shell
    tiup cluster
    ```

4.  TiUPがすでにインストールされている場合は、 TiUPクラスターコンポーネントを最新バージョンに更新します。

    ```shell
    tiup update --self && tiup update cluster
    ```

    `Update successfully!`が表示されれば、 TiUPクラスターは正常に更新されています。

5.  TiUPクラスターの現在のバージョンを確認します。

    ```shell
    tiup --binary cluster
    ```

### TiUP をオフラインでデプロイ {#deploy-tiup-offline}

TiUPを使用して TiDB クラスターをオフラインでデプロイするには、このセクションの次の手順を実行します。

#### TiUPオフラインコンポーネントパッケージを準備する {#prepare-the-tiup-offline-component-package}

方法 1: [公式ダウンロードページ](https://www.pingcap.com/download/)で、ターゲット TiDB バージョンのオフライン ミラー パッケージ (TiUPオフライン パッケージを含む) を選択します。サーバーパッケージとツールキット パッケージを同時にダウンロードする必要があることに注意してください。

方法 2: `tiup mirror clone`を使用してオフラインコンポーネントパッケージを手動でパックします。詳細な手順は次のとおりです。

1.  TiUPパッケージ マネージャーをオンラインでインストールします。

    1.  TiUPツールをインストールします。

        ```shell
        curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
        ```

    2.  グローバル環境変数を再宣言します。

        ```shell
        source .bash_profile
        ```

    3.  TiUPがインストールされているかどうかを確認します。

        ```shell
        which tiup
        ```

2.  TiUPを使用してミラーを引き出します。

    1.  インターネットにアクセスできるマシン上で必要なコンポーネントをプルします。

        ```shell
        tiup mirror clone tidb-community-server-${version}-linux-amd64 ${version} --os=linux --arch=amd64
        ```

        上記のコマンドは、現在のディレクトリに`tidb-community-server-${version}-linux-amd64`という名前のディレクトリを作成します。このディレクトリには、クラスターの起動に必要なコンポーネントパッケージが含まれています。

    2.  `tar`コマンドを使用してコンポーネントパッケージをパックし、そのパッケージを分離環境の制御マシンに送信します。

        ```bash
        tar czvf tidb-community-server-${version}-linux-amd64.tar.gz tidb-community-server-${version}-linux-amd64
        ```

        `tidb-community-server-${version}-linux-amd64.tar.gz`独立したオフライン環境パッケージです。

3.  オフライン ミラーをカスタマイズするか、既存のオフライン ミラーの内容を調整します。

    既存のオフライン ミラーを調整する場合 (新しいバージョンのコンポーネントを追加するなど)、次の手順を実行します。

    1.  オフライン ミラーをプルする場合、コンポーネントやバージョン情報などの特定の情報をパラメータで指定することで、不完全なオフライン ミラーを取得できます。たとえば、次のコマンドを実行すると、 TiUP v1.12.3 およびTiUP クラスタ v1.12.3 のオフライン ミラーのみを含むオフライン ミラーをプルできます。

        ```bash
        tiup mirror clone tiup-custom-mirror-v1.12.3 --tiup v1.12.3 --cluster v1.12.3
        ```

        特定のプラットフォームのコンポーネントのみが必要な場合は、 `--os`または`--arch`パラメータを使用してコンポーネントを指定できます。

    2.  「 TiUPを使用してミラーをプルする」の手順 2 を参照して、この未完成のオフライン ミラーを分離環境の制御マシンに送信します。

    3.  隔離された環境の制御マシン上の現在のオフライン ミラーのパスを確認します。 TiUPツールが最新バージョンの場合は、次のコマンドを実行して現在のミラー アドレスを取得できます。

        ```bash
        tiup mirror show
        ```

        上記のコマンドの出力で`show`コマンドが存在しないことが示されている場合は、古いバージョンのTiUPを使用している可能性があります。この場合、現在のミラー アドレスは`$HOME/.tiup/tiup.toml`から取得できます。このミラーアドレスを記録します。次の手順では、このアドレスを参照するために`${base_mirror}`が使用されます。

    4.  不完全なオフライン ミラーを既存のオフライン ミラーにマージします。

        まず、現在のオフライン ミラーの`keys`ディレクトリを`$HOME/.tiup`ディレクトリにコピーします。

        ```bash
        cp -r ${base_mirror}/keys $HOME/.tiup/
        ```

        次に、 TiUPコマンドを使用して、不完全なオフライン ミラーを使用中のミラーにマージします。

        ```bash
        tiup mirror merge tiup-custom-mirror-v1.12.3
        ```

    5.  上記の手順が完了したら、 `tiup list`コマンドを実行して結果を確認します。このドキュメントの例では、 `tiup list tiup`と`tiup list cluster`の両方の出力は、 `v1.12.3`の対応するコンポーネントが使用可能であることを示しています。

#### オフラインTiUPコンポーネントをデプロイ {#deploy-the-offline-tiup-component}

パッケージをターゲット クラスターの制御マシンに送信した後、次のコマンドを実行してTiUPコンポーネントをインストールします。

```bash
tar xzvf tidb-community-server-${version}-linux-amd64.tar.gz && \
sh tidb-community-server-${version}-linux-amd64/local_install.sh && \
source /home/tidb/.bash_profile
```

`local_install.sh`スクリプトは`tiup mirror set tidb-community-server-${version}-linux-amd64`コマンドを自動的に実行して、現在のミラー アドレスを`tidb-community-server-${version}-linux-amd64`に設定します。

#### オフラインパッケージをマージする {#merge-offline-packages}

[公式ダウンロードページ](https://www.pingcap.com/download/)からオフライン パッケージをダウンロードする場合は、サーバーパッケージとツールキット パッケージをオフライン ミラーにマージする必要があります。 `tiup mirror clone`コマンドを使用してオフラインコンポーネントパッケージを手動でパッケージ化する場合は、この手順をスキップできます。

次のコマンドを実行して、オフライン ツールキット パッケージをサーバーパッケージ ディレクトリにマージします。

```bash
tar xf tidb-community-toolkit-${version}-linux-amd64.tar.gz
ls -ld tidb-community-server-${version}-linux-amd64 tidb-community-toolkit-${version}-linux-amd64
cd tidb-community-server-${version}-linux-amd64/
cp -rp keys ~/.tiup/
tiup mirror merge ../tidb-community-toolkit-${version}-linux-amd64
```

ミラーを別のディレクトリに切り替えるには、 `tiup mirror set <mirror-dir>`コマンドを実行します。ミラーをオンライン環境に切り替えるには、 `tiup mirror set https://tiup-mirrors.pingcap.com`コマンドを実行します。

## ステップ 3. クラスター・トポロジー・ファイルを初期化する {#step-3-initialize-cluster-topology-file}

次のコマンドを実行して、クラスター トポロジ ファイルを作成します。

```shell
tiup cluster template > topology.yaml
```

次の 2 つの一般的なシナリオでは、コマンドを実行して推奨トポロジ テンプレートを生成できます。

-   ハイブリッド デプロイメントの場合: 複数のインスタンスが 1 台のマシンにデプロイされます。詳細は[ハイブリッド展開トポロジ](/hybrid-deployment-topology.md)を参照してください。

    ```shell
    tiup cluster template --full > topology.yaml
    ```

-   地理的に分散した展開の場合: TiDB クラスターは地理的に分散したデータ センターに展開されます。詳細は[地理的に分散した導入トポロジ](/geo-distributed-deployment-topology.md)を参照してください。

    ```shell
    tiup cluster template --multi-dc > topology.yaml
    ```

`vi topology.yaml`を実行して構成ファイルの内容を確認します。

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

次の例では、7 つの一般的なシナリオを取り上げます。対応するリンク内のトポロジーの説明とテンプレートに従って、構成ファイル ( `topology.yaml`という名前) を変更する必要があります。他のシナリオの場合は、それに応じて構成テンプレートを編集します。

| 応用                                                                    | コンフィグレーションタスク                                                   | コンフィグレーションファイルのテンプレート                                                                                                                                                                                                                                                                                                                                                                                   | トポロジの説明                                                                                                                                                       |
| :-------------------------------------------------------------------- | :-------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| OLTP                                                                  | [最小限のトポロジをデプロイ](/minimal-deployment-topology.md)                | [シンプルな最小限の構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-mini.yaml) <br/> [完全な最小構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-mini.yaml)                                                                                                                                                                                                | これは、tidb-server、tikv-server、pd-server を含む基本的なクラスター トポロジーです。                                                                                                   |
| HTAP                                                                  | [TiFlashトポロジをデプロイ](/tiflash-deployment-topology.md)             | [シンプルなTiFlash構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-tiflash.yaml) <br/> [完全なTiFlash構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-tiflash.yaml)                                                                                                                                                                                  | これは、最小限のクラスター トポロジとともにTiFlashを展開するためです。 TiFlashはカラム型storageエンジンであり、徐々に標準のクラスター トポロジになりつつあります。                                                                 |
| [TiCDC](/ticdc/ticdc-overview.md)を使用して増分データをレプリケートする                  | [TiCDC トポロジをデプロイ](/ticdc-deployment-topology.md)                | [シンプルな TiCDC 構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-cdc.yaml) <br/> [完全な TiCDC 構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-cdc.yaml)                                                                                                                                                                                          | これは、最小限のクラスター トポロジとともに TiCDC を展開するためです。 TiCDC は、TiDB、MySQL、Kafka、MQ、storageサービスなどの複数のダウンストリーム プラットフォームをサポートします。                                               |
| [TiDBBinlog](/tidb-binlog/tidb-binlog-overview.md)を使用して増分データをレプリケートする | [TiDB Binlogトポロジをデプロイ](/tidb-binlog-deployment-topology.md)     | [シンプルな TiDB Binlog構成テンプレート (ダウンストリームとして MySQL)](https://github.com/pingcap/docs/blob/master/config-templates/simple-tidb-binlog.yaml) <br/> [シンプルな TiDB Binlog構成テンプレート (ダウンストリームとしてのファイル)](https://github.com/pingcap/docs/blob/master/config-templates/simple-file-binlog.yaml) <br/> [完全な TiDB Binlog構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-tidb-binlog.yaml) | これは、最小限のクラスター トポロジとともに TiDB Binlogをデプロイするためです。                                                                                                                |
| Spark で OLAP を使用する                                                    | [TiSpark トポロジをデプロイ](/tispark-deployment-topology.md)            | [シンプルな TiSpark 構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-tispark.yaml) <br/> [完全な TiSpark 構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-tispark.yaml)                                                                                                                                                                              | これは、最小限のクラスター トポロジとともに TiSpark をデプロイするためです。 TiSpark は、TiDB/TiKV 上で Apache Spark を実行して OLAP クエリに応答するために構築されたコンポーネントです。現在、 TiUPクラスターの TiSpark サポートはまだ**実験的**です。 |
| 単一マシン上に複数のインスタンスをデプロイ                                                 | [ハイブリッド トポロジをデプロイ](/hybrid-deployment-topology.md)              | [ハイブリッド展開のためのシンプルな構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-multi-instance.yaml) <br/> [ハイブリッド展開用の完全な構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-multi-instance.yaml)                                                                                                                                                            | デプロイメント トポロジは、ディレクトリ、ポート、リソース比率、およびラベルの追加構成を追加する必要がある場合にも適用されます。                                                                                              |
| データセンター全体に TiDB クラスターをデプロイ                                            | [地理的に分散された展開トポロジをデプロイ](/geo-distributed-deployment-topology.md) | [地理的に分散した展開のためのコンフィグレーションテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/geo-redundancy-deployment.yaml)                                                                                                                                                                                                                                                                           | このトポロジは、2 つの都市にある 3 つのデータセンターの一般的なアーキテクチャを例にしています。地理的に分散された展開アーキテクチャと、注意が必要な主要な構成について説明します。                                                                   |

> **注記：**
>
> -   グローバルに有効にするパラメータについては、設定ファイルの`server_configs`セクションで対応するコンポーネントのパラメータを設定します。
> -   特定のノードで有効にするパラメータについては、このノードの`config`でこれらのパラメータを設定します。
> -   構成のサブカテゴリを示すには`.`を使用します ( `log.slow-threshold`など)。その他の形式については、 [TiUP設定テンプレート](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml)を参照してください。
> -   ターゲット マシン上に作成されるユーザー グループ名を指定する必要がある場合は、 [この例](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml#L7)を参照してください。

構成の詳細については、次の構成例を参照してください。

-   [TiDB `config.toml.example`](https://github.com/pingcap/tidb/blob/release-7.5/pkg/config/config.toml.example)
-   [TiKV `config.toml.example`](https://github.com/tikv/tikv/blob/release-7.5/etc/config-template.toml)
-   [PD `config.toml.example`](https://github.com/pingcap/pd/blob/release-7.5/conf/config.toml)
-   [TiFlash `config.toml.example`](https://github.com/pingcap/tiflash/blob/release-7.5/etc/config-template.toml)

## ステップ 4. デプロイメント・コマンドを実行する {#step-4-run-the-deployment-command}

> **注記：**
>
> TiUPを使用して TiDB をデプロイする場合、セキュリティ認証に秘密キーまたは対話型パスワードを使用できます。
>
> -   秘密鍵を使用する場合は、 `-i`または`--identity_file`で鍵のパスを指定します。
> -   パスワードを使用する場合は、 `-p`フラグを追加してパスワード対話ウィンドウに入ります。
> -   ターゲット マシンへのパスワードなしのログインが設定されている場合、認証は必要ありません。
>
> 一般に、 TiUP は、次の例外を除いて、 `topology.yaml`ファイルで指定されたユーザーとグループをターゲット マシンに作成します。
>
> -   `topology.yaml`で設定したユーザー名は、ターゲット マシン上にすでに存在します。
> -   コマンドラインで`--skip-create-user`オプションを使用して、ユーザーの作成手順を明示的にスキップしました。

`deploy`コマンドを実行する前に、 `check`と`check --apply`のコマンドを使用して、クラスター内の潜在的なリスクを検出し、自動的に修復します。

1.  潜在的なリスクを確認します。

    ```shell
    tiup cluster check ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

2.  自動修復を有効にする:

    ```shell
    tiup cluster check ./topology.yaml --apply --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

3.  TiDB クラスターをデプロイ。

    ```shell
    tiup cluster deploy tidb-test v7.5.0 ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

上記の`tiup cluster deploy`コマンドでは次のようになります。

-   `tidb-test`は、デプロイされる TiDB クラスターの名前です。
-   `v7.5.0`は、デプロイされる TiDB クラスターのバージョンです。 `tiup list tidb`を実行すると、サポートされている最新のバージョンを確認できます。
-   `topology.yaml`は初期化設定ファイルです。
-   `--user root` 、ターゲット マシンに`root`ユーザーとしてログインしてクラスターの展開を完了することを示します。 `root`ユーザーは、ターゲット マシンに対する`ssh`および`sudo`権限を持つことが期待されます。あるいは、 `ssh`および`sudo`権限を持つ他のユーザーを使用して展開を完了することもできます。
-   `[-i]`と`[-p]`はオプションです。パスワードなしでターゲット マシンへのログインを設定した場合、これらのパラメータは必要ありません。そうでない場合は、2 つのパラメータのいずれかを選択します。 `[-i]`は、ターゲット マシンにアクセスできる root ユーザー (または`--user`で指定された他のユーザー) の秘密キーです。 `[-p]`は、ユーザーのパスワードを対話的に入力するために使用されます。

出力ログの最後には``Deployed cluster `tidb-test` successfully``が表示されます。これは、展開が成功したことを示します。

## ステップ 5. TiUPによって管理されているクラスターを確認する {#step-5-check-the-clusters-managed-by-tiup}

```shell
tiup cluster list
```

TiUP は、複数の TiDB クラスターの管理をサポートします。前述のコマンドは、クラスター名、デプロイメント ユーザー、バージョン、秘密キー情報など、 TiUPによって現在管理されているすべてのクラスターの情報を出力します。

## ステップ 6. デプロイされた TiDB クラスターのステータスを確認する {#step-6-check-the-status-of-the-deployed-tidb-cluster}

たとえば、次のコマンドを実行して`tidb-test`クラスターのステータスを確認します。

```shell
tiup cluster display tidb-test
```

予期される出力には、インスタンス ID、ロール、ホスト、リスニング ポート、ステータス (クラスターがまだ起動していないため、ステータスは`Down` / `inactive`です)、およびディレクトリ情報が含まれます。

## ステップ 7. TiDB クラスターを開始する {#step-7-start-a-tidb-cluster}

TiUPクラスタ v1.9.0 以降、新しい起動方法としてセーフ スタートが導入されました。この方法を使用してデータベースを起動すると、データベースのセキュリティが向上します。この方法を使用することをお勧めします。

安全に起動した後、 TiUP はTiDB root ユーザーのパスワードを自動的に生成し、コマンドライン インターフェイスでそのパスワードを返します。

> **注記：**
>
> -   TiDB クラスターを安全に起動した後は、パスワードなしで root ユーザーを使用して TiDB にログインすることはできません。したがって、今後のログインに備えて、コマンド出力で返されたパスワードを記録する必要があります。
>
> -   パスワードは 1 回だけ生成されます。記録していない場合や忘れてしまった場合は、 [`root`パスワードを忘れた場合](/user-account-management.md#forget-the-root-password)を参照してパスワードを変更してください。

方法 1: 安全なスタート

```shell
tiup cluster start tidb-test --init
```

出力が次のようになれば、起動は成功です。

```shell
Started cluster `tidb-test` successfully.
The root password of TiDB database has been changed.
The new password is: 'y_+3Hwp=*AWz8971s6'.
Copy and record it to somewhere safe, it is only displayed once, and will not be stored.
The generated password can NOT be got again in future.
```

方法 2: 標準スタート

```shell
tiup cluster start tidb-test
```

出力ログに``Started cluster `tidb-test` successfully``が含まれていれば、起動は成功です。標準起動後は、パスワードなしで root ユーザーを使用してデータベースにログインできます。

## ステップ 8. TiDB クラスターの実行ステータスを確認する {#step-8-verify-the-running-status-of-the-tidb-cluster}

```shell
tiup cluster display tidb-test
```

出力ログに`Up`ステータスが示されている場合、クラスターは正常に実行されています。

## こちらも参照 {#see-also}

[TiFlash](/tiflash/tiflash-overview.md) TiDB クラスターとともにデプロイした場合は、次のドキュメントを参照してください。

-   [TiFlashを使用する](/tiflash/tiflash-overview.md#use-tiflash)
-   [TiFlashクラスタの管理](/tiflash/maintain-tiflash.md)
-   [TiFlashアラート ルールとソリューション](/tiflash/tiflash-alert-rules.md)
-   [TiFlashのトラブルシューティング](/tiflash/troubleshoot-tiflash.md)

[TiCDC](/ticdc/ticdc-overview.md) TiDB クラスターとともにデプロイした場合は、次のドキュメントを参照してください。

-   [チェンジフィードの概要](/ticdc/ticdc-changefeed-overview.md)
-   [変更フィードの管理](/ticdc/ticdc-manage-changefeed.md)
-   [TiCDC のトラブルシューティング](/ticdc/troubleshoot-ticdc.md)
-   [TiCDC よくある質問](/ticdc/ticdc-faq.md)
