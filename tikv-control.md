---
title: TiKV Control User Guide
summary: Use TiKV Control to manage a TiKV cluster.
---

# TiKVControlユーザーガイド {#tikv-control-user-guide}

TiKV Control（ `tikv-ctl` ）は、クラスタの管理に使用されるTiKVのコマンドラインツールです。そのインストールディレクトリは次のとおりです。

-   クラスタがTiUPを使用して展開されている場合、 `tikv-ctl`のディレクトリが`~/.tiup/components/ctl/{VERSION}/`のディレクトリにあります。

## TiUPでTiKVコントロールを使用する {#use-tikv-control-in-tiup}

> **ノート：**
>
> 使用するコントロールツールのバージョンは、クラスタのバージョンと一致していることをお勧めします。

`tikv-ctl`は`tiup`コマンドにも統合されています。次のコマンドを実行して、 `tikv-ctl`ツールを呼び出します。

{{< copyable "" >}}

```bash
tiup ctl tikv
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
        --ca-path <ca_path>              Set the CA certificate path
        --cert-path <cert_path>          Set the certificate path
        --config <config>                Set the config for rocksdb
        --db <db>                        Set the rocksdb path
        --decode <decode>                Decode a key in escaped format
        --encode <encode>                Encode a key in escaped format
        --to-hex <escaped-to-hex>        Convert an escaped key to hex key
        --to-escaped <hex-to-escaped>    Convert a hex key to escaped key
        --host <host>                    Set the remote host
        --key-path <key_path>            Set the private key path
        --pd <pd>                        Set the address of pd
        --raftdb <raftdb>                Set the raft rocksdb path
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

`tiup ctl tikv`の後に、対応するパラメータとサブコマンドを追加できます。

## 一般的なオプション {#general-options}

`tikv-ctl`は、次の2つの動作モードを提供します。

-   リモートモード： `--host`オプションを使用して、TiKVのサービスアドレスを引数として受け入れます

    このモードでは、SSLがTiKVで有効になっている場合、 `tikv-ctl`は関連する証明書ファイルも指定する必要があります。例えば：

    ```
    $ tikv-ctl --ca-path ca.pem --cert-path client.pem --key-path client-key.pem --host 127.0.0.1:20160 <subcommands>
    ```

    ただし、 `tikv-ctl`がTiKVではなくPDと通信する場合があります。この場合、 `--host`ではなく`--pd`オプションを使用する必要があります。次に例を示します。

    ```
    $ tikv-ctl --pd 127.0.0.1:2379 compact-cluster
    store:"127.0.0.1:20160" compact db:KV cf:default range:([], []) success!
    ```

-   ローカルモード： `--db`オプションを使用して、ローカルTiKVデータディレクトリパスを指定します。このモードでは、実行中のTiKVインスタンスを停止する必要があります。

特に明記されていない限り、すべてのコマンドはリモートモードとローカルモードの両方をサポートしています。

さらに、 `tikv-ctl`には2つの簡単なコマンド`--to-hex`と`--to-escaped`があり、これらはキーの形式に簡単な変更を加えるために使用されます。

通常、キーの`escaped`の形式を使用します。例えば：

```bash
$ tikv-ctl --to-escaped 0xaaff
\252\377
$ tikv-ctl --to-hex "\252\377"
AAFF
```

> **ノート：**
>
> コマンドラインでキーの`escaped`形式を指定する場合は、二重引用符で囲む必要があります。そうしないと、bashがバックスラッシュを食いつぶし、間違った結果が返されます。

## サブコマンド、いくつかのオプションとフラグ {#subcommands-some-options-and-flags}

このセクションでは、 `tikv-ctl`がサポートするサブコマンドについて詳しく説明します。一部のサブコマンドは、多くのオプションをサポートしています。詳細については、 `tikv-ctl --help <subcommand>`を実行してください。

### ラフトステートマシンの情報を表示する {#view-information-of-the-raft-state-machine}

`raft`サブコマンドを使用して、特定の時点でのRaftステートマシンのステータスを表示します。ステータス情報には、3つの構造体（ **RegionLocalState** 、 <strong>RaftLocalState</strong> 、および<strong>RegionApplyState</strong> ）と、特定のログの対応するエントリの2つの部分が含まれます。

`region`および`log`サブコマンドを使用して、それぞれ上記の情報を取得します。 2つのサブコマンドは、両方ともリモートモードとローカルモードを同時にサポートします。それらの使用法と出力は次のとおりです。

```bash
$ tikv-ctl --host 127.0.0.1:20160 raft region -r 2
region id: 2
region state key: \001\003\000\000\000\000\000\000\000\002\001
region state: Some(region {id: 2 region_epoch {conf_ver: 3 version: 1} peers {id: 3 store_id: 1} peers {id: 5 store_id: 4} peers {id: 7 store_id: 6}})
raft state key: \001\002\000\000\000\000\000\000\000\002\002
raft state: Some(hard_state {term: 307 vote: 5 commit: 314617} last_index: 314617)
apply state key: \001\002\000\000\000\000\000\000\000\002\003
apply state: Some(applied_index: 314617 truncated_state {index: 313474 term: 151})
```

### リージョンサイズを表示する {#view-the-region-size}

`size`コマンドを使用して、リージョンサイズを表示します。

```bash
$ tikv-ctl --data-dir /path/to/tikv size -r 2
region id: 2
cf default region size: 799.703 MB
cf write region size: 41.250 MB
cf lock region size: 27616
```

### 特定の範囲のMVCCを表示するためにスキャンします {#scan-to-view-mvcc-of-a-specific-range}

`scan`コマンドの`--from`および`--to`オプションは、2つのエスケープされた形式のrawキーを受け入れ、 `--show-cf`フラグを使用して、表示する必要のある列ファミリーを指定します。

```bash
$ tikv-ctl --data-dir /path/to/tikv scan --from 'zm' --limit 2 --show-cf lock,default,write
key: zmBootstr\377a\377pKey\000\000\377\000\000\373\000\000\000\000\000\377\000\000s\000\000\000\000\000\372
         write cf value: start_ts: 399650102814441473 commit_ts: 399650102814441475 short_value: "20"
