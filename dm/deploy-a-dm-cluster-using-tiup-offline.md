---
title: Deploy a DM Cluster Offline Using TiUP
summary: Introduce how to deploy a DM cluster offline using TiUP.
---

# TiUPを使用して DMクラスタをオフラインでデプロイ {#deploy-a-dm-cluster-offline-using-tiup}

このドキュメントでは、 TiUPを使用して DM クラスターをオフラインで展開する方法について説明します。

## ステップ 1: TiUPオフラインコンポーネントパッケージを準備する {#step-1-prepare-the-tiup-offline-component-package}

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

-   TiUPを使ってミラーを引く

    1.  インターネットにアクセスできるマシン上で必要なコンポーネントをプルします。

        ```bash
        # You can modify ${version} to the needed version.
        tiup mirror clone tidb-dm-${version}-linux-amd64 --os=linux --arch=amd64 \
            --dm-master=${version} --dm-worker=${version} --dmctl=${version} \
            --alertmanager=v0.17.0 --grafana=v4.0.3 --prometheus=v4.0.3 \
            --tiup=v$(tiup --version|grep 'tiup'|awk -F ' ' '{print $1}') --dm=v$(tiup --version|grep 'tiup'|awk -F ' ' '{print $1}')
        ```

        上記のコマンドは、現在のディレクトリに`tidb-dm-${version}-linux-amd64`という名前のディレクトリを作成します。このディレクトリには、 TiUPによって管理されるコンポーネントパッケージが含まれています。

    2.  `tar`コマンドを使用してコンポーネントパッケージをパックし、そのパッケージを分離環境の制御マシンに送信します。

        ```bash
        tar czvf tidb-dm-${version}-linux-amd64.tar.gz tidb-dm-${version}-linux-amd64
        ```

        `tidb-dm-${version}-linux-amd64.tar.gz`独立したオフライン環境パッケージです。

## ステップ 2: オフラインTiUPコンポーネントをデプロイ {#step-2-deploy-the-offline-tiup-component}

パッケージをターゲット クラスターの制御マシンに送信した後、次のコマンドを実行してTiUPコンポーネントをインストールします。

```bash
# You can modify ${version} to the needed version.
tar xzvf tidb-dm-${version}-linux-amd64.tar.gz
sh tidb-dm-${version}-linux-amd64/local_install.sh
source /home/tidb/.bash_profile
```

`local_install.sh`スクリプトは`tiup mirror set tidb-dm-${version}-linux-amd64`コマンドを自動的に実行して、現在のミラー アドレスを`tidb-dm-${version}-linux-amd64`に設定します。

ミラーを別のディレクトリに切り替えるには、 `tiup mirror set <mirror-dir>`コマンドを手動で実行します。公式ミラーに戻したい場合は、 `tiup mirror set https://tiup-mirrors.pingcap.com`を実行します。

## ステップ 3: 初期化構成ファイルを編集する {#step-3-edit-the-initialization-configuration-file}

さまざまなクラスター トポロジに応じてクラスター初期化構成ファイルを編集する必要があります。

