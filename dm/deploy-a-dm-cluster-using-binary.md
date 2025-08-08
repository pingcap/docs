---
title: Deploy Data Migration Using DM Binary
summary: DM バイナリを使用してデータ移行クラスターをデプロイする方法を学習します。
---

# DMバイナリを使用したデータ移行のデプロイ {#deploy-data-migration-using-dm-binary}

このドキュメントでは、DM バイナリを使用してデータ移行 (DM) クラスターを迅速にデプロイする方法を紹介します。

> **注記：**
>
> 本番環境では、 [TiUPを使用してDMクラスタを展開する](/dm/deploy-a-dm-cluster-using-tiup.md)を推奨します。

## DMバイナリをダウンロード {#download-dm-binary}

DMバイナリはTiDB Toolkitに含まれています。TiDBTiDB Toolkitをダウンロードするには、 [TiDBツールをダウンロード](/download-ecosystem-tools.md)参照してください。

## サンプルシナリオ {#sample-scenario}

次のサンプル シナリオに基づいて DM クラスターを展開するとします。

2 つの DM ワーカー ノードと 3 つの DM マスター ノードが 5 台のサーバーに展開されます。

各ノードのアドレスは次のとおりです。

| 実例      | サーバーアドレス    | ポート  |
| :------ | :---------- | :--- |
| DMマスター1 | 192.168.0.4 | 8261 |
| DMマスター2 | 192.168.0.5 | 8261 |
| DMマスター3 | 192.168.0.6 | 8261 |
| DMワーカー1 | 192.168.0.7 | 8262 |
| DMワーカー2 | 192.168.0.8 | 8262 |

このシナリオに基づいて、次のセクションでは DM クラスターを展開する方法について説明します。

> **注記：**
>
> -   単一のサーバーに複数の DM マスターまたは DM ワーカー インスタンスを展開する場合、各インスタンスのポートと作業ディレクトリは一意である必要があります。
>
> -   DM クラスターの高可用性を確保する必要がない場合は、DM マスター ノードを 1 つだけデプロイし、デプロイされる DM ワーカー ノードの数は、移行するアップストリーム MySQL/MariaDB インスタンスの数以上である必要があります。
>
> -   DM クラスターの高可用性を確保するには、3 つの DM マスター ノードを展開することをお勧めします。また、展開する DM ワーカー ノードの数は、移行するアップストリーム MySQL/MariaDB インスタンスの数より多くする必要があります (たとえば、DM ワーカー ノードの数は、アップストリーム インスタンスの数より 2 つ多くなります)。
>
> -   次のコンポーネント間のポートが相互接続されていることを確認します。
>     -   DM マスター ノード間の`8291`ポートは相互接続されています。
>     -   各 DM マスター ノードは、すべての DM ワーカー ノードの`8262`ポートに接続できます。
>     -   各 DM ワーカー ノードは、すべての DM マスター ノードの`8261`ポートに接続できます。

### DMマスターをデプロイ {#deploy-dm-master}

[コマンドラインパラメータ](#dm-master-command-line-parameters)または[設定ファイル](#dm-master-configuration-file)使用して DM マスターを設定できます。

#### DMマスターのコマンドラインパラメータ {#dm-master-command-line-parameters}

DM マスターのコマンドライン パラメータの説明は次のとおりです。

```bash
./dm-master --help
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

> **注記：**
>
> 一部の設定がコマンドラインから参照できないため、上記の方法でDMマスターを設定できない場合があります。そのような場合は、代わりに設定ファイルを使用してください。

#### DMマスター構成ファイル {#dm-master-configuration-file}

以下はDM-masterの設定ファイルです。この方法でDM-masterを設定することをお勧めします。

1.  次の設定を`conf/dm-master1.toml`に書き込みます。

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

2.  DM-master を実行するには、ターミナルで次のコマンドを実行します。

    ```bash
    ./dm-master -config conf/dm-master1.toml
    ```

    > **注記：**
    >
    > このコマンドを実行した後、コンソールにはログは出力されません。実行時ログを表示するには、 `tail -f dm-master.log`実行してください。

3.  DM-master2とDM-master3については、設定ファイルの`name`それぞれ`master2`と`master3`に変更し、 `peer-urls`それぞれ`192.168.0.5:8291`と`192.168.0.6:8291`に変更します。その後、手順2を繰り返します。

### DM-workerをデプロイ {#deploy-dm-worker}

[コマンドラインパラメータ](#dm-worker-command-line-parameters)または[設定ファイル](#dm-worker-configuration-file)使用して DM-worker を構成できます。

#### DM-workerのコマンドラインパラメータ {#dm-worker-command-line-parameters}

DM-worker のコマンドライン パラメータの説明は次のとおりです。

```bash
./dm-worker --help
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

> **注記：**
>
> 一部の設定がコマンドラインから参照できないため、上記の方法でDM-workerを設定できない場合があります。そのような場合は、代わりに設定ファイルを使用してください。

#### DMワーカー構成ファイル {#dm-worker-configuration-file}

以下はDM-workerの設定ファイルです。この方法でDM-workerを設定することをお勧めします。

1.  次の設定を`conf/dm-worker1.toml`に書き込みます。

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

2.  DM-worker を実行するには、ターミナルで次のコマンドを実行します。

    ```bash
    ./dm-worker -config conf/dm-worker1.toml
    ```

3.  DM-worker2 の場合、設定ファイルの`name` `worker2`に変更します。その後、手順 2 を繰り返します。

これで、DM クラスターが正常にデプロイされました。