key: zmDB:29\000\000\377\000\374\000\000\000\000\000\000\377\000H\000\000\000\000\000\000\371
         write cf value: start_ts: 399650105239273474 commit_ts: 399650105239273475 short_value: "\000\000\000\000\000\000\000\002"
         write cf value: start_ts: 399650105199951882 commit_ts: 399650105213059076 short_value: "\000\000\000\000\000\000\000\001"
```

### 特定のキーのMVCCを表示する {#view-mvcc-of-a-given-key}

`scan`コマンドと同様に、 `mvcc`コマンドを使用して特定のキーのMVCCを表示できます。

```bash
$ tikv-ctl --data-dir /path/to/tikv mvcc -k "zmDB:29\000\000\377\000\374\000\000\000\000\000\000\377\000H\000\000\000\000\000\000\371" --show-cf=lock,write,default
key: zmDB:29\000\000\377\000\374\000\000\000\000\000\000\377\000H\000\000\000\000\000\000\371
         write cf value: start_ts: 399650105239273474 commit_ts: 399650105239273475 short_value: "\000\000\000\000\000\000\000\002"
         write cf value: start_ts: 399650105199951882 commit_ts: 399650105213059076 short_value: "\000\000\000\000\000\000\000\001"
```

このコマンドでは、キーはエスケープされた形式のrawキーでもあります。

### 生のキーをスキャンする {#scan-raw-keys}

`raw-scan`コマンドは、RocksDBから直接スキャンします。データキーをスキャンするには、キーに`'z'`のプレフィックスを追加する必要があることに注意してください。

`--from`と`--to`のオプションを使用して、スキャンする範囲を指定します（デフォルトでは無制限）。印刷するキーの最大数を制限するには、 `--limit`を使用します（デフォルトでは30）。 `--cf`を使用して、スキャンするcfを指定します（ `default` 、または`write`のいずれかに`lock`ます）。

```bash
$ ./tikv-ctl --data-dir /var/lib/tikv raw-scan --from 'zt' --limit 2 --cf default
key: "zt\200\000\000\000\000\000\000\377\005_r\200\000\000\000\000\377\000\000\001\000\000\000\000\000\372\372b2,^\033\377\364", value: "\010\002\002\002%\010\004\002\010root\010\006\002\000\010\010\t\002\010\n\t\002\010\014\t\002\010\016\t\002\010\020\t\002\010\022\t\002\010\024\t\002\010\026\t\002\010\030\t\002\010\032\t\002\010\034\t\002\010\036\t\002\010 \t\002\010\"\t\002\010s\t\002\010&\t\002\010(\t\002\010*\t\002\010,\t\002\010.\t\002\0100\t\002\0102\t\002\0104\t\002"
key: "zt\200\000\000\000\000\000\000\377\025_r\200\000\000\000\000\377\000\000\023\000\000\000\000\000\372\372b2,^\033\377\364", value: "\010\002\002&slow_query_log_file\010\004\002P/usr/local/mysql/data/localhost-slow.log"

