---
title: Deploy a DM Cluster Using TiUP
summary: TiUP DMを使用して TiDB データ移行を展開する方法を学習します。
---

# TiUPを使用して DMクラスタをデプロイ {#deploy-a-dm-cluster-using-tiup}

[TiUP](https://github.com/pingcap/tiup) 、TiDB 4.0 で導入されたクラスター運用および保守ツールです。TiUPは、 Golangで記述されたクラスター管理コンポーネントである[TiUP DM](/dm/maintain-dm-using-tiup.md)提供します。TiUP TiUP DMを使用すると、DM クラスターの展開、起動、停止、破棄、スケーリング、アップグレードなどの日常的な TiDB データ移行 (DM) 操作を簡単に実行し、DM クラスター パラメーターを管理できます。

TiUP は、DM v2.0 以降の DM バージョンのデプロイをサポートしています。このドキュメントでは、さまざまなトポロジの DM クラスターをデプロイする方法について説明します。

> **注記：**
>
> ターゲットマシンのオペレーティング システムが SELinux をサポートしている場合は、SELinux が**無効になっている**ことを確認してください。

## 前提条件 {#prerequisites}

DM が完全なデータ レプリケーション タスクを実行する場合、DM ワーカーは 1 つのアップストリーム データベースのみにバインドされます。DM ワーカーは最初に全量のデータをローカルにエクスポートし、次にそのデータをダウンストリーム データベースにインポートします。したがって、ワーカーのホスト スペースは、エクスポートするすべてのアップストリーム テーブルを格納するのに十分な大きさである必要があります。storageパスは、後でタスクを作成するときに指定します。

さらに、DM クラスターを展開する際には、 [ハードウェアおよびソフトウェアの要件](/dm/dm-hardware-and-software-requirements.md)満たす必要があります。

## ステップ1: 制御マシンにTiUPをインストールする {#step-1-install-tiup-on-the-control-machine}

通常のユーザー アカウント (ユーザー`tidb`を例に挙げます) を使用して制御マシンにログインします。次のすべてのTiUPインストールおよびクラスター管理操作は、ユーザー`tidb`によって実行できます。

1.  次のコマンドを実行してTiUPをインストールします。

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

    インストール後、 `~/.bashrc` PATH にTiUPを追加するように変更されているため、これを使用するには新しいターミナルを開くか、グローバル環境変数`source ~/.bashrc`を再宣言する必要があります。

2.  TiUP DMコンポーネントをインストールします:

    ```shell
    tiup install dm dmctl
    ```

## ステップ2: 初期化構成ファイルを編集する {#step-2-edit-the-initialization-configuration-file}

意図したクラスター トポロジに応じて、クラスター初期化構成ファイルを手動で作成および編集する必要があります。

[設定ファイルテンプレート](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml)に従って、YAML 構成ファイル (たとえば、名前が`topology.yaml` ) を作成する必要があります。その他のシナリオでは、それに応じて構成を編集します。

コマンド`tiup dm template > topology.yaml`を使用すると、構成ファイル テンプレートをすばやく生成できます。

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
> -   1 つのホストで DM ワーカーをあまり多く実行することは推奨されません。各 DM ワーカーには、少なくとも 2 コアの CPU と 4 GiB のメモリを割り当てる必要があります。
>
> -   次のコンポーネント間のポートが相互接続されていることを確認します。
>     -   DM マスター ノードのうち`peer_port` (デフォルトでは`8291` ) が相互接続されています。
>     -   各 DM マスター ノードは、すべての DM ワーカー ノードのうちの`port`に接続できます (デフォルトでは`8262` )。
>     -   各 DM ワーカー ノードは、すべての DM マスター ノードのうちの`port`に接続できます (デフォルトでは`8261` )。
>     -   TiUPノードは、すべての DM マスター ノードのうち`port` (デフォルトでは`8261` ) に接続できます。
>     -   TiUPノードは、すべての DM ワーカー ノードのうち`port` (デフォルトでは`8262` ) に接続できます。

`master_servers.host.config`パラメータの詳細については[マスターパラメータ](https://github.com/pingcap/tiflow/blob/release-8.1/dm/master/dm-master.toml) `worker_servers.host.config`参照してください。5 パラメータの詳細については[ワーカーパラメータ](https://github.com/pingcap/tiflow/blob/release-8.1/dm/worker/dm-worker.toml)を参照してください。

## ステップ3: デプロイメントコマンドを実行する {#step-3-execute-the-deployment-command}

> **注記：**
>
> TiUPを使用して TiDB をデプロイする場合、セキュリティ認証に秘密鍵または対話型パスワードを使用できます。
>
> -   秘密鍵を使用する場合は、 `-i`または`--identity_file`を通じて鍵のパスを指定できます。
> -   パスワードを使用する場合は、 `-p`フラグを追加してパスワード対話ウィンドウに入ります。
> -   ターゲット マシンへのパスワードなしのログインが構成されている場合、認証は必要ありません。

```shell
tiup dm deploy ${name} ${version} ./topology.yaml -u ${ssh_user} [-p] [-i /home/root/.ssh/gcp_rsa]
```

このステップで使用されるパラメータは次のとおりです。

| パラメータ                    | 説明                                                                              |
| ------------------------ | ------------------------------------------------------------------------------- |
| `${name}`                | DM クラスターの名前 (例: dm-test)                                                        |
| `${version}`             | DM クラスターのバージョン。 `tiup list dm-master`実行すると、サポートされている他のバージョンを確認できます。             |
| `./topology.yaml`        | トポロジ構成ファイルのパス。                                                                  |
| `-u`または`--user`          | クラスターの展開を完了するには、root ユーザーまたは ssh および sudo権限を持つ他のユーザー アカウントとしてターゲット マシンにログインします。 |
| `-p`または`--password`      | ターゲット ホストのパスワード。指定すると、パスワード認証が使用されます。                                           |
| `-i`または`--identity_file` | SSH ID ファイルのパス。指定すると、公開キー認証が使用されます (デフォルトは &quot;/root/.ssh/id_rsa&quot;)。      |

出力ログの最後に``Deployed cluster `dm-test` successfully``表示されます。これは、デプロイメントが成功したことを示します。

## ステップ4: TiUPによって管理されているクラスターを確認する {#step-4-check-the-clusters-managed-by-tiup}

```shell
tiup dm list
```

TiUP は複数の DM クラスターの管理をサポートしています。上記のコマンドは、名前、デプロイメント ユーザー、バージョン、秘密鍵情報など、現在TiUPによって管理されているすべてのクラスターの情報を出力します。

```log
Name  User  Version  Path                                  PrivateKey
----  ----  -------  ----                                  ----------
dm-test  tidb  ${version}  /root/.tiup/storage/dm/clusters/dm-test  /root/.tiup/storage/dm/clusters/dm-test/ssh/id_rsa
```

## ステップ5: 展開されたDMクラスタのステータスを確認する {#step-5-check-the-status-of-the-deployed-dm-cluster}

`dm-test`クラスターのステータスを確認するには、次のコマンドを実行します。

```shell
tiup dm display dm-test
```

予想される出力には、インスタンス ID、ロール、ホスト、リスニング ポート、ステータス (クラスターはまだ起動されていないため、ステータスは`Down` `inactive` )、およびディレクトリ情報が含まれます。

## ステップ6: DMクラスターを起動する {#step-6-start-the-dm-cluster}

```shell
tiup dm start dm-test
```

出力ログに``Started cluster `dm-test` successfully``含まれていれば、起動は成功です。

## ステップ7: DMクラスターの実行ステータスを確認する {#step-7-verify-the-running-status-of-the-dm-cluster}

TiUPを使用して DM クラスターのステータスを確認します。

```shell
tiup dm display dm-test
```

出力の`Status`が`Up`場合、クラスターの状態は正常です。

## ステップ 8: dmctl を使用して移行タスクを管理する {#step-8-managing-migration-tasks-using-dmctl}

dmctl は、DM クラスターを制御するために使用されるコマンドライン ツールです。 [TiUP経由でdmctlを使用する](/dm/maintain-dm-using-tiup.md#dmctl)をお勧めします。

dmctl はコマンドモードと対話モードの両方をサポートしています。詳細については[dmctl を使用して DM クラスターを管理](/dm/dmctl-introduction.md#maintain-dm-clusters-using-dmctl)を参照してください。
