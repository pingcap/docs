---
title: Deploy a DM Cluster Offline Using TiUP
summary: Introduce how to deploy a DM cluster offline using TiUP.
---

# TiUPを使用してDMクラスターをオフラインでデプロイする {#deploy-a-dm-cluster-offline-using-tiup}

このドキュメントでは、TiUPを使用してDMクラスタをオフラインで展開する方法について説明します。

## ステップ1：TiUPオフラインコンポーネントパッケージを準備する {#step-1-prepare-the-tiup-offline-component-package}

-   TiUPパッケージマネージャーをオンラインでインストールします。

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

-   TiUPを使用してミラーを引っ張る

    1.  インターネットにアクセスできるマシンで必要なコンポーネントをプルします。

        {{< copyable "" >}}

        ```bash
        # You can modify ${version} to the needed version.
        tiup mirror clone tidb-dm-${version}-linux-amd64 --os=linux --arch=amd64 \
            --dm-master=${version} --dm-worker=${version} --dmctl=${version} \
            --alertmanager=v0.17.0 --grafana=v4.0.3 --prometheus=v4.0.3 \
            --tiup=v$(tiup --version|grep 'tiup'|awk -F ' ' '{print $1}') --dm=v$(tiup --version|grep 'tiup'|awk -F ' ' '{print $1}')
        ```

        上記のコマンドは、現在のディレクトリに`tidb-dm-${version}-linux-amd64`という名前のディレクトリを作成します。このディレクトリには、TiUPによって管理されるコンポーネントパッケージが含まれています。

    2.  `tar`コマンドを使用してコンポーネントパッケージをパックし、分離された環境の制御マシンにパッケージを送信します。

        {{< copyable "" >}}

        ```bash
        tar czvf tidb-dm-${version}-linux-amd64.tar.gz tidb-dm-${version}-linux-amd64
        ```

        `tidb-dm-${version}-linux-amd64.tar.gz`は独立したオフライン環境パッケージです。

## ステップ2：オフラインTiUPコンポーネントをデプロイ {#step-2-deploy-the-offline-tiup-component}

パッケージをターゲットクラスタの制御マシンに送信した後、次のコマンドを実行してTiUPコンポーネントをインストールします。

{{< copyable "" >}}

```bash
# You can modify ${version} to the needed version.
tar xzvf tidb-dm-${version}-linux-amd64.tar.gz
sh tidb-dm-${version}-linux-amd64/local_install.sh
source /home/tidb/.bash_profile
```

`local_install.sh`スクリプトは、 `tiup mirror set tidb-dm-${version}-linux-amd64`コマンドを自動的に実行して、現在のミラーアドレスを`tidb-dm-${version}-linux-amd64`に設定します。

ミラーを別のディレクトリに切り替えるには、 `tiup mirror set <mirror-dir>`コマンドを手動で実行します。公式ミラーに戻す場合は、 `tiup mirror set https://tiup-mirrors.pingcap.com`を実行します。

## ステップ3：初期化構成ファイルを編集する {#step-3-edit-the-initialization-configuration-file}

さまざまなクラスタトポロジに従って、クラスタ初期化構成ファイルを編集する必要があります。

完全な構成テンプレートについては、 [TiUP構成パラメーターテンプレート](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml)を参照してください。構成ファイルを作成します`topology.yaml` 。他の組み合わせたシナリオでは、テンプレートに従って必要に応じて構成ファイルを編集します。