Total scanned keys: 2
```

### 特定のキー値を出力する {#print-a-specific-key-value}

キーの値を出力するには、 `print`コマンドを使用します。

### 地域に関するいくつかのプロパティを印刷する {#print-some-properties-about-region}

リージョンの状態の詳細を記録するために、TiKVはリージョンのSSTファイルにいくつかの統計を書き込みます。これらのプロパティを表示するには、 `region-properties`サブコマンドで`tikv-ctl`を実行します。

```bash
$ tikv-ctl --host localhost:20160 region-properties -r 2
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

プロパティを使用して、リージョンが正常であるかどうかを確認できます。そうでない場合は、それらを使用してリージョンを修正できます。たとえば、リージョンを手動で`middle_key_approximate_size`で分割します。

### 各TiKVのコンパクトデータを手動で {#compact-data-of-each-tikv-manually}

`compact`コマンドを使用して、各TiKVのデータを手動で圧縮します。 `--from`および`--to`オプションを指定すると、それらのフラグもエスケープされたrawキーの形式になります。

-   `--host`オプションを使用して、圧縮を実行する必要があるTiKVを指定します。
-   `-d`オプションを使用して、圧縮を実行するRocksDBを指定します。オプションの値は`kv`と`raft`です。
-   `--threads`オプションを使用すると、TiKV圧縮の同時実行性を指定でき、デフォルト値は`8`です。一般に、同時実行性が高いほど圧縮速度が速くなりますが、サービスに影響を与える可能性があります。シナリオに基づいて、適切な同時実行数を選択する必要があります。
-   `--bottommost`オプションを使用して、TiKVが圧縮を実行するときに最下部のファイルを含めるか除外します。値のオプションは`default` 、および`skip` `force` 。デフォルト値は`default`です。
    -   `default`は、圧縮フィルター機能が有効になっている場合にのみ、最下部のファイルが含まれることを意味します。
    -   `skip`は、TiKVが圧縮を実行するときに最下部のファイルが除外されることを意味します。
    -   `force`は、TiKVが圧縮を実行するときに、最下部のファイルが常に含まれることを意味します。

```bash
$ tikv-ctl --data-dir /path/to/tikv compact -d kv
success!
```

### TiKVクラスタ全体のコンパクトなデータを手動で {#compact-data-of-the-whole-tikv-cluster-manually}

`compact-cluster`コマンドを使用して、TiKVクラスタ全体のデータを手動で圧縮します。このコマンドのフラグは、 `compact`コマンドのフラグと同じ意味と使用法を持っています。

### リージョンをトゥームストーンに設定します {#set-a-region-to-tombstone}

`tombstone`コマンドは通常、同期ログが有効になっておらず、電源を切るとRaftステートマシンに書き込まれたデータの一部が失われる状況で使用されます。

TiKVインスタンスでは、このコマンドを使用して、一部のリージョンのステータスをトゥームストーンに設定できます。次に、インスタンスを再起動すると、それらのリージョンはスキップされ、それらのリージョンの破損したRaftステートマシンによって引き起こされる再起動の失敗を回避します。これらのリージョンには、Raftメカニズムを介して読み取りと書き込みを続行できるように、他のTiKVインスタンスに十分な正常なレプリカが必要です。

