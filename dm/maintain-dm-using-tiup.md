---
title: Maintain a DM Cluster Using TiUP
summary: TiUPを使用して DM クラスターを保守する方法を学びます。
---

# TiUPを使用して DMクラスタを管理 {#maintain-a-dm-cluster-using-tiup}

このドキュメントでは、TiUP DMコンポーネントを使用して DM クラスターを保守する方法について説明します。

DM クラスターをまだ展開していない場合は、手順[TiUPを使用して DMクラスタをデプロイ](/dm/deploy-a-dm-cluster-using-tiup.md)を参照してください。

> **注記：**
>
> -   以下のコンポーネント間のポートが相互接続されていることを確認してください
>     -   DM マスター ノードのうち`peer_port` (デフォルトでは`8291` ) が相互接続されています。
>     -   各 DM マスター ノードは、すべての DM ワーカー ノードの`port` (デフォルトでは`8262` ) に接続できます。
>     -   各 DM ワーカー ノードは、すべての DM マスター ノードの`port` (デフォルトでは`8261` ) に接続できます。
>     -   TiUPノードは、すべての DM マスター ノードの`port` (デフォルトでは`8261` ) に接続できます。
>     -   TiUPノードは、すべての DM ワーカー ノードの`port` (デフォルトでは`8262` ) に接続できます。

TiUP DMコンポーネントのヘルプ情報については、次のコマンドを実行します。

```bash
tiup dm --help
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

## クラスターリストをビュー {#view-the-cluster-list}

クラスターが正常にデプロイされたら、次のコマンドを実行してクラスター リストを表示します。

```bash
tiup dm list
```

    Name  User  Version  Path                                  PrivateKey
    ----  ----  -------  ----                                  ----------
    prod-cluster  tidb  ${version}  /root/.tiup/storage/dm/clusters/test  /root/.tiup/storage/dm/clusters/test/ssh/id_rsa

## クラスターを起動する {#start-the-cluster}

クラスターが正常にデプロイされたら、次のコマンドを実行してクラスターを起動します。

```shell
tiup dm start prod-cluster
```

クラスターの名前を忘れた場合は、 `tiup dm list`実行してクラスター リストを表示します。

## クラスターのステータスを確認する {#check-the-cluster-status}

TiUPは、クラスタ内の各コンポーネントのステータスを表示するためのコマンド`tiup dm display`を提供しています。このコマンドを使用すると、コンポーネントのステータスを確認するために各マシンにログインする必要がなくなります。コマンドの使用方法は次のとおりです。

```bash
tiup dm display prod-cluster
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

`Status`列目では、 `Up`または`Down`使用して、サービスが正常に実行されているかどうかを示します。

DMマスターコンポーネントの場合、ステータスに`|L`が付加され、DMマスターノードがLeaderであることを示します。DMワーカーコンポーネントの場合、 `Free`現在のDMワーカーノードがアップストリームにバインドされていないことを示します。

## クラスターのスケールイン {#scale-in-a-cluster}

クラスターのスケールインとは、一部のノードをオフラインにすることを意味します。この操作により、指定されたノードがクラスターから削除され、残りのデータファイルが削除されます。

クラスターをスケールインすると、DM マスター コンポーネントと DM ワーカー コンポーネントに対する DM 操作が次の順序で実行されます。

1.  コンポーネントプロセスを停止します。
2.  DM-master の API を呼び出して`member`削除します。
3.  ノードに関連するデータ ファイルをクリーンアップします。

スケールイン コマンドの基本的な使用法:

```bash
tiup dm scale-in <cluster-name> -N <node-id>
```

このコマンドを使用するには、少なくとも2つの引数（クラスター名とノードID）を指定する必要があります。ノードIDは、前のセクションの`tiup dm display`コマンドを使用して取得できます。

たとえば、DM-worker ノード`172.16.5.140`をスケールインするには (DM-master のスケーリングと同様)、次のコマンドを実行します。

```bash
tiup dm scale-in prod-cluster -N 172.16.5.140:8262
```

## クラスターをスケールアウトする {#scale-out-a-cluster}

