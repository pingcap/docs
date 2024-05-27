---
title: TiDB 6.5.9 Release Notes
summary: TiDB 6.5.9 の互換性の変更、改善、バグ修正について説明します。
---

# TiDB 6.5.9 リリースノート {#tidb-6-5-9-release-notes}

発売日: 2024年4月12日

TiDB バージョン: 6.5.9

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [実稼働環境への導入](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   RocksDB 用の TiKV 構成項目[`track-and-verify-wals-in-manifest`](https://docs.pingcap.com/tidb/v6.5/tikv-configuration-file#track-and-verify-wals-in-manifest-new-in-v659)を追加します。これにより、Write Ahead Log (WAL) [＃16549](https://github.com/tikv/tikv/issues/16549) @ [v01dスター](https://github.com/v01dstar)の破損の可能性を調査できます。
-   DR自動同期は[`wait-recover-timeout`](https://docs.pingcap.com/tidb/v6.5/two-data-centers-in-one-city-deployment#enable-the-dr-auto-sync-mode)設定をサポートしており、ネットワークが回復した後`sync-recover`状態に戻るまでの待機時間を制御できます[＃6295](https://github.com/tikv/pd/issues/6295) @ [ディスク](https://github.com/disksing)

## 改善点 {#improvements}

-   ティビ

    -   `force-init-stats`を`true`に設定すると、TiDB は統計の初期化が完了するまで待機してから、TiDB の起動中にサービスを提供します。この設定により、HTTP サーバーの起動がブロックされなくなり、ユーザーは[＃50854](https://github.com/pingcap/tidb/issues/50854) @ [ホーキングレイ](https://github.com/hawkingrei)の監視を継続できます。
    -   `ANALYZE`文がメタデータ ロック[＃47475](https://github.com/pingcap/tidb/issues/47475) @ [翻訳:](https://github.com/wjhuang2016)をブロックする問題を最適化します。

-   ティクヴ

    -   不要な非同期ブロックを削除してメモリ使用量を削減する[＃16540](https://github.com/tikv/tikv/issues/16540) @ [金星の上](https://github.com/overvenus)
    -   TiKV の安定性を向上させるために、raftstore スレッドでスナップショット ファイルに対する IO 操作を実行しないようにします[＃16564](https://github.com/tikv/tikv/issues/16564) @ [コナー1996](https://github.com/Connor1996)
    -   ピアのスローログを追加し、メッセージ[＃16600](https://github.com/tikv/tikv/issues/16600) @ [コナー1996](https://github.com/Connor1996)を保存します。

-   ツール

    -   バックアップと復元 (BR)

        -   ローリング再起動中のログバックアップのリカバリポイント目標 (RPO) を最適化します。これで、ローリング再起動中のログバックアップタスクのチェックポイントラグが小さくなります[＃15410](https://github.com/tikv/tikv/issues/15410) @ [ユジュンセン](https://github.com/YuJuncen)
        -   ログバックアップのマージ操作に対する許容度を高めます。適度に長いマージ操作が発生した場合、ログバックアップタスクがエラー状態[＃16554](https://github.com/tikv/tikv/issues/16554) @ [ユジュンセン](https://github.com/YuJuncen)に入る可能性が低くなります。
        -   チェックポイントの大きな遅延が発生した場合にログ バックアップ タスクを自動的に中止し、GC の長時間のブロッキングや潜在的なクラスターの問題を回避することをサポートします[＃50803](https://github.com/pingcap/tidb/issues/50803) @ [リドリス](https://github.com/RidRisR)
        -   リージョンリーダーシップの移行が発生すると、PITR ログバックアップの進行のレイテンシーが長くなるという問題を緩和します[＃13638](https://github.com/tikv/tikv/issues/13638) @ [ユジュンセン](https://github.com/YuJuncen)
        -   より効率的なアルゴリズム[＃50613](https://github.com/pingcap/tidb/issues/50613) @ [リーヴルス](https://github.com/Leavrth)を使用して、データ復元中に SST ファイルをマージする速度を向上します
        -   データ復元中に SST ファイルをバッチで取り込むことをサポート[＃16267](https://github.com/tikv/tikv/issues/16267) @ [3ポインター](https://github.com/3pointer)
        -   Google Cloud Storage (GCS) を外部storageとして使用する場合の古い互換性チェックを削除する[＃50533](https://github.com/pingcap/tidb/issues/50533) @ [ランス6716](https://github.com/lance6716)
        -   ログバックアップ中にログとメトリックのグローバルチェックポイントの進行に影響を与える最も遅いリージョンの情報を出力します[＃51046](https://github.com/pingcap/tidb/issues/51046) @ [ユジュンセン](https://github.com/YuJuncen)
        -   BR例外処理メカニズムをリファクタリングして、未知のエラーに対する許容度を高める[＃47656](https://github.com/pingcap/tidb/issues/47656) @ [3ポインター](https://github.com/3pointer)

## バグの修正 {#bug-fixes}

-   ティビ

    -   多数のテーブルを作成した後、新しく作成されたテーブルに`stats_meta`情報が欠落し、後続のクエリ推定で正確な行数情報を取得できない問題を修正しました[＃36004](https://github.com/pingcap/tidb/issues/36004) @ [翻訳者](https://github.com/xuyifangreeneyes)
    -   ドロップされたテーブルがGrafana `Stats Healthy Distribution`パネル[＃39349](https://github.com/pingcap/tidb/issues/39349) @ [翻訳者](https://github.com/xuyifangreeneyes)でまだカウントされる問題を修正
    -   TiDB が SQL ステートメントのクエリに`MemTableScan`演算子[＃40937](https://github.com/pingcap/tidb/issues/40937) @ [中文](https://github.com/zhongzc)が含まれている場合に、SQL ステートメントの`WHERE <column_name>`フィルタリング条件を処理しない問題を修正しました。
    -   サブクエリの`HAVING`句に相関列[＃51107](https://github.com/pingcap/tidb/issues/51107) @ [ホーキングレイ](https://github.com/hawkingrei)が含まれている場合にクエリ結果が正しくない可能性がある問題を修正しました。
    -   共通テーブル式 (CTE) を使用して統計情報が欠落しているパーティション テーブルにアクセスすると、クエリ結果が不正確になる可能性がある問題を修正しました[＃51873](https://github.com/pingcap/tidb/issues/51873) @ [qw4990](https://github.com/qw4990)
    -   SQL ステートメントに`JOIN`含まれ、ステートメント内の`SELECT`リストに定数[＃50358](https://github.com/pingcap/tidb/issues/50358) @ [いいえ](https://github.com/yibin87)のみが含まれている場合に、MPP を使用してクエリを実行すると、誤ったクエリ結果が返される可能性がある問題を修正しました。
    -   自動増分 ID [＃50819](https://github.com/pingcap/tidb/issues/50819) @ [天菜まお](https://github.com/tiancaiamao)を割り当てるときに、 `AUTO_INCREMENT`属性によって不要なトランザクション競合が発生し、ID が連続しなくなる問題を修正しました。
    -   Grafana の監視メトリック`tidb_statistics_auto_analyze_total`が整数[＃51051](https://github.com/pingcap/tidb/issues/51051) @ [ホーキングレイ](https://github.com/hawkingrei)として表示されない問題を修正しました。
    -   パーティションテーブル[＃48713](https://github.com/pingcap/tidb/issues/48713) @ [ホーキングレイ](https://github.com/hawkingrei)のグローバル統計の同時マージ中にエラーが返される可能性がある問題を修正しました。
    -   列のデフォルト値が削除されている場合、列のデフォルト値を取得するとエラーが返される問題を修正[＃50043](https://github.com/pingcap/tidb/issues/50043) [＃51324](https://github.com/pingcap/tidb/issues/51324) @ [クレイジーcs520](https://github.com/crazycs520)
    -   列が書き込み専用の場合に`INSERT ignore`ステートメントでデフォルト値を入力できない問題を修正[＃40192](https://github.com/pingcap/tidb/issues/40192) @ [ヤンケオ](https://github.com/YangKeao)
    -   `shuffleExec`予期せず終了すると TiDB がクラッシュする問題を修正[＃48230](https://github.com/pingcap/tidb/issues/48230) @ [うわー](https://github.com/wshwsh12)
    -   `HashJoin`演算子がディスク[＃50841](https://github.com/pingcap/tidb/issues/50841) @ [うわー](https://github.com/wshwsh12)にスピルできない場合に発生する可能性のある goroutine リークの問題を修正しました。
    -   トランザクション[＃39664](https://github.com/pingcap/tidb/issues/39664) @ [天菜まお](https://github.com/tiancaiamao)で複数のステートメントをコミットするときにテーブル名の変更が有効にならない問題を修正しました
    -   `IN()`述語に`NULL` [＃51560](https://github.com/pingcap/tidb/issues/51560) @ [ウィノロス](https://github.com/winoros)が含まれている場合にクエリ結果が正しくない問題を修正しました
    -   `BINARY`タイプの JSON をクエリすると、場合によってはエラーが発生する可能性がある問題を修正しました[＃51547](https://github.com/pingcap/tidb/issues/51547) @ [ヤンケオ](https://github.com/YangKeao)
    -   テーブルにクラスター化インデックス[＃51372](https://github.com/pingcap/tidb/issues/51372) @ [グオシャオゲ](https://github.com/guo-shaoge)がある場合に並列`Apply`で誤った結果が生成される可能性がある問題を修正しました。
    -   `init-stats`プロセスが TiDB をpanicに陥らせ、 `load stats`プロセスが[＃51581](https://github.com/pingcap/tidb/issues/51581) @ [ホーキングレイ](https://github.com/hawkingrei)で終了する可能性がある問題を修正しました。
    -   `auto analyze`がパーティション テーブル[＃47594](https://github.com/pingcap/tidb/issues/47594) @ [ホーキングレイ](https://github.com/hawkingrei)を処理しているときに`tidb_merge_partition_stats_concurrency`変数が有効にならない問題を修正しました。
    -   自動統計更新の時間枠を設定した後、その時間枠外でも統計が更新される可能性がある問題を修正[＃49552](https://github.com/pingcap/tidb/issues/49552) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `approx_percentile`関数が TiDBpanic[＃40463](https://github.com/pingcap/tidb/issues/40463) @ [翻訳者](https://github.com/xzhangxian1008)を引き起こす可能性がある問題を修正
    -   `BIT`型の列が一部の関数の計算に関係する場合にデコード失敗によりクエリ エラーが発生する可能性がある問題を修正しました[＃49566](https://github.com/pingcap/tidb/issues/49566) [＃50850](https://github.com/pingcap/tidb/issues/50850) [＃50855](https://github.com/pingcap/tidb/issues/50855) @ [ジフハウス](https://github.com/jiyfhust)
    -   CTE クエリのメモリ使用量が制限[＃50337](https://github.com/pingcap/tidb/issues/50337) @ [グオシャオゲ](https://github.com/guo-shaoge)を超えた場合に発生する goroutine リークの問題を修正しました。
    -   `force-init-stats` [＃51473](https://github.com/pingcap/tidb/issues/51473) @ [ホーキングレイ](https://github.com/hawkingrei)に設定されている場合に TiDB が対応するポートをリッスンしない問題を修正
    -   主キータイプが`VARCHAR` [＃51810](https://github.com/pingcap/tidb/issues/51810) @ [そよ風のような](https://github.com/breezewish)の場合に`ALTER TABLE ... COMPACT TIFLASH REPLICA`が誤って終了する可能性がある問題を修正しました
    -   `tidb_server_memory_limit`変数が変更された後に`tidb_gogc_tuner_threshold`システム変数がそれに応じて調整されない問題を修正[＃48180](https://github.com/pingcap/tidb/issues/48180) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   集計関数をグループ計算に使用した場合に発生する可能性のある`Can't find column ...`エラーを修正[＃50926](https://github.com/pingcap/tidb/issues/50926) @ [qw4990](https://github.com/qw4990)
    -   `BIT`タイプの列[＃50850](https://github.com/pingcap/tidb/issues/50850) [＃50855](https://github.com/pingcap/tidb/issues/50855) @ [ジフハウス](https://github.com/jiyfhust)を処理するときに`REVERSE`関数がエラーを報告する問題を修正しました
    -   DDL操作中のテーブルにデータを一括挿入するとエラー`INSERT IGNORE`報告される問題を修正[＃50993](https://github.com/pingcap/tidb/issues/50993) @ [ヤンケオ](https://github.com/YangKeao)
    -   TiDBサーバーがHTTP インターフェース経由でラベルを追加し、成功を返すが、有効にならない問題を修正[＃51427](https://github.com/pingcap/tidb/issues/51427) @ [あなた06](https://github.com/you06)
    -   `IFNULL`関数によって返される型が MySQL [＃51765](https://github.com/pingcap/tidb/issues/51765) @ [ヤンケオ](https://github.com/YangKeao)と一致しない問題を修正
    -   初期化が完了する前に TiDBサーバーが正常とマークされる問題を修正[＃51596](https://github.com/pingcap/tidb/issues/51596) @ [神奇徳宝子](https://github.com/shenqidebaozi)
    -   `TIDB_HOT_REGIONS`テーブルをクエリすると、誤って`INFORMATION_SCHEMA`テーブル[＃50810](https://github.com/pingcap/tidb/issues/50810) @ [定義2014](https://github.com/Defined2014)が返される可能性がある問題を修正しました。
    -   `EXCHANGE PARTITION`外部キー[＃51807](https://github.com/pingcap/tidb/issues/51807) @ [ヤンケオ](https://github.com/YangKeao)を誤って処理する問題を修正
    -   CTE を含むクエリを実行すると TiDB がpanicになる問題を修正[＃41688](https://github.com/pingcap/tidb/issues/41688) @ [スタック](https://github.com/srstack)

-   ティクヴ

    -   スナップショットの適用によりピアの破棄処理が中断された後、スナップショットの適用が完了しても再開されない問題を修正[＃16561](https://github.com/tikv/tikv/issues/16561) @ [トニー](https://github.com/tonyxuqqi)
    -   RocksDB の非アクティブな Write Ahead Logs (WAL) によってデータが破損する可能性がある問題を修正[＃16705](https://github.com/tikv/tikv/issues/16705) @ [コナー1996](https://github.com/Connor1996)
    -   TiKV がブラジルとエジプトのタイムゾーンを誤って変換する問題を修正[＃16220](https://github.com/tikv/tikv/issues/16220) @ [金星の上](https://github.com/overvenus)
    -   監視メトリック`tikv_unified_read_pool_thread_count`にデータがない場合がある問題を修正[＃16629](https://github.com/tikv/tikv/issues/16629) @ [ユジュンセン](https://github.com/YuJuncen)
    -   最大値`INT64`より大きく最大値`UINT64`より小さい JSON 整数が TiKV によって`FLOAT64`として解析され、TiDB [＃16512](https://github.com/tikv/tikv/issues/16512) @ [ヤンケオ](https://github.com/YangKeao)との不整合が発生する問題を修正しました。
    -   楽観的トランザクションの実行中に、他のトランザクションがそのトランザクションに対してロック解決操作を開始すると、トランザクションの主キーに非同期コミットまたは 1PC モード[＃16620](https://github.com/tikv/tikv/issues/16620) @ [ミョンケミンタ](https://github.com/MyonKeminta)で以前にコミットされたデータが含まれている場合に、トランザクションの原子性が壊れる可能性がわずかにある問題を修正しました。

-   PD

    -   スケーリングの進行状況が正しく表示されない問題を修正[＃7726](https://github.com/tikv/pd/issues/7726) @ [キャビンフィーバーB](https://github.com/CabinfeverB)
    -   `MergeLabels`関数が[＃7535](https://github.com/tikv/pd/issues/7535) @ [翻訳者](https://github.com/lhy1024)で呼び出されたときにデータ競合が発生する問題を修正
    -   リーダースイッチ[＃7728](https://github.com/tikv/pd/issues/7728) @ [キャビンフィーバーB](https://github.com/CabinfeverB)後にPD監視項目`learner-peer-count`古い値を同期しない問題を修正
    -   クエリ結果`SHOW CONFIG`に非推奨の構成項目`trace-region-flow` [＃7917](https://github.com/tikv/pd/issues/7917) @ [rleungx](https://github.com/rleungx)が含まれる問題を修正しました

-   TiFlash

    -   レプリカ移行中にPDとのネットワーク接続が不安定になり、 TiFlashがpanic可能性がある問題を修正[＃8323](https://github.com/pingcap/tiflash/issues/8323) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   リモート読み取り[＃8685](https://github.com/pingcap/tiflash/issues/8685) @ [ソロッツ](https://github.com/solotzg)の場合にデータ競合によりTiFlash がクラッシュする可能性がある問題を修正しました
    -   チャンクエンコード[＃8674](https://github.com/pingcap/tiflash/issues/8674) @ [いいえ](https://github.com/yibin87)中に`ENUM`列目が原因でTiFlashがクラッシュする可能性がある問題を修正
    -   非厳密な`sql_mode` [＃8803](https://github.com/pingcap/tiflash/issues/8803) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)で無効なデフォルト値を持つ列にデータを挿入するとTiFlash がpanicになる可能性がある問題を修正しました
    -   `TIME`列の精度が変更された後にリージョンの移行、分割、またはマージが発生すると、クエリが失敗する可能性がある問題を修正しました[＃8601](https://github.com/pingcap/tiflash/issues/8601) @ [ジェイソン・ホアン](https://github.com/JaySon-Huang)

-   ツール

    -   バックアップと復元 (BR)

        -   フルバックアップが失敗したときにログが多すぎるという問題を修正[＃51572](https://github.com/pingcap/tidb/issues/51572) @ [リーヴルス](https://github.com/Leavrth)
        -   ログバックアップタスクを一時停止後に削除しても、GCセーフポイント[＃52082](https://github.com/pingcap/tidb/issues/52082) @ [3ポインター](https://github.com/3pointer)がすぐに復元されない問題を修正しました。
        -   BR が`AUTO_RANDOM`列[＃52255](https://github.com/pingcap/tidb/issues/52255) @ [リーヴルス](https://github.com/Leavrth)を含むユニオン クラスター化インデックスの`AUTO_RANDOM` ID 割り当ての進行状況をバックアップできない問題を修正しました。
        -   ログバックアップタスクを停止すると TiDB がクラッシュする問題を修正[＃50839](https://github.com/pingcap/tidb/issues/50839) @ [ユジュンセン](https://github.com/YuJuncen)
        -   極端なケースでフルバックアップがピアを見つけられなかった場合に TiKV がパニックになる問題を修正[＃16394](https://github.com/tikv/tikv/issues/16394) @ [リーヴルス](https://github.com/Leavrth)

    -   ティCDC

        -   変更フィードを再開するときに`snapshot lost caused by GC`時間内に報告されず、変更フィードの`checkpoint-ts` TiDB [＃10463](https://github.com/pingcap/tiflow/issues/10463) @ [スドジ](https://github.com/sdojjy)の GC セーフポイントよりも小さい問題を修正しました。
        -   DDL 文が頻繁に実行されるシナリオで、間違った BarrierTS が原因でデータが間違った CSV ファイルに書き込まれる問題を修正[＃10668](https://github.com/pingcap/tiflow/issues/10668) @ [リデズ](https://github.com/lidezhu)
        -   同期ポイントテーブルが誤って複製される可能性がある問題を修正[＃10576](https://github.com/pingcap/tiflow/issues/10576) @ [アズドンメン](https://github.com/asddongmen)
        -   テーブルレプリケーションタスク[＃10613](https://github.com/pingcap/tiflow/issues/10613) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)をスケジュールするときに TiCDC がパニックになる問題を修正
        -   KV クライアントでのデータ競合により TiCDC がpanic[＃10718](https://github.com/pingcap/tiflow/issues/10718) @ [アズドンメン](https://github.com/asddongmen)になる問題を修正
        -   storageシンク[＃10352](https://github.com/pingcap/tiflow/issues/10352) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)の使用時に、storageサービスによって生成されたファイルシーケンス番号が正しく増加しない可能性がある問題を修正しました。
        -   storageシンクシナリオ[＃10592](https://github.com/pingcap/tiflow/issues/10592) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)で TiCDC が Azure および GCS に正しくアクセスできない問題を修正
        -   `open-protocol`の古い値部分が、実際のタイプ[＃10803](https://github.com/pingcap/tiflow/issues/10803) @ [3エースショーハンド](https://github.com/3AceShowHand)ではなく、タイプ`STRING`に従ってデフォルト値を誤って出力する問題を修正しました。
        -   オブジェクトstorageシンクで一時的な障害が発生した場合に、結果整合性が有効になっている変更フィードが失敗する可能性がある問題を修正しました[＃10710](https://github.com/pingcap/tiflow/issues/10710) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)

    -   TiDB データ移行 (DM)

        -   アップストリームの主キーがバイナリタイプ[＃10672](https://github.com/pingcap/tiflow/issues/10672) @ [GMHDBJD](https://github.com/GMHDBJD)の場合にデータが失われる問題を修正しました

    -   TiDB Lightning

        -   ファイルスキャン中に無効なシンボリックリンクファイルに遭遇すると、 TiDB Lightning がエラーを報告する問題を修正[＃49423](https://github.com/pingcap/tidb/issues/49423) @ [ランス6716](https://github.com/lance6716)
