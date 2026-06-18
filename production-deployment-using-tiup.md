---
title: Deploy a TiDB Cluster Using TiUP
summary: TiUPを使用してTiDBクラスタを簡単にデプロイする方法を学びましょう。
---

# TiUPを使用してTiDBクラスタをデプロイ {#deploy-a-tidb-cluster-using-tiup}

このガイドでは、本番環境で[TiUP](https://github.com/pingcap/tiup)を使用してTiDBセルフマネージドクラスタをデプロイする方法について説明します。

TiUPは、TiDB v4.0で導入されたクラスタ運用・保守ツールです。TiUP [TiUPクラスター](https://github.com/pingcap/tiup/tree/master/components/cluster)は、TiDBクラスタを管理するためのGolangベースのコンポーネントです。TiUPクラスタを使用することで、 TiUPクラスタのデプロイ、起動、停止、削除、スケーリング、アップグレード、およびTiDBクラスタパラメータの管理といった、日常的なデータベース操作を容易に実行できます。

TiUPは、TiDB、 TiFlash、TiCDC、および監視システムのデプロイもサポートしています。このガイドでは、さまざまなトポロジーでTiDBクラスタをデプロイする方法について説明します。

## ステップ1．前提条件と事前確認 {#step-1-prerequisites-and-prechecks}

以下の文書を必ずお読みください。

-   [TiDBのソフトウェアおよびハードウェア要件](/hardware-and-software-requirements.md)
-   [TiDB環境およびシステムコンフィグレーションチェック](/check-before-deployment.md)

さらに、 [TiDBセキュリティ設定のベストプラクティス](/best-practices-for-security-configuration.md)学習することをお勧めします。

## ステップ2. 制御機にTiUPをデプロイ {#step-2-deploy-tiup-on-the-control-machine}

TiUPを制御マシンに展開するには、オンライン展開とオフライン展開の2つの方法があります。

### TiUPをオンラインでデプロイ {#deploy-tiup-online}

> **注記：**
>
> TiUP環境がオフラインに切り替わった場合は、 [TiUPをオフラインでデプロイ](#deploy-tiup-offline)デプロイ」の展開を参照してください。そうしないと、 TiUP が正常に動作しません。

通常のユーザーアカウントを使用して制御マシンにログインします（例として`tidb`ユーザーを使用します）。その後のTiUPのインストールとクラスタ管理は`tidb`ユーザーが実行できます。

1.  以下のコマンドを実行してTiUPをインストールしてください。

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2.  TiUP環境変数を設定する：

    1.  グローバル環境変数を再宣言します。

        ```shell
        source .bash_profile
        ```

    2.  TiUPがインストールされているかどうかを確認してください。

        ```shell
        which tiup
        ```

3.  TiUPクラスタコンポーネントをインストールします。

    ```shell
    tiup cluster
    ```

4.  TiUPが既にインストールされている場合は、 TiUPクラスタコンポーネントを最新バージョンにアップデートしてください。

    ```shell
    tiup update --self && tiup update cluster
    ```

    `Updated successfully!`が表示された場合、 TiUPクラスタは正常に更新されています。

5.  TiUPクラスターの現在のバージョンを確認してください。

    ```shell
    tiup --binary cluster
    ```

### TiUPをオフラインでデプロイ {#deploy-tiup-offline}

TiUPを使用してTiDBクラスタをオフラインでデプロイするには、このセクションで以下の手順を実行します。

#### TiUPオフラインコンポーネントパッケージを準備する {#prepare-the-tiup-offline-component-package}

**方法 1** : 以下のリンクを使用して、対象の TiDB バージョンのオフライン バイナリ パッケージ (TiUPオフライン パッケージを含む) をダウンロードします。サーバーとツールキット パッケージの両方をダウンロードする必要があります。ダウンロードすると[プライバシーポリシー](https://www.pingcap.com/privacy-policy/)次の規約に同意したことになります。 。

    https://download.pingcap.com/tidb-community-server-{version}-linux-{arch}.tar.gz

<!---->

    https://download.pingcap.com/tidb-community-toolkit-{version}-linux-{arch}.tar.gz

> **ヒント：**
>
> リンク内の`{version}`は TiDB のバージョン番号を示し、 `{arch}`システムのアーキテクチャを示し、 `amd64`または`arm64`のいずれかになります。たとえば、 `v8.5.4`アーキテクチャの`amd64`のダウンロードリンクは`https://download.pingcap.com/tidb-community-toolkit-v8.5.4-linux-amd64.tar.gz`です。

**方法2** ： `tiup mirror clone`を使用してオフラインコンポーネントパッケージを手動でパックします。詳細な手順は次のとおりです。

1.  TiUPパッケージマネージャーをオンラインでインストールしてください。

    1.  TiUPツールをインストールしてください。

        ```shell
        curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
        ```

    2.  グローバル環境変数を再宣言します。

        ```shell
        source .bash_profile
        ```

    3.  TiUPがインストールされているかどうかを確認してください。

        ```shell
        which tiup
        ```

2.  TiUPを使ってミラーを引き出します。

    1.  インターネットに接続できるマシンで、必要なコンポーネントを取り出してください。

        ```shell
        tiup mirror clone tidb-community-server-${version}-linux-amd64 ${version} --os=linux --arch=amd64
        ```

        上記のコマンドは、現在のディレクトリに`tidb-community-server-${version}-linux-amd64`という名前のディレクトリを作成します。このディレクトリには、クラスターの起動に必要なコンポーネントパッケージが含まれています。

    2.  `tar`コマンドを使用してコンポーネントパッケージを梱包し、隔離された環境にある制御マシンにパッケージを送信します。

        ```bash
        tar czvf tidb-community-server-${version}-linux-amd64.tar.gz tidb-community-server-${version}-linux-amd64
        ```

        `tidb-community-server-${version}-linux-amd64.tar.gz`は独立したオフライン環境パッケージです。

3.  オフラインミラーをカスタマイズするか、既存のオフラインミラーの内容を調整します。

    既存のオフラインミラーを調整する場合（コンポーネントの新しいバージョンを追加する場合など）、以下の手順に従ってください。

    1.  オフラインミラーを取得する際、コンポーネントやバージョン情報などの特定の情報をパラメータで指定することで、不完全なオフラインミラーを取得できます。たとえば、次のコマンドを実行すると、 TiUP v1.12.3 とTiUP クラスタ v1.12.3 のオフラインミラーのみを含むオフラインミラーを取得できます。

        ```bash
        tiup mirror clone tiup-custom-mirror-v1.12.3 --tiup v1.12.3 --cluster v1.12.3
        ```

        特定のプラットフォーム用のコンポーネントのみが必要な場合は、 `--os`または`--arch`パラメーターを使用して指定できます。

    2.  「 TiUPを使用してミラーを引き出す」の手順2を参照し、この不完全なオフラインミラーを隔離された環境にある制御機に送信します。

    3.  隔離された環境にある制御マシン上で、現在のオフラインミラーのパスを確認してください。TiUPツールが最新バージョンであれば、以下のコマンドを実行することで現在のミラーアドレスを取得できます。

        ```bash
        tiup mirror show
        ```

        上記のコマンドの出力で`show`コマンドが存在しないと表示される場合は、 TiUPの古いバージョンを使用している可能性があります。この場合、 `$HOME/.tiup/tiup.toml`から現在のミラー アドレスを取得できます。このミラー アドレスを記録してください。以降の手順では、 `${base_mirror}`このアドレスを参照するために使用されます。

    4.  不完全なオフラインミラーを既存のオフラインミラーに統合する：

        まず、現在のオフラインミラーにある`keys`ディレクトリを`$HOME/.tiup`ディレクトリにコピーします。

        ```bash
        cp -r ${base_mirror}/keys $HOME/.tiup/
        ```

        次に、 TiUPコマンドを使用して、不完全なオフラインミラーを現在使用中のミラーに統合します。

        ```bash
        tiup mirror merge tiup-custom-mirror-v1.12.3
        ```

    5.  上記の手順が完了したら、 `tiup list`コマンドを実行して結果を確認します。このドキュメントの例では、 `tiup list tiup`と`tiup list cluster`の両方の出力から`v1.12.3`の対応するコンポーネントが利用可能であることが示されています。

#### オフラインのTiUPコンポーネントをデプロイ {#deploy-the-offline-tiup-component}

対象クラスタの制御マシンにパッケージを送信した後、以下のコマンドを実行してTiUPコンポーネントをインストールします。

```bash
tar xzvf tidb-community-server-${version}-linux-amd64.tar.gz && \
sh tidb-community-server-${version}-linux-amd64/local_install.sh && \
source /home/tidb/.bash_profile
```

`local_install.sh`スクリプトは、 `tiup mirror set tidb-community-server-${version}-linux-amd64`コマンドを自動的に実行して、現在のミラー アドレスを`tidb-community-server-${version}-linux-amd64`に設定します。

#### オフラインパッケージをマージする {#merge-offline-packages}

ダウンロードリンクからオフラインパッケージをダウンロードする場合は、サーバーパッケージとツールキットパッケージをオフラインミラーに統合する必要があります。 `tiup mirror clone`コマンドを使用してオフラインコンポーネントパッケージを手動でパッケージ化する場合は、この手順をスキップできます。

オフラインツールキットパッケージをサーバーパッケージディレクトリにマージするには、以下のコマンドを実行してください。

```bash
tar xf tidb-community-toolkit-${version}-linux-amd64.tar.gz
ls -ld tidb-community-server-${version}-linux-amd64 tidb-community-toolkit-${version}-linux-amd64
cd tidb-community-server-${version}-linux-amd64/
cp -rp keys ~/.tiup/
tiup mirror merge ../tidb-community-toolkit-${version}-linux-amd64
```

ミラーを別のディレクトリに切り替えるには、 `tiup mirror set <mirror-dir>`コマンドを実行します。ミラーをオンライン環境に切り替えるには、 `tiup mirror set https://tiup-mirrors.pingcap.com`コマンドを実行します。

## ステップ3. クラスタトポロジーファイルを初期化する {#step-3-initialize-the-cluster-topology-file}

クラスタトポロジーファイルを作成するには、次のコマンドを実行します。

```shell
tiup cluster template > topology.yaml
```

以下の2つの一般的なシナリオでは、コマンドを実行することで推奨トポロジーテンプレートを生成できます。

-   ハイブリッド デプロイメントの場合: 複数のインスタンスが 1 台のマシンにデプロイされます。詳細は[ハイブリッド展開トポロジー](/hybrid-deployment-topology.md)を参照。

    ```shell
    tiup cluster template --full > topology.yaml
    ```

-   地理的に分散した展開の場合: TiDB クラスターは地理的に分散したデータ センターに展開されます。詳細については、[地理的に分散した展開トポロジー](/geo-distributed-deployment-topology.md)を参照してください。

    ```shell
    tiup cluster template --multi-dc > topology.yaml
    ```

`vi topology.yaml`を実行して、設定ファイルの内容を確認してください。

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

以下の例では、6つの一般的なシナリオを取り上げています。対応するリンク先のトポロジーの説明とテンプレートに従って、構成ファイル（ `topology.yaml`という名前）を変更する必要があります。その他のシナリオについては、構成テンプレートを適切に編集してください。

| 応用                                               | コンフィグレーションタスク                                                        | コンフィグレーションファイルテンプレート                                                                                                                                                                                                                       | トポロジーの説明                                                                                                         |
| :----------------------------------------------- | :------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------- |
| OLTP                                             | [最小限のトポロジーをデプロイ](/minimal-deployment-topology.md)                    | [シンプルな最小限の構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-mini.yaml) <br/> [完全な最小構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-mini.yaml)                                   | これは、tidb-server、tikv-server、およびpd-serverを含む基本的なクラスタトポロジーです。                                                      |
| HTAP                                             | [TiFlashトポロジーをデプロイ](/tiflash-deployment-topology.md)                 | [シンプルなTiFlash設定テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-tiflash.yaml) <br/> [TiFlashの完全な構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-tiflash.yaml)                    | これは、最小限のクラスタトポロジーとともにTiFlashをデプロイするためのものです。TiFlashはカラム型ストレージエンジンであり、徐々に標準的なクラスタトポロジーへと進化していきます。                |
| [TiCDC](/ticdc/ticdc-overview.md)を使用して増分データを複製する | [TiCDCトポロジーをデプロイ](/ticdc-deployment-topology.md)                     | [シンプルなTiCDC構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-cdc.yaml) <br/> [TiCDC構成テンプレート全体](https://github.com/pingcap/docs/blob/master/config-templates/complex-cdc.yaml)                                  | これは、最小限のクラスタトポロジーとともにTiCDCをデプロイするためのものです。TiCDCは、TiDB、MySQL、Kafka、MQ、ストレージサービスなど、複数のダウンストリームプラットフォームをサポートしています。 |
| 1台のマシンに複数のインスタンスをデプロイ                            | [ハイブリッドトポロジーをデプロイ](/hybrid-deployment-topology.md)                   | [ハイブリッド展開用のシンプルな構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-multi-instance.yaml) <br/> [ハイブリッド展開用の完全な構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-multi-instance.yaml) | ディレクトリ、ポート、リソース比率、ラベルなどの追加設定が必要な場合にも、デプロイメントトポロジーが適用されます。                                                        |
| TiDBクラスターをデータセンター全体にデプロイ                         | [地理的に分散したデプロイメントトポロジーをデプロイ](/geo-distributed-deployment-topology.md) | [地理的に分散したデプロイメントのためのコンフィグレーションテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/geo-redundancy-deployment.yaml)                                                                                                         | このトポロジーは、2つの都市に3つのデータセンターを配置する典型的なアーキテクチャを例として取り上げています。地理的に分散したデプロイメントアーキテクチャと、注意すべき重要な構成について解説します。              |

> **注記：**
>
> -   グローバルに適用されるべきパラメータについては、設定ファイルの`server_configs`セクションで、対応するコンポーネントのこれらのパラメータを設定します。
> -   特定のノードで有効にするパラメータについては、このノードの`config`でこれらのパラメータを設定します。
> -   `.`を使用して、構成のサブカテゴリを指定します (例: `log.slow-threshold` 。その他の形式については、 [TiUP構成テンプレート](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml)参照してください。
> -   対象マシン上に作成するユーザーグループ名を指定する必要がある場合は、 [この例](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml#L7)参照してください。

設定の詳細については、以下の設定例を参照してください。

-   [TiDB `config.toml.example`](https://github.com/pingcap/tidb/blob/release-8.5/pkg/config/config.toml.example)
-   [TiKV `config.toml.example`](https://github.com/tikv/tikv/blob/release-8.5/etc/config-template.toml)
-   [PD `config.toml.example`](https://github.com/tikv/pd/blob/release-8.5/conf/config.toml)
-   [TiFlash `config.toml.example`](https://github.com/pingcap/tiflash/blob/release-8.5/etc/config-template.toml)

## ステップ4. デプロイコマンドを実行します {#step-4-run-the-deployment-command}

> **注記：**
>
> TiUP ( `--user`で指定) を介してクラスタをデプロイする際に初期化に使用するユーザーを、キーまたはクロスパスワードのいずれかを使用して安全に認証できます。
>
> -   秘密鍵を使用する場合は、 `-i`または`--identity_file`を使用して鍵のパスを指定します。
> -   パスワードを使用する場合は、 `-p`フラグを追加して、パスワード入力ウィンドウを開きます。
> -   対象マシンへのパスワード不要ログインが設定されている場合、認証は不要です。
>
> 一般的に、 TiUPが実際にプロセスを実行するために使用するユーザーとグループ ( `topology.yaml`で指定され、デフォルト値は`tidb`です) は、次の例外を除き、ターゲット マシン上に自動的に作成されます。
>
> -   `topology.yaml`で設定されたユーザー名は、既にターゲットマシン上に存在します。
> -   コマンドラインで`--skip-create-user`オプションを使用して、ユーザーを作成する手順を明示的にスキップしました。
>
> `topology.yaml`で合意されたユーザーとグループが自動的に作成されるかどうかに関わらず、 TiUPは自動的にSSHキーのペアを生成し、各マシン上でそのユーザーに対してシークレットフリーのログインを設定します。このユーザーとSSHキーは、以降のすべての操作でマシンを管理するために使用され、初期化に使用されたユーザーとパスワードは、デプロイ完了後は使用されなくなります。

`deploy`コマンドを実行する前に、 `check`コマンドと`check --apply`コマンドを使用して、クラスター内の潜在的なリスクを検出し、自動的に修復してください。

1.  潜在的なリスクを確認してください。

    ```shell
    tiup cluster check ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

2.  自動修復を有効にする：

    ```shell
    tiup cluster check ./topology.yaml --apply --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

3.  TiDBクラスタをデプロイ：

    ```shell
    tiup cluster deploy tidb-test v8.5.4 ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

上記の`tiup cluster deploy`コマンドでは、次のようになります。

-   `tidb-test`は、デプロイされる TiDB クラスタの名前です。
-   `v8.5.4`は、デプロイする TiDB クラスタのバージョンです。 `tiup list tidb`を実行すると、サポートされている最新バージョンを確認できます。
-   `topology.yaml`は初期化設定ファイルです。
-   `--user root` `root`ユーザーとしてターゲット マシンにログインし、クラスタのデプロイを完了することを示します。 `root`ユーザーは、ターゲット マシンに対して`ssh`および`sudo`の権限を持っている必要があります。あるいは、 `ssh`および`sudo`の権限を持つ他のユーザーを使用してデプロイを完了することもできます。
-   `[-i]`と`[-p]`はオプションです。ターゲット マシンへのログインをパスワードなしで設定している場合は、これらのパラメーターは不要です。そうでない場合は、2 つのパラメーターのいずれかを選択してください。 `[-i]`は、ターゲット マシンへのアクセス権を持つルート ユーザー (または`--user`で指定された他のユーザー) の秘密鍵です。 `[-p]`は、ユーザー パスワードを対話的に入力するために使用されます。

出力ログの最後に``Deployed cluster `tidb-test` successfully``と表示されます。これは、デプロイが成功したことを示しています。

## ステップ5. TiUPによって管理されているクラスターを確認します。 {#step-5-check-the-clusters-managed-by-tiup}

```shell
tiup cluster list
```

TiUPは複数のTiDBクラスタの管理をサポートしています。上記のコマンドは、クラスタ名、デプロイメントユーザー、バージョン、秘密鍵情報など、現在TiUPによって管理されているすべてのクラスタの情報を出力します。

## ステップ6. デプロイされたTiDBクラスタの状態を確認します。 {#step-6-check-the-status-of-the-deployed-tidb-cluster}

例えば、次のコマンドを実行して、 `tidb-test`クラスターの状態を確認します。

```shell
tiup cluster display tidb-test
```

期待される出力には、インスタンス ID、ロール、ホスト、リスニング ポート、ステータス (クラスターがまだ起動していないため、ステータスは`Down` / `inactive`です)、およびディレクトリ情報が含まれます。

## ステップ7. TiDBクラスタを起動する {#step-7-start-a-tidb-cluster}

TiUP cluster v1.9.0以降、新しい起動方法としてセーフスタートが導入されました。この方法でデータベースを起動すると、データベースのセキュリティが向上します。この方法を使用することをお勧めします。

安全な起動後、 TiUPはTiDBのrootユーザーのパスワードを自動的に生成し、コマンドラインインターフェースにそのパスワードを表示します。

> **注記：**
>
> -   TiDBクラスタの安全な起動後、パスワードなしでrootユーザーとしてTiDBにログインすることはできません。そのため、今後のログインのために、コマンド出力に表示されるパスワードを記録しておく必要があります。
> -   パスワードは 1 回だけ生成されます。記録していない場合、または忘れた場合は、 [`root`パスワードを忘れる](/user-account-management.md#forget-the-root-password)を参照してパスワードを変更してください。

方法1：セーフスタート

```shell
tiup cluster start tidb-test --init
```

出力が以下のようであれば、起動は成功です。

```shell
Started cluster `tidb-test` successfully.
The root password of TiDB database has been changed.
The new password is: 'y_+3Hwp=*AWz8971s6'.
Copy and record it to somewhere safe, it is only displayed once, and will not be stored.
The generated password can NOT be got again in future.
```

方法2：標準的な開始

```shell
tiup cluster start tidb-test
```

出力ログに``Started cluster `tidb-test` successfully``が含まれていれば、起動は成功です。標準起動後、パスワードなしでrootユーザーを使用してデータベースにログインできます。

## ステップ8．TiDBクラスタの実行状態を確認する {#step-8-verify-the-running-status-of-the-tidb-cluster}

```shell
tiup cluster display tidb-test
```

出力ログに`Up`ステータスが表示されている場合、クラスターは正常に動作しています。

## 関連項目 {#see-also}

TiDBクラスタとともに[TiFlash](/tiflash/tiflash-overview.md)をデプロイしている場合は、以下のドキュメントを参照してください。

-   [TiFlashを使用する](/tiflash/tiflash-overview.md#use-tiflash)
-   [TiFlashクラスタの管理](/tiflash/maintain-tiflash.md)
-   [TiFlashアラートのルールと解決策](/tiflash/tiflash-alert-rules.md)
-   [TiFlashのトラブルシューティング](/tiflash/troubleshoot-tiflash.md)

TiDBクラスタとともに[TiCDC](/ticdc/ticdc-overview.md)をデプロイしている場合は、データのストリーミング方法について以下のドキュメントを参照してください。

-   [変更フィードの概要](/ticdc/ticdc-changefeed-overview.md)
-   [変更フィードを管理する](/ticdc/ticdc-manage-changefeed.md)
-   [TiCDCのトラブルシューティング](/ticdc/troubleshoot-ticdc.md)
-   [TiCDCに関するよくある質問](/ticdc/ticdc-faq.md)

オンライン サービスを中断せずに TiDB クラスターをスケールアウトまたはスケールインしたい場合は、 [TiUPを使用してTiDBクラスタをスケーリングする](/scale-tidb-using-tiup.md)参照してください。

## 関連リソース {#related-resources}

<RelatedResources>
  <ResourceCard title="TiDB Admin Lab 1: Deploying a TiDB Cluster Using TiUP" type="lab" link="https://labs.tidb.io/labs/dba_303_lab_ff0" imgSrc="https://lab-static.pingcap.com/quick-demo/dba_303_ch01_en.png" duration="60 mins" />
</RelatedResources>
