---
title: Deploy a DM Cluster Offline Using TiUP
summary: Introduce how to deploy a DM cluster offline using TiUP.
---

# TiUPを使用してオフラインで DMクラスタをデプロイ {#deploy-a-dm-cluster-offline-using-tiup}

このドキュメントでは、 TiUPを使用して DM クラスターをオフラインで展開する方法について説明します。

## 手順 1: TiUPオフラインコンポーネントパッケージを準備する {#step-1-prepare-the-tiup-offline-component-package}

-   TiUPパッケージ マネージャーをオンラインでインストールします。

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

-   TiUPを使用してミラーをプルします。

    1.  インターネットにアクセスできるマシンで必要なコンポーネントをプルします。

        {{< copyable "" >}}

        ```bash
        # You can modify ${version} to the needed version.
        tiup mirror clone tidb-dm-${version}-linux-amd64 --os=linux --arch=amd64 \
            --dm-master=${version} --dm-worker=${version} --dmctl=${version} \
            --alertmanager=v0.17.0 --grafana=v4.0.3 --prometheus=v4.0.3 \
            --tiup=v$(tiup --version|grep 'tiup'|awk -F ' ' '{print $1}') --dm=v$(tiup --version|grep 'tiup'|awk -F ' ' '{print $1}')
        ```

        上記のコマンドは、現在のディレクトリに`tidb-dm-${version}-linux-amd64`という名前のディレクトリを作成します。このディレクトリには、 TiUPによって管理されるコンポーネントパッケージが含まれます。

    2.  `tar`コマンドを使用してコンポーネントパッケージをパックし、隔離された環境のコントロール マシンにパッケージを送信します。

        {{< copyable "" >}}

        ```bash
        tar czvf tidb-dm-${version}-linux-amd64.tar.gz tidb-dm-${version}-linux-amd64
        ```

        `tidb-dm-${version}-linux-amd64.tar.gz`は独立したオフライン環境パッケージです。

## ステップ 2: オフラインTiUPコンポーネントをデプロイ {#step-2-deploy-the-offline-tiup-component}

パッケージをターゲット クラスタの制御マシンに送信した後、次のコマンドを実行してTiUPコンポーネントをインストールします。

{{< copyable "" >}}

```bash
# You can modify ${version} to the needed version.
tar xzvf tidb-dm-${version}-linux-amd64.tar.gz
sh tidb-dm-${version}-linux-amd64/local_install.sh
source /home/tidb/.bash_profile
```

`local_install.sh`スクリプトは`tiup mirror set tidb-dm-${version}-linux-amd64`コマンドを自動的に実行して、現在のミラー アドレスを`tidb-dm-${version}-linux-amd64`に設定します。

ミラーを別のディレクトリに切り替えるには、 `tiup mirror set <mirror-dir>`コマンドを手動で実行します。公式ミラーに戻したい場合は、 `tiup mirror set https://tiup-mirrors.pingcap.com`を実行します。

## ステップ 3: 初期化構成ファイルを編集する {#step-3-edit-the-initialization-configuration-file}

さまざまなクラスター トポロジに従って、クラスター初期化構成ファイルを編集する必要があります。

完全な構成テンプレートについては、 [TiUP構成パラメータ テンプレート](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml)を参照してください。構成ファイルを作成します。 `topology.yaml` .他の組み合わせたシナリオでは、テンプレートに従って、必要に応じて構成ファイルを編集します。

3 つの DM-master、3 つの DM-worker、および 1 つの監視コンポーネントインスタンスを展開する構成は次のとおりです。

```yaml
---
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/home/tidb/dm/deploy"
  data_dir: "/home/tidb/dm/data"
  # arch: "amd64"

master_servers:
  - host: 172.19.0.101
  - host: 172.19.0.102
  - host: 172.19.0.103

worker_servers:
  - host: 172.19.0.101
  - host: 172.19.0.102
  - host: 172.19.0.103

monitoring_servers:
  - host: 172.19.0.101

grafana_servers:
  - host: 172.19.0.101

alertmanager_servers:
  - host: 172.19.0.101
```

