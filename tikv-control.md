---
title: TiKV Control User Guide
summary: TiKV Controlを使用して TiKV クラスターを管理します。
---

# TiKV Controlユーザー ガイド {#tikv-control-user-guide}

TiKV Control ( `tikv-ctl` )は、クラスターの管理に使用されるTiKVのコマンドラインツールです。インストールディレクトリは次のとおりです。

-   クラスターがTiUPを使用してデプロイされている場合、 `tikv-ctl`ディレクトリが`~/.tiup/components/ctl/{VERSION}/`ディレクトリ内にあります。

## TiUPでTiKV Controlを使用する {#use-tikv-control-in-tiup}

> **注記：**
>
> 使用する制御ツールのバージョンは、クラスターのバージョンと一致させることをお勧めします。

`tikv-ctl`は`tiup`コマンドにも`tikv-ctl`されています。4 ツールを呼び出すには、次のコマンドを実行します。

```shell
tiup ctl:v<CLUSTER_VERSION> tikv
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

`tiup ctl:v<CLUSTER_VERSION> tikv`後に対応するパラメータとサブコマンドを追加できます。

## 一般的なオプション {#general-options}

`tikv-ctl` 2 つの動作モードがあります。

-   リモートモード: `--host`オプションを使用して、TiKVのサービスアドレスを引数として受け入れます

    このモードでは、TiKV で SSL が有効になっている場合、関連する証明書ファイルも指定する必要があり`tikv-ctl` 。例:

    ```shell
    tikv-ctl --ca-path ca.pem --cert-path client.pem --key-path client-key.pem --host 127.0.0.1:20160 <subcommands>
    ```

    ただし、 `tikv-ctl`​​ TiKV ではなく PD と通信する場合があります。この場合、 `--host`ではなく`--pd`オプションを使用する必要があります。次に例を示します。

    ```shell
    tikv-ctl --pd 127.0.0.1:2379 compact-cluster
    ```

        store:"127.0.0.1:20160" compact db:KV cf:default range:([], []) success!

-   ローカルモード:

    -   ローカル TiKV データ ディレクトリ パスを指定するには、 `--data-dir`オプションを使用します。
    -   ローカル TiKV 構成ファイル パスを指定するには、 `--config`オプションを使用します。

    このモードでは、実行中の TiKV インスタンスを停止する必要があります。

特に明記されていない限り、すべてのコマンドはリモート モードとローカル モードの両方をサポートします。

さらに、 `tikv-ctl`は`--to-hex`と`--to-escaped` 2 つの簡単なコマンドがあり、これらを使用してキーの形式に簡単な変更を加えることができます。

通常は、キーの`escaped`形式を使用します。例:

```shell
tikv-ctl --to-escaped 0xaaff
\252\377
tikv-ctl --to-hex "\252\377"
AAFF
```

> **注記：**
>
> コマンドラインでキーの`escaped`形式を指定する場合は、二重引用符で囲む必要があります。そうしないと、bash がバックスラッシュを解釈してしまい、間違った結果が返されます。

## サブコマンド、いくつかのオプションとフラグ {#subcommands-some-options-and-flags}

このセクションでは、 `tikv-ctl`サポートするサブコマンドについて詳しく説明します。一部のサブコマンドは多くのオプションをサポートしています。すべての詳細については、 `tikv-ctl --help <subcommand>`を実行してください。

### Raftステートマシンの情報をビュー {#view-information-of-the-raft-state-machine}

特定の瞬間のRaftステート マシンのステータスを表示するには、 `raft`サブコマンドを使用します。ステータス情報には、3 つの構造体 ( **RegionLocalState** 、 **RaftLocalState** 、および**RegionApplyState** ) と、特定のログの対応するエントリの 2 つの部分が含まれます。

上記の情報を取得するには、それぞれサブコマンド`region`と`log`を使用します。 2 つのサブコマンドは、リモート モードとローカル モードを同時にサポートします。

`region`サブコマンドの場合:

-   表示する地域を指定するには、 `-r`オプションを使用します。複数の地域を指定する場合は`,`で区切ります。 `--all-regions`オプションを使用してすべての地域を表示することもできます。 `-r`と`--all-regions`同時に使用できないことに注意してください。
-   印刷する領域の数を制限するには、 `--limit`オプションを使用します (デフォルト: `16` )。
-   特定のキー範囲に含まれるリージョンを照会するには、 `--start`および`--end`オプションを使用します (デフォルト: 範囲制限なし、16 進形式)。

たとえば、ID `1239`リージョンを印刷するには、次のコマンドを使用します。

```shell
tikv-ctl --host 127.0.0.1:20160 raft region -r 1239
```

出力は次のようになります。

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

特定のキー範囲に含まれるリージョンを照会するには、次のコマンドを使用します。

-   キー範囲がリージョン範囲内にある場合は、リージョン情報が出力されます。
-   キー範囲がリージョン範囲と同じ場合、たとえば、指定されたキー範囲がリージョン`1239`と同じ場合、リージョン範囲は左閉じ右開きの間隔であり、リージョン`1009`はリージョン`1239`の`end_key` `start_key`として取得するため、リージョン`1009`情報も出力されます。

```shell
tikv-ctl --host 127.0.0.1:20160 raft region --start 7480000000000000FF4E5F728000000000FF1443770000000000FA --end 7480000000000000FF4E5F728000000000FF21C4420000000000FA
```

出力は次のようになります。

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

### リージョンサイズをビュー {#view-the-region-size}

リージョンのサイズを表示するには、 `size`コマンドを使用します。

```shell
tikv-ctl --data-dir /path/to/tikv size -r 2
```

出力は次のようになります。

    region id: 2
    cf default region size: 799.703 MB
    cf write region size: 41.250 MB
    cf lock region size: 27616

### スキャンして特定の範囲のMVCCを表示する {#scan-to-view-mvcc-of-a-specific-range}

`scan`コマンドの`--from`および`--to`オプションは、2 つのエスケープ形式の生のキーを受け入れ、 `--show-cf`フラグを使用して、表示する必要がある列ファミリを指定します。

```shell
tikv-ctl --data-dir /path/to/tikv scan --from 'zm' --limit 2 --show-cf lock,default,write
```

    key: zmBootstr\377a\377pKey\000\000\377\000\000\373\000\000\000\000\000\377\000\000s\000\000\000\000\000\372
             write cf value: start_ts: 399650102814441473 commit_ts: 399650102814441475 short_value: "20"
    key: zmDB:29\000\000\377\000\374\000\000\000\000\000\000\377\000H\000\000\000\000\000\000\371
             write cf value: start_ts: 399650105239273474 commit_ts: 399650105239273475 short_value: "\000\000\000\000\000\000\000\002"
             write cf value: start_ts: 399650105199951882 commit_ts: 399650105213059076 short_value: "\000\000\000\000\000\000\000\001"

### 指定されたキーのMVCCをビュー {#view-mvcc-of-a-given-key}

`scan`コマンドと同様に、 `mvcc`コマンドを使用して、特定のキーの MVCC を表示できます。

```shell
tikv-ctl --data-dir /path/to/tikv mvcc -k "zmDB:29\000\000\377\000\374\000\000\000\000\000\000\377\000H\000\000\000\000\000\000\371" --show-cf=lock,write,default
```

    key: zmDB:29\000\000\377\000\374\000\000\000\000\000\000\377\000H\000\000\000\000\000\000\371
             write cf value: start_ts: 399650105239273474 commit_ts: 399650105239273475 short_value: "\000\000\000\000\000\000\000\002"
             write cf value: start_ts: 399650105199951882 commit_ts: 399650105213059076 short_value: "\000\000\000\000\000\000\000\001"

このコマンドでは、キーは生のキーのエスケープされた形式でもあります。

### 生のキーをスキャンする {#scan-raw-keys}

`raw-scan`コマンドは RocksDB から直接スキャンします。データ キーをスキャンするには、キーに`'z'`プレフィックスを追加する必要があることに注意してください。

スキャンする範囲を指定するには、 `--from`と`--to`オプションを使用します (デフォルトでは無制限)。 出力するキーの最大数を制限したい場合は、 `--limit`使用します (デフォルトでは 30 個)。 スキャンする cf を指定するには、 `--cf`使用します ( `default` 、 `write` 、または`lock`を指定できます)。

```shell
tikv-ctl --data-dir /var/lib/tikv raw-scan --from 'zt' --limit 2 --cf default
```

    key: "zt\200\000\000\000\000\000\000\377\005_r\200\000\000\000\000\377\000\000\001\000\000\000\000\000\372\372b2,^\033\377\364", value: "\010\002\002\002%\010\004\002\010root\010\006\002\000\010\010\t\002\010\n\t\002\010\014\t\002\010\016\t\002\010\020\t\002\010\022\t\002\010\024\t\002\010\026\t\002\010\030\t\002\010\032\t\002\010\034\t\002\010\036\t\002\010 \t\002\010\"\t\002\010s\t\002\010&\t\002\010(\t\002\010*\t\002\010,\t\002\010.\t\002\0100\t\002\0102\t\002\0104\t\002"
    key: "zt\200\000\000\000\000\000\000\377\025_r\200\000\000\000\000\377\000\000\023\000\000\000\000\000\372\372b2,^\033\377\364", value: "\010\002\002&slow_query_log_file\010\004\002P/usr/local/mysql/data/localhost-slow.log"

    Total scanned keys: 2

### 特定のキー値を印刷する {#print-a-specific-key-value}

キーの値を印刷するには、 `print`コマンドを使用します。

### リージョンに関するいくつかのプロパティを印刷する {#print-some-properties-about-region}

リージョンの状態の詳細を記録するために、TiKV はリージョンの SST ファイルにいくつかの統計情報を書き込みます。これらのプロパティを表示するには、サブコマンド`region-properties`で`tikv-ctl`実行します。

```shell
tikv-ctl --host localhost:20160 region-properties -r 2
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

