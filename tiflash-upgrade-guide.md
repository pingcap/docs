---
title: TiFlash Upgrade Guide
summary: TiFlashをアップグレードする際の注意事項を説明します。
---

# TiFlashアップグレードガイド {#tiflash-upgrade-guide}

このドキュメントでは、 TiFlash をアップグレードするときに知っておく必要のある機能の変更と推奨されるアクションについて説明します。

標準的なアップグレード プロセスについては、次のドキュメントを参照してください。

-   [TiUPを使用して TiDB をアップグレードする](/upgrade-tidb-using-tiup.md)
-   [Kubernetes 上の TiDB をアップグレードする](https://docs.pingcap.com/tidb-in-kubernetes/stable/upgrade-a-tidb-cluster)

> **注記：**
>
> -   [ファストスキャン](/tiflash/use-fastscan.md)はv6.2.0で実験的機能として導入され、v7.0.0で一般提供（GA）されます。強力なデータ整合性を犠牲にして、より効率的なクエリパフォーマンスを実現します。
>
> -   TiFlashを含む TiDB をメジャーバージョン間でアップグレードすることは推奨されません（例：v4.x から v6.x）。代わりに、まず v4.x から v5.x にアップグレードし、その後 v6.x にアップグレードする必要があります。
>
> -   v4.x のライフサイクルは終了に近づいています。できるだけ早く v5.x 以降にアップグレードすることをお勧めします。詳細については、 [TiDB リリース サポート ポリシー](https://www.pingcap.com/tidb-release-support-policy/)ご覧ください。
>
> -   PingCAPは、v6.0などのLTS以外のバージョンに対するバグ修正を提供していません。可能な限り、v6.1以降のLTSバージョンにアップグレードすることをお勧めします。

## TiUPを使用してTiFlashをアップグレードする {#upgrade-tiflash-using-tiup}

TiFlashをv5.3.0より前のバージョンからv5.3.0以降にアップグレードするには、 TiFlashを停止してからアップグレードする必要があります。TiUPを使用してTiFlashをアップグレードする際は、以下の点にご注意ください。

-   TiUPクラスタのバージョンがv1.12.0以降の場合、 TiFlashを停止してからアップグレードすることはできません。アップグレード先のバージョンでTiUPクラスタのバージョンがv1.12.0以降が必要な場合は、まず`tiup cluster:v1.11.3 <subcommand>`使用してTiFlashを中間バージョンにアップグレードし、TiDBクラスタのオンラインアップグレードを実行した後、 TiUPバージョンをアップグレードし、その後TiDBクラスタを停止せずに直接アップグレード先のバージョンにアップグレードすることをお勧めします。
-   TiUPクラスターのバージョンが v1.12.0 より前の場合は、次の手順を実行してTiFlashをアップグレードします。

次の手順に従うと、 TiUPを使用して他のコンポーネントを中断せずにTiFlashをアップグレードできます。

1.  TiFlashインスタンスを停止します。

    ```shell
    tiup cluster stop <cluster-name> -R tiflash
    ```

2.  TiDB クラスターを再起動せずにアップグレードします (ファイルの更新のみ)。

    ```shell
    tiup cluster upgrade <cluster-name> <version> --offline 
    ```

    例えば：

    ```shell
    tiup cluster upgrade <cluster-name> v5.3.0 --offline
    ```

3.  TiDB クラスターをリロードします。リロード後、 TiFlashインスタンスが起動するので、手動で起動する必要はありません。

    ```shell
    tiup cluster reload <cluster-name>
    ```

## 5.x または v6.0 から v6.1 へ {#from-5-x-or-v6-0-to-v6-1}

TiFlash をv5.x または v6.0 から v6.1 にアップグレードする場合は、 TiFlash Proxy と動的プルーニングの機能変更に注意してください。

### TiFlashプロキシ {#tiflash-proxy}

TiFlash Proxyはv6.1.0（TiKV v6.0.0と連動）にアップグレードされました。この新バージョンではRocksDBのバージョンもアップグレードされています。TiFlashをv6.1にアップグレードすると、データ形式は自動的に新しいバージョンに変換されます。

通常のアップグレードでは、データ変換にリスクは伴いません。ただし、特別なシナリオ（テストや検証など）でTiFlashをv6.1から以前のバージョンにダウングレードする必要がある場合、以前のバージョンでは新しいRocksDB構成の解析に失敗する可能性があります。その結果、 TiFlashの再起動に失敗する可能性があります。アップグレードプロセスを十分にテストおよび検証し、緊急時の対応策を準備することをお勧めします。

**テストやその他の特別なシナリオでTiFlashをダウングレードするための回避策**

対象のTiFlashノードを強制的にスケールインし、TiKVからデータを再度複製することができます。詳細な手順については、 [TiFlashクラスターのスケールイン](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster)参照してください。

### 動的剪定 {#dynamic-pruning}

[動的剪定モード](/partitioned-table.md#dynamic-pruning-mode)有効にせず、今後も使用しない場合は、このセクションをスキップできます。

-   新しくインストールされた TiDB v6.1.0: 動的プルーニングはデフォルトで有効になっています。

-   TiDB v6.0以前：動的プルーニングはデフォルトで無効になっています。アップグレード後の動的プルーニングの設定は、以前のバージョンの設定を継承します。つまり、アップグレード後も動的プルーニングは自動的に有効化（または無効化）されません。

    アップグレード後、動的プルーニングを有効にするには、 `tidb_partition_prune_mode`を`dynamic`に設定し、パーティションテーブルのグローバル統計を手動で更新してください。詳細については、 [動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode)参照してください。

## v5.x または v6.0 から v6.2 へ {#from-v5-x-or-v6-0-to-v6-2}

TiDB v6.2では、 TiFlashのデータstorageフォーマットがV3にアップグレードされ、書き込み増幅の低減とTiFlashの安定性向上が図られています。v5.x、v6.0、またはv6.1からv6.2以降のバージョンにアップグレードする場合は、 [TiFlashプロキシ](#tiflash-proxy)と[動的剪定](#dynamic-pruning)の機能変更に加えて、PageStorageの機能変更にも注意する必要があります。

### ページストレージ {#pagestorage}

TiFlash v6.2.0はデフォルトでPageStorage V3バージョン[`format_version = 4`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)使用します。この新しいデータフォーマットは、ピーク時の書き込みI/Oトラフィックを大幅に削減します。更新トラフィックが多く、同時実行性やクエリ負荷が高いシナリオでは、 TiFlashデータGCによる過剰なCPU使用率を効果的に軽減します。また、以前のstorageフォーマットと比較して、V3バージョンはスペース増幅とリソース消費を大幅に削減します。

-   v6.2.0 にアップグレードすると、新しいデータが既存のTiFlashノードに書き込まれると同時に、以前のデータは徐々に新しい形式に変換されます。
-   ただし、アップグレード中に以前のデータを完全に新しい形式に変換することはできません。これは、変換によってある程度のシステムオーバーヘッドが発生するためです（サービスには影響はありませんが、注意が必要です）。アップグレード後、 [`Compact`コマンド](/sql-statements/sql-statement-alter-table-compact.md)実行してデータを新しい形式に変換することをお勧めします。手順は次のとおりです。

    1.  TiFlashレプリカを含む各テーブルに対して次のコマンドを実行します。

        ```sql
        ALTER TABLE <table_name> COMPACT tiflash replica;
        ```

    2.  TiFlashノードを再起動します。

テーブルがまだ古いデータ形式を使用しているかどうかを Grafana で確認できます: **TiFlash-Summary** &gt; **Storage Pool** &gt; **Storage Pool Run Mode** 。

-   V2のみ: PageStorage V2を使用しているテーブルの数（パーティションを含む）
-   V3のみ: PageStorage V3を使用しているテーブルの数（パーティションを含む）
-   混合モード: PageStorage V2 から PageStorage V3 に変換されたデータ形式を持つテーブルの数 (パーティションを含む)

> **注記：**
>
> 以下のパッチバージョンには既知の問題（問題[＃9039](https://github.com/pingcap/tiflash/issues/9039) ）があります。これらのバージョンにアップグレードすると、 TiFlashデータが破損する可能性があります。
>
> -   v6.5.0 から v6.5.9
> -   バージョン6.6.0
> -   バージョン7.0.0
> -   v7.1.0 から v7.1.5
> -   バージョン7.2.0
> -   バージョン7.3.0
> -   バージョン7.4.0
> -   v7.5.0 から v7.5.1
>
> この問題が修正された v6.5.10、v7.1.6、v7.5.2 以降のバージョンにアップグレードすることをお勧めします。

**テストやその他の特別なシナリオでTiFlashをダウングレードするための回避策**

対象のTiFlashノードを強制的にスケールインし、TiKVからデータを再度複製することができます。詳細な手順については、 [TiFlashクラスターのスケールイン](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster)参照してください。

## v6.x または v7.x から<code>storage.format_version = 5</code>が設定された v7.3 へ {#from-v6-x-or-v7-x-to-v7-3-with-code-storage-format-version-5-code-configured}

TiFlash v7.3 以降、新しい DTFile バージョン DTFile V3 (実験的) が導入されました。この新しい DTFile バージョンでは、複数の小さなファイルを 1 つの大きなファイルに結合することで、ファイル総数を削減できます。v7.3 では、デフォルトの DTFile バージョンは引き続き V2 です。V3 を使用するには、 [TiFlash構成パラメータ](/tiflash/tiflash-configuration.md) `storage.format_version = 5`設定します。設定後もTiFlash はV2 DTFile を読み取り可能で、その後のデータ圧縮時に既存の V2 DTFile を徐々に V3 DTFile に書き換えます。

TiFlashをv7.3にアップグレードし、V3 DTFilesを使用するように設定した後、 TiFlashを以前のバージョンに戻す必要がある場合は、DTToolをオフラインで使用してV3 DTFilesをV2 DTFilesに書き換えることができます。詳細については、 [DTTool 移行ツール](/tiflash/tiflash-command-line-flags.md#dttool-migrate)参照してください。

## v6.x または v7.x から v7.4 以降のバージョンへ {#from-v6-x-or-v7-x-to-v7-4-or-a-later-version}

v7.4以降、データ圧縮中に発生する読み取りおよび書き込みの増幅を削減するため、 TiFlashはPageStorage V3のデータ圧縮ロジックを最適化します。これにより、基盤となるstorageファイル名の一部が変更されます。そのため、 TiFlashをv7.4以降のバージョンにアップグレードした後は、元のバージョンへのインプレースダウングレードはサポートされません。

## v7.x から v8.4 以降のバージョンへ {#from-v7-x-to-v8-4-or-a-later-version}

バージョン8.4以降、 TiFlashの基盤となるstorageフォーマットは[ベクトル検索](/vector-search/vector-search-overview.md)サポートするように更新されました。そのため、 TiFlashをバージョン8.4以降にアップグレードした後は、元のバージョンへのインプレースダウングレードはサポートされません。

**テストやその他の特別なシナリオでTiFlashをダウングレードするための回避策**

テストやその他の特殊なシナリオでTiFlashをダウングレードするには、対象のTiFlashノードを強制的にスケールインし、その後TiKVからデータを再度複製します。詳細な手順については、 [TiFlashクラスターのスケールイン](/scale-tidb-using-tiup.md#scale-in-a-tiflash-cluster)参照してください。