完全な構成テンプレートについては、 [TiUP設定パラメータ テンプレート](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml)を参照してください。 `topology.yaml`設定ファイルを作成します。その他の組み合わせシナリオでは、テンプレートに従って必要に応じて構成ファイルを編集します。

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
> -   DM クラスターの高可用性を確保する必要がない場合は、DM マスター ノードを 1 つだけデプロイし、デプロイされた DM ワーカー ノードの数が、移行する上流の MySQL/MariaDB インスタンスの数以上である必要があります。
>
> -   DM クラスターの高可用性を確保するには、3 つの DM マスター ノードをデプロイすることをお勧めします。また、デプロイされた DM ワーカー ノードの数は、移行する上流の MySQL/MariaDB インスタンスの数 (たとえば、 DM ワーカー ノードの数は上流インスタンスの数より 2 つ多くなります)。
>
> -   グローバルに有効にするパラメータについては、設定ファイルの`server_configs`セクションで対応するコンポーネントのパラメータを設定します。
>
> -   特定のノードで有効にするパラメータについては、このノードの`config`でこれらのパラメータを設定します。
>
> -   構成のサブカテゴリを示すには`.`を使用します ( `log.slow-threshold`など)。その他の形式については、 [TiUP設定テンプレート](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml)を参照してください。
>
> -   パラメーターの詳細については、 [マスター`config.toml.example`](https://github.com/pingcap/dm/blob/master/dm/master/dm-master.toml)および[ワーカーの`config.toml.example`](https://github.com/pingcap/dm/blob/master/dm/worker/dm-worker.toml)を参照してください。
>
> -   次のコンポーネント間のポートが相互接続されていることを確認してください。
>     -   DM マスター ノードのうちの`peer_port` (デフォルトでは`8291` ) は相互接続されています。
>     -   各 DM マスター ノードは、すべての DM ワーカー ノードのうち`port` (デフォルトでは`8262` ) に接続できます。
>     -   各 DM ワーカー ノードは、すべての DM マスター ノードのうち`port` (デフォルトでは`8261` ) に接続できます。
>     -   TiUPノードは、すべての DM マスター ノードのうちの`port`に接続できます (デフォルトでは`8261` )。
>     -   TiUPノードは、すべての DM ワーカー ノードのうちの`port`に接続できます (デフォルトでは`8262` )。

## ステップ 4: デプロイメント コマンドを実行する {#step-4-execute-the-deployment-command}

> **注記：**
>
> TiUPを使用して DM を展開する場合、セキュリティ認証に秘密キーまたは対話型パスワードを使用できます。
>
> -   秘密キーを使用する場合は、 `-i`または`--identity_file`でキーのパスを指定できます。
> -   パスワードを使用する場合は、 `-p`フラグを追加してパスワード対話ウィンドウに入ります。
> -   ターゲット マシンへのパスワードなしのログインが設定されている場合、認証は必要ありません。

```shell
tiup dm deploy dm-test ${version} ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
```

上記のコマンドでは次のようになります。

-   デプロイされた DM クラスターの名前は`dm-test`です。
-   DM クラスターのバージョンは`${version}`です。 `tiup list dm-master`を実行すると、 TiUPでサポートされている最新バージョンを表示できます。
-   初期化設定ファイルは`topology.yaml`です。
-   `--user root` : `root`キーを使用してターゲット マシンにログインしてクラスターのデプロイメントを完了するか、 `ssh`および`sudo`権限を持つ他のユーザーを使用してデプロイメントを完了することもできます。
-   `[-i]`および`[-p]` : オプション。パスワードなしでターゲット マシンへのログインを設定した場合、これらのパラメータは必要ありません。そうでない場合は、2 つのパラメータのいずれかを選択します。 `[-i]`ターゲット マシンにアクセスできるユーザー`root` (または`--user`で指定された他のユーザー) の秘密キーです。 `[-p]`ユーザーのパスワードを対話的に入力するために使用されます。
-   TiUP DM は組み込み SSH クライアントを使用します。制御マシン システムにネイティブな SSH クライアントを使用する場合は、 [システムのネイティブ SSH クライアントを使用してクラスターに接続する](/dm/maintain-dm-using-tiup.md#use-the-systems-native-ssh-client-to-connect-to-cluster)に従って設定を編集します。

出力ログの最後には``Deployed cluster `dm-test` successfully``が表示されます。これは、展開が成功したことを示します。

## ステップ 5: TiUPによって管理されているクラスターを確認する {#step-5-check-the-clusters-managed-by-tiup}

```shell
tiup dm list
```

TiUP は、複数の DM クラスターの管理をサポートします。上記のコマンドは、名前、デプロイメント ユーザー、バージョン、秘密キー情報など、現在TiUPによって管理されているすべてのクラスターの情報を出力します。

```log
Name  User  Version  Path                                  PrivateKey
----  ----  -------  ----                                  ----------
dm-test  tidb  ${version}  /root/.tiup/storage/dm/clusters/dm-test  /root/.tiup/storage/dm/clusters/dm-test/ssh/id_rsa
```

## ステップ 6: デプロイされた DM クラスターのステータスを確認する {#step-6-check-the-status-of-the-deployed-dm-cluster}

`dm-test`クラスターのステータスを確認するには、次のコマンドを実行します。

```shell
tiup dm display dm-test
```

予期される出力には、インスタンス ID、ロール、ホスト、リスニング ポート、ステータス (クラスターがまだ起動していないため、ステータスは`Down` / `inactive` )、およびクラスター`dm-test`のディレクトリ情報が含まれます。

## ステップ 7: クラスターを開始する {#step-7-start-the-cluster}

```shell
tiup dm start dm-test
```

出力ログに``Started cluster `dm-test` successfully``が含まれていれば、起動は成功です。

## ステップ 8: クラスターの実行ステータスを確認する {#step-8-verify-the-running-status-of-the-cluster}

TiUPを使用して DM クラスターのステータスを確認します。

```shell
tiup dm display dm-test
```

出力の`Status`が`Up`の場合、クラスターのステータスは正常です。
