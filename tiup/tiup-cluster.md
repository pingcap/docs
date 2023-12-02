---
title: Deploy and Maintain an Online TiDB Cluster Using TiUP
summary: Learns how to deploy and maintain an online TiDB cluster using TiUP.
---

# TiUPを使用したオンライン TiDBクラスタのデプロイと管理 {#deploy-and-maintain-an-online-tidb-cluster-using-tiup}

このドキュメントでは、 TiUPクラスターコンポーネントの使用方法に焦点を当てます。オンライン展開の完全な手順については、 [TiUPを使用した TiDBクラスタのデプロイ](/production-deployment-using-tiup.md)を参照してください。

ローカル テスト デプロイメントに使用される[TiUPプレイグラウンドコンポーネント](/tiup/tiup-playground.md)と同様に、 TiUPクラスターコンポーネントは、本番環境に TiDB を迅速にデプロイします。 Playground と比較して、クラスターコンポーネントは、アップグレード、スケーリング、さらには操作や監査など、より強力な本番クラスター管理機能を提供します。

クラスターコンポーネントのヘルプ情報を表示するには、次のコマンドを実行します。

```bash
tiup cluster
```

    Starting component `cluster`: /home/tidb/.tiup/components/cluster/v1.12.3/cluster
    Deploy a TiDB cluster for production

    Usage:
      tiup cluster [command]

    Available Commands:
      check       Precheck a cluster
      deploy      Deploy a cluster for production
      start       Start a TiDB cluster
      stop        Stop a TiDB cluster
      restart     Restart a TiDB cluster
      scale-in    Scale in a TiDB cluster
      scale-out   Scale out a TiDB cluster
      destroy     Destroy a specified cluster
      clean       (Experimental) Clean up a specified cluster
      upgrade     Upgrade a specified TiDB cluster
      display     Display information of a TiDB cluster
      list        List all clusters
      audit       Show audit log of cluster operation
      import      Import an existing TiDB cluster from TiDB-Ansible
      edit-config Edit TiDB cluster config
      reload      Reload a TiDB cluster's config and restart if needed
      patch       Replace the remote package with a specified package and restart the service
      help        Help about any command

    Flags:
      -c, --concurrency int     Maximum number of concurrent tasks allowed (defaults to `5`)
          --format string       (EXPERIMENTAL) The format of output, available values are [default, json] (default "default")
      -h, --help                help for tiup
          --ssh string          (Experimental) The executor type. Optional values are 'builtin', 'system', and 'none'.
          --ssh-timeout uint    Timeout in seconds to connect a host via SSH. Operations that don't need an SSH connection are ignored. (default 5)
      -v, --version            TiUP version
          --wait-timeout uint   Timeout in seconds to wait for an operation to complete. Inapplicable operations are ignored. (defaults to `120`)
      -y, --yes                 Skip all confirmations and assumes 'yes'

## クラスターをデプロイ {#deploy-the-cluster}

クラスターをデプロイするには、 `tiup cluster deploy`コマンドを実行します。コマンドの使用方法は次のとおりです。

```bash
tiup cluster deploy <cluster-name> <version> <topology.yaml> [flags]
```

このコマンドでは、クラスター名、TiDB クラスターのバージョン ( `v7.5.0`など)、およびクラスターのトポロジー ファイルを指定する必要があります。

トポロジ ファイルを作成するには、 [例](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml)を参照してください。次のファイルは、最も単純なトポロジの例です。

