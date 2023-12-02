---
title: How to Test TiDB Using Sysbench
---

# Sysbench を使用して TiDB をテストする方法 {#how-to-test-tidb-using-sysbench}

Sysbench 1.0 以降を使用することをお勧めします ( [ここからダウンロードされました](https://github.com/akopytov/sysbench/releases/tag/1.0.20)を使用できます)。

## テスト計画 {#test-plan}

### TiDB 構成 {#tidb-configuration}

ログ レベルが高いほど、印刷されるログが少なくなるため、TiDB のパフォーマンスにプラスの影響を与えます。具体的には、 TiUP構成ファイルに次のコマンドを追加できます。

```yaml
server_configs:
  tidb:
    log.level: "error"
```

また[`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)が有効になっていることを確認し、 `--db-ps-mode=auto`使用して sysbench がプリペアド ステートメントを使用できるようにすることもお勧めします。 SQL プラン キャッシュの機能とそれを監視する方法については、ドキュメント[SQL 準備済み実行プラン キャッシュ](/sql-prepared-plan-cache.md)を参照してください。

> **注記：**
>
> Sysbench のバージョンが異なると、デフォルト値の`db-ps-mode`が異なる場合があります。コマンド内で明示的に指定することを推奨します。

### TiKV 構成 {#tikv-configuration}

ログ レベルが高いほど、TiKV のパフォーマンスが向上することも意味します。

TiKV クラスターには複数のカラムファミリーがあり、主にデフォルト CF、書き込み CF、ロック CF など、さまざまな種類のデータを保存するために使用されます。 Sysbench テストでは、デフォルト CF と書き込み CF のみに注目する必要があります。データのインポートに使用されるカラムファミリーは、TiDB クラスター間で一定の割合を持ちます。

デフォルト CF : 書き込み CF = 4 : 1

メモリを最大限に活用するには、TiKV 上の RocksDB のブロックキャッシュをマシンのメモリサイズに基づいて構成する必要があります。 TiKV クラスターを 40 GB の仮想マシンにデプロイするには、次のようにブロックキャッシュを構成することをお勧めします。

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

TiKV パフォーマンス チューニングの詳細については、 [TiKV のパフォーマンスを調整する](/tune-tikv-memory-performance.md)を参照してください。

## テストプロセス {#test-process}

> **注記：**
>
> このドキュメントのテストは、HAproxy などの負荷分散ツールを使用せずに実行されました。個々の TiDB ノードで Sysbench テストを実行し、結果を合計しました。負荷分散ツールとさまざまなバージョンのパラメーターもパフォーマンスに影響を与える可能性があります。

### システムベンチ構成 {#sysbench-configuration}

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

上記のパラメータは、実際のニーズに応じて調整できます。このうち、 `TIDB_HOST`は TiDBサーバーの IP アドレス (構成ファイルに複数のアドレスを含めることはできないため)、 `threads`はテストでの同時接続数で、「8、16、32、64、 128、256インチ。データをインポートするときは、スレッド = 8 または 16 に設定することをお勧めします。 `threads`を調整した後、 **config**という名前のファイルを保存します。

サンプル**構成**ファイルとして以下を参照してください。

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

### データインポート {#data-import}

> **注記：**
>
> 楽観的トランザクション モデルを有効にすると (TiDB はデフォルトで悲観的トランザクション モードを使用します)、同時実行性の競合が見つかったときに TiDB はトランザクションをロールバックします。 `tidb_disable_txn_auto_retry`から`off`に設定すると、トランザクション競合が発生した後の自動再試行メカニズムがオンになり、トランザクション競合エラーによる Sysbench の終了を防ぐことができます。

データをインポートする前に、TiDB にいくつかの設定を行う必要があります。 MySQL クライアントで次のコマンドを実行します。

```sql
set global tidb_disable_txn_auto_retry = off;
```

その後、クライアントを終了します。

MySQL クライアントを再起動し、次の SQL ステートメントを実行してデータベース`sbtest`を作成します。

```sql
create database sbtest;
```

Sysbench スクリプトがインデックスを作成する順序を調整します。 Sysbench は「テーブルの構築 -&gt; データの挿入 -&gt; インデックスの作成」の順序でデータをインポートします。これにより、TiDB がデータをインポートするのに時間がかかります。ユーザーは順序を調整してデータのインポートを高速化できます。 Sysbench バージョン[1.0.20](https://github.com/akopytov/sysbench/tree/1.0.20)を使用するとします。次の 2 つの方法のいずれかで順序を調整できます。

-   TiDB 用に変更した[oltp_common.lua](https://raw.githubusercontent.com/pingcap/tidb-bench/master/sysbench/sysbench-patch/oltp_common.lua)ファイルをダウンロードし、そのファイルで`/usr/share/sysbench/oltp_common.lua`ファイルを上書きします。
-   `/usr/share/sysbench/oltp_common.lua`で、行[235-240](https://github.com/akopytov/sysbench/blob/1.0.20/src/lua/oltp_common.lua#L235-L240)行 198 のすぐ後ろに移動します。

> **注記：**
>
> この操作はオプションであり、データのインポートにかかる時間を節約することのみを目的としています。

コマンド ラインで次のコマンドを入力してデータのインポートを開始します。構成ファイルは、前の手順で構成されたものです。

```bash
sysbench --config-file=config oltp_point_select --tables=32 --table-size=10000000 prepare
```

### データのウォーミングと統計の収集 {#warming-data-and-collecting-statistics}

データをウォームアップするには、データをディスクからメモリのブロックキャッシュにロードします。ウォームアップされたデータにより、システム全体のパフォーマンスが大幅に向上しました。クラスターを再起動した後、データを一度ウォームアップすることをお勧めします。

```bash
sysbench --config-file=config oltp_point_select --tables=32 --table-size=10000000 prewarm
```

### 点選択テストコマンド {#point-select-test-command}

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

### TiDB と TiKV は両方とも高同時実行下で適切に構成されているのに、全体的なパフォーマンスが依然として低いのはなぜですか? {#tidb-and-tikv-are-both-properly-configured-under-high-concurrency-why-is-the-overall-performance-still-low}

この問題は多くの場合、プロキシの使用に関連しています。単一の TiDBサーバーに圧力を加え、それぞれの結果を合計し、合計した結果をプロキシを使用した結果と比較できます。

HAproxy を例に挙げます。パラメーター`nbproc` 、最大で開始できるプロセスの数を増やすことができます。 HAproxy の新しいバージョンでは`nbthread`および`cpu-map`もサポートされます。これらはすべて、プロキシの使用によるパフォーマンスへの悪影響を軽減できます。

### 高い同時実行性にもかかわらず、TiKV の CPU 使用率が依然として低いのはなぜですか? {#under-high-concurrency-why-is-the-cpu-utilization-rate-of-tikv-still-low}

TiKV の全体的な CPU 使用率は低くなりますが、クラスター内の一部のモジュールの CPU 使用率が高くなる可能性があります。

storage読み取りプール、コプロセッサ、gRPC など、TiKV 上の他のモジュールの最大同時実行制限は、TiKV 構成ファイルを通じて調整できます。

実際の CPU 使用率は、Grafana の TiKV スレッド CPU モニター パネルを通じて観察できます。モジュールにボトルネックがある場合は、モジュールの同時実行性を高めることで調整できます。

### TiKV が高同時実行下で CPU 使用率のボトルネックにまだ到達していないことを考えると、TiDB の CPU 使用率が依然として低いのはなぜでしょうか? {#given-that-tikv-has-not-yet-reached-the-cpu-usage-bottleneck-under-high-concurrency-why-is-tidb-s-cpu-utilization-rate-still-low}

NUMAアーキテクチャの CPU は一部のハイエンド機器で使用されており、リモートメモリへのクロス CPU アクセスによりパフォーマンスが大幅に低下します。デフォルトでは、TiDB はサーバーのすべての CPU を使用し、ゴルーチンのスケジューリングにより必然的にクロス CPUメモリアクセスが発生します。

したがって、NUMAアーキテクチャのサーバーに*n 個の*TiDB ( *n*は NUMA CPU の数) をデプロイし、同時に TiDB パラメータ`max-procs`を NUMA CPU コアの数と同じ値に設定することをお勧めします。
