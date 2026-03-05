---
title: TiDB 7.1.5 Release Notes
summary: TiDB 7.1.5 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 7.1.5 リリースノート {#tidb-7-1-5-release-notes}

発売日：2024年4月26日

TiDB バージョン: 7.1.5

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   RocksDB の TiKV 構成項目[`track-and-verify-wals-in-manifest`](https://docs.pingcap.com/tidb/v7.1/tikv-configuration-file#track-and-verify-wals-in-manifest-new-in-v659-and-v715)追加します。これは、Write Ahead Log (WAL) [＃16549](https://github.com/tikv/tikv/issues/16549) @ [v01dstar](https://github.com/v01dstar)の破損の可能性を調査するのに役立ちます。

## 改善点 {#improvements}

-   TiDB

    -   PD からリージョンを一括ロードすることをサポートし、大規模なテーブル[＃51326](https://github.com/pingcap/tidb/issues/51326) @ [シーライズ](https://github.com/SeaRise)をクエリするときに KV 範囲からリージョンへの変換プロセスを高速化します。
    -   `ANALYZE`文がメタデータロック[＃47475](https://github.com/pingcap/tidb/issues/47475) @ [wjhuang2016](https://github.com/wjhuang2016)をブロックする問題を最適化します
    -   リソースロック（RLock）が[＃51883](https://github.com/pingcap/tidb/issues/51883)内に解放されない問題を回避するために、LDAP認証にタイムアウトメカニズムを追加します[ヤンケオ](https://github.com/YangKeao)

-   TiKV

    -   ピアのスローログを追加し、メッセージ[＃16600](https://github.com/tikv/tikv/issues/16600) @ [コナー1996](https://github.com/Connor1996)を保存します
    -   TiKV の安定性を向上させるために、raftstore スレッドでスナップショット ファイルに対する IO 操作を実行しないようにします[＃16564](https://github.com/tikv/tikv/issues/16564) @ [コナー1996](https://github.com/Connor1996)

-   PD

    -   etcdのバージョンをv3.4.30 [＃7904](https://github.com/tikv/pd/issues/7904) @ [Jmポテト](https://github.com/JmPotato)にアップグレードします

-   ツール

    -   バックアップと復元 (BR)

        -   チェックポイントの遅延が大きい場合にログ バックアップ タスクを自動的に中止する機能をサポートし、GC の長時間のブロッキングや潜在的なクラスターの問題を回避します[＃50803](https://github.com/pingcap/tidb/issues/50803) @ [リドリスR](https://github.com/RidRisR)
        -   ログバックアップの互換性テストとインデックスアクセラレーション[＃51987](https://github.com/pingcap/tidb/issues/51987) @ [リーヴルス](https://github.com/Leavrth)をカバーするPITR統合テストケースを追加します。
        -   ログバックアップの開始時にアクティブなDDLジョブの無効な検証を削除します[＃52733](https://github.com/pingcap/tidb/issues/52733) @ [リーヴルス](https://github.com/Leavrth)

## バグ修正 {#bug-fixes}

-   TiDB

    -   `BINARY`タイプの JSON をクエリすると、場合によってはエラーが発生する可能性がある問題を修正しました[＃51547](https://github.com/pingcap/tidb/issues/51547) @ [ヤンケオ](https://github.com/YangKeao)
    -   SQL 文に`JOIN`が含まれ、文内の`SELECT`リストに定数[＃50358](https://github.com/pingcap/tidb/issues/50358) @ [イービン87](https://github.com/yibin87)のみが含まれる場合に、MPP を使用してクエリを実行すると、誤ったクエリ結果が返される可能性がある問題を修正しました。
    -   `init-stats`プロセスが TiDB をpanicに陥らせ、 `load stats`プロセスが[＃51581](https://github.com/pingcap/tidb/issues/51581) @ [ホーキングレイ](https://github.com/hawkingrei)で終了する可能性がある問題を修正しました。
    -   初期化が完了する前に TiDBサーバーが正常とマークされる問題を修正[＃51596](https://github.com/pingcap/tidb/issues/51596) @ [シェンキデバオジ](https://github.com/shenqidebaozi)
    -   主キーの型が`VARCHAR` [＃51810](https://github.com/pingcap/tidb/issues/51810) @ [そよ風のような](https://github.com/breezewish)の場合に`ALTER TABLE ... COMPACT TIFLASH REPLICA`誤って終了する可能性がある問題を修正しました
    -   `shuffleExec`予期せず終了すると TiDB がクラッシュする問題を修正[＃48230](https://github.com/pingcap/tidb/issues/48230) @ [wshwsh12](https://github.com/wshwsh12)
    -   特定の条件下で`SURVIVAL_PREFERENCES`属性が`SHOW CREATE PLACEMENT POLICY`ステートメントの出力に表示されない可能性がある問題を修正[＃51699](https://github.com/pingcap/tidb/issues/51699) @ [lcwangchao](https://github.com/lcwangchao)
    -   自動統計更新の時間枠を設定した後、その時間枠外でも統計が更新される可能性がある問題を修正[＃49552](https://github.com/pingcap/tidb/issues/49552) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   サブクエリの`HAVING`句に相関列[＃51107](https://github.com/pingcap/tidb/issues/51107) @ [ホーキングレイ](https://github.com/hawkingrei)が含まれている場合にクエリ結果が正しくない可能性がある問題を修正しました。
    -   `approx_percentile`関数が TiDBpanic[＃40463](https://github.com/pingcap/tidb/issues/40463) @ [xzhangxian1008](https://github.com/xzhangxian1008)を引き起こす可能性がある問題を修正しました
    -   `IN()`述語に`NULL` [＃51560](https://github.com/pingcap/tidb/issues/51560) @ [ウィノロス](https://github.com/winoros)が含まれている場合にクエリ結果が正しくない問題を修正しました
    -   無効な設定項目[＃51399](https://github.com/pingcap/tidb/issues/51399) @ [定義2014](https://github.com/Defined2014)が含まれている場合、設定ファイルが有効にならない問題を修正しました
    -   `EXCHANGE PARTITION`外部キー[＃51807](https://github.com/pingcap/tidb/issues/51807) @ [ヤンケオ](https://github.com/YangKeao)を誤って処理する問題を修正
    -   `TIDB_HOT_REGIONS`テーブルをクエリすると、誤って`INFORMATION_SCHEMA`テーブル[＃50810](https://github.com/pingcap/tidb/issues/50810) @ [定義2014](https://github.com/Defined2014)が返される可能性がある問題を修正しました。
    -   `IFNULL`関数によって返される型が MySQL [＃51765](https://github.com/pingcap/tidb/issues/51765) @ [ヤンケオ](https://github.com/YangKeao)と一致しない問題を修正しました
    -   TTL 機能により、データ範囲の分割が不正確になり、場合によっては[＃51527](https://github.com/pingcap/tidb/issues/51527) @ [lcwangchao](https://github.com/lcwangchao)でデータ ホットスポットが発生する問題を修正しました。
    -   TiDBがオフラインになっているTiFlashノードにプローブ要求を送信し続ける問題を修正[＃46602](https://github.com/pingcap/tidb/issues/46602) @ [ジグアン](https://github.com/zyguan)
    -   AutoIDLeaderの変更により、 `AUTO_ID_CACHE=1` [＃52600](https://github.com/pingcap/tidb/issues/52600) @ [天菜まお](https://github.com/tiancaiamao)の場合に自動増分列の値が減少する可能性がある問題を修正しました。
    -   `INSERT IGNORE`実行すると、一意のインデックスとデータ[＃51784](https://github.com/pingcap/tidb/issues/51784) @ [wjhuang2016](https://github.com/wjhuang2016)の間に不整合が発生する可能性がある問題を修正しました。
    -   ユニークインデックスを追加するとTiDBがpanic可能性がある問題を修正[＃52312](https://github.com/pingcap/tidb/issues/52312) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   関連するサブクエリがある場合にウィンドウ関数がpanic可能性がある問題を修正[＃42734](https://github.com/pingcap/tidb/issues/42734) @ [ハイラスティン](https://github.com/Rustin170506)
    -   `init-stats`プロセスが TiDB をpanicに陥らせ、 `load stats`プロセスが[＃51581](https://github.com/pingcap/tidb/issues/51581) @ [ホーキングレイ](https://github.com/hawkingrei)で終了する可能性がある問題を修正しました。
    -   TableDual [＃50614](https://github.com/pingcap/tidb/issues/50614) @ [時間と運命](https://github.com/time-and-fate)で述語プッシュダウンを無効にすることで発生するパフォーマンス低下の問題を修正しました
    -   サブクエリの`HAVING`句に相関列[＃51107](https://github.com/pingcap/tidb/issues/51107) @ [ホーキングレイ](https://github.com/hawkingrei)が含まれている場合にクエリ結果が正しくない可能性がある問題を修正しました。
    -   特定の列の統計情報が完全にロードされていない場合に、 `EXPLAIN`ステートメントの結果に誤った列 ID が表示される可能性がある問題を修正しました[＃52207](https://github.com/pingcap/tidb/issues/52207) @ [時間と運命](https://github.com/time-and-fate)

-   TiKV

    -   古いリージョンピアがGCメッセージ[＃16504](https://github.com/tikv/tikv/issues/16504) @ [crazycs520](https://github.com/crazycs520)を無視するとresolve-tsがブロックされる問題を修正しました
    -   RocksDB の非アクティブな Write Ahead Logs (WAL) によってデータが破損する可能性がある問題を修正しました[＃16705](https://github.com/tikv/tikv/issues/16705) @ [コナー1996](https://github.com/Connor1996)
    -   監視メトリック`tikv_unified_read_pool_thread_count`にデータがない場合がある問題を修正[＃16629](https://github.com/tikv/tikv/issues/16629) @ [ユジュンセン](https://github.com/YuJuncen)
    -   楽観的トランザクションの実行中に、他のトランザクションがそのトランザクションのロック解決操作を開始すると、トランザクションの主キーに非同期コミットまたは 1PC モード[＃16620](https://github.com/tikv/tikv/issues/16620) @ [ミョンケミンタ](https://github.com/MyonKeminta)で以前にコミットされたデータがある場合、トランザクションの原子性が壊れる可能性がわずかにあるという問題を修正しました。

-   PD

    -   書き込みホットスポットのスケジュール設定により配置ポリシーの制約が破られる可能性がある問題を修正[＃7848](https://github.com/tikv/pd/issues/7848) @ [lhy1024](https://github.com/lhy1024)
    -   クエリ結果`SHOW CONFIG`に非推奨の構成項目`trace-region-flow` [＃7917](https://github.com/tikv/pd/issues/7917) @ [rleungx](https://github.com/rleungx)が含まれる問題を修正しました
    -   スケーリングの進行状況が正しく表示されない問題を修正[＃7726](https://github.com/tikv/pd/issues/7726) @ [キャビンフィーバーB](https://github.com/CabinfeverB)

-   TiFlash

    -   ログ[＃8895](https://github.com/pingcap/tiflash/issues/8895) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)の誤った`local_region_num`値を修正
    -   生成された列をクエリするとエラー[＃8787](https://github.com/pingcap/tiflash/issues/8787) @ [グオシャオゲ](https://github.com/guo-shaoge)が返される問題を修正しました
    -   チャンクエンコード[＃8674](https://github.com/pingcap/tiflash/issues/8674) @ [イービン87](https://github.com/yibin87)中に`ENUM`列目がTiFlashを引き起こす可能性がある問題を修正しました
    -   非厳密な`sql_mode` [＃8803](https://github.com/pingcap/tiflash/issues/8803) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)で無効なデフォルト値を持つ列にデータを挿入するとTiFlash がpanic可能性がある問題を修正しました
    -   `TIME`列の精度が変更された後にリージョンの移行、分割、またはマージが発生すると、クエリが[＃8601](https://github.com/pingcap/tiflash/issues/8601) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)で失敗する可能性がある問題を修正しました。

-   ツール

    -   バックアップと復元 (BR)

        -   ログバックアップタスクを一時停止後に削除しても、GCセーフポイント[＃52082](https://github.com/pingcap/tidb/issues/52082) @ [3ポイントシュート](https://github.com/3pointer)がすぐに復元されない問題を修正しました。
        -   フルバックアップが失敗したときにログが多すぎる問題を修正[＃51572](https://github.com/pingcap/tidb/issues/51572) @ [リーヴルス](https://github.com/Leavrth)
        -   `AUTO_RANDOM`列が複合クラスタリングインデックス[＃52255](https://github.com/pingcap/tidb/issues/52255) @ [リーヴルス](https://github.com/Leavrth)にある場合、 BRが`AUTO_RANDOM` ID割り当ての進行状況をバックアップできなかった問題を修正します
        -   フルバックアップでピアが見つからない場合に TiKV がパニックを起こす問題を修正[＃16394](https://github.com/tikv/tikv/issues/16394) @ [リーヴルス](https://github.com/Leavrth)
        -   PD接続障害により、ログバックアップアドバンサ所有者が配置されているTiDBインスタンスがpanic[＃52597](https://github.com/pingcap/tidb/issues/52597) @ [ユジュンセン](https://github.com/YuJuncen)になる可能性がある問題を修正しました。
        -   不安定なテストケース[＃52547](https://github.com/pingcap/tidb/issues/52547) [リーヴルス](https://github.com/Leavrth)で修正する
        -   TiKV の再起動により、ログ バックアップのグローバル チェックポイントが実際のバックアップ ファイルの書き込みポイントよりも先に進められ、少量のバックアップ データが失われる可能性がある問題を修正しました[＃16809](https://github.com/tikv/tikv/issues/16809) @ [ユジュンセン](https://github.com/YuJuncen)
        -   特別なイベントタイミングにより、ログバックアップ[＃16739](https://github.com/tikv/tikv/issues/16739) @ [ユジュンセン](https://github.com/YuJuncen)でデータ損失が発生する可能性があるという稀な問題を修正しました。

    -   TiCDC

        -   TiCDC が上流に書き込まれた後に下流の`Exchange Partition ... With Validation` DDL の実行に失敗し、変更フィードが[＃10859](https://github.com/pingcap/tiflow/issues/10859) @ [ホンユニャン](https://github.com/hongyunyan)で停止する問題を修正しました。
        -   変更フィードを再開するときに`snapshot lost caused by GC`時間内に報告されず、変更フィードの`checkpoint-ts` TiDB [＃10463](https://github.com/pingcap/tiflow/issues/10463) @ [スドジ](https://github.com/sdojjy)の GC セーフポイントよりも小さい問題を修正しました。
        -   テーブルレプリケーションタスク[＃10613](https://github.com/pingcap/tiflow/issues/10613) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)をスケジュールするときに TiCDC がパニックになる問題を修正しました
        -   DDL文が頻繁に実行されるシナリオで、間違ったBarrierTSが原因でデータが間違ったCSVファイルに書き込まれる問題を修正[＃10668](https://github.com/pingcap/tiflow/issues/10668) @ [リデジュ](https://github.com/lidezhu)
        -   オブジェクトstorageシンクに一時的な障害が発生した場合に、結果整合性が有効になっている変更フィードが失敗する可能性がある問題を修正しました[＃10710](https://github.com/pingcap/tiflow/issues/10710) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   `open-protocol`の古い値部分が、実際のタイプ[＃10803](https://github.com/pingcap/tiflow/issues/10803) @ [3エースショーハンド](https://github.com/3AceShowHand)ではなく、タイプ`STRING`に応じて誤ってデフォルト値を出力する問題を修正しました。

    -   TiDB Lightning

        -   Parquet 形式[＃52518](https://github.com/pingcap/tidb/issues/52518) @ [ケニーtm](https://github.com/kennytm)の空のテーブルをインポートするときにTiDB Lightning がパニックになる問題を修正しました
        -   ログ内の機密情報がサーバーモード[＃36374](https://github.com/pingcap/tidb/issues/36374) @ [ケニーtm](https://github.com/kennytm)で印刷される問題を修正
