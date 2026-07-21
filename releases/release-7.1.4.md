---
title: TiDB 7.1.4 Release Notes
summary: TiDB 7.1.4 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 7.1.4 リリースノート {#tidb-7-1-4-release-notes}

発売日：2024年3月11日

TiDBバージョン: 7.1.4

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   ログ印刷のオーバーヘッドを減らすために、 TiFlashはデフォルト値の`logger.level` `"debug"`から`"info"` に変更します。 [＃8641](https://github.com/pingcap/tiflash/issues/8641) @ [JaySon-Huang](https://github.com/JaySon-Huang)
-   TiKV構成項目[`gc.num-threads`](https://docs.pingcap.com/tidb/v6.5/tikv-configuration-file#num-threads-new-in-v658)を導入して、 `enable-compaction-filter`が`false` の場合のGCスレッド数を設定します。 [＃16101](https://github.com/tikv/tikv/issues/16101) @ [tonyxuqqi](https://github.com/tonyxuqqi)

## 改善点 {#improvements}

-   TiDB

    -   特定のシナリオで`OUTER JOIN`を`INNER JOIN`に変換する能力を強化する[＃49616](https://github.com/pingcap/tidb/issues/49616) @ [qw4990](https://github.com/qw4990)
    -   `force-init-stats` `true`に設定すると、TiDB は起動時にサービスを提供する前に統計情報の初期化が完了するのを待ちます。この設定により HTTP サーバーの起動がブロックされなくなり、ユーザーはで監視を継続できます。 [＃50854](https://github.com/pingcap/tidb/issues/50854) @ [hawkingrei](https://github.com/hawkingrei)

-   TiKV

    -   TiKVは破損したSSTファイルの存在を検出すると、破損の具体的な理由をログに記録します[＃16308](https://github.com/tikv/tikv/issues/16308) @ [overvenus](https://github.com/overvenus)

-   PD

    -   バックアップ クラスタが切断されたときに PD がクラスタ ステータスを自動更新する速度を向上[＃6883](https://github.com/tikv/pd/issues/6883) @ [disksing](https://github.com/disksing)

-   TiFlash

    -   バックグラウンド GC タスクによる読み取りおよび書き込みタスクのレイテンシーへの影響を軽減します[＃8650](https://github.com/pingcap/tiflash/issues/8650) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   ディスクパフォ​​ーマンスジッターによる読み取りレイテンシーへの影響を軽減[＃8583](https://github.com/pingcap/tiflash/issues/8583) @ [JaySon-Huang](https://github.com/JaySon-Huang)

-   ツール

    -   Backup & Restore (BR)

        -   データ復元中にデータベースをバッチで作成するサポート[＃50767](https://github.com/pingcap/tidb/issues/50767) @ [Leavrth](https://github.com/Leavrth)
        -   大規模なデータセットのシナリオで`RESTORE`ステートメントのテーブル作成パフォーマンスを向上 [＃48301](https://github.com/pingcap/tidb/issues/48301) @ [Leavrth](https://github.com/Leavrth)
        -   より効率的なアルゴリズムを使用して、データ復元中に SST ファイルをマージする速度を改善します [＃50613](https://github.com/pingcap/tidb/issues/50613) @ [Leavrth](https://github.com/Leavrth)
        -   データ復元中に SST ファイルをバッチで取り込むことをサポート[＃16267](https://github.com/tikv/tikv/issues/16267) @ [3pointer](https://github.com/3pointer)
        -   ログバックアップ中に、ログとメトリックのグローバルチェックポイントの進行に影響を与える最も遅いリージョンの情報を出力します。 [＃51046](https://github.com/pingcap/tidb/issues/51046) @ [YuJuncen](https://github.com/YuJuncen)
        -   Google Cloud Storage（GCS）を外部ストレージとして使用する場合の古い互換性チェックを削除します[＃50533](https://github.com/pingcap/tidb/issues/50533) @ [lance6716](https://github.com/lance6716)
        -   複数のログバックアップ切り捨てタスク（ `br log truncate` ）が同時に実行されるのを防ぐためのロックメカニズムを実装する[＃49414](https://github.com/pingcap/tidb/issues/49414) @ [YuJuncen](https://github.com/YuJuncen)

    -   TiCDC

        -   ダウンストリームがKafkaの場合、トピック式は`schema`オプションとして許可し、トピック名を直接指定することをサポートします[＃9763](https://github.com/pingcap/tiflow/issues/9763) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   サポート[チェンジフィードの下流同期ステータスの照会](https://docs.pingcap.com/tidb/v7.1/ticdc-open-api-v2#query-whether-a-specific-replication-task-is-completed)は、TiCDC が受信した上流データの変更が下流システムに完全に同期されているかどうかを判断するのに役立ちます[＃10289](https://github.com/pingcap/tiflow/issues/10289) @ [hongyunyan](https://github.com/hongyunyan)
        -   TiDB DashboardでのTiCDCログの検索をサポート [＃10263](https://github.com/pingcap/tiflow/issues/10263) @ [CharlesCheung96](https://github.com/CharlesCheung96)

    -   TiDB Lightning

        -   `ALTER TABLE` 実行時にロック操作を削除することで、複数のテーブルをインポートするシナリオのパフォーマンスが向上します。 [＃50105](https://github.com/pingcap/tidb/issues/50105) @ [D3Hunter](https://github.com/D3Hunter)

## バグ修正 {#bug-fixes}

-   TiDB

    -   `tidb_multi_statement_mode`モードが有効になっている場合、インデックス検索を使用する`DELETE`および`UPDATE`ステートメントでエラーが報告される可能性がある問題を修正しました[＃50012](https://github.com/pingcap/tidb/issues/50012) @ [tangenta](https://github.com/tangenta)
    -   CTEクエリが再試行プロセス中にエラー`type assertion for CTEStorageMap failed`を報告する可能性がある問題を修正しました [＃46522](https://github.com/pingcap/tidb/issues/46522) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   Golang の暗黙的な変換アルゴリズムによって発生する統計情報の構築における過剰な統計エラーの問題を修正しました [＃49801](https://github.com/pingcap/tidb/issues/49801) @ [qw4990](https://github.com/qw4990)
    -   パーティションテーブルのグローバル統計の同時マージ中にエラーが返される可能性がある問題を修正しました。 [＃48713](https://github.com/pingcap/tidb/issues/48713) @ [hawkingrei](https://github.com/hawkingrei)
    -   TiDB が`group by` の定数値を誤って削除することによる間違ったクエリ結果の問題を修正しました [＃38756](https://github.com/pingcap/tidb/issues/38756) @ [Rustin170506](https://github.com/Rustin170506)
    -   `BIT`型の列が一部の関数の計算に関係する場合にデコード失敗によりクエリエラーが発生する可能性がある問題を修正しました[＃49566](https://github.com/pingcap/tidb/issues/49566) [＃50850](https://github.com/pingcap/tidb/issues/50850) [＃50855](https://github.com/pingcap/tidb/issues/50855) @ [jiyfhust](https://github.com/jiyfhust)
    -   複数レベルのネストされた`UNION`クエリの`LIMIT`無効になる可能性がある問題を修正しました[＃49874](https://github.com/pingcap/tidb/issues/49874) @ [Defined2014](https://github.com/Defined2014)
    -   `AUTO_ID_CACHE=1` のAUTO_INCREMENT列を使用すると同時競合によりAUTO_INCREMENT ID 割り当てでエラーが報告される問題を修正しました。 [＃50519](https://github.com/pingcap/tidb/issues/50519) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   クエリで`NATURAL JOIN` が使用される場合に発生する可能性のある`Column ... in from clause is ambiguous`エラーを修正します [＃32044](https://github.com/pingcap/tidb/issues/32044) @ [AilinKid](https://github.com/AilinKid)
    -   クエリがソートを強制するオプティマイザヒント（ `STREAM_AGG()`など）を使用し、その実行プランに`IndexMerge` が含まれている場合、強制ソートが無効になる可能性がある問題を修正しました。 [＃49605](https://github.com/pingcap/tidb/issues/49605) @ [AilinKid](https://github.com/AilinKid)
    -   `STREAM_AGG()` CI を誤って処理したためにクエリ結果が正しくない問題を修正しました [＃49902](https://github.com/pingcap/tidb/issues/49902) @ [wshwsh12](https://github.com/wshwsh12)
    -   `HashJoin`演算子がディスクにスピルできない場合に発生する可能性のある goroutine リークの問題を修正しました。 [＃50841](https://github.com/pingcap/tidb/issues/50841) @ [wshwsh12](https://github.com/wshwsh12)
    -   `REPLACE INTO`文でヒントが使用できない問題を修正 [＃34325](https://github.com/pingcap/tidb/issues/34325) @ [YangKeao](https://github.com/YangKeao)
    -   `GROUP_CONCAT(ORDER BY)`構文を含むクエリを実行するとエラーが返される可能性がある問題を修正しました [＃49986](https://github.com/pingcap/tidb/issues/49986) @ [AilinKid](https://github.com/AilinKid)
    -   多値インデックスを使用して空の JSON 配列にアクセスすると、誤った結果が返される可能性がある問題を修正しました[＃50125](https://github.com/pingcap/tidb/issues/50125) @ [YangKeao](https://github.com/YangKeao)
    -   CTEクエリのメモリ使用量が制限を超えたときに発生するgoroutineリークの問題を修正しました [＃50337](https://github.com/pingcap/tidb/issues/50337) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   古いインターフェースを使用するとテーブルのメタデータに不整合が発生する可能性がある問題を修正しました。 [＃49751](https://github.com/pingcap/tidb/issues/49751) @ [hawkingrei](https://github.com/hawkingrei)
    -   `ORDER BY`句で`UNIQUE`インデックス検索を実行するとエラーが発生する可能性がある問題を修正しました [＃49920](https://github.com/pingcap/tidb/issues/49920) @ [jackysp](https://github.com/jackysp)
    -   共通ヒントが`UNION ALL`文で有効にならない問題を修正 [＃50068](https://github.com/pingcap/tidb/issues/50068) @ [hawkingrei](https://github.com/hawkingrei)
    -   メモリが`tidb_mem_quota_query` を超えると IndexHashJoin 演算子を含むクエリが停止する問題を修正しました [＃49033](https://github.com/pingcap/tidb/issues/49033) @ [XuHuaiyu](https://github.com/XuHuaiyu)
    -   `WITH RECURSIVE` CTE を含む`UPDATE`または`DELETE`ステートメントで誤った結果が生成される可能性がある問題を修正しました[＃48969](https://github.com/pingcap/tidb/issues/48969) @ [winoros](https://github.com/winoros)
    -   ヒストグラムの境界に`NULL` が含まれている場合、ヒストグラム統計が読み取り可能な文字列に解析されない可能性がある問題を修正しました。 [＃49823](https://github.com/pingcap/tidb/issues/49823) @ [AilinKid](https://github.com/AilinKid)
    -   クエリに Apply 演算子が含まれており、 `fatal error: concurrent map writes`エラーが発生すると TiDB がpanicになる可能性がある問題を修正しました。 [＃50347](https://github.com/pingcap/tidb/issues/50347) @ [SeaRise](https://github.com/SeaRise)
    -   集計関数をグループ計算に使用すると発生する可能性のある`Can't find column ...`エラーを修正[＃50926](https://github.com/pingcap/tidb/issues/50926) @ [qw4990](https://github.com/qw4990)
    -   定数伝播で`ENUM`または`SET`型を処理するときに TiDB が間違ったクエリ結果を返す問題を修正しました [＃49440](https://github.com/pingcap/tidb/issues/49440) @ [winoros](https://github.com/winoros)
    -   依存関係のある 2 つの DDL タスクの完了時間がと誤って順序付けられる問題を修正しました。 [＃49498](https://github.com/pingcap/tidb/issues/49498) @ [tangenta](https://github.com/tangenta)
    -   `tidb_enable_prepared_plan_cache`システム変数が有効になってから無効になった後に`EXECUTE`ステートメントを使用して`PREPARE STMT`を実行すると、TiDB がpanicになる可能性がある問題を修正しました[＃49344](https://github.com/pingcap/tidb/issues/49344) @ [qw4990](https://github.com/qw4990)
    -   ネストされた`UNION`のクエリで`LIMIT`と`OPRDERBY`無効になる可能性がある問題を修正しました [＃49377](https://github.com/pingcap/tidb/issues/49377) @ [AilinKid](https://github.com/AilinKid)
    -   `LEADING`ヒントが`UNION ALL`ステートメントで有効にならない問題を修正しました [＃50067](https://github.com/pingcap/tidb/issues/50067) @ [hawkingrei](https://github.com/hawkingrei)
    -   `COM_STMT_EXECUTE`まで実行された`COMMIT`または`ROLLBACK`操作が、タイムアウトしたトランザクションを終了できない問題を修正しました。 [＃49151](https://github.com/pingcap/tidb/issues/49151) @ [zyguan](https://github.com/zyguan)
    -   無効なオプティマイザヒントによって有効なヒントが無効になる可能性がある問題を修正[＃49308](https://github.com/pingcap/tidb/issues/49308) @ [hawkingrei](https://github.com/hawkingrei)
    -   一部のタイムゾーンで夏時間が正しく表示されない問題を修正 [＃49586](https://github.com/pingcap/tidb/issues/49586) @ [overvenus](https://github.com/overvenus)
    -   `PREPARE`メソッドを使用して`SELECT INTO OUTFILE`を実行すると、エラーではなく、誤って成功メッセージが返される問題を修正しました。 [＃49166](https://github.com/pingcap/tidb/issues/49166) @ [qw4990](https://github.com/qw4990)
    -   PD との相互作用の問題により、 `tiup cluster upgrade/start`を使用してローリング アップグレードを実行すると TiDB がpanicになる可能性がある問題を修正しました。 [＃50152](https://github.com/pingcap/tidb/issues/50152) @ [zimulala](https://github.com/zimulala)
    -   空のテーブルにインデックスを追加したときに期待される最適化が有効にならない問題を修正しました [＃49682](https://github.com/pingcap/tidb/issues/49682) @ [zimulala](https://github.com/zimulala)
    -   多数のテーブルまたはパーティションが作成された場合に TiDB が OOM になる可能性がある問題を修正[＃50077](https://github.com/pingcap/tidb/issues/50077) @ [zimulala](https://github.com/zimulala)
    -   ネットワークが不安定な場合にインデックスを追加するとインデックスデータの不整合が発生する可能性がある問題を修正[＃49773](https://github.com/pingcap/tidb/issues/49773) @ [tangenta](https://github.com/tangenta)
    -   DDLジョブの実行順序を修正して、TiCDCが順序どおりに動作しないDDL を受信しないようにします。 [＃49498](https://github.com/pingcap/tidb/issues/49498) @ [tangenta](https://github.com/tangenta)
    -   `tidb_server_memory_limit`変数が変更された後、 `tidb_gogc_tuner_threshold`システム変数がそれに応じて調整されない問題を修正しました [＃48180](https://github.com/pingcap/tidb/issues/48180) @ [hawkingrei](https://github.com/hawkingrei)
    -   誤ったパーティションプルーニングが原因で、範囲パーティションテーブルのクエリ結果が間違っている場合がある問題を修正しました。 [＃50082](https://github.com/pingcap/tidb/issues/50082) @ [Defined2014](https://github.com/Defined2014)
    -   `CREATE TABLE`文に特定のパーティションまたは制約が含まれている場合に、テーブル名の変更などの DDL 操作が停止する問題を修正しました[＃50972](https://github.com/pingcap/tidb/issues/50972) @ [lcwangchao](https://github.com/lcwangchao)
    -   列のデフォルト値が削除されている場合に列のデフォルト値を取得するとエラーが返される問題を修正[＃50043](https://github.com/pingcap/tidb/issues/50043) [＃51324](https://github.com/pingcap/tidb/issues/51324) @ [crazycs520](https://github.com/crazycs520)
    -   Grafana の監視メトリック`tidb_statistics_auto_analyze_total`が整数として表示されない問題を修正しました [＃51051](https://github.com/pingcap/tidb/issues/51051) @ [hawkingrei](https://github.com/hawkingrei)
    -   `auto analyze`パーティションテーブルを処理しているときに`tidb_merge_partition_stats_concurrency`変数が有効にならない問題を修正しました [＃47594](https://github.com/pingcap/tidb/issues/47594) @ [hawkingrei](https://github.com/hawkingrei)
    -   クエリにJOIN操作が含まれる場合に`index out of range`エラーが発生する可能性がある問題を修正しました [＃42588](https://github.com/pingcap/tidb/issues/42588) @ [AilinKid](https://github.com/AilinKid)
    -   TiFlash の遅延マテリアライゼーションが関連列 を処理するときに間違った結果が返される可能性がある問題を修正しました [＃51204](https://github.com/pingcap/tidb/issues/51204) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger) [＃49241](https://github.com/pingcap/tidb/issues/49241)
    -   テーブルにクラスター化インデックスがある場合に並列`Apply`で誤った結果が生成される可能性がある問題を修正しました。 [＃51372](https://github.com/pingcap/tidb/issues/51372) @ [guo-shaoge](https://github.com/guo-shaoge)

-   TiKV

    -   例外的な状況で休止状態の領域がすぐに起動しない問題を修正[＃16368](https://github.com/tikv/tikv/issues/16368) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   ノードをオフラインにする前に、リージョン内のすべてのレプリカの最後のハートビート時間をチェックすることで、1 つのレプリカがオフラインになるとリージョン全体が使用できなくなる問題を修正しました[＃16465](https://github.com/tikv/tikv/issues/16465) @ [tonyxuqqi](https://github.com/tonyxuqqi)
    -   Titan が有効になっているときに RocksDB に保存されるテーブルプロパティが不正確になる可能性がある問題を修正[＃16319](https://github.com/tikv/tikv/issues/16319) @ [hicqu](https://github.com/hicqu)
    -   クラスターにTiFlashノードがある場合に`tikv-ctl compact-cluster`実行が失敗する問題を修正しました [＃16189](https://github.com/tikv/tikv/issues/16189) @ [frew](https://github.com/frew)
    -   gRPC スレッドが`is_shutdown` をチェックしているときに TiKV がpanicする可能性がある問題を修正しました [＃16236](https://github.com/tikv/tikv/issues/16236) @ [pingyu](https://github.com/pingyu)
    -   `DECIMAL`算術乗算切り捨てを処理するときに TiDB と TiKV が矛盾した結果を生成する可能性がある問題を修正しました [＃16268](https://github.com/tikv/tikv/issues/16268) @ [solotzg](https://github.com/solotzg)
    -   `cast_duration_as_time`誤った結果を返す可能性がある問題を修正[＃16211](https://github.com/tikv/tikv/issues/16211) @ [gengliqi](https://github.com/gengliqi)
    -   TiKVがブラジルとエジプトのタイムゾーンを誤って変換する問題を修正[＃16220](https://github.com/tikv/tikv/issues/16220) @ [overvenus](https://github.com/overvenus)
    -   JSON の整数が最大値`INT64`より大きく最大値`UINT64`より小さい場合、TiKV によって`FLOAT64`として解析され、TiDB との不整合が発生する問題を修正しました。 [＃16512](https://github.com/tikv/tikv/issues/16512) @ [YangKeao](https://github.com/YangKeao)

-   PD

    -   リソース グループ クライアントでスロットが完全に削除されず、割り当てられたトークンの数が指定された値より少なくなる問題を修正しました。 [＃7346](https://github.com/tikv/pd/issues/7346) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   一部のTSOログでエラー原因が出力されない問題を修正しました [＃7496](https://github.com/tikv/pd/issues/7496) @ [CabinfeverB](https://github.com/CabinfeverB)
    -   `BURSTABLE`有効になっているときにデフォルトのリソース グループに不要なトークンが蓄積される問題を修正[＃7206](https://github.com/tikv/pd/issues/7206) @ [CabinfeverB](https://github.com/CabinfeverB)
    -   `evict-leader-scheduler`インターフェースが呼び出されたときに出力がない問題を修正しました [＃7672](https://github.com/tikv/pd/issues/7672) @ [CabinfeverB](https://github.com/CabinfeverB)
    -   `watch etcd`正しくオフになっていない場合に発生するメモリリークの問題を修正[＃7807](https://github.com/tikv/pd/issues/7807) @ [rleungx](https://github.com/rleungx)
    -   `MergeLabels`関数が呼び出されたときにデータ競合が発生する問題を修正しました [＃7535](https://github.com/tikv/pd/issues/7535) @ [lhy1024](https://github.com/lhy1024)
    -   TLS が有効な場合に TiDB Dashboardが TiKV プロファイルを取得できない問題を修正[＃7561](https://github.com/tikv/pd/issues/7561) @ [Connor1996](https://github.com/Connor1996)
    -   レプリカ数が要件を満たしていない場合に孤立ピアが削除される問題を修正しました [＃7584](https://github.com/tikv/pd/issues/7584) @ [bufferflies](https://github.com/bufferflies)
    -   データレプリケーション自動同期（DR自動同期）モードを採用しているクラスタで`available_stores`誤って計算される問題を修正[＃7221](https://github.com/tikv/pd/issues/7221) @ [disksing](https://github.com/disksing)
    -   配置ルールの設定が複雑な場合、データレプリケーション自動同期（DR自動同期）モードを採用しているクラスタで`canSync`と`hasMajority`誤って計算される可能性がある問題を修正しました[＃7201](https://github.com/tikv/pd/issues/7201) @ [disksing](https://github.com/disksing)
    -   データレプリケーション自動同期（DR自動同期）モードを採用しているクラスターで、セカンダリAZがダウンしているときにプライマリAZがTiKVノードを追加できない問題を修正しました。 [＃7218](https://github.com/tikv/pd/issues/7218) @ [disksing](https://github.com/disksing)
    -   リソース グループをバッチでクエリすると PD がpanicになる可能性がある問題を修正しました [＃7206](https://github.com/tikv/pd/issues/7206) @ [nolouch](https://github.com/nolouch)
    -   `pd-ctl`を使用してリーダーのないリージョンを照会すると、PD がpanicになる可能性がある問題を修正しました。 [＃7630](https://github.com/tikv/pd/issues/7630) @ [rleungx](https://github.com/rleungx)
    -   リーダースイッチ後にPD監視項目`learner-peer-count`古い値を同期しない問題を修正 [＃7728](https://github.com/tikv/pd/issues/7728) @ [CabinfeverB](https://github.com/CabinfeverB)
    -   PDが`systemd` で起動したときにリソース制限を読み取れない問題を修正 [＃7628](https://github.com/tikv/pd/issues/7628) @ [bufferflies](https://github.com/bufferflies)

-   TiFlash

    -   レプリカ移行中に PD とのネットワーク接続が不安定になり、 TiFlash がpanicする可能性がある問題を修正しました [＃8323](https://github.com/pingcap/tiflash/issues/8323) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   `ENUM`値が 0 の場合にTiFlash が`ENUM`を誤って処理する問題を修正しました [＃8311](https://github.com/pingcap/tiflash/issues/8311) @ [solotzg](https://github.com/solotzg)
    -   定数文字列パラメータを含む`GREATEST`または`LEAST`関数で発生する可能性のある、ランダムに無効なメモリアクセスの問題を修正しました。 [＃8604](https://github.com/pingcap/tiflash/issues/8604) @ [windtalker](https://github.com/windtalker)
    -   `lowerUTF8`と`upperUTF8`関数で、大文字と小文字が異なるバイトを占めることができない問題を修正しました。 [＃8484](https://github.com/pingcap/tiflash/issues/8484) @ [gengliqi](https://github.com/gengliqi)
    -   短いクエリが正常に実行され、過剰な情報ログが出力される問題を修正しました。 [＃8592](https://github.com/pingcap/tiflash/issues/8592) @ [windtalker](https://github.com/windtalker)
    -   クエリの低速化によりメモリ使用量が大幅に増加する問題を修正 [＃8564](https://github.com/pingcap/tiflash/issues/8564) @ [JinheLin](https://github.com/JinheLin)
    -   `ALTER TABLE ... MODIFY COLUMN ... NOT NULL`を実行した後にTiFlash がパニックを起こし、null 許容列が非 null 許容に変更される問題を修正しました。 [＃8419](https://github.com/pingcap/tiflash/issues/8419) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   クエリを終了した後、 TiFlash上の多数のタスクが同時にキャンセルされると、同時データの競合によりTiFlash がクラッシュする問題を修正[＃7432](https://github.com/pingcap/tiflash/issues/7432) @ [SeaRise](https://github.com/SeaRise)
    -   リモート読み取り中にTiFlashがクラッシュする可能性がある問題を修正 [＃8685](https://github.com/pingcap/tiflash/issues/8685) @ [zanmato1984](https://github.com/zanmato1984)
    -   結合に非等価条件が含まれている場合に、 TiFlash Anti Semi Join が誤った結果を返す可能性がある問題を修正しました。 [＃8791](https://github.com/pingcap/tiflash/issues/8791) @ [windtalker](https://github.com/windtalker)

-   ツール

    -   Backup & Restore (BR)

        -   ログバックアップタスクを停止すると TiDB がクラッシュする問題を修正[＃50839](https://github.com/pingcap/tidb/issues/50839) @ [YuJuncen](https://github.com/YuJuncen)
        -   TiKVノードにリーダーがいないためにデータの復元が遅くなる問題を修正しました [＃50566](https://github.com/pingcap/tidb/issues/50566) @ [Leavrth](https://github.com/Leavrth)
        -   同じノードで TiKV IP アドレスを変更した後にログ バックアップが停止する問題を修正しました [＃50445](https://github.com/pingcap/tidb/issues/50445) @ [3pointer](https://github.com/3pointer)
        -   S3 からファイル コンテンツを読み取っているときにエラーが発生した場合にBR が再試行できない問題を修正しました [＃49942](https://github.com/pingcap/tidb/issues/49942) @ [Leavrth](https://github.com/Leavrth)
        -   古いバージョンのバックアップからデータを復元するときに`Unsupported collation`エラーが報告される問題を修正しました [＃49466](https://github.com/pingcap/tidb/issues/49466) @ [3pointer](https://github.com/3pointer)

    -   TiCDC

        -   アップストリームテーブルで`TRUNCATE PARTITION`を実行した後に、changefeed がエラーを報告する問題を修正しました。 [＃10522](https://github.com/pingcap/tiflow/issues/10522) @ [sdojjy](https://github.com/sdojjy)
        -   極端なケースでチェンジフィード`resolved ts`が進まない問題を修正[＃10157](https://github.com/pingcap/tiflow/issues/10157) @ [sdojjy](https://github.com/sdojjy)
        -   同期ポイントテーブルが誤って複製される可能性がある問題を修正[＃10576](https://github.com/pingcap/tiflow/issues/10576) @ [asddongmen](https://github.com/asddongmen)
        -   `ignore-event`で`add table partition`イベントをフィルタリングするように設定した後、TiCDC が関連パーティションの他のタイプの DML 変更をダウンストリームに複製しない問題を修正しました。 [＃10524](https://github.com/pingcap/tiflow/issues/10524) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   ストレージシンクの使用時に、ストレージサービスによって生成されたファイルシーケンス番号が正しく増加しない可能性がある問題を修正しました。 [＃10352](https://github.com/pingcap/tiflow/issues/10352) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   複数のチェンジフィードを同時に作成すると TiCDC が`ErrChangeFeedAlreadyExists`エラーを返す問題を修正しました [＃10430](https://github.com/pingcap/tiflow/issues/10430) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   変更フィードを再開するときに`snapshot lost caused by GC`時間内に報告されず、変更フィードの`checkpoint-ts`が TiDB の GC セーフポイントよりも小さい問題を修正しました。 [＃10463](https://github.com/pingcap/tiflow/issues/10463) @ [sdojjy](https://github.com/sdojjy)
        -   単一行データのデータ整合性検証が有効になった後、タイムゾーンの不一致により TiCDC が`TIMESTAMP`種類のチェックサムの検証に失敗する問題を修正[＃10573](https://github.com/pingcap/tiflow/issues/10573) @ [3AceShowHand](https://github.com/3AceShowHand)

    -   TiDB Data Migration (DM)

        -   タスク構成で間違ったbinlogイベントタイプがアップグレード失敗の原因となる問題を修正[＃10282](https://github.com/pingcap/tiflow/issues/10282) @ [GMHDBJD](https://github.com/GMHDBJD)
        -   `shard_row_id_bits`テーブルでスキーマ トラッカーがの初期化に失敗する問題を修正しました。 [＃10308](https://github.com/pingcap/tiflow/issues/10308) @ [GMHDBJD](https://github.com/GMHDBJD)

    -   TiDB Lightning

        -   ファイルスキャン中に無効なシンボリックリンクファイルに遭遇すると、 TiDB Lightning がエラーを報告する問題を修正しました[＃49423](https://github.com/pingcap/tidb/issues/49423) @ [lance6716](https://github.com/lance6716)
        -   `sql_mode` に`NO_ZERO_IN_DATE`が含まれていない場合に、 TiDB Lightning が`0`を含む日付値を正しく解析できない問題を修正しました。 [＃50757](https://github.com/pingcap/tidb/issues/50757) @ [GMHDBJD](https://github.com/GMHDBJD)
