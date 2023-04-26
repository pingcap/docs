---
title: TiKV Control User Guide
summary: Use TiKV Control to manage a TiKV cluster.
---

# TiKV Controlユーザー ガイド {#tikv-control-user-guide}

TiKV Control ( `tikv-ctl` ) は、クラスターを管理するために使用される TiKV のコマンド ライン ツールです。そのインストール ディレクトリは次のとおりです。

-   クラスタがTiUPを使用してデプロイされている場合、 `tikv-ctl`ディレクトリは`~/.tiup/components/ctl/{VERSION}/`のディレクトリにあります。

## TiUPでTiKV Controlを使用する {#use-tikv-control-in-tiup}

> **ノート：**
>
> 使用するコントロール ツールのバージョンは、クラスターのバージョンと一致していることが推奨されます。

`tiup`コマンドにも`tikv-ctl`組み込まれています。次のコマンドを実行して、 `tikv-ctl`ツールを呼び出します。

```shell
tiup ctl:v<CLUSTER_VERSION> tikv
```

```
Starting component `ctl`: /home/tidb/.tiup/components/ctl/v4.0.8/ctl tikv
TiKV Control (tikv-ctl)
Release Version:   4.0.8
Edition:           Community
Git Commit Hash:   83091173e960e5a0f5f417e921a0801d2f6635ae
Git Commit Branch: heads/refs/tags/v4.0.8
UTC Build Time:    2020-10-30 08:40:33
Rust Version:      rustc 1.42.0-nightly (0de96d37f 2019-12-19)
Enable Features:   jemalloc mem-profiling portable sse protobuf-codec
Profile:           dist_release

A tool for interacting with TiKV deployments.
USAGE:
    TiKV Control (tikv-ctl) [FLAGS] [OPTIONS] [SUBCOMMAND]
FLAGS:
    -h, --help                    Prints help information
        --skip-paranoid-checks    Skip paranoid checks when open rocksdb
    -V, --version                 Prints version information
OPTIONS:
        --ca-path <ca-path>              Set the CA certificate path
        --cert-path <cert-path>          Set the certificate path
        --config <config>                TiKV config path, by default it's <deploy-dir>/conf/tikv.toml
        --data-dir <data-dir>            TiKV data directory path, check <deploy-dir>/scripts/run.sh to get it
        --decode <decode>                Decode a key in escaped format
        --encode <encode>                Encode a key in escaped format
        --to-hex <escaped-to-hex>        Convert an escaped key to hex key
        --to-escaped <hex-to-escaped>    Convert a hex key to escaped key
        --host <host>                    Set the remote host
        --key-path <key-path>            Set the private key path
        --log-level <log-level>          Set the log level [default: warn]
        --pd <pd>                        Set the address of pd
SUBCOMMANDS:
    bad-regions           Get all regions with corrupt raft
    cluster               Print the cluster id
    compact               Compact a column family in a specified range
    compact-cluster       Compact the whole cluster in a specified range in one or more column families
    consistency-check     Force a consistency-check for a specified region
    decrypt-file          Decrypt an encrypted file
    diff                  Calculate difference of region keys from different dbs
    dump-snap-meta        Dump snapshot meta file
    encryption-meta       Dump encryption metadata
    fail                  Inject failures to TiKV and recovery
    help                  Prints this message or the help of the given subcommand(s)
    metrics               Print the metrics
    modify-tikv-config    Modify tikv config, eg. tikv-ctl --host ip:port modify-tikv-config -n
                          rocksdb.defaultcf.disable-auto-compactions -v true
    mvcc                  Print the mvcc value
    print                 Print the raw value
    raft                  Print a raft log entry
    raw-scan              Print all raw keys in the range
    recover-mvcc          Recover mvcc data on one node by deleting corrupted keys
    recreate-region       Recreate a region with given metadata, but alloc new id for it
    region-properties     Show region properties
    scan                  Print the range db range
    size                  Print region size
    split-region          Split the region
    store                 Print the store id
    tombstone             Set some regions on the node to tombstone by manual
    unsafe-recover        Unsafely recover the cluster when the majority replicas are failed
```

`tiup ctl:v<CLUSTER_VERSION> tikv`の後に、対応するパラメーターとサブコマンドを追加できます。

## 一般オプション {#general-options}

`tikv-ctl` 2 つの操作モードを提供します。