プロパティを使用して、リージョンが正常かどうかを確認できます。正常でない場合は、これらのプロパティを使用してリージョンを修正できます。たとえば、リージョンを手動で`middle_key_approximate_size`分割します。

### 各TiKVのデータを手動で圧縮する {#compact-data-of-each-tikv-manually}

`compact`コマンドを使用して、各 TiKV のデータを手動で圧縮します。

-   `--from`および`--to`オプションを使用して、エスケープされた生のキーの形式で圧縮範囲を指定します。設定されていない場合は、範囲全体が圧縮されます。

-   特定の領域の範囲を圧縮するには、 `--region`オプションを使用します。設定されている場合、 `--from`と`--to`は無視されます。

-   カラムファミリー名を指定するには、 `-c`オプションを使用します。デフォルト値は`default`です。オプションの値は`default` 、 `lock` 、および`write`です。

-   `-d`オプションを使用して、圧縮を実行する RocksDB を指定します。デフォルト値は`kv`です。オプションの値は`kv`と`raft`です。

-   `--threads`オプションを使用すると、TiKV 圧縮の同時実行性を指​​定できます。デフォルト値は`8`です。通常、同時実行性が高いほど圧縮速度が速くなりますが、サービスに影響する可能性があります。シナリオに基づいて適切な同時実行数を選択する必要があります。

