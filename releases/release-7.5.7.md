---
title: TiDB 7.5.7 Release Notes
summary: TiDB 7.5.7 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 7.5.7 リリースノート {#tidb-7-5-7-release-notes}

発売日：2025年9月4日

TiDB バージョン: 7.5.7

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   デフォルト値の[`tidb_enable_historical_stats`](https://docs.pingcap.com/tidb/v7.5/system-variables/#tidb_enable_historical_stats)を`ON`から`OFF`に変更します。これにより、潜在的な安定性の問題を回避するために履歴統計がオフになります[＃53048](https://github.com/pingcap/tidb/issues/53048) @ [hawkingrei](https://github.com/hawkingrei)
-   TiKV は以下の設定項目を廃止し、自動圧縮動作を制御する新しい[`gc.auto-compaction`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file/#gcauto-compaction)設定グループに置き換えます。 [＃18727](https://github.com/tikv/tikv/issues/18727) @ [v01dstar](https://github.com/v01dstar)

    -   非推奨の構成項目: [`region-compact-check-interval`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#region-compact-check-interval) 、 [`region-compact-check-step`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#region-compact-check-step) 、 [`region-compact-min-tombstones`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#region-compact-min-tombstones) 、 [`region-compact-tombstones-percent`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#region-compact-tombstones-percent) 、 [`region-compact-min-redundant-rows`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#region-compact-min-redundant-rows-new-in-v710) 、および[`region-compact-redundant-rows-percent`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#region-compact-redundant-rows-percent-new-in-v710) 。
    -   新しい[`gc.auto-compaction.tombstone-percent-threshold`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#tombstone-percent-threshold-new-in-v757) [`gc.auto-compaction.redundant-rows-threshold`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#redundant-rows-threshold-new-in-v757) : [`gc.auto-compaction.check-interval`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#check-interval-new-in-v757) [`gc.auto-compaction.redundant-rows-percent-threshold`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#redundant-rows-percent-threshold-new-in-v757)および[`gc.auto-compaction.bottommost-level-force`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#bottommost-level-force-new-in-v757) [`gc.auto-compaction.tombstone-num-threshold`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#tombstone-num-threshold-new-in-v757)

## 改善点 {#improvements}

-   TiDB

    -   データインポート中のリージョン分割とデータ取り込みのためのフロー制御インターフェースを追加します [＃61553](https://github.com/pingcap/tidb/issues/61553) @ [tangenta](https://github.com/tangenta)
    -   大容量データを持つテーブルに対して単純なクエリを実行する際に、データ分布情報を取得するパフォーマンスを最適化します[＃53850](https://github.com/pingcap/tidb/issues/53850) @ [you06](https://github.com/you06)
    -   インデックス追加中の TiKV への書き込み速度を観察するための監視メトリックを追加します。 [＃60925](https://github.com/pingcap/tidb/issues/60925) @ [CbcWestwolf](https://github.com/CbcWestwolf)
    -   DDL実行中のDMLのロックロジックを最適化し、DMLとDDL間のロック競合を軽減することで、一部のシナリオでDDLのパフォーマンスが向上します。ただし、セカンダリインデックスのロック操作が追加されるため、DMLのパフォーマンスがわずかに低下する可能性があります[＃62337](https://github.com/pingcap/tidb/issues/62337) @ [lcwangchao](https://github.com/lcwangchao)
    -   システム変数[`tidb_opt_ordering_index_selectivity_threshold`](/system-variables.md#tidb_opt_ordering_index_selectivity_threshold-new-in-v700) `1`に設定されている場合の動作を改善し、この変数の制御機能を強化します。 [＃60242](https://github.com/pingcap/tidb/issues/60242) @ [time-and-fate](https://github.com/time-and-fate)
    -   `ANALYZE`文実行後にクラスタ全体の統計を更新することを回避し、実行時間を`ANALYZE` に短縮します。 [＃57631](https://github.com/pingcap/tidb/issues/57631) @ [0xPoe](https://github.com/0xPoe)
    -   `NOT NULL`制約を持つ列の定数畳み込みをサポートし、 `IS NULL`評価を`FALSE` に畳み込みます。 [＃62050](https://github.com/pingcap/tidb/issues/62050) @ [hawkingrei](https://github.com/hawkingrei)
    -   オプティマイザは、より多くの種類の`JOIN`操作で定数伝播をサポートします。 [＃51700](https://github.com/pingcap/tidb/issues/51700) @ [hawkingrei](https://github.com/hawkingrei)
    -   DML 操作と DDL 操作の間に大規模なロック競合が存在する場合の一時インデックスのマージのパフォーマンスを向上[＃61433](https://github.com/pingcap/tidb/issues/61433) @ [tangenta](https://github.com/tangenta)

-   TiKV

    -   TiKV圧縮のトリガーロジックを最適化して、すべてのデータセグメントを再利用効率の順に処理し、MVCC冗長データのパフォーマンスへの影響を軽減します。 [＃18571](https://github.com/tikv/tikv/issues/18571) @ [v01dstar](https://github.com/v01dstar)
    -   多数の SST ファイルが存在する環境での非同期スナップショットおよび書き込み操作のテールレイテンシーを最適化します[＃18743](https://github.com/tikv/tikv/issues/18743) @ [Connor1996](https://github.com/Connor1996)
    -   空のテーブルと小さなリージョンシナリオでのリージョン結合の速度を改善 [＃17376](https://github.com/tikv/tikv/issues/17376) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   Raftstoreの`CompactedEvent`処理を`split-check`ワーカーに移動して最適化し、メインのRaftstoreスレッドのブロッキングを削減します。 [＃18532](https://github.com/tikv/tikv/issues/18532) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   スレッドごとのメモリ使用量のメトリックを追加します。 [＃15927](https://github.com/tikv/tikv/issues/15927) @ [Connor1996](https://github.com/Connor1996)
    -   SST の取り込みが遅すぎる場合は`SST ingest is experiencing slowdowns`のみをログに記録し、パフォーマンスのジッターを回避するために`get_sst_key_ranges`呼び出しをスキップします[＃18549](https://github.com/tikv/tikv/issues/18549) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   ログの適用を待つために TiKV を再起動するときに発生する不安定なアクセス遅延を最適化し、TiKV の安定性を向上しました。 [＃15874](https://github.com/tikv/tikv/issues/15874) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   残留データのクリーンアップメカニズムを最適化して、リクエストのレイテンシーへの影響を軽減します。 [＃18107](https://github.com/tikv/tikv/issues/18107) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   Raft Engineの`fetch_entries_to`のパフォーマンスを最適化して競合を減らし、混合ワークロードでのパフォーマンスを向上します。 [＃18605](https://github.com/tikv/tikv/issues/18605) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   書き込み操作のフロー制御構成の動的な変更をサポート[＃17395](https://github.com/tikv/tikv/issues/17395) @ [glorv](https://github.com/glorv)
    -   フォアグラウンド書き込みをブロックせずにSSTファイルの取り込みをサポートし、レイテンシーの影響を軽減します。 [＃18081](https://github.com/tikv/tikv/issues/18081) @ [hhwyt](https://github.com/hhwyt)
    -   KvDB と RaftDB が別々のマウント パスを使用する場合の KvDB ディスクの I/O ジッターの検出メカニズムを最適化します。 [＃18463](https://github.com/tikv/tikv/issues/18463) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   ピアのスローログを追加し、メッセージを保存します [＃16600](https://github.com/tikv/tikv/issues/16600) @ [Connor1996](https://github.com/Connor1996)

-   PD

    -   Prometheus に GO ランタイム関連の監視メトリクスを追加 [＃8931](https://github.com/tikv/pd/issues/8931) @ [bufferflies](https://github.com/bufferflies)
    -   不要なエラーログをつ@ [bufferflies](https://github.com/bufferflies)削減 [＃9370](https://github.com/tikv/pd/issues/9370)

-   TiFlash

    -   ワイドテーブルシナリオにおけるTiFlash OOM リスクの観測可能性を強化[＃10272](https://github.com/pingcap/tiflash/issues/10272) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   storageスナップショットを取得する際の最大再試行回数を増やし、大規模なテーブルのクエリの安定性を向上させます[＃10300](https://github.com/pingcap/tiflash/issues/10300) @ [JaySon-Huang](https://github.com/JaySon-Huang)

-   ツール

    -   Backup & Restore (BR)

        -   TiDBをAmazon EC2に導入する場合、 BRはAWSインスタンスメタデータサービスバージョン2（IMDSv2）をサポートします。EC2インスタンスを設定することで、 BRがインスタンスに関連付けられたIAMロールを使用してAmazon S3への適切なアクセス権限を付与できるようになります[＃16443](https://github.com/tikv/tikv/issues/16443) @ [pingyu](https://github.com/pingyu)
        -   TiKVのダウンロードAPIは、バックアップファイルをダウンロードする際に特定の時間範囲内のデータをフィルタリングすることをサポートしており、復元時に古いデータバージョンや将来のデータバージョンがインポートされるのを回避します[＃18399](https://github.com/tikv/tikv/issues/18399) @ [3pointer](https://github.com/3pointer)

## バグ修正 {#bug-fixes}

-   TiDB

    -   `IndexMerge`および`IndexLookUp`演算子の共有 KV リクエストがクエリをプッシュダウンするときにデータ競合を引き起こす問題を修正しました。 [＃60175](https://github.com/pingcap/tidb/issues/60175) @ [you06](https://github.com/you06)
    -   ハッシュ集計演算子における潜在的な goroutine リークの問題を修正しました。 [＃58004](https://github.com/pingcap/tidb/issues/58004) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   生成された列のインデックスが表示に設定されている場合、MPP プランが選択されない可能性がある問題を修正しました。 [＃47766](https://github.com/pingcap/tidb/issues/47766) @ [AilinKid](https://github.com/AilinKid)
    -   `_charset(xxx), _charset(xxx2), ...`を含む SQL 文が異なるダイジェストを生成する問題を修正しました [＃58447](https://github.com/pingcap/tidb/issues/58447) @ [xhebox](https://github.com/xhebox)
    -   頻繁なリージョンのマージにより TTL ジョブが開始できなくなる問題を修正しました [＃61512](https://github.com/pingcap/tidb/issues/61512) @ [YangKeao](https://github.com/YangKeao)
    -   損失のあるDDL文を実行した後にTiFlashクエリ結果が矛盾する問題を修正しました [＃61455](https://github.com/pingcap/tidb/issues/61455) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   `ALTER RANGE meta SET PLACEMENT POLICY` のキー範囲が正しくない問題を修正しました [＃60888](https://github.com/pingcap/tidb/issues/60888) @ [nolouch](https://github.com/nolouch)
    -   Grafanaの**Stats Healthy Distribution**パネルのデータが正しくない可能性がある問題を修正しました[＃57176](https://github.com/pingcap/tidb/issues/57176) @ [hawkingrei](https://github.com/hawkingrei)
    -   `latin1_bin`の比較動作が`utf8mb4_bin`および`utf8_bin` と異なる問題を修正しました [＃60701](https://github.com/pingcap/tidb/issues/60701) @ [hawkingrei](https://github.com/hawkingrei)
    -   メタデータ ロック (MDL) を無効にした後、スキーマ バージョン更新に失敗して DDL 操作が停止する問題を修正しました。 [＃61210](https://github.com/pingcap/tidb/issues/61210) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   特定のシナリオでログ編集が有効にならない問題を修正[＃59279](https://github.com/pingcap/tidb/issues/59279) @ [tangenta](https://github.com/tangenta)
    -   修正コントロール#44855が有効になっている場合にTiDBセッションがクラッシュする可能性がある問題を修正[＃59762](https://github.com/pingcap/tidb/issues/59762) @ [winoros](https://github.com/winoros)
    -   `IndexLookup`オペレータが`context canceled`エラーに遭遇したときに冗長なログエントリを削除します [＃61072](https://github.com/pingcap/tidb/issues/61072) @ [yibin87](https://github.com/yibin87)
    -   統計の不適切な例外処理により、バックグラウンドタスクがタイムアウトしたときにメモリ内の統計が誤って削除される問題を修正しました[＃57901](https://github.com/pingcap/tidb/issues/57901) @ [hawkingrei](https://github.com/hawkingrei)
    -   `ADD UNIQUE INDEX`を実行するとデータの不整合が発生する可能性がある問題を修正[＃60339](https://github.com/pingcap/tidb/issues/60339) @ [tangenta](https://github.com/tangenta)
    -   統計システムテーブルに非公開インデックスが表示される問題を修正しました [＃60430](https://github.com/pingcap/tidb/issues/60430) @ [tangenta](https://github.com/tangenta)
    -   ハッシュ結合v1演算子の`Close()`メソッドがpanicから回復できない問題を修正しました [＃60926](https://github.com/pingcap/tidb/issues/60926) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   `PhysicalExchangeSender.HashCol`の浅いコピーによりTiFlash がクラッシュしたり、誤った結果が生成される問題を修正[＃60517](https://github.com/pingcap/tidb/issues/60517) @ [windtalker](https://github.com/windtalker)
    -   `BIT`タイプのテーブルの統計情報をにロードできない問題を修正しました [＃62289](https://github.com/pingcap/tidb/issues/62289) @ [YangKeao](https://github.com/YangKeao)
    -   `BIT`型列の統計がメモリにロードされない問題を修正しました [＃59759](https://github.com/pingcap/tidb/issues/59759) @ [YangKeao](https://github.com/YangKeao)
    -   極端なケースで`ANALYZE`ステートメントのディスクスピル操作に時間がかかりすぎると、他の TiDB ノードが最新の統計を更新できない可能性がある問題を修正しました。 [＃54552](https://github.com/pingcap/tidb/issues/54552) @ [0xPoe](https://github.com/0xPoe)
    -   収集された列統計がすべて TopN にある場合、後続の書き込みの後でも行数の推定が 0 のままになる可能性がある問題を修正しました。 [＃47400](https://github.com/pingcap/tidb/issues/47400) @ [terry1purcell](https://github.com/terry1purcell)
    -   `explain format="cost_trace"`に表示される推定コストが正しくない可能性がある問題を修正[＃61155](https://github.com/pingcap/tidb/issues/61155) @ [hawkingrei](https://github.com/hawkingrei)
    -   `explain format="cost_trace"`に表示されるコストの計算式に空の括弧が含まれる可能性がある問題を修正しました [＃61127](https://github.com/pingcap/tidb/issues/61127) @ [hawkingrei](https://github.com/hawkingrei)
    -   循環外部キー定義が無限ループを引き起こす問題を修正[＃60985](https://github.com/pingcap/tidb/issues/60985) @ [hawkingrei](https://github.com/hawkingrei)
    -   `NULL` を使用すると内部クエリがインデックス範囲クエリを正しく構築できない可能性がある問題を修正しました。 [＃62196](https://github.com/pingcap/tidb/issues/62196) @ [hawkingrei](https://github.com/hawkingrei)
    -   プランキャッシュが誤った実行プランを保存し、実行エラーが発生する問題を修正しました [＃56772](https://github.com/pingcap/tidb/issues/56772) @ [dash12653](https://github.com/dash12653)
    -   月または年にわたる行数の推定値が大幅に過大評価される可能性がある問題を修正[＃50080](https://github.com/pingcap/tidb/issues/50080) @ [terry1purcell](https://github.com/terry1purcell)
    -   `ANALYZE`サブタスクの同時実行数が設定された制限を大幅に超える問題を修正しました [＃61785](https://github.com/pingcap/tidb/issues/61785) @ [hawkingrei](https://github.com/hawkingrei)
    -   TopNプッシュダウン中に式ベースのTopNソート項目が誤って生成される問題を修正しました [＃60655](https://github.com/pingcap/tidb/issues/60655) @ [hawkingrei](https://github.com/hawkingrei)
    -   列またはインデックスの統計情報が欠落している場合に、TiDB がバックグラウンドでpanicログを出力する可能性がある問題を修正しました[＃61733](https://github.com/pingcap/tidb/issues/61733) @ [winoros](https://github.com/winoros)
    -   列またはインデックスの統計情報が欠落している場合、 `JOIN`行数推定が非常に不正確になる可能性がある問題を修正しました[＃61602](https://github.com/pingcap/tidb/issues/61602) @ [qw4990](https://github.com/qw4990)
    -   システム変数`tidb_cost_model_version`のデフォルト値が誤って設定されている問題を修正[＃61565](https://github.com/pingcap/tidb/issues/61565) @ [hawkingrei](https://github.com/hawkingrei)
    -   テーブルの最初の列が仮想生成列の場合に統計が正しくない可能性がある問題を修正しました [＃61606](https://github.com/pingcap/tidb/issues/61606) @ [winoros](https://github.com/winoros)
    -   述語の簡素化でプラン キャッシュが誤ってスキップされる問題を修正しました [＃61513](https://github.com/pingcap/tidb/issues/61513) @ [hawkingrei](https://github.com/hawkingrei)
    -   インデックスの追加中に`ADMIN CANCEL DDL JOBS`を実行すると、インデックスの追加プロセスがハングする問題を修正しました。 [＃61087](https://github.com/pingcap/tidb/issues/61087) @ [tangenta](https://github.com/tangenta)
    -   一部の内部 SQL 実行が失敗した後でも`ADMIN CHECK`が成功を返す問題を修正[＃61612](https://github.com/pingcap/tidb/issues/61612) @ [joechenrh](https://github.com/joechenrh)
    -   マルチスキーマ変更で複数のインデックスを追加した後にデータとインデックスが不整合になる問題を修正 [＃61255](https://github.com/pingcap/tidb/issues/61255) @ [tangenta](https://github.com/tangenta)

-   TiKV

    -   CPUプロファイリング中にデッドロックが発生する可能性がある問題を修正 [＃18474](https://github.com/tikv/tikv/issues/18474) @ [YangKeao](https://github.com/YangKeao)
    -   特定のTiFlashレプリカによってオンライン アンセーフ リカバリがブロックされ、コミット インデックスがに進まなくなる問題を修正しました。 [＃18197](https://github.com/tikv/tikv/issues/18197) @ [v01dstar](https://github.com/v01dstar)
    -   TiKVがクライアントがをデコードできない圧縮アルゴリズムを使用する可能性がある問題を修正しました [＃18079](https://github.com/tikv/tikv/issues/18079) @ [ekexium](https://github.com/ekexium)
    -   TiKV が高同時実行で過剰な SST 取り込み要求を許可する問題を修正 [＃18452](https://github.com/tikv/tikv/issues/18452) @ [hbisheng](https://github.com/hbisheng)
    -   Grafana の TiKV ダッシュボードで`Ingestion picked level`と`Compaction Job Size(files)`誤って表示される問題を修正しました [＃15990](https://github.com/tikv/tikv/issues/15990) @ [Connor1996](https://github.com/Connor1996)
    -   TiKV が再起動した後に予期しない`Server is busy`エラーが発生する問題を修正しました [＃18233](https://github.com/tikv/tikv/issues/18233) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   TiKVがブラジルとエジプトのタイムゾーンを誤って変換する問題を修正[＃16220](https://github.com/tikv/tikv/issues/16220) @ [overvenus](https://github.com/overvenus)
    -   スローログの`StoreMsg`ログエントリの誤解を招く説明を修正 [＃18561](https://github.com/tikv/tikv/issues/18561) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   スレッドメモリメトリックの誤りを修正[＃18125](https://github.com/tikv/tikv/issues/18125) @ [Connor1996](https://github.com/Connor1996)
    -   TiKV が正常なシャットダウン中に進行中の手動圧縮タスクを終了できない問題を修正[＃18396](https://github.com/tikv/tikv/issues/18396) @ [LykxSassinator](https://github.com/LykxSassinator)

-   PD

    -   `split-merge-interval`構成項目の値を繰り返し変更すると（ `1s`から`1h`に変更して`1s`に戻すなど）、その設定項目が有効にならない可能性がある問題を修正しました[＃8404](https://github.com/tikv/pd/issues/8404) @ [lhy1024](https://github.com/lhy1024)
    -   デフォルト値`lease`が正しく設定されていない問題を修正[＃9156](https://github.com/tikv/pd/issues/9156) @ [rleungx](https://github.com/rleungx)
    -   TiDB Dashboard TCP接続を不適切に閉じるとPDゴルーチンリークが発生する可能性がある問題を修正[＃9402](https://github.com/tikv/pd/issues/9402) @ [baurine](https://github.com/baurine)
    -   新しく追加された TiKV ノードがにスケジュールされない可能性がある問題を修正しました [＃9145](https://github.com/tikv/pd/issues/9145) @ [bufferflies](https://github.com/bufferflies)
    -   `tidb_enable_tso_follower_proxy`有効にすると TSO サービスが利用できなくなる可能性がある問題を修正[＃9188](https://github.com/tikv/pd/issues/9188) @ [Tema](https://github.com/Tema)

-   TiFlash

    -   `IMPORT INTO`または`BR restore` の実行中に SST ファイルを誤って削除することによって発生するpanicの問題を修正しました [＃10141](https://github.com/pingcap/tiflash/issues/10141) @ [CalvinNeo](https://github.com/CalvinNeo)
    -   `((NULL))`形式で式インデックスを作成するとTiFlash がpanicになる問題を修正しました [＃9891](https://github.com/pingcap/tiflash/issues/9891) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   不規則なリージョンキー範囲を持つスナップショットを処理するときにTiFlash がpanic可能性がある問題を修正しました [＃10147](https://github.com/pingcap/tiflash/issues/10147) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   クラスター内のテーブルに多数の`ENUM`型列が含まれている場合、 TiFlashが大量のメモリを消費する可能性がある問題を修正しました。 [＃9947](https://github.com/pingcap/tiflash/issues/9947) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   16 MiB を超えるデータの単一行を挿入した後にTiFlash が再起動に失敗する可能性がある問題を修正しました [＃10052](https://github.com/pingcap/tiflash/issues/10052) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   リソース制御の低トークン信号が欠落するとクエリスロットリングが発生する問題を修正しました [＃10137](https://github.com/pingcap/tiflash/issues/10137) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   `GROUP BY ... WITH ROLLUP` を含むSQL文を実行するとTiFlashが`Exception: Block schema mismatch`エラーを返す可能性がある問題を修正しました。 [＃10110](https://github.com/pingcap/tiflash/issues/10110) @ [gengliqi](https://github.com/gengliqi)

-   ツール

    -   Backup & Restore (BR)

        -   PITRが3072バイトを超えるインデックスの復元に失敗する問題を修正[＃58430](https://github.com/pingcap/tidb/issues/58430) @ [YuJuncen](https://github.com/YuJuncen)
        -   大量のデータを転送するときに Azure Blob Storage へのログ バックアップのアップロードが遅くなる問題を修正[＃18410](https://github.com/tikv/tikv/issues/18410) @ [YuJuncen](https://github.com/YuJuncen)
        -   `-f` でテーブルをフィルタリングするときに、 BR が対応するテーブルがクラスター内に存在するかどうかをチェックしない問題を修正しました。 [＃61592](https://github.com/pingcap/tidb/issues/61592) @ [RidRisR](https://github.com/RidRisR)

    -   TiCDC

        -   外部ストレージをダウンストリームとして使用すると、チェンジフィードが停止する可能性がある問題を修正しました。 [＃9162](https://github.com/pingcap/tiflow/issues/9162) @ [asddongmen](https://github.com/asddongmen)
        -   レプリケーショントラフィックが下流の Kafka のトラフィックしきい値を超えた後に、変更フィードがスタックする可能性がある問題を修正しました。 [＃12110](https://github.com/pingcap/tiflow/issues/12110) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   `changefeed pause`コマンドで`--overwrite-checkpoint-ts`パラメータを使用すると、変更フィードが停止する可能性がある問題を修正しました。 [＃12055](https://github.com/pingcap/tiflow/issues/12055) @ [hongyunyan](https://github.com/hongyunyan)
        -   仮想列を含むテーブルでイベントフィルタ式を評価するとpanicが発生する可能性がある問題を修正[＃12206](https://github.com/pingcap/tiflow/issues/12206) @ [lidezhu](https://github.com/lidezhu)
        -   ディスパッチャ構成における列名とインデックス名の大文字と小文字を区別するマッチングの問題を修正しました [＃12103](https://github.com/pingcap/tiflow/issues/12103) @ [wk989898](https://github.com/wk989898)
        -   古いストア ID が原因で、同じ IP アドレス上の TiKV ノードをスケールインまたはスケールアウトした後に、解決された ts ラグが増加し続ける問題を修正しました。 [＃12162](https://github.com/pingcap/tiflow/issues/12162) @ [3AceShowHand](https://github.com/3AceShowHand)

    -   TiDB Lightning

        -   クラウドストレージから TiDB に Parquet ファイルをインポートするときに、 TiDB Lightning が数時間停止する可能性がある問題を修正しました。 [＃60224](https://github.com/pingcap/tidb/issues/60224) @ [joechenrh](https://github.com/joechenrh)
        -   TiKVへのRPCリクエストがタイムアウトするとTiDB Lightningが`context deadline exceeded`エラーを返す問題を修正しました [＃61326](https://github.com/pingcap/tidb/issues/61326) @ [OliverS929](https://github.com/OliverS929)

    -   NG Monitoring

        -   時系列データのカーディナリティが高い場合に TSDB がメモリを大量に消費する問題を修正し、TSDB のメモリ構成オプションを提供します。 [＃295](https://github.com/pingcap/ng-monitoring/issues/295) @ [mornyx](https://github.com/mornyx)
