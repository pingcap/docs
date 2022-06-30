---
title: Stress Test TiDB Using TiUP Bench Component
summary: Learns how to stress test TiDB with TPC-C and TPC-H workloads using TiUP.
---

# TiUPベンチコンポーネントを使用したTiDBのストレステスト {#stress-test-tidb-using-tiup-bench-component}

データベースのパフォーマンスをテストする場合、データベースのストレステストが必要になることがよくあります。これを容易にするために、TiUPはベンチコンポーネントを統合しました。これは、ストレステスト用の2つのワークロードを提供します： [TPC-C](http://www.tpc.org/tpcc/)と[TPC-H](http://www.tpc.org/tpch/) 。コマンドとフラグは次のとおりです。詳細については、 [TPC公式サイト](http://www.tpc.org)を参照してください。

{{< copyable "" >}}

```bash
tiup bench
```

```
Starting component `bench`: /home/tidb/.tiup/components/bench/v1.5.0/bench
Benchmark database with different workloads

Usage:
  tiup bench [command]

Available Commands:
  help        Help about any command
  tpcc
  tpch

Flags:
      --count int           Total execution count, 0 means infinite
  -D, --db string           Database name (default "test")
  -d, --driver string       Database driver: mysql
      --dropdata            Cleanup data before prepare
  -h, --help                help for /Users/joshua/.tiup/components/bench/v0.0.1/bench
  -H, --host string         Database host (default "127.0.0.1")
      --ignore-error        Ignore error when running workload
      --interval duration   Output interval time (default 10s)
      --isolation int       Isolation Level 0: Default, 1: ReadUncommitted,
                            2: ReadCommitted, 3: WriteCommitted, 4: RepeatableRead,
                            5: Snapshot, 6: Serializable, 7: Linerizable
      --max-procs int       runtime.GOMAXPROCS
  -p, --password string     Database password
  -P, --port int            Database port (default 4000)
      --pprof string        Address of pprof endpoint
      --silence             Don't print error when running workload
      --summary             Print summary TPM only, or also print current TPM when running workload
  -T, --threads int         Thread concurrency (default 16)
      --time duration       Total execution time (default 2562047h47m16.854775807s)
  -U, --user string         Database user (default "root")
```

次のセクションでは、TiUPを使用してTPC-CおよびTPC-Hテストを実行する方法について説明します。

## TiUPを使用してTPC-Cテストを実行します {#run-tpc-c-test-using-tiup}

TiUPベンチコンポーネントは、TPC-Cテストを実行するために次のコマンドとフラグをサポートしています。

```bash
Available Commands:
  check       Check data consistency for the workload
  cleanup     Cleanup data for the workload
  prepare     Prepare data for the workload
  run         Run workload

Flags:
      --check-all        Run all consistency checks
  -h, --help             help for tpcc
      --output string    Output directory for generating csv file when preparing data
      --parts int        Number to partition warehouses (default 1)
      --tables string    Specified tables for generating file, separated by ','. Valid only if output is set. If this flag is not set, generate all tables by default.
      --warehouses int   Number of warehouses (default 10)
```

### テスト手順 {#test-procedures}

1.  ハッシュを介して4つのパーティションを使用して4つのウェアハウスを作成します。

    {{< copyable "" >}}

    ```shell
    tiup bench tpcc --warehouses 4 --parts 4 prepare
    ```

2.  TPC-Cテストを実行します。

    {{< copyable "" >}}

    ```shell
    tiup bench tpcc --warehouses 4 run
    ```

3.  データのクリーンアップ：

    {{< copyable "" >}}

    ```shell
    tiup bench tpcc --warehouses 4 cleanup
    ```

4.  一貫性を確認します。

    {{< copyable "" >}}

    ```shell
    tiup bench tpcc --warehouses 4 check
    ```

5.  CSVファイルを生成します。

    {{< copyable "" >}}

    ```shell
    tiup bench tpcc --warehouses 4 prepare --output data
    ```

6.  指定されたテーブルのCSVファイルを生成します。

    {{< copyable "" >}}

    ```shell
    tiup bench tpcc --warehouses 4 prepare --output data --tables history,orders
    ```

7.  pprofを有効にします。

    {{< copyable "" >}}

    ```shell
    tiup bench tpcc --warehouses 4 prepare --output data --pprof :10111
    ```

8.  データのクリーンアップ：

    {{< copyable "" >}}

    ```shell
    tiup bench tpcc cleanup
    ```

## TiUPを使用してTPC-Hテストを実行します {#run-tpc-h-test-using-tiup}

TiUPベンチコンポーネントは、TPC-Hテストを実行するために次のコマンドとパラメータをサポートしています。

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

1.  データを準備する：

    {{< copyable "" >}}

    ```shell
    tiup bench tpch --sf=1 prepare
    ```

2.  次のいずれかのコマンドを実行して、TPC-Hテストを実行します。

    -   結果を確認する場合は、次のコマンドを実行します。

        {{< copyable "" >}}

        ```shell
        tiup bench tpch --sf=1 --check=true run
        ```

    -   結果を確認しない場合は、次のコマンドを実行します。

        {{< copyable "" >}}

        ```shell
        tiup bench tpch --sf=1 run
        ```

3.  データのクリーンアップ：

    {{< copyable "" >}}

    ```shell
    tiup bench tpch cleanup
    ```