-   `--bottommost`オプションを使用すると、TiKV が圧縮を実行するときに最下位のファイルを含めるか除外するかを指定できます。値のオプションは`default` 、 `skip` 、 `force`です。デフォルト値は`default`です。
    -   `default` 、圧縮フィルター機能が有効な場合にのみ最下位のファイルが含まれることを意味します。
    -   `skip` 、TiKV が圧縮を実行するときに最下位のファイルが除外されることを意味します。
    -   `force` 、TiKV が圧縮を実行するときに最下位のファイルが常に含まれることを意味します。

-   ローカル モードでデータを圧縮するには、次のコマンドを使用します。

    ```shell
    tikv-ctl --data-dir /path/to/tikv compact -d kv
    ```

-   リモート モードでデータを圧縮するには、次のコマンドを使用します。

    ```shell
    tikv-ctl --host ip:port compact -d kv
    ```

### TiKVクラスター全体のデータを手動で圧縮する {#compact-data-of-the-whole-tikv-cluster-manually}

`compact-cluster`コマンドを使用して、TiKV クラスター全体のデータを手動で圧縮します。このコマンドのフラグは、 `compact`コマンドと同じ意味と使用法を持ちます。唯一の違いは次のとおりです。

-   `compact-cluster`コマンドでは、 `--pd`を使用して PD のアドレスを指定します。これにより、 `tikv-ctl`クラスター内のすべての TiKV ノードをコンパクト ターゲットとして見つけることができます。
-   `compact`コマンドの場合、 `--data-dir`または`--host`を使用して、単一の TiKV をコンパクト ターゲットとして指定します。