-   リモート モード: `--host`オプションを使用して、TiKV のサービス アドレスを引数として受け入れます。

    このモードでは、TiKV で SSL が有効になっている場合、関連する証明書ファイル`tikv-ctl`指定する必要があります。例えば：

    ```shell
    tikv-ctl --ca-path ca.pem --cert-path client.pem --key-path client-key.pem --host 127.0.0.1:20160 <subcommands>
    ```

    ただし、TiKV ではなく`tikv-ctl`と通信する場合もあります。この場合、 `--host`の代わりに`--pd`オプションを使用する必要があります。次に例を示します。

    ```shell
    tikv-ctl --pd 127.0.0.1:2379 compact-cluster
    ```

    ```
    store:"127.0.0.1:20160" compact db:KV cf:default range:([], []) success!
    ```

-   ローカルモード:

    -   `--data-dir`オプションを使用して、ローカルの TiKV データ ディレクトリ パスを指定します。
    -   `--config`オプションを使用して、ローカルの TiKV 構成ファイル パスを指定します。

    このモードでは、実行中の TiKV インスタンスを停止する必要があります。

特に明記しない限り、すべてのコマンドはリモート モードとローカル モードの両方をサポートします。

さらに、 `tikv-ctl` 2 つの単純なコマンド`--to-hex`と`--to-escaped`があり、キーの形状を単純に変更するために使用されます。

通常、キーの`escaped`形式を使用します。例えば：

```shell
tikv-ctl --to-escaped 0xaaff
\252\377
tikv-ctl --to-hex "\252\377"
AAFF
```

> **ノート：**
>
> コマンド ラインでキーの`escaped`形式を指定する場合は、二重引用符で囲む必要があります。そうしないと、bash がバックスラッシュを食べてしまい、間違った結果が返されます。

## サブコマンド、いくつかのオプションとフラグ {#subcommands-some-options-and-flags}

このセクションでは、 `tikv-ctl`がサポートするサブコマンドについて詳しく説明します。一部のサブコマンドは、多くのオプションをサポートしています。詳細については、 `tikv-ctl --help <subcommand>`を実行してください。

### Raftステート マシンの情報をビュー {#view-information-of-the-raft-state-machine}

`raft`サブコマンドを使用して、特定の時点でのRaftステート マシンのステータスを表示します。ステータス情報には、3 つの構造体 ( **RegionLocalState** 、 <strong>RaftLocalState</strong> 、および<strong>RegionApplyState</strong> ) と、特定のログ片の対応するエントリの 2 つの部分が含まれます。

`region`および`log`サブコマンドを使用して、上記の情報をそれぞれ取得します。 2 つのサブコマンドは両方とも、リモート モードとローカル モードを同時にサポートします。

`region`サブコマンドの場合:

-   表示するリージョンを指定するには、 `-r`オプションを使用します。複数のリージョンは`,`で区切られます。 `--all-regions`オプションを使用して、すべての地域を表示することもできます。 `-r`と`--all-regions`同時に使用できませんのでご注意ください。
-   印刷するリージョンの数を制限するには、 `--limit`オプションを使用します (デフォルト: `16` )。
-   特定のキー範囲に含まれるリージョンを照会するには、 `--start`および`--end`オプションを使用します (デフォルト: 範囲制限なし、16 進形式)。

たとえば、ID `1239`のリージョンを出力するには、次のコマンドを使用します。

```shell
tikv-ctl --host 127.0.0.1:20160 raft region -r 1239
```

出力は次のとおりです。

```
"region id": 1239
"region state": {
    id: 1239,
    start_key: 7480000000000000FF4E5F728000000000FF1443770000000000FA,
    end_key: 7480000000000000FF4E5F728000000000FF21C4420000000000FA,
    region_epoch: {conf_ver: 1 version: 43},
    peers: [ {id: 1240 store_id: 1 role: Voter} ]
}
"raft state": {
    hard_state {term: 8 vote: 5 commit: 7}
    last_index: 8)
}
"apply state": {
    applied_index: 8 commit_index: 8 commit_term: 8
    truncated_state {index: 5 term: 5}
}
```

特定のキー範囲に含まれるリージョンを照会するには、次のコマンドを使用します。