> **ノート：**
>
> -   DM クラスターの高可用性を確保する必要がない場合は、DM マスター ノードを 1 つだけデプロイします。デプロイされる DM ワーカー ノードの数は、移行するアップストリームの MySQL/MariaDB インスタンスの数以上でなければなりません。
>
> -   DM クラスターの高可用性を確保するには、3 つの DM マスター ノードをデプロイすることをお勧めします。デプロイされる DM ワーカー ノードの数は、移行する上流の MySQL/MariaDB インスタンスの数よりも多くする必要があります (たとえば、数DM-worker ノードの数は、アップストリーム インスタンスの数よりも 2 つ多くなります)。
>
> -   グローバルに有効なパラメーターについては、構成ファイルの`server_configs`セクションで、対応するコンポーネントのこれらのパラメーターを構成します。
>
> -   特定のノードで有効にする必要があるパラメーターについては、このノードの`config`つでこれらのパラメーターを構成します。
>
> -   `.`を使用して、構成のサブカテゴリ`log.slow-threshold`など) を示します。その他の形式については、 [TiUP構成テンプレート](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml)を参照してください。
>
> -   パラメータの詳細については、 [マスター`config.toml.example`](https://github.com/pingcap/dm/blob/master/dm/master/dm-master.toml)および[ワーカー`config.toml.example`](https://github.com/pingcap/dm/blob/master/dm/worker/dm-worker.toml)を参照してください。
>
> -   次のコンポーネント間のポートが相互接続されていることを確認してください。
>     -   DM-master ノードの`peer_port` (デフォルトでは`8291` ) は相互接続されています。
>     -   各 DM-master ノードは、すべての DM-worker ノードの`port` (デフォルトでは`8262` ) に接続できます。
>     -   各 DM-worker ノードは、すべての DM-master ノードの`port` (デフォルトでは`8261` ) に接続できます。
>     -   TiUPノードは、すべての DM マスター ノードの`port` (デフォルトでは`8261` ) に接続できます。
>     -   TiUPノードは、すべての DM-worker ノードの`port` (デフォルトでは`8262` ) に接続できます。

## ステップ 4: デプロイ コマンドを実行する {#step-4-execute-the-deployment-command}

> **ノート：**
>
> TiUPを使用して DM を展開する場合、セキュリティ認証に秘密鍵またはインタラクティブ パスワードを使用できます。
>
> -   秘密鍵を使用する場合は、 `-i`または`--identity_file`で鍵のパスを指定できます。
> -   パスワードを使用する場合は、 `-p`フラグを追加してパスワード インタラクション ウィンドウに入ります。
> -   ターゲット マシンへのパスワードなしのログインが設定されている場合、認証は必要ありません。

{{< copyable "" >}}

```shell
tiup dm deploy dm-test ${version} ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
```

上記のコマンドで:

-   デプロイされた DM クラスターの名前は`dm-test`です。
-   DM クラスターのバージョンは`${version}`です。 `tiup list dm-master`を実行すると、 TiUPでサポートされている最新バージョンを表示できます。
-   初期設定ファイルは`topology.yaml`です。
-   `--user root` : `root`キーを使用してターゲット マシンにログインし、クラスターのデプロイを完了します。または、 `ssh`および`sudo`権限を持つ他のユーザーを使用してデプロイを完了できます。
-   `[-i]`および`[-p]` : オプション。パスワードなしでターゲット マシンへのログインを構成した場合、これらのパラメーターは必要ありません。そうでない場合は、2 つのパラメーターのいずれかを選択します。 `[-i]`ターゲット マシンにアクセスできる`root`ユーザー (または`--user`で指定された他のユーザー) の秘密鍵です。 `[-p]`対話的にユーザーパスワードを入力するために使用されます。
-   TiUP DM は組み込みの SSH クライアントを使用します。制御マシン システムにネイティブな SSH クライアントを使用する場合は、 [システムのネイティブ SSH クライアントを使用してクラスターに接続する](/dm/maintain-dm-using-tiup.md#use-the-systems-native-ssh-client-to-connect-to-cluster)に従って構成を編集します。

出力ログの最後に、 ``Deployed cluster `dm-test` successfully``が表示されます。これは、デプロイが成功したことを示します。

## ステップ 5: TiUPによって管理されているクラスターを確認する {#step-5-check-the-clusters-managed-by-tiup}

{{< copyable "" >}}

```shell
tiup dm list
```

TiUP は、複数の DM クラスターの管理をサポートしています。上記のコマンドは、現在TiUPによって管理されているすべてのクラスターの情報を出力します。これには、名前、デプロイ ユーザー、バージョン、秘密鍵の情報が含まれます。

```log
Name  User  Version  Path                                  PrivateKey
----  ----  -------  ----                                  ----------
dm-test  tidb  ${version}  /root/.tiup/storage/dm/clusters/dm-test  /root/.tiup/storage/dm/clusters/dm-test/ssh/id_rsa
```

## ステップ 6: デプロイされた DM クラスターのステータスを確認する {#step-6-check-the-status-of-the-deployed-dm-cluster}

`dm-test`クラスタのステータスを確認するには、次のコマンドを実行します。

{{< copyable "" >}}

```shell
tiup dm display dm-test
```

予想される出力には、インスタンス ID、ロール、ホスト、リスニング ポート、ステータス (クラスターがまだ開始されていないため、ステータスは`Down` / `inactive`です)、および`dm-test`クラスターのディレクトリ情報が含まれます。

## ステップ 7: クラスターを開始する {#step-7-start-the-cluster}

{{< copyable "" >}}

```shell
tiup dm start dm-test
```

出力ログに``Started cluster `dm-test` successfully``が含まれていれば、開始は成功しています。

## ステップ 8: クラスターの実行ステータスを確認する {#step-8-verify-the-running-status-of-the-cluster}

TiUPを使用して DM クラスターのステータスを確認します。

{{< copyable "" >}}

```shell
tiup dm display dm-test
```

出力の`Status`が`Up`の場合、クラスターのステータスは正常です。
