---
title: Deploy Data Migration Using DM Binary
summary: Learn how to deploy a Data Migration cluster using DM binary.
---

# DM Binary を使用したデータ移行のデプロイ {#deploy-data-migration-using-dm-binary}

このドキュメントでは、DM バイナリを使用して Data Migration (DM) クラスターを迅速にデプロイする方法を紹介します。

> **ノート：**
>
> 本番環境では、 [TiUP を使用して DM クラスターをデプロイする](/dm/deploy-a-dm-cluster-using-tiup.md)にすることをお勧めします。

## DMバイナリをダウンロード {#download-dm-binary}

DM バイナリはTiDB Toolkitに含まれています。 TiDB Toolkitをダウンロードするには、 [TiDB ツールをダウンロード](/download-ecosystem-tools.md)を参照してください。

## サンプル シナリオ {#sample-scenario}

次のサンプル シナリオに基づいて DM クラスタを展開するとします。

2 つの DM-worker ノードと 3 つの DM-master ノードが 5 つのサーバーにデプロイされます。

各ノードのアドレスは次のとおりです。

| 実例      | サーバーアドレス    | ポート  |
| :------ | :---------- | :--- |
| DMマスター1 | 192.168.0.4 | 8261 |
| DMマスター2 | 192.168.0.5 | 8261 |
| DMマスター3 | 192.168.0.6 | 8261 |
| DMワーカー1 | 192.168.0.7 | 8262 |
| DMワーカー2 | 192.168.0.8 | 8262 |

このシナリオに基づいて、以下のセクションでは DM クラスターを展開する方法について説明します。

> **ノート：**
>
> -   複数の DM-master または DM-worker インスタンスを 1 つのサーバーにデプロイする場合、各インスタンスのポートと作業ディレクトリは一意である必要があります。
>
> -   DM クラスターの高可用性を確保する必要がない場合は、DM マスター ノードを 1 つだけデプロイします。デプロイされる DM ワーカー ノードの数は、移行するアップストリームの MySQL/MariaDB インスタンスの数以上でなければなりません。
>
> -   DM クラスターの高可用性を確保するには、3 つの DM マスター ノードをデプロイすることをお勧めします。デプロイされる DM ワーカー ノードの数は、移行する上流の MySQL/MariaDB インスタンスの数よりも多くする必要があります (たとえば、数DM-worker ノードの数は、アップストリーム インスタンスの数よりも 2 つ多くなります)。
>
> -   次のコンポーネント間のポートが相互接続されていることを確認してください。
>     -   DM-master ノードの`8291`ポートは相互接続されています。
>     -   各 DM マスター ノードは、すべての DM ワーカー ノードの`8262`ポートに接続できます。
>     -   各 DM-worker ノードは、すべての DM-master ノードの`8261`ポートに接続できます。

### DM マスターをデプロイ {#deploy-dm-master}

[コマンドライン パラメータ](#dm-master-command-line-parameters)または[構成ファイル](#dm-master-configuration-file)を使用して DM-master を構成できます。

#### DM マスター コマンドライン パラメータ {#dm-master-command-line-parameters}

以下は、DM-master コマンドライン パラメータの説明です。

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
> 状況によっては、一部の構成がコマンド ラインに公開されないため、上記の方法を使用して DM マスターを構成できないことがあります。そのような場合は、代わりに構成ファイルを使用してください。

#### DM マスター構成ファイル {#dm-master-configuration-file}

以下はDM-masterの設定ファイルです。この方法を使用して DM-master を構成することをお勧めします。

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

2.  ターミナルで次のコマンドを実行して、DM-master を実行します。

    {{< copyable "" >}}

    ```bash
    ./dm-master -config conf/dm-master1.toml
    ```

    > **ノート：**
    >
    > このコマンドの実行後、コンソールはログを出力しません。ランタイム ログを表示する場合は、 `tail -f dm-master.log`を実行できます。

3.  DM-master2 と DM-master3 の場合、構成ファイルの`name`それぞれ`master2`と`master3`に変更し、 `peer-urls`それぞれ`192.168.0.5:8291`と`192.168.0.6:8291`に変更します。その後、手順 2 を繰り返します。

### DM ワーカーをデプロイ {#deploy-dm-worker}

[コマンドライン パラメータ](#dm-worker-command-line-parameters)または[構成ファイル](#dm-worker-configuration-file)を使用して DM-worker を構成できます。

#### DM-worker コマンドライン パラメータ {#dm-worker-command-line-parameters}

以下は、DM-worker コマンドライン パラメータの説明です。

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
> 状況によっては、一部の構成がコマンド ラインに公開されていないため、上記の方法を使用して DM-worker を構成できないことがあります。そのような場合は、代わりに構成ファイルを使用してください。

#### DM-worker 構成ファイル {#dm-worker-configuration-file}

以下は、DM-worker 構成ファイルです。この方法を使用して DM-worker を構成することをお勧めします。

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

2.  ターミナルで次のコマンドを実行して、DM-worker を実行します。

    {{< copyable "" >}}

    ```bash
    ./dm-worker -config conf/dm-worker1.toml
    ```

3.  DM-worker2 の場合、構成ファイルの`name` `worker2`に変更します。その後、手順 2 を繰り返します。

これで、DM クラスターが正常にデプロイされました。
