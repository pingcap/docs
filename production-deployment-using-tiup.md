---
title: Deploy a TiDB Cluster Using TiUP
summary: Learn how to easily deploy a TiDB cluster using TiUP.
---

# TiUPを使用してTiDBクラスターをデプロイする {#deploy-a-tidb-cluster-using-tiup}

[TiUP](https://github.com/pingcap/tiup)は、TiDB4.0で導入されたクラスタの運用および保守ツールです。 TiUPは、Golangで記述されたクラスタ管理コンポーネントである[TiUPクラスタ](https://github.com/pingcap/tiup/tree/master/components/cluster)を提供します。 TiUPクラスタを使用すると、TiDBクラスターのデプロイ、開始、停止、破棄、スケーリング、アップグレードなどの日常的なデータベース操作を簡単に実行し、TiDBクラスタパラメーターを管理できクラスタ。

TiUPは、TiDB、TiFlash、TiDB Binlog、TiCDC、および監視システムの展開をサポートします。このドキュメントでは、さまざまなトポロジのTiDBクラスターを展開する方法を紹介します。

> **ノート：**
>
> TiDB、TiUP、およびTiDBダッシュボードは、使用法の詳細をPingCAPと共有して、製品を改善する方法を理解するのに役立ちます。共有される内容と共有を無効にする方法の詳細については、 [テレメトリー](/telemetry.md)を参照してください。

## ステップ1：前提条件と事前チェック {#step-1-prerequisites-and-precheck}

次のドキュメントを読んだことを確認してください。

-   [ハードウェアとソフトウェアの要件](/hardware-and-software-requirements.md)
-   [環境とシステム構成のチェック](/check-before-deployment.md)

## ステップ2：制御マシンにTiUPをインストールします {#step-2-install-tiup-on-the-control-machine}

TiUPは、オンライン展開とオフライン展開の2つの方法のいずれかで制御マシンにインストールできます。

### 方法1：TiUPをオンラインでデプロイ {#method-1-deploy-tiup-online}

通常のユーザーアカウントを使用してコントロールマシンにログインします（例として`tidb`人のユーザーを取り上げます）。以下のすべてのTiUPインストールおよびクラスタ管理操作は、 `tidb`のユーザーが実行できます。

1.  次のコマンドを実行して、TiUPをインストールします。

    {{< copyable "" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2.  TiUP環境変数を設定します。

    グローバル環境変数を再宣言します。

    {{< copyable "" >}}

    ```shell
    source .bash_profile
    ```

    TiUPがインストールされているかどうかを確認します。

    {{< copyable "" >}}

    ```shell
    which tiup
    ```

3.  TiUPクラスタコンポーネントをインストールします。

    {{< copyable "" >}}

    ```shell
    tiup cluster
    ```

4.  TiUPがすでにインストールされている場合は、TiUPクラスタコンポーネントを最新バージョンに更新します。

    {{< copyable "" >}}

    ```shell
    tiup update --self && tiup update cluster
    ```

    期待される出力には`“Update successfully!”`が含まれます。

5.  TiUPクラスタの現在のバージョンを確認します。

    {{< copyable "" >}}

    ```shell
    tiup --binary cluster
    ```

### 方法2：TiUPをオフラインでデプロイ {#method-2-deploy-tiup-offline}

このセクションの次の手順を実行して、TiUPを使用してTiDBクラスタをオフラインでデプロイします。

#### ステップ1：TiUPオフラインコンポーネントパッケージを準備する {#step-1-prepare-the-tiup-offline-component-package}

TiUPオフラインコンポーネントパッケージを準備するには、 `tiup mirror clone`を使用してオフラインコンポーネントパッケージを手動でパックします。

1.  TiUPパッケージマネージャーをオンラインでインストールします。

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

2.  TiUPを使用してミラーを引きます。

    1.  インターネットにアクセスできるマシンで必要なコンポーネントをプルします。

        {{< copyable "" >}}

        ```shell
        tiup mirror clone tidb-community-server-${version}-linux-amd64 ${version} --os=linux --arch=amd64
        ```

        上記のコマンドは、現在のディレクトリに`tidb-community-server-${version}-linux-amd64`という名前のディレクトリを作成します。このディレクトリには、クラスタの起動に必要なコンポーネントパッケージが含まれています。

    2.  `tar`コマンドを使用してコンポーネントパッケージをパックし、分離された環境の制御マシンにパッケージを送信します。

        {{< copyable "" >}}

        ```bash
        tar czvf tidb-community-server-${version}-linux-amd64.tar.gz tidb-community-server-${version}-linux-amd64
        ```

        `tidb-community-server-${version}-linux-amd64.tar.gz`は独立したオフライン環境パッケージです。

3.  オフラインミラーをカスタマイズするか、既存のオフラインミラーの内容を調整します。

    既存のオフラインミラーを調整する場合（コンポーネントの新しいバージョンの追加など）、次の手順を実行します。

    1.  オフラインミラーをプルする場合、コンポーネントやバージョン情報などのパラメーターを介して特定の情報を指定することにより、不完全なオフラインミラーを取得できます。たとえば、次のコマンドを実行することにより、TiUPv1.10.0およびTiUPClusterv1.10.0のオフラインミラーのみを含むオフラインミラーをプルできます。

        {{< copyable "" >}}

        ```bash
        tiup mirror clone tiup-custom-mirror-v1.10.0 --tiup v1.10.0 --cluster v1.10.0
        ```

        特定のプラットフォームのコンポーネントのみが必要な場合は、 `--os`つまたは`--arch`のパラメーターを使用してそれらを指定できます。

    2.  「TiUPを使用してミラーをプルする」のステップ2を参照し、この不完全なオフラインミラーを隔離された環境の制御マシンに送信します。

    3.  隔離された環境の制御マシンで現在のオフラインミラーのパスを確認します。 TiUPツールが最新バージョンの場合は、次のコマンドを実行して現在のミラーアドレスを取得できます。

        {{< copyable "" >}}

        ```bash
        tiup mirror show
        ```

        上記のコマンドの出力が`show`コマンドが存在しないことを示している場合は、古いバージョンのTiUPを使用している可能性があります。この場合、 `$HOME/.tiup/tiup.toml`から現在のミラーアドレスを取得できます。このミラーアドレスを記録します。次の手順では、 `${base_mirror}`を使用してこのアドレスを参照します。

    4.  不完全なオフラインミラーを既存のオフラインミラーにマージします。

        まず、現在のオフラインミラーの`keys`ディレクトリを`$HOME/.tiup`ディレクトリにコピーします。

        {{< copyable "" >}}

        ```bash
        cp -r ${base_mirror}/keys $HOME/.tiup/
        ```

        次に、TiUPコマンドを使用して、不完全なオフラインミラーを使用中のミラーにマージします。

        {{< copyable "" >}}

        ```bash
        tiup mirror merge tiup-custom-mirror-v1.10.0
        ```

    5.  上記の手順が完了したら、 `tiup list`コマンドを実行して結果を確認します。このドキュメントの例では、 `tiup list tiup`と`tiup list cluster`の両方の出力は、 `v1.10.0`の対応するコンポーネントが使用可能であることを示しています。

#### ステップ2：オフラインTiUPコンポーネントをデプロイ {#step-2-deploy-the-offline-tiup-component}

パッケージをターゲットクラスタの制御マシンに送信した後、次のコマンドを実行してTiUPコンポーネントをインストールします。

{{< copyable "" >}}

```bash
tar xzvf tidb-community-server-${version}-linux-amd64.tar.gz && \
sh tidb-community-server-${version}-linux-amd64/local_install.sh && \
source /home/tidb/.bash_profile
```

`local_install.sh`スクリプトは、 `tiup mirror set tidb-community-server-${version}-linux-amd64`コマンドを自動的に実行して、現在のミラーアドレスを`tidb-community-server-${version}-linux-amd64`に設定します。

ミラーを別のディレクトリに切り替えるには、 `tiup mirror set <mirror-dir>`コマンドを手動で実行できます。ミラーをオンライン環境に切り替えるには、 `tiup mirror set https://tiup-mirrors.pingcap.com`コマンドを実行します。

## ステップ3：クラスタトポロジファイルを初期化する {#step-3-initialize-cluster-topology-file}

目的のクラスタトポロジに従って、クラスタ初期化構成ファイルを手動で作成および編集する必要があります。

クラスタ初期化構成ファイルを作成するには、TiUPを使用してコントロールマシンにYAML形式の構成ファイルを作成できます。

{{< copyable "" >}}

```shell
tiup cluster template > topology.yaml
```

> **ノート：**
>
> ハイブリッド展開シナリオの場合、 `tiup cluster template --full > topology.yaml`を実行して、推奨されるトポロジテンプレートを作成することもできます。地理的に分散された展開シナリオの場合、 `tiup cluster template --multi-dc > topology.yaml`を実行して、推奨されるトポロジテンプレートを作成できます。

`vi topology.yaml`を実行して、構成ファイルの内容を確認します。

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

次の例では、6つの一般的なシナリオについて説明します。対応するリンクのトポロジの説明とテンプレートに従って、構成ファイル（ `topology.yaml`という名前）を変更する必要があります。他のシナリオでは、それに応じて構成テンプレートを編集します。

-   [最小限の展開トポロジ](/minimal-deployment-topology.md)

    これは、tidb-server、tikv-server、およびpd-serverを含む基本的なクラスタトポロジです。 OLTPアプリケーションに適しています。

-   [TiFlash展開トポロジ](/tiflash-deployment-topology.md)

    これは、最小限のクラスタトポロジとともにTiFlashを展開するためです。 TiFlashは列指向ストレージエンジンであり、徐々に標準のクラスタトポロジになります。リアルタイムHTAPアプリケーションに適しています。

-   [TiCDC展開トポロジ](/ticdc-deployment-topology.md)

    これは、最小限のクラスタトポロジとともにTiCDCを展開するためです。 TiCDCは、TiDB4.0で導入されたTiDBのインクリメンタルデータを複製するためのツールです。 TiDB、MySQL、MQなどの複数のダウンストリームプラットフォームをサポートします。 TiDB Binlogと比較して、TiCDCはレイテンシーが低く、ネイティブの高可用性を備えています。展開後、TiCDCと[`cdc cli`を使用してレプリケーションタスクを作成します](/ticdc/manage-ticdc.md)を起動します。

-   [TiDBBinlogデプロイメントトポロジ](/tidb-binlog-deployment-topology.md)

    これは、最小限のクラスタトポロジとともにTiDBBinlogを展開するためです。 TiDB Binlogは、インクリメンタルデータを複製するために広く使用されているコンポーネントです。ほぼリアルタイムのバックアップとレプリケーションを提供します。

-   [TiSparkデプロイメントトポロジ](/tispark-deployment-topology.md)

    これは、最小限のクラスタトポロジとともにTiSparkを展開するためです。 TiSparkは、TiDB /TiKV上でApacheSparkを実行して、OLAPクエリに応答するために構築されたコンポーネントです。現在、TiSparkに対するTiUPクラスターのサポートはまだ**実験的**段階です。

-   [ハイブリッド展開トポロジ](/hybrid-deployment-topology.md)

    これは、1台のマシンに複数のインスタンスをデプロイするためのものです。ディレクトリ、ポート、リソース比率、およびラベルの構成を追加する必要があります。

-   [地理分散型デプロイメントトポロジ](/geo-distributed-deployment-topology.md)

    このトポロジでは、2つの都市にある3つのデータセンターの一般的なアーキテクチャを例として取り上げます。地理的に分散された展開アーキテクチャと、注意が必要な主要な構成を紹介します。

> **ノート：**
>
> -   グローバルに有効である必要があるパラメーターについては、構成ファイルの`server_configs`セクションで対応するコンポーネントのこれらのパラメーターを構成します。
> -   特定のノードで有効になるはずのパラメーターについては、このノードの`config`でこれらのパラメーターを構成します。
> -   `.`を使用して、構成のサブカテゴリ（ `log.slow-threshold`など）を示します。その他の形式については、 [TiUP構成テンプレート](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml)を参照してください。
> -   パラメータの詳細については、 [TiDB `config.toml.example`](https://github.com/pingcap/tidb/blob/master/config/config.toml.example) 、および[TiKV `config.toml.example`](https://github.com/tikv/tikv/blob/master/etc/config-template.toml)を[TiFlash構成](/tiflash/tiflash-configuration.md)して[PD `config.toml.example`](https://github.com/pingcap/pd/blob/master/conf/config.toml) 。

## 手順4：展開コマンドを実行する {#step-4-execute-the-deployment-command}

> **ノート：**
>
> TiUPを使用してTiDBを展開する場合、セキュリティ認証に秘密鍵または対話型パスワードを使用できます。
>
> -   秘密鍵を使用する場合は、 `-i`または`--identity_file`を介して鍵のパスを指定できます。
> -   パスワードを使用する場合は、 `-p`フラグを追加して、パスワード操作ウィンドウに入ります。
> -   ターゲットマシンへのパスワードなしのログインが設定されている場合、認証は必要ありません。
>
> 一般に、TiUPは、次の例外を除いて、ターゲットマシン上の`topology.yaml`ファイルで指定されたユーザーとグループを作成します。
>
> -   `topology.yaml`で構成されたユーザー名は、ターゲットマシンにすでに存在します。
> -   コマンドラインで`--skip-create-user`オプションを使用して、ユーザーを作成する手順を明示的にスキップしました。

`deploy`コマンドを実行する前に、 `check`および`check --apply`コマンドを使用して、クラスタの潜在的なリスクを検出し、自動的に修復します。

{{< copyable "" >}}

```shell
tiup cluster check ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
tiup cluster check ./topology.yaml --apply --user root [-p] [-i /home/root/.ssh/gcp_rsa]
```

次に、 `deploy`コマンドを実行してTiDBクラスタをデプロイします。

{{< copyable "" >}}

```shell
tiup cluster deploy tidb-test v6.1.0 ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
```

上記のコマンドでは：

-   デプロイされたTiDBクラスタの名前は`tidb-test`です。
-   `tiup list tidb`を実行すると、サポートされている最新バージョンを確認できます。このドキュメントでは、例として`v6.1.0`を取り上げます。
-   初期化設定ファイルは`topology.yaml`です。
-   `--user root` ： `root`キーを使用してターゲットマシンにログインしてクラスタの展開を完了するか、 `ssh`および`sudo`の特権を持つ他のユーザーを使用して展開を完了することができます。
-   `[-i]`および`[-p]` ：オプション。パスワードなしでターゲットマシンへのログインを設定した場合、これらのパラメータは必要ありません。そうでない場合は、2つのパラメーターのいずれかを選択してください。 `[-i]`は、ターゲットマシンにアクセスできる`root`のユーザー（または`--user`で指定された他のユーザー）の秘密鍵です。 `[-p]`は、ユーザーパスワードをインタラクティブに入力するために使用されます。
-   ターゲットマシンで作成するユーザーグループ名を指定する必要がある場合は、 [この例](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml#L7)を参照してください。

出力ログの最後に、 ``Deployed cluster `tidb-test` successfully``が表示されます。これは、展開が成功したことを示します。

## ステップ5：TiUPによって管理されているクラスターを確認します {#step-5-check-the-clusters-managed-by-tiup}

{{< copyable "" >}}

```shell
tiup cluster list
```

TiUPは、複数のTiDBクラスターの管理をサポートしています。上記のコマンドは、名前、展開ユーザー、バージョン、秘密鍵情報など、現在TiUPによって管理されているすべてのクラスターの情報を出力します。

```log
Starting /home/tidb/.tiup/components/cluster/v1.5.0/cluster list
Name              User  Version        Path                                                        PrivateKey
----              ----  -------        ----                                                        ----------
tidb-test         tidb  v5.3.0      /home/tidb/.tiup/storage/cluster/clusters/tidb-test         /home/tidb/.tiup/storage/cluster/clusters/tidb-test/ssh/id_rsa
```

## 手順6：デプロイされたTiDBクラスタのステータスを確認する {#step-6-check-the-status-of-the-deployed-tidb-cluster}

たとえば、次のコマンドを実行して、 `tidb-test`のクラスタのステータスを確認します。

{{< copyable "" >}}

```shell
tiup cluster display tidb-test
```

期待される出力には、インスタンスID、ロール、ホスト、リスニングポート、ステータス（クラスタがまだ開始されていないため、ステータスは`Down` ）、およびディレクトリ情報が含まれ`inactive` 。

## ステップ7：TiDBクラスタを開始する {#step-7-start-a-tidb-cluster}

TiUPクラスタv1.9.0以降、新しい開始方法としてセーフスタートが導入されました。この方法を使用してデータベースを開始すると、データベースのセキュリティが向上します。この方法を使用することをお勧めします。

安全に起動すると、TiUPはTiDB rootユーザーのパスワードを自動的に生成し、コマンドラインインターフェイスでパスワードを返します。

> **ノート：**
>
> -   TiDBクラスタを安全に起動した後は、パスワードなしでrootユーザーを使用してTiDBにログインすることはできません。したがって、今後のログインのために、コマンド出力で返されたパスワードを記録する必要があります。
>
> -   パスワードは1回だけ生成されます。記録しない場合や忘れた場合は、 [`root`パスワードを忘れる](/user-account-management.md#forget-the-root-password)を参照してパスワードを変更してください。

方法1：安全なスタート

{{< copyable "" >}}

```shell
tiup cluster start tidb-test --init
```

出力が次の場合、開始は成功しています。

{{< copyable "" >}}

```shell
Started cluster `tidb-test` successfully.
The root password of TiDB database has been changed.
The new password is: 'y_+3Hwp=*AWz8971s6'.
Copy and record it to somewhere safe, it is only displayed once, and will not be stored.
The generated password can NOT be got again in future.
```

方法2：標準開始

{{< copyable "" >}}

```shell
tiup cluster start tidb-test
```

出力ログに``Started cluster `tidb-test` successfully``が含まれている場合、開始は成功しています。標準の起動後、パスワードなしでrootユーザーを使用してデータベースにログインできます。

## 手順8：TiDBクラスタの実行ステータスを確認する {#step-8-verify-the-running-status-of-the-tidb-cluster}

具体的な操作については、 [クラスタステータスの確認](/post-installation-check.md)を参照してください。

## 次は何ですか {#what-s-next}

TiDBクラスタと一緒に[TiFlash](/tiflash/tiflash-overview.md)をデプロイした場合は、次のドキュメントを参照してください。

-   [TiFlashを使用する](/tiflash/use-tiflash.md)
-   [TiFlashクラスターを管理する](/tiflash/maintain-tiflash.md)
-   [TiFlashアラートルールとソリューション](/tiflash/tiflash-alert-rules.md)
-   [TiFlashのトラブルシューティング](/tiflash/troubleshoot-tiflash.md)

TiDBクラスタと一緒に[TiCDC](/ticdc/ticdc-overview.md)をデプロイした場合は、次のドキュメントを参照してください。

-   [TiCDCクラスターおよびレプリケーションタスクの管理](/ticdc/manage-ticdc.md)
-   [TiCDCのトラブルシューティング](/ticdc/troubleshoot-ticdc.md)
