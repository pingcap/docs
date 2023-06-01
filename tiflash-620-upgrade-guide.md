---
title: TiFlash v6.2 Upgrade Guide
summary: Learn the precautions when you upgrade TiFlash to v6.2.
---

# TiFlash v6.2 アップグレード ガイド {#tiflash-v6-2-upgrade-guide}

このドキュメントでは、 TiFlash を以前のバージョンから v6.2 にアップグレードするときに注意する必要があるTiFlashモジュールの機能変更と、推奨されるアクションについて説明します。

標準的なアップグレード プロセスについては、次のドキュメントを参照してください。

-   [<a href="/upgrade-tidb-using-tiup.md">TiUPを使用して TiDB をアップグレードする</a>](/upgrade-tidb-using-tiup.md)
-   [<a href="https://docs.pingcap.com/tidb-in-kubernetes/stable/upgrade-a-tidb-cluster">Kubernetes で TiDB をアップグレードする</a>](https://docs.pingcap.com/tidb-in-kubernetes/stable/upgrade-a-tidb-cluster)

> **ノート：**
>
> -   [<a href="/tiflash/use-fastscan.md">ファストスキャン</a>](/tiflash/use-fastscan.md)は実験的機能として v6.2.0 に導入され、v7.0.0 で一般利用可能 (GA) になります。強力なデータ一貫性を犠牲にして、より効率的なクエリ パフォーマンスを提供します。
>
> -   TiFlashを含む TiDB をメジャー バージョン間で (たとえば、v4.x から v6.x に) アップグレードすることはお勧めできません。代わりに、まず v4.x から v5.x にアップグレードし、次に v6.x にアップグレードする必要があります。
>
> -   v4.x はライフサイクルの終わりに近づいています。できるだけ早く v5.x 以降にアップグレードすることをお勧めします。詳細については、 [<a href="https://en.pingcap.com/tidb-release-support-policy/">TiDB リリース サポート ポリシー</a>](https://en.pingcap.com/tidb-release-support-policy/)を参照してください。
>
> -   PingCAP は、v6.0 などの非 LTS バージョンのバグ修正を提供しません。可能な限り、v6.1 以降の LTS バージョンにアップグレードすることをお勧めします。
>
> -   TiFlash をv5.3.0 より前のバージョンから v5.3.0 以降にアップグレードするには、 TiFlashを停止してからアップグレードする必要があります。次の手順は、他のコンポーネントを中断せずにTiFlashをアップグレードするのに役立ちます。
>
>     -   TiFlashインスタンスを停止します: `tiup cluster stop <cluster-name> -R tiflash`
>     -   TiDB クラスターを再起動せずにアップグレードします (ファイルの更新のみ): `tiup cluster upgrade <cluster-name> <version> --offline` (例: `tiup cluster upgrade <cluster-name> v5.3.0 --offline`
>     -   TiDB クラスターをリロードします。 `tiup cluster reload <cluster-name>` .リロード後、 TiFlashインスタンスが開始されるため、手動で開始する必要はありません。

## 5.x または v6.0 から v6.1 {#from-5-x-or-v6-0-to-v6-1}

TiFlash をv5.x または v6.0 から v6.1 にアップグレードする場合は、 TiFlashプロキシと動的プルーニングの機能変更に注意してください。

### TiFlashプロキシ {#tiflash-proxy}

TiFlashプロキシは v6.1.0 でアップグレードされます (TiKV v6.0.0 と連携)。新しいバージョンでは、RocksDB のバージョンがアップグレードされました。 TiFlash をv6.1 にアップグレードすると、データ形式が新しいバージョンに自動的に変換されます。

通常のアップグレードでは、データ変換にリスクは伴いません。ただし、特別なシナリオ (テストまたは検証シナリオなど) でTiFlash をv6.1 から以前のバージョンにダウングレードする必要がある場合、以前のバージョンでは新しい RocksDB 構成の解析に失敗する可能性があります。その結果、 TiFlash は再起動できなくなります。アップグレード プロセスを十分にテストおよび検証し、緊急時の計画を準備することをお勧めします。

**テストまたはその他の特別なシナリオでTiFlashをダウングレードするための回避策**

ターゲットTiFlashノードを強制的にスケールインしてから、TiKV からデータを再度レプリケートできます。詳細な手順については、 [<a href="/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster">TiFlashクラスターでのスケールイン</a>](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster)を参照してください。

### 動的枝刈り {#dynamic-pruning}

[<a href="/partitioned-table.md#dynamic-pruning-mode">動的プルーニングモード</a>](/partitioned-table.md#dynamic-pruning-mode)有効にせず、今後も使用しない場合は、このセクションをスキップできます。

-   新しくインストールされた TiDB v6.1.0: 動的プルーニングはデフォルトで有効になっています。

-   TiDB v6.0 以前: 動的プルーニングはデフォルトで無効になっています。アップグレード後の動的プルーニングの設定は、以前のバージョンの設定を継承します。つまり、動的プルーニングはアップグレード後に自動的に有効 (または無効) になりません。

    アップグレード後、動的プルーニングを有効にするには、 `tidb_partition_prune_mode`から`dynamic`を設定し、パーティション化されたテーブルの GlobalStats を手動で更新します。詳細は[<a href="/partitioned-table.md#dynamic-pruning-mode">動的プルーニングモード</a>](/partitioned-table.md#dynamic-pruning-mode)を参照してください。

## v5.x または v6.0 から v6.2 へ {#from-v5-x-or-v6-0-to-v6-2}

TiDB v6.2 では、 TiFlashのデータstorage形式が V3 バージョンにアップグレードされます。したがって、 TiFlash をv5.x または v6.0 から v6.2 にアップグレードする場合は、 [<a href="#tiflash-proxy">TiFlashプロキシ</a>](#tiflash-proxy)と[<a href="#dynamic-pruning">動的枝刈り</a>](#dynamic-pruning)の機能変更に加えて、PageStorage の機能変更にも注意する必要があります。

### ページストレージ {#pagestorage}

デフォルトでは、 TiFlash v6.2.0 は PageStorage V3 バージョン[<a href="/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file">`format_version = 4`</a>](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)を使用します。この新しいデータ形式により、ピーク時の書き込み I/O トラフィックが大幅に削減されます。更新トラフィックが多く、同時実行性が高い、またはクエリが重いシナリオでは、 TiFlashデータ GC によって引き起こされる過剰な CPU 使用率を効果的に軽減します。一方、以前のstorage形式と比較して、V3 バージョンではスペースの拡大とリソースの消費が大幅に削減されます。

-   v6.2.0 へのアップグレード後、新しいデータが既存のTiFlashノードに書き込まれるため、以前のデータは徐々に新しい形式に変換されます。
-   ただし、変換には一定量のシステム オーバーヘッドが消費されるため、アップグレード中に以前のデータを新しい形式に完全に変換することはできません (サービスには影響しませんが、注意が必要です)。アップグレード後、 [<a href="/sql-statements/sql-statement-alter-table-compact.md">`Compact`コマンド</a>](/sql-statements/sql-statement-alter-table-compact.md)を実行してデータを新しい形式に変換することをお勧めします。手順は次のとおりです。

    1.  TiFlashレプリカを含むテーブルごとに次のコマンドを実行します。

        ```sql
        ALTER TABLE <table_name> COMPACT tiflash replica;
        ```

    2.  TiFlashノードを再起動します。

Grafana でテーブルが古いデータ形式をまだ使用しているかどうかを確認できます: **TiFlash- Summary** &gt; **Storage Pool** &gt; **Storage Pool Run Mode** 。

-   V2 のみ: PageStorage V2 を使用するテーブルの数 (パーティションを含む)
-   V3 のみ: PageStorage V3 を使用するテーブルの数 (パーティションを含む)
-   混合モード: PageStorage V2 から PageStorage V3 に変換されたデータ形式のテーブルの数 (パーティションを含む)

**テストまたはその他の特別なシナリオでTiFlashをダウングレードするための回避策**

ターゲットTiFlashノードを強制的にスケールインしてから、TiKV からデータを再度レプリケートできます。詳細な手順については、 [<a href="/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster">TiFlashクラスターでのスケールイン</a>](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster)を参照してください。

## v6.1からv6.2へ {#from-v6-1-to-v6-2}

TiFlash をv6.1 から v6.2 にアップグレードする場合は、データstorage形式の変更に注意してください。詳細は[<a href="#pagestorage">ページストレージ</a>](#pagestorage)を参照してください。