### リージョンを墓石に設定する {#set-a-region-to-tombstone}

`tombstone`コマンドは通常、sync-log が有効になっていない状況で使用され、 Raftステート マシンに書き込まれたデータの一部が電源オフによって失われます。

TiKV インスタンスでは、このコマンドを使用して、一部のリージョンのステータスをトゥームストーンに設定できます。その後、インスタンスを再起動すると、それらのリージョンはスキップされ、それらのリージョンのRaftステート マシンの破損による再起動の失敗を回避します。それらのリージョンには、 Raftメカニズムを介して読み取りと書き込みを続行できるように、他の TiKV インスタンスに十分な正常なレプリカが必要です。

一般的なケースでは、 `remove-peer`コマンドを使用してこのリージョンの対応するピアを削除できます。

```shell
pd-ctl operator add remove-peer <region_id> <store_id>
```

次に、 `tikv-ctl`ツールを使用して、対応する TiKV インスタンスのリージョンをトゥームストーンに設定し、起動時にこのリージョンのヘルスチェックをスキップします。

```shell
tikv-ctl --data-dir /path/to/tikv tombstone -p 127.0.0.1:2379 -r <region_id>
```

    success!

ただし、場合によっては、このリージョンのこのピアを PD から簡単に削除できないため、 `tikv-ctl`の`--force`のオプションを指定して、ピアを強制的にトゥームストーンに設定できます。

```shell
tikv-ctl --data-dir /path/to/tikv tombstone -p 127.0.0.1:2379 -r <region_id>,<region_id> --force
```

    success!

> **注記：**
>
> -   `tombstone`コマンドはローカル モードのみをサポートします。
> -   `-p`オプションの引数は、 `http`プレフィックスなしで PD エンドポイントを指定します。PD エンドポイントを指定するのは、PD が Tombstone に安全に切り替えることができるかどうかを照会するためです。

### TiKVに<code>consistency-check</code>リクエストを送信する {#send-a-code-consistency-check-code-request-to-tikv}

`consistency-check`コマンドを使用して、特定のリージョンの対応するRaft内のレプリカ間の整合性チェックを実行します。チェックが失敗すると、TiKV 自体がパニックになります。3 `--host`指定された TiKV インスタンスがリージョンリーダーでない場合は、エラーが報告されます。

```shell
tikv-ctl --host 127.0.0.1:20160 consistency-check -r 2
success!
tikv-ctl --host 127.0.0.1:20161 consistency-check -r 2
DebugClient::check_region_consistency: RpcFailure(RpcStatus { status: Unknown, details: Some("StringError(\"Leader is on store 1\")") })
```

> **注記：**
>
> -   `consistency-check`コマンドは TiDB のガベージコレクションと互換性がなく、誤ってエラーを報告する可能性があるため、使用はお勧めし**ません**。
> -   このコマンドはリモート モードのみをサポートします。
> -   このコマンドが`success!`を返した場合でも、TiKV がパニックを起こすかどうかを確認する必要があります。これは、このコマンドがリーダーに対して一貫性チェックを要求する提案に過ぎず、チェックプロセス全体が成功したかどうかをクライアントから知ることができないためです。

### スナップショットのメタをダンプする {#dump-snapshot-meta}

