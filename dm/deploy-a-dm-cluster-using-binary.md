---
title: Deploy Data Migration Using DM Binary
summary: Learn how to deploy a Data Migration cluster using DM binary.
---

# DMバイナリを使用したデータ移行のデプロイ {#deploy-data-migration-using-dm-binary}

このドキュメントでは、DMバイナリを使用してデータ移行（DM）クラスタをすばやく展開する方法を紹介します。

> **ノート：**
>
> 実稼働環境では、 [TiUPを使用してDMクラスタをデプロイする](/dm/deploy-a-dm-cluster-using-tiup.md)にすることをお勧めします。

## DMバイナリをダウンロード {#download-dm-binary}

DMバイナリはTiDB Toolkitに含まれています。 TiDB Toolkitをダウンロードするには、 [TiDBツールをダウンロードする](/download-ecosystem-tools.md)を参照してください。

## サンプルシナリオ {#sample-scenario}

このサンプルシナリオに基づいてDMクラスタを展開するとします。

2つのDM-workerノードと3つのDM-masterノードが5つのサーバーにデプロイされます。

各ノードのアドレスは次のとおりです。

| 実例         | サーバーアドレス    | ポート  |
| :--------- | :---------- | :--- |
| DM-master1 | 192.168.0.4 | 8261 |
| DM-master2 | 192.168.0.5 | 8261 |
| DM-master3 | 192.168.0.6 | 8261 |
| DM-worker1 | 192.168.0.7 | 8262 |
| DM-worker2 | 192.168.0.8 | 8262 |

このシナリオに基づいて、次のセクションでは、DMクラスタをデプロイする方法について説明します。

> **ノート：**
>
> -   複数のDM-masterまたはDM-workerインスタンスを単一のサーバーにデプロイする場合、各インスタンスのポートと作業ディレクトリは一意である必要があります。
>
> -   DMクラスタの高可用性を確保する必要がない場合は、DM-masterノードを1つだけデプロイし、デプロイされるDM-workerノードの数は、移行するアップストリームのMySQL/MariaDBインスタンスの数以上である必要があります。
>
> -   DMクラスタの高可用性を確保するには、3つのDM-masterノードをデプロイすることをお勧めします。デプロイされるDM-workerノードの数は、移行するアップストリームのMySQL / MariaDBインスタンスの数（たとえば、 DMワーカーノードの数は、アップストリームインスタンスの数より2つ多くなります）。
>
> -   次のコンポーネント間のポートが相互接続されていることを確認してください。
>     -   DMマスターノード間の`8291`のポートは相互接続されています。
>     -   各DMマスターノードは、すべてのDMワーカーノードの`8262`のポートに接続できます。
>     -   各DM-workerノードは、すべてのDM-masterノードの`8261`のポートに接続できます。

### DMマスターをデプロイ {#deploy-dm-master}

