---
title: Deploy a DM Cluster Offline Using TiUP
summary: TiUP を使用して DM クラスターをオフラインでデプロイする方法を紹介します。
---

# TiUP を使用して DMクラスタをオフラインでデプロイ {#deploy-a-dm-cluster-offline-using-tiup}

このドキュメントでは、 TiUP を使用して DM クラスターをオフラインでデプロイする方法について説明します。

## ステップ1: TiUPオフラインコンポーネントパッケージを準備する {#step-1-prepare-the-tiup-offline-component-package}

-   TiUPパッケージ マネージャーをオンラインでインストールします。

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

-   TiUPを使用してミラーを引き出す

    1.  インターネットにアクセスできるマシンで必要なコンポーネントを取得します。

        ```bash
        # You can modify ${version} to the needed version.
        tiup mirror clone tidb-dm-${version}-linux-amd64 --os=linux --arch=amd64 \
            --dm-master=${version} --dm-worker=${version} --dmctl=${version} \
            --alertmanager=v0.17.0 --grafana=v4.0.3 --prometheus=v4.0.3 \
            --dm=v$(tiup --version|grep 'tiup'|awk -F ' ' '{print $1}')
        ```

        上記のコマンドは、現在のディレクトリに`tidb-dm-${version}-linux-amd64`という名前のディレクトリを作成します。このディレクトリには、 TiUPによって管理されるコンポーネントパッケージが含まれます。

    2.  `tar`コマンドを使用してコンポーネントパッケージをパックし、パッケージを分離された環境内の制御マシンに送信します。

        ```bash
        tar czvf tidb-dm-${version}-linux-amd64.tar.gz tidb-dm-${version}-linux-amd64
        ```

        `tidb-dm-${version}-linux-amd64.tar.gz`独立したオフライン環境パッケージです。

## ステップ2: オフラインTiUPコンポーネントをデプロイ {#step-2-deploy-the-offline-tiup-component}

パッケージをターゲット クラスターの制御マシンに送信した後、次のコマンドを実行してTiUPコンポーネントをインストールします。

```bash
# You can modify ${version} to the needed version.
tar xzvf tidb-dm-${version}-linux-amd64.tar.gz
sh tidb-dm-${version}-linux-amd64/local_install.sh
source /home/tidb/.bash_profile
```

`local_install.sh`スクリプトは`tiup mirror set tidb-dm-${version}-linux-amd64`コマンドを自動的に実行して、現在のミラー アドレスを`tidb-dm-${version}-linux-amd64`に設定します。

ミラーを別のディレクトリに切り替えるには、 `tiup mirror set <mirror-dir>`コマンドを手動で実行します。公式ミラーに戻す場合は、 `tiup mirror set https://tiup-mirrors.pingcap.com`実行します。

## ステップ3: 初期化構成ファイルを編集する {#step-3-edit-the-initialization-configuration-file}

さまざまなクラスター トポロジに応じて、クラスター初期化構成ファイルを編集する必要があります。

完全な構成テンプレートについては、「 [TiUP構成パラメータ テンプレート](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml) . 構成ファイルを作成する」を参照してください`topology.yaml` . その他の複合シナリオでは、テンプレートに従って必要に応じて構成ファイルを編集します。

3 つの DM マスター、3 つの DM ワーカー、および 1 つの監視コンポーネントインスタンスをデプロイする構成は次のとおりです。

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

