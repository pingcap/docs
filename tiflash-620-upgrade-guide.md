---
title: TiFlash v6.2 Upgrade Guide
summary: Learn the precautions when you upgrade TiFlash to v6.2.
---

# TiFlash v6.2 アップグレード ガイド {#tiflash-v6-2-upgrade-guide}

このドキュメントでは、 TiFlash を以前のバージョンから v6.2 にアップグレードする際に注意する必要があるTiFlashモジュールの機能変更と、推奨されるアクションについて説明します。

標準のアップグレード プロセスについては、次のドキュメントを参照してください。

-   [TiUPを使用して TiDB をアップグレードする](/upgrade-tidb-using-tiup.md)
-   [Kubernetes で TiDB をアップグレードする](https://docs.pingcap.com/tidb-in-kubernetes/stable/upgrade-a-tidb-cluster)

> **ノート：**
>
> -   v6.2.0, [ファストスキャン](/develop/dev-guide-use-fastscan.md)で導入された実験的機能は、強力なデータの一貫性を犠牲にして、より効率的なクエリ パフォーマンスを提供します。この機能の形式と使用法は、後続のバージョンで変更される可能性があることに注意してください。
>
> -   v4.x から v6.x など、メジャー バージョン間でTiFlashを含む TiDB をアップグレードすることはお勧めしません。代わりに、最初に v4.x から v5.x にアップグレードしてから v6.x にアップグレードする必要があります。
>
> -   v4.x はライフサイクルの終わりに近づいています。できるだけ早く v5.x 以降にアップグレードすることをお勧めします。詳細については、 [TiDB リリース サポート ポリシー](https://en.pingcap.com/tidb-release-support-policy/)を参照してください。
>
> -   PingCAP は、v6.0 などの非 LTS バージョンのバグ修正を提供しません。可能な限り、v6.1 以降の LTS バージョンにアップグレードすることをお勧めします。
>
> -   TiFlash をv5.3.0 より前のバージョンから v5.3.0 以降にアップグレードするには、 TiFlashを停止してからアップグレードする必要があります。次の手順は、他のコンポーネントを中断することなくTiFlashをアップグレードするのに役立ちます。
>
>     -   TiFlashインスタンスを停止します: `tiup cluster stop <cluster-name> -R tiflash`
>     -   再起動せずに TiDB クラスターをアップグレードします (ファイルの更新のみ): `tiup cluster upgrade <cluster-name> <version> --offline` 、 `tiup cluster upgrade <cluster-name> v5.3.0 --offline`など
>     -   TiDB クラスターをリロードします。 `tiup cluster reload <cluster-name>` .リロード後、 TiFlashインスタンスが開始されるため、手動で開始する必要はありません。

## 5.x または v6.0 から v6.1 へ {#from-5-x-or-v6-0-to-v6-1}

TiFlash をv5.x または v6.0 から v6.1 にアップグレードする場合は、 TiFlashプロキシと動的プルーニングの機能変更に注意してください。

### TiFlashプロキシ {#tiflash-proxy}

TiFlash Proxy は v6.1.0 でアップグレードされます (TiKV v6.0.0 に合わせて)。新しいバージョンは RocksDB のバージョンをアップグレードしました。 TiFlashを v6.1 にアップグレードすると、データ形式は自動的に新しいバージョンに変換されます。

通常のアップグレードでは、データ変換にリスクはありません。ただし、特別なシナリオ (テストまたは検証シナリオなど) でTiFlash をv6.1 から以前のバージョンにダウングレードする必要がある場合、以前のバージョンは新しい RocksDB 構成の解析に失敗する可能性があります。その結果、 TiFlash は再起動に失敗します。アップグレード プロセスを完全にテストおよび検証し、緊急計画を準備することをお勧めします。

**テストまたはその他の特別なシナリオでTiFlashをダウングレードするための回避策**

ターゲットのTiFlashノードを強制的にスケールインしてから、TiKV からデータを再度レプリケートできます。詳細な手順については、 [TiFlashクラスターのスケールイン](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster)を参照してください。

### 動的剪定 {#dynamic-pruning}

[動的プルーニング モード](/partitioned-table.md#dynamic-pruning-mode)有効にせず、今後も使用しない場合は、このセクションをスキップできます。

-   新しくインストールされた TiDB v6.1.0: 動的プルーニングはデフォルトで有効になっています。

-   TiDB v6.0 以前: 動的プルーニングはデフォルトで無効になっています。バージョンアップ後の動的枝刈りの設定は、旧バージョンの設定を引き継ぎます。つまり、動的プルーニングは、アップグレード後に自動的に有効化 (または無効化) されません。

    アップグレード後、動的プルーニングを有効にするには、 `tidb_partition_prune_mode`を`dynamic`に設定し、分割されたテーブルの GlobalStats を手動で更新します。詳細については、 [動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode)を参照してください。

## v5.x または v6.0 から v6.2 へ {#from-v5-x-or-v6-0-to-v6-2}

TiDB v6.2 では、 TiFlashのデータstorageフォーマットが V3 バージョンにアップグレードされます。したがって、 TiFlash をv5.x または v6.0 から v6.2 にアップグレードする場合、 [TiFlashプロキシ](#tiflash-proxy)と[動的剪定](#dynamic-pruning)の機能変更に加えて、PageStorage の機能変更にも注意する必要があります。

### ページストレージ {#pagestorage}

デフォルトでは、 TiFlash v6.2.0 は PageStorage V3 バージョン[`format_version = 4`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)を使用します。この新しいデータ形式により、ピーク時の書き込み I/O トラフィックが大幅に削減されます。更新トラフィックが多く、同時実行性が高い、またはクエリが重いシナリオでは、 TiFlashデータ GC によって引き起こされる過度の CPU 使用を効果的に軽減します。一方、以前のstorage形式と比較して、V3 バージョンでは、スペースの増幅とリソースの消費が大幅に削減されます。

-   v6.2.0 へのアップグレード後、新しいデータが既存のTiFlashノードに書き込まれると、以前のデータは徐々に新しい形式に変換されます。
-   ただし、アップグレード中に以前のデータを新しい形式に完全に変換することはできません。これは、変換によって一定量のシステム オーバーヘッドが消費されるためです (サービスには影響しませんが、それでも注意が必要です)。アップグレード後、 [`Compact`コマンド](/sql-statements/sql-statement-alter-table-compact.md)を実行してデータを新しい形式に変換することをお勧めします。手順は次のとおりです。

    1.  TiFlashレプリカを含むテーブルごとに次のコマンドを実行します。

        ```sql
        ALTER TABLE <table_name> COMPACT tiflash replica;
        ```

    2.  TiFlashノードを再起動します。

Grafana でテーブルがまだ古いデータ形式を使用しているかどうかを確認できます: **TiFlash-Summary** &gt; <strong>Storage Pool</strong> &gt; <strong>Storage Pool Run Mode</strong> 。

-   V2 のみ: PageStorage V2 を使用するテーブルの数 (パーティションを含む)
-   V3 のみ: PageStorage V3 を使用するテーブルの数 (パーティションを含む)
-   混合モード: データ形式が PageStorage V2 から PageStorage V3 に変換されたテーブルの数 (パーティションを含む)

**テストまたはその他の特別なシナリオでTiFlashをダウングレードするための回避策**

ターゲットのTiFlashノードを強制的にスケールインしてから、TiKV からデータを再度レプリケートできます。詳細な手順については、 [TiFlashクラスターのスケールイン](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster)を参照してください。

## v6.1 から v6.2 へ {#from-v6-1-to-v6-2}

TiFlash をv6.1 から v6.2 にアップグレードする場合、データstorageフォーマットの変更に注意してください。詳細については、 [ページストレージ](#pagestorage)を参照してください。
