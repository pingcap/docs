---
title: TiKV Control User Guide
summary: Use TiKV Control to manage a TiKV cluster.
---

# TiKV Controlユーザーガイド {#tikv-control-user-guide}

TiKV Control ( `tikv-ctl` ) は、クラスターの管理に使用される TiKV のコマンド ライン ツールです。インストールディレクトリは以下のとおりです。

-   TiUPを使用してクラスターがデプロイされている場合、 `~/.tiup/components/ctl/{VERSION}/`ディレクトリー内に`tikv-ctl`ディレクトリーが存在します。

## TiUPでTiKV Controlを使用する {#use-tikv-control-in-tiup}

> **注記：**
>
> 使用する制御ツールのバージョンがクラスターのバージョンと一致していることをお勧めします。

`tikv-ctl`は`tiup`コマンドにも組み込まれます。次のコマンドを実行して`tikv-ctl`ツールを呼び出します。

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

`tiup ctl:v<CLUSTER_VERSION> tikv`の後に、対応するパラメータとサブコマンドを追加できます。

## 一般的なオプション {#general-options}

`tikv-ctl` 2 つの動作モードを提供します。

-   リモート モード: `--host`オプションを使用して、TiKV のサービス アドレスを引数として受け入れます。

    このモードでは、TiKV で SSL が有効になっている場合、関連する証明書ファイル`tikv-ctl`指定する必要があります。例えば：

    ```shell
    tikv-ctl --ca-path ca.pem --cert-path client.pem --key-path client-key.pem --host 127.0.0.1:20160 <subcommands>
    ```

    ただし、TiKV ではなく`tikv-ctl`と通信する場合もあります。この場合、 `--host`の代わりに`--pd`オプションを使用する必要があります。以下に例を示します。

    ```shell
    tikv-ctl --pd 127.0.0.1:2379 compact-cluster
    ```

        store:"127.0.0.1:20160" compact db:KV cf:default range:([], []) success!

-   ローカルモード:

    -   `--data-dir`オプションを使用して、ローカル TiKV データ ディレクトリ パスを指定します。
    -   `--config`オプションを使用して、ローカル TiKV 構成ファイルのパスを指定します。

    このモードでは、実行中の TiKV インスタンスを停止する必要があります。

特に明記されていない限り、すべてのコマンドはリモート モードとローカル モードの両方をサポートします。

さらに、 `tikv-ctl` 2 つの単純なコマンド`--to-hex`および`--to-escaped`があり、これらはキーの形式に単純な変更を加えるために使用されます。

通常、キーの`escaped`形式を使用します。例えば：

```shell
tikv-ctl --to-escaped 0xaaff
\252\377
tikv-ctl --to-hex "\252\377"
AAFF
```

> **注記：**
>
> コマンド ラインでキーの`escaped`形式を指定する場合は、二重引用符で囲む必要があります。そうしないと、bash がバックスラッシュを使用してしまい、間違った結果が返されます。

## サブコマンド、いくつかのオプション、フラグ {#subcommands-some-options-and-flags}

このセクションでは、 `tikv-ctl`がサポートするサブコマンドについて詳しく説明します。一部のサブコマンドは多くのオプションをサポートしています。詳細については、 `tikv-ctl --help <subcommand>`を実行してください。

### Raftステート マシンの情報をビュー {#view-information-of-the-raft-state-machine}

`raft`サブコマンドを使用して、特定の時点でのRaftステート マシンのステータスを表示します。ステータス情報には 2 つの部分が含まれます。3 つの構造体 ( **RegionalLocalState** 、 **RaftLocalState** 、および**RegionApplyState** ) と、ログの特定の部分の対応するエントリです。

上記の情報を取得するには、それぞれ`region`サブコマンドと`log`サブコマンドを使用します。 2 つのサブコマンドは両方とも、リモート モードとローカル モードを同時にサポートします。

`region`サブコマンドの場合:

