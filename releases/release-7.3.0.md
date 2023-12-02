---
title: TiDB 7.3.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.3.0.
---

# TiDB 7.3.0 リリースノート {#tidb-7-3-0-release-notes}

発売日：2023年8月14日

TiDB バージョン: 7.3.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.3/quick-start-with-tidb) | [インストールパッケージ](https://www.pingcap.com/download/?version=v7.3.0#version-list)

7.3.0 では、次の主な機能が導入されています。それに加えて、7.3.0 には、TiDBサーバーとTiFlashの安定性をクエリするための一連の機能拡張 ( [機能の詳細](#feature-details)セクションで説明) も含まれています。これらの拡張機能は本質的にさまざまであり、ユーザー向けではないため、次の表には含まれていません。

<table><thead><tr><th>カテゴリー</th><th>特徴</th><th>説明</th></tr></thead><tbody><tr><td>スケーラビリティとパフォーマンス</td><td>TiDB Lightning は<a href="https://docs.pingcap.com/tidb/v7.3/partitioned-raft-kv">Partitioned Raft KV</a> (実験的) をサポートします</td><td>TiDB Lightning は、アーキテクチャの短期 GA の一部として、新しい Partitioned Raft KVアーキテクチャをサポートするようになりました。</td></tr><tr><td rowspan="2">信頼性と可用性</td><td><a href="https://docs.pingcap.com/tidb/v7.3/tidb-lightning-physical-import-mode-usage#conflict-detection">データのインポート時に自動競合検出と解決を追加する</a></td><td>TiDB Lightning物理インポート モードは、競合検出の新しいバージョンをサポートしています。これは、競合が発生したときに競合データを置換 ( <code>replace</code> ) または無視 ( <code>ignore</code> ) するセマンティクスを実装します。競合データを自動的に処理しながら、競合解決のパフォーマンスを向上させます。</td></tr><tr><td><a href="https://docs.pingcap.com/tidb/v7.3/tidb-resource-control#query-watch-parameters">暴走クエリの手動管理</a>(実験的)</td><td>クエリには予想よりも時間がかかる場合があります。リソース グループの新しいウォッチ リストを使用すると、クエリをより効果的に管理し、クエリの優先順位を下げるか強制終了できるようになりました。この機能により、オペレーターが正確な SQL テキスト、SQL ダイジェスト、またはプラン ダイジェストによってターゲット クエリをマークし、リソース グループ レベルでクエリを処理できるようになり、クラスターに対する予期しない大規模なクエリの潜在的な影響をより詳細に制御できるようになります。</td></tr><tr><td> SQL</td><td><a href="https://docs.pingcap.com/tidb/v7.3/optimizer-hints">クエリ プランナーにオプティマイザ ヒントをさらに追加することで、クエリの安定性に対するオペレータの制御を強化します。</a></td><td>追加されたヒント: <code>NO_INDEX_JOIN()</code> 、 <code>NO_MERGE_JOIN()</code> 、 <code>NO_INDEX_MERGE_JOIN()</code> 、 <code>NO_HASH_JOIN()</code> 、 <code>NO_INDEX_HASH_JOIN()</code></td></tr><tr><td> DB の操作と可観測性</td><td><a href="https://docs.pingcap.com/tidb/v7.3/sql-statement-show-analyze-status">統計収集タスクの進行状況を表示する</a></td><td><code>SHOW ANALYZE STATUS</code>ステートメントまたは<code>mysql.analyze_jobs</code>システム テーブルを使用した<code>ANALYZE</code>タスクの進行状況の表示をサポートします。</td></tr></tbody></table>

## 機能の詳細 {#feature-details}

### パフォーマンス {#performance}

-   TiFlash は、レプリカ選択戦略[#44106](https://github.com/pingcap/tidb/issues/44106) @ [徐淮嶼](https://github.com/XuHuaiyu)をサポートしています。

    v7.3.0 より前では、 TiFlash はパフォーマンスを最大化するために、データ スキャンと MPP 計算にすべてのノードのレプリカを使用します。 v7.3.0 以降、 TiFlash にはレプリカ選択戦略が導入され、 [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read-new-in-v730)システム変数を使用して構成できるようになりました。この戦略は、 [ゾーン属性](/schedule-replicas-by-topology-labels.md#optional-configure-labels-for-tidb)つのノードに基づいて特定のレプリカを選択し、データ スキャンと MPP 計算のために特定のノードをスケジュールすることをサポートします。

    複数のデータ センターに展開され、各データ センターに完全なTiFlashデータ レプリカがあるクラスターの場合、現在のデータ センターからTiFlashレプリカのみを選択するようにこの戦略を構成できます。これは、データ スキャンと MPP 計算が現在のデータ センター内のTiFlashノードでのみ実行されることを意味し、データ センター間での過剰なネットワーク データ送信が回避されます。

    詳細については、 [ドキュメンテーション](/system-variables.md#tiflash_replica_read-new-in-v730)を参照してください。

-   TiFlash はノード[#40220](https://github.com/pingcap/tidb/issues/40220) @ [エルサ0520](https://github.com/elsa0520)内のランタイム フィルターをサポートします

    ランタイム フィルターは、クエリ計画フェーズ中に生成される**動的な述語**です。テーブル結合のプロセスにおいて、これらの動的述語は結合条件を満たさない行を効果的に除外し、スキャン時間とネットワーク オーバーヘッドを削減し、テーブル結合の効率を向上させることができます。 v7.3.0 以降、 TiFlash はノード内のランタイム フィルターをサポートし、分析クエリの全体的なパフォーマンスを向上させます。一部の TPC-DS ワークロードでは、パフォーマンスが 10% ～ 50% 向上する可能性があります。

    この機能は、v7.3.0 ではデフォルトで無効になっています。この機能を有効にするには、システム変数[`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-new-in-v720)から`LOCAL`を設定します。

    詳細については、 [ドキュメンテーション](/runtime-filter.md)を参照してください。

-   TiFlash は、共通テーブル式 (CTE) の実行をサポートしています (実験的) [#43333](https://github.com/pingcap/tidb/issues/43333) @ [ウィノロス](https://github.com/winoros)

    v7.3.0 より前では、 TiFlashの MPP エンジンは、デフォルトでは CTE を含むクエリを実行できません。 MPP フレームワーク内で最高の実行パフォーマンスを達成するには、システム変数[`tidb_opt_force_inline_cte`](/system-variables.md#tidb_opt_force_inline_cte-new-in-v630)を使用してインライン CTE を強制する必要があります。

    v7.3.0 以降、TiFlash の MPP エンジンは、インライン化せずに CTE を使用したクエリの実行をサポートし、MPP フレームワーク内で最適なクエリの実行を可能にします。 TPC-DS ベンチマーク テストでは、CTE のインライン化と比較して、この機能により、CTE を含むクエリの全体的なクエリ実行速度が 20% 向上することが示されました。

    この機能は実験的であり、デフォルトでは無効になっています。これはシステム変数[`tidb_opt_enable_mpp_shared_cte_execution`](/system-variables.md#tidb_opt_enable_mpp_shared_cte_execution-new-in-v720)によって制御されます。

### 信頼性 {#reliability}

-   新しいオプティマイザー ヒント[#45520](https://github.com/pingcap/tidb/issues/45520) @ [qw4990](https://github.com/qw4990)を追加

    v7.3.0 では、TiDB は、テーブル間の結合方法を制御するために、次のようないくつかの新しいオプティマイザー ヒントを導入します。

    -   [`NO_MERGE_JOIN()`](/optimizer-hints.md#no_merge_joint1_name--tl_name-)はマージ結合以外の結合方法を選択します。
    -   [`NO_INDEX_JOIN()`](/optimizer-hints.md#no_index_joint1_name--tl_name-)指定すると、インデックスのネストされたループ結合以外の結合方法が選択されます。
    -   [`NO_INDEX_MERGE_JOIN()`](/optimizer-hints.md#no_index_merge_joint1_name--tl_name-)指定すると、インデックスネストループマージ結合以外の結合方法が選択されます。
    -   [`NO_HASH_JOIN()`](/optimizer-hints.md#no_hash_joint1_name--tl_name-)はハッシュ結合以外の結合方法を選択します。
    -   [`NO_INDEX_HASH_JOIN()`](/optimizer-hints.md#no_index_hash_joint1_name--tl_name-) [インデックスのネストされたループのハッシュ結合](/optimizer-hints.md#inl_hash_join)以外の結合方法を選択します。

    詳細については、 [ドキュメンテーション](/optimizer-hints.md)を参照してください。

-   予想を超えるリソースを使用するクエリに手動でマークを付ける (実験的) [#43691](https://github.com/pingcap/tidb/issues/43691) @ [コナー1996](https://github.com/Connor1996) @ [キャビンフィーバーB](https://github.com/CabinfeverB)

    v7.2.0 では、TiDB は、暴走クエリを自動的にダウングレードまたはキャンセルすることにより、予想を超えるリソースを使用するクエリ (暴走クエリ) を自動的に管理します。実際には、ルールだけですべてのケースをカバーできるわけではありません。したがって、TiDB v7.3.0 では、暴走クエリを手動でマークする機能が導入されています。新しいコマンド[`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md)を使用すると、SQL テキスト、SQL ダイジェスト、または実行計画に基づいて暴走クエリをマークでき、マークされた暴走クエリをダウングレードまたはキャンセルできます。

    この機能は、データベースの突然のパフォーマンス問題に対する効果的な介入方法を提供します。クエリによって引き起こされるパフォーマンスの問題については、根本原因を特定する前に、この機能を使用すると全体的なパフォーマンスへの影響を迅速に軽減できるため、システム サービスの品質が向上します。

    詳細については、 [ドキュメンテーション](/tidb-resource-control.md#query-watch-parameters)を参照してください。

### SQL {#sql}

-   List および List COLUMNS パーティション テーブルは、デフォルト パーティション[#20679](https://github.com/pingcap/tidb/issues/20679) @ [むじょん](https://github.com/mjonss) @ [bb7133](https://github.com/bb7133)をサポートします。

    v7.3.0 より前では、 `INSERT`ステートメントを使用して List または List COLUMNSパーティションテーブルにデータを挿入する場合、データはテーブルの指定されたパーティション条件を満たしている必要があります。挿入されるデータがこれらの条件のいずれかを満たさない場合、ステートメントの実行は失敗するか、準拠していないデータは無視されます。

    v7.3.0 以降、List および List COLUMNS パーティション テーブルはデフォルトのパーティションをサポートします。デフォルト パーティションの作成後、挿入されるデータがパーティション化条件を満たさない場合、そのデータはデフォルト パーティションに書き込まれます。この機能により、 List およびList COLUMNS パーティショニングの使いやすさが向上し、パーティショニング条件を満たさないデータによる`INSERT`ステートメントの実行失敗やデータの無視が回避されます。

    この機能は、MySQL 構文に対する TiDB 拡張機能であることに注意してください。デフォルトのパーティションを持つパーティションテーブルの場合、テーブル内のデータを MySQL に直接レプリケートすることはできません。

    詳細については、 [ドキュメンテーション](/partitioned-table.md#list-partitioning)を参照してください。

### 可観測性 {#observability}

-   統計収集の進行状況を表示[#44033](https://github.com/pingcap/tidb/issues/44033) @ [ホーキングレイ](https://github.com/hawkingrei)

    大きなテーブルの統計の収集には長い時間がかかることがよくあります。以前のバージョンでは、統計収集の進行状況を確認できないため、完了時間を予測できませんでした。 TiDB v7.3.0 では、統計収集の進行状況を表示する機能が導入されています。システム テーブル`mysql.analyze_jobs`または`SHOW ANALYZE STATUS`を使用して、全体のワークロード、現在の進行状況、各サブタスクの推定完了時間を表示できます。大規模なデータのインポートや SQL パフォーマンスの最適化などのシナリオでは、この機能はタスク全体の進行状況を把握するのに役立ち、ユーザー エクスペリエンスが向上します。

    詳細については、 [ドキュメンテーション](/sql-statements/sql-statement-show-analyze-status.md)を参照してください。

-   Plan Replayer は履歴統計のエクスポートをサポートします[#45038](https://github.com/pingcap/tidb/issues/45038) @ [時間と運命](https://github.com/time-and-fate)

    v7.3.0 以降、新しく追加された[`dump with stats as of timestamp`](/sql-plan-replayer.md)句により、Plan Replayer を使用して、特定の時点での指定された SQL 関連オブジェクトの統計をエクスポートできます。実行計画の問題の診断中に、履歴統計を正確に取得すると、問題が発生したときに実行計画がどのように生成されたかをより正確に分析するのに役立ちます。これは、問題の根本原因を特定するのに役立ち、実行計画の問題を診断する効率が大幅に向上します。

    詳細については、 [ドキュメンテーション](/sql-plan-replayer.md)を参照してください。

### データ移行 {#data-migration}

-   TiDB Lightning は、競合データの検出と処理戦略[#41629](https://github.com/pingcap/tidb/issues/41629) @ [ランス6716](https://github.com/lance6716)の新しいバージョンを導入します。

    以前のバージョンでは、 TiDB Lightning は論理インポート モードと物理インポート モードに異なる競合検出および処理方法を使用していましたが、これは設定が複雑で、ユーザーが理解するのが容易ではありませんでした。さらに、物理インポート モードでは、 `replace`または`ignore`戦略を使用して競合を処理できません。 v7.3.0 以降、 TiDB Lightning、論理インポート モードと物理インポート モードの両方に対して統合された競合検出および処理戦略が導入されています。競合が発生した場合、競合するデータをエラーを報告する ( `error` )、置換する ( `replace` )、または無視する ( `ignore` ) かを選択できます。指定した数の競合レコードを処理した後にタスクを中断して終了するなど、競合レコードの数を制限できます。さらに、システムはトラブルシューティングのために競合するデータを記録できます。

    競合が多いインポート データの場合、パフォーマンスを向上させるために、新しいバージョンの競合検出および処理戦略を使用することをお勧めします。ラボ環境では、新しいバージョン戦略により、競合検出と処理のパフォーマンスが古いバージョンよりも最大 3 倍高速化されます。この性能値は参考値です。実際のパフォーマンスは、構成、テーブル構造、競合するデータの割合によって異なる場合があります。新しいバージョンと古いバージョンの競合戦略を同時に使用することはできないことに注意してください。古い競合の検出および処理戦略は、将来廃止される予定です。

    詳細については、 [ドキュメンテーション](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#conflict-detection)を参照してください。

-   TiDB Lightning はPartitioned Raft KV (実験的) [#14916](https://github.com/tikv/tikv/issues/14916) @ [GMHDBJD](https://github.com/GMHDBJD)をサポートします

    TiDB Lightning がPartitioned Raft KV をサポートするようになりました。この機能は、 TiDB Lightningのデータ インポート パフォーマンスの向上に役立ちます。

-   TiDB Lightning、より多くの診断ログを出力することでトラブルシューティングを強化するための新しいパラメータ`enable-diagnose-log`が導入されました[#45497](https://github.com/pingcap/tidb/issues/45497) @ [D3ハンター](https://github.com/D3Hunter)

    デフォルトでは、この機能は無効になっており、 TiDB Lightning は`lightning/main`を含むログのみを出力。 TiDB Lightningを有効にすると、すべてのパッケージ ( `client-go`と`tidb`を含む) のログが出力、 `client-go`と`tidb`に関連する問題の診断に役立ちます。

    詳細については、 [ドキュメンテーション](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-global)を参照してください。

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> このセクションでは、v7.2.0 から現在のバージョン (v7.3.0) にアップグレードするときに知っておく必要がある互換性の変更について説明します。 v7.1.0 以前のバージョンから現在のバージョンにアップグレードする場合は、中間バージョンで導入された互換性の変更も確認する必要がある場合があります。

### 行動の変化 {#behavior-changes}

-   バックアップと復元 (BR)

    -   BR は、完全なデータ復元を実行する前に、空のクラスターのチェックを追加します。デフォルトでは、空ではないクラスターへのデータの復元は許可されていません。復元を強制する場合は、 `--filter`オプションを使用して、データを復元する対応するテーブル名を指定できます。

-   TiDB Lightning

    -   `tikv-importer.on-duplicate`は非推奨となり、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)に置き換えられます。
    -   TiDB Lightning が移行タスクを停止する前に許容できる致命的でないエラーの最大数を制御する`max-error`パラメーターは、インポート データの競合を制限しなくなりました。 [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)パラメータは、許容できる競合レコードの最大数を制御するようになりました。

-   TiCDC

    -   Kafka シンクが Avro プロトコルを使用する場合、 `force-replicate`パラメーターが`true`に設定されていると、TiCDC は変更フィードの作成時にエラーを報告します。
    -   `delete-only-output-handle-key-columns`と`force-replicate`パラメータの間に互換性がないため、両方のパラメータが有効になっていると、TiCDC は変更フィードの作成時にエラーを報告します。
    -   出力プロトコルがオープン プロトコルの場合、 `UPDATE`イベントは変更された列のみを出力します。

### システム変数 {#system-variables}

| 変数名                                                                                                                     | 種類の変更    | 説明                                                                         |
| ----------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------- |
| [`tidb_opt_enable_mpp_shared_cte_execution`](/system-variables.md#tidb_opt_enable_mpp_shared_cte_execution-new-in-v720) | 修正済み     | このシステム変数は、v7.3.0 から有効になります。非再帰共通テーブル式 (CTE) をTiFlash MPP で実行できるかどうかを制御します。 |
| [`tidb_lock_unchanged_keys`](/system-variables.md#tidb_lock_unchanged_keys-new-in-v711-and-v730)                        | 新しく追加された | この変数は、特定のシナリオで、トランザクションに関与しているが変更されていないキーをロックするかどうかを制御するために使用されます。         |
| [`tidb_opt_enable_non_eval_scalar_subquery`](/system-variables.md#tidb_opt_enable_non_eval_scalar_subquery-new-in-v730) | 新しく追加された | `EXPLAIN`ステートメントが、最適化段階で拡張できる定数サブクエリの実行を無効にするかどうかを制御します。                   |
| [`tidb_skip_missing_partition_stats`](/system-variables.md#tidb_skip_missing_partition_stats-new-in-v730)               | 新しく追加された | この変数は、パーティション統計が欠落している場合の GlobalStats の生成を制御します。                           |
| [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read-new-in-v730)                                         | 新しく追加された | クエリでTiFlashエンジンが必要な場合に、 TiFlashレプリカを選択する戦略を制御します。                          |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                                 | 種類の変更    | 説明                                                                                                                                                                                                                                                                                                                                                                        |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [`enable-32bits-connection-id`](/tidb-configuration-file.md#enable-32bits-connection-id-new-in-v730)                                            | 新しく追加された | 32 ビット接続 ID 機能を有効にするかどうかを制御します。                                                                                                                                                                                                                                                                                                                                           |
| TiDB           | [`in-mem-slow-query-recent-num`](/tidb-configuration-file.md#in-mem-slow-query-recent-num-new-in-v730)                                          | 新しく追加された | メモリにキャッシュされる、最近使用された低速クエリの数を制御します。                                                                                                                                                                                                                                                                                                                                        |
| TiDB           | [`in-mem-slow-query-topn-num`](/tidb-configuration-file.md#in-mem-slow-query-topn-num-new-in-v730)                                              | 新しく追加された | メモリにキャッシュされる最も遅いクエリの数を制御します。                                                                                                                                                                                                                                                                                                                                              |
| TiKV           | [`coprocessor.region-bucket-size`](/tikv-configuration-file.md#region-bucket-size-new-in-v610)                                                  | 修正済み     | デフォルト値を`96MiB`から`50MiB`に変更します。                                                                                                                                                                                                                                                                                                                                            |
| TiKV           | [`raft-engine.format-version`](/tikv-configuration-file.md#format-version-new-in-v630)                                                          | 修正済み     | Partitioned Raft KV ( `storage.engine="partitioned-raft-kv"` ) を使用する場合は、リボンフィルターが使用されます。したがって、TiKV はデフォルト値を`2`から`5`に変更します。                                                                                                                                                                                                                                                |
| TiKV           | [`raftdb.max-total-wal-size`](/tikv-configuration-file.md#max-total-wal-size-1)                                                                 | 修正済み     | Partitioned Raft KV ( `storage.engine="partitioned-raft-kv"` ) を使用する場合、TiKV は WAL の書き込みをスキップします。したがって、TiKV はデフォルト値を`"4GB"`から`1`に変更します。これは、WAL が無効になることを意味します。                                                                                                                                                                                                             |
| TiKV           | [`rocksdb.[defaultcf|writecf|lockcf].compaction-guard-min-output-file-size`](/tikv-configuration-file.md#compaction-guard-min-output-file-size) | 修正済み     | デフォルト値を`"1MB"`から`"8MB"`に変更して、大規模なデータの書き込み中に圧縮速度が書き込み速度に追いつかないという問題を解決します。                                                                                                                                                                                                                                                                                                 |
| TiKV           | [`rocksdb.[defaultcf|writecf|lockcf].format-version`](/tikv-configuration-file.md#format-version-new-in-v620)                                   | 修正済み     | Partitioned Raft KV ( `storage.engine="partitioned-raft-kv"` ) を使用する場合は、リボンフィルターが使用されます。したがって、TiKV はデフォルト値を`2`から`5`に変更します。                                                                                                                                                                                                                                                |
| TiKV           | [`rocksdb.lockcf.write-buffer-size`](/tikv-configuration-file.md#write-buffer-size)                                                             | 修正済み     | Partitioned Raft KV ( `storage.engine="partitioned-raft-kv"` ) を使用する場合、lockcf での圧縮を高速化するために、TiKV はデフォルト値を`"32MB"`から`"4MB"`に変更します。                                                                                                                                                                                                                                         |
| TiKV           | [`rocksdb.max-total-wal-size`](/tikv-configuration-file.md#max-total-wal-size)                                                                  | 修正済み     | Partitioned Raft KV ( `storage.engine="partitioned-raft-kv"` ) を使用する場合、TiKV は WAL の書き込みをスキップします。したがって、TiKV はデフォルト値を`"4GB"`から`1`に変更します。これは、WAL が無効になることを意味します。                                                                                                                                                                                                             |
| TiKV           | [`rocksdb.stats-dump-period`](/tikv-configuration-file.md#stats-dump-period)                                                                    | 修正済み     | Partitioned Raft KV ( `storage.engine="partitioned-raft-kv"` ) を使用する場合、冗長ログの印刷を無効にするために、デフォルト値が`"10m"`から`"0"`に変更されます。                                                                                                                                                                                                                                                     |
| TiKV           | [`rocksdb.write-buffer-limit`](/tikv-configuration-file.md#write-buffer-limit-new-in-v660)                                                      | 修正済み     | memtable のメモリオーバーヘッドを削減するために、 `storage.engine="raft-kv"`の場合、TiKV はデフォルト値をマシンのメモリの 25% から`0` (制限なしを意味します) に変更します。 Partitioned Raft KV ( `storage.engine="partitioned-raft-kv"` ) を使用する場合、TiKV はマシンのメモリのデフォルト値を 25% から 20% に変更します。                                                                                                                                          |
| TiKV           | [`storage.block-cache.capacity`](/tikv-configuration-file.md#capacity)                                                                          | 修正済み     | Partitioned Raft KV ( `storage.engine="partitioned-raft-kv"` ) を使用する場合、memtable のメモリオーバーヘッドを補うために、TiKV はデフォルト値をシステムメモリ全体のサイズの 45% から 30% に変更します。                                                                                                                                                                                                                          |
| TiFlash        | [`storage.format_version`](/tiflash/tiflash-configuration.md)                                                                                   | 修正済み     | 新しい DTFile フォーマット`format_version = 5`を導入し、より小さなファイルを結合することで物理ファイルの数を削減します。この形式は実験的であり、デフォルトでは有効になっていないことに注意してください。                                                                                                                                                                                                                                                        |
| TiDB Lightning | `tikv-importer.incremental-import`                                                                                                              | 削除されました  | TiDB Lightningの並行インポート パラメータ。これは増分インポート パラメーターと間違われやすいため、このパラメーターの名前は`tikv-importer.parallel-import`に変更されました。ユーザーが古いパラメータ名を渡すと、自動的に新しいパラメータ名に変換されます。                                                                                                                                                                                                                      |
| TiDB Lightning | `tikv-importer.on-duplicate`                                                                                                                    | 廃止されました  | 論理インポート モードで競合するレコードを挿入しようとしたときに実行するアクションを制御します。 v7.3.0 以降、このパラメータは[`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)に置き換えられます。                                                                                                                                                                                                   |
| TiDB Lightning | [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md)                                                                   | 新しく追加された | 競合するデータを処理するための新しいバージョンの戦略。 `conflict_records`のテーブル内の最大行数を制御します。デフォルト値は 100 です。                                                                                                                                                                                                                                                                                           |
| TiDB Lightning | [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md)                                                                          | 新しく追加された | 競合するデータを処理するための新しいバージョンの戦略。これには次のオプションが含まれます: &quot;&quot; (TiDB Lightning は競合するデータを検出および処理しません)、 `error` (インポートされたデータで主キーまたは一意キーの競合が検出された場合はインポートを終了し、エラーを報告します)、 `replace` (データが一致した場合)主キーまたは一意キーが競合する場合、新しいデータは保持され、古いデータは上書きされます。)、 `ignore` (主キーまたは一意キーが競合するデータが見つかった場合、古いデータは保持され、新しいデータは無視されます。)。デフォルト値は &quot;&quot; です。つまり、 TiDB Lightning は競合するデータを検出および処理しません。 |
| TiDB Lightning | [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md)                                                                         | 新しく追加された | 競合するデータの上限を制御します。 `conflict.strategy="error"`の場合、デフォルト値は`0`です。 `conflict.strategy="replace"`または`conflict.strategy="ignore"`の場合、それを maxint として設定できます。                                                                                                                                                                                                                      |
| TiDB Lightning | [`enable-diagnose-logs`](/tidb-lightning/tidb-lightning-configuration.md)                                                                       | 新しく追加された | 診断ログを有効にするかどうかを制御します。デフォルト値は`false`です。つまり、インポートに関連するログのみが出力され、他の依存コンポーネントのログは出力されません。 `true`に設定すると、インポート プロセスと他の依存コンポーネントの両方からのログが出力され、診断に使用できる GRPC デバッグが有効になります。                                                                                                                                                                                                        |
| TiDB Lightning | [`tikv-importer.parallel-import`](/tidb-lightning/tidb-lightning-configuration.md)                                                              | 新しく追加された | TiDB Lightningの並行インポート パラメータ。これは、増分インポート パラメータと誤って悪用される可能性がある既存の`tikv-importer.incremental-import`パラメータを置き換えます。                                                                                                                                                                                                                                                           |
| BR             | `azblob.encryption-scope`                                                                                                                       | 新しく追加された | BR は、 Azure Blob Storage の暗号化スコープのサポートを提供します。                                                                                                                                                                                                                                                                                                                             |
| BR             | `azblob.encryption-key`                                                                                                                         | 新しく追加された | BR は、 Azure Blob Storage の暗号化キーのサポートを提供します。                                                                                                                                                                                                                                                                                                                               |
| TiCDC          | [`large-message-handle-option`](/ticdc/ticdc-sink-to-kafka.md#handle-messages-that-exceed-the-kafka-topic-limit)                                | 新しく追加された | デフォルトでは空です。これは、メッセージ サイズが Kafka トピックの制限を超えると、変更フィードが失敗することを意味します。この構成が`"handle-key-only"`に設定されている場合、メッセージがサイズ制限を超えた場合、メッセージ サイズを減らすためにハンドル キーのみが送信されます。削減されたメッセージが依然として制限を超えている場合、変更フィードは失敗します。                                                                                                                                                                           |
| TiCDC          | [`sink.csv.binary-encoding-method`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                                      | 新しく追加された | バイナリ データのエンコード方法。 `'base64'`または`'hex'`です。デフォルト値は`'base64'`です。                                                                                                                                                                                                                                                                                                             |

### システムテーブル {#system-tables}

-   内部タイマーのメタデータを保存するための新しいシステム テーブル`mysql.tidb_timers`を追加します。

## 廃止された機能 {#deprecated-features}

-   TiDB

    -   統計の[`Fast Analyze`](/system-variables.md#tidb_enable_fast_analyze)機能 (実験的) は、v7.5.0 で非推奨になります。
    -   統計の[増分コレクション](https://docs.pingcap.com/tidb/v7.3/statistics#incremental-collection)機能は v7.5.0 で非推奨になります。

## 改善点 {#improvements}

-   TiDB

    -   新しいシステム変数[`tidb_opt_enable_non_eval_scalar_subquery`](/system-variables.md#tidb_opt_enable_non_eval_scalar_subquery-new-in-v730)を導入して、最適化フェーズ[#22076](https://github.com/pingcap/tidb/issues/22076) @ [ウィノロス](https://github.com/winoros)中にステートメント`EXPLAIN`が事前にサブクエリを実行するかどうかを制御します。
    -   [グローバルキル](/tidb-configuration-file.md#enable-global-kill-new-in-v610)が有効な場合、 <kbd>Ctrl+C</kbd> [#8854](https://github.com/pingcap/tidb/issues/8854) @ [ピンギュ](https://github.com/pingyu)を押すことで現在のセッションを終了できます。
    -   `IS_FREE_LOCK()`および`IS_USED_LOCK()`ロック関数[#44493](https://github.com/pingcap/tidb/issues/44493) @ [ドヴィーデン](https://github.com/dveeden)をサポート
    -   ディスク[#45125](https://github.com/pingcap/tidb/issues/45125) @ [ヤンケオ](https://github.com/YangKeao)からダンプされたチャンクを読み取るパフォーマンスを最適化します。
    -   Optimizer Fix Controls [#44855](https://github.com/pingcap/tidb/issues/44855) @ [時間と運命](https://github.com/time-and-fate)を使用して、インデックス結合の内部テーブルの過大評価の問題を最適化します。

-   TiKV

    -   `Max gap of safe-ts`と`Min safe ts region`メトリクスを追加し、 `tikv-ctl get-region-read-progress`コマンドを導入して、 resolved-tsとsafe-ts [#15082](https://github.com/tikv/tikv/issues/15082) @ [エキシウム](https://github.com/ekexium)のステータスをより適切に観察および診断します。

-   PD

    -   Swaggerサーバーが有効になっていない場合、デフォルトで Swagger API のブロックをサポート[#6786](https://github.com/tikv/pd/issues/6786) @ [バッファフライ](https://github.com/bufferflies)
    -   etcd [#6554](https://github.com/tikv/pd/issues/6554) [#6442](https://github.com/tikv/pd/issues/6442) @ [lhy1024](https://github.com/lhy1024)の高可用性を向上させます
    -   `GetRegions`リクエスト[#6835](https://github.com/tikv/pd/issues/6835) @ [lhy1024](https://github.com/lhy1024)のメモリ消費量を削減

-   TiFlash

    -   新しい DTFile 形式バージョン[`storage.format_version = 5`](/tiflash/tiflash-configuration.md)をサポートして、物理ファイルの数を削減します (実験的) [#7595](https://github.com/pingcap/tiflash/issues/7595) @ [ホンユニャン](https://github.com/hongyunyan)

-   ツール

    -   バックアップと復元 (BR)

        -   BRを使用してデータを Azure Blob Storage にバックアップする場合、サーバー側暗号化の暗号化スコープまたは暗号化キーのいずれかを指定できます[#45025](https://github.com/pingcap/tidb/issues/45025) @ [レヴルス](https://github.com/Leavrth)

    -   TiCDC

        -   オープン プロトコル出力のメッセージ サイズを最適化して、 `UPDATE`イベント[#9336](https://github.com/pingcap/tiflow/issues/9336) @ [3エースショーハンド](https://github.com/3AceShowHand)を送信するときに更新された列値のみを含めるようにします。
        -   Storage Sink は、HEX 形式のデータの 16 進エンコードをサポートするようになり、AWS DMS 形式仕様[#9373](https://github.com/pingcap/tiflow/issues/9373) @ [CharlesCheung96](https://github.com/CharlesCheung96)と互換性があります。
        -   Kafka Sink は、メッセージが大きすぎる場合に[ハンドルキーデータのみを送信する](/ticdc/ticdc-sink-to-kafka.md#handle-messages-that-exceed-the-kafka-topic-limit)をサポートし、メッセージのサイズを[#9382](https://github.com/pingcap/tiflow/issues/9382) @ [3エースショーハンド](https://github.com/3AceShowHand)に減らします。

## バグの修正 {#bug-fixes}

-   TiDB

    -   MySQL カーソル フェッチ プロトコルを使用すると、結果セットのメモリ消費量が`tidb_mem_quota_query`制限を超え、TiDB OOM が発生する可能性がある問題を修正します。修正後、TiDB は自動的に結果セットをディスクに書き込み、メモリ[#43233](https://github.com/pingcap/tidb/issues/43233) @ [ヤンケオ](https://github.com/YangKeao)を解放します。
    -   データ競合[#45561](https://github.com/pingcap/tidb/issues/45561) @ [ゲンリキ](https://github.com/gengliqi)によって引き起こされる TiDBpanic問題を修正
    -   `indexMerge`のクエリが[#45279](https://github.com/pingcap/tidb/issues/45279) @ [xzhangxian1008](https://github.com/xzhangxian1008)で強制終了されたときに発生するハングアップの問題を修正します。
    -   `tidb_enable_parallel_apply`が有効になっている場合、MPP モードでのクエリ結果が正しくない問題を修正します[#45299](https://github.com/pingcap/tidb/issues/45299) @ [ウィンドトーカー](https://github.com/windtalker)
    -   PD時間[#44822](https://github.com/pingcap/tidb/issues/44822) @ [ジグアン](https://github.com/zyguan)が急変した場合に`resolve lock`がハングすることがある問題を修正
    -   GC Resolve Locks ステップで一部の悲観的ロック[#45134](https://github.com/pingcap/tidb/issues/45134) @ [ミョンケミンタ](https://github.com/MyonKeminta)が見逃される可能性がある問題を修正します。
    -   動的プルーニング モード[#45007](https://github.com/pingcap/tidb/issues/45007) @ [定義2014](https://github.com/Defined2014)で`ORDER BY`を指定したクエリが誤った結果を返す問題を修正します。
    -   `DEFAULT`列の値[#45136](https://github.com/pingcap/tidb/issues/45136) @ [定義2014](https://github.com/Defined2014)と同じ列に`AUTO_INCREMENT`を指定できる問題を修正
    -   システム テーブル`INFORMATION_SCHEMA.TIKV_REGION_STATUS`をクエリすると、場合によっては誤った結果が返される問題を修正します[#45531](https://github.com/pingcap/tidb/issues/45531) @ [定義2014](https://github.com/Defined2014)
    -   場合によってはパーティション テーブルのプルーニングが正しく行われない問題を修正[#42273](https://github.com/pingcap/tidb/issues/42273) @ [ジフフスト](https://github.com/jiyfhust)
    -   パーティションテーブル[#42435](https://github.com/pingcap/tidb/issues/42435) @ [L-カエデ](https://github.com/L-maple)のパーティションを切り捨てるときにグローバルインデックスがクリアされない問題を修正
    -   1 つの TiDB ノード[#45022](https://github.com/pingcap/tidb/issues/45022) @ [ルクワンチャオ](https://github.com/lcwangchao)で障害が発生した後、他の TiDB ノードが TTL タスクを引き継がない問題を修正します。
    -   TTL [#45510](https://github.com/pingcap/tidb/issues/45510) @ [ルクワンチャオ](https://github.com/lcwangchao)実行時のメモリリークの問題を修正
    -   パーティションテーブル[#44966](https://github.com/pingcap/tidb/issues/44966) @ [リリンハイ](https://github.com/lilinghai)にデータを挿入するときに不正確なエラー メッセージが表示される問題を修正
    -   `INFORMATION_SCHEMA.TIFLASH_REPLICA`テーブル[#7795](https://github.com/pingcap/tiflash/issues/7795) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)の読み取り権限の問題を修正
    -   間違ったパーティションテーブル名[#44967](https://github.com/pingcap/tidb/issues/44967) @ [リバー2000i](https://github.com/River2000i)を使用するとエラーが発生する問題を修正
    -   `tidb_enable_dist_task`を有効にすると、場合によっては[#44440](https://github.com/pingcap/tidb/issues/44440) @ [タンジェンタ](https://github.com/tangenta)でインデックスの作成が停止する問題を修正
    -   BR [#44716](https://github.com/pingcap/tidb/issues/44716) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)を使用して`AUTO_ID_CACHE=1`持つテーブルを復元するときに発生する`duplicate entry`エラーを修正しました。
    -   `TRUNCATE TABLE`の実行にかかった時間が、 `ADMIN SHOW DDL JOBS` [#44785](https://github.com/pingcap/tidb/issues/44785) @ [タンジェンタ](https://github.com/tangenta)で示されるタスクの実行時間と一致しない問題を修正
    -   メタデータの読み取りに 1 回の DDL リース[#45176](https://github.com/pingcap/tidb/issues/45176) @ [ジムララ](https://github.com/zimulala)よりも長い時間がかかると TiDB のアップグレードが停止する問題を修正
    -   ステートメント内の`n`負の数[#44786](https://github.com/pingcap/tidb/issues/44786) @ [ゼボックス](https://github.com/xhebox)である場合、 `SELECT CAST(n AS CHAR)`ステートメントのクエリ結果が正しくない問題を修正します。
    -   `tidb_opt_agg_push_down`が有効になっている場合にクエリが間違った結果を返す可能性がある問題を修正します[#44795](https://github.com/pingcap/tidb/issues/44795) @ [アイリンキッド](https://github.com/AilinKid)
    -   `current_date()`クエリがプラン キャッシュ[#45086](https://github.com/pingcap/tidb/issues/45086) @ [qw4990](https://github.com/qw4990)を使用するときに発生する間違った結果の問題を修正します。

-   TiKV

    -   GC 中のデータ読み取りにより、まれに TiKVpanicが発生する可能性がある問題を修正[#15109](https://github.com/tikv/tikv/issues/15109) @ [ミョンケミンタ](https://github.com/MyonKeminta)

-   PD

    -   PD を再起動すると`default`リソース グループが再初期化される可能性がある問題を修正します[#6787](https://github.com/tikv/pd/issues/6787) @ [グロルフ](https://github.com/glorv)
    -   etcd がすでに開始されているが、クライアントがまだ接続していないときに、クライアントを呼び出すと PD がpanic[#6860](https://github.com/tikv/pd/issues/6860) @ [ヒューシャープ](https://github.com/HuSharp)になる可能性がある問題を修正します。
    -   リージョンの`health-check`出力が、リージョンID [#6560](https://github.com/tikv/pd/issues/6560) @ [Jmポテト](https://github.com/JmPotato)のクエリによって返されるリージョン情報と一致しない問題を修正します。
    -   `unsafe recovery`で失敗した学習者ピアが`auto-detect`モード[#6690](https://github.com/tikv/pd/issues/6690) @ [v01dstar](https://github.com/v01dstar)で無視される問題を修正
    -   配置ルールがルール[#6662](https://github.com/tikv/pd/issues/6662) @ [ルルンクス](https://github.com/rleungx)を満たさないTiFlash学習者を選択する問題を修正
    -   ルールチェッカーがピア[#6559](https://github.com/tikv/pd/issues/6559) @ [ノールーシュ](https://github.com/nolouch)を選択すると、異常なピアを削除できない問題を修正

-   TiFlash

    -   デッドロック[#7758](https://github.com/pingcap/tiflash/issues/7758) @ [ホンユニャン](https://github.com/hongyunyan)が原因で、 TiFlashがパーティション テーブルを正常に複製できない問題を修正します。
    -   `INFORMATION_SCHEMA.TIFLASH_REPLICA`システム テーブルにユーザーがアクセスする権限を持たないテーブルが含まれている問題を修正[#7795](https://github.com/pingcap/tiflash/issues/7795) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)
    -   同じ MPP タスク内に複数の HashAgg 演算子がある場合、MPP タスクのコンパイルに過度に時​​間がかかり、クエリのパフォーマンス[#7810](https://github.com/pingcap/tiflash/issues/7810) @ [シーライズ](https://github.com/SeaRise)に深刻な影響を与える可能性がある問題を修正します。

-   ツール

    -   TiCDC

        -   PD [#9294](https://github.com/pingcap/tiflow/issues/9294) @ [東門](https://github.com/asddongmen)が一時的に利用できないために変更フィードが失敗する問題を修正
        -   一部の TiCDC ノードがネットワーク[#9344](https://github.com/pingcap/tiflow/issues/9344) @ [CharlesCheung96](https://github.com/CharlesCheung96)から分離されている場合に発生する可能性があるデータの不整合の問題を修正します。
        -   Kafka シンクでエラーが発生すると、変更フィードの進行が無期限にブロックされる可能性がある問題を修正します[#9309](https://github.com/pingcap/tiflow/issues/9309) @ [ひっくり返る](https://github.com/hicqu)
        -   TiCDC ノードのステータスが[#9354](https://github.com/pingcap/tiflow/issues/9354) @ [スドジ](https://github.com/sdojjy)に変化したときに発生する可能性があるpanicの問題を修正しました。
        -   デフォルト値`ENUM` [#9259](https://github.com/pingcap/tiflow/issues/9259) @ [3エースショーハンド](https://github.com/3AceShowHand)のエンコード エラーを修正

    -   TiDB Lightning

        -   TiDB Lightning のインポート完了後にチェックサムを実行すると SSL エラー[#45462](https://github.com/pingcap/tidb/issues/45462) @ [D3ハンター](https://github.com/D3Hunter)が発生する可能性がある問題を修正
        -   論理インポート モードで、インポート中にダウンストリームのテーブルを削除すると、 TiDB Lightningメタデータが時間内に更新されなくなる可能性がある問題を修正します[#44614](https://github.com/pingcap/tidb/issues/44614) @ [dsダシュン](https://github.com/dsdashun)

## 貢献者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [チャールズジェン44](https://github.com/charleszheng44)
-   [ジズム](https://github.com/dhysum)
-   [ハイユクス](https://github.com/haiyux)
-   [ジャンファ](https://github.com/Jiang-Hua)
-   [ジル](https://github.com/Jille)
-   [ジフフスト](https://github.com/jiyfhust)
-   [クリシュナダットパンチャグヌラ](https://github.com/krishnaduttPanchagnula)
-   [L-カエデ](https://github.com/L-maple)
-   [ピンアンドブ](https://github.com/pingandb)
-   [テスト意志](https://github.com/testwill)
-   [てそくん](https://github.com/tisonkun)
-   [シュイファングリーンアイズ](https://github.com/xuyifangreeneyes)
-   [ヤムチナ](https://github.com/yumchina)
