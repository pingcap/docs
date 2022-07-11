---
title: Maintain a DM Cluster Using TiUP
summary: Learn how to maintain a DM cluster using TiUP.
---

# TiUPを使用してDMクラスターを管理する {#maintain-a-dm-cluster-using-tiup}

このドキュメントでは、 TiUP DMコンポーネントを使用してDMクラスタを保守する方法を紹介します。

DMクラスタをまだデプロイしていない場合は、 [TiUPを使用してDMクラスターをデプロイする](/dm/deploy-a-dm-cluster-using-tiup.md)を参照して手順を確認できます。

> **ノート：**
>
> -   次のコンポーネント間のポートが相互接続されていることを確認してください
>     -   DMマスターノード間の`peer_port` （デフォルトでは`8291` ）は相互接続されています。
>     -   各DMマスターノードは、すべてのDMワーカーノードの`port`つ（デフォルトでは`8262` ）に接続できます。
>     -   各DM-workerノードは、すべてのDM-masterノードの`port`つ（デフォルトでは`8261` ）に接続できます。
>     -   TiUPノードは、すべてのDMマスターノードの`port`つ（デフォルトでは`8261` ）に接続できます。
>     -   TiUPノードは、すべてのDMワーカーノードの`port`つ（デフォルトでは`8262` ）に接続できます。

TiUP DMコンポーネントのヘルプ情報については、次のコマンドを実行してください。

```bash
tiup dm --help
```

```
Deploy a DM cluster for production

Usage:
  tiup dm [flags]
  tiup dm [command]

Available Commands:
  deploy      Deploy a DM cluster for production
  start       Start a DM cluster
  stop        Stop a DM cluster
  restart     Restart a DM cluster
  list        List all clusters
  destroy     Destroy a specified DM cluster
  audit       Show audit log of cluster operation
  exec        Run shell command on host in the dm cluster
  edit-config Edit DM cluster config
  display     Display information of a DM cluster
  reload      Reload a DM cluster's config and restart if needed
  upgrade     Upgrade a specified DM cluster
  patch       Replace the remote package with a specified package and restart the service
  scale-out   Scale out a DM cluster
  scale-in    Scale in a DM cluster
  import      Import an exist DM 1.0 cluster from dm-ansible and re-deploy 2.0 version
  help        Help about any command

Flags:
  -h, --help               help for tiup-dm
      --native-ssh         Use the native SSH client installed on local system instead of the build-in one.
      --ssh-timeout int    Timeout in seconds to connect host via SSH, ignored for operations that don't need an SSH connection. (default 5)
  -v, --version            version for tiup-dm
      --wait-timeout int   Timeout in seconds to wait for an operation to complete, ignored for operations that don't fit. (default 60)
  -y, --yes                Skip all confirmations and assumes 'yes'
```

## クラスタリストをビューする {#view-the-cluster-list}

クラスタが正常にデプロイされたら、次のコマンドを実行してクラスタリストを表示します。

{{< copyable "" >}}

```bash
tiup dm list
```

```
Name  User  Version  Path                                  PrivateKey
----  ----  -------  ----                                  ----------
prod-cluster  tidb  ${version}  /root/.tiup/storage/dm/clusters/test  /root/.tiup/storage/dm/clusters/test/ssh/id_rsa
```

## クラスタを開始します {#start-the-cluster}

クラスタが正常にデプロイされたら、次のコマンドを実行してクラスタを開始します。

{{< copyable "" >}}

```shell
tiup dm start prod-cluster
```

クラスタの名前を忘れた場合は、 `tiup dm list`を実行してクラスタリストを表示します。

## クラスタのステータスを確認する {#check-the-cluster-status}

TiUPは、クラスタの各コンポーネントのステータスを表示するための`tiup dm display`のコマンドを提供します。このコマンドを使用すると、コンポーネントのステータスを確認するために各マシンにログインする必要はありません。コマンドの使用法は次のとおりです。

{{< copyable "" >}}

```bash
tiup dm display prod-cluster
```