このサブコマンドは、指定されたパスのスナップショット メタ ファイルを解析し、結果を印刷するために使用されます。

### Raftステートマシンが破損した領域を印刷する {#print-the-regions-where-the-raft-state-machine-corrupts}

TiKV の起動中に領域をチェックしないようにするには、 `tombstone`コマンドを使用して、 Raftステート マシンが Tombstone にエラーを報告する領域を設定できます。このコマンドを実行する前に、 `bad-regions`コマンドを使用してエラーのある領域を見つけ、複数のツールを組み合わせて自動処理できるようにします。

```shell
tikv-ctl --data-dir /path/to/tikv bad-regions
```

    all regions are healthy

コマンドが正常に実行されると、上記の情報が出力。コマンドが失敗すると、不良領域のリストが出力。現在、検出できるエラーには、 `last index` 、 `commit index` 、 `apply index`の不一致や、 Raftログの損失などがあります。スナップショット ファイルの破損など、その他の条件については、さらにサポートが必要です。

### リージョンのプロパティをビュー {#view-region-properties}

-   `/path/to/tikv`にデプロイされている TiKV インスタンスのリージョン2 のプロパティをローカルで表示するには:

    ```shell
    tikv-ctl --data-dir /path/to/tikv/data region-properties -r 2
    ```

-   `127.0.0.1:20160`で実行されている TiKV インスタンスのリージョン2 のプロパティをオンラインで表示するには:

    ```shell
    tikv-ctl --host 127.0.0.1:20160 region-properties -r 2
    ```

### TiKV設定を動的に変更する {#modify-the-tikv-configuration-dynamically}

