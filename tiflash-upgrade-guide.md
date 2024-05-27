---
title: TiFlash Upgrade Guide
summary: TiFlash をアップグレードする際の注意事項を説明します。
---

# TiFlashアップグレード ガイド {#tiflash-upgrade-guide}

このドキュメントでは、 TiFlash をアップグレードするときに知っておく必要のある機能の変更と推奨されるアクションについて説明します。

標準的なアップグレード プロセスについては、次のドキュメントを参照してください。

-   [TiUPを使用して TiDB をアップグレードする](/upgrade-tidb-using-tiup.md)
-   [Kubernetes 上の TiDB をアップグレードする](https://docs.pingcap.com/tidb-in-kubernetes/stable/upgrade-a-tidb-cluster)

> **注記：**
>
> -   [高速スキャン](/tiflash/use-fastscan.md) 、v6.2.0 で実験的機能として導入され、v7.0.0 で一般提供 (GA) されます。強力なデータ一貫性を犠牲にして、より効率的なクエリ パフォーマンスを提供します。
>
> -   TiFlashを含む TiDB をメジャー バージョン間でアップグレードすることはお勧めしません (たとえば、v4.x から v6.x へ)。代わりに、最初に v4.x から v5.x にアップグレードし、次に v6.x にアップグレードする必要があります。
>
> -   v4.x はライフサイクルの終了が近づいています。できるだけ早く v5.x 以降にアップグレードすることをお勧めします。詳細については、 [TiDB リリース サポート ポリシー](https://en.pingcap.com/tidb-release-support-policy/)参照してください。
>
> -   PingCAP は、v6.0 などの非 LTS バージョンに対するバグ修正を提供しません。可能な場合は、v6.1 以降の LTS バージョンにアップグレードすることをお勧めします。

## TiUPを使用してTiFlashをアップグレードする {#upgrade-tiflash-using-tiup}

TiFlashを v5.3.0 より前のバージョンから v5.3.0 以降にアップグレードするには、 TiFlash を停止してからアップグレードする必要があります。TiUPを使用してTiFlashをアップグレードする場合は、次の点に注意してください。

-   TiUPクラスターのバージョンが v1.12.0 以降の場合、 TiFlash を停止してからアップグレードすることはできません。ターゲット バージョンでTiUPクラスターのバージョンが v1.12.0 以降が必要な場合は、まず`tiup cluster:v1.11.3 <subcommand>`使用してTiFlashを中間バージョンにアップグレードし、TiDB クラスターのオンライン アップグレードを実行してから、 TiUPバージョンをアップグレードし、その後 TiDB クラスターを停止せずにターゲット バージョンに直接アップグレードすることをお勧めします。
-   TiUPクラスターのバージョンが v1.12.0 より前の場合は、次の手順を実行してTiFlashをアップグレードします。

次の手順に従うと、 TiUPを使用して他のコンポーネントを中断せずにTiFlashをアップグレードできます。

1.  TiFlashインスタンスを停止します。

    ```shell
    tiup cluster stop <cluster-name> -R tiflash
    ```

2.  TiDB クラスターを再起動せずにアップグレードします (ファイルのみを更新します)。

    ```shell
    tiup cluster upgrade <cluster-name> <version> --offline 
    ```

    例えば：

    ```shell
    tiup cluster upgrade <cluster-name> v5.3.0 --offline
    ```

3.  TiDB クラスターを再ロードします。再ロード後、 TiFlashインスタンスが起動されるため、手動で起動する必要はありません。

    ```shell
    tiup cluster reload <cluster-name>
    ```

## 5.x または v6.0 から v6.1 へ {#from-5-x-or-v6-0-to-v6-1}

TiFlash をv5.x または v6.0 から v6.1 にアップグレードする場合は、 TiFlash Proxy と動的プルーニングの機能変更に注意してください。

### TiFlashプロキシ {#tiflash-proxy}

TiFlash Proxy は v6.1.0 にアップグレードされました (TiKV v6.0.0 と連動)。新しいバージョンでは、RocksDB バージョンがアップグレードされました。TiFlashをv6.1 にアップグレードすると、データ形式は自動的に新しいバージョンに変換されます。

通常のアップグレードでは、データ変換にリスクはありません。ただし、特別なシナリオ (テストや検証のシナリオなど) でTiFlash をv6.1 から以前のバージョンにダウングレードする必要がある場合、以前のバージョンでは新しい RocksDB 構成を解析できない可能性があります。その結果、 TiFlash は再起動に失敗します。アップグレード プロセスを完全にテストおよび検証し、緊急時の計画を準備することをお勧めします。

**テストやその他の特別なシナリオでTiFlash をダウングレードするための回避策**

ターゲットTiFlashノードを強制的にスケールインし、TiKV からデータを再度複製することができます。詳細な手順については、 [TiFlashクラスターのスケールイン](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster)参照してください。

### 動的剪定 {#dynamic-pruning}

[動的剪定モード](/partitioned-table.md#dynamic-pruning-mode)有効にせず、今後も使用しない場合は、このセクションをスキップできます。

-   新しくインストールされた TiDB v6.1.0: 動的プルーニングはデフォルトで有効になっています。

-   TiDB v6.0 以前: 動的プルーニングはデフォルトで無効になっています。アップグレード後の動的プルーニングの設定は、以前のバージョンの設定を継承します。つまり、アップグレード後に動的プルーニングが自動的に有効化 (または無効化) されることはありません。

    アップグレード後、動的プルーニングを有効にするには、 `tidb_partition_prune_mode`を`dynamic`に設定し、パーティション化されたテーブルの GlobalStats を手動で更新します。詳細については、 [動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode)を参照してください。

## v5.x または v6.0 から v6.2 へ {#from-v5-x-or-v6-0-to-v6-2}

TiDB v6.2 では、 TiFlash はデータstorage形式を V3 バージョンにアップグレードします。そのため、 TiFlash をv5.x または v6.0 から v6.2 にアップグレードする場合は、 [TiFlashプロキシ](#tiflash-proxy)と[動的剪定](#dynamic-pruning)の機能変更に加えて、PageStorage の機能変更にも注意する必要があります。

### ページストレージ {#pagestorage}

デフォルトでは、 TiFlash v6.2.0 は PageStorage V3 バージョン[`format_version = 4`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)を使用します。この新しいデータ形式により、ピーク書き込み I/O トラフィックが大幅に削減されます。更新トラフィックが多く、同時実行性やクエリ量が多いシナリオでは、 TiFlashデータ GC による過剰な CPU 使用率を効果的に軽減します。一方、以前のstorage形式と比較して、V3 バージョンではスペース増幅とリソース消費が大幅に削減されます。

-   v6.2.0 にアップグレードすると、新しいデータが既存のTiFlashノードに書き込まれるにつれて、以前のデータは徐々に新しい形式に変換されます。
-   ただし、アップグレード中に以前のデータを完全に新しい形式に変換することはできません。これは、変換によって一定量のシステム オーバーヘッドが消費されるためです (サービスには影響しませんが、注意が必要です)。アップグレード後、 [`Compact`コマンド](/sql-statements/sql-statement-alter-table-compact.md)実行してデータを新しい形式に変換することをお勧めします。手順は次のとおりです。

    1.  TiFlashレプリカを含む各テーブルに対して次のコマンドを実行します。

        ```sql
        ALTER TABLE <table_name> COMPACT tiflash replica;
        ```

    2.  TiFlashノードを再起動します。

テーブルがまだ古いデータ形式を使用しているかどうかは、Grafana で確認できます: **TiFlash-Summary** &gt; **Storage Pool** &gt; **Storage Pool Run Mode** 。

-   V2のみ: PageStorage V2を使用しているテーブルの数（パーティションを含む）
-   V3のみ: PageStorage V3を使用しているテーブルの数（パーティションを含む）
-   ミックスモード: PageStorage V2 から PageStorage V3 に変換されたデータ形式を持つテーブルの数 (パーティションを含む)

**テストやその他の特別なシナリオでTiFlash をダウングレードするための回避策**

ターゲットTiFlashノードを強制的にスケールインし、TiKV からデータを再度複製することができます。詳細な手順については、 [TiFlashクラスターのスケールイン](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster)参照してください。

## v6.1 から v6.2 へ {#from-v6-1-to-v6-2}

TiFlashをv6.1からv6.2にアップグレードする場合は、データstorage形式の変更に注意してください。詳細については、 [ページストレージ](#pagestorage)を参照してください。

## v6.x または v7.x から<code>storage.format_version = 5</code>が設定された v7.3 へ {#from-v6-x-or-v7-x-to-v7-3-with-code-storage-format-version-5-code-configured}

v7.3 以降、 TiFlash は新しい DTFile バージョン DTFile V3 (実験的) を導入します。この新しい DTFile バージョンでは、複数の小さなファイルを 1 つの大きなファイルに結合して、ファイルの合計数を減らすことができます。v7.3 では、デフォルトの DTFile バージョンは V2 のままです。V3 を使用するには、 [TiFlash構成パラメータ](/tiflash/tiflash-configuration.md) `storage.format_version = 5`を設定できます。設定後、 TiFlash は引き続き V2 DTFile を読み取ることができ、その後のデータ圧縮中に既存の V2 DTFile を徐々に V3 DTFile に書き換えます。

TiFlashを v7.3 にアップグレードし、 TiFlash がV3 DTFiles を使用するように構成した後、 TiFlash を以前のバージョンに戻す必要がある場合は、DTTool をオフラインで使用して V3 DTFiles を V2 DTFiles に書き換えることができます。詳細については、 [DTTool 移行ツール](/tiflash/tiflash-command-line-flags.md#dttool-migrate)参照してください。

## v6.x または v7.x から v7.4 以降のバージョンへ {#from-v6-x-or-v7-x-to-v7-4-or-a-later-version}

v7.4 以降では、データ圧縮中に生成される読み取りおよび書き込み増幅を削減するために、 TiFlash はPageStorage V3 のデータ圧縮ロジックを最適化します。これにより、基盤となるstorageファイル名の一部が変更されます。そのため、v7.4 以降のバージョンにアップグレードした後は、元のバージョンへのインプレース ダウングレードはサポートされません。

**テストやその他の特別なシナリオでTiFlash をダウングレードするための回避策**

テストやその他の特別なシナリオでTiFlash をダウングレードするには、ターゲットTiFlashノードを強制的にスケールインし、TiKV からデータを再度複製します。詳細な手順については、 [TiFlashクラスターのスケールイン](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster)参照してください。