スケールアウト操作にはTiUP DMコンポーネントは、まずノードの SSH 接続を確認し、ターゲット ノードに必要なディレクトリを作成し、次にデプロイメント操作を実行して、ノード サービスを開始します。

たとえば、クラスター`prod-cluster`内の DM ワーカー ノードをスケール アウトするには、次の手順を実行します (DM マスターのスケール アウトにも同様の手順があります)。

1.  `scale.yaml`ファイルを作成し、新しいワーカー ノードの情報を追加します。

    > **注記：**
    >
    > トポロジファイルを作成する必要があります。このファイルには、既存のノードではなく、新しいノードの説明のみが含まれます。デプロイメントディレクトリなどの詳細な設定項目については、こちら[TiUP構成パラメータの例](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml)を参照してください。

    ```yaml
    ---

    worker_servers:
      - host: 172.16.5.140

    ```

2.  スケールアウト操作を実行します。TiUP TiUP DMは、 `scale.yaml`で説明したポート、ディレクトリ、その他の情報に従って、対応するノードをクラスターに追加します。

    ```shell
    tiup dm scale-out prod-cluster scale.yaml
    ```

    コマンドを実行した後、 `tiup dm display prod-cluster`実行してスケールアウトされたクラスターのステータスを確認できます。

## ローリングアップグレード {#rolling-upgrade}

