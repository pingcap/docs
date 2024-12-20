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

## GC I/O 制限 {#gc-i-o-limit}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> このセクションは、TiDB Self-Managed にのみ適用されます。TiDB TiDB Cloud には、デフォルトでは GC I/O 制限がありません。

</CustomContent>

TiKV は GC I/O 制限をサポートしています。1 `gc.max-write-bytes-per-sec`設定すると、GC ワーカーの 1 秒あたりの書き込みを制限し、通常のリクエストへの影響を軽減できます。

`0`この機能を無効にすることを示します。

tikv-ctl を使用してこの構成を動的に変更できます。

```bash
tikv-ctl --host=ip:port modify-tikv-config -n gc.max-write-bytes-per-sec -v 10MB
```

## TiDB 5.0 の変更点 {#changes-in-tidb-5-0}

以前のリリースの TiDB では、ガベージコレクションは`mysql.tidb`システム テーブルを介して構成されていました。このテーブルへの変更は引き続きサポートされますが、提供されているシステム変数を使用することをお勧めします。これにより、構成の変更が検証され、予期しない動作を防ぐことができます ( [＃20655](https://github.com/pingcap/tidb/issues/20655) )。

`CENTRAL` GC モードはサポートされなくなりました。代わりに、 `DISTRIBUTED` GC モード (TiDB 3.0 以降のデフォルト) が自動的に使用されます。このモードは、TiDB がガベージコレクションをトリガーするために各 TiKV 領域に要求を送信する必要がなくなったため、より効率的です。

以前のリリースの変更点については、左側のメニューにある*TIDB バージョン セレクターを*使用して、このドキュメントの以前のバージョンを参照してください。

## TiDB 6.1.0 の変更点 {#changes-in-tidb-6-1-0}

TiDB v6.1.0 より前では、TiDB 内のトランザクションは GC セーフ ポイントに影響を与えませんでした。v6.1.0 以降では、TiDB は GC セーフ ポイントを計算するときにトランザクションの startTS を考慮し、アクセス対象のデータがクリアされている問題を解決します。トランザクションが長すぎると、セーフ ポイントが長時間ブロックされ、アプリケーションのパフォーマンスに影響します。

TiDB v6.1.0 では、アクティブなトランザクションが GC セーフ ポイントをブロックする最大時間を制御するシステム変数[`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)が導入されました。この値を超えると、GC セーフ ポイントは強制的に転送されます。

### 圧縮フィルターのGC {#gc-in-compaction-filter}

`DISTRIBUTED` GC モードに基づいて、Compaction Filter の GC のメカニズムは、別の GC ワーカー スレッドではなく、RocksDB の圧縮プロセスを使用して GC を実行します。この新しい GC メカニズムは、GC による余分なディスク読み取りを回避するのに役立ちます。また、古いデータをクリアした後、シーケンシャル スキャンのパフォーマンスを低下させる大量のトゥームストーン マークが残るのを回避します。

<CustomContent platform="tidb-cloud">

> **注記：**
>
> TiKV 構成を変更する次の例は、TiDB Self-Managed にのみ適用されます。TiDB TiDB Cloudの場合、Compaction Filter の GC メカニズムはデフォルトで有効になっています。

</CustomContent>

次の例は、TiKV 構成ファイルでメカニズムを有効にする方法を示しています。

```toml
[gc]
enable-compaction-filter = true
```

構成を動的に変更することで、この GC メカニズムを有効にすることもできます。次の例を参照してください。

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
