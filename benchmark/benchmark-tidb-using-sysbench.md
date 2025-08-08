---
title: How to Test TiDB Using Sysbench
summary: TiDBのパフォーマンスは、Sysbench 1.0以降を使用することで最適化できます。TiDBとTiKVのログレベルを高く設定することで、パフォーマンスが向上します。Sysbenchの設定を調整し、データをインポートすることで、パフォーマンスを最適化できます。プロキシの使用とCPU使用率に関連する一般的な問題にも対処できます。
---

# Sysbenchを使用してTiDBをテストする方法 {#how-to-test-tidb-using-sysbench}

Sysbench 1.0 以降 ( [ここからダウンロード](https://github.com/akopytov/sysbench/releases/tag/1.0.20)も可) の使用をお勧めします。

## テスト計画 {#test-plan}

### TiDB構成 {#tidb-configuration}

ログレベルを高くすると、出力されるログが少なくなり、TiDBのパフォーマンスが向上します。具体的には、 TiUP設定ファイルに以下のコマンドを追加してください。

```yaml
server_configs:
  tidb:
    log.level: "error"
```

また、 [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)有効になっていることを確認し、 `--db-ps-mode=auto`使用して sysbench が準備済みステートメントを使用できるようにすることをお勧めします。SQL プランキャッシュの機能と監視方法については、 [SQL 準備済み実行プランキャッシュ](/sql-prepared-plan-cache.md)のドキュメントを参照してください。

> **注記：**
>
> Sysbenchのバージョンによっては、デフォルト値の`db-ps-mode`異なる場合があります。コマンドで明示的に指定することをお勧めします。

### TiKV構成 {#tikv-configuration}

ログ レベルが高いほど、TiKV のパフォーマンスも向上します。

TiKVクラスターには複数のカラムファミリーがあり、主に異なる種類のデータを格納するために使用されます。デフォルトカラムファミリー、書き込みカラムファミリー、ロックカラムファミリーなどです。Sysbenchテストでは、デフォルトカラムファミリーと書き込みカラムファミリーのみに注目してください。データのインポートに使用されるカラムファミリーは、TiDBクラスター間で一定の割合で存在します。

デフォルトCF：書き込みCF = 4：1

TiKV上のRocksDBのブロックキャッシュは、メモリを最大限に活用するために、マシンのメモリサイズに基づいて設定する必要があります。40GBの仮想マシンにTiKVクラスターをデプロイする場合は、ブロックキャッシュを次のように設定することをお勧めします。

```yaml
server_configs:
  tikv:
    log-level: "error"
    rocksdb.defaultcf.block-cache-size: "24GB"
    rocksdb.writecf.block-cache-size: "6GB"
```

ブロックキャッシュを共有するように TiKV を構成することもできます。

```yaml
server_configs:
  tikv:
    storage.block-cache.capacity: "30GB"
```

TiKV パフォーマンス チューニングの詳細については、 [TiKVパフォーマンスの調整](/tune-tikv-memory-performance.md)参照してください。

## テストプロセス {#test-process}

> **注記：**
>
> このドキュメントのテストは、HAproxyなどの負荷分散ツールを使用せずに実施しました。TiDBノードごとにSysbenchテストを実行し、結果を合計しました。負荷分散ツールや異なるバージョンのパラメータもパフォーマンスに影響を与える可能性があります。

### Sysbenchの構成 {#sysbench-configuration}

これは Sysbench 構成ファイルの例です。

```txt
mysql-host={TIDB_HOST}
mysql-port=4000
mysql-user=root
mysql-password=password
mysql-db=sbtest
time=600
threads={8, 16, 32, 64, 128, 256}
report-interval=10
db-driver=mysql
```

上記のパラメータは、実際のニーズに合わせて調整できます。1 `TIDB_HOST` TiDBサーバーのIPアドレス（設定ファイルに複数のアドレスを含めることはできないため）、 `threads`テストにおける同時接続数で、「8、16、32、64、128、256」の範囲で調整できます。データをインポートする際は、threads = 8または16に設定することをお勧めします`threads`を調整したら、 **config**というファイルを保存します。

サンプル**設定**ファイルとして以下を参照してください。

```txt
mysql-host=172.16.30.33
mysql-port=4000
mysql-user=root
mysql-password=password
mysql-db=sbtest
time=600
threads=16
report-interval=10
db-driver=mysql
```

### データのインポート {#data-import}

> **注記：**
>
> 楽観的トランザクションモデルを有効にすると（TiDBはデフォルトで悲観的トランザクションモードを使用します）、同時実行の競合が検出されるとTiDBはトランザクションをロールバックします。1～ `tidb_disable_txn_auto_retry` `off`設定すると、トランザクションの競合が発生した後に自動再試行メカニズムが有効になり、トランザクション競合エラーによってSysbenchが終了するのを防ぐことができます。

データをインポートする前に、TiDBにいくつかの設定を行う必要があります。MySQLクライアントで以下のコマンドを実行してください。

```sql
set global tidb_disable_txn_auto_retry = off;
```

次にクライアントを終了します。

MySQL クライアントを再起動し、次の SQL ステートメントを実行してデータベース`sbtest`を作成します。

```sql
create database sbtest;
```

Sysbench スクリプトがインデックスを作成する順序を調整します。Sysbench は「テーブルの作成 -&gt; データの挿入 -&gt; インデックスの作成」という順序でデータをインポートするため、TiDB によるデータのインポートに時間がかかります。ユーザーはこの順序を調整することで、データのインポートを高速化できます。Sysbench バージョン[1.0.20](https://github.com/akopytov/sysbench/tree/1.0.20)使用している場合、順序は次の 2 つの方法で調整できます。

-   TiDB 用に変更された[oltp_common.lua](https://raw.githubusercontent.com/pingcap/tidb-bench/master/sysbench/sysbench-patch/oltp_common.lua)ファイルをダウンロードし、 `/usr/share/sysbench/oltp_common.lua`ファイルをそれで上書きします。
-   `/usr/share/sysbench/oltp_common.lua`で、行[235-240](https://github.com/akopytov/sysbench/blob/1.0.20/src/lua/oltp_common.lua#L235-L240)行 198 のすぐ後ろに移動します。

> **注記：**
>
> この操作はオプションであり、データのインポートにかかる時間を節約するためだけに行われます。

コマンドラインで以下のコマンドを入力してデータのインポートを開始します。設定ファイルは前の手順で設定したファイルです。

```bash
sysbench --config-file=config oltp_point_select --tables=32 --table-size=10000000 prepare
```

### 温暖化データと統計の収集 {#warming-data-and-collecting-statistics}

データをウォームアップするには、ディスクからメモリのブロックキャッシュにデータをロードします。ウォームアップされたデータにより、システム全体のパフォーマンスが大幅に向上しました。クラスターを再起動した後は、一度データをウォームアップすることをお勧めします。

```bash
sysbench --config-file=config oltp_point_select --tables=32 --table-size=10000000 prewarm
```

### Point select test command {#point-select-test-command}

```bash
sysbench --config-file=config oltp_point_select --tables=32 --table-size=10000000 --db-ps-mode=auto --rand-type=uniform run
```

### インデックス更新テストコマンド {#update-index-test-command}

```bash
sysbench --config-file=config oltp_update_index --tables=32 --table-size=10000000 --db-ps-mode=auto --rand-type=uniform run
```

### 読み取り専用テストコマンド {#read-only-test-command}

```bash
sysbench --config-file=config oltp_read_only --tables=32 --table-size=10000000 --db-ps-mode=auto --rand-type=uniform run
```

## よくある問題 {#common-issues}

### TiDB と TiKV は両方とも高い同時実行性で適切に構成されているのに、全体的なパフォーマンスがまだ低いのはなぜですか? {#tidb-and-tikv-are-both-properly-configured-under-high-concurrency-why-is-the-overall-performance-still-low}

この問題は多くの場合、プロキシの使用に関係しています。単一のTiDBサーバーに負荷をかけ、それぞれの結果を合計し、プロキシを使用した結果と比較することができます。

HAproxyを例に挙げましょう。パラメータ`nbproc`指定すると、起動できるプロセスの最大数を増やすことができます。HAproxyの最新バージョンでは、 `nbthread`と`cpu-map`サポートされています。これらはすべて、プロキシの使用によるパフォーマンスへの悪影響を軽減します。

### 同時実行性が高いのに、TiKV の CPU 使用率が低いのはなぜですか? {#under-high-concurrency-why-is-the-cpu-utilization-rate-of-tikv-still-low}

TiKV 全体の CPU 使用率は低いですが、クラスター内の一部のモジュールの CPU 使用率は高くなる可能性があります。

storage読み取りプール、コプロセッサ、gRPC など、TiKV 上の他のモジュールの最大同時実行制限は、TiKV 構成ファイルを通じて調整できます。

実際のCPU使用率は、GrafanaのTiKVスレッドCPUモニターパネルで確認できます。モジュールにボトルネックがある場合は、モジュールの同時実行性を高めることで調整できます。

### TiKV が高同時実行時の CPU 使用率のボトルネックにまだ達していないのに、なぜ TiDB の CPU 使用率がまだ低いのでしょうか? {#given-that-tikv-has-not-yet-reached-the-cpu-usage-bottleneck-under-high-concurrency-why-is-tidb-s-cpu-utilization-rate-still-low}

NUMAアーキテクチャのCPUは、一部のハイエンド機器で使用されています。これらの機器では、リモートメモリへのCPU間アクセスによってパフォーマンスが大幅に低下します。デフォルトでは、TiDBはサーバーのすべてのCPUを使用するため、goroutineスケジューリングによって必然的にCPU間メモリアクセスが発生します。

したがって、NUMAアーキテクチャのサーバーに*n 個の*TiDB ( *n*は NUMA CPU の数) を展開し、同時に TiDB パラメータ`max-procs` NUMA CPU コアの数と同じ値に設定することをお勧めします。
