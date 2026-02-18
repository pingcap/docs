---
title: Deploy and Maintain an Online TiDB Cluster Using TiUP
summary: TiUPを使用してオンライン TiDB クラスターを展開および保守する方法を学習します。
---

# TiUPを使用してオンライン TiDBクラスタをデプロイおよび管理 {#deploy-and-maintain-an-online-tidb-cluster-using-tiup}

このドキュメントでは、 TiUPクラスタコンポーネントの使用方法に焦点を当てています。オンライン展開の詳細な手順については、 [TiUPを使用して TiDBクラスタをデプロイ](/production-deployment-using-tiup.md)を参照してください。

ローカルテストデプロイメントで使用される[TiUP遊び場コンポーネント](/tiup/tiup-playground.md)と同様に、 TiUPクラスタコンポーネントは本番環境向けにTiDBを迅速にデプロイします。プレイグラウンドと比較して、クラスタコンポーネントはアップグレード、スケーリング、さらには運用と監査を含む、より強力な本番クラスタ管理機能を提供します。

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

このコマンドでは、クラスター名、TiDB クラスター バージョン ( `v8.5.4`など)、およびクラスターのトポロジ ファイルを指定する必要があります。

トポロジファイルを作成するには、 [例](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml)を参照してください。次のファイルは最も単純なトポロジの例です。