-   表示するリージョンを指定するには、 `-r`オプションを使用します。複数のリージョンは`,`で区切られます。 `--all-regions`オプションを使用してすべてのリージョンを表示することもできます。 `-r`と`--all-regions`同時に使用できませんのでご注意ください。
-   印刷する領域の数を制限するには、 `--limit`オプションを使用します (デフォルト: `16` )。
-   特定のキー範囲にどのリージョンが含まれるかをクエリするには、 `--start`および`--end`オプションを使用します (デフォルト: 範囲制限なし、16 進形式)。

たとえば、ID `1239`のリージョンを印刷するには、次のコマンドを使用します。

```shell
tikv-ctl --host 127.0.0.1:20160 raft region -r 1239
```

出力は次のとおりです。

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

特定のキー範囲にどのリージョンが含まれているかをクエリするには、次のコマンドを使用します。

-   キー範囲がリージョン範囲にある場合は、リージョン情報が出力されます。
-   キー範囲がリージョン範囲と同じ場合、たとえば、指定されたキー範囲がリージョン`1239`と同じ場合、リージョン範囲は左が閉じて右が開いた間隔であり、リージョン`1009`次の`end_key`をとります。リージョン`1239`とリージョン`start_key` 、リージョン`1009`の情報も出力されます。

```shell
tikv-ctl --host 127.0.0.1:20160 raft region --start 7480000000000000FF4E5F728000000000FF1443770000000000FA --end 7480000000000000FF4E5F728000000000FF21C4420000000000FA
```

出力は次のとおりです。

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

`size`コマンドを使用してリージョンサイズを表示します。

```shell
tikv-ctl --data-dir /path/to/tikv size -r 2
```

出力は次のとおりです。

    region id: 2
    cf default region size: 799.703 MB
    cf write region size: 41.250 MB
    cf lock region size: 27616

### スキャンして特定範囲の MVCC を表示 {#scan-to-view-mvcc-of-a-specific-range}

`scan`コマンドの`--from`および`--to`オプションは、生キーの 2 つのエスケープ形式を受け入れ、 `--show-cf`フラグを使用して、表示する必要がある列ファミリーを指定します。

```shell
tikv-ctl --data-dir /path/to/tikv scan --from 'zm' --limit 2 --show-cf lock,default,write
```

    key: zmBootstr\377a\377pKey\000\000\377\000\000\373\000\000\000\000\000\377\000\000s\000\000\000\000\000\372
             write cf value: start_ts: 399650102814441473 commit_ts: 399650102814441475 short_value: "20"
    key: zmDB:29\000\000\377\000\374\000\000\000\000\000\000\377\000H\000\000\000\000\000\000\371
             write cf value: start_ts: 399650105239273474 commit_ts: 399650105239273475 short_value: "\000\000\000\000\000\000\000\002"
             write cf value: start_ts: 399650105199951882 commit_ts: 399650105213059076 short_value: "\000\000\000\000\000\000\000\001"

### 指定されたキーの MVCC をビュー {#view-mvcc-of-a-given-key}

`scan`コマンドと同様に、 `mvcc`コマンドを使用して、特定のキーの MVCC を表示できます。

```shell
tikv-ctl --data-dir /path/to/tikv mvcc -k "zmDB:29\000\000\377\000\374\000\000\000\000\000\000\377\000H\000\000\000\000\000\000\371" --show-cf=lock,write,default
```

    key: zmDB:29\000\000\377\000\374\000\000\000\000\000\000\377\000H\000\000\000\000\000\000\371
             write cf value: start_ts: 399650105239273474 commit_ts: 399650105239273475 short_value: "\000\000\000\000\000\000\000\002"
             write cf value: start_ts: 399650105199951882 commit_ts: 399650105213059076 short_value: "\000\000\000\000\000\000\000\001"

このコマンドでは、キーは生キーのエスケープ形式でもあります。