```
dm Cluster: prod-cluster
dm Version: ${version}
ID                 Role          Host          Ports      OS/Arch       Status     Data Dir                           Deploy Dir
--                 ----          ----          -----      -------       ------     --------                           ----------
172.19.0.101:9093  alertmanager  172.19.0.101  9093/9094  linux/x86_64  Up         /home/tidb/data/alertmanager-9093  /home/tidb/deploy/alertmanager-9093
172.19.0.101:8261  dm-master     172.19.0.101  8261/8291  linux/x86_64  Healthy|L  /home/tidb/data/dm-master-8261     /home/tidb/deploy/dm-master-8261
172.19.0.102:8261  dm-master     172.19.0.102  8261/8291  linux/x86_64  Healthy    /home/tidb/data/dm-master-8261     /home/tidb/deploy/dm-master-8261
172.19.0.103:8261  dm-master     172.19.0.103  8261/8291  linux/x86_64  Healthy    /home/tidb/data/dm-master-8261     /home/tidb/deploy/dm-master-8261
172.19.0.101:8262  dm-worker     172.19.0.101  8262       linux/x86_64  Free       /home/tidb/data/dm-worker-8262     /home/tidb/deploy/dm-worker-8262
172.19.0.102:8262  dm-worker     172.19.0.102  8262       linux/x86_64  Free       /home/tidb/data/dm-worker-8262     /home/tidb/deploy/dm-worker-8262
172.19.0.103:8262  dm-worker     172.19.0.103  8262       linux/x86_64  Free       /home/tidb/data/dm-worker-8262     /home/tidb/deploy/dm-worker-8262
172.19.0.101:3000  grafana       172.19.0.101  3000       linux/x86_64  Up         -                                  /home/tidb/deploy/grafana-3000
172.19.0.101:9090  prometheus    172.19.0.101  9090       linux/x86_64  Up         /home/tidb/data/prometheus-9090    /home/tidb/deploy/prometheus-9090
```

`Status`列は、サービスが正常に実行されているかどうかを示すために`Up`または`Down`を使用します。

DMマスターコンポーネントの場合、ステータスに`|L`が追加されることがあります。これは、DMマスターノードがリーダーであることを示します。 DM-workerコンポーネントの場合、 `Free`は、現在のDM-workerノードがアップストリームにバインドされていないことを示します。

## クラスタでのスケーリング {#scale-in-a-cluster}

クラスタでのスケーリングとは、一部のノードをオフラインにすることを意味します。この操作により、指定されたノードがクラスタから削除され、残りのデータファイルが削除されます。

クラスタでスケーリングする場合、DM-masterおよびDM-workerコンポーネントに対するDM操作は次の順序で実行されます。

1.  コンポーネントプロセスを停止します。
2.  DMマスターのAPIを呼び出して、 `member`を削除します。
3.  ノードに関連するデータファイルをクリーンアップします。

スケールインコマンドの基本的な使用法：

```bash
tiup dm scale-in <cluster-name> -N <node-id>
```

このコマンドを使用するには、クラスタ名とノードIDの少なくとも2つの引数を指定する必要があります。ノードIDは、前のセクションの`tiup dm display`コマンドを使用して取得できます。

たとえば、 `172.16.5.140`のDM-workerノードでスケーリングするには（DM-masterでのスケーリングと同様）、次のコマンドを実行します。

{{< copyable "" >}}

```bash
tiup dm scale-in prod-cluster -N 172.16.5.140:8262
```

## クラスタをスケールアウトする {#scale-out-a-cluster}

スケールアウト操作には、展開と同様の内部ロジックがありますTiUP DMコンポーネントは、最初にノードのSSH接続を確認し、ターゲットノードに必要なディレクトリを作成してから、展開操作を実行し、ノードサービスを開始します。

たとえば、 `prod-cluster`クラスタのDM-workerノードをスケールアウトするには、次の手順を実行します（DM-masterのスケールアウトにも同様の手順があります）。