> **注記：**
>
> v2.0.5 以降、dmctl は[データソースのエクスポートとインポート、およびクラスターのタスクコンフィグレーション](/dm/dm-export-import-config.md)サポートします。
>
> アップグレード前に、 `config export`使用してクラスターの設定ファイルをエクスポートできます。アップグレード後に以前のバージョンにダウングレードする必要がある場合は、まず以前のクラスターを再デプロイし、 `config import`使用して以前の設定ファイルをインポートできます。
>
> v2.0.5 より前のクラスターの場合は、dmctl (&gt;= v2.0.5 かつ &lt; v8.0.0) を使用して、データ ソースおよびタスク構成ファイルをエクスポートおよびインポートできます。
>
> v2.0.2以降のクラスターでは、現在、リレーワーカー関連の設定の自動インポートはサポートされていません`start-relay`コマンドを使用して手動で[リレーログを開始](/dm/relay-log.md#enable-and-disable-relay-log)実行できます。

ローリングアップグレードプロセスはアプリケーションに対して可能な限り透過的に実行され、ビジネスに影響を与えません。操作はノードごとに異なります。

### アップグレードコマンド {#upgrade-command}

DMクラスタをアップグレードするには、コマンド`tiup dm upgrade`を実行します。例えば、次のコマンドはクラスタを`${version}`にアップグレードします。このコマンドを実行する前に、 `${version}`必要なバージョンに変更してください。

> **注記：**
>
> バージョン8.0.0以降、DMは暗号化および復号化用の固定秘密鍵を削除し、暗号化および復号化用の秘密鍵をカスタマイズできるようになりました。アップグレード前に[データソース構成](/dm/dm-source-configuration-file.md)および[移行タスクの構成](/dm/task-configuration-file-full.md)で暗号化パスワードを使用している場合は、追加の操作については[DM 暗号化と復号化用の秘密鍵をカスタマイズする](/dm/dm-customized-secret-key.md)のアップグレード手順を参照してください。

```bash
tiup dm upgrade prod-cluster ${version}
```

## 構成の更新 {#update-configuration}

コンポーネント構成を動的に更新する場合、 TiUP DMコンポーネントは各クラスタの現在の構成を保存します。この構成を編集するには、 `tiup dm edit-config <cluster-name>`コマンドを実行します。例：

```bash
tiup dm edit-config prod-cluster
```

TiUP DMは設定ファイルをviエディタで開きます。他のエディタを使用する場合は、環境変数`EDITOR`使用してエディタをカスタマイズします（例： `export EDITOR=nano` ）。ファイルの編集後、変更を保存します。新しい設定をクラスターに適用するには、次のコマンドを実行します。

```bash
tiup dm reload prod-cluster
```

このコマンドは、構成をターゲット マシンに送信し、クラスターを再起動して構成を有効にします。

## コンポーネントの更新 {#update-component}

通常のアップグレードでは`upgrade`コマンドを使用できます。ただし、デバッグなどのシナリオでは、現在実行中のコンポーネントを一時パッケージに置き換える必要がある場合があります。これを行うには、 `patch`コマンドを使用します。

```bash
tiup dm patch --help
```

    Replace the remote package with a specified package and restart the service

    Usage:
      tiup dm patch <cluster-name> <package-path> [flags]

    Flags:
      -h, --help                   help for patch
      -N, --node strings           Specify the nodes
          --overwrite              Use this package in the future scale-out operations
      -R, --role strings           Specify the role
          --transfer-timeout int   Timeout in seconds when transferring dm-master leaders (default 600)

    Global Flags:
          --native-ssh         Use the native SSH client installed on local system instead of the build-in one.
          --ssh-timeout int    Timeout in seconds to connect host via SSH, ignored for operations that don't need an SSH connection. (default 5)
          --wait-timeout int   Timeout in seconds to wait for an operation to complete, ignored for operations that don't fit. (default 60)
      -y, --yes                Skip all confirmations and assumes 'yes'

DM マスター ホットフィックス パッケージが`/tmp/dm-master-hotfix.tar.gz`にあり、クラスター内のすべての DM マスター パッケージを置き換える場合は、次のコマンドを実行します。

```bash
tiup dm patch prod-cluster /tmp/dm-master-hotfix.tar.gz -R dm-master
```

クラスター内の DM マスター パッケージを 1 つだけ置き換えることもできます。

```bash
tiup dm patch prod-cluster /tmp/dm--hotfix.tar.gz -N 172.16.4.5:8261
```

## DM-Ansible を使用してデプロイされた DM 1.0 クラスターをインポートおよびアップグレードする {#import-and-upgrade-a-dm-1-0-cluster-deployed-using-dm-ansible}

> **注記：**
>
> -   TiUP は、DM 1.0 クラスターへの DM Portalコンポーネントのインポートをサポートしていません。
> -   インポートする前に元のクラスターを停止する必要があります。
> -   2.0 にアップグレードする必要があるタスクでは`stop-task`実行しないでください。
> -   TiUP は、v2.0.0-rc.2 以降のバージョンの DM クラスターへのインポートのみをサポートします。
> -   `import`コマンドは、DM 1.0 クラスターから新しい DM 2.0 クラスターにデータをインポートするために使用されます。既存の DM 2.0 クラスターに DM 移行タスクをインポートする必要がある場合は、 [TiDB データ移行を v1.0.x から v2.0+ に手動でアップグレードする](/dm/manually-upgrade-dm-1.0-to-2.0.md)参照してください。
> -   一部のコンポーネントのデプロイメントディレクトリは、元のクラスタのものと異なります。詳細を確認するには、 `display`コマンドを実行してください。
> -   インポートする前に`tiup update --self && tiup update dm`実行して、 TiUP DMコンポーネントが最新バージョンであることを確認します。
> -   インポート後、クラスターにはDMマスターノードが1つだけ存在します。DMマスターをスケールアウトするには、 [クラスターをスケールアウトする](#scale-out-a-cluster)を参照してください。

TiUPがリリースされる前は、DMクラスターのデプロイにはDM-Ansibleがよく使用されていました。DM-AnsibleによってデプロイされたDM 1.0クラスターをTiUPで引き継ぐには、 `import`コマンドを使用します。

たとえば、DM Ansible を使用してデプロイされたクラスターをインポートするには、次のようにします。

```bash
tiup dm import --dir=/path/to/dm-ansible --cluster-version ${version}
```

`tiup list dm-master`実行すると、 TiUPでサポートされている最新のクラスター バージョンが表示されます。

`import`コマンドを使用するプロセスは次のとおりです。

1.  TiUP は、DM-Ansible を使用して以前にデプロイされた DM クラスターに基づいてトポロジ ファイル[`topology.yml`](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml)を生成します。
2.  トポロジ ファイルが生成されたことを確認したら、それを使用して v2.0 以降のバージョンの DM クラスターをデプロイできます。

デプロイメントが完了したら、 `tiup dm start`コマンドを実行してクラスターを起動し、DM カーネルのアップグレード プロセスを開始できます。

## 操作ログをビュー {#view-the-operation-log}

操作ログを表示するには、 `audit`コマンドを使用します。3 `audit`の使用方法は次のとおりです。

```bash
Usage:
  tiup dm audit [audit-id] [flags]

Flags:
  -h, --help   help for audit
```

引数`[audit-id]`が指定されていない場合、コマンドは実行されたコマンドのリストを表示します。例:

```bash
tiup dm audit
```

    ID      Time                  Command
    --      ----                  -------
    4D5kQY  2020-08-13T05:38:19Z  tiup dm display test
    4D5kNv  2020-08-13T05:36:13Z  tiup dm list
    4D5kNr  2020-08-13T05:36:10Z  tiup dm deploy -p prod-cluster ${version} ./examples/dm/minimal.yaml

最初の列は`audit-id`です。特定のコマンドの実行ログを表示するには、次のように`audit-id`引数を渡します。

```bash
tiup dm audit 4D5kQY
```

## DM クラスター内のホストでコマンドを実行する {#run-commands-on-a-host-in-the-dm-cluster}

DMクラスタ内のホストでコマンドを実行するには、 `exec`コマンドを使用します。3 `exec`のコマンドの使用方法は次のとおりです。

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

たとえば、すべての DM ノードで`ls /tmp`実行するには、次のコマンドを実行します。

```bash
tiup dm exec prod-cluster --command='ls /tmp'
```

## dmctl {#dmctl}

TiUP はDM クラスタ コントローラ`dmctl`を統合します。

dmctl を使用するには、次のコマンドを実行します。

```bash
tiup dmctl [args]
```

dmctlのバージョンを指定します。このコマンドを実行する前に、 `${version}`必要なバージョンに変更してください。

    tiup dmctl:${version} [args]

以前のdmctlコマンドでソースを追加するには`dmctl --master-addr master1:8261 operate-source create /tmp/source1.yml`使用します。dmctlがTiUPに統合された後は、コマンドは以下のようになります。

```bash
tiup dmctl --master-addr master1:8261 operate-source create /tmp/source1.yml
```

## システムのネイティブSSHクライアントを使用してクラスタに接続します {#use-the-system-s-native-ssh-client-to-connect-to-cluster}

クラスタマシン上で実行される上記のすべての操作は、 TiUPに組み込まれたSSHクライアントを使用してクラスタに接続し、コマンドを実行します。ただし、シナリオによっては、制御マシンシステムにネイティブなSSHクライアントを使用してクラスタ操作を実行する必要がある場合もあります。例：

-   認証にSSHプラグインを使用するには
-   カスタマイズされたSSHクライアントを使用するには

次に、 `--native-ssh`コマンドライン フラグを使用して、システムネイティブのコマンドライン ツールを有効にできます。

-   クラスターをデプロイ: `tiup dm deploy <cluster-name> <version> <topo> --native-ssh` `<cluster-name>`にクラスターの名前、 `<version>`にデプロイする DM バージョン ( `v8.1.2`など)、 `<topo>`にトポロジ ファイル名を入力します。
-   クラスターを起動します: `tiup dm start <cluster-name> --native-ssh` .
-   クラスターのアップグレード: `tiup dm upgrade ... --native-ssh`

上記のすべてのクラスター操作コマンドに`--native-ssh`追加すると、システムのネイティブ SSH クライアントを使用できます。

すべてのコマンドにこのようなフラグを追加しないようにするには、 `TIUP_NATIVE_SSH`システム変数を使用して、ローカル SSH クライアントを使用するかどうかを指定します。

```sh
export TIUP_NATIVE_SSH=true
# or
export TIUP_NATIVE_SSH=1
# or
export TIUP_NATIVE_SSH=enable
```

この環境変数と`--native-ssh`同時に指定した場合、 `--native-ssh`優先されます。

> **注記：**
>
> クラスターの展開プロセス中に、接続にパスワードを使用する必要がある場合、またはキー ファイルに`passphrase`設定されている場合は、コントロール マシンに`sshpass`インストールされていることを確認する必要があります。そうでない場合、タイムアウト エラーが報告されます。