[コマンドラインパラメータ](#dm-master-command-line-parameters)または[構成ファイル](#dm-master-configuration-file)を使用してDMマスターを構成できます。

#### DM-masterコマンドラインパラメーター {#dm-master-command-line-parameters}

以下は、DM-masterコマンドラインパラメーターの説明です。

```bash
./dm-master --help
```

```
Usage of dm-master:
  -L string
        log level: debug, info, warn, error, fatal (default "info")
  -V    prints version and exit
  -advertise-addr string
        advertise address for client traffic (default "${master-addr}")
  -advertise-peer-urls string
        advertise URLs for peer traffic (default "${peer-urls}")
  -config string
        path to config file
  -data-dir string
        path to the data directory (default "default.${name}")
  -initial-cluster string
        initial cluster configuration for bootstrapping, e.g. dm-master=http://127.0.0.1:8291
  -join string
        join to an existing cluster (usage: cluster's "${master-addr}" list, e.g. "127.0.0.1:8261,127.0.0.1:18261"
  -log-file string
        log file path
  -master-addr string
        master API server and status addr
  -name string
        human-readable name for this DM-master member
  -peer-urls string
        URLs for peer traffic (default "http://127.0.0.1:8291")
  -print-sample-config
        print sample config file of dm-worker
```

> **ノート：**
>
> 一部の構成はコマンドラインに公開されていないため、状況によっては、上記の方法を使用してDMマスターを構成できない場合があります。このような場合は、代わりに構成ファイルを使用してください。

#### DMマスター構成ファイル {#dm-master-configuration-file}

以下はDM-masterの設定ファイルです。この方法を使用してDMマスターを構成することをお勧めします。

1.  次の構成を`conf/dm-master1.toml`に書き込みます。

    ```toml
    # Master Configuration.
    name = "master1"

    # Log configurations.
    log-level = "info"
    log-file = "dm-master.log"

    # The listening address of DM-master.
    master-addr = "192.168.0.4:8261"

    # The peer URLs of DM-master.
    peer-urls = "192.168.0.4:8291"

    # The value of `initial-cluster` is the combination of the `advertise-peer-urls` value of all DM-master nodes in the initial cluster.
    initial-cluster = "master1=http://192.168.0.4:8291,master2=http://192.168.0.5:8291,master3=http://192.168.0.6:8291"
    ```

2.  ターミナルで次のコマンドを実行して、DM-masterを実行します。

    {{< copyable "" >}}

    ```bash
    ./dm-master -config conf/dm-master1.toml
    ```

    > **ノート：**
    >
    > このコマンドが実行された後、コンソールはログを出力しません。ランタイムログを表示したい場合は、 `tail -f dm-master.log`を実行できます。

3.  DM-master2とDM-master3の場合、構成ファイルの`name`をそれぞれ`master2`と`master3`に変更し、 `peer-urls`をそれぞれ`192.168.0.5:8291`と`192.168.0.6:8291`に変更します。次に、手順2を繰り返します。

### DM-workerをデプロイ {#deploy-dm-worker}

[コマンドラインパラメータ](#dm-worker-command-line-parameters)または[構成ファイル](#dm-worker-configuration-file)を使用してDM-workerを構成できます。

#### DM-workerコマンドラインパラメーター {#dm-worker-command-line-parameters}

以下は、DM-workerコマンドラインパラメーターの説明です。

{{< copyable "" >}}

```bash
./dm-worker --help
```

```
Usage of worker:
  -L string
        log level: debug, info, warn, error, fatal (default "info")
  -V    prints version and exit
  -advertise-addr string
        advertise address for client traffic (default "${worker-addr}")
  -config string
        path to config file
  -join string
        join to an existing cluster (usage: dm-master cluster's "${master-addr}")
  -keepalive-ttl int
        dm-worker's TTL for keepalive with etcd (in seconds) (default 10)
  -log-file string
        log file path
  -name string
        human-readable name for DM-worker member
  -print-sample-config
        print sample config file of dm-worker
  -worker-addr string
        listen address for client traffic
```

> **ノート：**
>
> 一部の構成はコマンドラインに公開されていないため、状況によっては、上記の方法を使用してDM-workerを構成できない場合があります。このような場合は、代わりに構成ファイルを使用してください。

#### DM-worker構成ファイル {#dm-worker-configuration-file}

以下は、DM-worker構成ファイルです。この方法を使用してDM-workerを構成することをお勧めします。

1.  次の構成を`conf/dm-worker1.toml`に書き込みます。

    ```toml
    # Worker Configuration.
    name = "worker1"

    # Log configuration.
    log-level = "info"
    log-file = "dm-worker.log"

    # DM-worker address.
    worker-addr = ":8262"

    # The master-addr configuration of the DM-master nodes in the cluster.
    join = "192.168.0.4:8261,192.168.0.5:8261,192.168.0.6:8261"
    ```

2.  ターミナルで次のコマンドを実行して、DM-workerを実行します。

    {{< copyable "" >}}

    ```bash
    ./dm-worker -config conf/dm-worker1.toml
    ```

3.  DM-worker2の場合、構成ファイルの`name`を`worker2`に変更します。次に、手順2を繰り返します。

これで、DMクラスタが正常にデプロイされました。