-   キー範囲がリージョン範囲内にある場合、リージョン情報が出力されます。
-   キー範囲がリージョン範囲と同じ場合、たとえば、指定されたキー範囲がリージョン`1239`と同じ場合、リージョン範囲は左が閉じて右が開いている間隔であり、リージョン`1009`は`end_key`のリージョン`1239` `start_key`として、リージョン`1009`の情報も出力されます。

```shell
tikv-ctl --host 127.0.0.1:20160 raft region --start 7480000000000000FF4E5F728000000000FF1443770000000000FA --end 7480000000000000FF4E5F728000000000FF21C4420000000000FA
```

出力は次のとおりです。

```
"region state": {
    id: 1009
    start_key: 7480000000000000FF4E5F728000000000FF21C4420000000000FA,
    end_key: 7480000000000000FF5000000000000000F8,
    ...
}
"region state": {
    id: 1239
    start_key: 7480000000000000FF4E5F728000000000FF06C6D60000000000FA,
    end_key: 7480000000000000FF4E5F728000000000FF1443770000000000FA,
    ...
}
```

### リージョンサイズをビュー {#view-the-region-size}

`size`コマンドを使用して、リージョンサイズを表示します。

```shell
tikv-ctl --data-dir /path/to/tikv size -r 2
```

出力は次のとおりです。

```
region id: 2
cf default region size: 799.703 MB
cf write region size: 41.250 MB
cf lock region size: 27616
```

### スキャンして特定範囲の MVCC を表示 {#scan-to-view-mvcc-of-a-specific-range}

`scan`コマンドの`--from`および`--to`オプションは、未加工のキーの 2 つのエスケープ形式を受け入れ、 `--show-cf`フラグを使用して、表示する必要がある列ファミリーを指定します。

```shell
tikv-ctl --data-dir /path/to/tikv scan --from 'zm' --limit 2 --show-cf lock,default,write
```

```
key: zmBootstr\377a\377pKey\000\000\377\000\000\373\000\000\000\000\000\377\000\000s\000\000\000\000\000\372
         write cf value: start_ts: 399650102814441473 commit_ts: 399650102814441475 short_value: "20"
key: zmDB:29\000\000\377\000\374\000\000\000\000\000\000\377\000H\000\000\000\000\000\000\371
         write cf value: start_ts: 399650105239273474 commit_ts: 399650105239273475 short_value: "\000\000\000\000\000\000\000\002"
         write cf value: start_ts: 399650105199951882 commit_ts: 399650105213059076 short_value: "\000\000\000\000\000\000\000\001"
```

### 特定のキーの MVCCをビュー {#view-mvcc-of-a-given-key}

`scan`コマンドと同様に、 `mvcc`コマンドを使用して、特定のキーの MVCC を表示できます。

```shell
tikv-ctl --data-dir /path/to/tikv mvcc -k "zmDB:29\000\000\377\000\374\000\000\000\000\000\000\377\000H\000\000\000\000\000\000\371" --show-cf=lock,write,default
```

```
key: zmDB:29\000\000\377\000\374\000\000\000\000\000\000\377\000H\000\000\000\000\000\000\371
         write cf value: start_ts: 399650105239273474 commit_ts: 399650105239273475 short_value: "\000\000\000\000\000\000\000\002"
         write cf value: start_ts: 399650105199951882 commit_ts: 399650105213059076 short_value: "\000\000\000\000\000\000\000\001"
```

このコマンドでは、キーは raw キーのエスケープ形式でもあります。

### 生のキーをスキャンする {#scan-raw-keys}

`raw-scan`コマンドは、RocksDB から直接スキャンします。データ キーをスキャンするには、キーに`'z'`プレフィックスを追加する必要があることに注意してください。

`--from`と`--to`オプションを使用して、スキャンする範囲を指定します (デフォルトでは無制限)。印刷するキーの数を最大で`--limit`に制限するには、5 を使用します (デフォルトでは 30)。 `--cf`を使用して、スキャンする cf を指定します ( `default` 、 `write`または`lock`のいずれか)。

```shell
tikv-ctl --data-dir /var/lib/tikv raw-scan --from 'zt' --limit 2 --cf default
```