`modify-tikv-config`コマンドを使用して、構成引数を動的に変更できます。現在、動的に変更できる TiKV 構成項目と詳細な変更は、SQL 文を使用した構成の変更と一致しています。詳細については、 [TiKV 構成を動的に変更する](/dynamic-config.md#modify-tikv-configuration-dynamically)を参照してください。

-   `-n`構成項目の完全な名前を指定するために使用されます。動的に変更できる構成項目のリストについては、 [TiKV 構成を動的に変更する](/dynamic-config.md#modify-tikv-configuration-dynamically)を参照してください。
-   `-v`構成値を指定するために使用されます。

`shared block cache`のサイズを設定します:

```shell
tikv-ctl --host ip:port modify-tikv-config -n storage.block-cache.capacity -v 10GB
```

    success

`shared block cache`が無効の場合は、 `write` CF に`block cache size`設定します。

```shell
tikv-ctl --host ip:port modify-tikv-config -n rocksdb.writecf.block-cache-size -v 256MB
```

    success

```shell
tikv-ctl --host ip:port modify-tikv-config -n raftdb.defaultcf.disable-auto-compactions -v true
```

    success

```shell
tikv-ctl --host ip:port modify-tikv-config -n raftstore.sync-log -v false
```

    success

圧縮レート制限によって圧縮保留バイトが蓄積される場合は、 `rate-limiter-auto-tuned`モードを無効にするか、圧縮フローの制限を高く設定します。

```shell
tikv-ctl --host ip:port modify-tikv-config -n rocksdb.rate-limiter-auto-tuned -v false
```

    success

```shell
tikv-ctl --host ip:port modify-tikv-config -n rocksdb.rate-bytes-per-sec -v "1GB"
```

    success

### 複数のレプリカの障害からリージョンにサービスを強制的に回復させる (非推奨) {#force-regions-to-recover-services-from-failure-of-multiple-replicas-deprecated}

> **警告：**
>
> この機能の使用は推奨されません。代わりに、ワンストップ自動リカバリ機能を提供する`pd-ctl`の Online Unsafe Recovery を使用できます。サービスの停止などの追加操作は必要ありません。詳細な説明については、 [オンラインの安全でない回復](/online-unsafe-recovery.md)を参照してください。

`unsafe-recover remove-fail-stores`コマンドを使用すると、リージョンのピア リストから障害が発生したマシンを削除できます。このコマンドを実行する前に、対象の TiKV ストアのサービスを停止してファイル ロックを解除する必要があります。

`-s`オプションは、カンマで区切られた複数の`store_id`受け入れ、 `-r`フラグを使用して関連するリージョンを指定します。特定のストア内のすべてのリージョンに対してこの操作を実行する必要がある場合は、 `--all-regions`指定するだけです。

> **警告：**
>
> -   誤った操作が行われた場合、クラスターの回復が困難になる可能性があります。潜在的なリスクを認識し、本番環境ではこの機能を使用しないでください。
> -   `--all-regions`オプションを使用する場合は、クラスターに接続されている残りのすべてのストアでこのコマンドを実行する必要があります。損傷したストアを回復する前に、これらの正常なストアがサービスの提供を停止していることを確認する必要があります。そうしないと、リージョンレプリカのピア リストが一致していないために、 `split-region`または`remove-peer`を実行したときにエラーが発生します。これにより、他のメタデータ間の不一致がさらに発生し、最終的にリージョンが使用できなくなります。
> -   `remove-fail-stores`実行すると、削除したノードを再起動したり、これらのノードをクラスターに追加したりすることはできません。そうしないと、メタデータに不整合が生じ、最終的にリージョンが使用できなくなります。

```shell
tikv-ctl --data-dir /path/to/tikv unsafe-recover remove-fail-stores -s 3 -r 1001,1002
```

    success!

```shell
tikv-ctl --data-dir /path/to/tikv unsafe-recover remove-fail-stores -s 4,5 --all-regions
```

その後、TiKV を再起動すると、リージョンは残りの正常なレプリカを使用してサービスを引き続き提供できます。このコマンドは、複数の TiKV ストアが破損または削除された場合によく使用されます。

> **注記：**
>
> -   指定されたリージョンのピアが配置されているすべてのストアに対してこのコマンドを実行する必要があります。
> -   このコマンドはローカル モードのみをサポートします。正常に実行されると`success!`出力。

### MVCCデータ破損からの回復 {#recover-from-mvcc-data-corruption}

MVCC データの破損により TiKV が正常に実行できない場合は、 `recover-mvcc`コマンドを使用します。このコマンドは、3 つの CF (「default」、「write」、「lock」) をクロスチェックして、さまざまな種類の不整合から回復します。

-   `-r`オプションを使用して、 `region_id`で関係する領域を指定します。
-   PD エンドポイントを指定するには、 `-p`オプションを使用します。

```shell
tikv-ctl --data-dir /path/to/tikv recover-mvcc -r 1001,1002 -p 127.0.0.1:2379
success!
```

> **注記：**
>
> -   このコマンドはローカル モードのみをサポートします。正常に実行されると`success!`出力。
> -   `-p`オプションの引数は、プレフィックス`http`なしで PD エンドポイントを指定します。PD エンドポイントを指定すると、指定された`region_id`が検証されているかどうかが照会されます。
> -   指定されたリージョンのピアが配置されているすべてのストアに対してこのコマンドを実行する必要があります。

### Ldb コマンド {#ldb-command}

`ldb`コマンドライン ツールは、複数のデータ アクセス コマンドとデータベース管理コマンドを提供します。以下にいくつかの例を示します。詳細については、 `tikv-ctl ldb`実行時に表示されるヘルプ メッセージを参照するか、RocksDB のドキュメントを確認してください。

データ アクセス シーケンスの例:

既存の RocksDB を HEX でダンプするには:

```shell
tikv-ctl ldb --hex --db=/tmp/db dump
```

既存の RocksDB のマニフェストをダンプするには:

```shell
tikv-ctl ldb --hex manifest_dump --path=/tmp/db/MANIFEST-000001
```

`--column_family=<string>`コマンドラインを使用して、クエリの対象となるカラムファミリーを指定できます。

`--try_load_options`データベースを開くためにデータベース オプション ファイルをロードします。データベースの実行中は常にこのオプションをオンにしておくことをお勧めします。デフォルト オプションでデータベースを開くと、LSM ツリーが乱れる可能性があり、自動的に回復することはできません。

### 暗号化メタデータをダンプする {#dump-encryption-metadata}

暗号化メタデータをダンプするには、サブコマンド`encryption-meta`を使用します。サブコマンドは、データ ファイルの暗号化情報と、使用されるデータ暗号化キーのリストの 2 種類のメタデータをダンプできます。

データ ファイルの暗号化情報をダンプするには、 `encryption-meta dump-file`サブコマンドを使用します。TiKV デプロイメントに`data-dir`を指定するには、TiKV 構成ファイルを作成する必要があります。

    # conf.toml
    [storage]
    data-dir = "/path/to/tikv/data"

`--path`オプションを使用すると、対象のデータ ファイルへの絶対パスまたは相対パスを指定できます。データ ファイルが暗号化されていない場合、コマンドは空の出力を返すことがあります`--path`を指定しないと、すべてのデータ ファイルの暗号化情報が出力されます。

```shell
tikv-ctl --config=./conf.toml encryption-meta dump-file --path=/path/to/tikv/data/db/CURRENT
```

    /path/to/tikv/data/db/CURRENT: key_id: 9291156302549018620 iv: E3C2FDBF63FC03BFC28F265D7E78283F method: Aes128Ctr

データ暗号化キーをダンプするには、 `encryption-meta dump-key`サブコマンドを使用します。 `data-dir`に加えて、設定ファイルで現在使用されているマスター キーも指定する必要があります。マスター キーの設定方法については、 [保存時の暗号化](/encryption-at-rest.md)を参照してください。また、このコマンドでは、 `security.encryption.previous-master-key`設定は無視され、マスター キーのローテーションはトリガーされません。

    # conf.toml
    [storage]
    data-dir = "/path/to/tikv/data"

    [security.encryption.master-key]
    type = "kms"
    key-id = "0987dcba-09fe-87dc-65ba-ab0987654321"
    region = "us-west-2"

マスターキーが AWS KMS キーの場合、 `tikv-ctl` KMS キーにアクセスできる必要があります。AWS KMS キーへのアクセスは、環境変数、AWS デフォルト設定ファイル、またはIAMロールのいずれか適切なものを介して`tikv-ctl`に付与できます。使用方法については、AWS ドキュメントを参照してください。

`--ids`オプションを使用すると、印刷するデータ暗号化キー ID のリストをコンマで区切って指定できます。3 `--ids`指定しない場合は、最新のアクティブなデータ暗号化キーの ID である現在のキー ID とともに、すべてのデータ暗号化キーが印刷されます。

コマンドを使用すると、アクションによって機密情報が公開されるという警告が表示されます。続行するには、「同意します」と入力してください。

```shell
tikv-ctl --config=./conf.toml encryption-meta dump-key
```

    This action will expose encryption key(s) as plaintext. Do not output the result in file on disk.
    Type "I consent" to continue, anything else to exit: I consent
    current key id: 9291156302549018620
    9291156302549018620: key: 8B6B6B8F83D36BE2467ED55D72AE808B method: Aes128Ctr creation_time: 1592938357

```shell
tikv-ctl --config=./conf.toml encryption-meta dump-key --ids=9291156302549018620
```

    This action will expose encryption key(s) as plaintext. Do not output the result in file on disk.
    Type "I consent" to continue, anything else to exit: I consent
    9291156302549018620: key: 8B6B6B8F83D36BE2467ED55D72AE808B method: Aes128Ctr creation_time: 1592938357

> **注記：**
>
> このコマンドは、データ暗号化キーをプレーンテキストとして公開します。本番では、出力をファイルにリダイレクトしないでください。後で出力ファイルを削除しても、ディスクからコンテンツが完全に消去されない可能性があります。

### 破損したSSTファイルに関連する情報を印刷する {#print-information-related-to-damaged-sst-files}

TiKV 内の破損した SST ファイルにより、TiKV プロセスがpanicになる可能性があります。TiDB v6.1.0 より前では、これらのファイルにより TiKV は直ちにpanicになりました。TiDB v6.1.0 以降では、SST ファイルが破損してから 1 時間後に TiKV プロセスがpanic。

破損した SST ファイルをクリーンアップするには、 TiKV Controlで`bad-ssts`コマンドを実行して必要な情報を表示します。以下はコマンドと出力の例です。

> **注記：**
>
> このコマンドを実行する前に、実行中の TiKV インスタンスを停止してください。

```shell
tikv-ctl --data-dir </path/to/tikv> bad-ssts --pd <endpoint>
```

    --------------------------------------------------------
    corruption info:
    data/tikv-21107/db/000014.sst: Corruption: Bad table magic number: expected 9863518390377041911, found 759105309091689679 in data/tikv-21107/db/000014.sst

    sst meta:
    14:552997[1 .. 5520]['0101' seq:1, type:1 .. '7A7480000000000000FF0F5F728000000000FF0002160000000000FAFA13AB33020BFFFA' seq:2032, type:1] at level 0 for Column family "default"  (ID 0)
    it isn't easy to handle local data, start key:0101

    overlap region:
    RegionInfo { region: id: 4 end_key: 7480000000000000FF0500000000000000F8 region_epoch { conf_ver: 1 version: 2 } peers { id: 5 store_id: 1 }, leader: Some(id: 5 store_id: 1) }

    refer operations:
    tikv-ctl ldb --db=/path/to/tikv/db unsafe_remove_sst_file 000014
    tikv-ctl --data-dir=/path/to/tikv tombstone -r 4 --pd <endpoint>
    --------------------------------------------------------
    corruption analysis has completed

上記の出力から、破損した SST ファイルの情報が最初に印刷され、次にメタ情報が印刷されていることがわかります。

-   `sst meta`部分では、 `14` SST ファイル番号、 `552997`ファイル サイズを意味し、その後に最小および最大のシーケンス番号とその他のメタ情報が続きます。
-   `overlap region`部分は、関連するリージョンの情報を示しています。この情報は PDサーバーから取得されます。
-   パート`suggested operations`では、破損した SST ファイルをクリーンアップするための提案が提供されます。提案に従ってファイルをクリーンアップし、TiKV インスタンスを再起動できます。

### リージョンの<code>RegionReadProgress</code>の状態を取得する {#get-the-state-of-a-region-s-code-regionreadprogress-code}

v6.5.4 および v7.3.0 以降、TiKV では、リゾルバの最新の詳細を取得するための`get-region-read-progress`サブコマンドと`RegionReadProgress`が導入されています。リージョンID と TiKV を指定する必要があります。これらは、Grafana ( `Min Resolved TS Region`と`Min Safe TS Region` ) または`DataIsNotReady`ログから取得できます。

-   `--log` (オプション): 指定すると、TiKV は、リージョンのリゾルバ内のロックのうち最小の`start_ts`をこの TiKV のレベル`INFO`でログに記録します。このオプションは、resolved-tsをブロックする可能性のあるロックを事前に識別するのに役立ちます。

-   `--min-start-ts` (オプション): 指定すると、TiKV はログでこの値より`start_ts`小さいロックをフィルターします。これを使用して、ログに記録するトランザクションを指定できます。デフォルトは`0`で、フィルターなしを意味します。

次に例を示します。

    ./tikv-ctl --host 127.0.0.1:20160 get-region-read-progress -r 14 --log --min-start-ts 0

出力は次のようになります。

    Region read progress:
        exist: true,
        safe_ts: 0,
        applied_index: 92,
        pending front item (oldest) ts: 0,
        pending front item (oldest) applied index: 0,
        pending back item (latest) ts: 0,
        pending back item (latest) applied index: 0,
        paused: false,
    Resolver:
        exist: true,
        resolved_ts: 0,
        tracked index: 92,
        number of locks: 0,
        number of transactions: 0,
        stopped: false,

このサブコマンドは、 ステイル読み取りおよび safe-ts に関連する問題の診断に役立ちます。詳細については、 [TiKV のステイル読み取りと safe-ts を理解する](/troubleshoot-stale-read.md)を参照してください。