### 生の鍵をスキャンする {#scan-raw-keys}

`raw-scan`コマンドは RocksDB から直接スキャンします。データキーをスキャンするには、キーに`'z'`接頭辞を追加する必要があることに注意してください。

`--from`および`--to`オプションを使用して、スキャンする範囲を指定します (デフォルトでは無制限)。出力するキーの最大数を制限するには、 `--limit`を使用します (デフォルトでは 30)。 `--cf`を使用して、どの CF をスキャンするかを指定します ( `default` 、 `write`または`lock`を使用できます)。

```shell
tikv-ctl --data-dir /var/lib/tikv raw-scan --from 'zt' --limit 2 --cf default
```

    key: "zt\200\000\000\000\000\000\000\377\005_r\200\000\000\000\000\377\000\000\001\000\000\000\000\000\372\372b2,^\033\377\364", value: "\010\002\002\002%\010\004\002\010root\010\006\002\000\010\010\t\002\010\n\t\002\010\014\t\002\010\016\t\002\010\020\t\002\010\022\t\002\010\024\t\002\010\026\t\002\010\030\t\002\010\032\t\002\010\034\t\002\010\036\t\002\010 \t\002\010\"\t\002\010s\t\002\010&\t\002\010(\t\002\010*\t\002\010,\t\002\010.\t\002\0100\t\002\0102\t\002\0104\t\002"
    key: "zt\200\000\000\000\000\000\000\377\025_r\200\000\000\000\000\377\000\000\023\000\000\000\000\000\372\372b2,^\033\377\364", value: "\010\002\002&slow_query_log_file\010\004\002P/usr/local/mysql/data/localhost-slow.log"

    Total scanned keys: 2

### 特定のキー値を出力する {#print-a-specific-key-value}

キーの値を出力するには、 `print`コマンドを使用します。

### リージョンに関するいくつかのプロパティを出力します {#print-some-properties-about-region}

リージョンの状態の詳細を記録するために、TiKV はリージョンの SST ファイルにいくつかの統計を書き込みます。これらのプロパティを表示するには、 `tikv-ctl`と`region-properties`サブコマンドを実行します。

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

プロパティを使用して、リージョンが正常かどうかを確認できます。そうでない場合は、それらを使用してリージョンを修正できます。たとえば、 リージョン を手動で`middle_key_approximate_size`で分割します。

### 各 TiKV のデータを手動で圧縮します {#compact-data-of-each-tikv-manually}

`compact`コマンドを使用して、各 TiKV のデータを手動で圧縮します。

-   `--from`および`--to`オプションを使用して、エスケープされた生キーの形式で圧縮範囲を指定します。設定しない場合、範囲全体が圧縮されます。

-   特定の領域の範囲を圧縮するには、 `--region`オプションを使用します。設定されている場合、 `--from`と`--to`は無視されます。

-   `-c`オプションを使用してカラムファミリー名を指定します。デフォルト値は`default`です。オプションの値は`default` 、 `lock` 、および`write`です。

-   `-d`オプションを使用して、圧縮を実行する RocksDB を指定します。デフォルト値は`kv`です。オプションの値は`kv`と`raft`です。

-   `--threads`オプションを使用すると、TiKV 圧縮の同時実行性を指​​定できます。デフォルト値は`8`です。一般に、同時実行性が高くなると圧縮速度も速くなりますが、サービスに影響を与える可能性があります。シナリオに基づいて適切な同時実行数を選択する必要があります。

-   TiKV が圧縮を実行するときに最下位のファイルを含めるか除外するには、 `--bottommost`オプションを使用します。値のオプションは`default` 、 `skip` 、および`force`です。デフォルト値は`default`です。
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

### TiKV クラスター全体のデータを手動で圧縮する {#compact-data-of-the-whole-tikv-cluster-manually}

