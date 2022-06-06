---
title: Deploy and Maintain an Online TiDB Cluster Using TiUP
summary: Learns how to deploy and maintain an online TiDB cluster using TiUP.
---

# TiUPを使用したオンラインTiDBクラスターのデプロイと管理 {#deploy-and-maintain-an-online-tidb-cluster-using-tiup}

このドキュメントでは、TiUPクラスタコンポーネントの使用方法に焦点を当てています。オンライン展開の完全な手順については、 [TiUPを使用してTiDBクラスターをデプロイする](/production-deployment-using-tiup.md)を参照してください。

ローカルテストの展開に使用される[TiUPプレイグラウンドコンポーネント](/tiup/tiup-playground.md)と同様に、TiUPクラスタコンポーネントは、実稼働環境にTiDBをすばやく展開します。遊び場と比較して、クラスタコンポーネントは、アップグレード、スケーリング、さらには運用と監査を含む、より強力な本番クラスタ管理機能を提供します。

クラスタコンポーネントのヘルプ情報については、次のコマンドを実行してください。

```bash
tiup cluster
```

```
Starting component `cluster`: /home/tidb/.tiup/components/cluster/v1.9.0/cluster
Deploy a TiDB cluster for production

Usage:
  cluster [flags]
  cluster [command]

Available Commands:
  check       Perform preflight checks for the cluster
  deploy      Deploy a cluster for production
  start       Start a TiDB cluster
  stop        Stop a TiDB cluster
  restart     Restart a TiDB cluster
  scale-in    Scale in a TiDB cluster
  scale-out   Scale out a TiDB cluster
  clean       Clean up cluster data
  destroy     Destroy a specified cluster
  upgrade     Upgrade a specified TiDB cluster
  exec        Run shell command on host in the tidb cluster
  display     Display information of a TiDB cluster
  list        List all clusters
  audit       Show audit log of cluster operation
  import      Import an exist TiDB cluster from TiDB Ansible
  edit-config Edit TiDB cluster config
  reload      Reload a TiDB cluster's config and restart if needed
  patch       Replace the remote package with a specified package and restart the service
  help        Help about any command

Flags:
  -h, --help              help for cluster
      --native-ssh        Use the system's native SSH client
      --wait-timeout int  Timeout of waiting the operation
      --ssh-timeout int   Timeout in seconds to connect host via SSH, ignored for operations that don't need an SSH connection. (default 5)
  -y, --yes               Skip all confirmations and assumes 'yes'
```

## クラスタをデプロイします {#deploy-the-cluster}

クラスタをデプロイするには、 `tiup cluster deploy`コマンドを実行します。コマンドの使用法は次のとおりです。

```bash
tiup cluster deploy <cluster-name> <version> <topology.yaml> [flags]
```

このコマンドでは、クラスタ名、TiDBクラスタのバージョン、およびクラスタのトポロジーファイルを指定する必要があります。

トポロジーファイルを作成するには、 [例](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml)を参照してください。次のファイルは、最も単純なトポロジの例です。