通常、 `remove-peer`コマンドを使用して、このリージョンの対応するピアを削除できます。

{{< copyable "" >}}

```shell
pd-ctl operator add remove-peer <region_id> <store_id>
```

次に、 `tikv-ctl`ツールを使用して、対応するTiKVインスタンスのリージョンをトゥームストーンに設定し、起動時にこのリージョンのヘルスチェックをスキップします。

{{< copyable "" >}}

```shell
tikv-ctl --data-dir /path/to/tikv tombstone -p 127.0.0.1:2379 -r <region_id>
```

```
success!
```

ただし、場合によっては、このリージョンのこのピアをPDから簡単に削除できないため、 `tikv-ctl`の`--force`オプションを指定して、ピアをトゥームストーンに強制的に設定できます。

{{< copyable "" >}}

```shell
tikv-ctl --data-dir /path/to/tikv tombstone -p 127.0.0.1:2379 -r <region_id>,<region_id> --force
```

```
success!
```

> **ノート：**
>
> -   `tombstone`コマンドは、ローカルモードのみをサポートします。
> -   `-p`オプションの引数は、 `http`プレフィックスなしのPDエンドポイントを指定します。 PDエンドポイントを指定することは、PDがTombstoneに安全に切り替えることができるかどうかを照会することです。

### TiKVに<code>consistency-check</code>要求を送信します {#send-a-code-consistency-check-code-request-to-tikv}

`consistency-check`コマンドを使用して、特定のリージョンの対応するラフト内のレプリカ間の整合性チェックを実行します。チェックが失敗すると、TiKV自体がパニックになります。 `--host`で指定されたTiKVインスタンスがリージョンリーダーでない場合、エラーが報告されます。

```bash
$ tikv-ctl --host 127.0.0.1:20160 consistency-check -r 2
success!
$ tikv-ctl --host 127.0.0.1:20161 consistency-check -r 2
DebugClient::check_region_consistency: RpcFailure(RpcStatus { status: Unknown, details: Some("StringError(\"Leader is on store 1\")") })
```

> **ノート：**
>
> -   `consistency-check`コマンドを使用することはお勧めし**ません**。これは、TiDBのガベージコレクションと互換性がなく、誤ってエラーを報告する可能性があるためです。
> -   このコマンドは、リモートモードのみをサポートします。
> -   このコマンドが`success!`を返した場合でも、TiKVがパニックになるかどうかを確認する必要があります。これは、このコマンドがリーダーの整合性チェックを要求する提案にすぎず、チェックプロセス全体が成功したかどうかをクライアントから知ることができないためです。

### スナップショットメタをダンプ {#dump-snapshot-meta}

このサブコマンドは、指定されたパスでスナップショットメタファイルを解析し、結果を出力するために使用されます。

### Raftステートマシンが破損しているリージョンを印刷します {#print-the-regions-where-the-raft-state-machine-corrupts}

TiKVの起動中にリージョンをチェックしないようにするには、 `tombstone`コマンドを使用して、RaftステートマシンがTombstoneにエラーを報告するリージョンを設定します。このコマンドを実行する前に、 `bad-regions`コマンドを使用してエラーのあるリージョンを見つけ、自動処理のために複数のツールを組み合わせます。

```bash
$ tikv-ctl --data-dir /path/to/tikv bad-regions
all regions are healthy
```

コマンドが正常に実行されると、上記の情報が出力されます。コマンドが失敗すると、不良リージョンのリストが出力されます。現在、検出できるエラーには、 `last index`の不一致、および`apply index`ログの損失が含まれ`commit index` 。スナップショットファイルの損傷などの他の条件については、さらにサポートが必要です。

### リージョンのプロパティを表示する {#view-region-properties}

-   `/path/to/tikv`でデプロイされたTiKVインスタンスのリージョン2のプロパティをローカルで表示するには：

    ```bash
    $ tikv-ctl --data-dir /path/to/tikv/data region-properties -r 2
    ```