`compact-cluster`コマンドを使用して、TiKV クラスター全体のデータを手動で圧縮します。このコマンドのフラグの意味と使用法は、 `compact`コマンドのフラグと同じです。唯一の違いは次のとおりです。

-   `compact-cluster`コマンドの場合、 `--pd`使用して PD のアドレスを指定します。これにより、 `tikv-ctl`クラスター内のすべての TiKV ノードをコンパクト ターゲットとして見つけることができます。
-   `compact`コマンドの場合、 `--data-dir`または`--host`を使用して単一の TiKV をコンパクト ターゲットとして指定します。

### リージョンをトゥームストーンに設定する {#set-a-region-to-tombstone}

`tombstone`コマンドは通常、同期ログが有効になっておらず、 Raftステート マシンに書き込まれた一部のデータが電源切断により失われる状況で使用されます。

TiKV インスタンスでは、このコマンドを使用して、一部のリージョンのステータスを廃棄に設定できます。その後、インスタンスを再起動すると、それらのリージョンのRaftステート マシンの損傷によって引き起こされる再起動の失敗を避けるために、それらのリージョンはスキップされます。これらのリージョンでは、 Raftメカニズムを通じて読み取りと書き込みを続行できるように、他の TiKV インスタンスに十分な健全なレプリカが必要です。

通常、次の`remove-peer`コマンドを使用して、このリージョンの対応するピアを削除できます。

```shell
pd-ctl operator add remove-peer <region_id> <store_id>
```

次に、 `tikv-ctl`ツールを使用して、対応する TiKV インスタンスのトゥームストーンにリージョンを設定し、起動時にこのリージョンのヘルス チェックをスキップします。

```shell
tikv-ctl --data-dir /path/to/tikv tombstone -p 127.0.0.1:2379 -r <region_id>
```

    success!

ただし、場合によっては、このリージョンのこのピアを PD から簡単に削除できないため、 `tikv-ctl`の`--force`オプションを指定して、ピアを強制的に廃棄に設定できます。

```shell
tikv-ctl --data-dir /path/to/tikv tombstone -p 127.0.0.1:2379 -r <region_id>,<region_id> --force
```

    success!

> **注記：**
>
> -   `tombstone`コマンドはローカル モードのみをサポートします。
> -   `-p`オプションの引数は、 `http`プレフィックスを付けずに PD エンドポイントを指定します。 PD エンドポイントを指定すると、PD が安全に Tombstone に切り替えることができるかどうかがクエリされます。

### <code>consistency-check</code>リクエストを TiKV に送信する {#send-a-code-consistency-check-code-request-to-tikv}

`consistency-check`コマンドを使用して、特定のリージョンの対応するRaft内のレプリカ間の整合性チェックを実行します。チェックが失敗すると、TiKV 自体がパニックになります。 `--host`で指定された TiKV インスタンスがリージョンリーダーではない場合、エラーが報告されます。

```shell
tikv-ctl --host 127.0.0.1:20160 consistency-check -r 2
success!
tikv-ctl --host 127.0.0.1:20161 consistency-check -r 2
DebugClient::check_region_consistency: RpcFailure(RpcStatus { status: Unknown, details: Some("StringError(\"Leader is on store 1\")") })
```

> **注記：**
>
> -   `consistency-check`コマンドの使用は推奨され**ません**。このコマンドは TiDB のガベージコレクションと互換性がなく、誤ってエラーを報告する可能性があるためです。
> -   このコマンドはリモート モードのみをサポートします。
> -   このコマンドが`success!`を返した場合でも、TiKV がパニックするかどうかを確認する必要があります。これは、このコマンドはリーダーに対する整合性チェックを要求する提案にすぎず、チェック処理全体が成功したかどうかをクライアントからは知ることができないためです。

### スナップショットメタをダンプする {#dump-snapshot-meta}

このサブコマンドは、指定されたパスでスナップショット メタ ファイルを解析し、結果を出力するために使用されます。