1.  `scale.yaml`のファイルを作成し、新しいワーカーノードの情報を追加します。

    > **ノート：**
    >
    > トポロジファイルを作成する必要があります。このファイルには、既存のノードではなく、新しいノードの説明のみが含まれています。その他の構成項目（デプロイメントディレクトリなど）については、この[TiUP構成パラメーターの例](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml)を参照してください。

    ```yaml
    ---

    worker_servers:
      - host: 172.16.5.140

    ```

2.  スケールアウト操作を実行します。 TiUP DMは、ポート、ディレクトリ、および`scale.yaml`で説明されているその他の情報に従って、対応するノードをクラスタに追加します。

    {{< copyable "" >}}

    ```shell
    tiup dm scale-out prod-cluster scale.yaml
    ```

    コマンドの実行後、 `tiup dm display prod-cluster`を実行することにより、スケールアウトされたクラスタのステータスを確認できます。

## ローリングアップグレード {#rolling-upgrade}

> **ノート：**
>
> v2.0.5以降、dmctlは[データソースのエクスポートとインポート、およびクラスターのタスクConfiguration / コンフィグレーション](/dm/dm-export-import-config.md)をサポートします。
>
> アップグレードする前に、 `config export`を使用してクラスターの構成ファイルをエクスポートできます。アップグレード後、以前のバージョンにダウングレードする必要がある場合は、最初に以前のクラスタを再デプロイしてから、 `config import`を使用して以前の構成ファイルをインポートできます。
>
> v2.0.5より前のクラスターの場合、dmctl v2.0.5以降を使用して、データソースおよびタスク構成ファイルをエクスポートおよびインポートできます。
>
> v2.0.2以降のクラスターの場合、現在、リレーワーカーに関連する構成を自動的にインポートすることはサポートされていません。 `start-relay`のコマンドを使用して手動で[リレーログを開始](/dm/relay-log.md#start-and-stop-the-relay-log-feature)を実行できます。

ローリングアップグレードプロセスは、アプリケーションに対して可能な限り透過的に行われ、ビジネスに影響を与えません。操作はノードによって異なります。

### アップグレードコマンド {#upgrade-command}

`tiup dm upgrade`コマンドを実行して、DMクラスタをアップグレードできます。たとえば、次のコマンドはクラスタを`${version}`にアップグレードします。このコマンドを実行する前に、 `${version}`を必要なバージョンに変更してください。

{{< copyable "" >}}

```bash
tiup dm upgrade prod-cluster ${version}
```

## 構成を更新する {#update-configuration}

コンポーネント構成を動的に更新する場合、 TiUP DMコンポーネントは各クラスタの現在の構成を保存します。この構成を編集するには、 `tiup dm edit-config <cluster-name>`コマンドを実行します。例えば：

{{< copyable "" >}}

```bash
tiup dm edit-config prod-cluster
```

TiUP DMは、viエディターで構成ファイルを開きます。他のエディターを使用する場合は、 `EDITOR`環境変数を使用して、 `export EDITOR=nano`などのエディターをカスタマイズします。ファイルを編集した後、変更を保存します。新しい構成をクラスタに適用するには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
tiup dm reload prod-cluster
```

このコマンドは、構成をターゲットマシンに送信し、クラスタを再起動して構成を有効にします。

## コンポーネントを更新 {#update-component}

通常のアップグレードでは、 `upgrade`コマンドを使用できます。ただし、デバッグなどの一部のシナリオでは、現在実行中のコンポーネントを一時パッケージに置き換える必要がある場合があります。これを実現するには、次の`patch`のコマンドを使用します。

{{< copyable "" >}}

```bash
tiup dm patch --help
```

```
Replace the remote package with a specified package and restart the service

Usage:
  tiup dm patch <cluster-name> <package-path> [flags]

Flags:
  -h, --help                   help for patch
  -N, --node strings           Specify the nodes
      --overwrite              Use this package in the future scale-out operations
  -R, --role strings           Specify the role
      --transfer-timeout int   Timeout in seconds when transferring dm-master leaders (default 300)

Global Flags:
      --native-ssh         Use the native SSH client installed on local system instead of the build-in one.
      --ssh-timeout int    Timeout in seconds to connect host via SSH, ignored for operations that don't need an SSH connection. (default 5)
      --wait-timeout int   Timeout in seconds to wait for an operation to complete, ignored for operations that don't fit. (default 60)
  -y, --yes                Skip all confirmations and assumes 'yes'
```

DM-masterホットフィックスパッケージが`/tmp/dm-master-hotfix.tar.gz`に含まれていて、クラスタのすべてのDM-masterパッケージを置き換える場合は、次のコマンドを実行します。

{{< copyable "" >}}

```bash
tiup dm patch prod-cluster /tmp/dm-master-hotfix.tar.gz -R dm-master
```

クラスタのDMマスターパッケージを1つだけ置き換えることもできます。

{{< copyable "" >}}

```bash
tiup dm patch prod-cluster /tmp/dm--hotfix.tar.gz -N 172.16.4.5:8261
```

## DM-Ansibleを使用してデプロイされたDM1.0クラスタをインポートしてアップグレードします {#import-and-upgrade-a-dm-1-0-cluster-deployed-using-dm-ansible}

> **ノート：**
>
> -   TiUPは、DM1.0クラスタへのDMポータルコンポーネントのインポートをサポートしていません。
> -   インポートする前に、元のクラスタを停止する必要があります。
> -   2.0にアップグレードする必要があるタスクには`stop-task`を実行しないでください。
> -   TiUPは、v2.0.0-rc.2以降のバージョンのDMクラスタへのインポートのみをサポートします。
> -   `import`コマンドは、DM1.0クラスタから新しいDM2.0クラスターにデータをインポートするために使用されクラスタ。 DM移行タスクを既存のDM2.0クラスタにインポートする必要がある場合は、 [TiDBデータ移行をv1.0.xからv2.0+に手動でアップグレードする](/dm/manually-upgrade-dm-1.0-to-2.0.md)を参照してください。
> -   一部のコンポーネントのデプロイメントディレクトリは、元のクラスタのデプロイメントディレクトリとは異なります。 `display`コマンドを実行して詳細を表示できます。
> -   インポートする前に`tiup update --self && tiup update dm`を実行して、 TiUP DMコンポーネントが最新バージョンであることを確認します。
> -   インポート後、クラスタにはDMマスターノードが1つだけ存在します。 DMマスターをスケールアウトするには、 [クラスタをスケールアウトする](#scale-out-a-cluster)を参照してください。

TiUPがリリースされる前は、DM-Ansibleを使用してDMクラスターをデプロイすることがよくあります。 TiUPがDM-AnsibleによってデプロイされたDM1.0クラスタを引き継ぐことができるようにするには、 `import`コマンドを使用します。

たとえば、DM Ansibleを使用してデプロイされたクラスタをインポートするには、次のようにします。

{{< copyable "" >}}

```bash
tiup dm import --dir=/path/to/dm-ansible --cluster-version ${version}
```

`tiup list dm-master`を実行して、TiUPでサポートされている最新のクラスタバージョンを表示します。

`import`コマンドを使用するプロセスは次のとおりです。

1.  TiUPは、DM-Ansibleを使用して以前にデプロイされたDMクラスタに基づいてトポロジファイル[`topology.yml`](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml)を生成します。
2.  トポロジー・ファイルが生成されたことを確認した後、それを使用して、v2.0以降のバージョンのDMクラスタをデプロイできます。

展開が完了したら、 `tiup dm start`コマンドを実行してクラスタを開始し、DMカーネルのアップグレードプロセスを開始できます。

## 操作ログをビューする {#view-the-operation-log}

操作ログを表示するには、 `audit`コマンドを使用します。 `audit`コマンドの使用法は次のとおりです。

```bash
Usage:
  tiup dm audit [audit-id] [flags]

Flags:
  -h, --help   help for audit
```

`[audit-id]`引数が指定されていない場合、コマンドは実行されたコマンドのリストを表示します。例えば：

{{< copyable "" >}}

```bash
tiup dm audit
```

```
ID      Time                  Command
--      ----                  -------
4D5kQY  2020-08-13T05:38:19Z  tiup dm display test
4D5kNv  2020-08-13T05:36:13Z  tiup dm list
4D5kNr  2020-08-13T05:36:10Z  tiup dm deploy -p prod-cluster ${version} ./examples/dm/minimal.yaml
```

最初の列は`audit-id`です。特定のコマンドの実行ログを表示するには、次のように`audit-id`引数を渡します。

{{< copyable "" >}}

```bash
tiup dm audit 4D5kQY
```

## DMクラスタのホストでコマンドを実行する {#run-commands-on-a-host-in-the-dm-cluster}

DMクラスタのホストでコマンドを実行するには、 `exec`コマンドを使用します。 `exec`コマンドの使用法は次のとおりです。

```bash
Usage:
  tiup dm exec <cluster-name> [flags]

Flags:
      --command string   the command run on cluster host (default "ls")
  -h, --help             help for exec
  -N, --node strings     Only exec on host with specified nodes
  -R, --role strings     Only exec on host with specified roles
      --sudo             use root permissions (default false)
```

たとえば、すべてのDMノードで`ls /tmp`を実行するには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
tiup dm exec prod-cluster --command='ls /tmp'
```

## dmctl {#dmctl}

TiUPはDMクラスタコントローラー`dmctl`を統合します。

次のコマンドを実行して、dmctlを使用します。

```bash
tiup dmctl [args]
```

dmctlのバージョンを指定します。このコマンドを実行する前に、 `${version}`を必要なバージョンに変更してください。

```
tiup dmctl:${version} [args]
```

ソースを追加するための以前のdmctlコマンドは`dmctl --master-addr master1:8261 operate-source create /tmp/source1.yml`です。 dmctlがTiUPに統合された後、コマンドは次のようになります。

{{< copyable "" >}}

```bash
tiup dmctl --master-addr master1:8261 operate-source create /tmp/source1.yml
```

## システムのネイティブSSHクライアントを使用してクラスタに接続します {#use-the-system-s-native-ssh-client-to-connect-to-cluster}

クラスタマシンで実行される上記のすべての操作は、TiUPに組み込まれたSSHクライアントを使用してクラスタに接続し、コマンドを実行します。ただし、シナリオによっては、このようなクラスタ操作を実行するために、制御マシンシステムにネイティブなSSHクライアントを使用する必要がある場合もあります。例えば：

-   認証にSSHプラグインを使用するには
-   カスタマイズされたSSHクライアントを使用するには

次に、 `--native-ssh`コマンドラインフラグを使用して、システムネイティブのコマンドラインツールを有効にします。

-   クラスタのデプロイ： `tiup dm deploy <cluster-name> <version> <topo> --native-ssh`
-   クラスタを開始します： `tiup dm start <cluster-name> --native-ssh`
-   クラスタのアップグレード： `tiup dm upgrade ... --native-ssh`

上記のすべてのクラスタ操作コマンドに`--native-ssh`を追加して、システムのネイティブSSHクライアントを使用できます。

すべてのコマンドにこのようなフラグが追加されないようにするには、 `TIUP_NATIVE_SSH`システム変数を使用して、ローカルSSHクライアントを使用するかどうかを指定できます。

```sh
export TIUP_NATIVE_SSH=true
# or
export TIUP_NATIVE_SSH=1
# or
export TIUP_NATIVE_SSH=enable
```

この環境変数と`--native-ssh`を同時に指定すると、 `--native-ssh`の優先度が高くなります。

> **ノート：**
>
> クラスタ展開のプロセス中に、接続にパスワードを使用する必要がある場合、またはキーファイルに`passphrase`が設定されている場合は、 `sshpass`が制御マシンにインストールされていることを確認する必要があります。それ以外の場合は、タイムアウトエラーが報告されます。
