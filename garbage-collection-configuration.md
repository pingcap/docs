---
title: Garbage Collection Configuration
summary: GC 構成パラメータについて学習します。
---

# ガベージコレクションのコンフィグレーション {#garbage-collection-configuration}

次のシステム変数を使用してガベージコレクション(GC) を構成できます。

-   [`tidb_gc_enable`](/system-variables.md#tidb_gc_enable-new-in-v50) : TiKV のガベージコレクションを有効にするかどうかを制御します。
-   [`tidb_gc_run_interval`](/system-variables.md#tidb_gc_run_interval-new-in-v50) : GC 間隔を指定します。
-   [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) : 各 GC でデータが保持される時間制限を指定します。
-   [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50) : GC の[ロックを解決する](/garbage-collection-overview.md#resolve-locks)番目のステップのスレッド数を指定します。
-   [`tidb_gc_scan_lock_mode`](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50) : GC のロック解決ステップでロックをスキャンする方法を指定します。
-   [`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610) : アクティブなトランザクションが GC セーフ ポイントをブロックする最大時間を指定します。

システム変数の値を変更する方法の詳細については、 [システム変数](/system-variables.md)参照してください。

## GC I/O制限 {#gc-i-o-limit}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> このセクションは TiDB Self-Managed にのみ適用されます。TiDB TiDB Cloud には、デフォルトでは GC I/O 制限はありません。

</CustomContent>

TiKVはGC I/O制限をサポートしています。1 `gc.max-write-bytes-per-sec`設定すると、GCワーカーの1秒あたりの書き込み回数が制限され、通常のリクエストへの影響を軽減できます。

`0`この機能を無効にすることを示します。

tikv-ctl を使用してこの構成を動的に変更できます。

```bash
tikv-ctl --host=ip:port modify-tikv-config -n gc.max-write-bytes-per-sec -v 10MB
```

## TiDB 5.0 の変更点 {#changes-in-tidb-5-0}

TiDBの以前のリリースでは、ガベージコレクションは`mysql.tidb`システムテーブルを介して設定されていました。このテーブルへの変更は引き続きサポートされますが、提供されているシステム変数を使用することをお勧めします。これにより、設定の変更が確実に検証され、予期しない動作を防ぐことができます( [＃20655](https://github.com/pingcap/tidb/issues/20655) )。

`CENTRAL`ガベージコレクションはサポートされなくなりました。代わりに、TiDB 3.0以降のデフォルトである`DISTRIBUTED` GCモードが自動的に使用されます。このモードは、TiDBがガベージコレクションを開始するために各TiKVリージョンにリクエストを送信する必要がなくなるため、より効率的です。

以前のリリースの変更点については、左側のメニューにある*TIDB バージョン セレクター*を使用して、このドキュメントの以前のバージョンを参照してください。

## TiDB 6.1.0 の変更点 {#changes-in-tidb-6-1-0}

TiDB v6.1.0より前のバージョンでは、TiDBのトランザクションはGCセーフポイントに影響を与えませんでした。v6.1.0以降、TiDBはGCセーフポイントを計算する際にトランザクションの開始TSを考慮するようになりました。これにより、アクセス対象のデータがクリアされてしまうという問題が解決されます。トランザクションが長すぎると、セーフポイントが長時間ブロックされ、アプリケーションのパフォーマンスに影響を及ぼします。

TiDB v6.1.0では、アクティブなトランザクションがGCセーフポイントをブロックする最大時間を制御するためのシステム変数[`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)導入されました。この値を超えると、GCセーフポイントは強制的に転送されます。

### 圧縮フィルター内のGC {#gc-in-compaction-filter}

`DISTRIBUTED` GCモードをベースに、Compaction FilterのGCメカニズムは、独立したGCワーカースレッドではなく、RocksDBのコンパクションプロセスを利用してGCを実行します。この新しいGCメカニズムは、GCによる余分なディスク読み取りを回避します。また、古いデータをクリアした後、シーケンシャルスキャンのパフォーマンスを低下させる大量のトゥームストーンマークが残るのを防ぎます。

<CustomContent platform="tidb-cloud">

> **注記：**
>
> 以下のTiKV構成の変更例は、TiDB Self-Managedにのみ適用されます。TiDB TiDB Cloudでは、Compaction FilterのGCメカニズムがデフォルトで有効になっています。

</CustomContent>

次の例は、TiKV 構成ファイルでメカニズムを有効にする方法を示しています。

```toml
[gc]
enable-compaction-filter = true
```

このGCメカニズムは、設定を動的に変更することでも有効にできます。次の例をご覧ください。

```sql
show config where type = 'tikv' and name like '%enable-compaction-filter%';
```

```sql
+------+-------------------+-----------------------------+-------+
| Type | Instance          | Name                        | Value |
+------+-------------------+-----------------------------+-------+
| tikv | 172.16.5.37:20163 | gc.enable-compaction-filter | false |
| tikv | 172.16.5.36:20163 | gc.enable-compaction-filter | false |
| tikv | 172.16.5.35:20163 | gc.enable-compaction-filter | false |
+------+-------------------+-----------------------------+-------+
```

```sql
set config tikv gc.enable-compaction-filter = true;
show config where type = 'tikv' and name like '%enable-compaction-filter%';
```

```sql
+------+-------------------+-----------------------------+-------+
| Type | Instance          | Name                        | Value |
+------+-------------------+-----------------------------+-------+
| tikv | 172.16.5.37:20163 | gc.enable-compaction-filter | true  |
| tikv | 172.16.5.36:20163 | gc.enable-compaction-filter | true  |
| tikv | 172.16.5.35:20163 | gc.enable-compaction-filter | true  |
+------+-------------------+-----------------------------+-------+
```