-   `127.0.0.1:20160`で実行されているTiKVインスタンスのリージョン2のプロパティをオンラインで表示するには：

    ```bash
    $ tikv-ctl --host 127.0.0.1:20160 region-properties -r 2
    ```

### TiKV構成を動的に変更する {#modify-the-tikv-configuration-dynamically}

`modify-tikv-config`コマンドを使用して、構成引数を動的に変更できます。現在、動的に変更できるTiKV構成項目と詳細な変更は、SQLステートメントを使用した構成の変更と一致しています。詳細については、 [TiKV構成をオンラインで変更する](/dynamic-config.md#modify-tikv-configuration-online)を参照してください。

-   `-n`は、構成アイテムのフルネームを指定するために使用されます。オンラインで変更できる構成項目のリストについては、 [TiKV構成をオンラインで変更する](/dynamic-config.md#modify-tikv-configuration-online)を参照してください。
-   `-v`は、構成値を指定するために使用されます。

`shared block cache`のサイズを設定します：

{{< copyable "" >}}

```shell
tikv-ctl --host ip:port modify-tikv-config -n storage.block-cache.capacity -v 10GB
```

```
success
```

`shared block cache`が無効になっている場合、 `write`に`block cache size`を設定します。

{{< copyable "" >}}

```shell
tikv-ctl --host ip:port modify-tikv-config -n rocksdb.writecf.block-cache-size -v 256MB
```

```
success
```

{{< copyable "" >}}

```shell
tikv-ctl --host ip:port modify-tikv-config -n raftdb.defaultcf.disable-auto-compactions -v true
```

```
success
```

{{< copyable "" >}}

```shell
tikv-ctl --host ip:port modify-tikv-config -n raftstore.sync-log -v false
```

```
success
```

圧縮率の制限により累積圧縮保留バイトが発生する場合は、 `rate-limiter-auto-tuned`モードを無効にするか、圧縮フローの上限を設定します。

{{< copyable "" >}}

```shell
tikv-ctl --host ip:port modify-tikv-config -n rocksdb.rate-limiter-auto-tuned -v false
```

```
success
```

{{< copyable "" >}}

```shell
tikv-ctl --host ip:port modify-tikv-config -n rocksdb.rate-bytes-per-sec -v "1GB"
```

```
success
```

### リージョンに複数のレプリカの障害からサービスを回復させる（非推奨） {#force-regions-to-recover-services-from-failure-of-multiple-replicas-deprecated}

> **警告：**
>
> この機能の使用はお勧めしません。代わりに、ワンストップ自動リカバリ機能を提供するOnline Unsafe Recoveryin1を使用でき`pd-ctl` 。サービスの停止などの追加操作は必要ありません。詳細な紹介については、 [オンラインの安全でない回復](/online-unsafe-recovery.md)を参照してください。

`unsafe-recover remove-fail-stores`コマンドを使用して、障害が発生したマシンをリージョンのピアリストから削除できます。このコマンドを実行する前に、ターゲットTiKVストアのサービスを停止して、ファイルロックを解除する必要があります。

`-s`オプションは、コンマで区切られた複数の`store_id`を受け入れ、 `-r`フラグを使用して関連するリージョンを指定します。特定のストア内のすべてのリージョンでこの操作を実行する必要がある場合は、 `--all-regions`を指定するだけです。

> **警告：**
>
> -   誤操作が発生した場合、クラスタの復旧が困難になる場合があります。潜在的なリスクを認識し、本番環境でこの機能を使用しないようにしてください。
> -   `--all-regions`オプションを使用する場合、クラスタに接続されている残りのすべてのストアでこのコマンドを実行する必要があります。損傷した店舗を復旧する前に、これらの健全な店舗がサービスの提供を停止していることを確認する必要があります。そうしないと、リージョンレプリカのピアリストに一貫性がないため、 `split-region`または`remove-peer`を実行したときにエラーが発生します。これにより、他のメタデータ間の不整合がさらに発生し、最終的にリージョンが使用できなくなります。
> -   `remove-fail-stores`を実行すると、削除されたノードを再起動したり、これらのノードをクラスタに追加したりすることはできません。そうしないと、メタデータに一貫性がなくなり、最終的にリージョンが使用できなくなります。

{{< copyable "" >}}

```shell
tikv-ctl --data-dir /path/to/tikv unsafe-recover remove-fail-stores -s 3 -r 1001,1002
```

```
success!
```

{{< copyable "" >}}

```shell
tikv-ctl --data-dir /path/to/tikv unsafe-recover remove-fail-stores -s 4,5 --all-regions
```

次に、TiKVを再起動した後、リージョンは残りの正常なレプリカでサービスを提供し続けることができます。このコマンドは、複数のTiKVストアが破損または削除された場合によく使用されます。

> **ノート：**
>
> -   このコマンドは、指定されたリージョンのピアが配置されているすべてのストアに対して実行する必要があります。
> -   このコマンドはローカルモードのみをサポートします。正常に実行されると`success!`を出力します。

### MVCCデータ破損から回復する {#recover-from-mvcc-data-corruption}

MVCCデータの破損が原因でTiKVが正常に実行できない状況では、 `recover-mvcc`コマンドを使用します。 3つのCF（「デフォルト」、「書き込み」、「ロック」）をクロスチェックして、さまざまな種類の不整合から回復します。

-   `-r`オプションを使用して、関係するリージョンを`region_id`で指定します。
-   `-p`オプションを使用して、PDエンドポイントを指定します。

```bash
$ tikv-ctl --data-dir /path/to/tikv recover-mvcc -r 1001,1002 -p 127.0.0.1:2379
success!
```

> **注**：
>
> -   このコマンドはローカルモードのみをサポートします。正常に実行されると`success!`を出力します。
> -   `-p`オプションの引数は、 `http`プレフィックスなしのPDエンドポイントを指定します。 PDエンドポイントを指定することは、指定された`region_id`が検証されているかどうかを照会することです。
> -   このコマンドは、指定されたリージョンのピアが配置されているすべてのストアに対して実行する必要があります。

### Ldbコマンド {#ldb-command}

`ldb`コマンドラインツールは、複数のデータアクセスおよびデータベース管理コマンドを提供します。いくつかの例を以下に示します。詳細については、 `tikv-ctl ldb`の実行時に表示されるヘルプメッセージを参照するか、RocksDBのドキュメントを確認してください。

データアクセスシーケンスの例：

既存のRocksDBをHEXにダンプするには：

```bash
$ tikv-ctl ldb --hex --db=/tmp/db dump
```

既存のRocksDBのマニフェストをダンプするには：

```bash
$ tikv-ctl ldb --hex manifest_dump --path=/tmp/db/MANIFEST-000001
```

`--column_family=<string>`コマンドラインを使用して、クエリが対象となる列ファミリーを指定できます。

`--try_load_options`は、データベースオプションファイルをロードしてデータベースを開きます。データベースの実行中は、このオプションを常にオンにしておくことをお勧めします。デフォルトのオプションでデータベースを開くと、LSMツリーが混乱し、自動的に回復できない場合があります。

### 暗号化メタデータをダンプします {#dump-encryption-metadata}

`encryption-meta`サブコマンドを使用して、暗号化メタデータをダンプします。サブコマンドは、データファイルの暗号化情報と使用されるデータ暗号化キーのリストの2種類のメタデータをダンプできます。

データファイルの暗号化情報をダンプするには、 `encryption-meta dump-file`サブコマンドを使用します。 TiKV構成ファイルを作成して、TiKV展開に`data-dir`を指定する必要があります。

```
# conf.toml
[storage]
data-dir = "/path/to/tikv/data"
```

`--path`オプションを使用して、対象のデータファイルへの絶対パスまたは相対パスを指定できます。データファイルが暗号化されていない場合、コマンドは空の出力を提供する可能性があります。 `--path`が指定されていない場合、すべてのデータファイルの暗号化情報が出力されます。

```bash
$ tikv-ctl --config=./conf.toml encryption-meta dump-file --path=/path/to/tikv/data/db/CURRENT
/path/to/tikv/data/db/CURRENT: key_id: 9291156302549018620 iv: E3C2FDBF63FC03BFC28F265D7E78283F method: Aes128Ctr
```

データ暗号化キーをダンプするには、 `encryption-meta dump-key`サブコマンドを使用します。 `data-dir`に加えて、構成ファイルで使用されている現在のマスターキーも指定する必要があります。マスターキーの設定方法については、 [残りの暗号化](/encryption-at-rest.md)を参照してください。また、このコマンドを使用すると、 `security.encryption.previous-master-key`構成は無視され、マスターキーのローテーションはトリガーされません。

```
# conf.toml
[storage]
data-dir = "/path/to/tikv/data"

[security.encryption.master-key]
type = "kms"
key-id = "0987dcba-09fe-87dc-65ba-ab0987654321"
region = "us-west-2"
```

マスターキーがAWSKMSキーである場合、 `tikv-ctl`はKMSキーにアクセスできる必要があることに注意してください。 AWS KMSキーへのアクセスは、環境変数、AWSデフォルト設定ファイル、またはIAMロールのいずれか適切な方を介して`tikv-ctl`に付与できます。使用法については、AWSドキュメントを参照してください。

`--ids`オプションを使用して、印刷するコンマ区切りのデータ暗号化キーIDのリストを指定できます。 `--ids`が指定されていない場合、すべてのデータ暗号化キーが、最新のアクティブなデータ暗号化キーのIDである現在のキーIDとともに出力されます。

コマンドを使用すると、アクションによって機密情報が公開されることを警告するプロンプトが表示されます。 「同意します」と入力して続行します。

```bash
$ ./tikv-ctl --config=./conf.toml encryption-meta dump-key
This action will expose encryption key(s) as plaintext. Do not output the result in file on disk.
Type "I consent" to continue, anything else to exit: I consent
current key id: 9291156302549018620
9291156302549018620: key: 8B6B6B8F83D36BE2467ED55D72AE808B method: Aes128Ctr creation_time: 1592938357
```

```bash
$ ./tikv-ctl --config=./conf.toml encryption-meta dump-key --ids=9291156302549018620
This action will expose encryption key(s) as plaintext. Do not output the result in file on disk.
Type "I consent" to continue, anything else to exit: I consent
9291156302549018620: key: 8B6B6B8F83D36BE2467ED55D72AE808B method: Aes128Ctr creation_time: 1592938357
```

> **ノート**
>
> このコマンドは、データ暗号化キーをプレーンテキストとして公開します。本番環境では、出力をファイルにリダイレクトしないでください。後で出力ファイルを削除しても、ディスクからコンテンツを完全に消去できない場合があります。

### 破損したSSTファイルに関連する情報を印刷する {#print-information-related-to-damaged-sst-files}

TiKV内の破損したSSTファイルにより、TiKVプロセスがパニックになる可能性があります。 TiDB v6.1.0より前では、これらのファイルによりTiKVはすぐにパニックになります。 TiDB v6.1.0以降、TiKVプロセスはSSTファイルが破損してから1時間後にパニックになります。

破損したSSTファイルをクリーンアップするには、TiKV Controlで`bad-ssts`コマンドを実行して、必要な情報を表示します。以下は、コマンドと出力の例です。

> **ノート：**
>
> このコマンドを実行する前に、実行中のTiKVインスタンスを停止してください。

```bash
$ tikv-ctl bad-ssts --data-dir </path/to/tikv> --pd <endpoint>
```

```bash
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

上記の出力から、破損したSSTファイルの情報が最初に印刷され、次にメタ情報が印刷されていることがわかります。

-   `sst meta`の部分で、 `14`はSSTファイル番号を意味します。 `552997`はファイルサイズを意味し、その後に最小および最大のシーケンス番号とその他のメタ情報が続きます。
-   `overlap region`部は関係する地域の情報を示しています。この情報は、PDサーバーを介して取得されます。
-   `suggested operations`の部分は、破損したSSTファイルをクリーンアップするための提案を提供します。ファイルをクリーンアップしてTiKVインスタンスを再起動するという提案を受け入れることができます。
