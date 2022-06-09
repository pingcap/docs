---
title: How to Test TiDB Using Sysbench
---

# Sysbenchを使用してTiDBをテストする方法 {#how-to-test-tidb-using-sysbench}

Sysbench1.0以降を使用することをお勧めします。これは[ここからダウンロード](https://github.com/akopytov/sysbench/releases/tag/1.0.14)にすることができます。

## テスト計画 {#test-plan}

### TiDB構成 {#tidb-configuration}

ログレベルが高いほど、印刷されるログが少なくなるため、TiDBのパフォーマンスにプラスの影響を与えます。 TiDB構成で`prepared plan cache`を有効にすると、実行プランの最適化のコストが削減されます。具体的には、TiUP構成ファイルに次のコマンドを追加できます。

```yaml
server_configs:
  tidb:
    log.level: "error"
    prepared-plan-cache.enabled: true
```

### TiKV構成 {#tikv-configuration}

ログレベルが高いほど、TiKVのパフォーマンスも向上します。

TiKVクラスタには複数の列ファミリーがあり、主にデフォルトCF、書き込みCF、ロックCFなどのさまざまなタイプのデータを格納するために使用されます。 Sysbenchテストでは、デフォルトCFと書き込みCFにのみ焦点を当てる必要があります。データのインポートに使用される列ファミリーは、TiDBクラスター間で一定の割合を占めています。

デフォルトCF：書き込みCF = 4：1

TiKVでのRocksDBのブロックキャッシュの構成は、メモリを最大限に活用するために、マシンのメモリサイズに基づいている必要があります。 TiKVクラスタを40GBの仮想マシンにデプロイするには、ブロックキャッシュを次のように構成することをお勧めします。

```yaml
server_configs:
  tikv:
    log-level: "error"
    rocksdb.defaultcf.block-cache-size: "24GB"
    rocksdb.writecf.block-cache-size: "6GB"
```

ブロックキャッシュを共有するようにTiKVを構成することもできます。

```yaml
server_configs:
  tikv:
    storage.block-cache.capacity: "30GB"
```

TiKVパフォーマンスチューニングの詳細については、 [TiKVパフォーマンスを調整する](/tune-tikv-memory-performance.md)を参照してください。

## テストプロセス {#test-process}

> **ノート：**
>
> このドキュメントのテストは、HAproxyなどの負荷分散ツールを使用せずに実行されました。個々のTiDBノードでSysbenchテストを実行し、結果を追加しました。負荷分散ツールとさまざまなバージョンのパラメーターもパフォーマンスに影響を与える可能性があります。

### Sysbench構成 {#sysbench-configuration}

これは、Sysbench構成ファイルの例です。

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

上記のパラメータは、実際のニーズに応じて調整できます。このうち、 `TIDB_HOST`はTiDBサーバーのIPアドレス（構成ファイルに複数のアドレスを含めることができないため）、 `threads`はテストの同時接続数であり、「8、16、32、64、 128、256&quot;。データをインポートするときは、threads = 8または16に設定することをお勧めします`threads`を調整した後、 **config**という名前のファイルを保存します。

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
> 楽観的トランザクションモデルを有効にすると（TiDBはデフォルトで悲観的トランザクションモードを使用します）、同時実行の競合が検出されると、TiDBはトランザクションをロールバックします。 `tidb_disable_txn_auto_retry`から`off`に設定すると、トランザクションの競合が発生した後に自動再試行メカニズムがオンになります。これにより、トランザクションの競合エラーが原因でSysbenchが終了するのを防ぐことができます。

データをインポートする前に、TiDBにいくつかの設定を行う必要があります。 MySQLクライアントで次のコマンドを実行します。

{{< copyable "" >}}

```sql
set global tidb_disable_txn_auto_retry = off;
```

次に、クライアントを終了します。

MySQLクライアントを再起動し、次のSQLステートメントを実行してデータベースを作成します`sbtest` ：

{{< copyable "" >}}

```sql
create database sbtest;
```

Sysbenchスクリプトがインデックスを作成する順序を調整します。 Sysbenchは、「テーブルの作成-&gt;データの挿入-&gt;インデックスの作成」の順序でデータをインポートします。これにより、TiDBがデータをインポートするのに時間がかかります。ユーザーは、データのインポートを高速化するために順序を調整できます。 Sysbenchバージョン[1.0.14](https://github.com/akopytov/sysbench/tree/1.0.14)を使用するとします。次の2つの方法のいずれかで順序を調整できます。

-   TiDB用に変更された[oltp_common.lua](https://raw.githubusercontent.com/pingcap/tidb-bench/master/sysbench/sysbench-patch/oltp_common.lua)ファイルをダウンロードし、 `/usr/share/sysbench/oltp_common.lua`ファイルを上書きします。
-   `/usr/share/sysbench/oltp_common.lua`で、行[235](https://github.com/akopytov/sysbench/blob/1.0.14/src/lua/oltp_common.lua#L235)を行198のすぐ後ろに移動し[240](https://github.com/akopytov/sysbench/blob/1.0.14/src/lua/oltp_common.lua#L240) 。

> **ノート：**
>
> この操作はオプションであり、データのインポートにかかる時間を節約するためだけのものです。

コマンドラインで次のコマンドを入力して、データのインポートを開始します。構成ファイルは、前の手順で構成されたファイルです。

{{< copyable "" >}}

```bash
sysbench --config-file=config oltp_point_select --tables=32 --table-size=10000000 prepare
```

### データの温暖化と統計の収集 {#warming-data-and-collecting-statistics}

データをウォームアップするために、ディスクからメモリのブロックキャッシュにデータをロードします。ウォームされたデータにより、システムの全体的なパフォーマンスが大幅に向上しました。クラスタを再起動した後、一度データをウォームアップすることをお勧めします。

Sysbench 1.0.14はデータウォーミングを提供しないため、手動で実行する必要があります。 Sysbenchの新しいバージョンを使用している場合は、ツール自体に含まれているデータウォーミング機能を使用できます。

例として、Sysbenchのテーブルsbtest7を取り上げます。次のSQLを実行して、データをウォーミングアップします。

{{< copyable "" >}}

```sql
SELECT COUNT(pad) FROM sbtest7 USE INDEX (k_7);
```

統計を収集すると、オプティマイザーがより正確な実行プランを選択するのに役立ちます。 `analyze`コマンドを使用して、テーブルsbtestの統計を収集できます。各テーブルには統計が必要です。

{{< copyable "" >}}

```sql
ANALYZE TABLE sbtest7;
```

### ポイント選択テストコマンド {#point-select-test-command}

{{< copyable "" >}}

```bash
sysbench --config-file=config oltp_point_select --tables=32 --table-size=10000000 run
```

### インデックステストコマンドの更新 {#update-index-test-command}

{{< copyable "" >}}

```bash
sysbench --config-file=config oltp_update_index --tables=32 --table-size=10000000 run
```

### 読み取り専用のテストコマンド {#read-only-test-command}

{{< copyable "" >}}

```bash
sysbench --config-file=config oltp_read_only --tables=32 --table-size=10000000 run
```

## 一般的な問題 {#common-issues}

### TiDBとTiKVはどちらも高い同時実行性の下で適切に構成されていますが、全体的なパフォーマンスがまだ低いのはなぜですか？ {#tidb-and-tikv-are-both-properly-configured-under-high-concurrency-why-is-the-overall-performance-still-low}

この問題は、多くの場合、プロキシの使用に関係しています。単一のTiDBサーバーにプレッシャーを加え、各結果を合計し、合計した結果をプロキシを使用した結果と比較できます。

例としてHAproxyを取り上げます。パラメータ`nbproc`は、最大で開始できるプロセスの数を増やすことができます。それ以降のバージョンのHAproxyも`nbthread`と`cpu-map`をサポートしています。これらはすべて、プロキシの使用によるパフォーマンスへの悪影響を軽減できます。

### 同時実行性が高いのに、なぜTiKVのCPU使用率がまだ低いのですか？ {#under-high-concurrency-why-is-the-cpu-utilization-rate-of-tikv-still-low}

TiKVの全体的なCPU使用率は低くなりますが、クラスタの一部のモジュールのCPU使用率は高くなる可能性があります。

ストレージリードプール、コプロセッサー、gRPCなど、TiKV上の他のモジュールの最大同時実行制限は、TiKV構成ファイルを介して調整できます。

実際のCPU使用率は、GrafanaのTiKVスレッドCPUモニターパネルで確認できます。モジュールにボトルネックがある場合は、モジュールの同時実行性を増やすことで調整できます。

### TiKVが高い同時実行性の下でCPU使用率のボトルネックにまだ達していないことを考えると、なぜTiDBのCPU使用率はまだ低いのですか？ {#given-that-tikv-has-not-yet-reached-the-cpu-usage-bottleneck-under-high-concurrency-why-is-tidb-s-cpu-utilization-rate-still-low}

NUMAアーキテクチャのCPUは、リモートメモリへのクロスCPUアクセスによってパフォーマンスが大幅に低下する一部のハイエンド機器で使用されます。デフォルトでは、TiDBはサーバーのすべてのCPUを使用し、定期的なスケジューリングは必然的にクロスCPUメモリアクセスにつながります。

したがって、NUMAアーキテクチャのサーバーに*n個のTiDB（n*<em>は</em>NUMA CPUの数）をデプロイすることをお勧めします。その間、TiDBパラメーター`max-procs`をNUMACPUコアの数と同じ値に設定します。