```
key: "zt\200\000\000\000\000\000\000\377\005_r\200\000\000\000\000\377\000\000\001\000\000\000\000\000\372\372b2,^\033\377\364", value: "\010\002\002\002%\010\004\002\010root\010\006\002\000\010\010\t\002\010\n\t\002\010\014\t\002\010\016\t\002\010\020\t\002\010\022\t\002\010\024\t\002\010\026\t\002\010\030\t\002\010\032\t\002\010\034\t\002\010\036\t\002\010 \t\002\010\"\t\002\010s\t\002\010&\t\002\010(\t\002\010*\t\002\010,\t\002\010.\t\002\0100\t\002\0102\t\002\0104\t\002"
key: "zt\200\000\000\000\000\000\000\377\025_r\200\000\000\000\000\377\000\000\023\000\000\000\000\000\372\372b2,^\033\377\364", value: "\010\002\002&slow_query_log_file\010\004\002P/usr/local/mysql/data/localhost-slow.log"

Total scanned keys: 2
```

### 特定のキー値を出力する {#print-a-specific-key-value}

キーの値を表示するには、 `print`コマンドを使用します。

### リージョンに関するいくつかのプロパティを印刷する {#print-some-properties-about-region}

リージョンの状態の詳細を記録するために、TiKV はいくつかの統計をリージョンの SST ファイルに書き込みます。これらのプロパティを表示するには、 `region-properties`サブコマンドで`tikv-ctl`を実行します。

```shell
tikv-ctl --host localhost:20160 region-properties -r 2
```

```
num_files: 0
num_entries: 0
num_deletes: 0
mvcc.min_ts: 18446744073709551615
mvcc.max_ts: 0
mvcc.num_rows: 0
mvcc.num_puts: 0
mvcc.num_versions: 0
mvcc.max_row_versions: 0
middle_key_by_approximate_size:
```

プロパティを使用して、リージョンが正常かどうかを確認できます。そうでない場合は、それらを使用してリージョンを修正できます。たとえば、 リージョン を`middle_key_approximate_size`で手動で分割します。

### 各 TiKV のデータを手動で圧縮する {#compact-data-of-each-tikv-manually}

`compact`コマンドを使用して、各 TiKV のデータを手動で圧縮します。

-   `--from`および`--to`オプションを使用して、圧縮範囲をエスケープされた raw キーの形式で指定します。設定されていない場合、範囲全体が圧縮されます。

-   特定の領域の範囲を圧縮するには、 `--region`オプションを使用します。設定すると、 `--from`と`--to`は無視されます。

-   `--db`オプションを使用して、圧縮を実行する RocksDB を指定します。オプションの値は`kv`と`raft`です。

-   `--threads`オプションを使用すると、TiKV 圧縮の同時実行数を指定できます。デフォルト値は`8`です。一般に、コンカレンシーが高いほど圧縮速度が速くなりますが、サービスに影響を与える可能性があります。シナリオに基づいて、適切な同時実行数を選択する必要があります。

-   `--bottommost`オプションを使用して、TiKV が圧縮を実行するときに一番下のファイルを含めたり除外したりします。値のオプションは`default` 、 `skip` 、および`force`です。デフォルト値は`default`です。
    -   `default`圧縮フィルター機能が有効になっている場合にのみ、一番下のファイルが含まれることを意味します。
    -   `skip` TiKV が圧縮を実行するときに、一番下のファイルが除外されることを意味します。
    -   `force` TiKV が圧縮を実行するときに、一番下のファイルが常に含まれることを意味します。

-   ローカル モードでデータを圧縮するには、次のコマンドを使用します。

    ```shell
    tikv-ctl --data-dir /path/to/tikv compact --db kv
    ```

-   リモート モードでデータを圧縮するには、次のコマンドを使用します。

    ```shell
    tikv-ctl --host ip:port compact --db kv
    ```

### TiKV クラスター全体のデータを手動で圧縮する {#compact-data-of-the-whole-tikv-cluster-manually}

`compact-cluster`コマンドを使用して、TiKV クラスター全体のデータを手動で圧縮します。このコマンドのフラグの意味と使用法は、 `compact`コマンドのフラグと同じです。

### リージョンをトゥームストーンに設定する {#set-a-region-to-tombstone}

`tombstone`コマンドは通常、sync-log が有効になっておらず、 Raftステート マシンに書き込まれた一部のデータが電源切断によって失われる状況で使用されます。