> **注記：**
>
> TiUPクラスターコンポーネントがデプロイメントとスケーリングに使用するトポロジ ファイルは[ヤムル](https://yaml.org/spec/1.2/spec.html)構文を使用して記述されているため、インデントが正しいことを確認してください。

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

tiflash_servers:
  - host: 172.16.5.141
  - host: 172.16.5.142
  - host: 172.16.5.143

grafana_servers:
  - host: 172.16.5.134

monitoring_servers:
  - host: 172.16.5.134
```

デフォルトでは、 TiUP はamd64アーキテクチャ上で実行されるバイナリ ファイルとしてデプロイされます。ターゲット マシンが arm64アーキテクチャの場合は、トポロジ ファイルで構成できます。

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

ファイルを`/tmp/topology.yaml`として保存します。 TiDB v7.5.0 を使用し、クラスター名が`prod-cluster`場合は、次のコマンドを実行します。

```shell
tiup cluster deploy -p prod-cluster v7.5.0 /tmp/topology.yaml
```

実行中、 TiUP はトポロジを再度確認するように求め、ターゲット マシンの root パスワードを要求します ( `-p`フラグはパスワードの入力を意味します)。

```bash
Please confirm your topology:
TiDB Cluster: prod-cluster
TiDB Version: v7.5.0
Type        Host          Ports                            OS/Arch       Directories
----        ----          -----                            -------       -----------
pd          172.16.5.134  2379/2380                        linux/x86_64  deploy/pd-2379,data/pd-2379
pd          172.16.5.139  2379/2380                        linux/x86_64  deploy/pd-2379,data/pd-2379
pd          172.16.5.140  2379/2380                        linux/x86_64  deploy/pd-2379,data/pd-2379
tikv        172.16.5.134  20160/20180                      linux/x86_64  deploy/tikv-20160,data/tikv-20160
tikv        172.16.5.139  20160/20180                      linux/x86_64  deploy/tikv-20160,data/tikv-20160
tikv        172.16.5.140  20160/20180                      linux/x86_64  deploy/tikv-20160,data/tikv-20160
tidb        172.16.5.134  4000/10080                       linux/x86_64  deploy/tidb-4000
tidb        172.16.5.139  4000/10080                       linux/x86_64  deploy/tidb-4000
tidb        172.16.5.140  4000/10080                       linux/x86_64  deploy/tidb-4000
tiflash     172.16.5.141  9000/8123/3930/20170/20292/8234  linux/x86_64  deploy/tiflash-9000,data/tiflash-9000
tiflash     172.16.5.142  9000/8123/3930/20170/20292/8234  linux/x86_64  deploy/tiflash-9000,data/tiflash-9000
tiflash     172.16.5.143  9000/8123/3930/20170/20292/8234  linux/x86_64  deploy/tiflash-9000,data/tiflash-9000
prometheus  172.16.5.134  9090         deploy/prometheus-9090,data/prometheus-9090
grafana     172.16.5.134  3000         deploy/grafana-3000
Attention:
    1. If the topology is not what you expected, check your yaml file.
    2. Please confirm there is no port/directory conflicts in same host.
Do you want to continue? [y/N]:
```

パスワードを入力すると、 TiUPクラスターは必要なコンポーネントをダウンロードし、対応するマシンに展開します。次のメッセージが表示されたら、デプロイは成功です。

```bash
Deployed cluster `prod-cluster` successfully
```

## クラスターリストをビュー {#view-the-cluster-list}

クラスターが正常にデプロイされたら、次のコマンドを実行してクラスターのリストを表示します。

```bash
tiup cluster list
```

    Starting /root/.tiup/components/cluster/v1.12.3/cluster list
    Name          User  Version    Path                                               PrivateKey
    ----          ----  -------    ----                                               ----------
    prod-cluster  tidb  v7.5.0    /root/.tiup/storage/cluster/clusters/prod-cluster  /root/.tiup/storage/cluster/clusters/prod-cluster/ssh/id_rsa

## クラスターを開始する {#start-the-cluster}

クラスターが正常にデプロイされたら、次のコマンドを実行してクラスターを起動します。

```shell
tiup cluster start prod-cluster
```

クラスターの名前を忘れた場合は、 `tiup cluster list`を実行してクラスターのリストを表示します。

TiUP は`systemd`を使用してデーモン プロセスを開始します。プロセスが予期せず終了した場合、15 秒後にプルアップされます。

## クラスターのステータスを確認する {#check-the-cluster-status}

TiUP には、クラスター内の各コンポーネントのステータスを表示するコマンドが`tiup cluster display`あります。このコマンドを使用すると、コンポーネントのステータスを確認するために各マシンにログインする必要がなくなります。コマンドの使用方法は次のとおりです。

```bash
tiup cluster display prod-cluster
```

    Starting /root/.tiup/components/cluster/v1.12.3/cluster display prod-cluster
    TiDB Cluster: prod-cluster
    TiDB Version: v7.5.0
    ID                  Role        Host          Ports                            OS/Arch       Status  Data Dir              Deploy Dir
    --                  ----        ----          -----                            -------       ------  --------              ----------
    172.16.5.134:3000   grafana     172.16.5.134  3000                             linux/x86_64  Up      -                     deploy/grafana-3000
    172.16.5.134:2379   pd          172.16.5.134  2379/2380                        linux/x86_64  Up|L    data/pd-2379          deploy/pd-2379
    172.16.5.139:2379   pd          172.16.5.139  2379/2380                        linux/x86_64  Up|UI   data/pd-2379          deploy/pd-2379
    172.16.5.140:2379   pd          172.16.5.140  2379/2380                        linux/x86_64  Up      data/pd-2379          deploy/pd-2379
    172.16.5.134:9090   prometheus  172.16.5.134  9090                             linux/x86_64  Up      data/prometheus-9090  deploy/prometheus-9090
    172.16.5.134:4000   tidb        172.16.5.134  4000/10080                       linux/x86_64  Up      -                     deploy/tidb-4000
    172.16.5.139:4000   tidb        172.16.5.139  4000/10080                       linux/x86_64  Up      -                     deploy/tidb-4000
    172.16.5.140:4000   tidb        172.16.5.140  4000/10080                       linux/x86_64  Up      -                     deploy/tidb-4000
    172.16.5.141:9000   tiflash     172.16.5.141  9000/8123/3930/20170/20292/8234  linux/x86_64  Up      data/tiflash-9000     deploy/tiflash-9000
    172.16.5.142:9000   tiflash     172.16.5.142  9000/8123/3930/20170/20292/8234  linux/x86_64  Up      data/tiflash-9000     deploy/tiflash-9000
    172.16.5.143:9000   tiflash     172.16.5.143  9000/8123/3930/20170/20292/8234  linux/x86_64  Up      data/tiflash-9000     deploy/tiflash-9000
    172.16.5.134:20160  tikv        172.16.5.134  20160/20180                      linux/x86_64  Up      data/tikv-20160       deploy/tikv-20160
    172.16.5.139:20160  tikv        172.16.5.139  20160/20180                      linux/x86_64  Up      data/tikv-20160       deploy/tikv-20160
    172.16.5.140:20160  tikv        172.16.5.140  20160/20180                      linux/x86_64  Up      data/tikv-20160       deploy/tikv-20160

`Status`列は、サービスが正常に実行されているかどうかを示すために`Up`または`Down`を使用します。

PDコンポーネントの場合、 `Up`または`Down`に`|L`または`|UI`が追加される場合があります。 `|L` PD ノードがLeaderであることを示し、 `|UI`は[TiDB ダッシュボード](/dashboard/dashboard-intro.md) PD ノード上で実行されていることを示します。

## クラスタースケールイン {#scale-in-a-cluster}

> **注記：**
>
> このセクションでは、スケールイン コマンドの構文のみについて説明します。オンライン スケーリングの詳細な手順については、 [TiUPを使用して TiDBクラスタをスケールする](/scale-tidb-using-tiup.md)を参照してください。

クラスター内でのスケーリングとは、一部のノードをオフラインにすることを意味します。この操作により、クラスターから特定のノードが削除され、残りのファイルが削除されます。

TiKV、 TiFlash、および TiDB Binlogコンポーネントのオフライン プロセスは非同期であり (API を介してノードを削除する必要がある)、プロセスに時間がかかるため (ノードが正常にオフラインになったかどうかを継続的に観察する必要がある)、特別な処理が必要になります。 TiKV、 TiFlash、TiDB Binlogコンポーネントに与えられます。

-   TiKV、 TiFlash、およびBinlogの場合:

    -   TiUPクラスターは API を通じてノードをオフラインにし、プロセスの完了を待たずに直接終了します。
    -   その後、クラスター操作に関連するコマンドが実行されると、 TiUPクラスターは、オフラインになった TiKV、 TiFlash、またはBinlogノードが存在するかどうかを調べます。そうでない場合、 TiUPクラスターは指定された操作を続行します。存在する場合、 TiUPクラスターは次の手順を実行します。

        1.  オフラインになったノードのサービスを停止します。
        2.  ノードに関連するデータ ファイルをクリーンアップします。
        3.  クラスタ トポロジからノードを削除します。

-   他のコンポーネントの場合:

    -   PDコンポーネントを停止すると、 TiUPクラスターは API を通じて指定されたノードをクラスターから迅速に削除し、指定された PD ノードのサービスを停止し、関連するデータ ファイルを削除します。
    -   他のコンポーネントを停止すると、 TiUPクラスターはノード サービスを直接停止し、関連するデータ ファイルを削除します。

スケールイン コマンドの基本的な使用法:

```bash
tiup cluster scale-in <cluster-name> -N <node-id>
```

このコマンドを使用するには、クラスター名とノード ID という少なくとも 2 つのフラグを指定する必要があります。ノード ID は、前のセクションの`tiup cluster display`コマンドを使用して取得できます。

たとえば、 `172.16.5.140` TiKV ノードをオフラインにするには、次のコマンドを実行します。

```bash
tiup cluster scale-in prod-cluster -N 172.16.5.140:20160
```

`tiup cluster display`を実行すると、TiKV ノードが`Offline`マークされていることを確認できます。

```bash
tiup cluster display prod-cluster
```

    Starting /root/.tiup/components/cluster/v1.12.3/cluster display prod-cluster
    TiDB Cluster: prod-cluster
    TiDB Version: v7.5.0
    ID                  Role        Host          Ports                            OS/Arch       Status   Data Dir              Deploy Dir
    --                  ----        ----          -----                            -------       ------   --------              ----------
    172.16.5.134:3000   grafana     172.16.5.134  3000                             linux/x86_64  Up       -                     deploy/grafana-3000
    172.16.5.134:2379   pd          172.16.5.134  2379/2380                        linux/x86_64  Up|L     data/pd-2379          deploy/pd-2379
    172.16.5.139:2379   pd          172.16.5.139  2379/2380                        linux/x86_64  Up|UI    data/pd-2379          deploy/pd-2379
    172.16.5.140:2379   pd          172.16.5.140  2379/2380                        linux/x86_64  Up       data/pd-2379          deploy/pd-2379
    172.16.5.134:9090   prometheus  172.16.5.134  9090                             linux/x86_64  Up       data/prometheus-9090  deploy/prometheus-9090
    172.16.5.134:4000   tidb        172.16.5.134  4000/10080                       linux/x86_64  Up       -                     deploy/tidb-4000
    172.16.5.139:4000   tidb        172.16.5.139  4000/10080                       linux/x86_64  Up       -                     deploy/tidb-4000
    172.16.5.140:4000   tidb        172.16.5.140  4000/10080                       linux/x86_64  Up       -                     deploy/tidb-4000
    172.16.5.141:9000   tiflash     172.16.5.141  9000/8123/3930/20170/20292/8234  linux/x86_64  Up       data/tiflash-9000     deploy/tiflash-9000
    172.16.5.142:9000   tiflash     172.16.5.142  9000/8123/3930/20170/20292/8234  linux/x86_64  Up       data/tiflash-9000     deploy/tiflash-9000
    172.16.5.143:9000   tiflash     172.16.5.143  9000/8123/3930/20170/20292/8234  linux/x86_64  Up       data/tiflash-9000     deploy/tiflash-9000
    172.16.5.134:20160  tikv        172.16.5.134  20160/20180                      linux/x86_64  Up       data/tikv-20160       deploy/tikv-20160
    172.16.5.139:20160  tikv        172.16.5.139  20160/20180                      linux/x86_64  Up       data/tikv-20160       deploy/tikv-20160
    172.16.5.140:20160  tikv        172.16.5.140  20160/20180                      linux/x86_64  Offline  data/tikv-20160       deploy/tikv-20160

PD がノード上のデータを他の TiKV ノードにスケジュールすると、このノードは自動的に削除されます。

## クラスターをスケールアウトする {#scale-out-a-cluster}

> **注記：**
>
> このセクションでは、スケールアウト コマンドの構文についてのみ説明します。オンライン スケーリングの詳細な手順については、 [TiUPを使用して TiDBクラスタをスケールする](/scale-tidb-using-tiup.md)を参照してください。

スケールアウト操作には、デプロイメントの内部ロジックと同様の内部ロジックがありますTiUPクラスターコンポーネントは、まずノードの SSH 接続を確保し、ターゲット ノード上に必要なディレクトリを作成してから、デプロイメント操作を実行して、ノード サービスを開始します。

PD をスケールアウトすると、ノードがクラスターに`join`追加され、PD に関連付けられたサービスの構成が更新されます。他のサービスをスケールアウトすると、サービスは直接開始され、クラスターに追加されます。

すべてのサービスは、スケールアウト時に正当性検証を実行します。検証結果には、スケールアウトが成功したかどうかが示されます。

`tidb-test`クラスターに TiKV ノードと PD ノードを追加するには、次の手順を実行します。

1.  `scale.yaml`ファイルを作成し、新しい TiKV ノードと PD ノードの IP を追加します。

    > **注記：**
    >
    > トポロジ ファイルを作成する必要があります。このファイルには、既存のノードではなく、新しいノードの説明のみが含まれます。

    ```yaml
    ---

    pd_servers:
      - host: 172.16.5.140

    tikv_servers:
      - host: 172.16.5.140
    ```

2.  スケールアウト操作を実行します。 TiUPクラスターは、 `scale.yaml`で説明したポート、ディレクトリ、およびその他の情報に従って、対応するノードをクラスターに追加します。

    ```shell
    tiup cluster scale-out tidb-test scale.yaml
    ```

    コマンドの実行後、 `tiup cluster display tidb-test`を実行してスケールアウトされたクラスターのステータスを確認できます。

## ローリングアップグレード {#rolling-upgrade}

> **注記：**
>
> このセクションでは、アップグレード コマンドの構文のみについて説明します。オンライン アップグレードの詳細な手順については、 [TiUPを使用して TiDB をアップグレードする](/upgrade-tidb-using-tiup.md)を参照してください。

ローリング アップグレード機能は、TiDB の分散機能を活用します。アップグレード プロセスはアプリケーションに対して可能な限り透過的に行われ、ビジネスには影響しません。

アップグレード前に、 TiUPクラスターは各コンポーネントの構成ファイルが合理的であるかどうかをチェックします。その場合、コンポーネントはノードごとにアップグレードされます。そうでない場合、 TiUP はエラーを報告して終了します。操作はノードによって異なります。

### さまざまなノードの操作 {#operations-for-different-nodes}

-   PD ノードをアップグレードする

    -   まず、非リーダー ノードをアップグレードします。
    -   すべての非リーダー ノードがアップグレードされたら、Leaderノードをアップグレードします。
        -   アップグレード ツールは、Leaderを既にアップグレードされたノードに移行するコマンドを PD に送信します。
        -   Leaderの役割を別のノードに切り替えた後、以前のLeaderノードをアップグレードします。
    -   アップグレード中に異常なノードが検出された場合、ツールはこのアップグレード操作を停止して終了します。原因を手動で分析し、問題を修正して、アップグレードを再度実行する必要があります。

-   TiKV ノードをアップグレードする

    -   まず、この TiKV ノードのリージョンLeaderを移行するスケジューリング操作を PD に追加します。これにより、アップグレード プロセスがビジネスに影響を与えなくなります。
    -   Leaderの移行後、この TiKV ノードをアップグレードします。
    -   アップグレードされた TiKV が正常に起動したら、Leaderのスケジュールを削除します。

-   他のサービスをアップグレードする

    -   サービスを通常に停止し、ノードを更新します。

### アップグレードコマンド {#upgrade-command}

アップグレード コマンドのフラグは次のとおりです。

```bash
Usage:
  cluster upgrade <cluster-name> <version> [flags]

Flags:
      --force                  Force upgrade won't transfer leader
  -h, --help                   help for upgrade
      --transfer-timeout int   Timeout in seconds when transferring PD and TiKV store leaders (default 600)

Global Flags:
      --ssh string          (Experimental) The executor type. Optional values are 'builtin', 'system', and 'none'.
      --wait-timeout int  Timeout of waiting the operation
      --ssh-timeout int   Timeout in seconds to connect host via SSH, ignored for operations that don't need an SSH connection. (default 5)
  -y, --yes               Skip all confirmations and assumes 'yes'
```

たとえば、次のコマンドはクラスターを v7.5.0 にアップグレードします。

```bash
tiup cluster upgrade tidb-test v7.5.0
```

## 構成を更新する {#update-configuration}

コンポーネント構成を動的に更新する場合、 TiUPクラスターコンポーネントは各クラスターの現在の構成を保存します。この構成を編集するには、 `tiup cluster edit-config <cluster-name>`コマンドを実行します。例えば：

```bash
tiup cluster edit-config prod-cluster
```

TiUPクラスターは、vi エディターで構成ファイルを開きます。他のエディターを使用する場合は、 `EDITOR`環境変数を使用してエディターをカスタマイズします ( `export EDITOR=nano`など)。

ファイルを編集した後、変更を保存します。新しい構成をクラスターに適用するには、次のコマンドを実行します。

```bash
tiup cluster reload prod-cluster
```

このコマンドは、構成をターゲット マシンに送信し、クラスターを再起動して構成を有効にします。

> **注記：**
>
> コンポーネントを監視する場合は、 `tiup cluster edit-config`コマンドを実行して、対応するインスタンスにカスタム構成パスを追加して構成をカスタマイズします。例えば：

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

指定されたパスにあるファイルの内容と形式の要件は次のとおりです。

-   `grafana_servers`の`dashboard_dir`フィールドで指定されたフォルダーには、 `*.json`ファイルがすべて含まれている必要があります。
-   `monitoring_servers`の`rule_dir`フィールドで指定されたフォルダーには、 `*.rules.yml`ファイルがすべて含まれている必要があります。
-   `alertmanager_servers`の`config_file`フィールドで指定するファイルの形式については、 [Alertmanager 構成テンプレート](https://github.com/pingcap/tiup/blob/master/embed/templates/config/alertmanager.yml)を参照してください。

`tiup reload`を実行すると、 TiUP はまずターゲット マシン内の古い設定ファイルをすべて削除し、次に、対応する設定を制御マシンからターゲット マシンの対応する設定ディレクトリにアップロードします。したがって、特定の構成ファイルを変更する場合は、すべての構成ファイル (未変更のものを含む) が同じディレクトリにあることを確認してください。たとえば、Grafana の`tidb.json`ファイルを変更するには、まず Grafana の`dashboards`ディレクトリから`*.json`ファイルすべてをローカル ディレクトリにコピーする必要があります。そうしないと、他の JSON ファイルがターゲット マシンから失われます。

> **注記：**
>
> `dashboard_dir`フィールドを`grafana_servers`に設定した場合は、 `tiup cluster rename`コマンドを実行してクラスターの名前を変更した後、次の操作を完了する必要があります。
>
> 1.  ローカル`dashboards`ディレクトリで、クラスター名を新しいクラスター名に変更します。
> 2.  ローカル`dashboards`ディレクトリで、 `datasource`はクラスター名にちなんで命名されているため、 `datasource`を新しいクラスター名に変更します。
> 3.  `tiup cluster reload -R grafana`コマンドを実行します。

## コンポーネントを更新する {#update-component}

通常のアップグレードの場合は、 `upgrade`コマンドを使用できます。ただし、デバッグなどの一部のシナリオでは、現在実行中のコンポーネントを一時パッケージに置き換える必要がある場合があります。これを実現するには、 `patch`コマンドを使用します。

```bash
tiup cluster patch --help
```

    Replace the remote package with a specified package and restart the service

    Usage:
      cluster patch <cluster-name> <package-path> [flags]

    Flags:
      -h, --help                    help for patch
      -N, --node strings            Specify the nodes
          --offline                 Patch a stopped cluster
          --overwrite               Use this package in the future scale-out operations
      -R, --role strings            Specify the roles
          --transfer-timeout uint   Timeout in seconds when transferring PD and TiKV store leaders, also for TiCDC drain one capture (default 600)

    Global Flags:
      -c, --concurrency int     max number of parallel tasks allowed (default 5)
          --format string       (EXPERIMENTAL) The format of output, available values are [default, json] (default "default")
          --ssh string          (EXPERIMENTAL) The executor type: 'builtin', 'system', 'none'.
          --ssh-timeout uint    Timeout in seconds to connect host via SSH, ignored for operations that don't need an SSH connection. (default 5)
          --wait-timeout uint   Timeout in seconds to wait for an operation to complete, ignored for operations that don't fit. (default 120)
      -y, --yes                 Skip all confirmations and assumes 'yes'

TiDB ホットフィックス パッケージが`/tmp/tidb-hotfix.tar.gz`にあり、クラスター内のすべての TiDB パッケージを置き換える場合は、次のコマンドを実行します。

```bash
tiup cluster patch test-cluster /tmp/tidb-hotfix.tar.gz -R tidb
```

クラスター内の TiDB パッケージを 1 つだけ置き換えることもできます。

```bash
tiup cluster patch test-cluster /tmp/tidb-hotfix.tar.gz -N 172.16.4.5:4000
```

## TiDB Ansible クラスターのインポート {#import-tidb-ansible-cluster}

> **注記：**
>
> 現在、 TiUPクラスターの TiSpark サポートはまだ**実験的**です。 TiSpark が有効になっている TiDB クラスターのインポートはサポートされていません。

TiUPがリリースされる前は、TiDB Ansible が TiDB クラスターのデプロイによく使用されていました。 TiDB Ansible によってデプロイされたクラスターをTiUPが引き継げるようにするには、 `import`コマンドを使用します。

`import`コマンドの使用方法は次のとおりです。

```bash
tiup cluster import --help
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
          --ssh string        (Experimental) The executor type. Optional values are 'builtin', 'system', and 'none'.
          --wait-timeout int  Timeout of waiting the operation
          --ssh-timeout int   Timeout in seconds to connect host via SSH, ignored for operations that don't need an SSH connection. (default 5)
      -y, --yes               Skip all confirmations and assumes 'yes'

次のコマンドのいずれかを使用して、TiDB Ansible クラスターをインポートできます。

```bash
cd tidb-ansible
tiup cluster import
```

```bash
tiup cluster import --dir=/path/to/tidb-ansible
```

## 操作ログをビュー {#view-the-operation-log}

操作ログを表示するには、 `audit`コマンドを使用します。 `audit`コマンドの使用方法は次のとおりです。

```bash
Usage:
  tiup cluster audit [audit-id] [flags]

Flags:
  -h, --help   help for audit
```

`[audit-id]`フラグが指定されていない場合、コマンドは実行されたコマンドのリストを表示します。例えば：

```bash
tiup cluster audit
```

    Starting component `cluster`: /home/tidb/.tiup/components/cluster/v1.12.3/cluster audit
    ID      Time                       Command
    --      ----                       -------
    4BLhr0  2023-12-01T23:55:09+08:00  /home/tidb/.tiup/components/cluster/v1.12.3/cluster deploy test v7.5.0 /tmp/topology.yaml
    4BKWjF  2023-12-01T23:36:57+08:00  /home/tidb/.tiup/components/cluster/v1.12.3/cluster deploy test v7.5.0 /tmp/topology.yaml
    4BKVwH  2023-12-01T23:02:08+08:00  /home/tidb/.tiup/components/cluster/v1.12.3/cluster deploy test v7.5.0 /tmp/topology.yaml
    4BKKH1  2023-12-01T16:39:04+08:00  /home/tidb/.tiup/components/cluster/v1.12.3/cluster destroy test
    4BKKDx  2023-12-01T16:36:57+08:00  /home/tidb/.tiup/components/cluster/v1.12.3/cluster deploy test v7.5.0 /tmp/topology.yaml

最初の列は`audit-id`です。特定のコマンドの実行ログを表示するには、次のようにコマンドの`audit-id`をフラグとして渡します。

```bash
tiup cluster audit 4BLhr0
```

## TiDB クラスター内のホストでコマンドを実行する {#run-commands-on-a-host-in-the-tidb-cluster}

TiDB クラスター内のホストでコマンドを実行するには、 `exec`コマンドを使用します。 `exec`コマンドの使用方法は次のとおりです。

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

たとえば、すべての TiDB ノードで`ls /tmp`を実行するには、次のコマンドを実行します。

```bash
tiup cluster exec test-cluster --command='ls /tmp'
```

## クラスタコントローラー {#cluster-controllers}

TiUPがリリースされる前は、 `tidb-ctl` 、 `tikv-ctl` 、 `pd-ctl` 、およびその他のツールを使用してクラスターを制御できます。ツールのダウンロードと使用を容易にするために、 TiUP はツールをオールインワンコンポーネント`ctl`に統合します。

```bash
Usage:
  tiup ctl:v<CLUSTER_VERSION> {tidb/pd/tikv/binlog/etcd} [flags]

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

たとえば、以前に`pd-ctl -u http://127.0.0.1:2379 store`を実行してストアを表示した場合は、 TiUPで次のコマンドを実行できるようになります。

```bash
tiup ctl:v<CLUSTER_VERSION> pd -u http://127.0.0.1:2379 store
```

## ターゲットマシンの環境チェック {#environment-checks-for-target-machines}

`check`コマンドを使用して、対象マシンの環境に関する一連のチェックを実行し、チェック結果を出力します。 `check`コマンドを実行すると、よくある無理な設定やサポートされていない状況を見つけることができます。コマンドフラグリストは以下のとおりです。

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

デフォルトでは、このコマンドは展開前に環境をチェックするために使用されます。 `--cluster`フラグを指定してモードを切り替えると、次のように既存のクラスターのターゲット マシンを確認することもできます。

```bash
# check deployed servers before deployment
tiup cluster check topology.yml --user tidb -p
# check deployed servers of an existing cluster
tiup cluster check <cluster-name> --cluster
```

CPU スレッド数チェック、メモリサイズチェック、ディスク パフォーマンス チェックはデフォルトでは無効になっています。本番環境では、最高のパフォーマンスを得るために 3 つのチェックを有効にし、それらが合格することを確認することをお勧めします。

-   CPU: スレッド数が 16 以上の場合、チェックはパスします。
-   メモリ: 物理メモリの合計サイズが 32 GB 以上の場合、チェックは合格します。
-   ディスク: `data_dir`のパーティションに対して`fio`テストを実行し、結果を記録します。

チェックを実行するときに`--apply`フラグが指定されている場合、プログラムは失敗した項目を自動的に修復します。自動修復は、構成またはシステム パラメータを変更することで調整できる一部の項目に限定されます。その他の未修理項目は、実際の状況に応じて手動で処理する必要があります。

クラスターの展開には環境チェックは必要ありません。本番環境の場合は、展開前に環境チェックを実行し、すべてのチェック項目に合格することをお勧めします。すべてのチェック項目に合格しない場合、クラスターは正常にデプロイおよび実行されますが、最高のパフォーマンスが得られない可能性があります。

## システムのネイティブ SSH クライアントを使用してクラスターに接続します {#use-the-system-s-native-ssh-client-to-connect-to-cluster}

クラスター マシン上で実行される上記のすべての操作は、 TiUPに組み込まれた SSH クライアントを使用してクラスターに接続し、コマンドを実行します。ただし、シナリオによっては、そのようなクラスター操作を実行するために、制御マシン システムにネイティブな SSH クライアントを使用する必要がある場合もあります。例えば：

-   認証に SSH プラグインを使用するには
-   カスタマイズされた SSH クライアントを使用するには

次に、 `--ssh=system`コマンド ライン フラグを使用して、システム ネイティブのコマンド ライン ツールを有効にします。

-   クラスターをデプロイ。 `tiup cluster deploy <cluster-name> <version> <topo> --ssh=system` . `<cluster-name>`にはクラスターの名前を、 `<version>`にはデプロイする TiDB バージョン ( `v7.5.0`など)、 `<topo>`にはトポロジ ファイルを入力します。
-   クラスターを開始します: `tiup cluster start <cluster-name> --ssh=system`
-   クラスターのアップグレード: `tiup cluster upgrade ... --ssh=system`

システムのネイティブ SSH クライアントを使用するには、上記のすべてのクラスター操作コマンドに`--ssh=system`を追加します。

すべてのコマンドにこのようなフラグを追加しないようにするには、 `TIUP_NATIVE_SSH`システム変数を使用してローカル SSH クライアントを使用するかどうかを指定します。

```shell
export TIUP_NATIVE_SSH=true
# or
export TIUP_NATIVE_SSH=1
# or
export TIUP_NATIVE_SSH=enable
```

この環境変数と`--ssh`同時に指定した場合は`--ssh`が優先されます。

> **注記：**
>
> クラスター展開のプロセス中に、接続にパスワード ( `-p` ) を使用する必要がある場合、またはキー ファイルで`passphrase`が構成されている場合は、制御マシンに`sshpass`がインストールされていることを確認する必要があります。それ以外の場合は、タイムアウト エラーが報告されます。

## 制御マシンの移行とTiUPデータのバックアップ {#migrate-control-machine-and-back-up-tiup-data}

TiUPデータは、ユーザーのホーム ディレクトリの`.tiup`ディレクトリに保存されます。制御マシンを移行するには、次の手順を実行して、ディレクトリ`.tiup`対応するターゲット マシンにコピーします。

1.  元のマシンのホーム ディレクトリで`tar czvf tiup.tar.gz .tiup`を実行します。
2.  `tiup.tar.gz`ターゲット マシンのホーム ディレクトリにコピーします。
3.  ターゲットマシンのホームディレクトリで`tar xzvf tiup.tar.gz`を実行します。
4.  `.tiup`ディレクトリを`PATH`環境変数に追加します。

    `bash`を使用し、あなたが`tidb`ユーザーである場合は、 `~/.bashrc`に`export PATH=/home/tidb/.tiup/bin:$PATH`追加して`source ~/.bashrc`を実行できます。次に、使用するシェルとユーザーに応じて、対応する調整を行います。

> **注記：**
>
> 制御マシンのディスク損傷などの異常事態によるTiUPデータの損失を避けるため、 `.tiup`ディレクトリを定期的にバックアップすることをお勧めします。

## クラスターの展開と O&amp;M のためにメタ ファイルをバックアップおよび復元する {#back-up-and-restore-meta-files-for-cluster-deployment-and-o-x26-m}

運用と保守 (O&amp;M) に使用されるメタ ファイルが失われると、 TiUPを使用したクラスターの管理は失敗します。次のコマンドを実行して、メタ ファイルを定期的にバックアップすることをお勧めします。

```bash
tiup cluster meta backup ${cluster_name}
```

メタ ファイルが失われた場合は、次のコマンドを実行して復元できます。

```bash
tiup cluster meta restore ${cluster_name} ${backup_file}
```

> **注記：**
>
> 復元操作により、現在のメタ ファイルが上書きされます。したがって、メタ ファイルが失われた場合にのみ復元することをお勧めします。