### Raftステート マシンが破損している領域を出力します。 {#print-the-regions-where-the-raft-state-machine-corrupts}

TiKV の開始中にリージョンをチェックしないようにするには、 `tombstone`コマンドを使用して、 Raftステート マシンが Tombstone にエラーを報告するリージョンを設定します。このコマンドを実行する前に、 `bad-regions`コマンドを使用してエラーのある領域を見つけ、複数のツールを組み合わせて自動処理します。

```shell
tikv-ctl --data-dir /path/to/tikv bad-regions
```

    all regions are healthy

コマンドが正常に実行されると、上記の情報が出力。コマンドが失敗すると、不正なリージョンのリストが出力。現在、検出できるエラーには、 `last index` 、 `commit index` 、 `apply index`の間の不一致、およびRaftログの損失が含まれます。スナップショット ファイルの破損などのその他の状況については、さらなるサポートが必要です。

### リージョンのプロパティをビュー {#view-region-properties}

-   `/path/to/tikv`にデプロイされた TiKV インスタンス上のリージョン2 のプロパティをローカルで表示するには:

    ```shell
    tikv-ctl --data-dir /path/to/tikv/data region-properties -r 2
    ```

-   `127.0.0.1:20160`で実行されている TiKV インスタンス上のリージョン2 のプロパティをオンラインで表示するには、次の手順を実行します。

    ```shell
    tikv-ctl --host 127.0.0.1:20160 region-properties -r 2
    ```

### TiKV 構成を動的に変更する {#modify-the-tikv-configuration-dynamically}

