---
title: TiDB 7.1.4 Release Notes
summary: TiDB 7.1.4は2024年3月11日にリリースされました。このバージョンでは、TiFlashのログ出力のオーバーヘッドが軽減され、TiKVのGCスレッドの数が設定されました。さらに、TiDBやTiKV、PD、TiFlashなどの改善点やバグの修正が含まれています。また、バックアップと復元 (BR)、TiCDC、TiDB Lightningなどのツールにも改善が加えられています。
---

# TiDB 7.1.4 リリースノート {#tidb-7-1-4-release-notes}

発売日：2024年3月11日

TiDB バージョン: 7.1.4

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup) | [インストールパッケージ](https://www.pingcap.com/download/?version=v7.1.4#version-list)

## 互換性の変更 {#compatibility-changes}

-   ログ出力のオーバーヘッドを軽減するために、 TiFlash はデフォルト値`logger.level`を`"debug"`から`"info"` [#8641](https://github.com/pingcap/tiflash/issues/8641) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)に変更します。
-   TiKV 構成項目[`gc.num-threads`](https://docs.pingcap.com/tidb/v6.5/tikv-configuration-file#num-threads-new-in-v658)を導入して、 `enable-compaction-filter`が`false` [#16101](https://github.com/tikv/tikv/issues/16101) @ [トニーシュクキ](https://github.com/tonyxuqqi)の場合の GC スレッドの数を設定します。

## 改善点 {#improvements}

-   TiDB

    -   特定のシナリオ[#49616](https://github.com/pingcap/tidb/issues/49616) @ [qw4990](https://github.com/qw4990)で`OUTER JOIN`を`INNER JOIN`に変換する機能を強化します。
    -   `force-init-stats`を`true`に設定すると、TiDB は統計の初期化が完了するまで待機してから、TiDB の起動時にサービスを提供します。この設定により HTTP サーバーの起動がブロックされなくなり、ユーザーは[#50854](https://github.com/pingcap/tidb/issues/50854) @ [ホーキングレイ](https://github.com/hawkingrei)の監視を継続できるようになりました。

-   TiKV

    -   TiKV は破損した SST ファイルの存在を検出すると、破損の具体的な理由をログに記録します[#16308](https://github.com/tikv/tikv/issues/16308) @ [オーバーヴィーナス](https://github.com/overvenus)

-   PD

    -   バックアップ クラスターが切断されたときにクラスター ステータスを自動的に更新する PD の速度が向上しました[#6883](https://github.com/tikv/pd/issues/6883) @ [ディスク化](https://github.com/disksing)

-   TiFlash

    -   バックグラウンド GC タスクが読み取りおよび書き込みタスクのレイテンシーに及ぼす影響を軽減します[#8650](https://github.com/pingcap/tiflash/issues/8650) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)
    -   読み取りレイテンシー[#8583](https://github.com/pingcap/tiflash/issues/8583) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)に対するディスク パフォーマンス ジッターの影響を軽減します。

-   ツール

    -   バックアップと復元 (BR)

        -   データ復元中のデータベースのバッチ作成をサポート[#50767](https://github.com/pingcap/tidb/issues/50767) @ [レヴルス](https://github.com/Leavrth)
        -   大規模なデータセット[#48301](https://github.com/pingcap/tidb/issues/48301) @ [レヴルス](https://github.com/Leavrth)を使用するシナリオでの`RESTORE`ステートメントのテーブル作成パフォーマンスを向上させます。
        -   より効率的なアルゴリズム[#50613](https://github.com/pingcap/tidb/issues/50613) @ [レヴルス](https://github.com/Leavrth)を使用して、データ復元中の SST ファイルのマージ速度を向上させます。
        -   データ復元中のバッチでの SST ファイルの取り込みをサポート[#16267](https://github.com/tikv/tikv/issues/16267) @ [3ポインター](https://github.com/3pointer)
        -   ログ バックアップ中のログとメトリックのグローバル チェックポイントの進行に影響を与える最も遅いリージョンの情報を出力します[#51046](https://github.com/pingcap/tidb/issues/51046) @ [ユジュンセン](https://github.com/YuJuncen)
        -   Google Cloud Storage (GCS) を外部storageとして使用する場合の古い互換性チェックを削除[#50533](https://github.com/pingcap/tidb/issues/50533) @ [ランス6716](https://github.com/lance6716)
        -   複数のログ バックアップ トランケーション タスク ( `br log truncate` ) が同時に実行されることを避けるために、ロック メカニズムを実装します[#49414](https://github.com/pingcap/tidb/issues/49414) @ [ユジュンセン](https://github.com/YuJuncen)

    -   TiCDC

        -   ダウンストリームが Kafka の場合、トピック式では`schema`をオプションにすることができ、トピック名の直接指定をサポートします[#9763](https://github.com/pingcap/tiflow/issues/9763) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   サポート[変更フィードのダウンストリーム同期ステータスのクエリ](https://docs.pingcap.com/tidb/v7.1/ticdc-open-api-v2#query-whether-a-specific-replication-task-is-completed)は、TiCDC が受信したアップストリーム データ変更がダウンストリーム システムに完全に同期されているかどうかを判断するのに役立ちます[#10289](https://github.com/pingcap/tiflow/issues/10289) @ [ホンユニャン](https://github.com/hongyunyan)
        -   TiDB ダッシュボード[#10263](https://github.com/pingcap/tiflow/issues/10263) @ [CharlesCheung96](https://github.com/CharlesCheung96)での TiCDC ログの検索のサポート

    -   TiDB Lightning

        -   `ALTER TABLE` [#50105](https://github.com/pingcap/tidb/issues/50105) @ [D3ハンター](https://github.com/D3Hunter)の実行時にロック操作を削除することで、複数のテーブルがインポートされるシナリオのパフォーマンスが向上します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   `tidb_multi_statement_mode`モードが有効になっている場合、インデックス ルックアップを使用する`DELETE`および`UPDATE`ステートメントでエラーが報告される可能性がある問題を修正[#50012](https://github.com/pingcap/tidb/issues/50012) @ [タンジェンタ](https://github.com/tangenta)
    -   CTE クエリが再試行プロセス[#46522](https://github.com/pingcap/tidb/issues/46522) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)中にエラー`type assertion for CTEStorageMap failed`を報告する可能性がある問題を修正します。
    -   Golang の暗黙的な変換アルゴリズム[#49801](https://github.com/pingcap/tidb/issues/49801) @ [qw4990](https://github.com/qw4990)によって引き起こされる統計構築時の過剰な統計エラーの問題を修正
    -   パーティションテーブル[#48713](https://github.com/pingcap/tidb/issues/48713) @ [ホーキングレイ](https://github.com/hawkingrei)のグローバル統計の同時マージ中にエラーが返される可能性がある問題を修正
    -   TiDB が`group by` [#38756](https://github.com/pingcap/tidb/issues/38756) @ [こんにちはラスティン](https://github.com/hi-rustin)の定数値を誤って削除するため、間違ったクエリ結果が発生する問題を修正しました。
    -   `BIT`型の列が一部の関数[#49566](https://github.com/pingcap/tidb/issues/49566) [#50850](https://github.com/pingcap/tidb/issues/50850) [#50855](https://github.com/pingcap/tidb/issues/50855) @ [ジフフスト](https://github.com/jiyfhust)の計算に関与する場合、デコード エラーによりクエリ エラーが発生する可能性がある問題を修正します。
    -   マルチレベルでネストされた`UNION`クエリの`LIMIT`無効になる可能性がある問題を修正[#49874](https://github.com/pingcap/tidb/issues/49874) @ [定義2014](https://github.com/Defined2014)
    -   `AUTO_ID_CACHE=1` [#50519](https://github.com/pingcap/tidb/issues/50519) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)の自動インクリメント列を使用すると、同時競合により自動インクリメント ID 割り当てでエラーが報告される問題を修正します。
    -   クエリで`NATURAL JOIN` [#32044](https://github.com/pingcap/tidb/issues/32044) @ [アイリンキッド](https://github.com/AilinKid)を使用するときに発生する可能性がある`Column ... in from clause is ambiguous`エラーを修正しました。
    -   クエリでソートを強制するオプティマイザ ヒント ( `STREAM_AGG()`など) が使用されており、その実行プランに`IndexMerge` [#49605](https://github.com/pingcap/tidb/issues/49605) @ [アイリンキッド](https://github.com/AilinKid)が含まれている場合、強制ソートが無効になる可能性がある問題を修正します。
    -   `STREAM_AGG()`の CI [#49902](https://github.com/pingcap/tidb/issues/49902) @ [wshwsh12](https://github.com/wshwsh12)の処理が間違っているため、クエリ結果が正しくない問題を修正します。
    -   `HashJoin`オペレーターがディスク[#50841](https://github.com/pingcap/tidb/issues/50841) @ [wshwsh12](https://github.com/wshwsh12)へのスピルに失敗した場合に発生する可能性があるゴルーチン リークの問題を修正します。
    -   `REPLACE INTO`ステートメント[#34325](https://github.com/pingcap/tidb/issues/34325) @ [ヤンケオ](https://github.com/YangKeao)でヒントが使用できない問題を修正
    -   `GROUP_CONCAT(ORDER BY)`構文を含むクエリを実行するとエラー[#49986](https://github.com/pingcap/tidb/issues/49986) @ [アイリンキッド](https://github.com/AilinKid)が返される可能性がある問題を修正します。
    -   複数値インデックスを使用して空の JSON 配列にアクセスすると、誤った結果[#50125](https://github.com/pingcap/tidb/issues/50125) @ [ヤンケオ](https://github.com/YangKeao)が返される可能性がある問題を修正します。
    -   CTE クエリのメモリ使用量が制限[#50337](https://github.com/pingcap/tidb/issues/50337) @ [グオシャオゲ](https://github.com/guo-shaoge)を超えたときに発生するゴルーチン リークの問題を修正しました。
    -   古いインターフェースを使用すると、テーブル[#49751](https://github.com/pingcap/tidb/issues/49751) @ [ホーキングレイ](https://github.com/hawkingrei)のメタデータが不整合になる可能性がある問題を修正
    -   `ORDER BY`句を使用して`UNIQUE`インデックス ルックアップを実行すると、エラー[#49920](https://github.com/pingcap/tidb/issues/49920) @ [ジャッキースプ](https://github.com/jackysp)が発生する可能性がある問題を修正します。
    -   `UNION ALL`ステートメント[#50068](https://github.com/pingcap/tidb/issues/50068) @ [ホーキングレイ](https://github.com/hawkingrei)で共通ヒントが有効にならない問題を修正
    -   メモリが`tidb_mem_quota_query` [#49033](https://github.com/pingcap/tidb/issues/49033) @ [徐淮嶼](https://github.com/XuHuaiyu)を超えると、IndexHashJoin 演算子を含むクエリがスタックする問題を修正します。
    -   `WITH RECURSIVE` CTE を含む`UPDATE`または`DELETE`ステートメントが誤った結果を生成する可能性がある問題を修正します[#48969](https://github.com/pingcap/tidb/issues/48969) @ [ウィノロス](https://github.com/winoros)
    -   ヒストグラムの境界に`NULL` [#49823](https://github.com/pingcap/tidb/issues/49823) @ [アイリンキッド](https://github.com/AilinKid)が含まれる場合、ヒストグラム統計が読み取り可能な文字列に解析されない可能性がある問題を修正します。
    -   panicに適用演算子が含まれており、 `fatal error: concurrent map writes`エラーが発生すると TiDB がパニックになる可能性がある問題を修正します[#50347](https://github.com/pingcap/tidb/issues/50347) @ [シーライズ](https://github.com/SeaRise)
    -   グループ計算に集計関数が使用されている場合に発生する可能性がある`Can't find column ...`エラーを修正[#50926](https://github.com/pingcap/tidb/issues/50926) @ [qw4990](https://github.com/qw4990)
    -   定数伝播[#49440](https://github.com/pingcap/tidb/issues/49440) @ [ウィノロス](https://github.com/winoros)で`ENUM`または`SET`型を処理すると、TiDB が間違ったクエリ結果を返す問題を修正
    -   依存関係のある 2 つの DDL タスクの完了時間が誤って順序付けされる問題を修正します[#49498](https://github.com/pingcap/tidb/issues/49498) @ [タンジェンタ](https://github.com/tangenta)
    -   `tidb_enable_prepared_plan_cache`システム変数が有効になってから無効になった後、 `EXECUTE`ステートメントを使用して`PREPARE STMT`実行すると、TiDB がパニックになる可能panicがある問題を修正します[#49344](https://github.com/pingcap/tidb/issues/49344) @ [qw4990](https://github.com/qw4990)
    -   ネストされた`UNION`クエリ[#49377](https://github.com/pingcap/tidb/issues/49377) @ [アイリンキッド](https://github.com/AilinKid)で`LIMIT`と`OPRDERBY`無効になる可能性がある問題を修正
    -   `LEADING`ヒントが`UNION ALL`のステートメント[#50067](https://github.com/pingcap/tidb/issues/50067) @ [ホーキングレイ](https://github.com/hawkingrei)で有効にならない問題を修正
    -   `COM_STMT_EXECUTE`を介して実行された`COMMIT`または`ROLLBACK`操作がタイムアウトしたトランザクションを終了できない問題を修正します[#49151](https://github.com/pingcap/tidb/issues/49151) @ [ジグアン](https://github.com/zyguan)
    -   不正なオプティマイザ ヒントにより有効なヒントが無効になる可能性がある問題を修正[#49308](https://github.com/pingcap/tidb/issues/49308) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   一部のタイムゾーン[#49586](https://github.com/pingcap/tidb/issues/49586) @ [オーバーヴィーナス](https://github.com/overvenus)でサマータイムが正しく表示されない問題を修正
    -   `PREPARE`メソッドを使用して`SELECT INTO OUTFILE`を実行すると、エラー[#49166](https://github.com/pingcap/tidb/issues/49166) @ [qw4990](https://github.com/qw4990)ではなく成功メッセージが誤って返される問題を修正します。
    -   PD [#50152](https://github.com/pingcap/tidb/issues/50152) @ [ジムララ](https://github.com/zimulala)との相互作用の問題により、 `tiup cluster upgrade/start`を使用してローリング アップグレードを実行すると TiDB がpanicになる可能性がある問題を修正
    -   空のテーブル[#49682](https://github.com/pingcap/tidb/issues/49682) @ [ジムララ](https://github.com/zimulala)にインデックスを追加すると、予期した最適化が有効にならない問題を修正します。
    -   多数のテーブルまたはパーティションが作成されると TiDB が OOM になる可能性がある問題を修正します[#50077](https://github.com/pingcap/tidb/issues/50077) @ [ジムララ](https://github.com/zimulala)
    -   ネットワークが不安定な場合にインデックスを追加するとインデックス データの不整合が発生する可能性がある問題を修正[#49773](https://github.com/pingcap/tidb/issues/49773) @ [タンジェンタ](https://github.com/tangenta)
    -   TiCDC が順序どおりでない DDL [#49498](https://github.com/pingcap/tidb/issues/49498) @ [タンジェンタ](https://github.com/tangenta)を受信しないように、DDL ジョブの実行順序を修正しました。
    -   `tidb_server_memory_limit`変数が変更された後、 `tidb_gogc_tuner_threshold`システム変数がそれに応じて調整されない問題を修正[#48180](https://github.com/pingcap/tidb/issues/48180) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   間違ったパーティション プルーニング[#50082](https://github.com/pingcap/tidb/issues/50082) @ [定義2014](https://github.com/Defined2014)により、場合によってはレンジパーティションテーブルのクエリ結果が正しくなくなる問題を修正
    -   `CREATE TABLE`ステートメントに特定のパーティションまたは制約が含まれている場合に、テーブルの名前変更などの DDL 操作が停止する問題を修正します[#50972](https://github.com/pingcap/tidb/issues/50972) @ [ルクワンチャオ](https://github.com/lcwangchao)
    -   列のデフォルト値が削除された場合、列のデフォルト値を取得するとエラーが返される問題を修正[#50043](https://github.com/pingcap/tidb/issues/50043) [#51324](https://github.com/pingcap/tidb/issues/51324) @ [クレイジークス520](https://github.com/crazycs520)
    -   Grafana の監視メトリクス`tidb_statistics_auto_analyze_total`整数[#51051](https://github.com/pingcap/tidb/issues/51051) @ [ホーキングレイ](https://github.com/hawkingrei)として表示されない問題を修正
    -   `auto analyze`がパーティションテーブル[#47594](https://github.com/pingcap/tidb/issues/47594) @ [ホーキングレイ](https://github.com/hawkingrei)を処理しているときに`tidb_merge_partition_stats_concurrency`変数が有効にならない問題を修正します。
    -   クエリに JOIN 操作[#42588](https://github.com/pingcap/tidb/issues/42588) @ [アイリンキッド](https://github.com/AilinKid)が含まれる場合に`index out of range`エラーが発生する可能性がある問題を修正します。
    -   TiFlash の遅延マテリアライゼーションが関連する列[#49241](https://github.com/pingcap/tidb/issues/49241) [#51204](https://github.com/pingcap/tidb/issues/51204) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)を処理するときに、間違った結果が返される可能性がある問題を修正

-   TiKV

    -   例外的な状況で休止状態のリージョンがすぐに目覚めない問題を修正[#16368](https://github.com/tikv/tikv/issues/16368) @ [リククスサシネーター](https://github.com/LykxSassinator)
    -   リージョンのすべてのレプリカの最後のハートビート時間をチェックすることで、1 つのレプリカがオフラインになるとリージョン全体が使用できなくなる問題を修正します[#16465](https://github.com/tikv/tikv/issues/16465) @ [トニーシュクキ](https://github.com/tonyxuqqi)
    -   Titan が有効になっている場合、RocksDB に保存されているテーブル プロパティが不正確になる可能性がある問題を修正[#16319](https://github.com/tikv/tikv/issues/16319) @ [ひっくり返る](https://github.com/hicqu)
    -   クラスターにTiFlashノード[#16189](https://github.com/tikv/tikv/issues/16189) @ [数人](https://github.com/frew)がある場合、 `tikv-ctl compact-cluster`の実行が失敗する問題を修正
    -   gRPC スレッドが`is_shutdown` [#16236](https://github.com/tikv/tikv/issues/16236) @ [ピンギュ](https://github.com/pingyu)をチェックしているときに TiKV がpanicになる可能性がある問題を修正
    -   TiDB と TiKV が`DECIMAL`算術乗算切り捨て[#16268](https://github.com/tikv/tikv/issues/16268) @ [ソロッツグ](https://github.com/solotzg)を処理するときに一貫性のない結果を生成する可能性がある問題を修正します。
    -   `cast_duration_as_time`が間違った結果[#16211](https://github.com/tikv/tikv/issues/16211) @ [ゲンリチ](https://github.com/gengliqi)を返す可能性がある問題を修正
    -   TiKV がブラジルとエジプトのタイムゾーンを誤って変換する問題を修正します[#16220](https://github.com/tikv/tikv/issues/16220) @ [オーバーヴィーナス](https://github.com/overvenus)
    -   最大値`INT64`より大きく、最大値`UINT64`未満の JSON 整数が TiKV によって`FLOAT64`として解析され、TiDB [#16512](https://github.com/tikv/tikv/issues/16512) @ [ヤンケオ](https://github.com/YangKeao)との不整合が生じる問題を修正します。

-   PD

    -   リソース グループ クライアントでスロットが完全に削除されず、割り当てられたトークンの数が指定された値[#7346](https://github.com/tikv/pd/issues/7346) @ [グオシャオゲ](https://github.com/guo-shaoge)未満になる問題を修正します。
    -   一部の TSO ログでエラー原因[#7496](https://github.com/tikv/pd/issues/7496) @ [キャビンフィーバーB](https://github.com/CabinfeverB)が出力されない問題を修正
    -   `BURSTABLE`を有効にした場合、デフォルトのリソース グループに不要なトークンが蓄積される問題を修正[#7206](https://github.com/tikv/pd/issues/7206) @ [キャビンフィーバーB](https://github.com/CabinfeverB)
    -   `evict-leader-scheduler`インターフェースが[#7672](https://github.com/tikv/pd/issues/7672) @ [キャビンフィーバーB](https://github.com/CabinfeverB)で呼び出されたときに出力がない問題を修正
    -   `watch etcd`が正しくオフになっていない場合に発生するメモリリークの問題を修正[#7807](https://github.com/tikv/pd/issues/7807) @ [ルルンクス](https://github.com/rleungx)
    -   `MergeLabels`関数を[#7535](https://github.com/tikv/pd/issues/7535) @ [lhy1024](https://github.com/lhy1024)で呼び出すとデータ競合が発生する問題を修正
    -   TLS が有効になっている場合に TiDB ダッシュボードが TiKV プロファイルを取得できない問題を修正[#7561](https://github.com/tikv/pd/issues/7561) @ [コナー1996](https://github.com/Connor1996)
    -   レプリカの数が要件[#7584](https://github.com/tikv/pd/issues/7584) @ [バッファフライ](https://github.com/bufferflies)を満たさない場合に孤立ピアが削除される問題を修正
    -   データ レプリケーション自動同期 (DR Auto-Sync) モード[#7221](https://github.com/tikv/pd/issues/7221) @ [ディスク化](https://github.com/disksing)を採用しているクラスターで`available_stores`が正しく計算されない問題を修正します。
    -   配置ルールの構成が複雑な場合、データ レプリケーション自動同期 (DR Auto-Sync) モードを採用しているクラスターで`canSync`と`hasMajority`が正しく計算されないことがある問題を修正[#7201](https://github.com/tikv/pd/issues/7201) @ [ディスク化](https://github.com/disksing)
    -   データ レプリケーション自動同期 (DR Auto-Sync) モード[#7218](https://github.com/tikv/pd/issues/7218) @ [ディスク化](https://github.com/disksing)を採用しているクラスターでセカンダリ AZ がダウンしている場合、プライマリ AZ が TiKV ノードを追加できない問題を修正します。
    -   バッチでリソース グループをクエリすると PD がpanic[#7206](https://github.com/tikv/pd/issues/7206) @ [ノールーシュ](https://github.com/nolouch)になる可能性がある問題を修正
    -   `pd-ctl`を使用してリーダーなしでリージョンをクエリすると、PD がpanic[#7630](https://github.com/tikv/pd/issues/7630) @ [ルルンクス](https://github.com/rleungx)になる可能性がある問題を修正します。
    -   PD監視項目`learner-peer-count`がリーダースイッチ[#7728](https://github.com/tikv/pd/issues/7728) @ [キャビンフィーバーB](https://github.com/CabinfeverB)後に古い値と同期しない問題を修正
    -   PD が`systemd` [#7628](https://github.com/tikv/pd/issues/7628) @ [バッファフライ](https://github.com/bufferflies)で起動されたときにリソース制限を読み取れない問題を修正

-   TiFlash

    -   レプリカ移行[#8323](https://github.com/pingcap/tiflash/issues/8323) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)中に PD とのネットワーク接続が不安定なためにTiFlash がpanicになる可能性がある問題を修正
    -   `ENUM`値が 0 [#8311](https://github.com/pingcap/tiflash/issues/8311) @ [ソロッツグ](https://github.com/solotzg)の場合にTiFlash が`ENUM`を誤って処理する問題を修正
    -   定数文字列パラメーター[#8604](https://github.com/pingcap/tiflash/issues/8604) @ [ウィンドトーカー](https://github.com/windtalker)を含む`GREATEST`または`LEAST`関数で発生する可能性があるランダムな無効なメモリアクセスの問題を修正します。
    -   `lowerUTF8`および`upperUTF8`関数で、大文字と小文字が異なる文字が異なるバイト[#8484](https://github.com/pingcap/tiflash/issues/8484) @ [ゲンリチ](https://github.com/gengliqi)を占めることができない問題を修正します。
    -   短いクエリが正常に実行されると過剰な情報ログ[#8592](https://github.com/pingcap/tiflash/issues/8592) @ [ウィンドトーカー](https://github.com/windtalker)が出力される問題を修正します。
    -   遅いクエリ[#8564](https://github.com/pingcap/tiflash/issues/8564) @ [ジンヘリン](https://github.com/JinheLin)によりメモリ使用量が大幅に増加する問題を修正
    -   Null 許容カラムを Null 非許容カラム[#8419](https://github.com/pingcap/tiflash/issues/8419) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)に変更する`ALTER TABLE ... MODIFY COLUMN ... NOT NULL`の実行後にTiFlashがパニックになる問題を修正
    -   クエリ終了後、 TiFlash上の多数のタスクが同時にキャンセルされると同時データの競合によりTiFlashがクラッシュする問題を修正[#7432](https://github.com/pingcap/tiflash/issues/7432) @ [シーライズ](https://github.com/SeaRise)
    -   リモート読み取り[#8685](https://github.com/pingcap/tiflash/issues/8685) @ [ザンマト1984](https://github.com/zanmato1984)中にTiFlash がクラッシュする可能性がある問題を修正
    -   結合に等価でない条件[#8791](https://github.com/pingcap/tiflash/issues/8791) @ [ウィンドトーカー](https://github.com/windtalker)が含まれている場合、 TiFlash Anti Semi Join が誤った結果を返す可能性がある問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   ログ バックアップ タスクを停止すると TiDB がクラッシュする問題を修正します[#50839](https://github.com/pingcap/tidb/issues/50839) @ [ユジュンセン](https://github.com/YuJuncen)
        -   TiKV ノード[#50566](https://github.com/pingcap/tidb/issues/50566) @ [レヴルス](https://github.com/Leavrth)にリーダーが存在しないためにデータの復元が遅くなる問題を修正
        -   同じノード[#50445](https://github.com/pingcap/tidb/issues/50445) @ [3ポインター](https://github.com/3pointer)で TiKV IP アドレスを変更した後にログのバックアップが停止する問題を修正
        -   S3 [#49942](https://github.com/pingcap/tidb/issues/49942) @ [レヴルス](https://github.com/Leavrth)からファイルの内容を読み取るときにエラーが発生した場合にBR が再試行できない問題を修正
        -   古いバージョン[#49466](https://github.com/pingcap/tidb/issues/49466) @ [3ポインター](https://github.com/3pointer)のバックアップからデータを復元すると`Unsupported collation`エラーが報告される問題を修正します。

    -   TiCDC

        -   上流テーブル[#10522](https://github.com/pingcap/tiflow/issues/10522) @ [スドジ](https://github.com/sdojjy)で`TRUNCATE PARTITION`が実行された後、変更フィードがエラーを報告する問題を修正します。
        -   極端なケース[#10157](https://github.com/pingcap/tiflow/issues/10157) @ [スドジ](https://github.com/sdojjy)でチェンジフィード`resolved ts`が進まない問題を修正
        -   同期ポイント テーブルが誤って複製される可能性がある問題を修正[#10576](https://github.com/pingcap/tiflow/issues/10576) @ [東門](https://github.com/asddongmen)
        -   `ignore-event`で構成された`add table partition`イベントをフィルタリングした後、TiCDC が関連パーティションの他のタイプの DML 変更をダウンストリーム[#10524](https://github.com/pingcap/tiflow/issues/10524) @ [CharlesCheung96](https://github.com/CharlesCheung96)にレプリケートしない問題を修正します。
        -   storageシンク[#10352](https://github.com/pingcap/tiflow/issues/10352) @ [CharlesCheung96](https://github.com/CharlesCheung96)を使用する場合、storageサービスによって生成されたファイル シーケンス番号が正しく増加しないことがある問題を修正します。
        -   複数の変更フィード[#10430](https://github.com/pingcap/tiflow/issues/10430) @ [CharlesCheung96](https://github.com/CharlesCheung96)を同時に作成すると TiCDC が`ErrChangeFeedAlreadyExists`エラーを返す問題を修正
        -   チェンジフィードを再開するときに`snapshot lost caused by GC`が時間内に報告されず、チェンジフィードの`checkpoint-ts`が TiDB [#10463](https://github.com/pingcap/tiflow/issues/10463) @ [スドジ](https://github.com/sdojjy)の GC セーフポイントより小さいという問題を修正します。
        -   単一行データのデータ整合性検証が有効になった後、タイム ゾーンの不一致により TiCDC が`TIMESTAMP`タイプのチェックサムの検証に失敗する問題を修正[#10573](https://github.com/pingcap/tiflow/issues/10573) @ [3エースショーハンド](https://github.com/3AceShowHand)

    -   TiDB データ移行 (DM)

        -   タスク構成内の間違ったbinlogイベント タイプによりアップグレードが失敗する問題を修正します[#10282](https://github.com/pingcap/tiflow/issues/10282) @ [GMHDBJD](https://github.com/GMHDBJD)
        -   `shard_row_id_bits`を持つテーブルによりスキーマ トラッカーが[#10308](https://github.com/pingcap/tiflow/issues/10308) @ [GMHDBJD](https://github.com/GMHDBJD)の初期化に失敗する問題を修正します。

    -   TiDB Lightning

        -   ファイル スキャン中に無効なシンボリック リンク ファイルが見つかったときにTiDB Lightning がエラーを報告する問題を修正[#49423](https://github.com/pingcap/tidb/issues/49423) @ [ランス6716](https://github.com/lance6716)
        -   `sql_mode` [#50757](https://github.com/pingcap/tidb/issues/50757) @ [GMHDBJD](https://github.com/GMHDBJD)に`NO_ZERO_IN_DATE`が含まれていない場合、 TiDB Lightning が`0`含む日付値を正しく解析できない問題を修正