> **注記：**
>
> TiUPクラスターコンポーネントがデプロイメントとスケーリングに使用するトポロジ ファイルは[ヤムル](https://yaml.org/spec/1.2/spec.html)構文を使用して記述されるため、インデントが正しいことを確認してください。

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

tiproxy_servers:
  - host: 172.16.5.144

grafana_servers:
  - host: 172.16.5.134

monitoring_servers:
  - host: 172.16.5.134
```

デフォルトでは、 TiUPは amd64アーキテクチャ上で実行されるバイナリファイルとして展開されます。ターゲットマシンが arm64アーキテクチャの場合は、トポロジファイルで設定できます。

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

ファイルを`/tmp/topology.yaml`として保存します。TiDB v8.5.4 を使用し、クラスター名が`prod-cluster`の場合は、次のコマンドを実行します。

```shell
tiup cluster deploy -p prod-cluster v8.5.4 /tmp/topology.yaml
```

実行中に、 TiUP はトポロジーを再度確認するように要求し、ターゲット マシンのルート パスワードを要求します (フラグ`-p`はパスワードの入力を意味します)。

```bash
Please confirm your topology:
TiDB Cluster: prod-cluster
TiDB Version: v8.5.4
Type        Host          Ports                            OS/Arch       Directories
----        ----          -----                            -------       -----------
pd          172.16.5.134  2379/2380                        linux/x86_64  deploy/pd-2379,data/pd-2379
pd          172.16.5.139  2379/2380                        linux/x86_64  deploy/pd-2379,data/pd-2379
pd          172.16.5.140  2379/2380                        linux/x86_64  deploy/pd-2379,data/pd-2379
tiproxy     172.16.5.144  6000/3080                        linux/x86_64  deploy/tiproxy-6000
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

パスワードを入力すると、 TiUPクラスターは必要なコンポーネントをダウンロードし、対応するマシンに展開します。次のメッセージが表示されれば、展開は成功です。

```bash
Deployed cluster `prod-cluster` successfully
```

## クラスターリストをビュー {#view-the-cluster-list}

クラスターが正常にデプロイされたら、次のコマンドを実行してクラスター リストを表示します。

```bash
tiup cluster list
```

    Starting /root/.tiup/components/cluster/v1.12.3/cluster list
    Name          User  Version    Path                                               PrivateKey
    ----          ----  -------    ----                                               ----------
    prod-cluster  tidb  v8.5.4    /root/.tiup/storage/cluster/clusters/prod-cluster  /root/.tiup/storage/cluster/clusters/prod-cluster/ssh/id_rsa

## クラスターを起動する {#start-the-cluster}

クラスターが正常にデプロイされたら、次のコマンドを実行してクラスターを起動します。

```shell
tiup cluster start prod-cluster
```

クラスターの名前を忘れた場合は、 `tiup cluster list`を実行してクラスター リストを表示します。

TiUPはデーモンプロセスを起動するために`systemd`使用します。プロセスが予期せず終了した場合、15秒後に再起動されます。

## クラスターのステータスを確認する {#check-the-cluster-status}

TiUPは、クラスター内の各コンポーネントのステータスを表示するためのコマンド`tiup cluster display`を提供しています。このコマンドを使用すると、コンポーネントのステータスを確認するために各マシンにログインする必要がなくなります。コマンドの使用方法は次のとおりです。

```bash
tiup cluster display prod-cluster
```

    Starting /root/.tiup/components/cluster/v1.12.3/cluster display prod-cluster
    TiDB Cluster: prod-cluster
    TiDB Version: v8.5.4
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
    172.16.5.144:6000   tiproxy     172.16.5.144  6000/3080                        linux/x86_64  Up      -                     deploy/tiproxy-6000

`Status`列目では、 `Up`または`Down`を使用して、サービスが正常に実行されているかどうかを示します。

PDコンポーネントの場合、 `|L`または`|UI` `Up`または`Down`に追加されることがあります。 `|L` PD ノードがLeaderであることを示し、 `|UI` [TiDBダッシュボード](/dashboard/dashboard-intro.md) PD ノードで実行されていることを示します。

## クラスターのスケールイン {#scale-in-a-cluster}

> **注記：**
>
> このセクションでは、スケールインコマンドの構文のみを説明します。オンラインスケーリングの詳細な手順については、 [TiUPを使用して TiDBクラスタをスケールする](/scale-tidb-using-tiup.md)を参照してください。

クラスターをスケールインするとは、一部のノードをオフラインにすることを意味します。この操作により、特定のノードがクラスターから削除され、残りのファイルも削除されます。

TiKV およびTiFlashコンポーネントのオフライン プロセスは非同期 (API 経由でノードを削除する必要がある) であり、プロセスに長い時間がかかる (ノードが正常にオフラインになったかどうかを継続的に監視する必要がある) ため、TiKV およびTiFlashコンポーネントには特別な処理が行われます。

-   TiKV およびTiFlashの場合:

    -   TiUPクラスターは API を介してノードをオフラインにし、プロセスが完了するのを待たずに直接終了します。
    -   その後、クラスタ操作に関連するコマンドが実行されると、 TiUPクラスタはオフラインになったTiKVノードまたはTiFlashノードがあるかどうかを確認します。オフラインになったノードがない場合、 TiUPクラスタは指定された操作を続行します。オフラインになったノードがある場合、 TiUPクラスタは以下の手順を実行します。

        1.  オフラインになったノードのサービスを停止します。
        2.  ノードに関連するデータ ファイルをクリーンアップします。
        3.  クラスター トポロジからノードを削除します。

-   その他のコンポーネントの場合:

    -   PDコンポーネントをダウンさせる場合、 TiUPクラスターは API を介して指定されたノードをクラスターから迅速に削除し、指定された PD ノードのサービスを停止し、関連するデータ ファイルを削除します。
    -   他のコンポーネントを停止する場合、 TiUPクラスターはノード サービスを直接停止し、関連するデータ ファイルを削除します。

スケールイン コマンドの基本的な使用方法:

```bash
tiup cluster scale-in <cluster-name> -N <node-id>
```

このコマンドを使用するには、少なくとも2つのフラグ（クラスター名とノードID）を指定する必要があります。ノードIDは、前のセクションの`tiup cluster display`コマンドを使用して取得できます。

たとえば、 `172.16.5.140`上の TiKV ノードをオフラインにするには、次のコマンドを実行します。

```bash
tiup cluster scale-in prod-cluster -N 172.16.5.140:20160
```

`tiup cluster display`実行すると、TiKV ノードが`Offline`マークされていることがわかります。

```bash
tiup cluster display prod-cluster
```

    Starting /root/.tiup/components/cluster/v1.12.3/cluster display prod-cluster
    TiDB Cluster: prod-cluster
    TiDB Version: v8.5.4
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
    172.16.5.144:6000   tiproxy     172.16.5.144  6000/3080                        linux/x86_64  Up       -                     deploy/tiproxy-6000

PD がノード上のデータを他の TiKV ノードにスケジュールすると、このノードは自動的に削除されます。

## クラスターをスケールアウトする {#scale-out-a-cluster}

> **注記：**
>
> このセクションでは、スケールアウトコマンドの構文のみを説明します。オンラインスケーリングの詳細な手順については、 [TiUPを使用して TiDBクラスタをスケールする](/scale-tidb-using-tiup.md)を参照してください。

スケールアウト操作にはデプロイメントと同様の内部ロジックがあります。TiUPTiUPコンポーネントは、まずノードの SSH 接続を確認し、ターゲット ノードに必要なディレクトリを作成してから、デプロイメント操作を実行し、ノード サービスを開始します。

PDをスケールアウトすると、ノードがクラスターに`join`つ追加され、PDに関連付けられたサービスの設定が更新されます。他のサービスをスケールアウトすると、サービスが直接起動され、クラスターに追加されます。

すべてのサービスは、スケールアウト時に正確性の検証を実施します。検証結果から、スケールアウトが成功したかどうかがわかります。

`tidb-test`クラスターに TiKV ノードと PD ノードを追加するには、次の手順を実行します。

1.  `scale.yaml`ファイルを作成し、新しい TiKV ノードと PD ノードの IP を追加します。

    > **注記：**
    >
    > 既存のノードではなく、新しいノードの説明のみを含むトポロジ ファイルを作成する必要があります。

    ```yaml
    ---

    pd_servers:
      - host: 172.16.5.140

    tikv_servers:
      - host: 172.16.5.140
    ```

2.  スケールアウト操作を実行します。TiUP クラスターは、 `scale.yaml`で説明したポート、ディレクトリ、その他の情報に従って、対応するノードをクラスターに追加します。

    ```shell
    tiup cluster scale-out tidb-test scale.yaml
    ```

    コマンドを実行した後、 `tiup cluster display tidb-test`を実行してスケールアウトされたクラスターのステータスを確認できます。

## ローリングアップグレード {#rolling-upgrade}

> **注記：**
>
> このセクションでは、アップグレードコマンドの構文のみを説明します。オンラインアップグレードの詳細な手順については、 [TiUPを使用して TiDB をアップグレードする](/upgrade-tidb-using-tiup.md)を参照してください。

ローリングアップグレード機能は、TiDBの分散機能を活用します。アップグレードプロセスはアプリケーションに対して可能な限り透過的に行われるため、ビジネスに影響を与えることはありません。

アップグレード前に、 TiUPクラスタは各コンポーネントの設定ファイルが適切かどうかを確認します。適切であれば、コンポーネントはノードごとにアップグレードされます。適切でない場合、 TiUPはエラーを報告して終了します。処理はノードによって異なります。

### 異なるノードに対する操作 {#operations-for-different-nodes}

-   PDノードをアップグレードする

    -   まず、リーダー以外のノードをアップグレードします。
    -   リーダー以外のノードがすべてアップグレードされたら、Leaderノードをアップグレードします。
        -   アップグレード ツールは、Leaderをすでにアップグレードされたノードに移行するコマンドを PD に送信します。
        -   Leaderの役割が別のノードに切り替えられた後、以前のLeaderノードをアップグレードします。
    -   アップグレード中に異常なノードが検出された場合、ツールはアップグレード操作を停止して終了します。手動で原因を分析し、問題を修正してから、アップグレードを再度実行する必要があります。

-   TiKVノードをアップグレードする

    -   まず、PD にこの TiKV ノードのリージョンLeaderを移行するスケジュール操作を追加します。これにより、アップグレードプロセスがビジネスに影響を与えないことが保証されます。
    -   Leaderが移行された後、この TiKV ノードをアップグレードします。
    -   アップグレードした TiKV が正常に起動したら、Leaderのスケジュールを削除します。

-   他のサービスをアップグレードする

    -   サービスを通常どおり停止し、ノードを更新します。

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

たとえば、次のコマンドはクラスターを v8.5.4 にアップグレードします。

```bash
tiup cluster upgrade tidb-test v8.5.4
```

## 構成を更新する {#update-configuration}

コンポーネント構成を動的に更新する場合、 TiUPクラスタコンポーネントは各クラスタの現在の構成を保存します。この構成を編集するには、 `tiup cluster edit-config <cluster-name>`コマンドを実行します。例：

```bash
tiup cluster edit-config prod-cluster
```

TiUPクラスターは設定ファイルをviエディタで開きます。他のエディタを使用する場合は、環境変数`EDITOR`を使用してエディタをカスタマイズします（例： `export EDITOR=nano` ）。

ファイルを編集したら、変更を保存します。新しい設定をクラスターに適用するには、次のコマンドを実行します。

```bash
tiup cluster reload prod-cluster
```

このコマンドは、構成をターゲット マシンに送信し、クラスターを再起動して構成を有効にします。

> **注記：**
>
> 監視コンポーネントについては、 `tiup cluster edit-config`コマンドを実行して対応するインスタンスにカスタム設定パスを追加することで、設定をカスタマイズします。例:

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

指定されたパスの下にあるファイルの内容と形式の要件は次のとおりです。

-   `grafana_servers`の`dashboard_dir`フィールドで指定されたフォルダーには、完全な`*.json`ファイルが含まれている必要があります。
-   `monitoring_servers`の`rule_dir`フィールドで指定されたフォルダーには、完全な`*.rules.yml`ファイルが含まれている必要があります。
-   `alertmanager_servers`の`config_file`欄に指定するファイルの形式については[Alertmanager 構成テンプレート](https://github.com/pingcap/tiup/blob/master/embed/templates/config/alertmanager.yml)を参照してください。

`tiup reload`実行すると、 TiUP はまずターゲットマシン上の古い設定ファイルをすべて削除し、次にコントロールマシンから対応する設定ファイルをターゲットマシンの対応する設定ディレクトリにアップロードします。したがって、特定の設定ファイルを変更する場合は、すべての設定ファイル（変更されていないものも含む）が同じディレクトリにあることを確認してください。例えば、Grafana の`tidb.json`ファイルを変更するには、まず Grafana の`dashboards`ディレクトリにある`*.json`ファイルすべてをローカルディレクトリにコピーする必要があります。そうしないと、ターゲットマシンから他の JSON ファイルが失われます。

> **注記：**
>
> `dashboard_dir`フィールドを`grafana_servers`に設定した場合、 `tiup cluster rename`コマンドを実行してクラスターの名前を変更した後、次の操作を完了する必要があります。
>
> 1.  ローカル`dashboards`ディレクトリで、クラスター名を新しいクラスター名に変更します。
> 2.  ローカルの`dashboards`ディレクトリで、 `datasource`クラスター名に基づいて命名されているため、 `datasource`新しいクラスター名に変更します。
> 3.  `tiup cluster reload -R grafana`コマンドを実行します。

## コンポーネントの更新 {#update-component}

通常のアップグレードでは`upgrade`コマンドを使用できます。ただし、デバッグなどの一部のシナリオでは、現在実行中のコンポーネントを一時パッケージに置き換える必要がある場合があります。これを行うには、 `patch`コマンドを使用します。

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

クラスター内の 1 つの TiDB パッケージのみを置き換えることもできます。

```bash
tiup cluster patch test-cluster /tmp/tidb-hotfix.tar.gz -N 172.16.4.5:4000
```

## TiDB Ansibleクラスターをインポートする {#import-tidb-ansible-cluster}

TiUPがリリースされる前は、TiDBクラスタのデプロイにTiDB Ansibleがよく使用されていました。TiDB AnsibleによってデプロイされたクラスタをTiUPが引き継ぐようにするには、 `import`コマンドを使用します。

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

次のいずれかのコマンドを使用して、TiDB Ansible クラスターをインポートできます。

```bash
cd tidb-ansible
tiup cluster import
```

```bash
tiup cluster import --dir=/path/to/tidb-ansible
```

## 操作ログをビュー {#view-the-operation-log}

操作ログを表示するには、 `audit`コマンドを使用します。3 コマンドの使用方法は`audit`のとおりです。

```bash
Usage:
  tiup cluster audit [audit-id] [flags]

Flags:
  -h, --help   help for audit
```

フラグ`[audit-id]`が指定されていない場合、コマンドは実行されたコマンドのリストを表示します。例:

```bash
tiup cluster audit
```

    Starting component `cluster`: /home/tidb/.tiup/components/cluster/v1.12.3/cluster audit
    ID      Time                       Command
    --      ----                       -------
    4BLhr0  2025-11-27T23:55:09+08:00  /home/tidb/.tiup/components/cluster/v1.12.3/cluster deploy test v8.5.4 /tmp/topology.yaml
    4BKWjF  2025-11-27T23:36:57+08:00  /home/tidb/.tiup/components/cluster/v1.12.3/cluster deploy test v8.5.4 /tmp/topology.yaml
    4BKVwH  2025-11-27T23:02:08+08:00  /home/tidb/.tiup/components/cluster/v1.12.3/cluster deploy test v8.5.4 /tmp/topology.yaml
    4BKKH1  2025-11-27T16:39:04+08:00  /home/tidb/.tiup/components/cluster/v1.12.3/cluster destroy test
    4BKKDx  2025-11-27T16:36:57+08:00  /home/tidb/.tiup/components/cluster/v1.12.3/cluster deploy test v8.5.4 /tmp/topology.yaml

最初の列は`audit-id`です。特定のコマンドの実行ログを表示するには、次のようにコマンドの`audit-id`をフラグとして渡します。

```bash
tiup cluster audit 4BLhr0
```

## TiDB クラスター内のホストでコマンドを実行する {#run-commands-on-a-host-in-the-tidb-cluster}

TiDBクラスタ内のホストでコマンドを実行するには、 `exec`コマンドを使用します。3 `exec`のコマンドの使用方法は次のとおりです。

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

たとえば、すべての TiDB ノードで`ls /tmp`実行するには、次のコマンドを実行します。

```bash
tiup cluster exec test-cluster --command='ls /tmp'
```

## クラスタコントローラー {#cluster-controllers}

TiUPがリリースされる前は、 `tidb-ctl` `pd-ctl`のツールを使用してクラスターを制御できました。これら`tikv-ctl`ツールをより簡単にダウンロードして使用できるように、 TiUPはそれらをオールインワンコンポーネント`ctl`に統合しています。

```bash
Usage:
  tiup ctl:v<CLUSTER_VERSION> {tidb/pd/tikv/etcd} [flags]

Flags:
  -h, --help   help for tiup
```

このコマンドは、以前のツールのコマンドと対応関係があります。

```bash
tidb-ctl [args] = tiup ctl tidb [args]
pd-ctl [args] = tiup ctl pd [args]
tikv-ctl [args] = tiup ctl tikv [args]
etcdctl [args] = tiup ctl etcd [args]
```

たとえば、以前に`pd-ctl -u http://127.0.0.1:2379 store`実行してストアを表示していた場合、今度はTiUPで次のコマンドを実行できます。

```bash
tiup ctl:v<CLUSTER_VERSION> pd -u http://127.0.0.1:2379 store
```

## 対象マシンの環境チェック {#environment-checks-for-target-machines}

`check`コマンドを使用すると、ターゲットマシンの環境に対して一連のチェックを実行し、チェック結果を出力できます`check`コマンドを実行すると、よくある不適切な構成やサポートされていない状況を特定できます。コマンドフラグリストは次のとおりです。

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

デフォルトでは、このコマンドはデプロイメント前の環境チェックに使用されます。モードを切り替えるために`--cluster`フラグを指定すると、既存のクラスターのターゲットマシンもチェックできます。例:

```bash
# check deployed servers before deployment
tiup cluster check topology.yml --user tidb -p
# check deployed servers of an existing cluster
tiup cluster check <cluster-name> --cluster
```

CPUスレッド数チェック、メモリサイズチェック、ディスクパフォ​​ーマンスチェックはデフォルトで無効になっています。本番環境では、最高のパフォーマンスを得るために、これら3つのチェックを有効にし、それらがパスすることを確認することをお勧めします。

-   CPU: スレッド数が 16 以上の場合、チェックに合格します。
-   メモリ: 物理メモリの合計サイズが 32 GB 以上の場合、チェックは合格です。
-   ディスク: `data_dir`のパーティションに対して`fio`テストを実行し、結果を記録します。

チェック実行時にフラグ`--apply`が指定されている場合、プログラムは失敗した項目を自動的に修復します。自動修復は、設定またはシステムパラメータの変更によって調整可能な一部の項目に限定されます。修復されないその他の項目は、実際の状況に応じて手動で処理する必要があります。

クラスタのデプロイには環境チェックは必須ではありません。本番環境では、デプロイ前に環境チェックを実施し、すべてのチェック項目に合格することをお勧めします。すべてのチェック項目に合格していない場合、クラスタはデプロイされ正常に動作しますが、最適なパフォーマンスが得られない可能性があります。

## システムのネイティブSSHクライアントを使用してクラスタに接続します {#use-the-system-s-native-ssh-client-to-connect-to-cluster}

クラスタマシン上で実行される上記のすべての操作は、 TiUPに組み込まれたSSHクライアントを使用してクラスタに接続し、コマンドを実行します。ただし、シナリオによっては、制御マシンシステムにネイティブなSSHクライアントを使用してクラスタ操作を実行する必要がある場合もあります。例：

-   認証にSSHプラグインを使用するには
-   カスタマイズされたSSHクライアントを使用するには

次に、 `--ssh=system`コマンドライン フラグを使用して、システムネイティブのコマンドライン ツールを有効にできます。

-   クラスターをデプロイ: `tiup cluster deploy <cluster-name> <version> <topo> --ssh=system` . `<cluster-name>`にクラスターの名前、 `<version>`にデプロイする TiDB バージョン ( `v8.5.4`など)、 `<topo>`にトポロジ ファイルを入力します。
-   クラスターを開始する: `tiup cluster start <cluster-name> --ssh=system`
-   クラスターのアップグレード: `tiup cluster upgrade ... --ssh=system`

上記のすべてのクラスター操作コマンドに`--ssh=system`追加すると、システムのネイティブ SSH クライアントを使用できます。

すべてのコマンドにこのようなフラグを追加しないようにするには、 `TIUP_NATIVE_SSH`システム変数を使用して、ローカル SSH クライアントを使用するかどうかを指定します。

```shell
export TIUP_NATIVE_SSH=true
# or
export TIUP_NATIVE_SSH=1
# or
export TIUP_NATIVE_SSH=enable
```

この環境変数と`--ssh`同時に指定した場合、 `--ssh`優先されます。

> **注記：**
>
> クラスターの展開プロセス中に、接続にパスワードを使用する必要がある場合 ( `-p` ) またはキー ファイルに`passphrase`が設定されている場合は、制御マシンに`sshpass`がインストールされていることを確認する必要があります。そうでない場合、タイムアウト エラーが報告されます。

## 制御マシンを移行し、 TiUPデータをバックアップする {#migrate-control-machine-and-back-up-tiup-data}

TiUPデータは、ユーザーのホームディレクトリ内の`.tiup`ディレクトリに保存されます。コントロールマシンを移行するには、以下の手順に従って`.tiup`ディレクトリを対応するターゲットマシンにコピーします。

1.  元のマシンのホームディレクトリで`tar czvf tiup.tar.gz .tiup`実行します。
2.  `tiup.tar.gz`ターゲット マシンのホーム ディレクトリにコピーします。
3.  対象マシンのホームディレクトリで`tar xzvf tiup.tar.gz`実行します。
4.  `.tiup`ディレクトリを`PATH`環境変数に追加します。

    `bash`使用し、 `tidb`ユーザーの場合は、 `~/.bashrc`に`export PATH=/home/tidb/.tiup/bin:$PATH`追加して`source ~/.bashrc`実行します。その後、使用するシェルとユーザーに応じて調整してください。

> **注記：**
>
> 制御マシンのディスク破損などの異常な状況によってTiUPデータが失われないように、 `.tiup`ディレクトリを定期的にバックアップすることをお勧めします。

## クラスタの展開とO&amp;Mのためのメタファイルのバックアップと復元 {#back-up-and-restore-meta-files-for-cluster-deployment-and-o-x26-m}

運用保守（O&amp;M）に使用するメタファイルが失われると、 TiUPを使用したクラスターの管理が失敗します。以下のコマンドを実行して、メタファイルを定期的にバックアップすることをお勧めします。

```bash
tiup cluster meta backup ${cluster_name}
```

メタ ファイルが失われた場合は、次のコマンドを実行して復元できます。

```bash
tiup cluster meta restore ${cluster_name} ${backup_file}
```

> **注記：**
>
> 復元操作により、現在のメタファイルが上書きされます。そのため、メタファイルが失われた場合にのみ復元することをお勧めします。
