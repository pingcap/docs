---
title: How to Test TiDB Using Sysbench
summary: TiDB のパフォーマンスは、Sysbench 1.0 以降を使用して最適化できます。パフォーマンスを向上させるには、TiDB と TiKV をより高いログ レベルで構成します。Sysbench 構成を調整し、データをインポートしてパフォーマンスを最適化します。プロキシの使用と CPU 使用率に関連する一般的な問題に対処します。
---

# Sysbench を使用して TiDB をテストする方法 {#how-to-test-tidb-using-sysbench}

Sysbench 1.0 以降 ( [ここからダウンロード](https://github.com/akopytov/sysbench/releases/tag/1.0.20)も可) を使用することをお勧めします。

## テスト計画 {#test-plan}

### TiDB 構成 {#tidb-configuration}

ログ レベルを高くすると、出力されるログが少なくなり、TiDB のパフォーマンスが向上します。具体的には、 TiUP構成ファイルに次のコマンドを追加できます。

```yaml
server_configs:
  tidb:
    log.level: "error"
```

また、 [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)有効になっていることを確認し、 `--db-ps-mode=auto`使用して sysbench が準備されたステートメントを使用できるようにすることもお勧めします。SQL プラン キャッシュの機能と監視方法については、 [SQL 準備実行プラン キャッシュ](/sql-prepared-plan-cache.md)ドキュメントを参照してください。

> **注記：**
>
> Sysbench のバージョンによって、デフォルト値`db-ps-mode`が異なる場合があります。コマンドで明示的に指定することをお勧めします。

### TiKV 構成 {#tikv-configuration}

ログ レベルが高くなると、TiKV のパフォーマンスも向上します。

TiKV クラスターには、デフォルト CF、書き込み CF、ロック CF など、主にさまざまな種類のデータを格納するために使用される複数のカラムファミリがあります。Sysbench テストでは、デフォルト CF と書き込み CF にのみ焦点を当てる必要があります。データのインポートに使用されるカラムファミリは、TiDB クラスター間で一定の割合を持ちます。

デフォルト CF : 書き込み CF = 4 : 1

TiKV 上の RocksDB のブロックキャッシュを構成する場合は、メモリを最大限に活用するために、マシンのメモリサイズに基づいて構成する必要があります。40 GB の仮想マシンに TiKV クラスターをデプロイするには、ブロックキャッシュを次のように構成することをお勧めします。

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

TiKV パフォーマンス チューニングの詳細については、 [TiKV パフォーマンスの調整](/tune-tikv-memory-performance.md)参照してください。

## テストプロセス {#test-process}

> **注記：**
>
> このドキュメントのテストは、HAproxy などの負荷分散ツールを使用せずに実行されました。個々の TiDB ノードで Sysbench テストを実行し、結果を合計しました。負荷分散ツールと異なるバージョンのパラメータもパフォーマンスに影響を与える可能性があります。

### Sysbench 構成 {#sysbench-configuration}

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

上記のパラメータは、実際のニーズに応じて調整できます。そのうち、 `TIDB_HOST`は TiDBサーバーの IP アドレス (構成ファイルに複数のアドレスを含めることができないため)、 `threads`テストの同時接続数で、「8、16、32、64、128、256」に調整できます。データをインポートするときは、threads = 8 または 16 に設定することをお勧めします`threads`を調整したら、 **config**という名前のファイルを保存します。

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
> 楽観的トランザクション モデルを有効にすると (TiDB はデフォルトで悲観的トランザクション モードを使用します)、同時実行の競合が見つかったときに TiDB はトランザクションをロールバックします。1 から`tidb_disable_txn_auto_retry` `off`設定すると、トランザクションの競合が発生した後に自動再試行メカニズムがオンになり、トランザクションの競合エラーが原因で Sysbench が終了するのを防ぐことができます。

データをインポートする前に、TiDB にいくつかの設定を行う必要があります。MySQL クライアントで次のコマンドを実行します。

```sql
set global tidb_disable_txn_auto_retry = off;
```

次にクライアントを終了します。

MySQL クライアントを再起動し、次の SQL ステートメントを実行してデータベース`sbtest`を作成します。

```sql
create database sbtest;
```

Sysbench スクリプトがインデックスを作成する順序を調整します。Sysbench は、「テーブルの作成 -&gt; データの挿入 -&gt; インデックスの作成」の順序でデータをインポートするため、TiDB がデータをインポートするのに時間がかかります。ユーザーは順序を調整して、データのインポートを高速化できます。Sysbench バージョン[1.0.20](https://github.com/akopytov/sysbench/tree/1.0.20)を使用するとします。順序は、次の 2 つの方法のいずれかで調整できます。

-   TiDB 用に変更された[oltp_common.lua](https://raw.githubusercontent.com/pingcap/tidb-bench/master/sysbench/sysbench-patch/oltp_common.lua)ファイルをダウンロードし、 `/usr/share/sysbench/oltp_common.lua`ファイルを上書きします。
-   `/usr/share/sysbench/oltp_common.lua`で、行[235-240](https://github.com/akopytov/sysbench/blob/1.0.20/src/lua/oltp_common.lua#L235-L240)行 198 のすぐ後ろに移動します。

> **注記：**
>
> この操作はオプションであり、データのインポートにかかる時間を節約するためだけに行われます。

コマンド ラインで次のコマンドを入力して、データのインポートを開始します。構成ファイルは、前の手順で構成されたものです。

```bash
sysbench --config-file=config oltp_point_select --tables=32 --table-size=10000000 prepare
```

### 温暖化データと統計の収集 {#warming-data-and-collecting-statistics}

データをウォームアップするには、ディスクからメモリのブロックキャッシュにデータをロードします。ウォームアップされたデータにより、システム全体のパフォーマンスが大幅に向上します。クラスターを再起動した後、一度データをウォームアップすることをお勧めします。

```bash
sysbench --config-file=config oltp_point_select --tables=32 --table-size=10000000 prewarm
```

### ポイント選択テストコマンド {#point-select-test-command}

```bash
sysbench --config-file=config oltp_point_select --tables=32 --table-size=10000000 --db-ps-mode=auto --rand-type=uniform run
```

### インデックステストコマンドの更新 {#update-index-test-command}

```bash
sysbench --config-file=config oltp_update_index --tables=32 --table-size=10000000 --db-ps-mode=auto --rand-type=uniform run
```

### 読み取り専用テストコマンド {#read-only-test-command}

```bash
sysbench --config-file=config oltp_read_only --tables=32 --table-size=10000000 --db-ps-mode=auto --rand-type=uniform run
```

## よくある問題 {#common-issues}

### TiDB と TiKV は両方とも高い同時実行性で適切に構成されているのに、全体的なパフォーマンスがまだ低いのはなぜですか? {#tidb-and-tikv-are-both-properly-configured-under-high-concurrency-why-is-the-overall-performance-still-low}

この問題は、多くの場合、プロキシの使用に関係しています。単一の TiDBサーバーに負荷をかけ、各結果を合計し、合計結果をプロキシを使用した結果と比較することができます。

HAproxy を例に挙げてみましょう。パラメータ`nbproc` 、最大で起動できるプロセスの数を増やすことができます。HAproxy の最新バージョンでは、 `nbthread`と`cpu-map`もサポートされています。これらすべてにより、プロキシの使用によるパフォーマンスへの悪影響を軽減できます。

### 同時実行性が高いにもかかわらず、TiKV の CPU 使用率が低いのはなぜですか? {#under-high-concurrency-why-is-the-cpu-utilization-rate-of-tikv-still-low}

TiKV 全体の CPU 使用率は低いですが、クラスター内の一部のモジュールの CPU 使用率は高くなる可能性があります。

storage読み取りプール、コプロセッサ、gRPC など、TiKV 上の他のモジュールの最大同時実行制限は、TiKV 構成ファイルを通じて調整できます。

実際の CPU 使用率は、Grafana の TiKV スレッド CPU モニター パネルで確認できます。モジュールにボトルネックがある場合は、モジュールの同時実行性を高めることで調整できます。

### TiKV は高同時実行性下で CPU 使用率のボトルネックにまだ達していないのに、なぜ TiDB の CPU 使用率がまだ低いのでしょうか? {#given-that-tikv-has-not-yet-reached-the-cpu-usage-bottleneck-under-high-concurrency-why-is-tidb-s-cpu-utilization-rate-still-low}

NUMAアーキテクチャの CPU は、リモートメモリへの CPU 間アクセスによってパフォーマンスが大幅に低下する一部のハイエンド機器で使用されます。デフォルトでは、TiDB はサーバーのすべての CPU を使用するため、goroutine スケジューリングによって必然的に CPU 間メモリアクセスが発生します。

したがって、NUMAアーキテクチャのサーバーに*n 個の*TiDB ( *n*は NUMA CPU の数) を展開し、同時に TiDB パラメータ`max-procs`を NUMA CPU コアの数と同じ値に設定することをお勧めします。
