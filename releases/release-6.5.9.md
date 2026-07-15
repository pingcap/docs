---
title: TiDB 6.5.9 Release Notes
summary: TiDB 6.5.9 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 6.5.9 リリースノート {#tidb-6-5-9-release-notes}

発売日：2024年4月12日

TiDB バージョン: 6.5.9

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   RocksDB の TiKV 構成項目[`track-and-verify-wals-in-manifest`](https://docs.pingcap.com/tidb/v6.5/tikv-configuration-file#track-and-verify-wals-in-manifest-new-in-v659)追加します。これは、Write Ahead Log (WAL) の破損の可能性を調査するのに役立ちます。 [＃16549](https://github.com/tikv/tikv/issues/16549) @ [v01dstar](https://github.com/v01dstar)
-   DR自動同期は[`wait-recover-timeout`](https://docs.pingcap.com/tidb/v6.5/two-data-centers-in-one-city-deployment#enable-the-dr-auto-sync-mode)設定をサポートしており、ネットワークが回復した後、 `sync-recover`状態に戻るまでの待機時間を制御できます[＃6295](https://github.com/tikv/pd/issues/6295) @ [disksing](https://github.com/disksing)

## 改善点 {#improvements}

-   TiDB

    -   `force-init-stats` `true`に設定すると、TiDB は起動時にサービスを提供する前に統計情報の初期化が完了するのを待ちます。この設定により HTTP サーバーの起動がブロックされなくなり、ユーザーはで監視を継続できます。 [＃50854](https://github.com/pingcap/tidb/issues/50854) @ [hawkingrei](https://github.com/hawkingrei)
    -   `ANALYZE`文がメタデータロックをブロックする問題を最適化します [＃47475](https://github.com/pingcap/tidb/issues/47475) @ [wjhuang2016](https://github.com/wjhuang2016)

-   TiKV

    -   不要な非同期ブロックを削除してメモリ使用量を削減する[＃16540](https://github.com/tikv/tikv/issues/16540) @ [overvenus](https://github.com/overvenus)
    -   TiKV の安定性を向上させるために、raftstore スレッドでスナップショット ファイルに対する IO 操作を実行しないようにします[＃16564](https://github.com/tikv/tikv/issues/16564) @ [Connor1996](https://github.com/Connor1996)
    -   ピアのスローログを追加し、メッセージを保存します [＃16600](https://github.com/tikv/tikv/issues/16600) @ [Connor1996](https://github.com/Connor1996)

-   ツール

    -   Backup & Restore (BR)

        -   ローリング再起動時のログバックアップのRPO（目標復旧時点）を最適化します。これにより、ローリング再起動時のログバックアップタスクのチェックポイントラグが短縮されます[＃15410](https://github.com/tikv/tikv/issues/15410) @ [YuJuncen](https://github.com/YuJuncen) 。
        -   ログバックアップのマージ操作に対する許容度を向上します。比較的長いマージ操作が発生した場合、ログバックアップタスクがエラー状態に陥る可能性が低くなります。 [＃16554](https://github.com/tikv/tikv/issues/16554) @ [YuJuncen](https://github.com/YuJuncen)
        -   チェックポイントの遅延が大きい場合にログ バックアップ タスクを自動的に中止する機能をサポートし、GC の長時間のブロッキングや潜在的なクラスターの問題を回避します[＃50803](https://github.com/pingcap/tidb/issues/50803) @ [RidRisR](https://github.com/RidRisR)
        -   リージョンリーダーシップの移行が発生すると、PITR ログバックアップの進行のレイテンシーが長くなるという問題を軽減します[＃13638](https://github.com/tikv/tikv/issues/13638) @ [YuJuncen](https://github.com/YuJuncen)
        -   より効率的なアルゴリズムを使用して、データ復元中に SST ファイルをマージする速度を改善します [＃50613](https://github.com/pingcap/tidb/issues/50613) @ [Leavrth](https://github.com/Leavrth)
        -   データ復元中に SST ファイルをバッチで取り込むことをサポート[＃16267](https://github.com/tikv/tikv/issues/16267) @ [3pointer](https://github.com/3pointer)
        -   Google Cloud Storage（GCS）を外部ストレージとして使用する場合の古い互換性チェックを削除します[＃50533](https://github.com/pingcap/tidb/issues/50533) @ [lance6716](https://github.com/lance6716)
        -   ログバックアップ中に、ログとメトリックのグローバルチェックポイントの進行に影響を与える最も遅いリージョンの情報を出力します。 [＃51046](https://github.com/pingcap/tidb/issues/51046) @ [YuJuncen](https://github.com/YuJuncen)
        -   BR例外処理メカニズムをリファクタリングして、未知のエラーに対する許容度を高めます[＃47656](https://github.com/pingcap/tidb/issues/47656) @ [3pointer](https://github.com/3pointer)

## バグ修正 {#bug-fixes}

-   TiDB

    -   ドロップされたテーブルがGrafana `Stats Healthy Distribution`パネルでまだカウントされる問題を修正 [＃39349](https://github.com/pingcap/tidb/issues/39349) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    -   SQL文のクエリに`MemTableScan`の演算子が含まれている場合、TiDBがSQL文の`WHERE <column_name>`のフィルタリング条件を処理しない問題を修正しました。 [＃40937](https://github.com/pingcap/tidb/issues/40937) @ [zhongzc](https://github.com/zhongzc)
    -   サブクエリの`HAVING`句に相関列が含まれている場合にクエリ結果が正しくない可能性がある問題を修正しました。 [＃51107](https://github.com/pingcap/tidb/issues/51107) @ [hawkingrei](https://github.com/hawkingrei)
    -   共通テーブル式 (CTE) を使用して、統計情報が欠落しているパーティション テーブルにアクセスすると、クエリ結果が正しくなくなる可能性がある問題を修正しました[＃51873](https://github.com/pingcap/tidb/issues/51873) @ [qw4990](https://github.com/qw4990)
    -   SQL 文に`JOIN`が含まれ、文内の`SELECT`リストに定数のみが含まれる場合に、MPP を使用してクエリを実行すると、誤ったクエリ結果が返される可能性がある問題を修正しました。 [＃50358](https://github.com/pingcap/tidb/issues/50358) @ [yibin87](https://github.com/yibin87)
    -   AUTO_INCREMENT ID を割り当てるときに、 `AUTO_INCREMENT`属性によって不要なトランザクション競合が発生し、ID が連続しなくなる問題を修正しました。 [＃50819](https://github.com/pingcap/tidb/issues/50819) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   Grafana の監視メトリック`tidb_statistics_auto_analyze_total`整数として表示されない問題を修正しました [＃51051](https://github.com/pingcap/tidb/issues/51051) @ [hawkingrei](https://github.com/hawkingrei)
    -   パーティションテーブルのグローバル統計の同時マージ中にエラーが返される可能性がある問題を修正しました。 [＃48713](https://github.com/pingcap/tidb/issues/48713) @ [hawkingrei](https://github.com/hawkingrei)
    -   列のデフォルト値が削除されている場合、列のデフォルト値を取得するとエラーが返される問題を修正[＃50043](https://github.com/pingcap/tidb/issues/50043) [＃51324](https://github.com/pingcap/tidb/issues/51324) @ [crazycs520](https://github.com/crazycs520)
    -   列が書き込み専用の場合に`INSERT ignore`文でデフォルト値を入力できない問題を修正[＃40192](https://github.com/pingcap/tidb/issues/40192) @ [YangKeao](https://github.com/YangKeao)
    -   `shuffleExec`予期せず終了すると TiDB がクラッシュする問題を修正[＃48230](https://github.com/pingcap/tidb/issues/48230) @ [wshwsh12](https://github.com/wshwsh12)
    -   `HashJoin`演算子がディスクにスピルできない場合に発生する可能性のある goroutine リークの問題を修正しました。 [＃50841](https://github.com/pingcap/tidb/issues/50841) @ [wshwsh12](https://github.com/wshwsh12)
    -   トランザクションで複数のステートメントをコミットするときにテーブル名の変更が有効にならない問題を修正しました [＃39664](https://github.com/pingcap/tidb/issues/39664) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   `IN()`述語に`NULL` が含まれている場合にクエリ結果が正しくない問題を修正しました [＃51560](https://github.com/pingcap/tidb/issues/51560) @ [winoros](https://github.com/winoros)
    -   `BINARY`タイプの JSON をクエリすると、場合によってはエラーが発生する可能性がある問題を修正しました[＃51547](https://github.com/pingcap/tidb/issues/51547) @ [YangKeao](https://github.com/YangKeao)
    -   テーブルにクラスター化インデックスがある場合に並列`Apply`で誤った結果が生成される可能性がある問題を修正しました。 [＃51372](https://github.com/pingcap/tidb/issues/51372) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   `init-stats`プロセスが TiDB をpanicに陥らせ、 `load stats`プロセスが終了する可能性がある問題を修正しました。 [＃51581](https://github.com/pingcap/tidb/issues/51581) @ [hawkingrei](https://github.com/hawkingrei)
    -   `auto analyze`パーティションテーブルを処理しているときに`tidb_merge_partition_stats_concurrency`変数が有効にならない問題を修正しました [＃47594](https://github.com/pingcap/tidb/issues/47594) @ [hawkingrei](https://github.com/hawkingrei)
    -   自動統計更新の時間枠を設定した後、その時間枠外でも統計が更新される可能性がある問題を修正[＃49552](https://github.com/pingcap/tidb/issues/49552) @ [hawkingrei](https://github.com/hawkingrei)
    -   `approx_percentile`関数が TiDB panicを引き起こす可能性がある問題を修正しました [＃40463](https://github.com/pingcap/tidb/issues/40463) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   `BIT`型の列が一部の関数の計算に関係する場合にデコード失敗によりクエリエラーが発生する可能性がある問題を修正しました[＃49566](https://github.com/pingcap/tidb/issues/49566) [＃50850](https://github.com/pingcap/tidb/issues/50850) [＃50855](https://github.com/pingcap/tidb/issues/50855) @ [jiyfhust](https://github.com/jiyfhust)
    -   CTEクエリのメモリ使用量が制限を超えたときに発生するゴルーチンリークの問題を修正しました [＃50337](https://github.com/pingcap/tidb/issues/50337) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   `force-init-stats` に設定されている場合に TiDB が対応するポートを listen しない問題を修正しました [＃51473](https://github.com/pingcap/tidb/issues/51473) @ [hawkingrei](https://github.com/hawkingrei)
    -   主キーの型が`VARCHAR` の場合に`ALTER TABLE ... COMPACT TIFLASH REPLICA`誤って終了する可能性がある問題を修正しました [＃51810](https://github.com/pingcap/tidb/issues/51810) @ [breezewish](https://github.com/breezewish)
    -   `tidb_server_memory_limit`変数がに変更された後、 `tidb_gogc_tuner_threshold`システム変数がそれに応じて調整されない問題を修正しました [＃48180](https://github.com/pingcap/tidb/issues/48180) @ [hawkingrei](https://github.com/hawkingrei)
    -   集計関数をグループ計算に使用すると発生する可能性のある`Can't find column ...`エラーを修正[＃50926](https://github.com/pingcap/tidb/issues/50926) @ [qw4990](https://github.com/qw4990)
    -   `BIT`タイプの列 を処理するときに`REVERSE`関数がエラーを報告する問題を修正しました [＃50855](https://github.com/pingcap/tidb/issues/50855) @ [jiyfhust](https://github.com/jiyfhust) [＃50850](https://github.com/pingcap/tidb/issues/50850)
    -   DDL操作を実行しているテーブルにデータを一括挿入するときにエラーが報告される問題を修正しました`INSERT IGNORE` [＃50993](https://github.com/pingcap/tidb/issues/50993) @ [YangKeao](https://github.com/YangKeao)
    -   TiDBサーバーがHTTPインターフェース経由でラベルを追加し成功を返すが、それが有効にならない問題を修正[＃51427](https://github.com/pingcap/tidb/issues/51427) @ [you06](https://github.com/you06)
    -   `IFNULL`関数によって返される型が MySQL と一致しない問題を修正しました [＃51765](https://github.com/pingcap/tidb/issues/51765) @ [YangKeao](https://github.com/YangKeao)
    -   初期化が完了する前に TiDBサーバーが正常とマークされる問題を修正[＃51596](https://github.com/pingcap/tidb/issues/51596) @ [shenqidebaozi](https://github.com/shenqidebaozi)
    -   `TIDB_HOT_REGIONS`テーブルをクエリすると、誤って`INFORMATION_SCHEMA`テーブルが返される可能性がある問題を修正しました。 [＃50810](https://github.com/pingcap/tidb/issues/50810) @ [Defined2014](https://github.com/Defined2014)
    -   `EXCHANGE PARTITION`外部キーを誤って処理する問題を修正 [＃51807](https://github.com/pingcap/tidb/issues/51807) @ [YangKeao](https://github.com/YangKeao)
    -   CTE を含むクエリを実行すると TiDB がpanicになる問題を修正[＃41688](https://github.com/pingcap/tidb/issues/41688) @ [srstack](https://github.com/srstack)

-   TiKV

    -   スナップショットの適用によってピアの破棄処理が中断された後、スナップショットの適用が完了しても再開されない問題を修正[＃16561](https://github.com/tikv/tikv/issues/16561) @ [tonyxuqqi](https://github.com/tonyxuqqi)
    -   RocksDB の非アクティブな Write Ahead Logs (WAL) によってデータが破損する可能性がある問題を修正しました[＃16705](https://github.com/tikv/tikv/issues/16705) @ [Connor1996](https://github.com/Connor1996)
    -   TiKVがブラジルとエジプトのタイムゾーンを誤って変換する問題を修正[＃16220](https://github.com/tikv/tikv/issues/16220) @ [overvenus](https://github.com/overvenus)
    -   監視メトリック`tikv_unified_read_pool_thread_count`にデータがない場合がある問題を修正[＃16629](https://github.com/tikv/tikv/issues/16629) @ [YuJuncen](https://github.com/YuJuncen)
    -   JSON 整数の最大値`INT64`より大きく最大値`UINT64`より小さい値が TiKV によって`FLOAT64`として解析され、TiDB との不整合が発生する問題を修正しました。 [＃16512](https://github.com/tikv/tikv/issues/16512) @ [YangKeao](https://github.com/YangKeao)
    -   楽観的トランザクションの実行中に、他のトランザクションがそのトランザクションのロック解決操作を開始すると、トランザクションの主キーに非同期コミットまたは 1PC モードで以前にコミットされたデータがある場合、トランザクションの原子性が壊れる可能性がわずかにあるという問題を修正しました。 [＃16620](https://github.com/tikv/tikv/issues/16620) @ [MyonKeminta](https://github.com/MyonKeminta)

-   PD

    -   スケーリングの進行状況が正しく表示されない問題を修正[＃7726](https://github.com/tikv/pd/issues/7726) @ [CabinfeverB](https://github.com/CabinfeverB)
    -   `MergeLabels`関数が呼び出されたときにデータ競合が発生する問題を修正しました [＃7535](https://github.com/tikv/pd/issues/7535) @ [lhy1024](https://github.com/lhy1024)
    -   リーダースイッチ後にPD監視項目`learner-peer-count`古い値を同期しない問題を修正 [＃7728](https://github.com/tikv/pd/issues/7728) @ [CabinfeverB](https://github.com/CabinfeverB)
    -   クエリ結果`SHOW CONFIG`に非推奨の構成項目`trace-region-flow` が含まれる問題を修正しました [＃7917](https://github.com/tikv/pd/issues/7917) @ [rleungx](https://github.com/rleungx)

-   TiFlash

    -   レプリカ移行中に PD とのネットワーク接続が不安定になり、 TiFlash がpanic可能性がある問題を修正しました [＃8323](https://github.com/pingcap/tiflash/issues/8323) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   リモート読み取りの場合にデータ競合によりTiFlash がクラッシュする可能性がある問題を修正しました [＃8685](https://github.com/pingcap/tiflash/issues/8685) @ [solotzg](https://github.com/solotzg)
    -   チャンクエンコード中に`ENUM`列がTiFlashを引き起こす可能性がある問題を修正しました [＃8674](https://github.com/pingcap/tiflash/issues/8674) @ [yibin87](https://github.com/yibin87)
    -   非厳密モードの`sql_mode` で無効なデフォルト値を持つ列にデータを挿入するとTiFlash がpanic可能性がある問題を修正しました [＃8803](https://github.com/pingcap/tiflash/issues/8803) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   `TIME`列の精度が変更された後にリージョンの移行、分割、またはマージが発生すると、クエリが失敗する可能性がある問題を修正しました。 [＃8601](https://github.com/pingcap/tiflash/issues/8601) @ [JaySon-Huang](https://github.com/JaySon-Huang)

-   ツール

    -   Backup & Restore (BR)

        -   フルバックアップが失敗したときにログが多すぎる問題を修正[＃51572](https://github.com/pingcap/tidb/issues/51572) @ [Leavrth](https://github.com/Leavrth)
        -   ログバックアップタスクを一時停止後に削除しても、GCセーフポイントがすぐに復元されない問題を修正しました。 [＃52082](https://github.com/pingcap/tidb/issues/52082) @ [3pointer](https://github.com/3pointer)
        -   BRが`AUTO_RANDOM`列を含むユニオンクラスター化インデックスの`AUTO_RANDOM` ID割り当ての進行状況をバックアップできなかった問題を修正しました。 [＃52255](https://github.com/pingcap/tidb/issues/52255) @ [Leavrth](https://github.com/Leavrth)
        -   ログバックアップタスクを停止すると TiDB がクラッシュする問題を修正[＃50839](https://github.com/pingcap/tidb/issues/50839) @ [YuJuncen](https://github.com/YuJuncen)
        -   フルバックアップでピアが見つからない場合に TiKV がパニックを起こす問題を修正[＃16394](https://github.com/tikv/tikv/issues/16394) @ [Leavrth](https://github.com/Leavrth)

    -   TiCDC

        -   変更フィードを再開するときに`snapshot lost caused by GC`時間内に報告されず、変更フィードの`checkpoint-ts` TiDB の GC セーフポイントよりも小さい問題を修正しました。 [＃10463](https://github.com/pingcap/tiflow/issues/10463) @ [sdojjy](https://github.com/sdojjy)
        -   DDL文が頻繁に実行されるシナリオで、間違ったBarrierTSが原因でデータが間違ったCSVファイルに書き込まれる問題を修正[＃10668](https://github.com/pingcap/tiflow/issues/10668) @ [lidezhu](https://github.com/lidezhu)
        -   同期ポイントテーブルが誤って複製される可能性がある問題を修正[＃10576](https://github.com/pingcap/tiflow/issues/10576) @ [asddongmen](https://github.com/asddongmen)
        -   テーブルレプリケーションタスクをスケジュールするときに TiCDC がパニックになる問題を修正しました [＃10613](https://github.com/pingcap/tiflow/issues/10613) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   KVクライアントのデータ競合によりTiCDCがpanicになる問題を修正 [＃10718](https://github.com/pingcap/tiflow/issues/10718) @ [asddongmen](https://github.com/asddongmen)
        -   ストレージシンク使用時に、ストレージサービスによって生成されたファイルシーケンス番号が正しく増加しない可能性がある問題を修正しました。 [＃10352](https://github.com/pingcap/tiflow/issues/10352) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   ストレージシンクシナリオでTiCDCがAzureとGCSに正しくアクセスできない問題を修正 [＃10592](https://github.com/pingcap/tiflow/issues/10592) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   `open-protocol`の古い値部分が、実際のタイプではなく、タイプ`STRING`に応じて誤ってデフォルト値を出力する問題を修正しました。 [＃10803](https://github.com/pingcap/tiflow/issues/10803) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   オブジェクトストレージシンクに一時的な障害が発生した場合に、結果整合性が有効になっている変更フィードが失敗する可能性がある問題を修正しました[＃10710](https://github.com/pingcap/tiflow/issues/10710) @ [CharlesCheung96](https://github.com/CharlesCheung96)

    -   TiDB Data Migration (DM)

        -   アップストリーム主キーがバイナリ型の場合にデータが失われる問題を修正しました [＃10672](https://github.com/pingcap/tiflow/issues/10672) @ [GMHDBJD](https://github.com/GMHDBJD)

    -   TiDB Lightning

        -   ファイルスキャン中に無効なシンボリックリンクファイルに遭遇すると、 TiDB Lightning がエラーを報告する問題を修正しました[＃49423](https://github.com/pingcap/tidb/issues/49423) @ [lance6716](https://github.com/lance6716)
