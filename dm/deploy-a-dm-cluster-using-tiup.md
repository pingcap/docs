---
title: Deploy a DM Cluster Using TiUP
summary: Learn how to deploy TiDB Data Migration using TiUP DM.
---

# TiUPを使用した DMクラスタのデプロイ {#deploy-a-dm-cluster-using-tiup}

[TiUP](https://github.com/pingcap/tiup)は、TiDB 4.0 で導入されたクラスターの運用および保守ツールです。 TiUP は、 Golangで書かれたクラスター管理コンポーネント[TiUP DM](/dm/maintain-dm-using-tiup.md)を提供します。 TiUP DMを使用すると、DM クラスターのデプロイ、開始、停止、破棄、スケーリング、アップグレードなどの毎日の TiDB データ移行 (DM) 操作を簡単に実行し、DM クラスターのパラメーターを管理できます。

TiUP は、 DM v2.0 以降の DM バージョンの導入をサポートしています。このドキュメントでは、さまざまなトポロジの DM クラスターを展開する方法を紹介します。

> **注記：**
>
> ターゲット マシンのオペレーティング システムが SELinux をサポートしている場合は、SELinux が**無効になっている**ことを確認してください。

## 前提条件 {#prerequisites}

DM が完全なデータ レプリケーション タスクを実行する場合、DM ワーカーは 1 つのアップストリーム データベースのみにバインドされます。 DM ワーカーは、まず全量のデータをローカルにエクスポートし、次にそのデータをダウンストリーム データベースにインポートします。したがって、ワーカーのホスト領域には、エクスポートするすべての上流テーブルを格納できる十分な大きさが必要です。storageパスは、後でタスクを作成するときに指定します。

さらに、DM クラスターをデプロイする場合は[ハードウェアとソフトウェアの要件](/dm/dm-hardware-and-software-requirements.md)を満たす必要があります。

## ステップ 1: TiUP を制御マシンにインストールする {#step-1-install-tiup-on-the-control-machine}

通常のユーザー アカウントを使用して制御マシンにログインします (例として`tidb`ユーザーを取り上げます)。次のすべてのTiUPインストールおよびクラスター管理操作は、 `tidb`ユーザーによって実行できます。

1.  次のコマンドを実行してTiUPをインストールします。

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

    インストール後、 `~/.bashrc` TiUP をPATH に追加するように変更されているため、これを使用するには、新しいターミナルを開くか、グローバル環境変数`source ~/.bashrc`を再宣言する必要があります。

2.  TiUP DMコンポーネントをインストールします。

    ```shell
    tiup install dm dmctl
    ```

## ステップ 2: 初期化構成ファイルを編集する {#step-2-edit-the-initialization-configuration-file}

目的のクラスター トポロジに応じて、クラスター初期化構成ファイルを手動で作成および編集する必要があります。

[設定ファイルのテンプレート](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml)に従って、YAML 構成ファイル (たとえば`topology.yaml`という名前) を作成する必要があります。他のシナリオの場合は、それに応じて構成を編集します。

コマンド`tiup dm template > topology.yaml`を使用すると、構成ファイルのテンプレートをすばやく生成できます。

3 つの DM マスター、3 つの DM ワーカー、および 1 つの監視コンポーネントインスタンスをデプロイする構成は次のとおりです。

```yaml
# The global variables apply to all other components in the configuration. If one specific value is missing in the component instance, the corresponding global variable serves as the default value.
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/dm-deploy"
  data_dir: "/dm-data"

server_configs:
  master:
    log-level: info
    # rpc-timeout: "30s"
    # rpc-rate-limit: 10.0
    # rpc-rate-burst: 40
  worker:
    log-level: info

master_servers:
  - host: 10.0.1.11
    name: master1
    ssh_port: 22
    port: 8261
    # peer_port: 8291
    # deploy_dir: "/dm-deploy/dm-master-8261"
    # data_dir: "/dm-data/dm-master-8261"
    # log_dir: "/dm-deploy/dm-master-8261/log"
    # numa_node: "0,1"
    # The following configs are used to overwrite the `server_configs.master` values.
    config:
      log-level: info
      # rpc-timeout: "30s"
      # rpc-rate-limit: 10.0
      # rpc-rate-burst: 40
  - host: 10.0.1.18
    name: master2
    ssh_port: 22
    port: 8261
  - host: 10.0.1.19
    name: master3
    ssh_port: 22
    port: 8261
# If you do not need to ensure high availability of the DM cluster, deploy only one DM-master node, and the number of deployed DM-worker nodes must be no less than the number of upstream MySQL/MariaDB instances to be migrated.
# To ensure high availability of the DM cluster, it is recommended to deploy three DM-master nodes, and the number of deployed DM-worker nodes must exceed the number of upstream MySQL/MariaDB instances to be migrated (for example, the number of DM-worker nodes is two more than the number of upstream instances).
worker_servers:
  - host: 10.0.1.12
    ssh_port: 22
    port: 8262
    # deploy_dir: "/dm-deploy/dm-worker-8262"
    # log_dir: "/dm-deploy/dm-worker-8262/log"
    # numa_node: "0,1"
    # The following configs are used to overwrite the `server_configs.worker` values.
    config:
      log-level: info
  - host: 10.0.1.19
    ssh_port: 22
    port: 8262

monitoring_servers:
  - host: 10.0.1.13
    ssh_port: 22
    port: 9090
    # deploy_dir: "/tidb-deploy/prometheus-8249"
    # data_dir: "/tidb-data/prometheus-8249"
    # log_dir: "/tidb-deploy/prometheus-8249/log"

grafana_servers:
  - host: 10.0.1.14
    port: 3000
    # deploy_dir: /tidb-deploy/grafana-3000

alertmanager_servers:
  - host: 10.0.1.15
    ssh_port: 22
    web_port: 9093
    # cluster_port: 9094
    # deploy_dir: "/tidb-deploy/alertmanager-9093"
    # data_dir: "/tidb-data/alertmanager-9093"
    # log_dir: "/tidb-deploy/alertmanager-9093/log"

```

> **注記：**
>
> -   1 つのホスト上であまりにも多くの DM ワーカーを実行することはお勧めできません。各 DM ワーカーには、少なくとも 2 コアの CPU と 4 GiB のメモリを割り当てる必要があります。
>
> -   次のコンポーネント間のポートが相互接続されていることを確認してください。
>     -   DM マスター ノードのうちの`peer_port` (デフォルトでは`8291` ) は相互接続されています。
>     -   各 DM マスター ノードは、すべての DM ワーカー ノードのうち`port` (デフォルトでは`8262` ) に接続できます。
>     -   各 DM ワーカー ノードは、すべての DM マスター ノードのうち`port` (デフォルトでは`8261` ) に接続できます。
>     -   TiUPノードは、すべての DM マスター ノードのうちの`port`に接続できます (デフォルトでは`8261` )。
>     -   TiUPノードは、すべての DM ワーカー ノードのうちの`port`に接続できます (デフォルトでは`8262` )。

`master_servers.host.config`パラメータの詳細については、 [マスターパラメータ](https://github.com/pingcap/dm/blob/master/dm/master/dm-master.toml)を参照してください。 `worker_servers.host.config`パラメータの詳細については、 [ワーカーパラメータ](https://github.com/pingcap/dm/blob/master/dm/worker/dm-worker.toml)を参照してください。

## ステップ 3: デプロイメント コマンドを実行する {#step-3-execute-the-deployment-command}

> **注記：**
>
> TiUPを使用して TiDB をデプロイする場合、セキュリティ認証に秘密キーまたは対話型パスワードを使用できます。
>
> -   秘密キーを使用する場合は、 `-i`または`--identity_file`でキーのパスを指定できます。
> -   パスワードを使用する場合は、 `-p`フラグを追加してパスワード対話ウィンドウに入ります。
> -   ターゲット マシンへのパスワードなしのログインが設定されている場合、認証は必要ありません。

```shell
tiup dm deploy ${name} ${version} ./topology.yaml -u ${ssh_user} [-p] [-i /home/root/.ssh/gcp_rsa]
```

このステップで使用されるパラメータは次のとおりです。

| パラメータ                    | 説明                                                                           |
| ------------------------ | ---------------------------------------------------------------------------- |
| `${name}`                | DM クラスターの名前 (例: dm-test)                                                     |
| `${version}`             | DM クラスターのバージョン。 `tiup list dm-master`を実行すると、サポートされている他のバージョンを確認できます。         |
| `./topology.yaml`        | トポロジ構成ファイルのパス。                                                               |
| `-u`または`--user`          | root ユーザーまたは ssh および sudo権限を持つ他のユーザー アカウントとしてターゲット マシンにログインし、クラスターの展開を完了します。 |
| `-p`または`--password`      | ターゲットホストのパスワード。指定した場合、パスワード認証が使用されます。                                        |
| `-i`または`--identity_file` | SSH ID ファイルのパス。指定した場合、公開キー認証が使用されます (デフォルトは「/root/.ssh/id_rsa」)。             |

出力ログの最後には``Deployed cluster `dm-test` successfully``が表示されます。これは、展開が成功したことを示します。

## ステップ 4: TiUPによって管理されているクラスターを確認する {#step-4-check-the-clusters-managed-by-tiup}

```shell
tiup dm list
```

TiUP は、複数の DM クラスターの管理をサポートします。上記のコマンドは、名前、デプロイメント ユーザー、バージョン、秘密キー情報など、現在TiUPによって管理されているすべてのクラスターの情報を出力します。

```log
Name  User  Version  Path                                  PrivateKey
----  ----  -------  ----                                  ----------
dm-test  tidb  ${version}  /root/.tiup/storage/dm/clusters/dm-test  /root/.tiup/storage/dm/clusters/dm-test/ssh/id_rsa
```

## ステップ 5: デプロイされた DM クラスターのステータスを確認する {#step-5-check-the-status-of-the-deployed-dm-cluster}

`dm-test`クラスターのステータスを確認するには、次のコマンドを実行します。

```shell
tiup dm display dm-test
```

予期される出力には、インスタンス ID、ロール、ホスト、リスニング ポート、ステータス (クラスターがまだ起動していないため、ステータスは`Down` / `inactive`です)、およびディレクトリ情報が含まれます。

## ステップ 6: DM クラスターを開始する {#step-6-start-the-dm-cluster}

```shell
tiup dm start dm-test
```

出力ログに``Started cluster `dm-test` successfully``が含まれていれば、起動は成功です。

## ステップ 7: DM クラスターの実行ステータスを確認する {#step-7-verify-the-running-status-of-the-dm-cluster}

TiUPを使用して DM クラスターのステータスを確認します。

```shell
tiup dm display dm-test
```

出力の`Status`が`Up`の場合、クラスターのステータスは正常です。

## ステップ 8: dmctl を使用した移行タスクの管理 {#step-8-managing-migration-tasks-using-dmctl}

dmctl は、DM クラスターの制御に使用されるコマンドライン ツールです。 [TiUP経由で dmctl を使用する](/dm/maintain-dm-using-tiup.md#dmctl)をお勧めします。

dmctl は、コマンド モードと対話モードの両方をサポートします。詳細は[dmctl を使用した DM クラスターの管理](/dm/dmctl-introduction.md#maintain-dm-clusters-using-dmctl)を参照してください。
