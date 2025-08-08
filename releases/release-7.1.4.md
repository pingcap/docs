---
title: TiDB 7.1.4 Release Notes
summary: TiDB 7.1.4 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 7.1.4 リリースノート {#tidb-7-1-4-release-notes}

発売日：2024年3月11日

TiDB バージョン: 7.1.4

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   ログ印刷のオーバーヘッドを減らすために、 TiFlashはデフォルト値の`logger.level`を`"debug"`から`"info"` [＃8641](https://github.com/pingcap/tiflash/issues/8641) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)に変更します。
-   TiKV構成項目[`gc.num-threads`](https://docs.pingcap.com/tidb/v6.5/tikv-configuration-file#num-threads-new-in-v658)を導入して、 `enable-compaction-filter`が`false` [＃16101](https://github.com/tikv/tikv/issues/16101) @ [トニー・シュッキ](https://github.com/tonyxuqqi)の場合のGCスレッド数を設定します。

## 改善点 {#improvements}

-   TiDB

    -   特定のシナリオで`OUTER JOIN`を`INNER JOIN`に変換する能力を強化する[＃49616](https://github.com/pingcap/tidb/issues/49616) @ [qw4990](https://github.com/qw4990)
    -   `force-init-stats` `true`に設定すると、TiDB は起動時にサービスを提供する前に統計情報の初期化が完了するのを待ちます。この設定により HTTP サーバーの起動がブロックされなくなり、ユーザーは[＃50854](https://github.com/pingcap/tidb/issues/50854) @ [ホーキングレイ](https://github.com/hawkingrei)で監視を継続できます。

-   TiKV

    -   TiKVは破損したSSTファイルの存在を検出すると、破損の具体的な理由をログに記録します[＃16308](https://github.com/tikv/tikv/issues/16308) @ [金星の上](https://github.com/overvenus)

-   PD

    -   バックアップクラスタが切断されたときにPDがクラスタステータスを自動更新する速度を向上[＃6883](https://github.com/tikv/pd/issues/6883) @ [ディスク](https://github.com/disksing)

-   TiFlash

    -   バックグラウンド GC タスクによる読み取りおよび書き込みタスクのレイテンシーへの影響を軽減[＃8650](https://github.com/pingcap/tiflash/issues/8650) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   ディスクパフォーマンスジッタによる読み取りレイテンシーへの影響を軽減[＃8583](https://github.com/pingcap/tiflash/issues/8583) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)

-   ツール

    -   バックアップと復元 (BR)

        -   データ復元中にデータベースをバッチで作成するサポート[＃50767](https://github.com/pingcap/tidb/issues/50767) @ [リーヴルス](https://github.com/Leavrth)
        -   大規模なデータセット[＃48301](https://github.com/pingcap/tidb/issues/48301) @ [リーヴルス](https://github.com/Leavrth)シナリオで`RESTORE`ステートメントのテーブル作成パフォーマンスを向上
        -   より効率的なアルゴリズム[＃50613](https://github.com/pingcap/tidb/issues/50613) @ [リーヴルス](https://github.com/Leavrth)を使用して、データ復元中に SST ファイルをマージする速度を改善します
        -   データ復元中に SST ファイルをバッチで取り込むことをサポート[＃16267](https://github.com/tikv/tikv/issues/16267) @ [3ポイントシュート](https://github.com/3pointer)
        -   ログバックアップ[＃51046](https://github.com/pingcap/tidb/issues/51046) @ [ユジュンセン](https://github.com/YuJuncen)中に、ログとメトリックのグローバルチェックポイントの進行に影響を与える最も遅いリージョンの情報を出力します。
        -   Google Cloud Storage（GCS）を外部storageとして使用する場合の古い互換性チェックを削除します[＃50533](https://github.com/pingcap/tidb/issues/50533) @ [ランス6716](https://github.com/lance6716)
        -   複数のログバックアップ切り捨てタスク（ `br log truncate` ）が同時に実行されるのを防ぐためのロックメカニズムを実装する[＃49414](https://github.com/pingcap/tidb/issues/49414) @ [ユジュンセン](https://github.com/YuJuncen)

    -   TiCDC

        -   ダウンストリームがKafkaの場合、トピック式では`schema`オプションとして指定でき、トピック名を直接指定できます[＃9763](https://github.com/pingcap/tiflow/issues/9763) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   サポート[変更フィードの下流同期ステータスの照会](https://docs.pingcap.com/tidb/v7.1/ticdc-open-api-v2#query-whether-a-specific-replication-task-is-completed) 、TiCDC が受信した上流データの変更が下流システムに完全に同期されているかどうかを判断するのに役立ちます[＃10289](https://github.com/pingcap/tiflow/issues/10289) @ [ホンユニャン](https://github.com/hongyunyan)
        -   TiDBダッシュボード[＃10263](https://github.com/pingcap/tiflow/issues/10263) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)でのTiCDCログの検索をサポート

    -   TiDB Lightning

        -   `ALTER TABLE` [＃50105](https://github.com/pingcap/tidb/issues/50105) @ [D3ハンター](https://github.com/D3Hunter)実行時にロック操作を削除することで、複数のテーブルをインポートするシナリオのパフォーマンスが向上します。

## バグ修正 {#bug-fixes}

-   TiDB

    -   `tidb_multi_statement_mode`モードが有効になっている場合、インデックス検索を使用する`DELETE`および`UPDATE`ステートメントでエラーが報告される可能性がある問題を修正しました[＃50012](https://github.com/pingcap/tidb/issues/50012) @ [接線](https://github.com/tangenta)
    -   CTEクエリが再試行プロセス[＃46522](https://github.com/pingcap/tidb/issues/46522) @ [天菜まお](https://github.com/tiancaiamao)中にエラー`type assertion for CTEStorageMap failed`を報告する可能性がある問題を修正しました
    -   Golang の暗黙的な変換アルゴリズム[＃49801](https://github.com/pingcap/tidb/issues/49801) @ [qw4990](https://github.com/qw4990)によって発生する統計情報の構築における過剰な統計エラーの問題を修正しました
    -   パーティションテーブル[＃48713](https://github.com/pingcap/tidb/issues/48713) @ [ホーキングレイ](https://github.com/hawkingrei)のグローバル統計の同時マージ中にエラーが返される可能性がある問題を修正しました。
    -   TiDB が`group by` [＃38756](https://github.com/pingcap/tidb/issues/38756) @ [ハイラスティン](https://github.com/Rustin170506)の定数値を誤って削除することによる間違ったクエリ結果の問題を修正しました
    -   `BIT`型の列が一部の関数の計算に関係する場合にデコード失敗によりクエリエラーが発生する可能性がある問題を修正しました[＃49566](https://github.com/pingcap/tidb/issues/49566) [＃50850](https://github.com/pingcap/tidb/issues/50850) [＃50855](https://github.com/pingcap/tidb/issues/50855) @ [ジフハウス](https://github.com/jiyfhust)
    -   複数レベルのネストされた`UNION`クエリの`LIMIT`無効になる可能性がある問題を修正しました[＃49874](https://github.com/pingcap/tidb/issues/49874) @ [定義2014](https://github.com/Defined2014)
    -   `AUTO_ID_CACHE=1` [＃50519](https://github.com/pingcap/tidb/issues/50519) @ [天菜まお](https://github.com/tiancaiamao)の自動インクリメント列を使用すると同時競合により自動インクリメント ID 割り当てでエラーが報告される問題を修正しました。
    -   クエリで`NATURAL JOIN` [＃32044](https://github.com/pingcap/tidb/issues/32044) @ [アイリンキッド](https://github.com/AilinKid)が使用される場合に発生する可能性のある`Column ... in from clause is ambiguous`エラーを修正します
    -   クエリがソートを強制するオプティマイザヒント（ `STREAM_AGG()`など）を使用し、その実行プランに`IndexMerge` [＃49605](https://github.com/pingcap/tidb/issues/49605) @ [アイリンキッド](https://github.com/AilinKid)が含まれている場合、強制ソートが無効になる可能性がある問題を修正しました。
    -   `STREAM_AGG()` CI [＃49902](https://github.com/pingcap/tidb/issues/49902) @ [wshwsh12](https://github.com/wshwsh12)を誤って処理したためにクエリ結果が正しくない問題を修正しました
    -   `HashJoin`演算子がディスク[＃50841](https://github.com/pingcap/tidb/issues/50841) @ [wshwsh12](https://github.com/wshwsh12)にスピルできない場合に発生する可能性のある goroutine リークの問題を修正しました。
    -   `REPLACE INTO`文[＃34325](https://github.com/pingcap/tidb/issues/34325) @ [ヤンケオ](https://github.com/YangKeao)でヒントが使用できない問題を修正
    -   `GROUP_CONCAT(ORDER BY)`構文を含むクエリを実行するとエラー[＃49986](https://github.com/pingcap/tidb/issues/49986) @ [アイリンキッド](https://github.com/AilinKid)が返される可能性がある問題を修正しました
    -   複数値インデックスを使用して空の JSON 配列にアクセスすると、誤った結果が返される可能性がある問題を修正しました[＃50125](https://github.com/pingcap/tidb/issues/50125) @ [ヤンケオ](https://github.com/YangKeao)
    -   CTEクエリのメモリ使用量が制限[＃50337](https://github.com/pingcap/tidb/issues/50337) @ [グオシャオゲ](https://github.com/guo-shaoge)を超えたときに発生するゴルーチンリークの問題を修正しました
    -   古いインターフェースを使用するとテーブル[＃49751](https://github.com/pingcap/tidb/issues/49751) @ [ホーキングレイ](https://github.com/hawkingrei)メタデータに不整合が生じる可能性がある問題を修正しました
    -   `ORDER BY`句で`UNIQUE`インデックス検索を実行するとエラー[＃49920](https://github.com/pingcap/tidb/issues/49920) @ [ジャッキーsp](https://github.com/jackysp)が発生する可能性がある問題を修正しました。
    -   共通ヒントが`UNION ALL`文[＃50068](https://github.com/pingcap/tidb/issues/50068) @ [ホーキングレイ](https://github.com/hawkingrei)で有効にならない問題を修正
    -   IndexHashJoin 演算子を含むクエリがメモリが`tidb_mem_quota_query` [＃49033](https://github.com/pingcap/tidb/issues/49033) @ [徐淮嶼](https://github.com/XuHuaiyu)を超えると停止する問題を修正しました
    -   `WITH RECURSIVE` CTE を含む`UPDATE`または`DELETE`ステートメントで誤った結果が生成される可能性がある問題を修正しました[＃48969](https://github.com/pingcap/tidb/issues/48969) @ [ウィノロス](https://github.com/winoros)
    -   ヒストグラムの境界に`NULL` [＃49823](https://github.com/pingcap/tidb/issues/49823) @ [アイリンキッド](https://github.com/AilinKid)が含まれている場合、ヒストグラム統計が読み取り可能な文字列に解析されない可能性がある問題を修正しました。
    -   クエリに Apply 演算子が含まれており、 `fatal error: concurrent map writes`エラーが[＃50347](https://github.com/pingcap/tidb/issues/50347) @ [シーライズ](https://github.com/SeaRise)で発生すると TiDB がpanic可能性がある問題を修正しました。
    -   集計関数をグループ計算に使用すると発生する可能性のある`Can't find column ...`エラーを修正[＃50926](https://github.com/pingcap/tidb/issues/50926) @ [qw4990](https://github.com/qw4990)
    -   定数伝播[＃49440](https://github.com/pingcap/tidb/issues/49440) @ [ウィノロス](https://github.com/winoros)で`ENUM`または`SET`型を処理するときに TiDB が間違ったクエリ結果を返す問題を修正しました
    -   依存関係のある 2 つの DDL タスクの完了時間が[＃49498](https://github.com/pingcap/tidb/issues/49498) @ [接線](https://github.com/tangenta)と誤って順序付けられる問題を修正しました。
    -   `tidb_enable_prepared_plan_cache`システム変数が有効になってから無効になった後、 `EXECUTE`ステートメントを使用して`PREPARE STMT`実行すると TiDB がpanicになる可能性がある問題を修正しました[＃49344](https://github.com/pingcap/tidb/issues/49344) @ [qw4990](https://github.com/qw4990)
    -   ネストされた`UNION`クエリ[＃49377](https://github.com/pingcap/tidb/issues/49377) @ [アイリンキッド](https://github.com/AilinKid)で`LIMIT`と`OPRDERBY`無効になる可能性がある問題を修正しました
    -   `LEADING`ヒントが`UNION ALL`ステートメント[＃50067](https://github.com/pingcap/tidb/issues/50067) @ [ホーキングレイ](https://github.com/hawkingrei)で有効にならない問題を修正しました
    -   `COM_STMT_EXECUTE`まで実行された`COMMIT`または`ROLLBACK`操作が、タイムアウトしたトランザクションを[＃49151](https://github.com/pingcap/tidb/issues/49151) @ [ジグアン](https://github.com/zyguan)で終了できない問題を修正しました。
    -   不正なオプティマイザヒントによって有効なヒントが無効になる可能性がある問題を修正[＃49308](https://github.com/pingcap/tidb/issues/49308) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   一部のタイムゾーン[＃49586](https://github.com/pingcap/tidb/issues/49586) @ [金星の上](https://github.com/overvenus)で夏時間が正しく表示されない問題を修正
    -   `PREPARE`メソッドを使用して`SELECT INTO OUTFILE`実行すると、エラー[＃49166](https://github.com/pingcap/tidb/issues/49166) @ [qw4990](https://github.com/qw4990)ではなく、誤って成功メッセージが返される問題を修正しました。
    -   PD [＃50152](https://github.com/pingcap/tidb/issues/50152) @ [ジムララ](https://github.com/zimulala)との相互作用の問題により、 `tiup cluster upgrade/start`使用してローリング アップグレードを実行すると TiDB がpanicになる可能性がある問題を修正しました。
    -   空のテーブル[＃49682](https://github.com/pingcap/tidb/issues/49682) @ [ジムララ](https://github.com/zimulala)にインデックスを追加したときに期待される最適化が有効にならない問題を修正しました
    -   多数のテーブルまたはパーティションが作成された場合に TiDB が OOM になる可能性がある問題を修正[＃50077](https://github.com/pingcap/tidb/issues/50077) @ [ジムララ](https://github.com/zimulala)
    -   ネットワークが不安定なときにインデックスを追加するとインデックスデータの不整合が発生する可能性がある問題を修正[＃49773](https://github.com/pingcap/tidb/issues/49773) @ [接線](https://github.com/tangenta)
    -   DDLジョブの実行順序を修正し、TiCDCが順序どおりに動作しないDDL [＃49498](https://github.com/pingcap/tidb/issues/49498) @ [接線](https://github.com/tangenta)を受信しないようにします。
    -   `tidb_server_memory_limit`変数が[＃48180](https://github.com/pingcap/tidb/issues/48180) @ [ホーキングレイ](https://github.com/hawkingrei)に変更された後、 `tidb_gogc_tuner_threshold`システム変数がそれに応じて調整されない問題を修正しました
    -   誤ったパーティションプルーニング[＃50082](https://github.com/pingcap/tidb/issues/50082) @ [定義2014](https://github.com/Defined2014)が原因で、範囲パーティションテーブルのクエリ結果が間違っている場合がある問題を修正しました。
    -   `CREATE TABLE`文に特定のパーティションまたは制約が含まれている場合に、テーブル名の変更などの DDL 操作が停止する問題を修正しました[＃50972](https://github.com/pingcap/tidb/issues/50972) @ [lcwangchao](https://github.com/lcwangchao)
    -   列のデフォルト値が削除されている場合、列のデフォルト値を取得するとエラーが返される問題を修正[＃50043](https://github.com/pingcap/tidb/issues/50043) [＃51324](https://github.com/pingcap/tidb/issues/51324) @ [crazycs520](https://github.com/crazycs520)
    -   Grafana の監視メトリック`tidb_statistics_auto_analyze_total`整数[＃51051](https://github.com/pingcap/tidb/issues/51051) @ [ホーキングレイ](https://github.com/hawkingrei)として表示されない問題を修正しました
    -   `auto analyze`パーティションテーブル[＃47594](https://github.com/pingcap/tidb/issues/47594) @ [ホーキングレイ](https://github.com/hawkingrei)を処理しているときに`tidb_merge_partition_stats_concurrency`変数が有効にならない問題を修正しました
    -   クエリにJOIN操作[＃42588](https://github.com/pingcap/tidb/issues/42588) @ [アイリンキッド](https://github.com/AilinKid)が含まれる場合に`index out of range`エラーが発生する可能性がある問題を修正しました
    -   TiFlash の遅延マテリアライゼーションが関連列[＃49241](https://github.com/pingcap/tidb/issues/49241) [＃51204](https://github.com/pingcap/tidb/issues/51204) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)を処理するときに間違った結果が返される可能性がある問題を修正しました
    -   テーブルにクラスター化インデックス[＃51372](https://github.com/pingcap/tidb/issues/51372) @ [グオシャオゲ](https://github.com/guo-shaoge)がある場合に並列`Apply`で誤った結果が生成される可能性がある問題を修正しました。

-   TiKV

    -   例外的な状況で休止状態の領域がすぐに復帰しない問題を修正[＃16368](https://github.com/tikv/tikv/issues/16368) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   ノードをオフラインにする前に、リージョン内のすべてのレプリカの最後のハートビート時間をチェックすることで、1 つのレプリカがオフラインになるとリージョン全体が使用できなくなる問題を修正しました[＃16465](https://github.com/tikv/tikv/issues/16465) @ [トニー・シュッキ](https://github.com/tonyxuqqi)
    -   Titan が有効な場合に RocksDB に保存されるテーブルプロパティが不正確になる可能性がある問題を修正[＃16319](https://github.com/tikv/tikv/issues/16319) @ [ヒック](https://github.com/hicqu)
    -   クラスターにTiFlashノード[＃16189](https://github.com/tikv/tikv/issues/16189) @ [新鮮な](https://github.com/frew)がある場合に`tikv-ctl compact-cluster`実行が失敗する問題を修正しました
    -   gRPC スレッドが`is_shutdown` [＃16236](https://github.com/tikv/tikv/issues/16236) @ [ピンギュ](https://github.com/pingyu)をチェックしているときに TiKV がpanic可能性がある問題を修正しました
    -   `DECIMAL`算術乗算切り捨て[＃16268](https://github.com/tikv/tikv/issues/16268) @ [ソロツグ](https://github.com/solotzg)を処理するときに TiDB と TiKV が矛盾した結果を生成する可能性がある問題を修正しました
    -   `cast_duration_as_time`誤った結果を返す可能性がある問題を修正[＃16211](https://github.com/tikv/tikv/issues/16211) @ [ゲンリチ](https://github.com/gengliqi)
    -   TiKVがブラジルとエジプトのタイムゾーンを誤って変換する問題を修正[＃16220](https://github.com/tikv/tikv/issues/16220) @ [金星の上](https://github.com/overvenus)
    -   JSON 整数の最大値`INT64`より大きく最大値`UINT64`より小さい値が TiKV によって`FLOAT64`として解析され、TiDB [＃16512](https://github.com/tikv/tikv/issues/16512) @ [ヤンケオ](https://github.com/YangKeao)との不整合が発生する問題を修正しました。

-   PD

    -   リソース グループ クライアントでスロットが完全に削除されず、割り当てられたトークンの数が指定された値[＃7346](https://github.com/tikv/pd/issues/7346) @ [グオシャオゲ](https://github.com/guo-shaoge)より少なくなる問題を修正しました。
    -   一部のTSOログにエラー原因[＃7496](https://github.com/tikv/pd/issues/7496) @ [キャビンフィーバーB](https://github.com/CabinfeverB)が出力されない問題を修正
    -   `BURSTABLE`有効になっているときにデフォルトのリソース グループに不要なトークンが蓄積される問題を修正[＃7206](https://github.com/tikv/pd/issues/7206) @ [キャビンフィーバーB](https://github.com/CabinfeverB)
    -   `evict-leader-scheduler`インターフェースが[＃7672](https://github.com/tikv/pd/issues/7672) @ [キャビンフィーバーB](https://github.com/CabinfeverB)で呼び出されたときに出力がない問題を修正しました
    -   `watch etcd`正しくオフになっていない場合に発生するメモリリークの問題を修正[＃7807](https://github.com/tikv/pd/issues/7807) @ [rleungx](https://github.com/rleungx)
    -   `MergeLabels`関数が[＃7535](https://github.com/tikv/pd/issues/7535) @ [lhy1024](https://github.com/lhy1024)で呼び出されたときにデータ競合が発生する問題を修正しました
    -   TLS が有効な場合に TiDB ダッシュボードが TiKV プロファイルを取得できない問題を修正[＃7561](https://github.com/tikv/pd/issues/7561) @ [コナー1996](https://github.com/Connor1996)
    -   レプリカ数が[＃7584](https://github.com/tikv/pd/issues/7584) @ [バッファフライ](https://github.com/bufferflies)要件を満たしていない場合に孤立ピアが削除される問題を修正しました
    -   データレプリケーション自動同期（DR自動同期）モードを採用しているクラスタで`available_stores`誤って計算される問題を修正[＃7221](https://github.com/tikv/pd/issues/7221) @ [ディスク](https://github.com/disksing)
    -   配置ルールの設定が複雑な場合、データレプリケーション自動同期（DR自動同期）モードを採用しているクラスタで`canSync`と`hasMajority`誤って計算される可能性がある問題を修正しました[＃7201](https://github.com/tikv/pd/issues/7201) @ [ディスク](https://github.com/disksing)
    -   データレプリケーション自動同期（DR自動同期）モード[＃7218](https://github.com/tikv/pd/issues/7218) @ [ディスク](https://github.com/disksing)を採用しているクラスターで、セカンダリAZがダウンしているときにプライマリAZがTiKVノードを追加できない問題を修正しました。
    -   リソース グループをバッチでクエリすると PD がpanic[＃7206](https://github.com/tikv/pd/issues/7206) @ [ノルーシュ](https://github.com/nolouch)になる可能性がある問題を修正しました
    -   `pd-ctl`使用してリーダーのないリージョンを照会すると、PD が[＃7630](https://github.com/tikv/pd/issues/7630) @ [rleungx](https://github.com/rleungx)でpanicになる可能性がある問題を修正しました。
    -   リーダースイッチ[＃7728](https://github.com/tikv/pd/issues/7728) @ [キャビンフィーバーB](https://github.com/CabinfeverB)後にPD監視項目`learner-peer-count`古い値を同期しない問題を修正
    -   PDが`systemd` [＃7628](https://github.com/tikv/pd/issues/7628) @ [バッファフライ](https://github.com/bufferflies)で起動したときにリソース制限を読み取れない問題を修正

-   TiFlash

    -   レプリカ移行[＃8323](https://github.com/pingcap/tiflash/issues/8323) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)中に PD とのネットワーク接続が不安定になり、 TiFlash がpanic可能性がある問題を修正しました
    -   `ENUM`値が0 [＃8311](https://github.com/pingcap/tiflash/issues/8311) @ [ソロツグ](https://github.com/solotzg)ときにTiFlashが`ENUM`誤って処理する問題を修正しました
    -   定数文字列パラメータ[＃8604](https://github.com/pingcap/tiflash/issues/8604) @ [ウィンドトーカー](https://github.com/windtalker)を含む`GREATEST`または`LEAST`関数で発生する可能性のある、ランダムに無効なメモリアクセスの問題を修正しました。
    -   `lowerUTF8`と`upperUTF8`関数で、大文字と小文字が異なるバイト[＃8484](https://github.com/pingcap/tiflash/issues/8484) @ [ゲンリチ](https://github.com/gengliqi)を占めることができない問題を修正しました。
    -   短いクエリが正常に実行され、過剰な情報ログ[＃8592](https://github.com/pingcap/tiflash/issues/8592) @ [ウィンドトーカー](https://github.com/windtalker)が出力される問題を修正しました。
    -   クエリ[＃8564](https://github.com/pingcap/tiflash/issues/8564) @ [ジンヘリン](https://github.com/JinheLin)の低速化によりメモリ使用量が大幅に増加する問題を修正
    -   `ALTER TABLE ... MODIFY COLUMN ... NOT NULL`実行した後にTiFlash がパニックを起こし、NULL 可能列が[＃8419](https://github.com/pingcap/tiflash/issues/8419) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)に非 NULL に変更される問題を修正しました。
    -   クエリを終了した後、 TiFlash上の多数のタスクが同時にキャンセルされると、同時データの競合によりTiFlashがクラッシュする問題を修正[＃7432](https://github.com/pingcap/tiflash/issues/7432) @ [シーライズ](https://github.com/SeaRise)
    -   リモート読み取り[＃8685](https://github.com/pingcap/tiflash/issues/8685) @ [zanmato1984](https://github.com/zanmato1984)中にTiFlashがクラッシュする可能性がある問題を修正
    -   結合に非等価条件[＃8791](https://github.com/pingcap/tiflash/issues/8791) @ [ウィンドトーカー](https://github.com/windtalker)が含まれている場合にTiFlash Anti Semi Join が誤った結果を返す可能性がある問題を修正しました

-   ツール

    -   バックアップと復元 (BR)

        -   ログバックアップタスクを停止すると TiDB がクラッシュする問題を修正[＃50839](https://github.com/pingcap/tidb/issues/50839) @ [ユジュンセン](https://github.com/YuJuncen)
        -   TiKVノード[＃50566](https://github.com/pingcap/tidb/issues/50566) @ [リーヴルス](https://github.com/Leavrth)にリーダーがいないためにデータ復元が遅くなる問題を修正
        -   同じノード[＃50445](https://github.com/pingcap/tidb/issues/50445) @ [3ポイントシュート](https://github.com/3pointer)で TiKV IP アドレスを変更した後にログ バックアップが停止する問題を修正しました
        -   S3 [＃49942](https://github.com/pingcap/tidb/issues/49942) @ [リーヴルス](https://github.com/Leavrth)からファイル コンテンツを読み取っているときにエラーが発生した場合にBR が再試行できない問題を修正しました
        -   古いバージョン[＃49466](https://github.com/pingcap/tidb/issues/49466) @ [3ポイントシュート](https://github.com/3pointer)のバックアップからデータを復元するときに`Unsupported collation`エラーが報告される問題を修正しました

    -   TiCDC

        -   アップストリームテーブル[＃10522](https://github.com/pingcap/tiflow/issues/10522) @ [スドジ](https://github.com/sdojjy)で`TRUNCATE PARTITION`が実行された後にチェンジフィードがエラーを報告する問題を修正しました
        -   極端なケースでチェンジフィード`resolved ts`が進まない問題を修正[＃10157](https://github.com/pingcap/tiflow/issues/10157) @ [スドジ](https://github.com/sdojjy)
        -   同期ポイントテーブルが誤って複製される可能性がある問題を修正[＃10576](https://github.com/pingcap/tiflow/issues/10576) @ [アズドンメン](https://github.com/asddongmen)
        -   `ignore-event`で`add table partition`イベントをフィルタリングするように構成した後、TiCDC が関連パーティションの他のタイプの DML 変更をダウンストリーム[＃10524](https://github.com/pingcap/tiflow/issues/10524) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)に複製しない問題を修正しました。
        -   storageシンク[＃10352](https://github.com/pingcap/tiflow/issues/10352) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)使用時に、storageサービスによって生成されたファイルシーケンス番号が正しく増加しない可能性がある問題を修正しました。
        -   複数のチェンジフィード[＃10430](https://github.com/pingcap/tiflow/issues/10430) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)を同時に作成すると TiCDC が`ErrChangeFeedAlreadyExists`エラーを返す問題を修正しました
        -   変更フィードを再開するときに`snapshot lost caused by GC`時間内に報告されず、変更フィードの`checkpoint-ts` TiDB [＃10463](https://github.com/pingcap/tiflow/issues/10463) @ [スドジ](https://github.com/sdojjy)の GC セーフポイントよりも小さい問題を修正しました。
        -   単一行データのデータ整合性検証が有効にされた後、タイムゾーンの不一致により TiCDC が`TIMESTAMP`種類のチェックサムの検証に失敗する問題を修正[＃10573](https://github.com/pingcap/tiflow/issues/10573) @ [3エースショーハンド](https://github.com/3AceShowHand)

    -   TiDB データ移行 (DM)

        -   タスク構成で間違ったbinlogイベントタイプがアップグレード失敗の原因となる問題を修正[＃10282](https://github.com/pingcap/tiflow/issues/10282) @ [GMHDBJD](https://github.com/GMHDBJD)
        -   `shard_row_id_bits`のテーブルでスキーマ トラッカーが[＃10308](https://github.com/pingcap/tiflow/issues/10308) @ [GMHDBJD](https://github.com/GMHDBJD)初期化に失敗する問題を修正しました。

    -   TiDB Lightning

        -   ファイルスキャン中に無効なシンボリックリンクファイルに遭遇すると、 TiDB Lightning がエラーを報告する問題を修正しました[＃49423](https://github.com/pingcap/tidb/issues/49423) @ [ランス6716](https://github.com/lance6716)
        -   `sql_mode` [＃50757](https://github.com/pingcap/tidb/issues/50757) @ [GMHDBJD](https://github.com/GMHDBJD)に`NO_ZERO_IN_DATE`含まれていない場合に、 TiDB Lightning が`0`を含む日付値を正しく解析できない問題を修正しました。
