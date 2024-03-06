---
title: TiDB 7.5.1 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 7.5.1.
---

# TiDB 7.5.1 リリースノート {#tidb-7-5-1-release-notes}

発売日：2024年2月29日

TiDB バージョン: 7.5.1

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup) | [インストールパッケージ](https://www.pingcap.com/download/?version=v7.5.1#version-list)

## 互換性の変更 {#compatibility-changes}

-   ユーザー[#47665](https://github.com/pingcap/tidb/issues/47665) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)の潜在的な接続問題を防ぐために、Security強化モード (SEM) で[`require_secure_transport`](https://docs.pingcap.com/tidb/v7.5/system-variables#require_secure_transport-new-in-v610) ～ `ON`の設定を禁止します。
-   ログ出力のオーバーヘッドを軽減するために、 TiFlash はデフォルト値`logger.level`を`"debug"`から`"info"` [#8641](https://github.com/pingcap/tiflash/issues/8641) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)に変更します。
-   TiKV 構成項目[`gc.num-threads`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#num-threads-new-in-v658-and-v751)を導入して、 `enable-compaction-filter`が`false` [#16101](https://github.com/tikv/tikv/issues/16101) @ [トニーシュクキ](https://github.com/tonyxuqqi)の場合の GC スレッドの数を設定します。
-   TiCDC Changefeed、次の新しい構成項目が導入されています。
    -   [`compression`](/ticdc/ticdc-changefeed-config.md) : REDO ログ ファイル[#10176](https://github.com/pingcap/tiflow/issues/10176) @ [スドジ](https://github.com/sdojjy)の圧縮動作を構成できます。
    -   [`sink.cloud-storage-config`](/ticdc/ticdc-changefeed-config.md) : データをオブジェクトstorage[#10109](https://github.com/pingcap/tiflow/issues/10109) @ [CharlesCheung96](https://github.com/CharlesCheung96)にレプリケートするときに、履歴データの自動クリーンアップを設定できます。
    -   [`consistent.flush-concurrency`](/ticdc/ticdc-changefeed-config.md) : 単一の REDO ファイルをアップロードするための同時実行性を設定できます[#10226](https://github.com/pingcap/tiflow/issues/10226) @ [スドジ](https://github.com/sdojjy)

## 改善点 {#improvements}

-   TiDB

    -   DDL スキーマのリロード プロセス中に`tikv_client_read_timeout`使用して、クラスター[#48124](https://github.com/pingcap/tidb/issues/48124) @ [cfzjywxk](https://github.com/cfzjywxk)でメタリージョンLeaderの読み取りが利用できないことによる影響を軽減します。

    -   リソース制御に関する可観測性の向上[#49318](https://github.com/pingcap/tidb/issues/49318) @ [グロルフ](https://github.com/glorv) @ [バッファフライ](https://github.com/bufferflies) @ [ノールーシュ](https://github.com/nolouch)

        アプリケーションのワークロードを分離するためにリソース グループを使用するユーザーが増えているため、リソース コントロールはリソース グループに基づいた拡張データを提供します。これにより、リソース グループのワークロードと設定を監視し、次のような問題を迅速に特定して正確に診断できるようになります。

        -   [遅いクエリ](/identify-slow-queries.md) : リソース グループ名、リソース ユニット (RU) の消費量、およびリソースの待機時間を追加します。
        -   [ステートメント概要テーブル](/statement-summary-tables.md) : リソース グループ名、RU 消費量、およびリソースの待機時間を追加します。
        -   システム変数[`tidb_last_query_info`](/system-variables.md#tidb_last_query_info-new-in-v4014)に、SQL ステートメントによって消費される[RU](/tidb-resource-control.md#what-is-request-unit-ru)を示す新しいエントリ`ru_consumption`を追加します。この変数を使用すると、セッション内の最後のステートメントのリソース消費量を取得できます。
        -   リソース グループに基づいてデータベース メトリックを追加します: QPS/TPS、実行時間 (P999/P99/P95)、失敗数、接続数。

    -   `CANCEL IMPORT JOB`ステートメントを同期ステートメント[#48736](https://github.com/pingcap/tidb/issues/48736) @ [D3ハンター](https://github.com/D3Hunter)に変更します。

    -   [`FLASHBACK CLUSTER TO TSO`](https://docs.pingcap.com/tidb/v7.5/sql-statement-flashback-cluster)構文[#48372](https://github.com/pingcap/tidb/issues/48372) @ [ボーンチェンジャー](https://github.com/BornChanger)をサポートします

    -   一部の型変換を処理するときに TiDB 実装を最適化し、関連する問題を修正しました[#47945](https://github.com/pingcap/tidb/issues/47945) [#47864](https://github.com/pingcap/tidb/issues/47864) [#47829](https://github.com/pingcap/tidb/issues/47829) [#47816](https://github.com/pingcap/tidb/issues/47816) @ [ヤンケオ](https://github.com/YangKeao) @ [ルクワンチャオ](https://github.com/lcwangchao)

    -   非バイナリ照合順序が設定されており、クエリに`LIKE`含まれる場合、オプティマイザは実行効率を向上させるために`IndexRangeScan`を生成します[#48181](https://github.com/pingcap/tidb/issues/48181) [#49138](https://github.com/pingcap/tidb/issues/49138) @ [時間と運命](https://github.com/time-and-fate)

    -   特定のシナリオ[#49616](https://github.com/pingcap/tidb/issues/49616) @ [qw4990](https://github.com/qw4990)で`OUTER JOIN`を`INNER JOIN`に変換する機能を強化します。

    -   通常の`ADD INDEX`タスク[#47758](https://github.com/pingcap/tidb/issues/47758) @ [タンジェンタ](https://github.com/tangenta)にフォールバックするのではなく、実行のためにキューに入れられる複数の高速化された`ADD INDEX` DDL タスクをサポートします。

    -   空のテーブル[#49682](https://github.com/pingcap/tidb/issues/49682) @ [ジムララ](https://github.com/zimulala)へのインデックスの追加速度を向上させました。

-   TiFlash

    -   RU 値をより安定させるために[リクエストユニット (RU)](/tidb-resource-control.md#what-is-request-unit-ru)計算方法を改善[#8391](https://github.com/pingcap/tiflash/issues/8391) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   読み取りレイテンシー[#8583](https://github.com/pingcap/tiflash/issues/8583) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)に対するディスク パフォーマンス ジッターの影響を軽減します。
    -   バックグラウンド GC タスクが読み取りおよび書き込みタスクのレイテンシーに及ぼす影響を軽減します[#8650](https://github.com/pingcap/tiflash/issues/8650) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)

-   ツール

    -   バックアップと復元 (BR)

        -   より効率的なアルゴリズム[#50613](https://github.com/pingcap/tidb/issues/50613) @ [レヴルス](https://github.com/Leavrth)を使用して、データ復元中の SST ファイルのマージ速度を向上させます。
        -   データ復元中のデータベースのバッチ作成をサポート[#50767](https://github.com/pingcap/tidb/issues/50767) @ [レヴルス](https://github.com/Leavrth)
        -   データ復元中のバッチでの SST ファイルの取り込みをサポート[#16267](https://github.com/tikv/tikv/issues/16267) @ [3ポインター](https://github.com/3pointer)
        -   ログ バックアップ中のログとメトリックのグローバル チェックポイントの進行に影響を与える最も遅いリージョンの情報を出力します[#51046](https://github.com/pingcap/tidb/issues/51046) @ [ユジュンセン](https://github.com/YuJuncen)
        -   大規模なデータセット[#48301](https://github.com/pingcap/tidb/issues/48301) @ [レヴルス](https://github.com/Leavrth)を使用するシナリオでの`RESTORE`ステートメントのテーブル作成パフォーマンスを向上させます。
        -   BR は、 `merge-schedule-limit`構成を`0` [#7148](https://github.com/tikv/pd/issues/7148) @ [ボーンチェンジャー](https://github.com/3pointer)に設定することで、リージョンのマージを一時停止できます。
        -   BR例外処理メカニズムをリファクタリングして、未知のエラー[#47656](https://github.com/pingcap/tidb/issues/47656) @ [3ポインター](https://github.com/3pointer)に対する許容度を高めます。

    -   TiCDC

        -   TiDB ダッシュボード[#10263](https://github.com/pingcap/tiflow/issues/10263) @ [CharlesCheung96](https://github.com/CharlesCheung96)での TiCDC ログの検索のサポート
        -   サポート[変更フィードのダウンストリーム同期ステータスのクエリ](https://docs.pingcap.com/tidb/v7.5/ticdc-open-api-v2#query-whether-a-specific-replication-task-is-completed)は、TiCDC が受信したアップストリーム データ変更がダウンストリーム システムに完全に同期されているかどうかを判断するのに役立ちます[#10289](https://github.com/pingcap/tiflow/issues/10289) @ [ホンユニャン](https://github.com/hongyunyan)
        -   並列処理[#10098](https://github.com/pingcap/tiflow/issues/10098) @ [CharlesCheung96](https://github.com/CharlesCheung96)を増やすことで、データをオブジェクトstorageにレプリケートする TiCDC のパフォーマンスを向上させます。

    -   TiDB Lightning

        -   多数の小さなテーブル[#50105](https://github.com/pingcap/tidb/issues/50105) @ [D3ハンター](https://github.com/D3Hunter)をインポートするときの`ALTER TABLE`のパフォーマンスを向上させます。

## バグの修正 {#bug-fixes}

-   TiDB

    -   システム変数`tidb_service_scope`の設定が反映されない問題を修正[#49245](https://github.com/pingcap/tidb/issues/49245) @ [ywqzzy](https://github.com/ywqzzy)
    -   圧縮が有効な場合、通信プロトコルが 16 MB 以上のパケットを処理できない問題を修正[#47157](https://github.com/pingcap/tidb/issues/47157) [#47161](https://github.com/pingcap/tidb/issues/47161) @ [ドヴィーデン](https://github.com/dveeden)
    -   `approx_percentile`関数が TiDBpanic[#40463](https://github.com/pingcap/tidb/issues/40463) @ [xzhangxian1008](https://github.com/xzhangxian1008)を引き起こす可能性がある問題を修正
    -   文字列関数の引数が`NULL`定数の場合、TiDB が暗黙的に`from_binary`関数を挿入する可能性があり、一部の式をTiFlash [#49526](https://github.com/pingcap/tidb/issues/49526) @ [ヤンケオ](https://github.com/YangKeao)にプッシュダウンできなくなる問題を修正しました。
    -   `HashJoin`オペレーターがディスク[#50841](https://github.com/pingcap/tidb/issues/50841) @ [wshwsh12](https://github.com/wshwsh12)へのスピルに失敗した場合に発生する可能性があるゴルーチン リークの問題を修正します。
    -   `BIT`型の列が一部の関数[#49566](https://github.com/pingcap/tidb/issues/49566) [#50850](https://github.com/pingcap/tidb/issues/50850) [#50855](https://github.com/pingcap/tidb/issues/50855) @ [ジフフスト](https://github.com/jiyfhust)の計算に関与する場合、デコード エラーによりクエリ エラーが発生する可能性がある問題を修正します。
    -   CTE クエリのメモリ使用量が制限[#50337](https://github.com/pingcap/tidb/issues/50337) @ [グオシャオゲ](https://github.com/guo-shaoge)を超えたときに発生するゴルーチン リークの問題を修正します。
    -   TiFlash の遅延マテリアライゼーションが関連する列[#49241](https://github.com/pingcap/tidb/issues/49241) [#51204](https://github.com/pingcap/tidb/issues/51204) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)を処理するときに間違った結果が返される可能性がある問題を修正
    -   TiDB が履歴統計[#49076](https://github.com/pingcap/tidb/issues/49076) @ [ホーキングレイ](https://github.com/hawkingrei)を記録するときに TiDB のバックグラウンド ジョブ スレッドがpanicになる可能性がある問題を修正
    -   TiDB がパーティション テーブル[#49023](https://github.com/pingcap/tidb/issues/49023) @ [ホーキングレイ](https://github.com/hawkingrei)のグローバル統計のヒストグラムをマージするときに発生する可能性があるエラーを修正しました。
    -   パーティションが削除された後、 `stats_meta`テーブルの履歴統計が更新されない問題を修正します[#49334](https://github.com/pingcap/tidb/issues/49334) @ [こんにちはラスティン](https://github.com/hi-rustin)
    -   誤って`Index Join`プローブ サイド[#50382](https://github.com/pingcap/tidb/issues/50382) @ [アイリンキッド](https://github.com/AilinKid)として選択された複数値インデックスによって引き起こされる誤ったクエリ結果の問題を修正します。
    -   `USE_INDEX_MERGE`ヒントが複数値インデックス[#50553](https://github.com/pingcap/tidb/issues/50553) @ [アイリンキッド](https://github.com/AilinKid)に対して有効にならない問題を修正します。
    -   `INFORMATION_SCHEMA.ANALYZE_STATUS`システム テーブル[#48835](https://github.com/pingcap/tidb/issues/48835) @ [こんにちはラスティン](https://github.com/hi-rustin)をクエリするときにユーザーがエラーを受け取る可能性がある問題を修正します。
    -   TiDB が`group by` [#38756](https://github.com/pingcap/tidb/issues/38756) @ [こんにちはラスティン](https://github.com/hi-rustin)の定数値を誤って削除するため、間違ったクエリ結果が発生する問題を修正しました。
    -   テーブル上の`ANALYZE`タスクのうち`processed_rows`が、そのテーブルの総行数[#50632](https://github.com/pingcap/tidb/issues/50632) @ [ホーキングレイ](https://github.com/hawkingrei)を超える可能性がある問題を修正します。
    -   `tidb_enable_prepared_plan_cache`システム変数が有効になってから無効になった後、 `EXECUTE`ステートメントを使用して`PREPARE STMT`を実行すると、TiDB がパニックになる可能panicがある問題を修正します[#49344](https://github.com/pingcap/tidb/issues/49344) @ [qw4990](https://github.com/qw4990)
    -   クエリで`NATURAL JOIN` [#32044](https://github.com/pingcap/tidb/issues/32044) @ [アイリンキッド](https://github.com/AilinKid)を使用するときに発生する可能性がある`Column ... in from clause is ambiguous`エラーを修正しました。
    -   複数値インデックスを使用して空の JSON 配列にアクセスすると、誤った結果[#50125](https://github.com/pingcap/tidb/issues/50125) @ [ヤンケオ](https://github.com/YangKeao)が返される可能性がある問題を修正します。
    -   グループ計算に集計関数が使用されている場合に発生する可能性がある`Can't find column ...`エラーを修正[#50926](https://github.com/pingcap/tidb/issues/50926) @ [qw4990](https://github.com/qw4990)
    -   文字列型変数の`SET_VAR`の制御が無効になる場合がある問題を修正[#50507](https://github.com/pingcap/tidb/issues/50507) @ [qw4990](https://github.com/qw4990)
    -   `tidb_server_memory_limit` [#48741](https://github.com/pingcap/tidb/issues/48741) @ [徐淮嶼](https://github.com/XuHuaiyu)による長期的なメモリ負荷により TiDB の CPU 使用率が高くなる問題を修正
    -   依存関係のある 2 つの DDL タスクの完了時間が誤って順序付けされる問題を修正します[#49498](https://github.com/pingcap/tidb/issues/49498) @ [タンジェンタ](https://github.com/tangenta)
    -   不正なオプティマイザ ヒントにより有効なヒントが無効になる可能性がある問題を修正[#49308](https://github.com/pingcap/tidb/issues/49308) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `CHECK`制約を持つ DDL ステートメントが[#47632](https://github.com/pingcap/tidb/issues/47632) @ [ジフフスト](https://github.com/jiyfhust)でスタックする問題を修正
    -   `CHECK`制約の`ENFORCED`オプションの動作が MySQL 8.0 [#47567](https://github.com/pingcap/tidb/issues/47567) [#47631](https://github.com/pingcap/tidb/issues/47631) @ [ジフフスト](https://github.com/jiyfhust)と矛盾する問題を修正
    -   CTE クエリが再試行プロセス[#46522](https://github.com/pingcap/tidb/issues/46522) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)中にエラー`type assertion for CTEStorageMap failed`を報告する可能性がある問題を修正します。
    -   `tidb_multi_statement_mode`モードが有効になっている場合、インデックス ルックアップを使用する`DELETE`および`UPDATE`ステートメントでエラーが報告される可能性がある問題を修正[#50012](https://github.com/pingcap/tidb/issues/50012) @ [タンジェンタ](https://github.com/tangenta)
    -   `WITH RECURSIVE` CTE を含む`UPDATE`または`DELETE`ステートメントが誤った結果を生成する可能性がある問題を修正します[#48969](https://github.com/pingcap/tidb/issues/48969) @ [ウィノロス](https://github.com/winoros)
    -   特定のシナリオ[#49285](https://github.com/pingcap/tidb/issues/49285) @ [アイリンキッド](https://github.com/AilinKid)で、オプティマイザーがTiFlash選択パスを DUAL テーブルに誤って変換する問題を修正します。
    -   同じクエリ プランに異なる`PLAN_DIGEST`値、場合によっては[#47634](https://github.com/pingcap/tidb/issues/47634) @ [キングディラン](https://github.com/King-Dylan)含まれる問題を修正
    -   自動統計更新の時間枠が設定された後でも、その時間枠外で統計が更新される可能性がある問題を修正します[#49552](https://github.com/pingcap/tidb/issues/49552) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `ENUM`型のカラムを結合キー[#48991](https://github.com/pingcap/tidb/issues/48991) @ [ウィノロス](https://github.com/winoros)として使用した場合、クエリ結果が正しくない問題を修正
    -   `ORDER BY`句を使用して`UNIQUE`インデックス ルックアップを実行すると、エラー[#49920](https://github.com/pingcap/tidb/issues/49920) @ [ジャッキースプ](https://github.com/jackysp)が発生する可能性がある問題を修正します。
    -   マルチレベルでネストされた`UNION`クエリの`LIMIT`無効になる可能性がある問題を修正[#49874](https://github.com/pingcap/tidb/issues/49874) @ [定義2014](https://github.com/Defined2014)
    -   MPP で計算した`COUNT(INT)`の結果が[#48643](https://github.com/pingcap/tidb/issues/48643) @ [アイリンキッド](https://github.com/AilinKid)と正しくない場合がある問題を修正
    -   `ENUM`または`SET`種類の無効な値を解析すると SQL ステートメント エラー[#49487](https://github.com/pingcap/tidb/issues/49487) @ [ウィノロス](https://github.com/winoros)が直接発生する問題を修正します。
    -   TiDB がパニックになり、エラー`invalid memory address or nil pointer dereference` [#42739](https://github.com/pingcap/tidb/issues/42739) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)を報告する問題を修正
    -   最初のサブノードとして DUAL テーブルを使用して`UNION ALL`を実行すると、エラー[#48755](https://github.com/pingcap/tidb/issues/48755) @ [ウィノロス](https://github.com/winoros)が発生する可能性がある問題を修正します。
    -   `UNION ALL`ステートメント[#50068](https://github.com/pingcap/tidb/issues/50068) @ [ホーキングレイ](https://github.com/hawkingrei)で共通ヒントが有効にならない問題を修正
    -   正常なシャットダウン[#36793](https://github.com/pingcap/tidb/issues/36793) @ [bb7133](https://github.com/bb7133)中に TiDBサーバーがpanicになる可能性がある問題を修正
    -   一部のタイムゾーン[#49586](https://github.com/pingcap/tidb/issues/49586) @ [オーバーヴィーナス](https://github.com/overvenus)でサマータイムが正しく表示されない問題を修正
    -   static `CALIBRATE RESOURCE`が Prometheus データ[#49174](https://github.com/pingcap/tidb/issues/49174) @ [グロルフ](https://github.com/glorv)に依存する問題を修正
    -   `REPLACE INTO`ステートメント[#34325](https://github.com/pingcap/tidb/issues/34325) @ [ヤンケオ](https://github.com/YangKeao)でヒントが使用できない問題を修正
    -   `GROUP_CONCAT(ORDER BY)`構文を含むクエリを実行するとエラー[#49986](https://github.com/pingcap/tidb/issues/49986) @ [アイリンキッド](https://github.com/AilinKid)が返される可能性がある問題を修正します。
    -   監査ログ用のエンタープライズ プラグインが使用されている場合、TiDBサーバーが大量のリソースを消費する可能性がある問題を修正[#49273](https://github.com/pingcap/tidb/issues/49273) @ [ルクワンチャオ](https://github.com/lcwangchao)
    -   古いインターフェースを使用すると、テーブル[#49751](https://github.com/pingcap/tidb/issues/49751) @ [ホーキングレイ](https://github.com/hawkingrei)のメタデータが不整合になる可能性がある問題を修正
    -   `tidb_enable_collect_execution_info`を無効にするとコプロセッサ キャッシュがpanic[#48212](https://github.com/pingcap/tidb/issues/48212) @ [あなた06](https://github.com/you06)になる問題を修正
    -   パーティション列タイプが`DATETIME` [#48814](https://github.com/pingcap/tidb/issues/48814) @ [クレイジークス520](https://github.com/crazycs520)の場合、 `ALTER TABLE ... LAST PARTITION`の実行が失敗する問題を修正
    -   `COM_STMT_EXECUTE`を介して実行された`COMMIT`または`ROLLBACK`操作がタイムアウトしたトランザクションを終了できない問題を修正します[#49151](https://github.com/pingcap/tidb/issues/49151) @ [ジグアン](https://github.com/zyguan)
    -   ヒストグラムの境界に`NULL` [#49823](https://github.com/pingcap/tidb/issues/49823) @ [アイリンキッド](https://github.com/AilinKid)が含まれる場合、ヒストグラム統計が読み取り可能な文字列に解析されない可能性がある問題を修正します。
    -   メモリ制限[#49096](https://github.com/pingcap/tidb/issues/49096) @ [アイリンキッド](https://github.com/AilinKid)を超えると、共通テーブル式 (CTE) を含むクエリが予期せずスタックする問題を修正します。
    -   DDL 所有者がネットワーク分離された後に`ADD INDEX`実行すると、TiDB 分散実行フレームワーク (DXF) でデータが矛盾する問題を修正[#49773](https://github.com/pingcap/tidb/issues/49773) @ [タンジェンタ](https://github.com/tangenta)
    -   `AUTO_ID_CACHE=1` [#50519](https://github.com/pingcap/tidb/issues/50519) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)の自動インクリメント列を使用すると、同時競合により自動インクリメント ID 割り当てでエラーが報告される問題を修正します。
    -   panicに適用演算子が含まれており、 `fatal error: concurrent map writes`エラーが発生すると TiDB がパニックになる可能性がある問題を修正します[#50347](https://github.com/pingcap/tidb/issues/50347) @ [シーライズ](https://github.com/SeaRise)
    -   DDL `jobID`が 0 [#46296](https://github.com/pingcap/tidb/issues/46296) @ [ジフフスト](https://github.com/jiyfhust)に復元されるときに発生する TiDB ノードのpanic問題を修正
    -   `STREAM_AGG()`の CI [#49902](https://github.com/pingcap/tidb/issues/49902) @ [wshwsh12](https://github.com/wshwsh12)の処理が間違っているため、クエリ結果が正しくない問題を修正します。
    -   多数のテーブルまたはパーティション[#50077](https://github.com/pingcap/tidb/issues/50077) @ [ジムララ](https://github.com/zimulala)を処理するときに TiDB ノードで OOM エラーが発生する可能性がある問題を軽減します。
    -   `LEADING`ヒントが`UNION ALL`のステートメント[#50067](https://github.com/pingcap/tidb/issues/50067) @ [ホーキングレイ](https://github.com/hawkingrei)で有効にならない問題を修正
    -   ネストされた`UNION`クエリ[#49377](https://github.com/pingcap/tidb/issues/49377) @ [アイリンキッド](https://github.com/AilinKid)で`LIMIT`と`OPRDERBY`無効になる可能性がある問題を修正
    -   メモリが`tidb_mem_quota_query` [#49033](https://github.com/pingcap/tidb/issues/49033) @ [徐淮嶼](https://github.com/XuHuaiyu)を超えると、IndexHashJoin 演算子を含むクエリがスタックする問題を修正します。
    -   定数伝播[#49440](https://github.com/pingcap/tidb/issues/49440) @ [ウィノロス](https://github.com/winoros)で`ENUM`または`SET`型を処理すると、TiDB が間違ったクエリ結果を返す問題を修正
    -   `PREPARE`メソッドを使用して`SELECT INTO OUTFILE`を実行すると、エラー[#49166](https://github.com/pingcap/tidb/issues/49166) @ [qw4990](https://github.com/qw4990)ではなく成功メッセージが誤って返される問題を修正します。
    -   クエリでソートを強制するオプティマイザ ヒント ( `STREAM_AGG()`など) が使用されており、その実行プランに`IndexMerge` [#49605](https://github.com/pingcap/tidb/issues/49605) @ [アイリンキッド](https://github.com/AilinKid)が含まれている場合、強制ソートが無効になる可能性がある問題を修正します。
    -   多数のテーブル[#48869](https://github.com/pingcap/tidb/issues/48869) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)がある場合、 `AUTO_ID_CACHE=1`テーブルによって gRPC クライアント リークが発生する可能性がある問題を修正します。
    -   非厳密モード ( `sql_mode = ''` ) で、 `INSERT`の実行中に切り詰めると引き続きエラー[#49369](https://github.com/pingcap/tidb/issues/49369) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)が報告される問題を修正します。
    -   データの末尾にスペースが含まれている場合に`LIKE`に`_`ワイルドカードを使用すると、誤ったクエリ結果[#48983](https://github.com/pingcap/tidb/issues/48983) @ [時間と運命](https://github.com/time-and-fate)が発生する可能性がある問題を修正します。
    -   `tidb_mem_quota_query`システム変数を更新した後に`ADMIN CHECK`を実行すると`ERROR 8175` [#49258](https://github.com/pingcap/tidb/issues/49258) @ [タンジェンタ](https://github.com/tangenta)が返される問題を修正
    -   Golang の暗黙的な変換アルゴリズム[#49801](https://github.com/pingcap/tidb/issues/49801) @ [qw4990](https://github.com/qw4990)によって引き起こされる統計構築時の過剰な統計エラーの問題を修正
    -   `tidb_max_chunk_size`が小さい値[#48808](https://github.com/pingcap/tidb/issues/48808) @ [グオシャオゲ](https://github.com/guo-shaoge)に設定されている場合、CTE を含むクエリで`runtime error: index out of range [32] with length 32`が報告される問題を修正します。

-   TiKV

    -   `tidb_enable_row_level_checksum`を有効にすると TiKV がpanic[#16371](https://github.com/tikv/tikv/issues/16371) @ [cfzjywxk](https://github.com/cfzjywxk)になる可能性がある問題を修正
    -   gRPC スレッドが`is_shutdown` [#16236](https://github.com/tikv/tikv/issues/16236) @ [ピンギュ](https://github.com/pingyu)をチェックしているときに TiKV がpanicになる可能性がある問題を修正
    -   TiKV がブラジルとエジプトのタイムゾーンを誤って変換する問題を修正します[#16220](https://github.com/tikv/tikv/issues/16220) @ [オーバーヴィーナス](https://github.com/overvenus)
    -   Titanの`blob-run-mode`オンライン[#15978](https://github.com/tikv/tikv/issues/15978) @ [トニーシュクキ](https://github.com/tonyxuqqi)に更新できない問題を修正
    -   TiDB と TiKV が`DECIMAL`算術乗算切り捨て[#16268](https://github.com/tikv/tikv/issues/16268) @ [ソロッツグ](https://github.com/solotzg)を処理するときに一貫性のない結果を生成する可能性がある問題を修正します。
    -   `notLeader`または`regionNotFound` [#15712](https://github.com/tikv/tikv/issues/15712) @ [ヒューシャープ](https://github.com/HuSharp)に遭遇したときにフラッシュバックがスタックすることがある問題を修正
    -   破損した SST ファイルが他の TiKV ノード[#15986](https://github.com/tikv/tikv/issues/15986) @ [コナー1996](https://github.com/Connor1996)に拡散する可能性がある問題を修正
    -   TiKV の実行が非常に遅い場合、リージョンマージ[#16111](https://github.com/tikv/tikv/issues/16111) @ [オーバーヴィーナス](https://github.com/overvenus)後にpanicが発生する可能性がある問題を修正
    -   [#15817](https://github.com/tikv/tikv/issues/15817) @ [コナー1996](https://github.com/Connor1996)のスケールアウト時に DR Auto-Sync のジョイント状態がタイムアウトになる可能性がある問題を修正
    -   解決済み TS が 2 時間ブロックされる可能性がある問題を修正[#11847](https://github.com/tikv/tikv/issues/11847) [#15520](https://github.com/tikv/tikv/issues/15520) [#39130](https://github.com/pingcap/tidb/issues/39130) @ [オーバーヴィーナス](https://github.com/overvenus)
    -   `cast_duration_as_time`が間違った結果[#16211](https://github.com/tikv/tikv/issues/16211) @ [ゲンリキ](https://github.com/gengliqi)を返す可能性がある問題を修正

-   PD

    -   バッチでリソース グループをクエリすると PD がpanic[#7206](https://github.com/tikv/pd/issues/7206) @ [ノールーシュ](https://github.com/nolouch)になる可能性がある問題を修正
    -   PD が`systemd` [#7628](https://github.com/tikv/pd/issues/7628) @ [バッファフライ](https://github.com/bufferflies)で起動されたときにリソース制限を読み取れない問題を修正
    -   PD ディスクレイテンシーにおける継続的なジッターにより、PD が新しいリーダー[#7251](https://github.com/tikv/pd/issues/7251) @ [ヒューシャープ](https://github.com/HuSharp)の選択に失敗する可能性がある問題を修正します。
    -   PD のネットワーク分割によりスケジューリングがすぐに開始されないことがある問題を修正[#7016](https://github.com/tikv/pd/issues/7016) @ [ヒューシャープ](https://github.com/HuSharp)
    -   PD監視項目`learner-peer-count`がリーダースイッチ[#7728](https://github.com/tikv/pd/issues/7728) @ [キャビンフィーバーB](https://github.com/CabinfeverB)後に古い値と同期しない問題を修正
    -   PD リーダーが移動され、新しいリーダーと PD クライアントの間にネットワーク分割がある場合、PD クライアントがリーダー[#7416](https://github.com/tikv/pd/issues/7416) @ [キャビンフィーバーB](https://github.com/CabinfeverB)の情報を更新できない問題を修正します
    -   Jin Web Framework のバージョンを v1.8.1 から v1.9.1 [#7438](https://github.com/tikv/pd/issues/7438) @ [ニューベル](https://github.com/niubell)にアップグレードすることで、いくつかのセキュリティ問題を修正します。
    -   レプリカの数が要件[#7584](https://github.com/tikv/pd/issues/7584) @ [バッファフライ](https://github.com/bufferflies)を満たさない場合に孤立ピアが削除される問題を修正
    -   `pd-ctl`を使用してリーダーなしでリージョンをクエリすると、PD がpanic[#7630](https://github.com/tikv/pd/issues/7630) @ [ルルンクス](https://github.com/rleungx)になる可能性がある問題を修正します。

-   TiFlash

    -   レプリカ移行[#8323](https://github.com/pingcap/tiflash/issues/8323) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)中に PD とのネットワーク接続が不安定なためにTiFlash がpanicになる可能性がある問題を修正
    -   TiFlashレプリカを削除してから再度追加すると、 TiFlash [#8695](https://github.com/pingcap/tiflash/issues/8695) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)でデータ破損が発生する可能性がある問題を修正します。
    -   データ挿入[#8395](https://github.com/pingcap/tiflash/issues/8395) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)の直後に`DROP TABLE`を実行すると、 `FLASHBACK TABLE`または`RECOVER TABLE`一部のTiFlashレプリカのデータを回復できない可能性があるという潜在的な問題を修正します。
    -   Grafana [#8076](https://github.com/pingcap/tiflash/issues/8076) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)の一部のパネルの最大パーセンタイル時間の誤った表示を修正
    -   リモート読み取り[#8685](https://github.com/pingcap/tiflash/issues/8685) @ [グオシャオゲ](https://github.com/guo-shaoge)中にTiFlash がクラッシュする可能性がある問題を修正
    -   `ENUM`値が 0 [#8311](https://github.com/pingcap/tiflash/issues/8311) @ [ソロッツグ](https://github.com/solotzg)の場合にTiFlash が`ENUM`を誤って処理する問題を修正
    -   短いクエリが正常に実行されると過剰な情報ログ[#8592](https://github.com/pingcap/tiflash/issues/8592) @ [ウィンドトーカー](https://github.com/windtalker)が出力される問題を修正します。
    -   遅いクエリ[#8564](https://github.com/pingcap/tiflash/issues/8564) @ [ジンヘリン](https://github.com/JinheLin)によりメモリ使用量が大幅に増加する問題を修正
    -   `lowerUTF8`および`upperUTF8`関数で、大文字と小文字が異なる文字が異なるバイト[#8484](https://github.com/pingcap/tiflash/issues/8484) @ [ゲンリキ](https://github.com/gengliqi)を占めることができない問題を修正します。
    -   ストリーム読み取り[#8505](https://github.com/pingcap/tiflash/issues/8505) @ [ゲンリチ](https://github.com/gengliqi)中に複数のパーティション分割テーブルをスキャンするときに発生する可能性がある OOM の問題を修正します。
    -   TiFlash がクエリ[#8447](https://github.com/pingcap/tiflash/issues/8447) @ [ジンヘリン](https://github.com/JinheLin)中にメモリ制限に遭遇した場合のメモリリークの問題を修正
    -   DDL の同時実行中にTiFlash で競合が発生した場合のTiFlashpanic問題を修正[#8578](https://github.com/pingcap/tiflash/issues/8578) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)
    -   Null 許容カラムを Null 非許容カラム[#8419](https://github.com/pingcap/tiflash/issues/8419) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)に変更する`ALTER TABLE ... MODIFY COLUMN ... NOT NULL`の実行後にTiFlashがパニックになる問題を修正
    -   `ColumnRef in (Literal, Func...)` [#8631](https://github.com/pingcap/tiflash/issues/8631) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)のようなフィルタリング条件を使用してクエリを実行すると、クエリ結果が正しくなくなる問題を修正
    -   `FLASHBACK DATABASE` [#8450](https://github.com/pingcap/tiflash/issues/8450) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)を実行した後もTiFlashレプリカのデータがガベージ コレクションされる問題を修正
    -   TiFlash が、非集約storageおよびコンピューティングアーキテクチャ[#8519](https://github.com/pingcap/tiflash/issues/8519) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)でオブジェクトstorageデータの GC 所有者を選択できない可能性がある問題を修正します。
    -   定数文字列パラメーター[#8604](https://github.com/pingcap/tiflash/issues/8604) @ [ウィンドトーカー](https://github.com/windtalker)を含む`GREATEST`または`LEAST`関数で発生する可能性があるランダムな無効なメモリアクセスの問題を修正します。
    -   ポイントインタイム リカバリ (PITR) の実行後、または`FLASHBACK CLUSTER TO`実行後にTiFlashレプリカ データが誤って削除され、データ異常が発生する可能性がある問題を修正します[#8777](https://github.com/pingcap/tiflash/issues/8777) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)
    -   結合に等価でない条件[#8791](https://github.com/pingcap/tiflash/issues/8791) @ [ウィンドトーカー](https://github.com/windtalker)が含まれている場合、 TiFlash Anti Semi Join が誤った結果を返す可能性がある問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   TiKV ノード[#50566](https://github.com/pingcap/tidb/issues/50566) @ [レヴルス](https://github.com/Leavrth)にリーダーが存在しないためにデータの復元が遅くなる問題を修正
        -   `--filter`オプションを指定した後も完全復元ではターゲット クラスターが空である必要があるという問題を修正します[#51009](https://github.com/pingcap/tidb/issues/51009) @ [3ポインター](https://github.com/3pointer)
        -   データの復元に失敗した後にチェックポイントから再開すると、エラー`the target cluster is not fresh`が発生する問題を修正します[#50232](https://github.com/pingcap/tidb/issues/50232) @ [レヴルス](https://github.com/Leavrth)
        -   ログ バックアップ タスクを停止すると TiDB がクラッシュする問題を修正します[#50839](https://github.com/pingcap/tidb/issues/50839) @ [ユジュンセン](https://github.com/YuJuncen)
        -   古いバージョン[#49466](https://github.com/pingcap/tidb/issues/49466) @ [3ポインター](https://github.com/3pointer)のバックアップからデータを復元すると`Unsupported collation`エラーが報告される問題を修正します。
        -   タスクの初期化中に PD への接続に失敗すると、ログ バックアップ タスクを開始できても正しく動作しない問題を修正[#16056](https://github.com/tikv/tikv/issues/16056) @ [ユジュンセン](https://github.com/YuJuncen)
        -   BR が外部storageファイル[#48452](https://github.com/pingcap/tidb/issues/48452) @ [3エースショーハンド](https://github.com/3AceShowHand)に対して間違った URI を生成する問題を修正
        -   同じノード[#50445](https://github.com/pingcap/tidb/issues/50445) @ [3ポインター](https://github.com/3pointer)で TiKV IP アドレスを変更した後にログのバックアップが停止する問題を修正
        -   S3 [#49942](https://github.com/pingcap/tidb/issues/49942) @ [レヴルス](https://github.com/Leavrth)からファイルの内容を読み取るときにエラーが発生した場合にBR が再試行できない問題を修正

    -   TiCDC

        -   Syncpoint が有効になっている場合にエラーが発生した後、シンク モジュールが正しく再起動できない問題を修正します ( `enable-sync-point = true` ) [#10091](https://github.com/pingcap/tiflow/issues/10091) @ [ひっくり返る](https://github.com/hicqu)
        -   storageシンク[#10352](https://github.com/pingcap/tiflow/issues/10352) @ [CharlesCheung96](https://github.com/CharlesCheung96)を使用する場合、storageサービスによって生成されたファイル シーケンス番号が正しく増加しないことがある問題を修正します。
        -   同期ポイント テーブルが誤って複製される可能性がある問題を修正[#10576](https://github.com/pingcap/tiflow/issues/10576) @ [東門](https://github.com/asddongmen)
        -   Apache Pulsar をダウンストリーム[#10602](https://github.com/pingcap/tiflow/issues/10602) @ [東門](https://github.com/asddongmen)として使用する場合、OAuth2.0、TLS、および mTLS を適切に有効にできない問題を修正
        -   複数の変更フィード[#10430](https://github.com/pingcap/tiflow/issues/10430) @ [CharlesCheung96](https://github.com/CharlesCheung96)を同時に作成すると TiCDC が`ErrChangeFeedAlreadyExists`エラーを返す問題を修正
        -   極端なケース[#10157](https://github.com/pingcap/tiflow/issues/10157) @ [スドジ](https://github.com/sdojjy)でチェンジフィード`resolved ts`が進まない問題を修正
        -   特定の特別なシナリオ[#10239](https://github.com/pingcap/tiflow/issues/10239) @ [ひっくり返る](https://github.com/hicqu)で、TiCDC が誤って TiKV との接続を閉じる問題を修正します。
        -   データをオブジェクトstorageサービス[#10137](https://github.com/pingcap/tiflow/issues/10137) @ [スドジ](https://github.com/sdojjy)にレプリケートするときに TiCDCサーバーがpanicになる可能性がある問題を修正します。
        -   上流テーブル[#10522](https://github.com/pingcap/tiflow/issues/10522) @ [スドジ](https://github.com/sdojjy)で`TRUNCATE PARTITION`が実行された後、変更フィードがエラーを報告する問題を修正します。
        -   `ignore-event`で構成された`add table partition`イベントをフィルタリングした後、TiCDC が関連パーティションの他のタイプの DML 変更をダウンストリーム[#10524](https://github.com/pingcap/tiflow/issues/10524) @ [CharlesCheung96](https://github.com/CharlesCheung96)にレプリケートしない問題を修正します。
        -   `kv-client`初期化[#10095](https://github.com/pingcap/tiflow/issues/10095) @ [3エースショーハンド](https://github.com/3AceShowHand)中の潜在的なデータ競合の問題を修正

    -   TiDB データ移行 (DM)

        -   ダウンストリームのテーブル構造に`shard_row_id_bits` [#10308](https://github.com/pingcap/tiflow/issues/10308) @ [GMHDBJD](https://github.com/GMHDBJD)が含まれる場合に移行タスク エラーが発生する問題を修正
        -   DM で「イベント タイプの切り捨てが無効です」エラーが発生し、アップグレードが失敗する問題を修正します[#10282](https://github.com/pingcap/tiflow/issues/10282) @ [GMHDBJD](https://github.com/GMHDBJD)