TiKV インスタンスでは、このコマンドを使用して、一部のリージョンのステータスをトゥームストーンに設定できます。その後、インスタンスを再起動すると、それらのリージョンのRaftステート マシンの損傷によって引き起こされる再起動の失敗を回避するために、それらのリージョンはスキップされます。これらのリージョンでは、 Raftメカニズムを介して読み取りと書き込みを続行できるように、他の TiKV インスタンスに十分な健全なレプリカが必要です。

通常、 `remove-peer`コマンドを使用して、このリージョンの対応するピアを削除できます。

```shell
pd-ctl operator add remove-peer <region_id> <store_id>
```

次に、 `tikv-ctl`ツールを使用して、リージョンを対応する TiKV インスタンスのトゥームストーンに設定し、起動時にこのリージョンのヘルス チェックをスキップします。

```shell
tikv-ctl --data-dir /path/to/tikv tombstone -p 127.0.0.1:2379 -r <region_id>
```

```
success!
```

ただし、場合によっては、このリージョンのピアを PD から簡単に削除できないため、 `tikv-ctl`の`--force`オプションを指定して、ピアを強制的にトゥームストーンに設定できます。

```shell
tikv-ctl --data-dir /path/to/tikv tombstone -p 127.0.0.1:2379 -r <region_id>,<region_id> --force
```

```
success!
```

> **ノート：**
>
> -   `tombstone`コマンドは、ローカル モードのみをサポートします。
> -   `-p`オプションの引数は、 `http`プレフィックスなしで PD エンドポイントを指定します。 PD エンドポイントを指定することは、PD が安全に Tombstone に切り替えることができるかどうかを照会することです。

### <code>consistency-check</code>リクエストを TiKV に送信する {#send-a-code-consistency-check-code-request-to-tikv}

`consistency-check`コマンドを使用して、特定のリージョンの対応するRaft内のレプリカ間で整合性チェックを実行します。チェックが失敗すると、TiKV 自体がパニックになります。 `--host`で指定された TiKV インスタンスがリージョンリーダーでない場合、エラーが報告されます。

```shell
tikv-ctl --host 127.0.0.1:20160 consistency-check -r 2
success!
tikv-ctl --host 127.0.0.1:20161 consistency-check -r 2
DebugClient::check_region_consistency: RpcFailure(RpcStatus { status: Unknown, details: Some("StringError(\"Leader is on store 1\")") })
```

> **ノート：**
>
> -   `consistency-check`コマンドの使用はお勧めし**ません**。TiDB のガベージコレクションと互換性がなく、誤ってエラーを報告する可能性があるためです。
> -   このコマンドは、リモート モードのみをサポートします。
> -   このコマンドが`success!`を返す場合でも、TiKV がパニックするかどうかを確認する必要があります。これは、このコマンドがリーダーに対して整合性チェックを要求する提案に過ぎず、チェック プロセス全体が成功したかどうかをクライアントから知ることができないためです。

### スナップショット メタのダンプ {#dump-snapshot-meta}

このサブコマンドは、指定されたパスにあるスナップショット メタ ファイルを解析し、結果を出力するために使用されます。

### Raftステート マシンが破損している領域を出力します。 {#print-the-regions-where-the-raft-state-machine-corrupts}

TiKV の開始中にリージョンをチェックしないようにするために、 `tombstone`コマンドを使用して、 Raftステート マシンがエラーをトゥームストーンに報告するリージョンを設定できます。このコマンドを実行する前に、 `bad-regions`コマンドを使用してエラーのあるリージョンを見つけ、複数のツールを組み合わせて自動処理を行います。

```shell
tikv-ctl --data-dir /path/to/tikv bad-regions
```

```
all regions are healthy
```

コマンドが正常に実行されると、上記の情報が出力。コマンドが失敗すると、不正なリージョンのリストが出力。現在、検出できるエラーには、 `last index` 、 `commit index` 、および`apply index`の不一致、およびRaftログの損失が含まれます。スナップショット ファイルの損傷などのその他の状態については、さらにサポートが必要です。

### リージョンのプロパティをビュー {#view-region-properties}

-   `/path/to/tikv`にデプロイされた TiKV インスタンスのリージョン2 のプロパティをローカルで表示するには:

    ```shell
    tikv-ctl --data-dir /path/to/tikv/data region-properties -r 2
    ```

-   `127.0.0.1:20160`で実行されている TiKV インスタンスのリージョン2 のプロパティをオンラインで表示するには、次のようにします。

    ```shell
    tikv-ctl --host 127.0.0.1:20160 region-properties -r 2
    ```