3つのDMマスター、3つのDMワーカー、および1つの監視コンポーネントインスタンスをデプロイする構成は次のとおりです。

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
> -   DMクラスタの高可用性を確保する必要がない場合は、DM-masterノードを1つだけデプロイし、デプロイされるDM-workerノードの数は、移行するアップストリームのMySQL/MariaDBインスタンスの数以上である必要があります。
>
> -   DMクラスタの高可用性を確保するには、3つのDM-masterノードをデプロイすることをお勧めします。デプロイされるDM-workerノードの数は、移行するアップストリームのMySQL / MariaDBインスタンスの数（たとえば、 DMワーカーノードの数は、アップストリームインスタンスの数より2つ多くなります）。
>
> -   グローバルに有効である必要があるパラメーターについては、構成ファイルの`server_configs`セクションで対応するコンポーネントのこれらのパラメーターを構成します。
>
> -   特定のノードで有効になるはずのパラメーターについては、このノードの`config`つでこれらのパラメーターを構成します。
>
> -   `.`を使用して、構成のサブカテゴリ（ `log.slow-threshold`など）を示します。その他の形式については、 [TiUP構成テンプレート](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml)を参照してください。
>
> -   パラメータの詳細については、 [マスター`config.toml.example`](https://github.com/pingcap/dm/blob/master/dm/master/dm-master.toml)および[ワーカー`config.toml.example`](https://github.com/pingcap/dm/blob/master/dm/worker/dm-worker.toml)を参照してください。
>
> -   次のコンポーネント間のポートが相互接続されていることを確認してください。
>     -   DMマスターノード間の`peer_port` （デフォルトでは`8291` ）は相互接続されています。
>     -   各DMマスターノードは、すべてのDMワーカーノードの`port`つ（デフォルトでは`8262` ）に接続できます。
>     -   各DM-workerノードは、すべてのDM-masterノードの`port`つ（デフォルトでは`8261` ）に接続できます。
>     -   TiUPノードは、すべてのDMマスターノードの`port`つ（デフォルトでは`8261` ）に接続できます。
>     -   TiUPノードは、すべてのDMワーカーノードの`port`つ（デフォルトでは`8262` ）に接続できます。

## 手順4：展開コマンドを実行する {#step-4-execute-the-deployment-command}

> **ノート：**
>
> TiUPを使用してDMを展開する場合、セキュリティ認証に秘密鍵または対話型パスワードを使用できます。
>
> -   秘密鍵を使用する場合は、 `-i`または`--identity_file`を介して鍵のパスを指定できます。
> -   パスワードを使用する場合は、 `-p`フラグを追加して、パスワード操作ウィンドウに入ります。
> -   ターゲットマシンへのパスワードなしのログインが設定されている場合、認証は必要ありません。

{{< copyable "" >}}

```shell
tiup dm deploy dm-test ${version} ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
```

上記のコマンドでは：

-   デプロイされたDMクラスタの名前は`dm-test`です。
-   DMクラスタのバージョンは`${version}`です。 `tiup list dm-master`を実行すると、TiUPでサポートされている最新バージョンを表示できます。
-   初期化構成ファイルは`topology.yaml`です。
-   `--user root` ： `root`キーを使用してターゲットマシンにログインしてクラスタの展開を完了するか、 `ssh`および`sudo`の特権を持つ他のユーザーを使用して展開を完了することができます。
-   `[-i]`および`[-p]` ：オプション。パスワードなしでターゲットマシンへのログインを設定した場合、これらのパラメータは必要ありません。そうでない場合は、2つのパラメーターのいずれかを選択してください。 `[-i]`は、ターゲットマシンにアクセスできる`root`のユーザー（または`--user`で指定された他のユーザー）の秘密鍵です。 `[-p]`は、ユーザーパスワードをインタラクティブに入力するために使用されます。
-   TiUP DMは、組み込みSSHクライアントを使用します。制御マシンシステムにネイティブなSSHクライアントを使用する場合は、 [システムのネイティブSSHクライアントを使用してクラスタに接続する](/dm/maintain-dm-using-tiup.md#use-the-systems-native-ssh-client-to-connect-to-cluster)に従って構成を編集します。

出力ログの最後に、 ``Deployed cluster `dm-test` successfully``が表示されます。これは、展開が成功したことを示します。

## ステップ5：TiUPによって管理されているクラスターを確認します {#step-5-check-the-clusters-managed-by-tiup}

{{< copyable "" >}}

```shell
tiup dm list
```

TiUPは、複数のDMクラスターの管理をサポートしています。上記のコマンドは、名前、展開ユーザー、バージョン、秘密鍵情報など、現在TiUPによって管理されているすべてのクラスターの情報を出力します。

```log
Name  User  Version  Path                                  PrivateKey
----  ----  -------  ----                                  ----------
dm-test  tidb  ${version}  /root/.tiup/storage/dm/clusters/dm-test  /root/.tiup/storage/dm/clusters/dm-test/ssh/id_rsa
```

## 手順6：デプロイされたDMクラスタのステータスを確認する {#step-6-check-the-status-of-the-deployed-dm-cluster}

`dm-test`のクラスタのステータスを確認するには、次のコマンドを実行します。

{{< copyable "" >}}

```shell
tiup dm display dm-test
```

期待される出力には、インスタンスID、ロール、ホスト、リスニングポート、ステータス（クラスタがまだ開始されていないため、ステータスは`Down` ）、および`inactive`クラスタのディレクトリ情報が含まれ`dm-test` 。

## ステップ7：クラスタを開始します {#step-7-start-the-cluster}

{{< copyable "" >}}

```shell
tiup dm start dm-test
```

出力ログに``Started cluster `dm-test` successfully``が含まれている場合、開始は成功しています。

## 手順8：クラスタの実行ステータスを確認する {#step-8-verify-the-running-status-of-the-cluster}

TiUPを使用してDMクラスタのステータスを確認します。

{{< copyable "" >}}

```shell
tiup dm display dm-test
```

出力で`Status`が`Up`の場合、クラスタのステータスは正常です。