`modify-tikv-config`コマンドを使用すると、構成引数を動的に変更できます。現時点では、動的に変更できる TiKV 構成項目と詳細な変更は、SQL ステートメントを使用した構成変更と一致しています。詳細は[TiKV 構成を動的に変更する](/dynamic-config.md#modify-tikv-configuration-dynamically)を参照してください。

-   `-n`は、構成アイテムの完全名を指定するために使用されます。動的に変更できる構成項目のリストについては、 [TiKV 構成を動的に変更する](/dynamic-config.md#modify-tikv-configuration-dynamically)を参照してください。
-   `-v`は設定値を指定するために使用されます。

サイズを`shared block cache`に設定します。

```shell
tikv-ctl --host ip:port modify-tikv-config -n storage.block-cache.capacity -v 10GB
```

    success

`shared block cache`が無効な場合、 `write` CF に`block cache size`を設定します。

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

圧縮レート制限によって圧縮保留中のバイトが蓄積される場合は、 `rate-limiter-auto-tuned`モードを無効にするか、圧縮フローの制限値を高く設定します。

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
> この機能の使用はお勧めしません。代わりに、ワンストップの自動回復機能を提供する`pd-ctl`の Online Unsafe Recovery を使用できます。サービスを停止するなどの余分な操作は必要ありません。詳細な紹介については、 [オンラインの安全でないリカバリ](/online-unsafe-recovery.md)を参照してください。

`unsafe-recover remove-fail-stores`コマンドを使用して、障害が発生したマシンをリージョンのピア リストから削除できます。このコマンドを実行する前に、ターゲット TiKV ストアのサービスを停止してファイル ロックを解除する必要があります。

`-s`オプションは、カンマで区切られた複数の`store_id`受け入れ、 `-r`フラグを使用して関連するリージョンを指定します。特定のストア内のすべてのリージョンに対してこの操作を実行する必要がある場合は、単に`--all-regions`を指定するだけで済みます。

> **警告：**
>
> -   誤った操作を行った場合、クラスタの復旧が困難になる可能性があります。潜在的なリスクを認識し、本番環境でこの機能を使用しないようにしてください。
> -   `--all-regions`オプションを使用する場合は、クラスターに接続されている残りのすべてのストアでこのコマンドを実行する必要があります。損傷したストアを回復する前に、これらの健全なストアがサービスの提供を停止していることを確認する必要があります。そうしないと、リージョンレプリカ内のピア リストに一貫性がないため、 `split-region`または`remove-peer`を実行するとエラーが発生します。これにより、他のメタデータ間でさらに不整合が発生し、最終的にはリージョンが使用できなくなります。
> -   `remove-fail-stores`を実行すると、削除されたノードを再起動したり、これらのノードをクラスターに追加したりすることはできません。そうしないと、メタデータに一貫性がなくなり、最終的にリージョンが使用できなくなります。

```shell
tikv-ctl --data-dir /path/to/tikv unsafe-recover remove-fail-stores -s 3 -r 1001,1002
```

    success!

```shell
tikv-ctl --data-dir /path/to/tikv unsafe-recover remove-fail-stores -s 4,5 --all-regions
```

その後、TiKV を再起動した後、リージョンは残りの正常なレプリカを使用してサービスを提供し続けることができます。このコマンドは、複数の TiKV ストアが破損または削除された場合によく使用されます。

> **注記：**
>
> -   このコマンドは、指定したリージョンのピアが存在するすべてのストアに対して実行する必要があります。
> -   このコマンドはローカル モードのみをサポートします。正常に実行されると`success!`出力。

### MVCC データ破損から回復する {#recover-from-mvcc-data-corruption}

MVCC データ破損により TiKV が正常に実行できない状況では、 `recover-mvcc`コマンドを使用します。 3 つの CF (「デフォルト」、「書き込み」、「ロック」) をクロスチェックして、さまざまな種類の不整合から回復します。

-   `-r`オプションを使用して、関係するリージョンを`region_id`で指定します。
-   PD エンドポイントを指定するには、 `-p`オプションを使用します。

```shell
tikv-ctl --data-dir /path/to/tikv recover-mvcc -r 1001,1002 -p 127.0.0.1:2379
success!
```

> **注記：**
>
> -   このコマンドはローカル モードのみをサポートします。正常に実行されると`success!`出力。
> -   `-p`オプションの引数は、 `http`プレフィックスを付けずに PD エンドポイントを指定します。 PD エンドポイントの指定は、指定された`region_id`が検証されるかどうかを問い合わせることです。
> -   指定したリージョンのピアが配置されているすべてのストアに対してこのコマンドを実行する必要があります。

### Ldbコマンド {#ldb-command}

`ldb`コマンド ライン ツールは、複数のデータ アクセスおよびデータベース管理コマンドを提供します。いくつかの例を以下に示します。詳細については、 `tikv-ctl ldb`実行時に表示されるヘルプ メッセージを参照するか、RocksDB のドキュメントを確認してください。

データアクセスシーケンスの例:

既存の RocksDB を HEX でダンプするには:

```shell
tikv-ctl ldb --hex --db=/tmp/db dump
```

既存の RocksDB のマニフェストをダンプするには:

```shell
tikv-ctl ldb --hex manifest_dump --path=/tmp/db/MANIFEST-000001
```

`--column_family=<string>`コマンド ラインを使用して、クエリの対象となるカラムファミリーを指定できます。

`--try_load_options`データベース オプション ファイルをロードしてデータベースを開きます。データベースの実行中は、このオプションを常にオンにしておくことが推奨されます。デフォルトのオプションでデータベースを開くと、LSM ツリーが破損する可能性があり、自動的に回復できません。

### 暗号化メタデータをダンプする {#dump-encryption-metadata}

`encryption-meta`サブコマンドを使用して、暗号化メタデータをダンプします。このサブコマンドは、データ ファイルの暗号化情報と使用されるデータ暗号化キーのリストという 2 種類のメタデータをダンプできます。

データ ファイルの暗号化情報をダンプするには、 `encryption-meta dump-file`サブコマンドを使用します。 TiKV 構成ファイルを作成して、TiKV 展開に`data-dir`を指定する必要があります。

    # conf.toml
    [storage]
    data-dir = "/path/to/tikv/data"

`--path`オプションを使用すると、対象のデータ ファイルへの絶対パスまたは相対パスを指定できます。データ ファイルが暗号化されていない場合、コマンドは空の出力を返す可能性があります。 `--path`を指定しない場合、すべてのデータ ファイルの暗号化情報が出力されます。

```shell
tikv-ctl --config=./conf.toml encryption-meta dump-file --path=/path/to/tikv/data/db/CURRENT
```

    /path/to/tikv/data/db/CURRENT: key_id: 9291156302549018620 iv: E3C2FDBF63FC03BFC28F265D7E78283F method: Aes128Ctr

データ暗号化キーをダンプするには、 `encryption-meta dump-key`サブコマンドを使用します。 `data-dir`に加えて、構成ファイルで使用されている現在のマスター キーを指定する必要もあります。マスターキーの設定方法については、 [保存時の暗号化](/encryption-at-rest.md)を参照してください。また、このコマンドを使用すると、 `security.encryption.previous-master-key`設定は無視され、マスター キーのローテーションはトリガーされません。

    # conf.toml
    [storage]
    data-dir = "/path/to/tikv/data"

    [security.encryption.master-key]
    type = "kms"
    key-id = "0987dcba-09fe-87dc-65ba-ab0987654321"
    region = "us-west-2"

マスターキーが AWS KMS キーの場合、 `tikv-ctl` KMS キーにアクセスできる必要があることに注意してください。 AWS KMS キーへのアクセスは、環境変数、AWS のデフォルト設定ファイル、またはIAMロールのいずれか適切なものを介して`tikv-ctl`に付与できます。使用方法については AWS のドキュメントを参照してください。

`--ids`オプションを使用すると、印刷するデータ暗号化キー ID のカンマ区切りリストを指定できます。 `--ids`が指定されていない場合は、すべてのデータ暗号化キーが、最新のアクティブなデータ暗号化キーの ID である現在のキー ID とともに出力されます。

このコマンドを使用すると、この操作により機密情報が公開されることを警告するプロンプトが表示されます。 「同意する」と入力して続行します。

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
> このコマンドは、データ暗号化キーを平文として公開します。本番では、出力をファイルにリダイレクトしないでください。後で出力ファイルを削除しても、ディスクからコンテンツが完全に消去されない場合があります。

### 破損した SST ファイルに関連する情報を出力します。 {#print-information-related-to-damaged-sst-files}

TiKV 内の SST ファイルが破損すると、TiKV プロセスがpanicを引き起こす可能性があります。 TiDB v6.1.0 より前では、これらのファイルにより TiKV が即座にpanicを起こします。 TiDB v6.1.0 以降、TiKV プロセスは、SST ファイルが破損してから 1 時間後にpanic。

破損した SST ファイルをクリーンアップするには、 TiKV Controlで`bad-ssts`コマンドを実行して、必要な情報を表示します。以下はコマンドと出力の例です。

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

    suggested operations:
    tikv-ctl ldb --db=data/tikv-21107/db unsafe_remove_sst_file "data/tikv-21107/db/000014.sst"
    tikv-ctl --db=data/tikv-21107/db tombstone -r 4 --pd <endpoint>
    --------------------------------------------------------
    corruption analysis has completed

上記の出力から、破損した SST ファイルの情報が最初に出力され、次にメタ情報が出力されることがわかります。

-   `sst meta`部分の`14` SST ファイル番号を意味します。 `552997`ファイル サイズを意味し、その後に最小および最大のシーケンス番号およびその他のメタ情報が続きます。
-   `overlap region`部分は、関係するリージョンの情報を示します。この情報は PDサーバーを通じて取得されます。
-   `suggested operations`番目の部分では、破損した SST ファイルをクリーンアップするための提案が提供されます。ファイルをクリーンアップして TiKV インスタンスを再起動するという提案を採用できます。
