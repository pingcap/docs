---
title: TiDB 7.5.7 Release Notes
summary: TiDB 7.5.7 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 7.5.7 リリースノート {#tidb-7-5-7-release-notes}

発売日：2025年9月4日

TiDB バージョン: 7.5.7

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   デフォルト値の[`tidb_enable_historical_stats`](https://docs.pingcap.com/tidb/v7.5/system-variables/#tidb_enable_historical_stats)を`ON`から`OFF`に変更します。これにより、潜在的な安定性の問題を回避するために履歴統計がオフになります[＃53048](https://github.com/pingcap/tidb/issues/53048) @ [ホーキングレイ](https://github.com/hawkingrei)
-   TiKV は以下の設定項目を廃止し、自動圧縮動作[＃18727](https://github.com/tikv/tikv/issues/18727) @ [v01dスター](https://github.com/v01dstar)を制御する新しい[`gc.auto-compaction`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file/#gcauto-compaction)設定グループに置き換えます。

    -   非推奨の構成項目: [`region-compact-check-interval`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#region-compact-check-interval) 、 [`region-compact-check-step`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#region-compact-check-step) 、 [`region-compact-min-tombstones`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#region-compact-min-tombstones) 、 [`region-compact-tombstones-percent`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#region-compact-tombstones-percent) 、 [`region-compact-min-redundant-rows`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#region-compact-min-redundant-rows-new-in-v710) 、および[`region-compact-redundant-rows-percent`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#region-compact-redundant-rows-percent-new-in-v710) 。
    -   新しい[`gc.auto-compaction.tombstone-percent-threshold`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#tombstone-percent-threshold-new-in-v757) [`gc.auto-compaction.redundant-rows-threshold`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#redundant-rows-threshold-new-in-v757) : [`gc.auto-compaction.check-interval`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#check-interval-new-in-v757) [`gc.auto-compaction.redundant-rows-percent-threshold`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#redundant-rows-percent-threshold-new-in-v757)および[`gc.auto-compaction.bottommost-level-force`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#bottommost-level-force-new-in-v757) [`gc.auto-compaction.tombstone-num-threshold`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#tombstone-num-threshold-new-in-v757)

## 改善点 {#improvements}

-   TiDB

    -   データインポート[＃61553](https://github.com/pingcap/tidb/issues/61553) @ [接線](https://github.com/tangenta)中のリージョン分割とデータ取り込みのためのフロー制御インターフェースを追加します
    -   大容量データを持つテーブルに対して単純なクエリを実行する際に、データ分布情報を取得するパフォーマンスを最適化します[＃53850](https://github.com/pingcap/tidb/issues/53850) @ [あなた06](https://github.com/you06)
    -   インデックス追加[＃60925](https://github.com/pingcap/tidb/issues/60925) @ [CbcWestwolf](https://github.com/CbcWestwolf)中の TiKV への書き込み速度を観察するための監視メトリックを追加します。
    -   DDL実行中のDMLのロックロジックを最適化し、DMLとDDL間のロック競合を軽減することで、一部のシナリオでDDLのパフォーマンスが向上します。ただし、セカンダリインデックスのロック操作が追加されるため、DMLのパフォーマンスがわずかに低下する可能性があります[＃62337](https://github.com/pingcap/tidb/issues/62337) @ [lcwangchao](https://github.com/lcwangchao)
    -   システム変数[`tidb_opt_ordering_index_selectivity_threshold`](/system-variables.md#tidb_opt_ordering_index_selectivity_threshold-new-in-v700) `1`に設定されている場合の動作を改善し、この変数[＃60242](https://github.com/pingcap/tidb/issues/60242) @ [時間と運命](https://github.com/time-and-fate)の制御機能を強化します。
    -   `ANALYZE`文実行後にクラスタ全体の統計を更新することを回避し、実行時間を`ANALYZE` [＃57631](https://github.com/pingcap/tidb/issues/57631) @ [0xPoe](https://github.com/0xPoe)に短縮します。
    -   `NOT NULL`制約を持つ列の定数畳み込みをサポートし、 `IS NULL`評価を`FALSE` [＃62050](https://github.com/pingcap/tidb/issues/62050) @ [ホーキングレイ](https://github.com/hawkingrei)に畳み込みます。
    -   オプティマイザは、より多くの種類の`JOIN`操作[＃51700](https://github.com/pingcap/tidb/issues/51700) @ [ホーキングレイ](https://github.com/hawkingrei)で定数伝播をサポートします。
    -   DML 操作と DDL 操作の間に大規模なロック競合が存在する場合の一時インデックスのマージのパフォーマンスを向上[＃61433](https://github.com/pingcap/tidb/issues/61433) @ [接線](https://github.com/tangenta)

-   TiKV

    -   TiKV圧縮のトリガーロジックを最適化して、すべてのデータセグメントを再利用効率の順に処理し、MVCC冗長データ[＃18571](https://github.com/tikv/tikv/issues/18571) @ [v01dstar](https://github.com/v01dstar)のパフォーマンスへの影響を軽減します。
    -   多数の SST ファイルが存在する環境での非同期スナップショットおよび書き込み操作のテールレイテンシーを最適化します[＃18743](https://github.com/tikv/tikv/issues/18743) @ [コナー1996](https://github.com/Connor1996)
    -   空のテーブルと小さなリージョン[＃17376](https://github.com/tikv/tikv/issues/17376) @ [LykxSassinator](https://github.com/LykxSassinator)シナリオでのリージョン結合の速度を改善
    -   Raftstoreの`CompactedEvent`処理を`split-check`ワーカーに移動して最適化し、メインのRaftstoreスレッド[＃18532](https://github.com/tikv/tikv/issues/18532) @ [LykxSassinator](https://github.com/LykxSassinator)のブロッキングを削減します。
    -   スレッド[＃15927](https://github.com/tikv/tikv/issues/15927) @ [コナー1996](https://github.com/Connor1996)ごとのメモリ使用量のメトリックを追加します。
    -   SST の取り込みが遅すぎる場合は`SST ingest is experiencing slowdowns`のみをログに記録し、パフォーマンスのジッターを回避するために`get_sst_key_ranges`呼び出しをスキップします[＃18549](https://github.com/tikv/tikv/issues/18549) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   ログの適用を待つために TiKV を再起動するときに発生する不安定なアクセス遅延を最適化し、TiKV [＃15874](https://github.com/tikv/tikv/issues/15874) @ [LykxSassinator](https://github.com/LykxSassinator)の安定性を向上しました。
    -   残留データのクリーンアップメカニズムを最適化して、リクエストのレイテンシー[＃18107](https://github.com/tikv/tikv/issues/18107) @ [LykxSassinator](https://github.com/LykxSassinator)への影響を軽減します。
    -   Raft Engineの`fetch_entries_to`のパフォーマンスを最適化して競合を減らし、混合ワークロード[＃18605](https://github.com/tikv/tikv/issues/18605) @ [LykxSassinator](https://github.com/LykxSassinator)でのパフォーマンスを向上します。
    -   書き込み操作のフロー制御構成の動的な変更をサポート[＃17395](https://github.com/tikv/tikv/issues/17395) @ [栄光](https://github.com/glorv)
    -   フォアグラウンド書き込みをブロックせずにSSTファイルの取り込みをサポートし、レイテンシー[＃18081](https://github.com/tikv/tikv/issues/18081) @ [hhwyt](https://github.com/hhwyt)の影響を軽減します。
    -   KvDB と RaftDB が別々のマウント パス[＃18463](https://github.com/tikv/tikv/issues/18463) @ [LykxSassinator](https://github.com/LykxSassinator)を使用する場合の KvDB ディスクの I/O ジッターの検出メカニズムを最適化します。
    -   ピアのスローログを追加し、メッセージ[＃16600](https://github.com/tikv/tikv/issues/16600) @ [コナー1996](https://github.com/Connor1996)を保存します

-   PD

    -   Prometheus [＃8931](https://github.com/tikv/pd/issues/8931) @ [バッファフライ](https://github.com/bufferflies)に GO ランタイム関連の監視メトリクスを追加
    -   不要なエラーログを[＃9370](https://github.com/tikv/pd/issues/9370)つ[バッファフライ](https://github.com/bufferflies)削減

-   TiFlash

    -   ワイドテーブルシナリオにおけるTiFlash OOM リスクの観測可能性を強化[＃10272](https://github.com/pingcap/tiflash/issues/10272) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   storageスナップショットを取得する際の最大再試行回数を増やし、大規模なテーブルのクエリの安定性を向上させます[＃10300](https://github.com/pingcap/tiflash/issues/10300) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)

-   ツール

    -   バックアップと復元 (BR)

        -   TiDBをAmazon EC2に導入する場合、 BRはAWSインスタンスメタデータサービスバージョン2（IMDSv2）をサポートします。EC2インスタンスを設定することで、 BRがインスタンスに関連付けられたIAMロールを使用してAmazon S3への適切なアクセス権限を付与できるようになります[＃16443](https://github.com/tikv/tikv/issues/16443) @ [ピンギュ](https://github.com/pingyu)
        -   TiKVのダウンロードAPIは、バックアップファイルをダウンロードする際に特定の時間範囲内のデータをフィルタリングすることをサポートしており、復元時に古いデータバージョンや将来のデータバージョンがインポートされるのを回避します[＃18399](https://github.com/tikv/tikv/issues/18399) @ [3ポイントシュート](https://github.com/3pointer)

## バグ修正 {#bug-fixes}

-   TiDB

    -   `IndexMerge`および`IndexLookUp`演算子の共有 KV リクエストがクエリ[＃60175](https://github.com/pingcap/tidb/issues/60175) @ [あなた06](https://github.com/you06)をプッシュダウンするときにデータ競合を引き起こす問題を修正しました。
    -   ハッシュ集計演算子[＃58004](https://github.com/pingcap/tidb/issues/58004) @ [xzhangxian1008](https://github.com/xzhangxian1008)における潜在的な goroutine リークの問題を修正しました。
    -   生成された列のインデックスが表示[＃47766](https://github.com/pingcap/tidb/issues/47766) @ [アイリンキッド](https://github.com/AilinKid)に設定されている場合、MPP プランが選択されない可能性がある問題を修正しました。
    -   `_charset(xxx), _charset(xxx2), ...`を含む SQL 文が[＃58447](https://github.com/pingcap/tidb/issues/58447) @ [xhebox](https://github.com/xhebox)で異なるダイジェストを生成する問題を修正しました
    -   頻繁なリージョンのマージにより TTL ジョブが[＃61512](https://github.com/pingcap/tidb/issues/61512) @ [ヤンケオ](https://github.com/YangKeao)で開始できなくなる問題を修正しました
    -   損失のあるDDL文[＃61455](https://github.com/pingcap/tidb/issues/61455) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)を実行した後にTiFlashクエリ結果が矛盾する問題を修正しました
    -   `ALTER RANGE meta SET PLACEMENT POLICY` [＃60888](https://github.com/pingcap/tidb/issues/60888) @ [ノルーシュ](https://github.com/nolouch)のキー範囲が正しくない問題を修正しました
    -   Grafanaの**Stats Healthy Distribution**パネルのデータが正しくない可能性がある問題を修正しました[＃57176](https://github.com/pingcap/tidb/issues/57176) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `latin1_bin`の比較動作が`utf8mb4_bin`および`utf8_bin` [＃60701](https://github.com/pingcap/tidb/issues/60701) @ [ホーキングレイ](https://github.com/hawkingrei)と異なる問題を修正しました
    -   メタデータ ロック (MDL) を無効にした後、スキーマ バージョン[＃61210](https://github.com/pingcap/tidb/issues/61210) @ [wjhuang2016](https://github.com/wjhuang2016)更新に失敗して DDL 操作が停止する問題を修正しました。
    -   特定のシナリオでログ編集が有効にならない問題を修正[＃59279](https://github.com/pingcap/tidb/issues/59279) @ [接線](https://github.com/tangenta)
    -   修正コントロール#44855が有効になっている場合にTiDBセッションがクラッシュする可能性がある問題を修正[＃59762](https://github.com/pingcap/tidb/issues/59762) @ [ウィノロス](https://github.com/winoros)
    -   `IndexLookup`オペレータが`context canceled`エラー[＃61072](https://github.com/pingcap/tidb/issues/61072) @ [イービン87](https://github.com/yibin87)に遭遇したときに冗長なログエントリを削除します
    -   統計の不適切な例外処理により、バックグラウンドタスクがタイムアウトしたときにメモリ内の統計が誤って削除される問題を修正しました[＃57901](https://github.com/pingcap/tidb/issues/57901) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `ADD UNIQUE INDEX`実行するとデータの不整合が発生する可能性がある問題を修正[＃60339](https://github.com/pingcap/tidb/issues/60339) @ [接線](https://github.com/tangenta)
    -   統計システムテーブル[＃60430](https://github.com/pingcap/tidb/issues/60430) @ [接線](https://github.com/tangenta)に非公開インデックスが表示される問題を修正しました
    -   ハッシュ結合v1演算子の`Close()`メソッドがpanic[＃60926](https://github.com/pingcap/tidb/issues/60926) @ [xzhangxian1008](https://github.com/xzhangxian1008)から回復できない問題を修正しました
    -   `PhysicalExchangeSender.HashCol`の浅いコピーによりTiFlash がクラッシュしたり、誤った結果が生成される問題を修正[＃60517](https://github.com/pingcap/tidb/issues/60517) @ [ウィンドトーカー](https://github.com/windtalker)
    -   `BIT`タイプのテーブルの統計情報を[＃62289](https://github.com/pingcap/tidb/issues/62289) @ [ヤンケオ](https://github.com/YangKeao)にロードできない問題を修正しました
    -   `BIT`型列の統計がメモリ[＃59759](https://github.com/pingcap/tidb/issues/59759) @ [ヤンケオ](https://github.com/YangKeao)にロードされない問題を修正しました
    -   極端なケースで`ANALYZE`ステートメントのディスクスピル操作に時間がかかりすぎると、他の TiDB ノードが最新の統計[＃54552](https://github.com/pingcap/tidb/issues/54552) @ [0xPoe](https://github.com/0xPoe)を更新できない可能性がある問題を修正しました。
    -   収集された列統計がすべて TopN にある場合、後続の書き込み[＃47400](https://github.com/pingcap/tidb/issues/47400) @ [テリー・パーセル](https://github.com/terry1purcell)の後でも行数の推定が 0 のままになる可能性がある問題を修正しました。
    -   `explain format="cost_trace"`に表示される推定コストが正しくない可能性がある問題を修正[＃61155](https://github.com/pingcap/tidb/issues/61155) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `explain format="cost_trace"`に表示されるコストの計算式に空の括弧[＃61127](https://github.com/pingcap/tidb/issues/61127) @ [ホーキングレイ](https://github.com/hawkingrei)が含まれる可能性がある問題を修正しました
    -   循環外部キー定義が無限ループを引き起こす問題を修正[＃60985](https://github.com/pingcap/tidb/issues/60985) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `NULL` [＃62196](https://github.com/pingcap/tidb/issues/62196) @ [ホーキングレイ](https://github.com/hawkingrei)を使用すると内部クエリがインデックス範囲クエリを正しく構築できない可能性がある問題を修正しました。
    -   プランキャッシュが誤った実行プランを保存し、実行エラー[＃56772](https://github.com/pingcap/tidb/issues/56772) @ [ダッシュ12653](https://github.com/dash12653)が発生する問題を修正しました
    -   月または年にわたる行数の推定値が大幅に過大評価される可能性がある問題を修正[＃50080](https://github.com/pingcap/tidb/issues/50080) @ [テリー・パーセル](https://github.com/terry1purcell)
    -   `ANALYZE`サブタスクの同時実行数が設定された制限[＃61785](https://github.com/pingcap/tidb/issues/61785) @ [ホーキングレイ](https://github.com/hawkingrei)を大幅に超える問題を修正しました
    -   TopNプッシュダウン[＃60655](https://github.com/pingcap/tidb/issues/60655) @ [ホーキングレイ](https://github.com/hawkingrei)中に式ベースのTopNソート項目が誤って生成される問題を修正しました
    -   列またはインデックスの統計情報が欠落している場合に、TiDB がバックグラウンドでpanicログを出力する可能性がある問題を修正しました[＃61733](https://github.com/pingcap/tidb/issues/61733) @ [ウィノロス](https://github.com/winoros)
    -   列またはインデックスの統計情報が欠落している場合、 `JOIN`行数推定が非常に不正確になる可能性がある問題を修正しました[＃61602](https://github.com/pingcap/tidb/issues/61602) @ [qw4990](https://github.com/qw4990)
    -   システム変数`tidb_cost_model_version`のデフォルト値が誤って設定されている問題を修正[＃61565](https://github.com/pingcap/tidb/issues/61565) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   テーブルの最初の列が仮想生成列[＃61606](https://github.com/pingcap/tidb/issues/61606) @ [ウィノロス](https://github.com/winoros)の場合に統計が正しくない可能性がある問題を修正しました
    -   述語の簡素化[＃61513](https://github.com/pingcap/tidb/issues/61513) @ [ホーキングレイ](https://github.com/hawkingrei)でプラン キャッシュが誤ってスキップされる問題を修正しました
    -   インデックスの追加中に`ADMIN CANCEL DDL JOBS`実行すると、インデックスの追加プロセスが[＃61087](https://github.com/pingcap/tidb/issues/61087) @ [接線](https://github.com/tangenta)でハングする問題を修正しました。
    -   一部の内部 SQL 実行が失敗した後でも`ADMIN CHECK`が成功を返す問題を修正[＃61612](https://github.com/pingcap/tidb/issues/61612) @ [ヨッヘンrh](https://github.com/joechenrh)
    -   マルチスキーマ変更[＃61255](https://github.com/pingcap/tidb/issues/61255) @ [接線](https://github.com/tangenta)で複数のインデックスを追加した後にデータとインデックスが不整合になる問題を修正

-   TiKV

    -   CPUプロファイリング[＃18474](https://github.com/tikv/tikv/issues/18474) @ [ヤンケオ](https://github.com/YangKeao)中にデッドロックが発生する可能性がある問題を修正
    -   特定のTiFlashレプリカによってオンライン アンセーフ リカバリがブロックされ、コミット インデックスが[＃18197](https://github.com/tikv/tikv/issues/18197) @ [v01dスター](https://github.com/v01dstar)に進まなくなる問題を修正しました。
    -   TiKVがクライアントが[＃18079](https://github.com/tikv/tikv/issues/18079) @ [エキシウム](https://github.com/ekexium)をデコードできない圧縮アルゴリズムを使用する可能性がある問題を修正しました
    -   TiKV が高同時実行[＃18452](https://github.com/tikv/tikv/issues/18452) @ [ヒビシェン](https://github.com/hbisheng)で過剰な SST 取り込み要求を許可する問題を修正
    -   Grafana [＃15990](https://github.com/tikv/tikv/issues/15990) @ [コナー1996](https://github.com/Connor1996)の TiKV ダッシュボードで`Ingestion picked level`と`Compaction Job Size(files)`誤って表示される問題を修正しました
    -   TiKV が[＃18233](https://github.com/tikv/tikv/issues/18233) @ [LykxSassinator](https://github.com/LykxSassinator)で再起動した後に予期しない`Server is busy`エラーが発生する問題を修正しました
    -   TiKVがブラジルとエジプトのタイムゾーンを誤って変換する問題を修正[＃16220](https://github.com/tikv/tikv/issues/16220) @ [金星の上](https://github.com/overvenus)
    -   スローログ[＃18561](https://github.com/tikv/tikv/issues/18561) @ [LykxSassinator](https://github.com/LykxSassinator)の`StoreMsg`ログエントリの誤解を招く説明を修正
    -   スレッドメモリメトリックの誤りを修正[＃18125](https://github.com/tikv/tikv/issues/18125) @ [コナー1996](https://github.com/Connor1996)
    -   TiKV が正常なシャットダウン中に進行中の手動圧縮タスクを終了できない問題を修正[＃18396](https://github.com/tikv/tikv/issues/18396) @ [LykxSassinator](https://github.com/LykxSassinator)

-   PD

    -   `split-merge-interval`構成項目の値を繰り返し変更すると（ `1s`から`1h`に変更して`1s`に戻すなど）、その設定項目が有効にならない可能性がある問題を修正しました[＃8404](https://github.com/tikv/pd/issues/8404) @ [lhy1024](https://github.com/lhy1024)
    -   デフォルト値`lease`が正しく設定されていない問題を修正[＃9156](https://github.com/tikv/pd/issues/9156) @ [rleungx](https://github.com/rleungx)
    -   TiDBダッシュボードTCP接続を不適切に閉じるとPDゴルーチンリークが発生する可能性がある問題を修正[＃9402](https://github.com/tikv/pd/issues/9402) @ [バウリン](https://github.com/baurine)
    -   新しく追加された TiKV ノードが[＃9145](https://github.com/tikv/pd/issues/9145) @ [バッファフライ](https://github.com/bufferflies)にスケジュールされない可能性がある問題を修正しました
    -   `tidb_enable_tso_follower_proxy`有効にすると TSO サービスが利用できなくなる可能性がある問題を修正[＃9188](https://github.com/tikv/pd/issues/9188) @ [テーマ](https://github.com/Tema)

-   TiFlash

    -   `IMPORT INTO`または`BR restore` [＃10141](https://github.com/pingcap/tiflash/issues/10141) @ [カルビンネオ](https://github.com/CalvinNeo)の実行中に SST ファイルを誤って削除することによって発生するpanicの問題を修正しました
    -   `((NULL))`形式で式インデックスを作成するとTiFlash が[＃9891](https://github.com/pingcap/tiflash/issues/9891) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)でpanicになる問題を修正しました
    -   不規則なリージョンキー範囲[＃10147](https://github.com/pingcap/tiflash/issues/10147) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を持つスナップショットを処理するときにTiFlash がpanic可能性がある問題を修正しました
    -   クラスター内のテーブルに多数の`ENUM`型列[＃9947](https://github.com/pingcap/tiflash/issues/9947) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)が含まれている場合、 TiFlashが大量のメモリを消費する可能性がある問題を修正しました。
    -   16 MiB [＃10052](https://github.com/pingcap/tiflash/issues/10052) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を超えるデータの単一行を挿入した後にTiFlash が再起動に失敗する可能性がある問題を修正しました
    -   リソース制御の低トークン信号が欠落するとクエリスロットリング[＃10137](https://github.com/pingcap/tiflash/issues/10137) @ [グオシャオゲ](https://github.com/guo-shaoge)が発生する問題を修正しました
    -   `GROUP BY ... WITH ROLLUP` [＃10110](https://github.com/pingcap/tiflash/issues/10110) @ [ゲンリキ](https://github.com/gengliqi)を含むSQL文を実行するとTiFlashが`Exception: Block schema mismatch`エラーを返す可能性がある問題を修正しました。

-   ツール

    -   バックアップと復元 (BR)

        -   PITRが3072バイトを超えるインデックスの復元に失敗する問題を修正[＃58430](https://github.com/pingcap/tidb/issues/58430) @ [ユジュンセン](https://github.com/YuJuncen)
        -   大量のデータを転送するときに Azure Blob Storage へのログ バックアップのアップロードが遅くなる問題を修正[＃18410](https://github.com/tikv/tikv/issues/18410) @ [ユジュンセン](https://github.com/YuJuncen)
        -   `-f` [＃61592](https://github.com/pingcap/tidb/issues/61592) @ [リドリスR](https://github.com/RidRisR)でテーブルをフィルタリングするときに、 BR が対応するテーブルがクラスター内に存在するかどうかをチェックしない問題を修正しました。

    -   TiCDC

        -   外部storageをダウンストリーム[＃9162](https://github.com/pingcap/tiflow/issues/9162) @ [アズドンメン](https://github.com/asddongmen)として使用すると、チェンジフィードが停止する可能性がある問題を修正しました。
        -   レプリケーショントラフィックが下流の Kafka [＃12110](https://github.com/pingcap/tiflow/issues/12110) @ [3エースショーハンド](https://github.com/3AceShowHand)のトラフィックしきい値を超えた後に、変更フィードがスタックする可能性がある問題を修正しました。
        -   `changefeed pause`コマンドで`--overwrite-checkpoint-ts`パラメータを使用すると、変更フィードが[＃12055](https://github.com/pingcap/tiflow/issues/12055) @ [ホンユニャン](https://github.com/hongyunyan)で停止する可能性がある問題を修正しました。
        -   仮想列を含むテーブルでイベントフィルタ式を評価するとpanicが発生する可能性がある問題を修正[＃12206](https://github.com/pingcap/tiflow/issues/12206) @ [リデズ](https://github.com/lidezhu)
        -   ディスパッチャ構成[＃12103](https://github.com/pingcap/tiflow/issues/12103) @ [wk989898](https://github.com/wk989898)における列名とインデックス名の大文字と小文字を区別するマッチングの問題を修正しました
        -   古いストア ID [＃12162](https://github.com/pingcap/tiflow/issues/12162) @ [3エースショーハンド](https://github.com/3AceShowHand)が原因で、同じ IP アドレス上の TiKV ノードをスケールインまたはスケールアウトした後に、解決された ts ラグが増加し続ける問題を修正しました。

    -   TiDB Lightning

        -   クラウドstorageから TiDB [＃60224](https://github.com/pingcap/tidb/issues/60224) @ [ヨッヘンrh](https://github.com/joechenrh)に Parquet ファイルをインポートするときに、 TiDB Lightning が数時間停止する可能性がある問題を修正しました。
        -   TiKVへのRPCリクエストが[＃61326](https://github.com/pingcap/tidb/issues/61326) @ [オリバーS929](https://github.com/OliverS929)でタイムアウトするとTiDB Lightningが`context deadline exceeded`エラーを返す問題を修正しました

    -   NGモニタリング

        -   時系列データのカーディナリティが高い場合に TSDB がメモリを大量に消費する問題を修正し、TSDB [＃295](https://github.com/pingcap/ng-monitoring/issues/295) @ [モーニクス](https://github.com/mornyx)のメモリ構成オプションを提供します。
