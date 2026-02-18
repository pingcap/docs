---
title: Deploy a TiDB Cluster Using TiUP
summary: TiUPを使用して TiDB クラスターを簡単にデプロイする方法を学びます。
---

# TiUPを使用して TiDBクラスタをデプロイ {#deploy-a-tidb-cluster-using-tiup}

このガイドでは、 [TiUP](https://github.com/pingcap/tiup)を使用して TiDB セルフマネージド クラスターを本番環境にデプロイする方法について説明します。

TiUPは、TiDB v4.0で導入されたクラスタ運用・保守ツールです。TiDBクラスタを管理するためのGo言語ベースのコンポーネントである[TiUPクラスター](https://github.com/pingcap/tiup/tree/master/components/cluster)提供します。TiUPクラスタを使用することで、 TiUPクラスタのデプロイ、起動、停止、破棄、スケーリング、アップグレード、TiDBクラスタパラメータの管理といった日常的なデータベース操作を簡単に実行できます。

TiUPは、TiDB、 TiFlash、TiCDC、および監視システムのデプロイもサポートしています。このガイドでは、さまざまなトポロジでTiDBクラスターをデプロイする方法を紹介します。

## ステップ1. 前提条件と事前チェック {#step-1-prerequisites-and-prechecks}

以下の文書を必ず読んでください。

-   [TiDB のソフトウェアおよびハードウェア要件](/hardware-and-software-requirements.md)
-   [TiDB環境とシステムコンフィグレーションのチェック](/check-before-deployment.md)

さらに、 [TiDBSecurityコンフィグレーションのベストプラクティス](/best-practices-for-security-configuration.md)を学習することをお勧めします。

## ステップ2. 制御マシンにTiUPをデプロイ {#step-2-deploy-tiup-on-the-control-machine}

TiUP をコントロール マシンに展開するには、オンライン展開とオフライン展開の 2 つの方法があります。

### TiUPをオンラインでデプロイ {#deploy-tiup-online}

> **注記：**
>
> TiUP環境がオフラインになった場合は、デプロイメントの[TiUPをオフラインでデプロイ](#deploy-tiup-offline)を参照してください。そうでない場合、 TiUPは正常に動作しません。

通常のユーザーアカウント（ユーザー`tidb`を例に挙げます）を使用して制御マシンにログインします。その後のTiUPのインストールとクラスタ管理は、ユーザー`tidb`で実行できます。

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

    `Updated successfully!`表示されている場合、 TiUPクラスターは正常に更新されています。

5.  TiUPクラスターの現在のバージョンを確認します。

    ```shell
    tiup --binary cluster
    ```

### TiUPをオフラインでデプロイ {#deploy-tiup-offline}

TiUPを使用して TiDB クラスターをオフラインでデプロイするには、このセクションで次の手順を実行します。

#### TiUPオフラインコンポーネントパッケージを準備する {#prepare-the-tiup-offline-component-package}

**方法1** ：以下のリンクから、対象のTiDBバージョンのオフラインバイナリパッケージ（TiUPオフラインパッケージを含む）をダウンロードします。サーバーとツールキットパッケージの両方をダウンロードする必要があります。ダウンロードを行うことで、 [プライバシーポリシー](https://www.pingcap.com/privacy-policy/) .に同意したものとみなされますのでご注意ください。

    https://download.pingcap.com/tidb-community-server-{version}-linux-{arch}.tar.gz

<!---->

    https://download.pingcap.com/tidb-community-toolkit-{version}-linux-{arch}.tar.gz

> **ヒント：**
>
> リンク内の`{version}` TiDBのバージョン番号を示し、 `{arch}`システムのアーキテクチャ（ `amd64`または`arm64`を示します。例えば、 `amd64`アーキテクチャの`v8.5.4`のダウンロードリンクは`https://download.pingcap.com/tidb-community-toolkit-v8.5.4-linux-amd64.tar.gz`です。

**方法2** ： `tiup mirror clone`を使用してオフラインコンポーネントパッケージを手動でパックします。詳細な手順は次のとおりです。

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

2.  TiUPを使用してミラーを引きます。

    1.  インターネットにアクセスできるマシンで必要なコンポーネントを取得します。

        ```shell
        tiup mirror clone tidb-community-server-${version}-linux-amd64 ${version} --os=linux --arch=amd64
        ```

        上記のコマンドは、現在のディレクトリに`tidb-community-server-${version}-linux-amd64`という名前のディレクトリを作成します。このディレクトリには、クラスターの起動に必要なコンポーネントパッケージが含まれます。

    2.  `tar`コマンドを使用してコンポーネントパッケージをパックし、そのパッケージを分離された環境内の制御マシンに送信します。

        ```bash
        tar czvf tidb-community-server-${version}-linux-amd64.tar.gz tidb-community-server-${version}-linux-amd64
        ```

        `tidb-community-server-${version}-linux-amd64.tar.gz`は独立したオフライン環境パッケージです。

3.  オフライン ミラーをカスタマイズするか、既存のオフライン ミラーの内容を調整します。

    既存のオフライン ミラーを調整する場合 (コンポーネントの新しいバージョンを追加するなど)、次の手順を実行します。

    1.  オフラインミラーをプルする際に、パラメータでコンポーネントやバージョン情報などの特定の情報を指定することで、不完全なオフラインミラーを取得できます。例えば、 TiUP v1.12.3とTiUP クラスタ v1.12.3のオフラインミラーのみを含むオフラインミラーをプルするには、以下のコマンドを実行します。

        ```bash
        tiup mirror clone tiup-custom-mirror-v1.12.3 --tiup v1.12.3 --cluster v1.12.3
        ```

        特定のプラットフォームのコンポーネントのみが必要な場合は、 `--os`または`--arch`パラメータを使用して指定できます。

    2.  「 TiUPを使用してミラーをプルする」の手順 2 を参照して、この不完全なオフライン ミラーを分離された環境内の制御マシンに送信します。

    3.  隔離環境内のコントロールマシン上の現在のオフラインミラーのパスを確認します。TiUPTiUPが最新バージョンの場合は、次のコマンドを実行して現在のミラーアドレスを取得できます。

        ```bash
        tiup mirror show
        ```

        上記のコマンドの出力で`show`コマンドが存在しないと表示される場合は、古いバージョンのTiUPを使用している可能性があります。その場合は、 `$HOME/.tiup/tiup.toml`から現在のミラーアドレスを取得できます。このミラーアドレスを記録してください。以降の手順では、 `${base_mirror}`このアドレスを参照するために使用されます。

    4.  不完全なオフライン ミラーを既存のオフライン ミラーにマージします。

        まず、現在のオフライン ミラー内の`keys`ディレクトリを`$HOME/.tiup`ディレクトリにコピーします。

        ```bash
        cp -r ${base_mirror}/keys $HOME/.tiup/
        ```

        次に、 TiUPコマンドを使用して、不完全なオフライン ミラーを使用中のミラーにマージします。

        ```bash
        tiup mirror merge tiup-custom-mirror-v1.12.3
        ```

    5.  上記の手順が完了したら、コマンド`tiup list`を実行して結果を確認します。このドキュメントの例では、コマンド`tiup list tiup`と`tiup list cluster`の両方の出力から、コマンド`v1.12.3`に対応するコンポーネントが利用可能であることがわかります。

#### オフラインTiUPコンポーネントをデプロイ {#deploy-the-offline-tiup-component}

パッケージをターゲット クラスターの制御マシンに送信した後、次のコマンドを実行してTiUPコンポーネントをインストールします。

```bash
tar xzvf tidb-community-server-${version}-linux-amd64.tar.gz && \
sh tidb-community-server-${version}-linux-amd64/local_install.sh && \
source /home/tidb/.bash_profile
```

`local_install.sh`スクリプトは自動的に`tiup mirror set tidb-community-server-${version}-linux-amd64`コマンドを実行し、現在のミラー アドレスを`tidb-community-server-${version}-linux-amd64`に設定します。

#### オフラインパッケージをマージする {#merge-offline-packages}

ダウンロードリンク経由でオフラインパッケージをダウンロードする場合は、サーバーパッケージとツールキットパッケージをオフラインミラーにマージする必要があります。1 `tiup mirror clone`を使用してオフラインコンポーネントパッケージを手動でパッケージ化する場合は、この手順を省略できます。

オフライン ツールキット パッケージをサーバーパッケージ ディレクトリにマージするには、次のコマンドを実行します。

```bash
tar xf tidb-community-toolkit-${version}-linux-amd64.tar.gz
ls -ld tidb-community-server-${version}-linux-amd64 tidb-community-toolkit-${version}-linux-amd64
cd tidb-community-server-${version}-linux-amd64/
cp -rp keys ~/.tiup/
tiup mirror merge ../tidb-community-toolkit-${version}-linux-amd64
```

ミラーを別のディレクトリに切り替えるには、 `tiup mirror set <mirror-dir>`コマンドを実行します。ミラーをオンライン環境に切り替えるには、 `tiup mirror set https://tiup-mirrors.pingcap.com`コマンドを実行します。

## ステップ3. クラスタトポロジファイルを初期化する {#step-3-initialize-the-cluster-topology-file}

次のコマンドを実行して、クラスター トポロジ ファイルを作成します。

```shell
tiup cluster template > topology.yaml
```

次の 2 つの一般的なシナリオでは、コマンドを実行して推奨されるトポロジ テンプレートを生成できます。

-   ハイブリッド展開の場合：複数のインスタンスが1台のマシンに展開されます。詳細については、 [ハイブリッド展開トポロジ](/hybrid-deployment-topology.md)参照してください。

    ```shell
    tiup cluster template --full > topology.yaml
    ```

-   地理的に分散したデプロイメントの場合：TiDB クラスターは地理的に分散したデータセンターにデプロイされます。詳細については、 [地理的に分散した展開トポロジ](/geo-distributed-deployment-topology.md)参照してください。

    ```shell
    tiup cluster template --multi-dc > topology.yaml
    ```

`vi topology.yaml`実行して構成ファイルの内容を確認します。

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

以下の例は、6つの一般的なシナリオを網羅しています。トポロジの説明と、対応するリンクにあるテンプレートに従って、設定ファイル（名前は`topology.yaml` ）を変更する必要があります。その他のシナリオについては、設定テンプレートを適宜編集してください。

| 応用                                             | コンフィグレーションタスク                                                  | コンフィグレーションファイルテンプレート                                                                                                                                                                                                                       | トポロジの説明                                                                                                         |
| :--------------------------------------------- | :------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------- |
| OLTP                                           | [最小限のトポロジをデプロイ](/minimal-deployment-topology.md)               | [シンプルで最小限の構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-mini.yaml) <br/> [完全な最小限の構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-mini.yaml)                                 | これは、tidb-server、tikv-server、pd-server を含む基本的なクラスター トポロジです。                                                      |
| HTAP                                           | [TiFlashトポロジをデプロイ](/tiflash-deployment-topology.md)            | [シンプルなTiFlash構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-tiflash.yaml) <br/> [完全なTiFlash構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-tiflash.yaml)                     | これは、最小限のクラスタートポロジーに沿ってTiFlashを導入するものです。TiFlashは列指向のstorageエンジンであり、徐々に標準的なクラスタートポロジーになりつつあります。                   |
| [TiCDC](/ticdc/ticdc-overview.md)を使用して増分データを複製 | [TiCDCトポロジをデプロイ](/ticdc-deployment-topology.md)                | [シンプルな TiCDC 構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-cdc.yaml) <br/> [完全な TiCDC 構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-cdc.yaml)                             | これは、最小限のクラスタトポロジに沿ってTiCDCをデプロイするためのものです。TiCDCは、TiDB、MySQL、Kafka、MQ、storageサービスなど、複数のダウンストリームプラットフォームをサポートしています。 |
| 1台のマシンに複数のインスタンスをデプロイ                          | [ハイブリッドトポロジをデプロイ](/hybrid-deployment-topology.md)              | [ハイブリッド展開用のシンプルな構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-multi-instance.yaml) <br/> [ハイブリッド展開用の完全な構成テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-multi-instance.yaml) | デプロイメント トポロジは、ディレクトリ、ポート、リソース比率、およびラベルの追加構成を追加する必要がある場合にも適用されます。                                                |
| データセンター全体に TiDB クラスターをデプロイ                     | [地理的に分散した展開トポロジをデプロイ](/geo-distributed-deployment-topology.md) | [地理的に分散した展開用のコンフィグレーションテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/geo-redundancy-deployment.yaml)                                                                                                                | このトポロジーでは、2つの都市に3つのデータセンターを配置するという典型的なアーキテクチャを例に挙げ、地理的に分散したデプロイメントアーキテクチャと、注意が必要な主要な構成について説明します。                |

> **注記：**
>
> -   グローバルに有効にする必要があるパラメータについては、構成ファイルの`server_configs`セクションで対応するコンポーネントのこれらのパラメータを構成します。
> -   特定のノードで有効にするパラメータについては、このノードの`config`でこれらのパラメータを設定します。
> -   `.`構成のサブカテゴリ（例： `log.slow-threshold` ）を示します。その他の形式については、 [TiUP構成テンプレート](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml)参照してください。
> -   ターゲットマシンに作成するユーザーグループ名を指定する必要がある場合は、 [この例](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml#L7)参照してください。

詳細な構成の説明については、次の構成例を参照してください。

-   [TiDB `config.toml.example`](https://github.com/pingcap/tidb/blob/release-8.5/pkg/config/config.toml.example)
-   [TiKV `config.toml.example`](https://github.com/tikv/tikv/blob/release-8.5/etc/config-template.toml)
-   [PD `config.toml.example`](https://github.com/tikv/pd/blob/release-8.5/conf/config.toml)
-   [TiFlash `config.toml.example`](https://github.com/pingcap/tiflash/blob/release-8.5/etc/config-template.toml)

## ステップ4. デプロイメントコマンドを実行する {#step-4-run-the-deployment-command}

> **注記：**
>
> TiUP ( `--user`で指定) 経由でクラスターをデプロイするときに、キーまたはクロスパスワードを使用して初期化に使用するユーザーを安全に認証できます。
>
> -   秘密鍵を使用する場合は、 `-i`または`--identity_file`を通じて鍵のパスを指定します。
> -   パスワードを使用する場合は、パスワード対話ウィンドウに入るために`-p`フラグを追加します。
> -   ターゲット マシンへのパスワードなしのログインが設定されている場合は、認証は必要ありません。
>
> 一般に、 TiUPが実際にプロセスを実行するために使用するユーザーとグループ ( `topology.yaml`で指定され、デフォルト値は`tidb` ) は、次の例外を除き、ターゲット マシン上に自動的に作成されます。
>
> -   `topology.yaml`で設定されたユーザー名は、対象マシンに既に存在します。
> -   コマンドラインで`--skip-create-user`オプションを使用して、ユーザーの作成手順を明示的にスキップしました。
>
> `topology.yaml`で合意したユーザーとグループが自動的に作成されるかどうかに関わらず、 TiUPは各マシン上でSSHキーのペアを自動的に生成し、そのユーザーに対してシークレットフリーのログインを設定します。このユーザーとSSHキーは、以降のすべての操作におけるマシンの管理に使用されます。一方、初期化に使用されたユーザー名とパスワードは、デプロイメント完了後は使用されません。

`deploy`コマンドを実行する前に、 `check`コマンドと`check --apply`コマンドを使用して、クラスター内の潜在的なリスクを検出し、自動的に修復します。

1.  潜在的なリスクを確認してください:

    ```shell
    tiup cluster check ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

2.  自動修復を有効にする:

    ```shell
    tiup cluster check ./topology.yaml --apply --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

3.  TiDB クラスターをデプロイ。

    ```shell
    tiup cluster deploy tidb-test v8.5.4 ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

上記の`tiup cluster deploy`コマンドでは:

-   `tidb-test`は、デプロイする TiDB クラスターの名前です。
-   `v8.5.4`はデプロイする TiDB クラスタのバージョンです。2 `tiup list tidb`実行すると、サポートされている最新バージョンを確認できます。
-   `topology.yaml`は初期化構成ファイルです。
-   `--user root` 、クラスタのデプロイメントを完了するために、 `root`ユーザーとしてターゲットマシンにログインすることを示します。4 `root`ユーザーは、ターゲットマシンに対して`ssh`と`sudo`権限を持つことが想定されています。または、 `ssh`と`sudo`権限を持つ他のユーザーを使用してデプロイメントを完了することもできます。
-   `[-i]`と`[-p]`オプションです。ターゲットマシンへのログインをパスワードなしで設定している場合、これらのパラメータは不要です。そうでない場合は、2つのパラメータのいずれかを選択してください。4 `[-i]` 、ターゲットマシンにアクセスできるルートユーザー（または`--user`で指定された他のユーザー）の秘密鍵です。8 `[-p]` 、ユーザーパスワードを対話的に入力するために使用されます。

出力ログの最後に``Deployed cluster `tidb-test` successfully``表示されます。これは、デプロイメントが成功したことを示します。

## ステップ5. TiUPによって管理されているクラスターを確認する {#step-5-check-the-clusters-managed-by-tiup}

```shell
tiup cluster list
```

TiUP は複数の TiDB クラスタの管理をサポートしています。上記のコマンドは、クラスタ名、デプロイメントユーザー、バージョン、秘密鍵情報など、現在TiUPによって管理されているすべてのクラスタの情報を出力します。

## ステップ6. デプロイされたTiDBクラスタのステータスを確認する {#step-6-check-the-status-of-the-deployed-tidb-cluster}

たとえば、 `tidb-test`クラスターのステータスを確認するには、次のコマンドを実行します。

```shell
tiup cluster display tidb-test
```

予想される出力には`inactive`インスタンス ID、ロール、ホスト、リスニング ポート、ステータス (クラスターはまだ起動されていないため、ステータスは`Down`です)、およびディレクトリ情報が含まれます。

## ステップ7. TiDBクラスターを起動する {#step-7-start-a-tidb-cluster}

TiUPクラスタv1.9.0以降、新しい起動方法としてセーフスタートが導入されました。この方法でデータベースを起動すると、データベースのセキュリティが向上します。この方法を使用することをお勧めします。

安全に起動すると、 TiUP はTiDB ルート ユーザーのパスワードを自動的に生成し、コマンド ライン インターフェイスでそのパスワードを返します。

> **注記：**
>
> -   TiDBクラスタを安全に起動した後、パスワードなしでrootユーザーを使用してTiDBにログインすることはできません。そのため、今後のログインのために、コマンド出力で返されたパスワードを記録しておく必要があります。
> -   パスワードは一度だけ生成されます。記録していない場合、または忘れた場合は、 [`root`パスワードを忘れた](/user-account-management.md#forget-the-root-password)を参照してパスワードを変更してください。

方法1：安全なスタート

```shell
tiup cluster start tidb-test --init
```

出力が次のようであれば、起動は成功です。

```shell
Started cluster `tidb-test` successfully.
The root password of TiDB database has been changed.
The new password is: 'y_+3Hwp=*AWz8971s6'.
Copy and record it to somewhere safe, it is only displayed once, and will not be stored.
The generated password can NOT be got again in future.
```

方法2: 標準スタート

```shell
tiup cluster start tidb-test
```

出力ログに``Started cluster `tidb-test` successfully``含まれていれば、起動は成功です。標準起動後、パスワードなしでrootユーザーを使用してデータベースにログインできます。

## ステップ8. TiDBクラスタの実行状態を確認する {#step-8-verify-the-running-status-of-the-tidb-cluster}

```shell
tiup cluster display tidb-test
```

出力ログにステータス`Up`が表示されている場合、クラスターは正常に実行されています。

## 参照 {#see-also}

TiDB クラスターとともに[TiFlash](/tiflash/tiflash-overview.md)デプロイした場合は、次のドキュメントを参照してください。

-   [TiFlashを使用する](/tiflash/tiflash-overview.md#use-tiflash)
-   [TiFlashクラスタを管理](/tiflash/maintain-tiflash.md)
-   [TiFlashアラートのルールと解決策](/tiflash/tiflash-alert-rules.md)
-   [TiFlashのトラブルシューティング](/tiflash/troubleshoot-tiflash.md)

TiDB クラスターとともに[TiCDC](/ticdc/ticdc-overview.md)デプロイした場合は、データのストリーミングについては次のドキュメントを参照してください。

-   [チェンジフィードの概要](/ticdc/ticdc-changefeed-overview.md)
-   [Changefeed を管理する](/ticdc/ticdc-manage-changefeed.md)
-   [TiCDC のトラブルシューティング](/ticdc/troubleshoot-ticdc.md)
-   [TiCDC よくある質問](/ticdc/ticdc-faq.md)

オンライン サービスを中断せずに TiDB クラスターをスケール アウトまたはスケール インする場合は、 [TiUPを使用して TiDBクラスタをスケールする](/scale-tidb-using-tiup.md)参照してください。
