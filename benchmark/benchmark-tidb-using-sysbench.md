---
title: How to Test TiDB Using Sysbench
---

# Sysbench を使用して TiDB をテストする方法 {#how-to-test-tidb-using-sysbench}

[ここからダウンロード](https://github.com/akopytov/sysbench/releases/tag/1.0.20)にすることができる Sysbench 1.0 以降を使用することをお勧めします。

## テスト計画 {#test-plan}

### TiDB 構成 {#tidb-configuration}

ログレベルが高いほど、印刷されるログが少なくなるため、TiDB のパフォーマンスにプラスの影響を与えます。具体的には、 TiUP構成ファイルに次のコマンドを追加できます。

```yaml
server_configs:
  tidb:
    log.level: "error"
```

また[`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)が有効になっていることを確認し、 `--db-ps-mode=disabled`使用せ*ず*に sysbench が準備済みステートメントを使用できるようにすることもお勧めします。 SQL プラン キャッシュの機能とその監視方法に関するドキュメントについては、 [SQL 準備済み実行計画キャッシュ](/sql-prepared-plan-cache.md)を参照してください。

### TiKV構成 {#tikv-configuration}

ログレベルが高いほど、TiKV のパフォーマンスも向上します。

TiKV クラスターには複数のカラムファミリーがあり、主にデフォルト CF、書き込み CF、ロック CF など、さまざまな種類のデータを格納するために使用されます。 Sysbench テストでは、Default CF と Write CF のみに注目する必要があります。データのインポートに使用されるカラムファミリーは、TiDB クラスター間で一定の割合を持っています。

デフォルト CF : 書き込み CF = 4 : 1

TiKV 上の RocksDB のブロックキャッシュの構成は、メモリを最大限に活用するために、マシンのメモリサイズに基づいている必要があります。 40 GB の仮想マシンに TiKV クラスターをデプロイするには、次のようにブロックキャッシュを構成することをお勧めします。

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

## 試験工程 {#test-process}

> **ノート：**
>
> このドキュメントのテストは、HAproxy などの負荷分散ツールを使用せずに実行されました。個々の TiDB ノードで Sysbench テストを実行し、結果を追加しました。異なるバージョンの負荷分散ツールとパラメーターも、パフォーマンスに影響を与える可能性があります。

### シスベンチ構成 {#sysbench-configuration}

これは、Sysbench 構成ファイルの例です。

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

上記のパラメータは、実際のニーズに応じて調整できます。その中で、 `TIDB_HOST`は TiDBサーバーの IP アドレス (構成ファイルに複数のアドレスを含めることができないため)、 `threads`はテストでの同時接続数で、「8、16、32、64、 128、256」。データをインポートするときは、threads = 8 または 16 に設定することをお勧めします`threads`を調整したら、 **config**という名前のファイルを保存します。

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

### データのインポート {#data-import}

> **ノート：**
>
> 楽観的トランザクション モデルを有効にすると (TiDB はデフォルトで悲観的トランザクション モードを使用します)、TiDB は同時実行の競合が見つかったときにトランザクションをロールバックします。 `tidb_disable_txn_auto_retry`から`off`に設定すると、トランザクション競合が発生した後に自動再試行メカニズムがオンになり、トランザクション競合エラーが原因で Sysbench が終了するのを防ぐことができます。

データをインポートする前に、TiDB にいくつかの設定を行う必要があります。 MySQL クライアントで次のコマンドを実行します。

{{< copyable "" >}}

```sql
set global tidb_disable_txn_auto_retry = off;
```

次に、クライアントを終了します。

MySQL クライアントを再起動し、次の SQL ステートメントを実行してデータベースを作成します`sbtest` :

{{< copyable "" >}}

```sql
create database sbtest;
```

Sysbench スクリプトがインデックスを作成する順序を調整します。 Sysbench は「テーブルの作成 -&gt; データの挿入 -&gt; インデックスの作成」の順序でデータをインポートしますが、TiDB がデータをインポートするのにより多くの時間がかかります。ユーザーは順序を調整して、データのインポートを高速化できます。 Sysbench バージョン[1.0.20](https://github.com/akopytov/sysbench/tree/1.0.20)を使用するとします。次の 2 つの方法のいずれかで順序を調整できます。

-   TiDB 用に変更された[oltp_common.lua](https://raw.githubusercontent.com/pingcap/tidb-bench/master/sysbench/sysbench-patch/oltp_common.lua)ファイルをダウンロードし、 `/usr/share/sysbench/oltp_common.lua`ファイルを上書きします。
-   `/usr/share/sysbench/oltp_common.lua`で、ライン[235-240](https://github.com/akopytov/sysbench/blob/1.0.20/src/lua/oltp_common.lua#L235-L240)をライン 198 のすぐ後ろに移動します。

> **ノート：**
>
> この操作はオプションであり、データのインポートにかかる時間を節約するためだけのものです。

コマンド ラインで次のコマンドを入力して、データのインポートを開始します。構成ファイルは、前の手順で構成されたものです。

{{< copyable "" >}}

```bash
sysbench --config-file=config oltp_point_select --tables=32 --table-size=10000000 prepare
```

### 温暖化データと統計収集 {#warming-data-and-collecting-statistics}

データをウォームアップするには、ディスクからメモリのブロックキャッシュにデータを読み込みます。ウォーミングされたデータにより、システムの全体的なパフォーマンスが大幅に向上しました。クラスタを再起動した後、データを 1 回ウォームアップすることをお勧めします。

```bash
sysbench --config-file=config oltp_point_select --tables=32 --table-size=10000000 warmup
```

### ポイントセレクトテストコマンド {#point-select-test-command}

{{< copyable "" >}}

```bash
sysbench --config-file=config oltp_point_select --tables=32 --table-size=10000000 run
```

### 更新インデックス テスト コマンド {#update-index-test-command}

{{< copyable "" >}}

```bash
sysbench --config-file=config oltp_update_index --tables=32 --table-size=10000000 run
```

### 読み取り専用テスト コマンド {#read-only-test-command}

{{< copyable "" >}}

```bash
sysbench --config-file=config oltp_read_only --tables=32 --table-size=10000000 run
```

## 一般的な問題 {#common-issues}

### TiDB と TiKV はどちらも高い同時実行性の下で適切に構成されていますが、全体的なパフォーマンスがまだ低いのはなぜですか? {#tidb-and-tikv-are-both-properly-configured-under-high-concurrency-why-is-the-overall-performance-still-low}

この問題は、多くの場合、プロキシの使用に関係しています。単一の TiDBサーバーに圧力を加え、各結果を合計し、合計した結果をプロキシを使用した結果と比較できます。

例として HAproxy を取り上げます。パラメーター`nbproc`最大で開始できるプロセスの数を増やすことができます。 HAproxy の新しいバージョンでは、 `nbthread`および`cpu-map`もサポートされています。これらはすべて、プロキシの使用によるパフォーマンスへの悪影響を軽減できます。

### 高い並行性の下で、TiKV の CPU 使用率がまだ低いのはなぜですか? {#under-high-concurrency-why-is-the-cpu-utilization-rate-of-tikv-still-low}

TiKV の全体的な CPU 使用率は低いですが、クラスター内の一部のモジュールの CPU 使用率が高い場合があります。

storagereadpool、コプロセッサ、gRPC など、TiKV の他のモジュールの最大同時実行制限は、TiKV 構成ファイルを使用して調整できます。

実際の CPU 使用率は、Grafana の TiKV Thread CPU モニター パネルで確認できます。モジュールにボトルネックがある場合は、モジュールの同時実行性を高めることで調整できます。

### TiKV が高い並行性の下で CPU 使用率のボトルネックにまだ達していないことを考えると、TiDB の CPU 使用率がまだ低いのはなぜですか? {#given-that-tikv-has-not-yet-reached-the-cpu-usage-bottleneck-under-high-concurrency-why-is-tidb-s-cpu-utilization-rate-still-low}

NUMAアーキテクチャの CPU は、リモートメモリへのクロス CPU アクセスによってパフォーマンスが大幅に低下する一部のハイエンド機器で使用されます。デフォルトでは、TiDB はサーバーのすべての CPU を使用し、ゴルーチン スケジューリングは必然的にクロス CPUメモリアクセスにつながります。

したがって、NUMAアーキテクチャのサーバーに*n 個の*TiDB ( <em>n</em>は NUMA CPU の数) をデプロイし、TiDB パラメーター`max-procs`を NUMA CPU コアの数と同じ値に設定することをお勧めします。
