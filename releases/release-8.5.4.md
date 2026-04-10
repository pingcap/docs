---
title: TiDB 8.5.4 Release Notes
summary: TiDB 8.5.4 の機能、互換性の変更点、改善点、およびバグ修正について学びましょう。
---

# TiDB 8.5.4 リリースノート {#tidb-8-5-4-release-notes}

発売日：2025年11月27日

TiDBバージョン：8.5.4

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb)| [本番環境への展開](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

## 特徴 {#features}

-   特定テーブルのデータ再配布のサポート（実験的） [#63260](https://github.com/pingcap/tidb/issues/63260) @[bufferflies](https://github.com/bufferflies)

    PDは、クラスタ内のすべてのTiKVノードにデータが可能な限り均等に分散されるように自動的にスケジュールします。ただし、この自動スケジュールはクラスタ全体を対象としています。場合によっては、クラスタ全体のデータ分散がバランスが取れていても、特定のテーブルのデータがTiKVノード間で不均等に分散される可能性があります。

    バージョン8.5.4以降では、 [`SHOW TABLE DISTRIBUTION`](https://docs.pingcap.com/tidb/v8.5/sql-statement-show-table-distribution/)ステートメントを使用して、特定のテーブルのデータがすべてのTiKVノードにどのように分散されているかを確認できます。データの分散が不均衡な場合は、 [`DISTRIBUTE TABLE`](https://docs.pingcap.com/tidb/v8.5/sql-statement-distribute-table)ステートメントを使用してテーブルのデータを再分散（実験的）し、負荷分散を改善できます。

    特定のテーブルのデータの再分配は、タイムアウト制限のある1回限りのタスクであることに注意してください。分配タスクがタイムアウト時間内に完了しない場合、自動的に終了します。

    詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v8.5/sql-statement-distribute-table)を参照してください。

-   DDL ステートメントに埋め込まれた`ANALYZE`をサポート [#57948](https://github.com/pingcap/tidb/issues/57948) @[terry1purcell](https://github.com/terry1purcell) @[AilinKid](https://github.com/AilinKid)

    この機能は、以下の種類のDDLステートメントに適用されます。

    -   新しいインデックスを作成するDDLステートメント： [`ADD INDEX`](/sql-statements/sql-statement-add-index.md)
    -   既存のインデックスを再編成するDDLステートメント： [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md)および[`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)

    この機能を有効にすると、TiDB は新規または再編成されたインデックスがユーザーに表示される前に`ANALYZE` (統計情報収集) 操作を自動的に実行します。これにより、インデックスの作成または再編成後に一時的に利用できなくなる統計情報によって、オプティマイザの推定値が不正確になったり、実行計画が変更されたりするのを防ぎます。

    詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v8.5/ddl_embedded_analyze)を参照してください。

-   パーティションテーブルの一意でない列に対するグローバルインデックスの作成をサポート [#58650](https://github.com/pingcap/tidb/issues/58650) @[Defined2014](https://github.com/Defined2014) @[mjonss](https://github.com/mjonss)

    バージョン8.3.0以降、TiDBではパーティションテーブルの一意列にグローバルインデックスを作成してクエリパフォーマンスを向上させることができます。ただし、一意でない列へのグローバルインデックスの作成はサポートされていませんでした。バージョン8.5.4以降、TiDBはこの制限を撤廃し、パーティションテーブルの一意でない列にもグローバルインデックスを作成できるようにすることで、グローバルインデックスの使いやすさを向上させています。

    詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v8.5/global-indexes/)を参照してください。

-   TiFlashの正常なシャットダウンをサポート [#10266](https://github.com/pingcap/tiflash/issues/10266) @[gengliqi](https://github.com/gengliqi)

    TiFlashサーバーをシャットダウンする際、 TiFlashは現在実行中のMPPタスクを構成可能なタイムアウト時間だけ継続させ、新しいMPPタスク要求を拒否するようになりました。デフォルトのタイムアウト時間は600秒で、 [`flash.graceful_wait_shutdown_timeout`](https://docs.pingcap.com/tidb/v8.5/tiflash-configuration#graceful_wait_shutdown_timeout-new-in-v854)設定項目を使用して調整できます。

    -   実行中のすべてのMPPタスクがタイムアウト期間内に終了した場合、 TiFlashは直ちにシャットダウンします。
    -   タイムアウト期間が経過しても未完了のMPPタスクが残っている場合、 TiFlashは強制的にシャットダウンします。

    詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v8.5/tiflash-configuration#graceful_wait_shutdown_timeout-new-in-v854)を参照してください。

-   パフォーマンス、拡張性、安定性を向上させるための新しいTiCDCアーキテクチャオプションを導入 [#442](https://github.com/pingcap/ticdc/issues/442) @[CharlesCheung96](https://github.com/CharlesCheung96)

    この新しいアーキテクチャは[従来のTiCDCアーキテクチャ](/ticdc/ticdc-classic-architecture.md)アーキテクチャの構成、使用法、API との互換性を維持しながら、TiCDC コア コンポーネントを再設計し、そのデータ処理ワークフローを最適化します。

    この新しいアーキテクチャを使用するように構成すると、TiCDC はほぼ線形のスケーラビリティを実現し、より低いリソース消費で数百万のテーブルを複製できます。また、変更フィードのレイテンシーを削減し、書き込みワークロードが高いシナリオ、頻繁な DDL 操作、クラスタのスケーリングにおいて、より安定したパフォーマンスを提供します。なお、この新しいアーキテクチャには現在、いくつか[初期の制約](https://docs.pingcap.com/tidb/v8.5/ticdc-architecture#limitations)があります。

    新しいアーキテクチャを使用するには、TiCDC 構成項目[`newarch`](https://docs.pingcap.com/tidb/v8.5/ticdc-server-config#newarch-new-in-v854-release1) `true`に設定します。

    詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v8.5/ticdc-architecture)を参照してください。

## 互換性の変更 {#compatibility-changes}

新規作成されたv8.5.3クラスタは、v8.5.4へスムーズにアップグレードできます。ただし、v8.5.4では、システム変数と構成パラメータの**デフォルト値の変更や動作調整が**いくつか導入されています。アップグレード前に、以下の点にご注意ください。

-   ほとんどの変更は、通常のアップグレードであれば安全です。ただし、クラスターにTiFlashやTiKVの圧縮構成のカスタマイズなど、パフォーマンスチューニングが施されている場合は、このセクションをよくお読みください。
-   バージョン8.5.4では、一部の従来のTiKV設定項目が非推奨となり、使用が推奨されなくなりました。代替として、このセクションで説明する新しいTiKV設定グループを使用することをお勧めします。

### システム変数 {#system-variables}

| 変数                                                                                                                                                     | 種類を変更する  | 説明                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`tidb_mpp_store_fail_ttl`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_mpp_store_fail_ttl)                                               | 修正済み     | デフォルト値を`60s`から`0s`に変更します。これにより、クエリの失敗を防ぐための遅延が不要になるため、TiDB は新しく起動したTiFlashノードにクエリを送信する前に待機する必要がなくなります。 [#61826](https://github.com/pingcap/tidb/issues/61826) [@genliqi](https://github.com/gengliqi)                                                                                                                                                                                                                    |
| [`tidb_replica_read`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_replica_read-new-in-v40)                                                | 修正済み     | バージョン8.5.4以降、この変数は読み取り専用のSQLステートメントにのみ適用されます。これにより、データ読み取りの安全性が向上し、他の機能との重複が軽減されます。 [#62856](https://github.com/pingcap/tidb/issues/62856) [@you06](https://github.com/you06)                                                                                                                                                                                                                                            |
| [`tidb_opt_enable_no_decorrelate_in_select`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_opt_enable_no_decorrelate_in_select-new-in-v854) | 新しく追加された | `SELECT`リスト内のサブクエリの関連付けを解除するかどうかを制御します。デフォルト値は`OFF`です。 [#51116](https://github.com/pingcap/tidb/issues/51116) [@terry1purcell](https://github.com/terry1purcell)                                                                                                                                                                                                                                                         |
| [`tidb_opt_enable_semi_join_rewrite`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_opt_enable_semi_join_rewrite-new-in-v854)               | 新しく追加された | `EXISTS`サブクエリを書き換えるかどうかを制御します。デフォルト値は`OFF`です。 [#44850](https://github.com/pingcap/tidb/issues/44850) [@terry1purcell](https://github.com/terry1purcell)                                                                                                                                                                                                                                                                  |
| [`tidb_stats_update_during_ddl`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_stats_update_during_ddl-new-in-v854)                         | 新しく追加された | [DDLステートメントに埋め込まれた`ANALYZE`](https://docs.pingcap.com/tidb/v8.5/ddl_embedded_analyze) 。デフォルト値は`OFF`です。有効にすると、 `ADD INDEX` DDL ステートメントは実行中に新しいインデックスの統計情報を収集し、オプティマイザがインデックスの追加直後にインデックスを使用できるようにします。この変数を有効にすると、大きなテーブルにインデックスを追加する際の DDL 実行時間が長くなる可能性があることに注意してください。 [#57948](https://github.com/pingcap/tidb/issues/57948) [@terry1purcell](https://github.com/terry1purcell) [@AilinKid](https://github.com/AilinKid) |

### コンフィグレーションパラメータ {#configuration-parameters}

| コンフィグレーションファイルまたはコンポーネント | コンフィグレーションパラメータ                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | 種類を変更する  | 説明                                                                                                                                                                                                                                                                                                     |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ティクヴ                     | [`rocksdb.max-manifest-file-size`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#max-manifest-file-size)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | 修正済み     | 単一の TiKV ノードに多数の SST ファイルが含まれている場合に、全体的なパフォーマンスに影響を与える可能性のある頻繁なマニフェスト ファイル圧縮を回避するため、デフォルト値を`128MiB` `256MiB`に変更します。 [#18889](https://github.com/tikv/tikv/issues/18889) [@glorv](https://github.com/glorv)                                                                                             |
| ティクヴ                     | [`server.grpc-raft-conn-num`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#grpc-raft-conn-num)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | 修正済み     | デフォルト値を`1`から`MAX(1, MIN(4, CPU cores / 8))`に変更します。これにより、gRPC 関連のスレッド設定が CPU コア数に応じて調整されるようになります。CPU コア数が 32 以上の場合、デフォルトの最大接続数は 4 になります。 [#18806](https://github.com/tikv/tikv/issues/18806) [@LykxSassinator](https://github.com/LykxSassinator)                                                       |
| ティクヴ                     | [`server.grpc-concurrency`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#grpc-concurrency)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | 修正済み     | デフォルト値を`5`から`grpc-raft-conn-num * 3 + 2`に変更します。これにより、gRPC 関連のスレッド設定が CPU コア数に合わせて調整されるようになります。 [#18806](https://github.com/tikv/tikv/issues/18806) [@LykxSassinator](https://github.com/LykxSassinator)                                                                                                |
| ティクヴ                     | <li>[`region-compact-check-interval`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-check-interval)</li><li>[`region-compact-check-step`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-check-step)</li><li>[`region-compact-min-tombstones`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-min-tombstones)</li><li>[`region-compact-tombstones-percent`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-tombstones-percent)</li><li>[`region-compact-min-redundant-rows`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-min-redundant-rows-new-in-v710)</li><li>[`region-compact-redundant-rows-percent`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-redundant-rows-percent-new-in-v710)</li>                                                                                                                                                                                                                                                           | 非推奨      | これらの設定項目は、自動圧縮動作を制御する[`gc.auto-compaction`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#gcauto-compaction)設定グループに置き換えられます。 [#18727](https://github.com/tikv/tikv/issues/18727) [@v01dstar](https://github.com/v01dstar)                                                                 |
| ティクヴ                     | [`gc.auto-compaction`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#gcauto-compaction)設定グループ:<ul><li> [`gc.auto-compaction.check-interval`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#check-interval-new-in-v757-and-v854)</li><li> [`gc.auto-compaction.tombstone-num-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#tombstone-num-threshold-new-in-v757-and-v854)</li><li> [`gc.auto-compaction.tombstone-percent-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#tombstone-percent-threshold-new-in-v757-and-v854)</li><li> [`gc.auto-compaction.redundant-rows-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#redundant-rows-threshold-new-in-v757-and-v854)</li><li> [`gc.auto-compaction.redundant-rows-percent-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#redundant-rows-percent-threshold-new-in-v757-and-v854)</li><li> [`gc.auto-compaction.bottommost-level-force`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#bottommost-level-force-new-in-v757-and-v854)</li></ul> | 新しく追加された | この構成グループは、自動圧縮動作を制御します。 [#18727](https://github.com/tikv/tikv/issues/18727) [@v01dstar](https://github.com/v01dstar)                                                                                                                                                                                   |
| TiFlash                  | [`flash.graceful_wait_shutdown_timeout`](https://docs.pingcap.com/tidb/v8.5/tiflash-configuration#graceful_wait_shutdown_timeout-new-in-v854)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | 新しく追加された | TiFlashの正常なシャットダウンの最大待機時間（秒単位）を制御します。デフォルト値は`600`です。TiFlashをシャットダウンする際、未完了のMPPタスクの実行は継続されますが、新しいMPPタスクは受け付けなくなります。すべてのMPPタスクがタイムアウト前に完了した場合、 TiFlashは直ちにシャットダウンします。そうでない場合は、タイムアウト後に強制的にシャットダウンされます。 [#10266](https://github.com/pingcap/tiflash/issues/10266) [@genliqi](https://github.com/gengliqi) |

### MySQLとの互換性 {#mysql-compatibility}

バージョン 8.5.4 以降、TiDB は`DECIMAL`列にデータを挿入する際の動作を MySQL と同期させました。小数点以下の桁数が列の定義済みスケールを超えた場合、TiDB は余分な桁を自動的に切り捨て、切り捨てられたデータを正常に挿入します。小数点以下の桁数に関係なく、切り捨てられたデータは挿入されます。以前の TiDB バージョンでは、挿入される`DECIMAL`値の小数点以下の桁数が 72 を超えると、挿入は失敗し、エラーが返されました。詳細については、 [JDBCを使用してTiDBに接続する](https://docs.pingcap.com/tidb/v8.5/dev-guide-sample-application-java-jdbc#mysql-compatibility)

## 改善点 {#improvements}

-   TiDB

    -   `semi_join_rewrite`サブクエリのセミテーブル結合に`IN`ヒントを適用することをサポートする [#58829](https://github.com/pingcap/tidb/issues/58829) @[qw4990](https://github.com/qw4990)
    -   `tidb_opt_ordering_index_selectivity_ratio`システム変数が有効になったときに推定戦略を最適化する [#62817](https://github.com/pingcap/tidb/issues/62817) @[terry1purcell](https://github.com/terry1purcell)
    -   オプティマイザの選択ロジックを調整して、特定のシナリオで新しく作成されたインデックスが選択される可能性が高くなるようにする [#57948](https://github.com/pingcap/tidb/issues/57948) @[terry1purcell](https://github.com/terry1purcell)
    -   一意の値の数が少ない列（NDV）のクエリ推定ロジックを最適化する [#61792](https://github.com/pingcap/tidb/issues/61792) @[terry1purcell](https://github.com/terry1purcell)
    -   `LIMIT OFFSET`を含む Index Join クエリの推定戦略を最適化する [#45077](https://github.com/pingcap/tidb/issues/45077) @[qw4990](https://github.com/qw4990)
    -   統計情報が時間内に収集されない場合の範囲外推定戦略を最適化する [#58068](https://github.com/pingcap/tidb/issues/58068) @[terry1purcell](https://github.com/terry1purcell)
    -   Grafana の**パフォーマンス概要**&gt; **SQL 実行時間概要**パネルに`backoff`メトリックを追加してデバッグを容易にします [#61441](https://github.com/pingcap/tidb/issues/61441) @[dbsid](https://github.com/dbsid)
    -   監査ログ プラグインにステートメント ID 情報を追加 [#63525](https://github.com/pingcap/tidb/issues/63525) @[YangKeao](https://github.com/YangKeao)

-   ティクヴ

    -   BRモジュール内の特定の自動回復可能なエラーのログレベルを`ERROR`から`WARN`に変更して、不要なアラートを削減します [#18493](https://github.com/tikv/tikv/issues/18493) @[YuJuncen](https://github.com/YuJuncen)
    -   不要なアラートを減らすため、特定の TiKV エラーのログレベルを`ERROR`から`WARN`に変更します [#18745](https://github.com/tikv/tikv/issues/18745) @[exit-code-1](https://github.com/exit-code-1)
    -   RaftモジュールのGCチェックプロセスを2つのフェーズに分割し、リージョン内の冗長なMVCCバージョンのガベージコレクションの効率を向上させる [#18695](https://github.com/tikv/tikv/issues/18695) @[v01dstar](https://github.com/v01dstar)
    -   GCセーフポイントとRocksDB統計に基づいてMVCC冗長性を計算し、圧縮の効率と精度を向上させる [#18697](https://github.com/tikv/tikv/issues/18697) @[v01dstar](https://github.com/v01dstar)
    -   リージョン MVCC の GC 処理ロジックを GC ワーカー スレッドで実行するように変更し、GC 処理ロジック全体を統一します [#18727](https://github.com/tikv/tikv/issues/18727) @[v01dstar](https://github.com/v01dstar)
    -   デフォルトのgRPCスレッドプールサイズの計算方法を最適化し、固定値ではなくCPUクォータの合計に基づいて動的に計算するようにすることで、gRPCスレッド不足によるパフォーマンスボトルネックを回避します [#18613](https://github.com/tikv/tikv/issues/18613) @[LykxSassinator](https://github.com/LykxSassinator)
    -   多数のSSTファイルが存在する環境における非同期スナップショットおよび書き込み操作のテールレイテンシーを最適化する [#18743](https://github.com/tikv/tikv/issues/18743) @[Connor1996](https://github.com/Connor1996)

-   PD

    -   不要なエラーログを削減 [#9370](https://github.com/tikv/pd/issues/9370) @[bufferflies](https://github.com/bufferflies)
    -   Golangのバージョンを1.23.0から1.23.12にアップグレードし、関連する依存関係を更新します [#9788](https://github.com/tikv/pd/issues/9788) @[JmPotato](https://github.com/JmPotato)
    -   テーブルレベルで散布領域をサポートして、 `scatter-role`と`engine`の次元全体にバランスの取れた分布を実現します [#8986](https://github.com/tikv/pd/issues/8986) @[bufferflies](https://github.com/bufferflies)

-   TiFlash

    -   `TableScan`パフォーマンスを向上させるために不要なデータ読み取りをスキップします [#9875](https://github.com/pingcap/tiflash/issues/9875) @[gengliqi](https://github.com/gengliqi)
    -   TiFlash [#10361](https://github.com/pingcap/tiflash/issues/10361) 10361 @ジェイソン・ファンで、多くの列とスパース データ (つまり、大量の`TableScan` } または空の値) を含む広いテーブルでの { `NULL`パフォーマンスを最適[ジェイソン・ファン](https://github.com/JaySon-Huang)ます。
    -   多くのテーブルを持つクラスターにベクトル インデックスを追加することによって発生するTiFlash CPU オーバーヘッドを削減 [#10357](https://github.com/pingcap/tiflash/issues/10357) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   無駄なRaftコマンド処理時の不要なログ出力を最小限にしてログ量を削減 [#10467](https://github.com/pingcap/tiflash/issues/10467) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   TiFlashの小さなパーティション分割テーブルでの`TableScan`パフォーマンスを向上 [#10487](https://github.com/pingcap/tiflash/issues/10487) @[JaySon-Huang](https://github.com/JaySon-Huang)

-   ツール

    -   TiDBデータ移行（DM）

        -   上流の`GTID_MODE`を取得する際に、大文字小文字を区別しないマッチングをサポートする [#12167](https://github.com/pingcap/tiflow/issues/12167) @[OliverS929](https://github.com/OliverS929)

## バグ修正 {#bug-fixes}

-   TiDB

    -   `use index`が`tidb_isolation_read_engines`に設定されている場合、 `tiflash`ヒントが [#60869](https://github.com/pingcap/tidb/issues/60869) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   `max_execution_time`が`SELECT FOR UPDATE`ステートメントに適用されない問題を修正 [#62960](https://github.com/pingcap/tidb/issues/62960) @[ekexium](https://github.com/ekexium)
    -   月や年をまたいだ行数の推定値が大幅に過大評価される問題を修正 [#50080](https://github.com/pingcap/tidb/issues/50080) @[terry1purcell](https://github.com/terry1purcell)
    -   プリペアドステートメントにおける`Decimal`タイプの処理が MySQL と矛盾する問題を修正 [#62602](https://github.com/pingcap/tidb/issues/62602) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan)
    -   `TRUNCATE()`関数内の短いパスが正しく処理されない問題を修正しました [#57608](https://github.com/pingcap/tidb/issues/57608) @[xzhangxian1008](https://github.com/xzhangxian1008)
    -   `Out Of Quota For Local Temporary Space`エラーが発生した際に、スピルしたファイルが完全に削除されない可能性がある問題を修正しました [#63216](https://github.com/pingcap/tidb/issues/63216) @[xzhangxian1008](https://github.com/xzhangxian1008)
    -   `INFORMATION_SCHEMA`テーブルに対して正規表現を使用したクエリが誤った結果を返す可能性がある問題を修正しました [#62347](https://github.com/pingcap/tidb/issues/62347) @[River2000i](https://github.com/River2000i)
    -   TiDBがPDからタイムスタンプを取得できなかった場合にエラーを返さない問題を修正します [#58871](https://github.com/pingcap/tidb/issues/58871) @[joechenrh](https://github.com/joechenrh)
    -   `MODIFY COLUMN`ステートメントの実行中に、所有者 TiDB インスタンスと非所有者 TiDB インスタンス間でクエリ結果が異なる問題を修正します [#60264](https://github.com/pingcap/tidb/issues/60264) @[tangenta](https://github.com/tangenta)
    -   `ADMIN ALTER DDL JOBS`ステートメントでパラメータを動的に変更した後に誤ったパラメータ値が表示される問題を修正します [#63201](https://github.com/pingcap/tidb/issues/63201) @[fzzf678](https://github.com/fzzf678)
    -   トランザクション内でインデックスを追加する際にGCセーフポイントが進まない問題を修正 [#62424](https://github.com/pingcap/tidb/issues/62424) @[wjhuang2016](https://github.com/wjhuang2016)
    -   過度に大きな SST ファイルを L0 に取り込むとフロー制御がトリガーされる問題を修正 [#63466](https://github.com/pingcap/tidb/issues/63466) @[CbcWestwolf](https://github.com/CbcWestwolf)
    -   CPUとメモリの比率が1:2の場合にグローバルソートがブロックされる問題を修正 [#60951](https://github.com/pingcap/tidb/issues/60951) @[wjhuang2016](https://github.com/wjhuang2016)
    -   タスク数が16を超えると、保留中の分散実行フレームワーク（DXF）タスクをキャンセルできない問題を修正しました [#63896](https://github.com/pingcap/tidb/issues/63896) @[D3Hunter](https://github.com/D3Hunter)
    -   DXFタスクがキャンセルされた後、他のタスクが終了しない問題を修正します [#63927](https://github.com/pingcap/tidb/issues/63927) @[D3Hunter](https://github.com/D3Hunter)
    -   `Apply`演算子の同時実行（ `tidb_enable_parallel_apply = on` ）を有効にすると、クローン実装が欠落しているためにプラン生成が失敗する問題を修正しました [#59863](https://github.com/pingcap/tidb/issues/59863) @[hawkingrei](https://github.com/hawkingrei)
    -   `ATAN2`関数を使用すると誤った結果が生じる可能性がある問題を修正しました [#60093](https://github.com/pingcap/tidb/issues/60093) @[guo-shaoge](https://github.com/guo-shaoge)
    -   `select 1 from dual`がインスタンスレベルのプランキャッシュを使用できない問題を修正 [#63075](https://github.com/pingcap/tidb/issues/63075) @[time-and-fate](https://github.com/time-and-fate)
    -   参加順序を変更するとプランナーが失敗する可能性がある問題を修正 [#61715](https://github.com/pingcap/tidb/issues/61715) @[hawkingrei](https://github.com/hawkingrei)
    -   `set_var`ヒントをバインディングで使用すると、変数が元の設定に戻らない問題を修正します [#59822](https://github.com/pingcap/tidb/issues/59822) @[wddevries](https://github.com/wddevries)
    -   `ONLY_FULL_GROUP_BY`負の値に設定すると検証が失敗する問題を修正 [#62617](https://github.com/pingcap/tidb/issues/62617) @[AilinKid](https://github.com/AilinKid)
    -   `ONLY_FULL_GROUP_BY`チェックで大文字と小文字が区別されない問題を修正 [#62672](https://github.com/pingcap/tidb/issues/62672) @[AilinKid](https://github.com/AilinKid)
    -   DP結合順序アルゴリズムが誤ったプランを生成する可能性がある問題を修正 [#63353](https://github.com/pingcap/tidb/issues/63353) @[winoros](https://github.com/winoros)
    -   外部結合を内部結合に書き換えると誤った結果が生じる可能性がある問題を修正 [#61327](https://github.com/pingcap/tidb/issues/61327) @[hawkingrei](https://github.com/hawkingrei)
    -   特定のクエリを実行すると内部panicが発生する可能性がある問題を修正 [#58600](https://github.com/pingcap/tidb/issues/58600) @[Defined2014](https://github.com/Defined2014)
    -   グローバルインデックスが特定の`ALTER PARTITION`操作中に誤ったデータを読み取る可能性がある問題を修正 [#64084](https://github.com/pingcap/tidb/pull/64084) @[mjonss](https://github.com/mjonss)
    -   場合によってはグローバルインデックスが誤った結果を返す可能性がある問題を修正 [#61083](https://github.com/pingcap/tidb/issues/61083) @[Defined2014](https://github.com/Defined2014)
    -   `character_set_results`が誤った文字を置き換えるのではなく切り捨ててしまう問題を修正 [#61085](https://github.com/pingcap/tidb/issues/61085) @[xhebox](https://github.com/xhebox)
    -   `ADD COLUMN`と`UPDATE`ステートメントを同時に実行するとエラーが発生する可能性がある問題を修正しました [#60047](https://github.com/pingcap/tidb/issues/60047) @[L-maple](https://github.com/L-maple)
    -   マージ結合時にコスト計算時にフィルタ条件が省略される可能性がある問題を修正 [#62917](https://github.com/pingcap/tidb/issues/62917) @[qw4990](https://github.com/qw4990)

-   PD

    -   PDクライアントの再試行戦略が正しく初期化されない問題を修正 [#9013](https://github.com/tikv/pd/issues/9013) @[rleungx](https://github.com/rleungx)
    -   TSO HTTP API `/config`および`/members`が誤った結果を返す問題を修正します [#9797](https://github.com/tikv/pd/issues/9797) @[lhy1024](https://github.com/lhy1024)
    -   TSOFollowerプロキシの誤ったエラー処理ロジックを修正 [#9188](https://github.com/tikv/pd/issues/9188) @[Tema](https://github.com/Tema)
    -   バケットのレポートが無効になった後でもバケットの分割が機能する問題を修正 [#9726](https://github.com/tikv/pd/issues/9726) @[bufferflies](https://github.com/bufferflies)
    -   リソースマネージャがトークンを誤って割り当て、クエリが停止する問題を修正しました [#9455](https://github.com/tikv/pd/issues/9455) @[JmPotato](https://github.com/JmPotato)
    -   PDリーダーが交代した後、配置ルールが有効にならない問題を修正 [#9602](https://github.com/tikv/pd/issues/9602) [okJiang](https://github.com/okJiang)
    -   PDが科学表記の大きな数値を解析できない場合があり、その結果、一部のTTL関連の設定が有効にならない問題を修正します。 [#9343](https://github.com/tikv/pd/issues/9343) @[lhy1024](https://github.com/lhy1024)

-   TiFlash

    -   クエリ対象の列に多数の`NULL`値が含まれている場合にクエリが失敗する可能性がある問題を修正 [#10340](https://github.com/pingcap/tiflash/issues/10340) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   TiFlashがRU消費量の統計情報を水増しして生成する問題を修正 [#10380](https://github.com/pingcap/tiflash/issues/10380) @[JinheLin](https://github.com/JinheLin)
    -   分離されたstorageとコンピューティングアーキテクチャの下で低速クエリが存在する場合にTiFlash でOOM が発生する可能性がある問題を修正 [#10278](https://github.com/pingcap/tiflash/issues/10278) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   分散storageおよびコンピューティングアーキテクチャ下でTiFlashと S3 の間でネットワーク分割が発生した場合、 TiFlash が無期限に再試行する可能性がある問題を修正 [#10424](https://github.com/pingcap/tiflash/issues/10424) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   `FLOOR()`関数と`CEIL()`関数のパラメータ`DECIMAL`型の場合、誤った結果を返すことがある問題を修正 [#10365](https://github.com/pingcap/tiflash/issues/10365) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan)

-   ツール

    -   バックアップと復元 (BR)

        -   ログ バックアップの zstd 圧縮が有効にならず、出力が圧縮されないままになる問題を修正 [#18836](https://github.com/tikv/tikv/issues/18836) @[3pointer](https://github.com/3pointer)
        -   Azure Blob Storageへのデータバックアップ時にフラッシュ操作が時々遅くなる問題を修正 [#18410](https://github.com/tikv/tikv/issues/18410) @[YuJuncen](https://github.com/YuJuncen)
        -   ファイル削除が失敗した場合に`log truncate`が発生する可能性がある問題を修正 [#63358](https://github.com/pingcap/tidb/issues/63358) @[YuJuncen](https://github.com/YuJuncen)
        -   バックアップ中に`--checksum`を`false`に設定すると、リストア後に`count`テーブルの`mysql.stats_meta`列が`0`になる可能性がある問題を修正 [#60978](https://github.com/pingcap/tidb/issues/60978) @[Leavrth](https://github.com/Leavrth)
        -   S3互換storageサービスの帯域幅制限が有効になっている場合に、 BRがこれらのサービスからデータを復元できない可能性を低減する [#18846](https://github.com/tikv/tikv/issues/18846) @[kennytm](https://github.com/kennytm)
        -   `log backup observer`リージョン上の観測を失う可能性があり、ログバックアップの進行が進まなくなる問題を修正しました [#18243](https://github.com/tikv/tikv/issues/18243) @[Leavrth](https://github.com/Leavrth)
        -   バックアップされたテーブルに特定の特殊スキーマが含まれている場合に`restore point`作成が失敗する問題を修正します [#63663](https://github.com/pingcap/tidb/issues/63663) @[RidRisR](https://github.com/RidRisR)

    -   TiCDC

        -   仮想列を含む列型パーティションディスパッチャを構成する際に発生する可能性のあるpanicを修正します [#12241](https://github.com/pingcap/tiflow/issues/12241) @[wk989898](https://github.com/wk989898)
        -   DDLプーラーを閉じるときに発生する可能性のあるpanicを修正しました [#12244](https://github.com/pingcap/tiflow/issues/12244) @[wk989898](https://github.com/wk989898)
        -   `ignore-txn-start-ts`設定の`filter`パラメーターを使用して、サポートされていない DDL タイプをフィルタリングする機能をサポートする [#12286](https://github.com/pingcap/tiflow/issues/12286) @[asddongmen](https://github.com/asddongmen)
        -   Azure Blob Storage をダウンストリームとして使用している場合、changefeed タスクが停止する可能性がある問題を修正します [#12277](https://github.com/pingcap/tiflow/issues/12277) @[zurakutsia](https://github.com/zurakutsia)
        -   `DROP FOREIGN KEY` DDL がダウンストリームにレプリケートされない問題を修正 [#12328](https://github.com/pingcap/tiflow/issues/12328) @[3AceShowHand](https://github.com/3AceShowHand)
        -   リージョンサブスクリプション中にロールバックと事前書き込みエントリが発生したときに TiCDC がpanicになる可能性がある問題を修正 [#19048](https://github.com/tikv/tikv/issues/19048) @[3AceShowHand](https://github.com/3AceShowHand)
        -   TiKV のアサーション エラーが TiCDC をpanic可能性がある問題を修正 [#18498](https://github.com/tikv/tikv/issues/18498) @[tharanga](https://github.com/tharanga)
