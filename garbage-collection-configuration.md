---
title: Garbage Collection Configuration
summary: Learn about GC configuration parameters.
---

# ガベージ コレクションのコンフィグレーション {#garbage-collection-configuration}

ガベージ コレクションは、次のシステム変数を介して構成されます。

-   [`tidb_gc_enable`](/system-variables.md#tidb_gc_enable-new-in-v50)
-   [`tidb_gc_run_interval`](/system-variables.md#tidb_gc_run_interval-new-in-v50)
-   [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)
-   [`tidb_gc_concurrency`](/system-variables.md#tidb_gc_concurrency-new-in-v50)
-   [`tidb_gc_scan_lock_mode`](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50)
-   [`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)

## GC I/O 制限 {#gc-i-o-limit}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> このセクションは、オンプレミスの TiDB にのみ適用されます。 TiDB Cloud にはデフォルトで GC I/O 制限がありません。

</CustomContent>

TiKV は GC I/O 制限をサポートしています。 1 を設定して`gc.max-write-bytes-per-sec`秒あたりの GC ワーカーの書き込みを制限し、通常のリクエストへの影響を減らすことができます。

`0` 、この機能を無効にすることを示します。

tikv-ctl を使用して、この構成を動的に変更できます。

{{< copyable "" >}}

```bash
tikv-ctl --host=ip:port modify-tikv-config -n gc.max-write-bytes-per-sec -v 10MB
```

## TiDB 5.0 の変更点 {#changes-in-tidb-5-0}

TiDB の以前のリリースでは、ガベージコレクションは`mysql.tidb`システム テーブルを介して構成されていました。この表への変更は引き続きサポートされますが、提供されているシステム変数を使用することをお勧めします。これにより、構成への変更を検証し、予期しない動作を防ぐことができます ( [#20655](https://github.com/pingcap/tidb/issues/20655) )。

`CENTRAL`ガベージコレクションモードはサポートされなくなりました。代わりに`DISTRIBUTED` GC モード (TiDB 3.0 以降のデフォルト) が自動的に使用されます。このモードは、TiDB がガベージコレクションをトリガーするために各 TiKV リージョンにリクエストを送信する必要がなくなるため、より効率的です。

以前のリリースでの変更点については、左側のメニューにある*TIDB バージョン セレクタ*を使用して、このドキュメントの以前のバージョンを参照してください。

## TiDB 6.1.0 の変更点 {#changes-in-tidb-6-1-0}

TiDB v6.1.0 より前では、TiDB のトランザクションは GC セーフ ポイントに影響しません。 v6.1.0以降、TiDBはGCセーフポイントの計算時にトランザクションのstartTSを考慮し、アクセス対象のデータがクリアされてしまう問題を解決しました。トランザクションが長すぎると、セーフ ポイントが長時間ブロックされ、アプリケーションのパフォーマンスに影響します。

TiDB v6.1.0 では、システム変数[`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)が導入され、アクティブなトランザクションが GC セーフ ポイントをブロックする最大時間を制御します。値を超えると、強制的に GC セーフ ポイントが転送されます。

### 圧縮フィルターでの GC {#gc-in-compaction-filter}

`DISTRIBUTED` GC モードに基づいて、Compaction Filter の GC のメカニズムは、別の GC ワーカー スレッドではなく、RocksDB の圧縮プロセスを使用して GC を実行します。この新しい GC メカニズムは、GC による余分なディスク読み取りを回避するのに役立ちます。また、古いデータを消去した後、シーケンシャル スキャンのパフォーマンスを低下させる多数の廃棄マークが残されることを回避します。

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> 次の TiKV 構成の変更例は、オンプレミスの TiDB にのみ適用されます。 TiDB Cloudでは、圧縮フィルターの GC のメカニズムがデフォルトで有効になっています。

</CustomContent>

次の例は、TiKV 構成ファイルでメカニズムを有効にする方法を示しています。

{{< copyable "" >}}

```toml
[gc]
enable-compaction-filter = true
```

構成を動的に変更することで、この GC メカニズムを有効にすることもできます。次の例を参照してください。

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