> **注記：**
>
> -   DM クラスターの高可用性を確保する必要がない場合は、DM マスター ノードを 1 つだけデプロイし、デプロイされた DM ワーカー ノードの数は、移行するアップストリーム MySQL/MariaDB インスタンスの数以上である必要があります。
>
> -   DM クラスターの高可用性を確保するには、3 つの DM マスター ノードを展開することをお勧めします。また、展開する DM ワーカー ノードの数は、移行するアップストリーム MySQL/MariaDB インスタンスの数より多くする必要があります (たとえば、DM ワーカー ノードの数は、アップストリーム インスタンスの数より 2 つ多くなります)。
>
> -   グローバルに有効にする必要があるパラメータについては、構成ファイルの`server_configs`セクションで対応するコンポーネントのこれらのパラメータを構成します。
>
> -   特定のノードで有効にするパラメータについては、このノードの`config`でこれらのパラメータを設定します。
>
> -   `.`使用して、構成のサブカテゴリを示します (例: `log.slow-threshold` 。その他の形式については、 [TiUP構成テンプレート](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml)参照してください。
>
> -   詳細なパラメータの説明については、 [マスター`config.toml.example`](https://github.com/pingcap/tiflow/blob/release-8.5/dm/master/dm-master.toml)と[ワーカー`config.toml.example`](https://github.com/pingcap/tiflow/blob/release-8.5/dm/worker/dm-worker.toml)参照してください。
>
> -   次のコンポーネント間のポートが相互接続されていることを確認します。
>     -   DM マスター ノードのうち`peer_port` (デフォルトでは`8291` ) が相互接続されています。
>     -   各 DM マスター ノードは、すべての DM ワーカー ノードのうちの`port`に接続できます (デフォルトでは`8262` )。
>     -   各 DM ワーカー ノードは、すべての DM マスター ノードのうちの`port`に接続できます (デフォルトでは`8261` )。
>     -   TiUPノードは、すべての DM マスター ノードのうち`port` (デフォルトでは`8261` ) に接続できます。
>     -   TiUPノードは、すべての DM ワーカー ノードのうち`port` (デフォルトでは`8262` ) に接続できます。

## ステップ4: デプロイメントコマンドを実行する {#step-4-execute-the-deployment-command}

> **注記：**
>
> TiUPを使用して DM を展開する場合、セキュリティ認証に秘密キーまたは対話型パスワードを使用できます。
>
> -   秘密鍵を使用する場合は、 `-i`または`--identity_file`を通じて鍵のパスを指定できます。
> -   パスワードを使用する場合は、 `-p`フラグを追加してパスワード対話ウィンドウに入ります。
> -   ターゲット マシンへのパスワードなしのログインが構成されている場合、認証は必要ありません。

```shell
tiup dm deploy dm-test ${version} ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
```

上記のコマンドでは:

-   デプロイされた DM クラスターの名前は`dm-test`です。
-   DM クラスターのバージョンは`${version}`です`tiup list dm-master`実行すると、 TiUPでサポートされている最新バージョンを表示できます。
-   初期化構成ファイルは`topology.yaml`です。
-   `--user root` : `root`キーを使用してターゲット マシンにログインし、クラスターの展開を完了するか、 `ssh`および`sudo`権限を持つ他のユーザーを使用して展開を完了することができます。
-   `[-i]`と`[-p]` : オプション。パスワードなしでターゲット マシンにログインするように設定した場合、これらのパラメータは必要ありません。そうでない場合は、2 つのパラメータのいずれかを選択します。4 `[-i]` 、ターゲット マシンにアクセスできる`root`ユーザー (または`--user`で指定された他のユーザー) の秘密鍵です。10 `[-p]` 、ユーザー パスワードを対話的に入力するために使用されます。
-   TiUP DM は組み込みの SSH クライアントを使用します。制御マシン システムにネイティブの SSH クライアントを使用する場合は、 [システムのネイティブSSHクライアントを使用してクラスターに接続する](/dm/maintain-dm-using-tiup.md#use-the-systems-native-ssh-client-to-connect-to-cluster)に従って設定を編集します。

出力ログの最後に``Deployed cluster `dm-test` successfully``表示されます。これは、デプロイメントが成功したことを示します。

## ステップ5: TiUPによって管理されているクラスターを確認する {#step-5-check-the-clusters-managed-by-tiup}

```shell
tiup dm list
```

TiUP は複数の DM クラスターの管理をサポートしています。上記のコマンドは、名前、デプロイメント ユーザー、バージョン、秘密キー情報など、現在TiUPによって管理されているすべてのクラスターの情報を出力します。

```log
Name  User  Version  Path                                  PrivateKey
----  ----  -------  ----                                  ----------
dm-test  tidb  ${version}  /root/.tiup/storage/dm/clusters/dm-test  /root/.tiup/storage/dm/clusters/dm-test/ssh/id_rsa
```

## ステップ6: 展開されたDMクラスタのステータスを確認する {#step-6-check-the-status-of-the-deployed-dm-cluster}

`dm-test`クラスターのステータスを確認するには、次のコマンドを実行します。

```shell
tiup dm display dm-test
```

予想される出力には、インスタンス ID、ロール、ホスト、リスニング ポート、ステータス (クラスターはまだ起動されていないため、ステータスは`Down`です`inactive` 、および`dm-test`クラスターのディレクトリ情報が含まれます。

## ステップ7: クラスターを起動する {#step-7-start-the-cluster}

```shell
tiup dm start dm-test
```

出力ログに``Started cluster `dm-test` successfully``が含まれていれば、起動は成功です。

## ステップ8: クラスターの実行状態を確認する {#step-8-verify-the-running-status-of-the-cluster}

TiUP を使用して DM クラスターのステータスを確認します。

```shell
tiup dm display dm-test
```

出力の`Status`が`Up`の場合、クラスターの状態は正常です。
