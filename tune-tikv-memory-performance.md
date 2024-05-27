---
title: Tune TiKV Memory Parameter Performance
summary: 最適なパフォーマンスを得るために TiKV パラメータを調整する方法を学びます。
---

# TiKV メモリ パラメータのパフォーマンスを調整する {#tune-tikv-memory-parameter-performance}

このドキュメントでは、最適なパフォーマンスを得るために TiKV パラメータを調整する方法について説明します。 デフォルトの構成ファイルは[etc/config-template.toml](https://github.com/tikv/tikv/blob/release-8.1/etc/config-template.toml)にあります。 構成を変更するには、構成項目の限定セットに対して[TiUPを使用する](/maintain-tidb-using-tiup.md#modify-the-configuration)または[TiKVを動的に変更する](/dynamic-config.md#modify-tikv-configuration-dynamically)実行します。 完全な構成については、 [TiKV 設定ファイル](/tikv-configuration-file.md)を参照してください。

TiKV は、TiKVアーキテクチャの最下位レベルで永続storageとして RocksDB を使用します。そのため、パフォーマンス パラメータの多くは RocksDB に関連しています。TiKV は 2 つの RocksDB インスタンスを使用します。デフォルトの RocksDB インスタンスは KV データを格納し、 Raft RocksDB インスタンス (RaftDB) はRaftログを格納します。

TiKV は RocksDB から`Column Families` (CF) を実装します。

-   デフォルトの RocksDB インスタンスは`write` KV データを`default` 、および`lock` CF に保存します。

    -   `default` CF には実際のデータが格納されます。対応するパラメータは`[rocksdb.defaultcf]`にあります。
    -   `write` CF には、マルチバージョン同時実行制御 (MVCC) のバージョン情報とインデックス関連のデータが格納されます。対応するパラメータは`[rocksdb.writecf]`にあります。
    -   `lock` CF にはロック情報が保存されます。システムはデフォルトのパラメータを使用します。

-   Raft RocksDB (RaftDB) インスタンスはRaftログを保存します。

    -   `default` CF にはRaftログが格納されます。対応するパラメータは`[raftdb.defaultcf]`にあります。

TiKV 3.0 以降では、デフォルトではすべての CF が 1 つのブロックキャッシュインスタンスを共有します。 `[storage.block-cache]`未満の`capacity`パラメータを設定することで、キャッシュのサイズを構成できます。ブロックキャッシュが大きいほど、より多くのホット データをキャッシュでき、データの読み取りが容易になりますが、その一方で、システムメモリの占有量も多くなります。

TiKV 3.0 より前では、共有ブロックキャッシュはサポートされていないため、各 CF ごとにブロックキャッシュを個別に構成する必要があります。

各 CF には個別の`write buffer`あります。 `write-buffer-size`パラメータを設定することでサイズを設定できます。

## パラメータ仕様 {#parameter-specification}

    # Log level: trace, debug, warn, error, info, off.
    log-level = "info"

    [server]
    # Set listening address
    # addr = "127.0.0.1:20160"

    # Size of thread pool for gRPC
    # grpc-concurrency = 4
    # The number of gRPC connections between each TiKV instance
    # grpc-raft-conn-num = 10

    # Most read requests from TiDB are sent to the coprocessor of TiKV. This parameter is used to set the number of threads
    # of the coprocessor. If many read requests exist, add the number of threads and keep the number within that of the
    # system CPU cores. For example, for a 32-core machine deployed with TiKV, you can even set this parameter to 30 in
    # repeatable read scenarios. If this parameter is not set, TiKV automatically sets it to CPU cores * 0.8.
    # end-point-concurrency = 8

    # Tag the TiKV instances to schedule replicas.
    # labels = {zone = "cn-east-1", host = "118", disk = "ssd"}

    [storage]
    # The data directory
    # data-dir = "/tmp/tikv/store"

    # In most cases, you can use the default value. When importing data, it is recommended to set the parameter to 1024000.
    # scheduler-concurrency = 102400
    # This parameter controls the number of write threads. When write operations occur frequently, set this parameter value
    # higher. Run `top -H -p tikv-pid` and if the threads named `sched-worker-pool` are busy, set the value of parameter
    # `scheduler-worker-pool-size` higher and increase the number of write threads.
    # scheduler-worker-pool-size = 4

    [storage.block-cache]
    ## Whether to create a shared block cache for all RocksDB column families.
    ##
    ## Block cache is used by RocksDB to cache uncompressed blocks. Big block cache can speed up read.
    ## It is recommended to turn on shared block cache. Since only the total cache size need to be
    ## set, it is easier to configure. In most cases, it should be able to auto-balance cache usage
    ## between column families with standard LRU algorithm.
    ##
    ## The rest of config in the storage.block-cache session is effective only when shared block cache
    ## is on.
    ## Starting from v6.6.0, the `shared` option is always enabled and cannot be disabled.
    # shared = true

    ## Size of the shared block cache. Normally it should be tuned to 30%-50% of system's total memory.
    ## When the config is not set, it is decided by the sum of the following fields or their default
    ## value:
    ##   * rocksdb.defaultcf.block-cache-size or 25% of system's total memory
    ##   * rocksdb.writecf.block-cache-size   or 15% of system's total memory
    ##   * rocksdb.lockcf.block-cache-size    or  2% of system's total memory
    ##   * raftdb.defaultcf.block-cache-size  or  2% of system's total memory
    ##
    ## To deploy multiple TiKV nodes on a single physical machine, configure this parameter explicitly.
    ## Otherwise, the OOM problem might occur in TiKV.
    # capacity = "1GB"

    [pd]
    # PD address
    # endpoints = ["127.0.0.1:2379","127.0.0.2:2379","127.0.0.3:2379"]

    [metric]
    # The interval of pushing metrics to Prometheus Pushgateway
    interval = "15s"
    # Prometheus Pushgateway address
    address = ""
    job = "tikv"

    [raftstore]
    # Raft RocksDB directory. The default value is Raft subdirectory of [storage.data-dir].
    # If there are multiple disks on the machine, store the data of Raft RocksDB on different disks to improve TiKV performance.
    # raftdb-path = "/tmp/tikv/store/raft"

    # When the data size change in a Region is larger than the threshold value, TiKV checks whether this Region needs split.
    # To reduce the costs of scanning data in the checking process, set the value to 32 MB during the data import process. In the normal operation status, set it to the default value.
    region-split-check-diff = "32MB"

    [coprocessor]
    ## If the size of a Region with the range of [a,e) is larger than the value of `region_max_size`, TiKV tries to split the Region to several Regions, for example, the Regions with the ranges of [a,b), [b,c), [c,d), and [d,e).
    ## After the Region split, the size of the split Regions is equal to the value of `region_split_size` (or slightly larger than the value of `region_split_size`).
    # region-max-size = "144MB"
    # region-split-size = "96MB"

    [rocksdb]
    # The maximum number of threads of RocksDB background tasks. The background tasks include compaction and flush.
    # For detailed information why RocksDB needs to implement compaction, see RocksDB-related materials. When write
    # traffic (like the importing data size) is big, it is recommended to enable more threads. But set the number of the enabled
    # threads smaller than that of CPU cores. For example, when importing data, for a machine with a 32-core CPU,
    # set the value to 28.
    # max-background-jobs = 8

    # The maximum number of file handles RocksDB can open
    # max-open-files = 40960

    # The file size limit of RocksDB MANIFEST. For more details, see https://github.com/facebook/rocksdb/wiki/MANIFEST
    max-manifest-file-size = "20MB"

    # The directory of RocksDB write-ahead logs. If there are two disks on the machine, store the RocksDB data and WAL logs
    # on different disks to improve TiKV performance.
    # wal-dir = "/tmp/tikv/store"

    # Use the following two parameters to deal with RocksDB archiving WAL.
    # For more details, see https://github.com/facebook/rocksdb/wiki/How-to-persist-in-memory-RocksDB-database%3F
    # wal-ttl-seconds = 0
    # wal-size-limit = 0

    # In most cases, set the maximum total size of RocksDB WAL logs to the default value.
    # max-total-wal-size = "4GB"

    # Use this parameter to enable the readahead feature during RocksDB compaction. If you are using mechanical disks, it is recommended to set the value to 2MB at least.
    # compaction-readahead-size = "2MB"

    [rocksdb.defaultcf]
    # The data block size. RocksDB compresses data based on the unit of block.
    # Similar to page in other databases, block is the smallest unit cached in block-cache.
    block-size = "64KB"

    # The compaction mode of each layer of RocksDB data. The optional values include no, snappy, zlib,
    # bzip2, lz4, lz4hc, and zstd. Note that the Snappy compressed file must be in the [official Snappy format](https://github.com/google/snappy). Other variants of Snappy compression are not supported.
    # "no:no:lz4:lz4:lz4:zstd:zstd" indicates there is no compaction of level0 and level1; lz4 compaction algorithm is used
    # from level2 to level4; zstd compaction algorithm is used from level5 to level6.
    # "no" means no compaction. "lz4" is a compaction algorithm with moderate speed and compaction ratio. The
    # compaction ratio of zlib is high. It is friendly to the storage space, but its compaction speed is slow. This
    # compaction occupies many CPU resources. Different machines deploy compaction modes according to CPU and I/O resources.
    # For example, if you use the compaction mode of "no:no:lz4:lz4:lz4:zstd:zstd" and find much I/O pressure of the
    # system (run the iostat command to find %util lasts 100%, or run the top command to find many iowaits) when writing
    # (importing) a lot of data while the CPU resources are adequate, you can compress level0 and level1 and exchange CPU
    # resources for I/O resources. If you use the compaction mode of "no:no:lz4:lz4:lz4:zstd:zstd" and you find the I/O
    # pressure of the system is not big when writing a lot of data, but CPU resources are inadequate. Then run the top
    # command and choose the -H option. If you find a lot of bg threads (namely the compaction thread of RocksDB) are
    # running, you can exchange I/O resources for CPU resources and change the compaction mode to "no:no:no:lz4:lz4:zstd:zstd".
    # In a word, it aims at making full use of the existing resources of the system and improving TiKV performance
    # in terms of the current resources.
    compression-per-level = ["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]

    # The RocksDB memtable size
    write-buffer-size = "128MB"

    # The maximum number of the memtables. The data written into RocksDB is first recorded in the WAL log, and then inserted
    # into memtables. When the memtable reaches the size limit of `write-buffer-size`, it turns into read only and generates
    # a new memtable receiving new write operations. The flush threads of RocksDB will flush the read only memtable to the
    # disks to become an sst file of level0. `max-background-flushes` controls the maximum number of flush threads. When the
    # flush threads are busy, resulting in the number of the memtables waiting to be flushed to the disks reaching the limit
    # of `max-write-buffer-number`, RocksDB stalls the new operation.
    # "Stall" is a flow control mechanism of RocksDB. When importing data, you can set the `max-write-buffer-number` value
    # higher, like 10.
    max-write-buffer-number = 5

    # When the number of sst files of level0 reaches the limit of `level0-slowdown-writes-trigger`, RocksDB
    # tries to slow down the write operation, because too many sst files of level0 can cause higher read pressure of
    # RocksDB. `level0-slowdown-writes-trigger` and `level0-stop-writes-trigger` are for the flow control of RocksDB.
    # When the number of sst files of level0 reaches 4 (the default value), the sst files of level0 and the sst files
    # of level1 which overlap those of level0 implement compaction to relieve the read pressure.
    level0-slowdown-writes-trigger = 20

    # When the number of sst files of level0 reaches the limit of `level0-stop-writes-trigger`, RocksDB stalls the new
    # write operation.
    level0-stop-writes-trigger = 36

    # When the level1 data size reaches the limit value of `max-bytes-for-level-base`, the sst files of level1
    # and their overlap sst files of level2 implement compaction. The golden rule: the first reference principle
    # of setting `max-bytes-for-level-base` is guaranteeing that the `max-bytes-for-level-base` value is roughly equal to the
    # data volume of level0. Thus unnecessary compaction is reduced. For example, if the compaction mode is
    # "no:no:lz4:lz4:lz4:lz4:lz4", the `max-bytes-for-level-base` value is write-buffer-size * 4, because there is no
    # compaction of level0 and level1 and the trigger condition of compaction for level0 is that the number of the
    # sst files reaches 4 (the default value). When both level0 and level1 adopt compaction, it is necessary to analyze
    # RocksDB logs to know the size of an sst file compressed from an mentable. For example, if the file size is 32MB,
    # the proposed value of `max-bytes-for-level-base` is 32MB * 4 = 128MB.
    max-bytes-for-level-base = "512MB"

    # The sst file size. The sst file size of level0 is influenced by the compaction algorithm of `write-buffer-size`
    # and level0. `target-file-size-base` is used to control the size of a single sst file of level1-level6.
    target-file-size-base = "32MB"

    [rocksdb.writecf]
    # Set it the same as `rocksdb.defaultcf.compression-per-level`.
    compression-per-level = ["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]

    # Set it the same as `rocksdb.defaultcf.write-buffer-size`.
    write-buffer-size = "128MB"
    max-write-buffer-number = 5
    min-write-buffer-number-to-merge = 1

    # Set it the same as `rocksdb.defaultcf.max-bytes-for-level-base`.
    max-bytes-for-level-base = "512MB"
    target-file-size-base = "32MB"

    [raftdb]
    # The maximum number of the file handles RaftDB can open
    # max-open-files = 40960

    # Enable the readahead feature in RaftDB compaction. If you are using mechanical disks, it is recommended to set
    # this value to 2MB at least.
    # compaction-readahead-size = "2MB"

    [raftdb.defaultcf]
    # Set it the same as `rocksdb.defaultcf.compression-per-level`.
    compression-per-level = ["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]

    # Set it the same as `rocksdb.defaultcf.write-buffer-size`.
    write-buffer-size = "128MB"
    max-write-buffer-number = 5
    min-write-buffer-number-to-merge = 1

    # Set it the same as `rocksdb.defaultcf.max-bytes-for-level-base`.
    max-bytes-for-level-base = "512MB"
    target-file-size-base = "32MB"

## TiKVメモリ使用量 {#tikv-memory-usage}

システムメモリを占有する`block cache`と`write buffer`の他に、次のシナリオでもシステムメモリが占​​有されます。

-   メモリの一部はシステムのページ キャッシュとして予約されています。

-   TiKV が`select * from ...`のような大きなクエリを処理する場合、データを読み取り、対応するデータ構造をメモリ内に生成し、この構造を TiDB に返します。このプロセス中、TiKV はメモリの一部を占有します。

## TiKVの推奨構成 {#recommended-configuration-of-tikv}

-   本番環境では、CPU コアが 8 未満、またはメモリが32 GB 未満のマシンに TiKV を展開することは推奨されません。

-   高い書き込みスループットが求められる場合は、スループット容量の優れたディスクを使用することをお勧めします。

-   非常に低い読み取り/書き込みレイテンシーを要求する場合は、高 IOPS の SSD を使用することをお勧めします。
