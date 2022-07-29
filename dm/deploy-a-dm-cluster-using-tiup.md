---
title: Deploy a DM Cluster Using TiUP
summary: Learn how to deploy TiDB Data Migration using TiUP DM.
---

# TiUPを使用してDMクラスターをデプロイする {#deploy-a-dm-cluster-using-tiup}

[TiUP](https://github.com/pingcap/tiup)は、TiDB4.0で導入されたクラスタ操作および保守ツールです。 TiUPは、Golangで記述されたクラスタ管理コンポーネントである[TiUP DM](/dm/maintain-dm-using-tiup.md)を提供します。 TiUP DMを使用すると、DMクラスターの展開、開始、停止、破棄、スケーリング、アップグレードなど、毎日のTiDBデータ移行（DM）操作を簡単に実行し、DMクラスタパラメーターを管理できクラスタ。

TiUPは、DMv2.0以降のDMバージョンの展開をサポートします。このドキュメントでは、さまざまなトポロジのDMクラスターを展開する方法を紹介します。

> **ノート：**
>
> ターゲットマシンのオペレーティングシステムがSELinuxをサポートしている場合は、SELinuxが**無効**になっていることを確認してください。

## 前提条件 {#prerequisites}

DMが完全なデータ複製タスクを実行する場合、DMワーカーは1つのアップストリームデータベースのみにバインドされます。 DMワーカーは、最初に全量のデータをローカルにエクスポートし、次にデータをダウンストリームデータベースにインポートします。したがって、ワーカーのホストスペースは、エクスポートするすべてのアップストリームテーブルを格納するのに十分な大きさである必要があります。ストレージパスは、後でタスクを作成するときに指定されます。

さらに、DMクラスタをデプロイするときに[ハードウェアとソフトウェアの要件](/dm/dm-hardware-and-software-requirements.md)を満たす必要があります。

## ステップ1：制御マシンにTiUPをインストールする {#step-1-install-tiup-on-the-control-machine}

通常のユーザーアカウントを使用してコントロールマシンにログインします（例として`tidb`ユーザーを取り上げます）。以下のすべてのTiUPインストールおよびクラスタ管理操作は、 `tidb`ユーザーが実行できます。

1.  次のコマンドを実行して、TiUPをインストールします。

    {{< copyable "" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

    インストール後、 `~/.bashrc`はPATHにTiUPを追加するように変更されているため、新しいターミナルを開くか、グローバル環境変数`source ~/.bashrc`を再宣言して使用する必要があります。

2.  TiUP DMコンポーネントをインストールします。

    {{< copyable "" >}}

    ```shell
    tiup install dm dmctl
    ```

## ステップ2：初期化構成ファイルを編集する {#step-2-edit-the-initialization-configuration-file}

目的のクラスタトポロジに従って、クラスタ初期化構成ファイルを手動で作成および編集する必要があります。

[構成ファイルテンプレート](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml)に従ってYAML構成ファイル（たとえば`topology.yaml`という名前）を作成する必要があります。他のシナリオでは、それに応じて構成を編集します。

コマンド`tiup dm template > topology.yaml`を使用すると、構成ファイルテンプレートをすばやく生成できます。

3つのDMマスター、3つのDMワーカー、および1つの監視コンポーネントインスタンスをデプロイする構成は次のとおりです。

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

> **ノート：**
>
> -   1つのホストであまりにも多くのDMワーカーを実行することはお勧めしません。各DMワーカーには、少なくとも2つのコアCPUと4つのGiBメモリを割り当てる必要があります。
>
> -   次のコンポーネント間のポートが相互接続されていることを確認してください。
>     -   DMマスターノード間の`peer_port` （デフォルトでは`8291` ）は相互接続されています。
>     -   各DMマスターノードは、すべてのDMワーカーノードの`port`つ（デフォルトでは`8262` ）に接続できます。
>     -   各DM-workerノードは、すべてのDM-masterノードの`port`つ（デフォルトでは`8261` ）に接続できます。
>     -   TiUPノードは、すべてのDMマスターノードの`port`つ（デフォルトでは`8261` ）に接続できます。
>     -   TiUPノードは、すべてのDMワーカーノードの`port`つ（デフォルトでは`8262` ）に接続できます。

`master_servers.host.config`つのパラメータの説明については、 [マスターパラメーター](https://github.com/pingcap/dm/blob/master/dm/master/dm-master.toml)を参照してください。 `worker_servers.host.config`パラメータの詳細については、 [ワーカーパラメータ](https://github.com/pingcap/dm/blob/master/dm/worker/dm-worker.toml)を参照してください。

## 手順3：展開コマンドを実行する {#step-3-execute-the-deployment-command}

> **ノート：**
>
> TiUPを使用してTiDBを展開する場合、セキュリティ認証に秘密鍵または対話型パスワードを使用できます。
>
> -   秘密鍵を使用する場合は、 `-i`または`--identity_file`を介して鍵のパスを指定できます。
> -   パスワードを使用する場合は、 `-p`フラグを追加して、パスワード操作ウィンドウに入ります。
> -   ターゲットマシンへのパスワードなしのログインが設定されている場合、認証は必要ありません。

{{< copyable "" >}}

```shell
tiup dm deploy ${name} ${version} ./topology.yaml -u ${ssh_user} [-p] [-i /home/root/.ssh/gcp_rsa]
```

このステップで使用されるパラメーターは次のとおりです。

| パラメータ                    | 説明                                                                    |
| ------------------------ | --------------------------------------------------------------------- |
| `${name}`                | DMクラスタの名前。例：dm-test                                                   |
| `${version}`             | DMクラスタのバージョン。 `tiup list dm-master`を実行すると、サポートされている他のバージョンを確認できます。    |
| `./topology.yaml`        | トポロジ構成ファイルのパス。                                                        |
| `-u`または`--user`          | rootユーザーまたはsshおよびsudo権限を持つ他のユーザーアカウントとしてターゲットマシンにログインし、クラスタの展開を完了します。 |
| `-p`または`--password`      | ターゲットホストのパスワード。指定した場合、パスワード認証が使用されます。                                 |
| `-i`または`--identity_file` | SSHIDファイルのパス。指定した場合、公開鍵認証が使用されます（デフォルトは「/root/.ssh/id_rsa」）。          |

出力ログの最後に、 ``Deployed cluster `dm-test` successfully``が表示されます。これは、展開が成功したことを示します。

## ステップ4：TiUPによって管理されているクラスターを確認します {#step-4-check-the-clusters-managed-by-tiup}

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

## 手順5：デプロイされたDMクラスタのステータスを確認する {#step-5-check-the-status-of-the-deployed-dm-cluster}

`dm-test`のクラスタのステータスを確認するには、次のコマンドを実行します。

{{< copyable "" >}}

```shell
tiup dm display dm-test
```

期待される出力には、インスタンスID、ロール、ホスト、リスニングポート、ステータス（クラスタがまだ開始されていないため、ステータスは`Down` ）、およびディレクトリ情報が含まれ`inactive` 。

## ステップ6：TiDBクラスタを開始します {#step-6-start-the-tidb-cluster}

{{< copyable "" >}}

```shell
tiup dm start dm-test
```

出力ログに``Started cluster `dm-test` successfully``が含まれている場合、開始は成功しています。

## 手順7：TiDBクラスタの実行ステータスを確認する {#step-7-verify-the-running-status-of-the-tidb-cluster}

TiUPを使用してDMクラスタのステータスを確認します。

{{< copyable "" >}}

```shell
tiup dm display dm-test
```

出力で`Status`が`Up`の場合、クラスタのステータスは正常です。

## ステップ8：dmctlを使用した移行タスクの管理 {#step-8-managing-migration-tasks-using-dmctl}

dmctlは、DMクラスターを制御するために使用されるコマンドラインツールです。 [TiUP経由でdmctlを使用する](/dm/maintain-dm-using-tiup.md#dmctl)をお勧めします。

dmctlは、コマンドモードとインタラクティブモードの両方をサポートします。詳細については、 [dmctlを使用してDMクラスターを管理する](/dm/dmctl-introduction.md#maintain-dm-clusters-using-dmctl)を参照してください。
