---
title: TiFlash Upgrade Guide
summary: Learn the precautions when you upgrade TiFlash.
aliases: ['/tidb/stable/tiflash-620-upgrade-guide']
---

# TiFlashアップグレード ガイド {#tiflash-upgrade-guide}

このドキュメントでは、 TiFlashをアップグレードする際に知っておく必要がある機能の変更点と推奨されるアクションについて説明します。

標準的なアップグレード プロセスについては、次のドキュメントを参照してください。

-   [TiUPを使用して TiDB をアップグレードする](/upgrade-tidb-using-tiup.md)
-   [Kubernetes で TiDB をアップグレードする](https://docs.pingcap.com/tidb-in-kubernetes/stable/upgrade-a-tidb-cluster)

> **注記：**
>
> -   [ファストスキャン](/tiflash/use-fastscan.md)は実験的機能として v6.2.0 に導入され、v7.0.0 で一般提供 (GA) になります。強力なデータ一貫性を犠牲にして、より効率的なクエリ パフォーマンスを提供します。
>
> -   TiFlashを含む TiDB をメジャー バージョン間で (たとえば、v4.x から v6.x に) アップグレードすることはお勧めできません。代わりに、まず v4.x から v5.x にアップグレードし、次に v6.x にアップグレードする必要があります。
>
> -   v4.x はライフサイクルの終わりに近づいています。できるだけ早く v5.x 以降にアップグレードすることをお勧めします。詳細については、 [TiDB リリース サポート ポリシー](https://en.pingcap.com/tidb-release-support-policy/)を参照してください。
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

ターゲットTiFlashノードを強制的にスケールインしてから、TiKV からデータを再度レプリケートできます。詳細な手順については、 [TiFlashクラスターでのスケールイン](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster)を参照してください。

### 動的枝刈り {#dynamic-pruning}

[動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode)有効にせず、今後も使用しない場合は、このセクションをスキップしてください。

-   新しくインストールされた TiDB v6.1.0: 動的プルーニングはデフォルトで有効になっています。

-   TiDB v6.0 以前: 動的プルーニングはデフォルトで無効になっています。アップグレード後の動的プルーニングの設定は、以前のバージョンの設定を継承します。つまり、動的プルーニングはアップグレード後に自動的に有効 (または無効) になりません。

    アップグレード後、動的プルーニングを有効にするには、 `tidb_partition_prune_mode`から`dynamic`を設定し、パーティション化されたテーブルの GlobalStats を手動で更新します。詳細は[動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode)を参照してください。

## v5.x または v6.0 から v6.2 へ {#from-v5-x-or-v6-0-to-v6-2}

TiDB v6.2 では、 TiFlashのデータstorage形式が V3 バージョンにアップグレードされます。したがって、 TiFlash をv5.x または v6.0 から v6.2 にアップグレードする場合は、 [TiFlashプロキシ](#tiflash-proxy)と[動的枝刈り](#dynamic-pruning)の機能変更に加えて、PageStorage の機能変更にも注意する必要があります。

### ページストレージ {#pagestorage}

デフォルトでは、 TiFlash v6.2.0 は PageStorage V3 バージョン[`format_version = 4`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)を使用します。この新しいデータ形式により、ピーク時の書き込み I/O トラフィックが大幅に削減されます。更新トラフィックが多く、同時実行性が高い、またはクエリが重いシナリオでは、 TiFlashデータ GC によって引き起こされる過剰な CPU 使用率を効果的に軽減します。一方、以前のstorage形式と比較して、V3 バージョンではスペースの拡大とリソースの消費が大幅に削減されます。

-   v6.2.0 へのアップグレード後、新しいデータが既存のTiFlashノードに書き込まれるため、以前のデータは徐々に新しい形式に変換されます。
-   ただし、変換には一定量のシステム オーバーヘッドが消費されるため、アップグレード中に以前のデータを新しい形式に完全に変換することはできません (サービスには影響しませんが、注意が必要です)。アップグレード後、 [`Compact`コマンド](/sql-statements/sql-statement-alter-table-compact.md)を実行してデータを新しい形式に変換することをお勧めします。手順は次のとおりです。

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

ターゲットTiFlashノードを強制的にスケールインしてから、TiKV からデータを再度レプリケートできます。詳細な手順については、 [TiFlashクラスターでのスケールイン](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster)を参照してください。

## v6.1からv6.2へ {#from-v6-1-to-v6-2}

TiFlash をv6.1 から v6.2 にアップグレードする場合は、データstorage形式の変更に注意してください。詳細は[ページストレージ](#pagestorage)を参照してください。

## <code>storage.format_version = 5</code>が構成された v6.x または v7.x から v7.3 へ {#from-v6-x-or-v7-x-to-v7-3-with-code-storage-format-version-5-code-configured}

v7.3 以降、 TiFlash には新しい DTFile バージョン、DTFile V3 (実験的) が導入されています。この新しい DTFile バージョンでは、複数の小さなファイルを 1 つの大きなファイルにマージして、ファイルの総数を減らすことができます。 v7.3 では、デフォルトの DTFile バージョンは依然として V2 です。 V3 を使用するには、 [TiFlash設定パラメータ](/tiflash/tiflash-configuration.md) `storage.format_version = 5`を設定できます。設定後も、 TiFlash は引き続き V2 DTFile を読み取ることができ、その後のデータ圧縮中に既存の V2 DTFile を V3 DTFile に徐々に書き換えます。

TiFlashを v7.3 にアップグレードし、V3 DTFile を使用するようにTiFlashを構成した後、 TiFlash を以前のバージョンに戻す必要がある場合は、DTTool をオフラインで使用して、V3 DTFile を V2 DTFile に書き戻すことができます。詳細については、 [DTTool 移行ツール](/tiflash/tiflash-command-line-flags.md#dttool-migrate)を参照してください。

## v6.x または v7.x から v7.4 以降のバージョン {#from-v6-x-or-v7-x-to-v7-4-or-a-later-version}

v7.4 以降、データ圧縮中に生成される読み取りおよび書き込みの増幅を軽減するために、 TiFlash はPageStorage V3 のデータ圧縮ロジックを最適化します。これにより、基になるstorageファイル名の一部が変更されます。したがって、v7.4 以降のバージョンにアップグレードした後は、元のバージョンへのインプレース ダウングレードはサポートされません。

**テストまたはその他の特別なシナリオでTiFlashをダウングレードするための回避策**

テストまたはその他の特殊なシナリオでTiFlash をダウングレードするには、ターゲットTiFlashノードを強制的にスケールインしてから、TiKV からデータを再度レプリケートします。詳細な手順については、 [TiFlashクラスターでのスケールイン](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster)を参照してください。
