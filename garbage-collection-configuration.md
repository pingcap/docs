---
title: Garbage Collection Configuration
summary: Learn about GC configuration parameters.
---

# ガベージコレクションのConfiguration / コンフィグレーション {#garbage-collection-configuration}

ガベージコレクションは、次のシステム変数を介して構成されます。

-   [`tidb_gc_enable`](/system-variables.md#tidb_gc_enable-new-in-v50)
-   [`tidb_gc_run_interval`](/system-variables.md#tidb_gc_run_interval-new-in-v50)
-   [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)
-   [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50)
-   [`tidb_gc_scan_lock_mode`](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50)
-   [`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)

## GC I/O制限 {#gc-i-o-limit}

TiKVはGCI/O制限をサポートします。 `gc.max-write-bytes-per-sec`を設定して、1秒あたりのGCワーカーの書き込みを制限し、通常のリクエストへの影響を減らすことができます。

`0`は、この機能を無効にすることを示します。

tikv-ctlを使用して、この構成を動的に変更できます。

{{< copyable "" >}}

```bash
tikv-ctl --host=ip:port modify-tikv-config -n gc.max-write-bytes-per-sec -v 10MB
```

## TiDB5.0での変更 {#changes-in-tidb-5-0}

TiDBの以前のリリースでは、ガベージコレクションは`mysql.tidb`のシステムテーブルを介して構成されていました。このテーブルへの変更は引き続きサポートされますが、提供されているシステム変数を使用することをお勧めします。これにより、構成への変更を確実に検証し、予期しない動作を防ぐことができます（ [＃20655](https://github.com/pingcap/tidb/issues/20655) ）。

`CENTRAL`ガベージコレクションモードはサポートされなくなりました。 `DISTRIBUTED` GCモード（TiDB 3.0以降のデフォルト）が代わりに自動的に使用されます。 TiDBがガベージコレクションをトリガーするために各TiKVリージョンにリクエストを送信する必要がなくなるため、このモードはより効率的です。

以前のリリースでの変更点については、左側のメニューの*TIDBバージョンセレクター*を使用して、このドキュメントの以前のバージョンを参照してください。

## TiDB6.1.0での変更 {#changes-in-tidb-6-1-0}

TiDB v6.1.0より前では、TiDBのトランザクションはGCセーフポイントに影響を与えません。 v6.1.0以降、TiDBは、アクセスされるデータがクリアされたという問題を解決するために、GCセーフポイントを計算するときにトランザクションのstartTSを考慮します。トランザクションが長すぎると、セーフポイントが長時間ブロックされ、アプリケーションのパフォーマンスに影響します。

TiDB v6.1.0では、システム変数[`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)が導入され、アクティブなトランザクションがGCセーフポイントをブロックする最大時間を制御します。値を超えると、GCセーフポイントが強制的に転送されます。

### コンパクションフィルターのGC {#gc-in-compaction-filter}

`DISTRIBUTED` GCモードに基づいて、圧縮フィルターのGCのメカニズムは、個別のGCワーカースレッドではなく、RocksDBの圧縮プロセスを使用してGCを実行します。この新しいGCメカニズムは、GCによって引き起こされる余分なディスク読み取りを回避するのに役立ちます。また、廃止されたデータをクリアした後、シーケンシャルスキャンのパフォーマンスを低下させる多数の左のトゥームストーンマークを回避します。次の例は、TiKV構成ファイルでメカニズムを有効にする方法を示しています。

{{< copyable "" >}}

```toml
[gc]
enable-compaction-filter = true
```

オンラインで構成を変更することにより、このGCメカニズムを有効にすることもできます。次の例を参照してください。

{{< copyable "" >}}

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

{{< copyable "" >}}

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