> **ノート：**
>
> TiUPクラスタコンポーネントが展開とスケーリングに使用するトポロジファイルは、 [yaml](https://yaml.org/spec/1.2/spec.html)の構文を使用して記述されているため、インデントが正しいことを確認してください。

```yaml
---

pd_servers:
  - host: 172.16.5.134
    name: pd-134
  - host: 172.16.5.139
    name: pd-139
  - host: 172.16.5.140
    name: pd-140

tidb_servers:
  - host: 172.16.5.134
  - host: 172.16.5.139
  - host: 172.16.5.140

tikv_servers:
  - host: 172.16.5.134
  - host: 172.16.5.139
  - host: 172.16.5.140

grafana_servers:
  - host: 172.16.5.134

monitoring_servers:
  - host: 172.16.5.134
```

デフォルトでは、TiUPはamd64アーキテクチャで実行されているバイナリファイルとしてデプロイされます。ターゲットマシンがarm64アーキテクチャである場合は、トポロジファイルで構成できます。

```yaml
global:
  arch: "arm64"           # Configures all machines to use the binary files of the arm64 architecture by default

tidb_servers:
  - host: 172.16.5.134
    arch: "amd64"         # Configures this machine to use the binary files of the amd64 architecture
  - host: 172.16.5.139
    arch: "arm64"         # Configures this machine to use the binary files of the arm64 architecture
  - host: 172.16.5.140    # Machines that are not configured with the arch field use the default value in the global field, which is arm64 in this case.

...
```

ファイルを`/tmp/topology.yaml`として保存します。 TiDB v5.4.1を使用する場合で、クラスタ名が`prod-cluster`の場合は、次のコマンドを実行します。

{{< copyable "" >}}

```shell
tiup cluster deploy -p prod-cluster v5.4.1 /tmp/topology.yaml
```

実行中に、TiUPはトポロジを再度確認するように要求し、ターゲットマシンのルートパスワードを要求します（ `-p`フラグはパスワードの入力を意味します）。

```bash
Please confirm your topology:
TiDB Cluster: prod-cluster
TiDB Version: v5.4.1
Type        Host          Ports        Directories
----        ----          -----        -----------
pd          172.16.5.134  2379/2380    deploy/pd-2379,data/pd-2379
pd          172.16.5.139  2379/2380    deploy/pd-2379,data/pd-2379
pd          172.16.5.140  2379/2380    deploy/pd-2379,data/pd-2379
tikv        172.16.5.134  20160/20180  deploy/tikv-20160,data/tikv-20160
tikv        172.16.5.139  20160/20180  deploy/tikv-20160,data/tikv-20160
tikv        172.16.5.140  20160/20180  deploy/tikv-20160,data/tikv-20160
tidb        172.16.5.134  4000/10080   deploy/tidb-4000
tidb        172.16.5.139  4000/10080   deploy/tidb-4000
tidb        172.16.5.140  4000/10080   deploy/tidb-4000
prometheus  172.16.5.134  9090         deploy/prometheus-9090,data/prometheus-9090
grafana     172.16.5.134  3000         deploy/grafana-3000
Attention:
    1. If the topology is not what you expected, check your yaml file.
    2. Please confirm there is no port/directory conflicts in same host.
Do you want to continue? [y/N]:
```

パスワードを入力すると、TiUPクラスタは必要なコンポーネントをダウンロードし、対応するマシンにデプロイします。次のメッセージが表示されたら、展開は成功しています。

```bash
Deployed cluster `prod-cluster` successfully
```

## クラスタリストを表示する {#view-the-cluster-list}

クラスタが正常にデプロイされたら、次のコマンドを実行してクラスタリストを表示します。

{{< copyable "" >}}

```bash
tiup cluster list
```

```
Starting /root/.tiup/components/cluster/v1.9.0/cluster list
Name          User  Version    Path                                               PrivateKey
----          ----  -------    ----                                               ----------
prod-cluster  tidb  v5.4.1    /root/.tiup/storage/cluster/clusters/prod-cluster  /root/.tiup/storage/cluster/clusters/prod-cluster/ssh/id_rsa
```

## クラスタを起動します {#start-the-cluster}

クラスタが正常にデプロイされたら、次のコマンドを実行してクラスタを起動します。

{{< copyable "" >}}

```shell
tiup cluster start prod-cluster
```

クラスタの名前を忘れた場合は、 `tiup cluster list`を実行してクラスタリストを表示します。

## クラスタのステータスを確認する {#check-the-cluster-status}

TiUPは、クラスタの各コンポーネントのステータスを表示するための`tiup cluster display`のコマンドを提供します。このコマンドを使用すると、コンポーネントのステータスを確認するために各マシンにログインする必要はありません。コマンドの使用法は次のとおりです。

{{< copyable "" >}}

```bash
tiup cluster display prod-cluster
```

```
Starting /root/.tiup/components/cluster/v1.9.0/cluster display prod-cluster
TiDB Cluster: prod-cluster
TiDB Version: v5.4.1
ID                  Role        Host          Ports        Status     Data Dir              Deploy Dir
--                  ----        ----          -----        ------     --------              ----------
172.16.5.134:3000   grafana     172.16.5.134  3000         Up         -                     deploy/grafana-3000
172.16.5.134:2379   pd          172.16.5.134  2379/2380    Up|L       data/pd-2379          deploy/pd-2379
172.16.5.139:2379   pd          172.16.5.139  2379/2380    Up|UI      data/pd-2379          deploy/pd-2379
172.16.5.140:2379   pd          172.16.5.140  2379/2380    Up         data/pd-2379          deploy/pd-2379
172.16.5.134:9090   prometheus  172.16.5.134  9090         Up         data/prometheus-9090  deploy/prometheus-9090
172.16.5.134:4000   tidb        172.16.5.134  4000/10080   Up         -                     deploy/tidb-4000
172.16.5.139:4000   tidb        172.16.5.139  4000/10080   Up         -                     deploy/tidb-4000
172.16.5.140:4000   tidb        172.16.5.140  4000/10080   Up         -                     deploy/tidb-4000
172.16.5.134:20160  tikv        172.16.5.134  20160/20180  Up         data/tikv-20160       deploy/tikv-20160
172.16.5.139:20160  tikv        172.16.5.139  20160/20180  Up         data/tikv-20160       deploy/tikv-20160
172.16.5.140:20160  tikv        172.16.5.140  20160/20180  Up         data/tikv-20160       deploy/tikv-20160
```

`Status`列は、サービスが正常に実行されているかどうかを示すために`Up`または`Down`を使用します。

PDコンポーネントの場合、 `|L`または`|UI`が`Up`または`Down`に追加される場合があります。 `|L`はPDノードがリーダーであることを示し、 `|UI`は[TiDBダッシュボード](/dashboard/dashboard-intro.md)がPDノードで実行されていることを示します。

## クラスタでのスケーリング {#scale-in-a-cluster}

> **ノート：**
>
> このセクションでは、scale-inコマンドの構文についてのみ説明します。オンラインスケーリングの詳細な手順については、 [TiUPを使用してTiDBクラスターをスケーリングする](/scale-tidb-using-tiup.md)を参照してください。

クラスタでのスケーリングとは、一部のノードをオフラインにすることを意味します。この操作により、特定のノードがクラスタから削除され、残りのファイルが削除されます。

TiKVおよびTiDBBinlogコンポーネントのオフラインプロセスは非同期であり（APIを介してノードを削除する必要があります）、プロセスに時間がかかるため（ノードが正常にオフラインになるかどうかを継続的に監視する必要があります）、特別な処理が行われます。 TiKVおよびTiDBBinlogコンポーネント。

-   TiKVおよびBinlogの場合：

    -   TiUPクラスタは、APIを介してノードをオフラインにし、プロセスが完了するのを待たずに直接終了します。
    -   その後、クラスタ操作に関連するコマンドが実行されると、TiUPクラスタはオフラインにされたTiKV/Binlogノードがあるかどうかを調べます。そうでない場合、TiUPクラスタは指定された操作を続行します。存在する場合、TiUPクラスタは次の手順を実行します。

        1.  オフラインになったノードのサービスを停止します。
        2.  ノードに関連するデータファイルをクリーンアップします。
        3.  クラスタトポロジからノードを削除します。

-   その他のコンポーネントの場合：

    -   PDコンポーネントを停止すると、TiUPクラスタはAPIを介してクラスタから指定されたノードをすばやく削除し、指定されたPDノードのサービスを停止し、関連するデータファイルを削除します。
    -   他のコンポーネントを停止すると、TiUPクラスタはノードサービスを直接停止し、関連するデータファイルを削除します。

scale-inコマンドの基本的な使用法：

```bash
tiup cluster scale-in <cluster-name> -N <node-id>
```

このコマンドを使用するには、クラスタ名とノードIDの少なくとも2つのフラグを指定する必要があります。ノードIDは、前のセクションの`tiup cluster display`コマンドを使用して取得できます。

たとえば、 `172.16.5.140`のTiKVノードをオフラインにするには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
tiup cluster scale-in prod-cluster -N 172.16.5.140:20160
```

`tiup cluster display`を実行すると、TiKVノードが`Offline`とマークされていることがわかります。

{{< copyable "" >}}

```bash
tiup cluster display prod-cluster
```

```
Starting /root/.tiup/components/cluster/v1.9.0/cluster display prod-cluster
TiDB Cluster: prod-cluster
TiDB Version: v5.4.1
ID                  Role        Host          Ports        Status     Data Dir              Deploy Dir
--                  ----        ----          -----        ------     --------              ----------
172.16.5.134:3000   grafana     172.16.5.134  3000         Up         -                     deploy/grafana-3000
172.16.5.134:2379   pd          172.16.5.134  2379/2380    Up|L       data/pd-2379          deploy/pd-2379
172.16.5.139:2379   pd          172.16.5.139  2379/2380    Up|UI      data/pd-2379          deploy/pd-2379
172.16.5.140:2379   pd          172.16.5.140  2379/2380    Up         data/pd-2379          deploy/pd-2379
172.16.5.134:9090   prometheus  172.16.5.134  9090         Up         data/prometheus-9090  deploy/prometheus-9090
172.16.5.134:4000   tidb        172.16.5.134  4000/10080   Up         -                     deploy/tidb-4000
172.16.5.139:4000   tidb        172.16.5.139  4000/10080   Up         -                     deploy/tidb-4000
172.16.5.140:4000   tidb        172.16.5.140  4000/10080   Up         -                     deploy/tidb-4000
172.16.5.134:20160  tikv        172.16.5.134  20160/20180  Up         data/tikv-20160       deploy/tikv-20160
172.16.5.139:20160  tikv        172.16.5.139  20160/20180  Up         data/tikv-20160       deploy/tikv-20160
172.16.5.140:20160  tikv        172.16.5.140  20160/20180  Offline    data/tikv-20160       deploy/tikv-20160
```

PDがノード上のデータを他のTiKVノードにスケジュールした後、このノードは自動的に削除されます。

## クラスタをスケールアウトする {#scale-out-a-cluster}

> **ノート：**
>
> このセクションでは、scale-outコマンドの構文についてのみ説明します。オンラインスケーリングの詳細な手順については、 [TiUPを使用してTiDBクラスターをスケーリングする](/scale-tidb-using-tiup.md)を参照してください。

スケールアウト操作には、展開と同様の内部ロジックがあります。TiUPクラスタコンポーネントは、最初にノードのSSH接続を確認し、ターゲットノードに必要なディレクトリを作成してから、展開操作を実行し、ノードサービスを開始します。

PDをスケールアウトすると、ノードが`join`クラスタに追加され、PDに関連付けられているサービスの構成が更新されます。他のサービスをスケールアウトすると、サービスが直接開始され、クラスタに追加されます。

すべてのサービスは、スケールアウト時に正確性の検証を実行します。検証結果は、スケールアウトが成功したかどうかを示します。

`tidb-test`のクラスタにTiKVノードとPDノードを追加するには、次の手順を実行します。

1.  `scale.yaml`のファイルを作成し、新しいTiKVおよびPDノードのIPを追加します。

    > **ノート：**
    >
    > トポロジファイルを作成する必要があります。このファイルには、既存のノードではなく、新しいノードの説明のみが含まれています。

    ```yaml
    ---

    pd_servers:
      - ip: 172.16.5.140

    tikv_servers:
      - ip: 172.16.5.140
    ```

2.  スケールアウト操作を実行します。 TiUPクラスタは、ポート、ディレクトリ、および`scale.yaml`で説明されているその他の情報に従って、対応するノードをクラスタに追加します。

    {{< copyable "" >}}

    ```shell
    tiup cluster scale-out tidb-test scale.yaml
    ```

    コマンドの実行後、 `tiup cluster display tidb-test`を実行することにより、スケールアウトされたクラスタのステータスを確認できます。

## ローリングアップグレード {#rolling-upgrade}

> **ノート：**
>
> このセクションでは、upgradeコマンドの構文についてのみ説明します。オンラインアップグレードの詳細な手順については、 [TiUPを使用してTiDBをアップグレードする](/upgrade-tidb-using-tiup.md)を参照してください。

ローリングアップグレード機能は、TiDBの分散機能を活用します。アップグレードプロセスは、アプリケーションに対して可能な限り透過的に行われ、ビジネスに影響を与えません。

アップグレードの前に、TiUPクラスタは各コンポーネントの構成ファイルが妥当であるかどうかをチェックします。その場合、コンポーネントはノードごとにアップグレードされます。そうでない場合、TiUPはエラーを報告して終了します。操作はノードによって異なります。

### さまざまなノードの操作 {#operations-for-different-nodes}

-   PDノードをアップグレードします

    -   まず、非リーダーノードをアップグレードします。
    -   すべての非リーダーノードがアップグレードされたら、リーダーノードをアップグレードします。
        -   アップグレードツールは、リーダーをすでにアップグレードされたノードに移行するコマンドをPDに送信します。
        -   リーダーの役割が別のノードに切り替えられたら、前のリーダーノードをアップグレードします。
    -   アップグレード中に、異常なノードが検出された場合、ツールはこのアップグレード操作を停止して終了します。原因を手動で分析し、問題を修正して、アップグレードを再実行する必要があります。

-   TiKVノードをアップグレードします

    -   まず、このTiKVノードのリージョンリーダーを移行するスケジューリング操作をPDに追加します。これにより、アップグレードプロセスがビジネスに影響を与えないことが保証されます。
    -   リーダーが移行されたら、このTiKVノードをアップグレードします。
    -   アップグレードされたTiKVが正常に開始されたら、リーダーのスケジュールを削除します。

-   他のサービスをアップグレードする

    -   サービスを正常に停止し、ノードを更新します。

### アップグレードコマンド {#upgrade-command}

upgradeコマンドのフラグは次のとおりです。

```bash
Usage:
  cluster upgrade <cluster-name> <version> [flags]

Flags:
      --force                  Force upgrade won't transfer leader
  -h, --help                   help for upgrade
      --transfer-timeout int   Timeout in seconds when transferring PD and TiKV store leaders (default 300)

Global Flags:
      --native-ssh        Use the system's native SSH client
      --wait-timeout int  Timeout of waiting the operation
      --ssh-timeout int   Timeout in seconds to connect host via SSH, ignored for operations that don't need an SSH connection. (default 5)
  -y, --yes               Skip all confirmations and assumes 'yes'
```

たとえば、次のコマンドはクラスタをv5.4.1にアップグレードします。

{{< copyable "" >}}

```bash
tiup cluster upgrade tidb-test v5.4.1
```

## 構成を更新する {#update-configuration}

コンポーネント構成を動的に更新する場合、TiUPクラスタコンポーネントは各クラスタの現在の構成を保存します。この構成を編集するには、 `tiup cluster edit-config <cluster-name>`コマンドを実行します。例えば：

{{< copyable "" >}}

```bash
tiup cluster edit-config prod-cluster
```

TiUPクラスタは、viエディターで構成ファイルを開きます。他のエディターを使用する場合は、 `EDITOR`環境変数を使用して、 `export EDITOR=nano`などのエディターをカスタマイズします。

ファイルを編集した後、変更を保存します。新しい構成をクラスタに適用するには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
tiup cluster reload prod-cluster
```

このコマンドは、構成をターゲットマシンに送信し、クラスタを再起動して構成を有効にします。

> **ノート：**
>
> コンポーネントを監視する場合は、 `tiup cluster edit-config`コマンドを実行して構成をカスタマイズし、対応するインスタンスにカスタム構成パスを追加します。例えば：

```yaml
---

grafana_servers:
  - host: 172.16.5.134
    dashboard_dir: /path/to/local/dashboards/dir

monitoring_servers:
  - host: 172.16.5.134
    rule_dir: /path/to/local/rules/dir

alertmanager_servers:
  - host: 172.16.5.134
    config_file: /path/to/local/alertmanager.yml
```

指定されたパスの下にあるファイルのコンテンツとフォーマットの要件は次のとおりです。

-   `grafana_servers`の`dashboard_dir`フィールドで指定されたフォルダーには、完全な`*.json`のファイルが含まれている必要があります。
-   `monitoring_servers`の`rule_dir`フィールドで指定されたフォルダーには、完全な`*.rules.yml`のファイルが含まれている必要があります。
-   `alertmanager_servers`の`config_file`フィールドで指定されるファイルの形式については、 [Alertmanager構成テンプレート](https://github.com/pingcap/tiup/blob/master/embed/templates/config/alertmanager.yml)を参照してください。

`tiup reload`を実行すると、TiUPは最初にターゲットマシン内のすべての古い構成ファイルを削除し、次に対応する構成をコントロールマシンからターゲットマシンの対応する構成ディレクトリにアップロードします。したがって、特定の構成ファイルを変更する場合は、すべての構成ファイル（変更されていないものを含む）が同じディレクトリーにあることを確認してください。たとえば、Grafanaの`tidb.json`ファイルを変更するには、最初に`*.json`のファイルすべてをGrafanaの`dashboards`ディレクトリからローカルディレクトリにコピーする必要があります。そうしないと、他のJSONファイルがターゲットマシンから失われます。

> **ノート：**
>
> `grafana_servers`の`dashboard_dir`フィールドを構成した場合は、 `tiup cluster rename`コマンドを実行してクラスタの名前を変更した後、次の操作を完了する必要があります。
>
> 1.  ローカル`dashboards`ディレクトリで、クラスタ名を新しいクラスタ名に変更します。
> 2.  ローカル`dashboards`ディレクトリで、 `datasource`を新しいクラスタ名に変更します`datasource`はクラスタ名にちなんで名付けられているためです。
> 3.  `tiup cluster reload -R grafana`コマンドを実行します。

## コンポーネントを更新 {#update-component}

通常のアップグレードでは、 `upgrade`コマンドを使用できます。ただし、デバッグなどの一部のシナリオでは、現在実行中のコンポーネントを一時パッケージに置き換える必要がある場合があります。これを実現するには、次の`patch`のコマンドを使用します。

{{< copyable "" >}}

```bash
tiup cluster patch --help
```

```
Replace the remote package with a specified package and restart the service

Usage:
  cluster patch <cluster-name> <package-path> [flags]

Flags:
  -h, --help                   help for patch
  -N, --node strings           Specify the nodes
      --overwrite              Use this package in the future scale-out operations
  -R, --role strings           Specify the role
      --transfer-timeout int   Timeout in seconds when transferring PD and TiKV store leaders (default 300)

Global Flags:
      --native-ssh        Use the system's native SSH client
      --wait-timeout int  Timeout of waiting the operation
      --ssh-timeout int   Timeout in seconds to connect host via SSH, ignored for operations that don't need an SSH connection. (default 5)
  -y, --yes               Skip all confirmations and assumes 'yes'
```

TiDBホットフィックスパッケージが`/tmp/tidb-hotfix.tar.gz`に含まれていて、クラスタのすべてのTiDBパッケージを置き換える場合は、次のコマンドを実行します。

{{< copyable "" >}}

```bash
tiup cluster patch test-cluster /tmp/tidb-hotfix.tar.gz -R tidb
```

クラスタの1つのTiDBパッケージのみを置き換えることもできます。

{{< copyable "" >}}

```bash
tiup cluster patch test-cluster /tmp/tidb-hotfix.tar.gz -N 172.16.4.5:4000
```

## TiDBAnsibleクラスタをインポートする {#import-tidb-ansible-cluster}

> **ノート：**
>
> 現在、TiSparkに対するTiUPクラスターのサポートはまだ**実験的**段階です。 TiSparkが有効になっているTiDBクラスタのインポートはサポートされていません。

TiUPがリリースされる前は、TiDBAnsibleを使用してTiDBクラスターをデプロイすることがよくあります。 TiUPがTiDBAnsibleによってデプロイされたクラスタを引き継ぐことができるようにするには、 `import`コマンドを使用します。

`import`コマンドの使用法は次のとおりです。

{{< copyable "" >}}

```bash
tiup cluster import --help
```

```
Import an exist TiDB cluster from TiDB-Ansible

Usage:
  cluster import [flags]

Flags:
  -d, --dir string         The path to TiDB-Ansible directory
  -h, --help               help for import
      --inventory string   The name of inventory file (default "inventory.ini")
      --no-backup          Don't backup ansible dir, useful when there're multiple inventory files
  -r, --rename NAME        Rename the imported cluster to NAME

Global Flags:
      --native-ssh        Use the system's native SSH client
      --wait-timeout int  Timeout of waiting the operation
      --ssh-timeout int   Timeout in seconds to connect host via SSH, ignored for operations that don't need an SSH connection. (default 5)
  -y, --yes               Skip all confirmations and assumes 'yes'
```

次のコマンドのいずれかを使用して、TiDBAnsibleクラスタをインポートできます。

{{< copyable "" >}}

```bash
cd tidb-ansible
tiup cluster import
```

{{< copyable "" >}}

```bash
tiup cluster import --dir=/path/to/tidb-ansible
```

## 操作ログを表示する {#view-the-operation-log}

操作ログを表示するには、 `audit`コマンドを使用します。 `audit`コマンドの使用法は次のとおりです。

```bash
Usage:
  tiup cluster audit [audit-id] [flags]

Flags:
  -h, --help   help for audit
```

`[audit-id]`フラグが指定されていない場合、コマンドは実行されたコマンドのリストを表示します。例えば：

{{< copyable "" >}}

```bash
tiup cluster audit
```

```
Starting component `cluster`: /home/tidb/.tiup/components/cluster/v1.9.0/cluster audit
ID      Time                       Command
--      ----                       -------
4BLhr0  2022-05-13T13:25:09+08:00  /home/tidb/.tiup/components/cluster/v1.9.0/cluster deploy test v5.4.1 /tmp/topology.yaml
4BKWjF  2022-05-13T23:36:57+08:00  /home/tidb/.tiup/components/cluster/v1.9.0/cluster deploy test v5.4.1 /tmp/topology.yaml
4BKVwH  2022-05-13T23:02:08+08:00  /home/tidb/.tiup/components/cluster/v1.9.0/cluster deploy test v5.4.1 /tmp/topology.yaml
4BKKH1  2022-05-13T16:39:04+08:00  /home/tidb/.tiup/components/cluster/v1.9.0/cluster destroy test
4BKKDx  2022-05-13T16:36:57+08:00  /home/tidb/.tiup/components/cluster/v1.9.0/cluster deploy test v5.4.1 /tmp/topology.yaml
```

最初の列は`audit-id`です。特定のコマンドの実行ログを表示するには、次のようにコマンドの`audit-id`をフラグとして渡します。

{{< copyable "" >}}

```bash
tiup cluster audit 4BLhr0
```

## TiDBクラスタのホストでコマンドを実行する {#run-commands-on-a-host-in-the-tidb-cluster}

TiDBクラスタのホストでコマンドを実行するには、 `exec`コマンドを使用します。 `exec`コマンドの使用法は次のとおりです。

```bash
Usage:
  cluster exec <cluster-name> [flags]

Flags:
      --command string   the command run on cluster host (default "ls")
  -h, --help             help for exec
  -N, --node strings     Only exec on host with specified nodes
  -R, --role strings     Only exec on host with specified roles
      --sudo             use root permissions (default false)

Global Flags:
      --ssh-timeout int   Timeout in seconds to connect host via SSH, ignored for operations that don't need an SSH connection. (default 5)
  -y, --yes               Skip all confirmations and assumes 'yes'
```

たとえば、すべてのTiDBノードで`ls /tmp`を実行するには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
tiup cluster exec test-cluster --command='ls /tmp'
```

## クラスターコントローラー {#cluster-controllers}

`tikv-ctl`がリリースされる前は、 `tidb-ctl` 、およびその他のツールを使用してクラスタを制御でき`pd-ctl` 。ツールのダウンロードと使用を容易にするために、TiUPはツールをオールインワンコンポーネントに統合します`ctl` 。

```bash
Usage:
  tiup ctl {tidb/pd/tikv/binlog/etcd} [flags]

Flags:
  -h, --help   help for tiup
```

このコマンドは、以前のツールのコマンドと対応する関係があります。

```bash
tidb-ctl [args] = tiup ctl tidb [args]
pd-ctl [args] = tiup ctl pd [args]
tikv-ctl [args] = tiup ctl tikv [args]
binlogctl [args] = tiup ctl bindlog [args]
etcdctl [args] = tiup ctl etcd [args]
```

たとえば、以前に`pd-ctl -u http://127.0.0.1:2379 store`を実行してストアを表示していた場合、TiUPで次のコマンドを実行できるようになりました。

{{< copyable "" >}}

```bash
tiup ctl pd -u http://127.0.0.1:2379 store
```

## ターゲットマシンの環境チェック {#environment-checks-for-target-machines}

`check`コマンドを使用して、ターゲットマシンの環境に対して一連のチェックを実行し、チェック結果を出力できます。 `check`コマンドを実行することにより、一般的な不合理な構成またはサポートされていない状況を見つけることができます。コマンドフラグリストは次のとおりです。

```bash
Usage:
  tiup cluster check <topology.yml | cluster-name> [flags]
Flags:
      --apply                  Try to fix failed checks
      --cluster                Check existing cluster, the input is a cluster name.
      --enable-cpu             Enable CPU thread count check
      --enable-disk            Enable disk IO (fio) check
      --enable-mem             Enable memory size check
  -h, --help                   help for check
  -i, --identity_file string   The path of the SSH identity file. If specified, public key authentication will be used.
  -p, --password               Use password of target hosts. If specified, password authentication will be used.
      --user string            The user name to login via SSH. The user must has root (or sudo) privilege.
```

デフォルトでは、このコマンドは展開前に環境をチェックするために使用されます。 `--cluster`フラグを指定してモードを切り替えることにより、既存のクラスタのターゲットマシンを確認することもできます。次に例を示します。

```bash
# check deployed servers before deployment
tiup cluster check topology.yml --user tidb -p
# check deployed servers of an existing cluster
tiup cluster check <cluster-name> --cluster
```

CPUスレッド数チェック、メモリサイズチェック、およびディスクパフォーマンスチェックはデフォルトで無効になっています。実稼働環境では、3つのチェックを有効にし、それらが合格して最高のパフォーマンスが得られることを確認することをお勧めします。

-   CPU：スレッド数が16以上の場合、チェックに合格します。
-   メモリ：物理メモリの合計サイズが32 GB以上の場合、チェックに合格します。
-   ディスク： `data_dir`のパーティションで`fio`のテストを実行し、結果を記録します。

チェックを実行するときに、 `--apply`フラグが指定されている場合、プログラムは失敗したアイテムを自動的に修復します。自動修復は、構成またはシステムパラメータを変更することで調整できる一部の項目に制限されています。その他の未修理品は、実情に応じて手作業で取り扱う必要があります。

クラスタをデプロイするために環境チェックは必要ありません。実稼働環境では、展開前に環境チェックを実行し、すべてのチェック項目に合格することをお勧めします。すべてのチェック項目に合格しなかった場合、クラスタは正常にデプロイおよび実行される可能性がありますが、最高のパフォーマンスが得られない可能性があります。

## システムのネイティブSSHクライアントを使用してクラスタに接続します {#use-the-system-s-native-ssh-client-to-connect-to-cluster}

クラスタマシンで実行される上記のすべての操作は、TiUPに組み込まれたSSHクライアントを使用してクラスタに接続し、コマンドを実行します。ただし、シナリオによっては、このようなクラスタ操作を実行するために、制御マシンシステムにネイティブなSSHクライアントを使用する必要がある場合もあります。例えば：

-   認証にSSHプラグインを使用するには
-   カスタマイズされたSSHクライアントを使用するには

次に、 `--native-ssh`コマンドラインフラグを使用して、システムネイティブのコマンドラインツールを有効にします。

-   クラスタのデプロイ： `tiup cluster deploy <cluster-name> <version> <topo> --native-ssh`
-   クラスタを開始します： `tiup cluster start <cluster-name> --native-ssh`
-   クラスタのアップグレード： `tiup cluster upgrade ... --native-ssh`

上記のすべてのクラスタ操作コマンドに`--native-ssh`を追加して、システムのネイティブSSHクライアントを使用できます。

すべてのコマンドにこのようなフラグが追加されないようにするには、 `TIUP_NATIVE_SSH`システム変数を使用して、ローカルSSHクライアントを使用するかどうかを指定できます。

```shell
export TIUP_NATIVE_SSH=true
# or
export TIUP_NATIVE_SSH=1
# or
export TIUP_NATIVE_SSH=enable
```

この環境変数と`--native-ssh`を同時に指定すると、 `--native-ssh`の優先度が高くなります。

> **ノート：**
>
> クラスタ展開のプロセス中に、接続にパスワードを使用する必要がある場合（ `-p` ）、またはキーファイルに`passphrase`が設定されている場合は、 `sshpass`が制御マシンにインストールされていることを確認する必要があります。それ以外の場合は、タイムアウトエラーが報告されます。

## 制御マシンを移行し、TiUPデータをバックアップします {#migrate-control-machine-and-back-up-tiup-data}

TiUPデータは、ユーザーのホームディレクトリの`.tiup`ディレクトリに保存されます。コントロールマシンを移行するには、次の手順を実行して、 `.tiup`ディレクトリを対応するターゲットマシンにコピーします。

1.  元のマシンのホームディレクトリで`tar czvf tiup.tar.gz .tiup`を実行します。
2.  `tiup.tar.gz`をターゲットマシンのホームディレクトリにコピーします。
3.  ターゲットマシンのホームディレクトリで`tar xzvf tiup.tar.gz`を実行します。
4.  `.tiup`のディレクトリを`PATH`の環境変数に追加します。

    `bash`を使用し、 `tidb`ユーザーの場合、 `~/.bashrc`に`export PATH=/home/tidb/.tiup/bin:$PATH`を追加して、 `source ~/.bashrc`を実行できます。次に、使用するシェルとユーザーに応じて、対応する調整を行います。

> **ノート：**
>
> 制御マシンのディスク損傷などの異常な状態によって引き起こされるTiUPデータの損失を回避するために、 `.tiup`のディレクトリを定期的にバックアップすることをお勧めします。