### TiKV 構成を動的に変更する {#modify-the-tikv-configuration-dynamically}

`modify-tikv-config`コマンドを使用して、構成引数を動的に変更できます。現在、動的に変更できる TiKV の構成項目と詳細な変更は、SQL ステートメントを使用した構成の変更と一致しています。詳細については、 [TiKV 構成を動的に変更する](/dynamic-config.md#modify-tikv-configuration-dynamically)を参照してください。

-   `-n`は、構成アイテムの完全な名前を指定するために使用されます。動的に変更できる構成アイテムのリストについては、 [TiKV 構成を動的に変更する](/dynamic-config.md#modify-tikv-configuration-dynamically)を参照してください。
-   `-v`は、構成値を指定するために使用されます。

`shared block cache`のサイズを設定します。

```shell
tikv-ctl --host ip:port modify-tikv-config -n storage.block-cache.capacity -v 10GB
```

```
success
```

`shared block cache`が無効の場合、 `write` CF に`block cache size`を設定します。

```shell
tikv-ctl --host ip:port modify-tikv-config -n rocksdb.writecf.block-cache-size -v 256MB
```

```
success
```

```shell
tikv-ctl --host ip:port modify-tikv-config -n raftdb.defaultcf.disable-auto-compactions -v true
```

```
success
```

```shell
tikv-ctl --host ip:port modify-tikv-config -n raftstore.sync-log -v false
```

```
success
```

圧縮レート制限により圧縮保留中のバイトが蓄積される場合は、 `rate-limiter-auto-tuned`モードを無効にするか、圧縮フローの制限を高く設定します。

```shell
tikv-ctl --host ip:port modify-tikv-config -n rocksdb.rate-limiter-auto-tuned -v false
```

```
success
```

```shell
tikv-ctl --host ip:port modify-tikv-config -n rocksdb.rate-bytes-per-sec -v "1GB"
```

```
success
```

### 複数のレプリカの障害からサービスを回復するようにリージョンを強制する (非推奨) {#force-regions-to-recover-services-from-failure-of-multiple-replicas-deprecated}

> **警告：**
>
> この機能を使用することはお勧めしません。代わりに、ワンストップの自動回復機能を提供する Online Unsafe Recovery in `pd-ctl`を使用できます。サービスの停止などの余分な操作は必要ありません。詳細な紹介については、 [オンラインの安全でない回復](/online-unsafe-recovery.md)を参照してください。

`unsafe-recover remove-fail-stores`コマンドを使用して、失敗したマシンをリージョンのピア リストから削除できます。このコマンドを実行する前に、対象の TiKV ストアのサービスを停止してファイル ロックを解除する必要があります。

`-s`オプションは、コンマで区切られた複数の`store_id`受け入れ、 `-r`フラグを使用して関連するリージョンを指定します。特定のストアのすべてのリージョンでこの操作を実行する必要がある場合は、単純に`--all-regions`を指定できます。

> **警告：**
>
> -   操作を誤ると、クラスタの復旧が困難になる場合があります。潜在的なリスクを認識し、本番環境でこの機能を使用しないようにしてください。
> -   `--all-regions`オプションを使用する場合、クラスターに接続されている残りのすべてのストアでこのコマンドを実行する必要があります。損傷したストアを回復する前に、これらの健全なストアがサービスの提供を停止することを確認する必要があります。そうしないと、リージョンレプリカの一貫性のないピア リストが原因で、 `split-region`または`remove-peer`を実行したときにエラーが発生します。これにより、他のメタデータ間の不一致がさらに発生し、最終的にリージョンが使用できなくなります。
> -   `remove-fail-stores`を実行すると、削除されたノードを再起動したり、これらのノードをクラスターに追加したりすることはできません。そうしないと、メタデータに一貫性がなくなり、最終的にリージョンが使用できなくなります。

```shell
tikv-ctl --data-dir /path/to/tikv unsafe-recover remove-fail-stores -s 3 -r 1001,1002
```

```
success!
```

```shell
tikv-ctl --data-dir /path/to/tikv unsafe-recover remove-fail-stores -s 4,5 --all-regions
```

次に、TiKV を再起動した後、リージョンは残りの正常なレプリカでサービスを提供し続けることができます。このコマンドは、複数の TiKV ストアが破損または削除された場合によく使用されます。

> **ノート：**
>
> -   指定されたリージョンのピアが配置されているすべてのストアに対して、このコマンドを実行する必要があります。
> -   このコマンドは、ローカル モードのみをサポートします。正常に実行されると`success!`出力。

### MVCC データ破損からの回復 {#recover-from-mvcc-data-corruption}

MVCC のデータ破損により TiKV が正常に動作しない場合は、 `recover-mvcc`コマンドを使用してください。 3 つの CF (「デフォルト」、「書き込み」、「ロック」) をクロスチェックして、さまざまな種類の不整合から回復します。

-   `-r`オプションを使用して、関係するリージョンを`region_id`で指定します。
-   PD エンドポイントを指定するには、 `-p`オプションを使用します。

```shell
tikv-ctl --data-dir /path/to/tikv recover-mvcc -r 1001,1002 -p 127.0.0.1:2379
success!
```

> **ノート：**
>
> -   このコマンドは、ローカル モードのみをサポートします。正常に実行されると`success!`出力。
> -   `-p`オプションの引数は、 `http`プレフィックスなしで PD エンドポイントを指定します。 PD エンドポイントを指定すると、指定された`region_id`が検証されているかどうかを照会します。
> -   指定したリージョンのピアが配置されているすべてのストアに対して、このコマンドを実行する必要があります。

### Ldb コマンド {#ldb-command}

`ldb`コマンド ライン ツールは、複数のデータ アクセスおよびデータベース管理コマンドを提供します。以下にいくつかの例を示します。詳細については、 `tikv-ctl ldb`実行時に表示されるヘルプ メッセージを参照するか、RocksDB のドキュメントを確認してください。

データ アクセス シーケンスの例:

既存の RocksDB を HEX でダンプするには:

```shell
tikv-ctl ldb --hex --db=/tmp/db dump
```

既存の RocksDB のマニフェストをダンプするには:

```shell
tikv-ctl ldb --hex manifest_dump --path=/tmp/db/MANIFEST-000001
```

`--column_family=<string>`コマンド ラインを使用して、クエリの対象となるカラムファミリーを指定できます。

`--try_load_options`データベース オプション ファイルをロードしてデータベースを開きます。データベースの実行中は、このオプションを常にオンにしておくことをお勧めします。デフォルトのオプションでデータベースを開くと、LSM ツリーが混乱する可能性があり、自動的に回復することはできません。

### 暗号化メタデータのダンプ {#dump-encryption-metadata}

`encryption-meta`サブコマンドを使用して、暗号化メタデータをダンプします。このサブコマンドは、データ ファイルの暗号化情報と、使用されているデータ暗号化キーのリストの 2 種類のメタデータをダンプできます。

データファイルの暗号化情報をダンプするには、 `encryption-meta dump-file`サブコマンドを使用します。 TiKV 展開用に`data-dir`指定するには、TiKV 構成ファイルを作成する必要があります。

```
# conf.toml
[storage]
data-dir = "/path/to/tikv/data"
```

`--path`オプションを使用して、目的のデータ ファイルへの絶対パスまたは相対パスを指定できます。データ ファイルが暗号化されていない場合、コマンドは空の出力を返す可能性があります。 `--path`が指定されていない場合、すべてのデータ ファイルの暗号化情報が出力されます。

```shell
tikv-ctl --config=./conf.toml encryption-meta dump-file --path=/path/to/tikv/data/db/CURRENT
```

```
/path/to/tikv/data/db/CURRENT: key_id: 9291156302549018620 iv: E3C2FDBF63FC03BFC28F265D7E78283F method: Aes128Ctr
```

データ暗号鍵をダンプするには、 `encryption-meta dump-key`サブコマンドを使用します。 `data-dir`に加えて、構成ファイルで使用されている現在のマスター キーも指定する必要があります。マスターキーの設定方法については、 [保存時の暗号化](/encryption-at-rest.md)を参照してください。また、このコマンドを使用すると、 `security.encryption.previous-master-key`構成は無視され、マスター キーのローテーションはトリガーされません。

```
# conf.toml
[storage]
data-dir = "/path/to/tikv/data"

[security.encryption.master-key]
type = "kms"
key-id = "0987dcba-09fe-87dc-65ba-ab0987654321"
region = "us-west-2"
```

マスター キーが AWS KMS キーの場合、KMS キーにアクセスできる`tikv-ctl`があることに注意してください。 AWS KMS キーへのアクセスは、環境変数、AWS デフォルト設定ファイル、またはIAMロールのいずれか適切なものを介して`tikv-ctl`に付与できます。使用方法については、AWS のドキュメントを参照してください。

`--ids`オプションを使用して、出力するコンマ区切りのデータ暗号化キー ID のリストを指定できます。 `--ids`が指定されていない場合、すべてのデータ暗号化キーが、最新のアクティブなデータ暗号化キーの ID である現在のキー ID と共に出力されます。

コマンドを使用すると、アクションによって機密情報が公開されることを警告するプロンプトが表示されます。 「同意します」と入力して続行します。

```shell
tikv-ctl --config=./conf.toml encryption-meta dump-key
```

```
This action will expose encryption key(s) as plaintext. Do not output the result in file on disk.
Type "I consent" to continue, anything else to exit: I consent
current key id: 9291156302549018620
9291156302549018620: key: 8B6B6B8F83D36BE2467ED55D72AE808B method: Aes128Ctr creation_time: 1592938357
```

```shell
tikv-ctl --config=./conf.toml encryption-meta dump-key --ids=9291156302549018620
```

```
This action will expose encryption key(s) as plaintext. Do not output the result in file on disk.
Type "I consent" to continue, anything else to exit: I consent
9291156302549018620: key: 8B6B6B8F83D36BE2467ED55D72AE808B method: Aes128Ctr creation_time: 1592938357
```

> **ノート：**
>
> このコマンドは、データ暗号化キーをプレーンテキストとして公開します。本番では、出力をファイルにリダイレクトしないでください。後で出力ファイルを削除しても、コンテンツがディスクから完全に消去されない場合があります。

### 破損した SST ファイルに関する情報の出力 {#print-information-related-to-damaged-sst-files}

TiKV の破損した SST ファイルにより、TiKV プロセスがpanicに陥る可能性があります。 TiDB v6.1.0 より前では、これらのファイルが原因で TiKV が即座にpanicに陥ります。 TiDB v6.1.0 以降、SST ファイルが破損してから 1 時間後に TiKV プロセスがpanic。

破損した SST ファイルをクリーンアップするには、 TiKV Controlで`bad-ssts`コマンドを実行して、必要な情報を表示します。以下は、コマンドと出力の例です。

> **ノート：**
>
> このコマンドを実行する前に、実行中の TiKV インスタンスを停止してください。

```shell
tikv-ctl --data-dir </path/to/tikv> bad-ssts --pd <endpoint>
```

```
--------------------------------------------------------
corruption info:
data/tikv-21107/db/000014.sst: Corruption: Bad table magic number: expected 9863518390377041911, found 759105309091689679 in data/tikv-21107/db/000014.sst

sst meta:
14:552997[1 .. 5520]['0101' seq:1, type:1 .. '7A7480000000000000FF0F5F728000000000FF0002160000000000FAFA13AB33020BFFFA' seq:2032, type:1] at level 0 for Column family "default"  (ID 0)
it isn't easy to handle local data, start key:0101

overlap region:
RegionInfo { region: id: 4 end_key: 7480000000000000FF0500000000000000F8 region_epoch { conf_ver: 1 version: 2 } peers { id: 5 store_id: 1 }, leader: Some(id: 5 store_id: 1) }

suggested operations:
tikv-ctl ldb --db=data/tikv-21107/db unsafe_remove_sst_file "data/tikv-21107/db/000014.sst"
tikv-ctl --db=data/tikv-21107/db tombstone -r 4 --pd <endpoint>
--------------------------------------------------------
corruption analysis has completed
```

上記の出力から、破損した SST ファイルの情報が最初に出力され、次にメタ情報が出力されていることがわかります。

-   `sst meta`部分で、 `14` SST ファイル番号を意味します。 `552997`ファイル サイズを意味し、その後に最小および最大のシーケンス番号とその他のメタ情報が続きます。
-   `overlap region`番目の部分は、関係するリージョンの情報を示します。この情報は、PDサーバーを通じて取得されます。
-   `suggested operations`部分は、破損した SST ファイルをクリーンアップするための提案を提供します。ファイルをクリーンアップして TiKV インスタンスを再起動するという提案を受け入れることができます。
