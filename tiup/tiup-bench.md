---
title: Stress Test TiDB Using TiUP Bench Component
summary: TiUPを使用して、TPC-C、TPC-H、CH、RawSQL、および YCSB ワークロードで TiDB のストレス テストを実行する方法を学習します。
---

# TiUPベンチコンポーネントを使用したTiDBのストレステスト {#stress-test-tidb-using-tiup-bench-component}

データベースのパフォーマンスをテストする際には、データベースのストレステストが必要になることがよくあります。これを容易にするために、 TiUPにはベンチコンポーネントが統合されており、ストレステスト用の複数のワークロードが用意されています。これらのワークロードには、以下のコマンドでアクセスできます。

```bash
tiup bench tpcc   # Benchmark a database using TPC-C
tiup bench tpch   # Benchmark a database using TPC-H
tiup bench ch     # Benchmark a database using CH-benCHmark
tiup bench ycsb   # Benchmark a database using YCSB
tiup bench rawsql # Benchmark a database using arbitrary SQL files
```

`tpcc` 、 `tpch` 、 `ch` 、 `rawsql`以下の共通コマンドフラグを共有します。ただし、 `ycsb`主に`.properties`ファイルによって設定され、その[使用ガイド](https://github.com/pingcap/go-ycsb#usage)に記述されています。

      -t, --acThreads int         OLAP client concurrency, only for CH-benCHmark (default to 1)
          --conn-params string    Session variables, such as setting `--conn-params tidb_isolation_read_engines='tiflash'` for TiDB queries and setting `--conn-params sslmode=disable` for PostgreSQL connections
          --count int             Total execution count (0 means infinite count)
      -D, --db string             Database name (default to "test")
      -d, --driver string         Database driver: mysql, postgres (default to "mysql")
          --dropdata              Clean up historical data before preparing
      -H, --host strings          Database host (default to [127.0.0.1])
          --ignore-error          Ignore errors when running workload
          --interval duration     Output interval time (default to 10s)
          --isolation int         Isolation Level (0: Default; 1: ReadUncommitted;
                                  2: ReadCommitted; 3: WriteCommitted; 4: RepeatableRead;
                                  5: Snapshot; 6: Serializable; 7: Linerizable)
          --max-procs int         runtime.GOMAXPROCS of golang, the limits of how many cores can be used
          --output string         Output style. Valid values can be { plain | table | json } (default to "plain")
      -p, --password string       Database password
      -P, --port ints             Database port (default to [4000])
          --pprof string          Address of pprof endpoint
          --silence               Don't print errors when running workload
      -S, --statusPort int        Database status port (default to 10080)
      -T, --threads int           Thread concurrency (default to 1)
          --time duration         Total execution time (default to 2562047h47m16.854775807s)
      -U, --user string           Database user (default to "root")

-   `--host`と`--port`にカンマ区切りの値を指定すると、クライアント側の負荷分散が有効になります。例えば`--host 172.16.4.1,172.16.4.2 --port 4000,4001`指定すると、プログラムはラウンドロビン方式で選択された 172.16.4.1:4000、172.16.4.1:4001、172.16.4.2:4000、172.16.4.2:4001 に接続します。
-   ローカルデプロイメントの場合、デフォルトのデータベースホストアドレスは`127.0.0.1`です。リモートデータベースに接続する場合は、ホストとその他の関連パラメータを指定する必要があります。例: `tiup bench tpcc -H 192.168.169.31 -P 4000 -D tpcc -U root -p tidb --warehouses 4 --parts 4 prepare`
-   `--conn-params` [クエリ文字列](https://en.wikipedia.org/wiki/Query_string)の形式に従う必要があります。データベースによってパラメータが異なる場合があります。例:
    -   `--conn-params tidb_isolation_read_engines='tiflash'` TiDB にTiFlashからの読み取りを強制します。
    -   `--conn-params sslmode=disable` 、PostgreSQL に接続するときに SSL を無効にします。
-   CH-benCHmark を実行する場合、 `--ap-host` 、 `--ap-port` 、 `--ap-conn-params`使用して、OLAP クエリ用のスタンドアロン TiDBサーバーを指定できます。

次のセクションでは、 TiUPを使用して TPC-C、TPC-H、YCSB テストを実行する方法について説明します。

## TiUPを使用してTPC-Cテストを実行する {#run-tpc-c-test-using-tiup}

TiUPベンチコンポーネントは、TPC-C テストを実行するために次のコマンドとフラグをサポートしています。

```bash
Available Commands:
  check       Check data consistency for the workload
  cleanup     Cleanup data for the workload
  prepare     Prepare data for the workload
  run         Run workload

Flags:
      --check-all            Run all consistency checks
  -h, --help                 Help for TPC-C
      --partition-type int   Partition type: 1 - HASH, 2 - RANGE, 3 - LIST (HASH-like), 4 - LIST (RANGE-like) (default to 1)
      --parts int            Number of partitions (default to 1)
      --warehouses int       Number of warehouses (default to 10)

```

### テスト手順 {#test-procedures}

TPC-Cテストを実行するための簡略化された手順を以下に示します。詳細な手順については、 [TiDBでTPC-Cテストを実行する方法](/benchmark/benchmark-tidb-using-tpcc.md)参照してください。

1.  ハッシュを使用して 4 つのパーティションを使用して 4 つの倉庫を作成します。

    ```shell
    tiup bench tpcc --warehouses 4 --parts 4 prepare
    ```

2.  TPC-C テストを実行します。

    ```shell
    tiup bench tpcc --warehouses 4 --time 10m run
    ```

3.  一貫性を確認します。

    ```shell
    tiup bench tpcc --warehouses 4 check
    ```

4.  データをクリーンアップします:

    ```shell
    tiup bench tpcc --warehouses 4 cleanup
    ```

大規模なデータセットでベンチマークを実行する場合、SQLによるデータ準備は遅くなる可能性があります。その場合は、以下のコマンドでCSV形式のデータを生成し、 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)経由でTiDBにインポートできます。

-   CSV ファイルを生成します。

    ```shell
    tiup bench tpcc --warehouses 4 prepare --output-dir data --output-type=csv
    ```

-   指定されたテーブルの CSV ファイルを生成します。

    ```shell
    tiup bench tpcc --warehouses 4 prepare --output-dir data --output-type=csv --tables history,orders
    ```

## TiUPを使用してTPC-Hテストを実行する {#run-tpc-h-test-using-tiup}

TiUPベンチコンポーネントは、TPC-H テストを実行するために次のコマンドとパラメーターをサポートしています。

```bash
Available Commands:
  cleanup     Cleanup data for the workload
  prepare     Prepare data for the workload
  run         Run workload

Flags:
      --check            Check output data, only when the scale factor equals 1
  -h, --help             help for tpch
      --queries string   All queries (default "q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22")
      --sf int           scale factor
```

### テスト手順 {#test-procedures}

1.  データを準備します:

    ```shell
    tiup bench tpch --sf=1 prepare
    ```

2.  統計を収集します。

    OLAPシナリオでは、TiDBオプティマイザーが最適な実行プランを生成できるように、以下のSQL文を実行して事前に統計情報を収集してください。tidb_analyze_column_options **<a href="/system-variables.md#tidb_analyze_column_options-new-in-v830">`tidb_analyze_column_options`</a> `ALL`に設定してください。そうしないと、統計情報を収集するとクエリのパフォーマンスが大幅に低下する可能性があります。**

    ```sql
    set global tidb_analyze_column_options='ALL';
    ```

3.  次のいずれかのコマンドを実行して、TPC-H テストを実行します。

    -   結果を確認する場合は、次のコマンドを実行します。

        ```shell
        tiup bench tpch --count=22 --sf=1 --check=true run
        ```

    -   結果を確認しない場合は、次のコマンドを実行します。

        ```shell
        tiup bench tpch --count=22 --sf=1 run
        ```

4.  データをクリーンアップします:

    ```shell
    tiup bench tpch cleanup
    ```

## TiUPを使用してYCSBテストを実行する {#run-ycsb-test-using-tiup}

YCSB を介して TiDB と TiKV の両方をストレス テストできます。

### ストレステスト TiDB {#stress-test-tidb}

1.  データを準備します:

    ```shell
    tiup bench ycsb load tidb -p tidb.instances="127.0.0.1:4000" -p recordcount=10000
    ```

2.  YCSB ワークロードを実行します。

    ```shell
    # The read-write percent is 95% by default
    tiup bench ycsb run tidb -p tidb.instances="127.0.0.1:4000" -p operationcount=10000
    ```

### ストレステスト TiKV {#stress-test-tikv}

1.  データを準備します:

    ```shell
    tiup bench ycsb load tikv -p tikv.pd="127.0.0.1:2379" -p recordcount=10000
    ```

2.  YCSB ワークロードを実行します。

    ```shell
    # The read-write percent is 95% by default
    tiup bench ycsb run tikv -p tikv.pd="127.0.0.1:2379" -p operationcount=10000
    ```

## TiUPを使用してRawSQLテストを実行する {#run-rawsql-test-using-tiup}

任意のクエリを SQL ファイルに記述し、次のように`tiup bench rawsql`実行してテストに使用することができます。

1.  データとクエリを準備します。

    ```sql
    -- Prepare data
    CREATE TABLE t (a int);
    INSERT INTO t VALUES (1), (2), (3);

    -- Save your query in a SQL file. For example, you can save the following query in `demo.sql`.
    SELECT a, sleep(rand()) FROM t WHERE a < 4*rand();
    ```

2.  RawSQL テストを実行します。

    ```shell
    tiup bench rawsql run --count 60 --query-files demo.sql
    ```
