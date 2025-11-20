---
title: TiDB 7.5.1 Release Notes
summary: TiDB 7.5.1 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 7.5.1 リリースノート {#tidb-7-5-1-release-notes}

発売日：2024年2月29日

TiDB バージョン: 7.5.1

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   Security強化モード（SEM）で設定[`require_secure_transport`](https://docs.pingcap.com/tidb/v7.5/system-variables#require_secure_transport-new-in-v610) ～ `ON`を禁止し、ユーザー[＃47665](https://github.com/pingcap/tidb/issues/47665) @ [天菜麻緒](https://github.com/tiancaiamao)の潜在的な接続問題を防ぎます。
-   ログ印刷のオーバーヘッドを減らすために、 TiFlashはデフォルト値の`logger.level` `"debug"`から`"info"` [＃8641](https://github.com/pingcap/tiflash/issues/8641) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)に変更します。
-   TiKV構成項目[`gc.num-threads`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#num-threads-new-in-v658-and-v751)を導入して、 `enable-compaction-filter`が`false` [＃16101](https://github.com/tikv/tikv/issues/16101) @ [トニーシュキ](https://github.com/tonyxuqqi)の場合のGCスレッド数を設定します。
-   TiCDC Changefeed、次の新しい構成項目が導入されています。
    -   [`compression`](/ticdc/ticdc-changefeed-config.md) : REDOログファイルの圧縮動作を設定できます[＃10176](https://github.com/pingcap/tiflow/issues/10176) @ [スドジ](https://github.com/sdojjy)
    -   [`sink.cloud-storage-config`](/ticdc/ticdc-changefeed-config.md) : オブジェクトstorage[＃10109](https://github.com/pingcap/tiflow/issues/10109) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)にデータを複製するときに履歴データの自動クリーンアップを設定できます。
    -   [`consistent.flush-concurrency`](/ticdc/ticdc-changefeed-config.md) : 単一のREDOファイルのアップロードの同時実行を[＃10226](https://github.com/pingcap/tiflow/issues/10226) @ [スドジ](https://github.com/sdojjy)に設定できます

## 改善点 {#improvements}

-   ティドブ

    -   DDLスキーマの再ロードプロセス中に`tikv_client_read_timeout`使用して、クラスタ[＃48124](https://github.com/pingcap/tidb/issues/48124) @ [cfzjywxk](https://github.com/cfzjywxk)でのメタリージョンLeaderの読み取り不可の影響を軽減します。

    -   リソース制御に関する可観測性を強化する[＃49318](https://github.com/pingcap/tidb/issues/49318) @ [栄光](https://github.com/glorv) @ [バッファフライ](https://github.com/bufferflies) @ [ノルーシュ](https://github.com/nolouch)

        リソースグループを使用してアプリケーションのワークロードを分離するユーザーが増えるにつれ、リソースコントロールはリソースグループに基づいた拡張データを提供します。これにより、リソースグループのワークロードと設定を監視し、次のような問題を迅速に特定し、正確に診断できるようになります。

        -   [遅いクエリ](/identify-slow-queries.md) : リソース グループ名、リソース ユニット (RU) の消費量、およびリソースの待機時間を追加します。
        -   [明細書要約表](/statement-summary-tables.md) : リソース グループ名、RU 消費量、リソースの待機時間を追加します。
        -   システム変数[`tidb_last_query_info`](/system-variables.md#tidb_last_query_info-new-in-v4014)に、SQL文によって消費されたリソース量[ロシア](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru)を示す新しいエントリ`ru_consumption`を追加します。この変数を使用して、セッション内の最後の文のリソース消費量を取得できます。
        -   リソース グループに基づいてデータベース メトリックを追加します: QPS/TPS、実行時間 (P999/P99/P95)、障害数、接続数。

    -   `CANCEL IMPORT JOB`文を同期文[＃48736](https://github.com/pingcap/tidb/issues/48736) @ [D3ハンター](https://github.com/D3Hunter)に変更します。

    -   [`FLASHBACK CLUSTER TO TSO`](https://docs.pingcap.com/tidb/v7.5/sql-statement-flashback-cluster)構文[＃48372](https://github.com/pingcap/tidb/issues/48372) @ [生まれ変わった人](https://github.com/BornChanger)をサポート

    -   いくつかの型変換を処理する際の TiDB 実装を最適化し、関連する問題を修正しました[＃47945](https://github.com/pingcap/tidb/issues/47945) [＃47864](https://github.com/pingcap/tidb/issues/47864) [＃47829](https://github.com/pingcap/tidb/issues/47829) [＃47816](https://github.com/pingcap/tidb/issues/47816) @ [ヤンケオ](https://github.com/YangKeao) @ [lcwangchao](https://github.com/lcwangchao)

    -   非バイナリ照合順序が設定され、クエリに`LIKE`含まれている場合、オプティマイザは実行効率を向上させるために`IndexRangeScan`を生成します[＃48181](https://github.com/pingcap/tidb/issues/48181) [＃49138](https://github.com/pingcap/tidb/issues/49138) @ [時間と運命](https://github.com/time-and-fate)

    -   特定のシナリオで`OUTER JOIN`を`INNER JOIN`に変換する能力を強化する[＃49616](https://github.com/pingcap/tidb/issues/49616) @ [qw4990](https://github.com/qw4990)

    -   通常の`ADD INDEX`タスク[＃47758](https://github.com/pingcap/tidb/issues/47758) @ [接線](https://github.com/tangenta)にフォールバックするのではなく、複数の加速された`ADD INDEX` DDL タスクをキューに入れて実行できるようにサポートします。

    -   空のテーブルにインデックスを追加する速度を向上[＃49682](https://github.com/pingcap/tidb/issues/49682) @ [ジムララ](https://github.com/zimulala)

-   ティクブ

    -   低速ストア検出アルゴリズムを強化し、感度を向上させ、特に集中的な読み取りおよび書き込み負荷のシナリオで誤検出率を低減します[＃15909](https://github.com/tikv/tikv/issues/15909) @ [LykxSassinator](https://github.com/LykxSassinator)

-   TiFlash

    -   RU値をより安定させるために[リクエストユニット（RU）](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru)計算方法を改善する[＃8391](https://github.com/pingcap/tiflash/issues/8391) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   ディスクパフォ​​ーマンスジッターによる読み取りレイテンシーへの影響を軽減[＃8583](https://github.com/pingcap/tiflash/issues/8583) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   バックグラウンド GC タスクによる読み取りおよび書き込みタスクのレイテンシーへの影響を軽減します[＃8650](https://github.com/pingcap/tiflash/issues/8650) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)

-   ツール

    -   バックアップと復元 (BR)

        -   より効率的なアルゴリズム[＃50613](https://github.com/pingcap/tidb/issues/50613) @ [リーヴルス](https://github.com/Leavrth)を使用して、データ復元中に SST ファイルをマージする速度を改善します
        -   データ復元中にデータベースをバッチで作成するサポート[＃50767](https://github.com/pingcap/tidb/issues/50767) @ [リーヴルス](https://github.com/Leavrth)
        -   データ復元中に SST ファイルをバッチで取り込むことをサポート[＃16267](https://github.com/tikv/tikv/issues/16267) @ [3ポイントシュート](https://github.com/3pointer)
        -   ログバックアップ[＃51046](https://github.com/pingcap/tidb/issues/51046) @ [ユジュンセン](https://github.com/YuJuncen)中に、ログとメトリックのグローバルチェックポイントの進行に影響を与える最も遅いリージョンの情報を出力します。
        -   大規模なデータセット[＃48301](https://github.com/pingcap/tidb/issues/48301) @ [リーヴルス](https://github.com/Leavrth)のシナリオで`RESTORE`ステートメントのテーブル作成パフォーマンスを向上
        -   BRは`merge-schedule-limit`設定を`0` [＃7148](https://github.com/tikv/pd/issues/7148) @ [生まれ変わった人](https://github.com/3pointer)に設定することでリージョンのマージを一時停止できます。
        -   BR例外処理メカニズムをリファクタリングして、未知のエラーに対する許容度を高めます[＃47656](https://github.com/pingcap/tidb/issues/47656) @ [3ポイントシュート](https://github.com/3pointer)

    -   TiCDC

        -   TiDBダッシュボード[＃10263](https://github.com/pingcap/tiflow/issues/10263) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)でのTiCDCログの検索をサポート
        -   サポート[チェンジフィードの下流同期ステータスの照会](https://docs.pingcap.com/tidb/v7.5/ticdc-open-api-v2#query-whether-a-specific-replication-task-is-completed)は、TiCDC が受信した上流データの変更が下流システムに完全に同期されているかどうかを判断するのに役立ちます[＃10289](https://github.com/pingcap/tiflow/issues/10289) @ [ホンユニャン](https://github.com/hongyunyan)
        -   並列処理を[＃10098](https://github.com/pingcap/tiflow/issues/10098) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)に増やすことで、TiCDC がオブジェクトstorageにデータを複製する際のパフォーマンスが向上します。

    -   TiDB Lightning

        -   多数の小さなテーブル[＃50105](https://github.com/pingcap/tidb/issues/50105) `ALTER TABLE` [D3ハンター](https://github.com/D3Hunter)

## バグ修正 {#bug-fixes}

-   ティドブ

    -   システム変数`tidb_service_scope`設定が[＃49245](https://github.com/pingcap/tidb/issues/49245)で[ywqzzy](https://github.com/ywqzzy)に反映されない問題を修正
    -   圧縮が有効になっている場合、通信プロトコルが16 MB以上のパケットを処理できない問題を修正[＃47157](https://github.com/pingcap/tidb/issues/47157) [＃47161](https://github.com/pingcap/tidb/issues/47161) @ [ドヴェーデン](https://github.com/dveeden)
    -   `approx_percentile`関数が TiDBpanic[＃40463](https://github.com/pingcap/tidb/issues/40463) @ [xzhangxian1008](https://github.com/xzhangxian1008)を引き起こす可能性がある問題を修正しました
    -   文字列関数の引数が`NULL`定数の場合に TiDB が暗黙的に`from_binary`関数を挿入し、一部の式がTiFlash [＃49526](https://github.com/pingcap/tidb/issues/49526) @ [ヤンケオ](https://github.com/YangKeao)にプッシュダウンできない問題を修正しました。
    -   `HashJoin`演算子がディスク[＃50841](https://github.com/pingcap/tidb/issues/50841) @ [wshwsh12](https://github.com/wshwsh12)にスピルできない場合に発生する可能性のある goroutine リークの問題を修正しました。
    -   `BIT`型の列が一部の関数の計算に関係する場合にデコード失敗によりクエリエラーが発生する可能性がある問題を修正しました[＃49566](https://github.com/pingcap/tidb/issues/49566) [＃50850](https://github.com/pingcap/tidb/issues/50850) [＃50855](https://github.com/pingcap/tidb/issues/50855) @ [ジフハスト](https://github.com/jiyfhust)
    -   CTEクエリのメモリ使用量が制限[＃50337](https://github.com/pingcap/tidb/issues/50337) @ [グオシャオゲ](https://github.com/guo-shaoge)を超えたときに発生するgoroutineリークの問題を修正しました
    -   TiFlash の遅延マテリアライゼーションが関連列[＃49241](https://github.com/pingcap/tidb/issues/49241) [＃51204](https://github.com/pingcap/tidb/issues/51204) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)を処理するときに間違った結果が返される可能性がある問題を修正しました
    -   TiDB が履歴統計[＃49076](https://github.com/pingcap/tidb/issues/49076) @ [ホーキングレイ](https://github.com/hawkingrei)を記録するときに TiDB のバックグラウンド ジョブ スレッドがpanicになる可能性がある問題を修正しました
    -   TiDBがパーティションテーブル[＃49023](https://github.com/pingcap/tidb/issues/49023) @ [ホーキングレイ](https://github.com/hawkingrei)のグローバル統計のヒストグラムをマージするときに発生する可能性のあるエラーを修正しました。
    -   パーティションが[＃49334](https://github.com/pingcap/tidb/issues/49334) @ [ハイ・ラスティン](https://github.com/Rustin170506)に削除された後、 `stats_meta`テーブルの履歴統計が更新されない問題を修正しました
    -   複数値インデックスが誤って`Index Join`プローブ側[＃50382](https://github.com/pingcap/tidb/issues/50382) @ [アイリンキッド](https://github.com/AilinKid)として選択されたために発生する誤ったクエリ結果の問題を修正しました。
    -   `USE_INDEX_MERGE`ヒントが複数値インデックス[＃50553](https://github.com/pingcap/tidb/issues/50553) @ [アイリンキッド](https://github.com/AilinKid)に効果がない問題を修正しました
    -   `INFORMATION_SCHEMA.ANALYZE_STATUS`システムテーブル[＃48835](https://github.com/pingcap/tidb/issues/48835) @ [ハイ・ラスティン](https://github.com/Rustin170506)をクエリするときにユーザーがエラーを受け取る可能性がある問題を修正しました
    -   TiDB が`group by` [＃38756](https://github.com/pingcap/tidb/issues/38756) @ [ハイ・ラスティン](https://github.com/Rustin170506)の定数値を誤って削除することによる間違ったクエリ結果の問題を修正しました
    -   テーブル上の`ANALYZE`タスクのうち`processed_rows`が、そのテーブルの合計行数[＃50632](https://github.com/pingcap/tidb/issues/50632) @ [ホーキングレイ](https://github.com/hawkingrei)を超える可能性がある問題を修正しました。
    -   `tidb_enable_prepared_plan_cache`システム変数が有効になってから無効になった後に`EXECUTE`ステートメントを使用して`PREPARE STMT`実行すると、TiDB がpanicになる可能性がある問題を修正しました[＃49344](https://github.com/pingcap/tidb/issues/49344) @ [qw4990](https://github.com/qw4990)
    -   クエリで`NATURAL JOIN` [＃32044](https://github.com/pingcap/tidb/issues/32044) @ [アイリンキッド](https://github.com/AilinKid)が使用される場合に発生する可能性のある`Column ... in from clause is ambiguous`エラーを修正します
    -   複数値インデックスを使用して空の JSON 配列にアクセスすると、誤った結果が返される可能性がある問題を修正しました[＃50125](https://github.com/pingcap/tidb/issues/50125) @ [ヤンケオ](https://github.com/YangKeao)
    -   集計関数をグループ計算に使用すると発生する可能性のある`Can't find column ...`エラーを修正[＃50926](https://github.com/pingcap/tidb/issues/50926) @ [qw4990](https://github.com/qw4990)
    -   文字列型の変数に対する`SET_VAR`の制御が無効になる可能性がある問題を修正[＃50507](https://github.com/pingcap/tidb/issues/50507) @ [qw4990](https://github.com/qw4990)
    -   `tidb_server_memory_limit` [＃48741](https://github.com/pingcap/tidb/issues/48741) @ [徐淮嶼](https://github.com/XuHuaiyu)による長期メモリ圧迫により TiDB の CPU 使用率が上昇する問題を修正
    -   依存関係のある 2 つの DDL タスクの完了時間が[＃49498](https://github.com/pingcap/tidb/issues/49498) @ [接線](https://github.com/tangenta)と誤って順序付けられる問題を修正しました。
    -   無効なオプティマイザヒントによって有効なヒントが無効になる可能性がある問題を修正[＃49308](https://github.com/pingcap/tidb/issues/49308) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `CHECK`制約の DDL 文が[＃47632](https://github.com/pingcap/tidb/issues/47632) @ [ジフハスト](https://github.com/jiyfhust)でスタックする問題を修正しました
    -   `CHECK`制約の`ENFORCED`オプションの動作がMySQL 8.0 [＃47567](https://github.com/pingcap/tidb/issues/47567) [＃47631](https://github.com/pingcap/tidb/issues/47631) @ [ジフハスト](https://github.com/jiyfhust)と一致しない問題を修正
    -   CTEクエリが再試行プロセス[＃46522](https://github.com/pingcap/tidb/issues/46522) @ [天菜麻緒](https://github.com/tiancaiamao)中にエラー`type assertion for CTEStorageMap failed`を報告する可能性がある問題を修正しました
    -   `tidb_multi_statement_mode`モードが有効になっている場合、インデックス検索を使用する`DELETE`および`UPDATE`ステートメントでエラーが報告される可能性がある問題を修正しました[＃50012](https://github.com/pingcap/tidb/issues/50012) @ [接線](https://github.com/tangenta)
    -   `WITH RECURSIVE` CTE を含む`UPDATE`または`DELETE`ステートメントで誤った結果が生成される可能性がある問題を修正しました[＃48969](https://github.com/pingcap/tidb/issues/48969) @ [ウィノロス](https://github.com/winoros)
    -   特定のシナリオ[＃49285](https://github.com/pingcap/tidb/issues/49285) @ [アイリンキッド](https://github.com/AilinKid)でオプティマイザがTiFlash選択パスを DUAL テーブルに誤って変換する問題を修正しました
    -   同じクエリプランで、場合によっては[＃47634](https://github.com/pingcap/tidb/issues/47634) @ [キング・ディラン](https://github.com/King-Dylan)の`PLAN_DIGEST`値が異なる問題を修正しました
    -   自動統計更新の時間枠を設定した後、その時間枠外でも統計が更新される可能性がある問題を修正[＃49552](https://github.com/pingcap/tidb/issues/49552) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `ENUM`型の列を結合キー[＃48991](https://github.com/pingcap/tidb/issues/48991) @ [ウィノロス](https://github.com/winoros)として使用した場合にクエリ結果が正しくない問題を修正しました
    -   `ORDER BY`句で`UNIQUE`インデックス検索を実行するとエラー[＃49920](https://github.com/pingcap/tidb/issues/49920) @ [ジャッキーsp](https://github.com/jackysp)が発生する可能性がある問題を修正しました
    -   複数レベルのネストされた`UNION`クエリの`LIMIT`無効になる可能性がある問題を修正しました[＃49874](https://github.com/pingcap/tidb/issues/49874) @ [定義2014](https://github.com/Defined2014)
    -   MPPで計算された`COUNT(INT)`の結果が正しくない可能性がある問題を修正[＃48643](https://github.com/pingcap/tidb/issues/48643) @ [アイリンキッド](https://github.com/AilinKid)
    -   `ENUM`または`SET`種類の無効な値を解析すると、SQL ステートメント エラー[＃49487](https://github.com/pingcap/tidb/issues/49487) @ [ウィノロス](https://github.com/winoros)が直接発生する問題を修正しました。
    -   TiDBがパニックを起こしてエラーを報告する問題を修正`invalid memory address or nil pointer dereference` [＃42739](https://github.com/pingcap/tidb/issues/42739) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)
    -   最初のサブノードとしてDUALテーブルを使用して`UNION ALL`実行すると、エラー[＃48755](https://github.com/pingcap/tidb/issues/48755) @ [ウィノロス](https://github.com/winoros)が発生する可能性がある問題を修正しました。
    -   共通ヒントが`UNION ALL`文[＃50068](https://github.com/pingcap/tidb/issues/50068) @ [ホーキングレイ](https://github.com/hawkingrei)で有効にならない問題を修正
    -   正常なシャットダウン中に TiDBサーバーがpanic可能性がある問題を修正[＃36793](https://github.com/pingcap/tidb/issues/36793) @ [bb7133](https://github.com/bb7133)
    -   一部のタイムゾーン[＃49586](https://github.com/pingcap/tidb/issues/49586) @ [金星の上](https://github.com/overvenus)で夏時間が正しく表示されない問題を修正
    -   静的`CALIBRATE RESOURCE` Prometheusデータ[＃49174](https://github.com/pingcap/tidb/issues/49174) @ [栄光](https://github.com/glorv)に依存している問題を修正
    -   `REPLACE INTO`文[＃34325](https://github.com/pingcap/tidb/issues/34325) @ [ヤンケオ](https://github.com/YangKeao)でヒントが使用できない問題を修正
    -   `GROUP_CONCAT(ORDER BY)`構文を含むクエリを実行するとエラー[＃49986](https://github.com/pingcap/tidb/issues/49986) @ [アイリンキッド](https://github.com/AilinKid)が返される可能性がある問題を修正しました
    -   監査ログ用のエンタープライズプラグインを使用すると、TiDBサーバーが大量のリソースを消費する可能性がある問題を修正しました[＃49273](https://github.com/pingcap/tidb/issues/49273) @ [lcwangchao](https://github.com/lcwangchao)
    -   古いインターフェースを使用するとテーブル[＃49751](https://github.com/pingcap/tidb/issues/49751) @ [ホーキングレイ](https://github.com/hawkingrei)のメタデータに不整合が発生する可能性がある問題を修正しました。
    -   `tidb_enable_collect_execution_info`を無効にするとコプロセッサキャッシュがpanicになる問題を修正[＃48212](https://github.com/pingcap/tidb/issues/48212) @ [あなた06](https://github.com/you06)
    -   パーティション列タイプが`DATETIME` [＃48814](https://github.com/pingcap/tidb/issues/48814) @ [crazycs520](https://github.com/crazycs520)の場合に`ALTER TABLE ... LAST PARTITION`実行が失敗する問題を修正しました
    -   `COM_STMT_EXECUTE`まで実行された`COMMIT`または`ROLLBACK`操作が、タイムアウトしたトランザクションを[＃49151](https://github.com/pingcap/tidb/issues/49151) @ [ジグアン](https://github.com/zyguan)で終了できない問題を修正しました。
    -   ヒストグラムの境界に`NULL` [＃49823](https://github.com/pingcap/tidb/issues/49823) @ [アイリンキッド](https://github.com/AilinKid)が含まれている場合、ヒストグラム統計が読み取り可能な文字列に解析されない可能性がある問題を修正しました。
    -   共通テーブル式 (CTE) を含むクエリがメモリ制限を超えたときに予期せず停止する問題を修正[＃49096](https://github.com/pingcap/tidb/issues/49096) @ [アイリンキッド](https://github.com/AilinKid)
    -   DDL所有者がネットワークから分離されている[＃49773](https://github.com/pingcap/tidb/issues/49773) @ [接線](https://github.com/tangenta)の後に`ADD INDEX`実行すると、TiDB分散実行フレームワーク（DXF）でデータが不整合になる問題を修正しました
    -   `AUTO_ID_CACHE=1` [＃50519](https://github.com/pingcap/tidb/issues/50519) @ [天菜麻緒](https://github.com/tiancaiamao)の自動インクリメント列を使用すると同時競合により自動インクリメント ID 割り当てでエラーが報告される問題を修正しました。
    -   クエリに Apply 演算子が含まれており、 `fatal error: concurrent map writes`エラーが[＃50347](https://github.com/pingcap/tidb/issues/50347) @ [シーライズ](https://github.com/SeaRise)で発生すると TiDB がpanicになる可能性がある問題を修正しました。
    -   DDL `jobID` 0 [＃46296](https://github.com/pingcap/tidb/issues/46296) @ [ジフハスト](https://github.com/jiyfhust)に復元されたときに発生する TiDB ノードpanicの問題を修正しました
    -   `STREAM_AGG()` CI [＃49902](https://github.com/pingcap/tidb/issues/49902) @ [wshwsh12](https://github.com/wshwsh12)を誤って処理したためにクエリ結果が正しくない問題を修正しました
    -   多数のテーブルまたはパーティション[＃50077](https://github.com/pingcap/tidb/issues/50077) @ [ジムララ](https://github.com/zimulala)を処理するときに TiDB ノードが OOM エラーに遭遇する可能性がある問題を軽減します。
    -   `LEADING`ヒントが`UNION ALL`ステートメント[＃50067](https://github.com/pingcap/tidb/issues/50067) @ [ホーキングレイ](https://github.com/hawkingrei)で有効にならない問題を修正しました
    -   ネストされた`UNION`のクエリ[＃49377](https://github.com/pingcap/tidb/issues/49377) @ [アイリンキッド](https://github.com/AilinKid)で`LIMIT`と`OPRDERBY`無効になる可能性がある問題を修正しました
    -   メモリが`tidb_mem_quota_query` [＃49033](https://github.com/pingcap/tidb/issues/49033) @ [徐淮嶼](https://github.com/XuHuaiyu)を超えると IndexHashJoin 演算子を含むクエリが停止する問題を修正しました
    -   定数伝播[＃49440](https://github.com/pingcap/tidb/issues/49440) @ [ウィノロス](https://github.com/winoros)で`ENUM`または`SET`型を処理するときに TiDB が間違ったクエリ結果を返す問題を修正しました
    -   `PREPARE`メソッドを使用して`SELECT INTO OUTFILE`実行すると、エラー[＃49166](https://github.com/pingcap/tidb/issues/49166) @ [qw4990](https://github.com/qw4990)ではなく、誤って成功メッセージが返される問題を修正しました。
    -   クエリがソートを強制するオプティマイザヒント（ `STREAM_AGG()`など）を使用し、その実行プランに`IndexMerge` [＃49605](https://github.com/pingcap/tidb/issues/49605) @ [アイリンキッド](https://github.com/AilinKid)が含まれている場合、強制ソートが無効になる可能性がある問題を修正しました。
    -   テーブルが[＃48869](https://github.com/pingcap/tidb/issues/48869) @ [天菜麻緒](https://github.com/tiancaiamao)と多数ある場合に、テーブルが`AUTO_ID_CACHE=1`の場合に gRPC クライアント リークが発生する可能性がある問題を修正しました。
    -   非厳密モード（ `sql_mode = ''` ）で、 `INSERT`実行中に切り捨てが行われても、 [天菜麻緒](https://github.com/tiancaiamao)でエラー[＃49369](https://github.com/pingcap/tidb/issues/49369)が報告される問題を修正しました。
    -   データの末尾にスペースが含まれている場合に`LIKE`で`_`ワイルドカードを使用すると、誤ったクエリ結果[＃48983](https://github.com/pingcap/tidb/issues/48983) @ [時間と運命](https://github.com/time-and-fate)が返される可能性がある問題を修正しました
    -   `tidb_mem_quota_query`システム変数を更新した後に`ADMIN CHECK`実行すると`ERROR 8175` [＃49258](https://github.com/pingcap/tidb/issues/49258) @ [接線](https://github.com/tangenta)が返される問題を修正しました
    -   Golang の暗黙的な変換アルゴリズム[＃49801](https://github.com/pingcap/tidb/issues/49801) @ [qw4990](https://github.com/qw4990)によって発生する統計情報の構築における過剰な統計エラーの問題を修正しました
    -   CTE を含むクエリが、 `tidb_max_chunk_size`小さい値[＃48808](https://github.com/pingcap/tidb/issues/48808) @ [グオシャオゲ](https://github.com/guo-shaoge)に設定されている場合に`runtime error: index out of range [32] with length 32`報告する問題を修正しました。

-   TiKV

    -   `tidb_enable_row_level_checksum`有効にすると TiKV がpanicを起こす可能性がある問題を修正[＃16371](https://github.com/tikv/tikv/issues/16371) @ [cfzjywxk](https://github.com/cfzjywxk)
    -   gRPC スレッドが`is_shutdown` [＃16236](https://github.com/tikv/tikv/issues/16236) @ [ピンギュ](https://github.com/pingyu)をチェックしているときに TiKV がpanic可能性がある問題を修正しました
    -   TiKVがブラジルとエジプトのタイムゾーンを誤って変換する問題を修正[＃16220](https://github.com/tikv/tikv/issues/16220) @ [金星の上](https://github.com/overvenus)
    -   Titanの`blob-run-mode`オンライン[＃15978](https://github.com/tikv/tikv/issues/15978) @ [トニーシュキ](https://github.com/tonyxuqqi)に更新できない問題を修正
    -   `DECIMAL`算術乗算切り捨て[＃16268](https://github.com/tikv/tikv/issues/16268) @ [ソロツグ](https://github.com/solotzg)を処理するときに TiDB と TiKV が矛盾した結果を生成する可能性がある問題を修正しました
    -   `notLeader`または`regionNotFound` [＃15712](https://github.com/tikv/tikv/issues/15712) @ [HuSharp](https://github.com/HuSharp)に遭遇するとフラッシュバックが停止する可能性がある問題を修正しました
    -   破損したSSTファイルが他のTiKVノード[＃15986](https://github.com/tikv/tikv/issues/15986) @ [コナー1996](https://github.com/Connor1996)に広がる可能性がある問題を修正
    -   TiKV の実行速度が非常に遅い場合、リージョン[＃16111](https://github.com/tikv/tikv/issues/16111)と[金星の上](https://github.com/overvenus)マージ後にpanicする可能性がある問題を修正しました。
    -   [＃15817](https://github.com/tikv/tikv/issues/15817) @ [コナー1996](https://github.com/Connor1996)にスケールアウトするときに DR 自動同期のジョイント状態がタイムアウトする可能性がある問題を修正しました
    -   解決済みのTSが2時間ブロックされる可能性がある問題を修正[＃11847](https://github.com/tikv/tikv/issues/11847) [＃15520](https://github.com/tikv/tikv/issues/15520) [＃39130](https://github.com/pingcap/tidb/issues/39130) @ [金星の上](https://github.com/overvenus)
    -   `cast_duration_as_time`誤った結果を返す可能性がある問題を修正[＃16211](https://github.com/tikv/tikv/issues/16211) @ [ゲンリキ](https://github.com/gengliqi)
    -   コーナーケース（ディスクI/O操作がブロックされている場合など）でTiKVがハングし、可用性[＃16368](https://github.com/tikv/tikv/issues/16368) @ [LykxSassinator](https://github.com/LykxSassinator)に影響する問題を修正しました。

-   PD

    -   リソース グループをバッチでクエリすると PD がpanic[＃7206](https://github.com/tikv/pd/issues/7206) @ [ノルーシュ](https://github.com/nolouch)になる可能性がある問題を修正しました
    -   PDが`systemd` [＃7628](https://github.com/tikv/pd/issues/7628) @ [バッファフライ](https://github.com/bufferflies)で起動したときにリソース制限を読み取れない問題を修正
    -   PD ディスクレイテンシーの継続的なジッタにより、PD が新しいリーダー[＃7251](https://github.com/tikv/pd/issues/7251) @ [HuSharp](https://github.com/HuSharp)を選択できない可能性がある問題を修正しました。
    -   PD のネットワーク パーティションにより、スケジュールがすぐに開始されない可能性がある問題を修正[＃7016](https://github.com/tikv/pd/issues/7016) @ [HuSharp](https://github.com/HuSharp)
    -   リーダースイッチ[＃7728](https://github.com/tikv/pd/issues/7728) @ [キャビンフィーバーB](https://github.com/CabinfeverB)後にPD監視項目`learner-peer-count`古い値を同期しない問題を修正
    -   PDリーダーが転送され、新しいリーダーとPDクライアントの間にネットワークパーティションがある場合、PDクライアントがリーダー[＃7416](https://github.com/tikv/pd/issues/7416) @ [キャビンフィーバーB](https://github.com/CabinfeverB)の情報を更新できない問題を修正しました。
    -   Gin Web Framework のバージョンを v1.8.1 から v1.9.1 にアップグレードして、いくつかのセキュリティ問題を修正しました[＃7438](https://github.com/tikv/pd/issues/7438) @ [ニューベル](https://github.com/niubell)
    -   レプリカ数が要件[＃7584](https://github.com/tikv/pd/issues/7584) @ [バッファフライ](https://github.com/bufferflies)を満たしていない場合に孤立ピアが削除される問題を修正しました
    -   `pd-ctl`を使用してリーダーのないリージョンを照会すると、PD が[＃7630](https://github.com/tikv/pd/issues/7630) @ [rleungx](https://github.com/rleungx)でpanicになる可能性がある問題を修正しました。

-   TiFlash

    -   レプリカ移行[＃8323](https://github.com/pingcap/tiflash/issues/8323) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)中に PD とのネットワーク接続が不安定になり、 TiFlash がpanic可能性がある問題を修正しました
    -   TiFlashレプリカを削除して再度追加すると、 TiFlash [＃8695](https://github.com/pingcap/tiflash/issues/8695) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)でデータ破損が発生する可能性がある問題を修正しました。
    -   `DROP TABLE`データ挿入[＃8395](https://github.com/pingcap/tiflash/issues/8395) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)の直後に実行されると、 `FLASHBACK TABLE`または`RECOVER TABLE`一部のTiFlashレプリカのデータを回復できない可能性がある潜在的な問題を修正しました。
    -   Grafana [＃8076](https://github.com/pingcap/tiflash/issues/8076) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)の一部のパネルの最大パーセンタイル時間の表示が誤っていた問題を修正
    -   リモート読み取り[＃8685](https://github.com/pingcap/tiflash/issues/8685) @ [グオシャオゲ](https://github.com/guo-shaoge)中にTiFlashがクラッシュする可能性がある問題を修正
    -   `ENUM`値が 0 [＃8311](https://github.com/pingcap/tiflash/issues/8311) @ [ソロツグ](https://github.com/solotzg)の場合にTiFlash が`ENUM`誤って処理する問題を修正しました
    -   短いクエリが正常に実行され、過剰な情報ログ[＃8592](https://github.com/pingcap/tiflash/issues/8592) @ [ウィンドトーカー](https://github.com/windtalker)が出力される問題を修正しました。
    -   クエリ[＃8564](https://github.com/pingcap/tiflash/issues/8564) @ [ジンヘリン](https://github.com/JinheLin)の低速化によりメモリ使用量が大幅に増加する問題を修正
    -   `lowerUTF8`と`upperUTF8`関数で、大文字と小文字が異なるバイト[＃8484](https://github.com/pingcap/tiflash/issues/8484) @ [ゲンリチ](https://github.com/gengliqi)を占めることができない問題を修正しました。
    -   ストリーム読み取り[＃8505](https://github.com/pingcap/tiflash/issues/8505) @ [ゲンリチ](https://github.com/gengliqi)中に複数のパーティション テーブルをスキャンするときに発生する可能性のある OOM 問題を修正しました。
    -   クエリ[＃8447](https://github.com/pingcap/tiflash/issues/8447) @ [ジンヘリン](https://github.com/JinheLin)中にTiFlash がメモリ制限に遭遇した場合のメモリリークの問題を修正しました
    -   TiFlash が同時 DDL 実行中に競合に遭遇した場合のTiFlashpanic問題を修正[＃8578](https://github.com/pingcap/tiflash/issues/8578) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   `ALTER TABLE ... MODIFY COLUMN ... NOT NULL`実行した後にTiFlash がパニックを起こし、null 許容列が[＃8419](https://github.com/pingcap/tiflash/issues/8419) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)に非 null 許容に変更される問題を修正しました。
    -   `ColumnRef in (Literal, Func...)` [＃8631](https://github.com/pingcap/tiflash/issues/8631) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)のようなフィルタリング条件でクエリを実行したときにクエリ結果が正しくない問題を修正しました
    -   `FLASHBACK DATABASE` [＃8450](https://github.com/pingcap/tiflash/issues/8450) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を実行した後もTiFlashレプリカのデータがガベージコレクションされる問題を修正しました
    -   分散storageおよびコンピューティングアーキテクチャ[＃8519](https://github.com/pingcap/tiflash/issues/8519) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)で、 TiFlash がオブジェクトstorageデータの GC 所有者を選択できない可能性がある問題を修正しました。
    -   定数文字列パラメータ[＃8604](https://github.com/pingcap/tiflash/issues/8604) @ [ウィンドトーカー](https://github.com/windtalker)を含む`GREATEST`または`LEAST`関数で発生する可能性のある、ランダムに無効なメモリアクセスの問題を修正しました。
    -   ポイントインタイムリカバリ（PITR）を実行した後、または`FLASHBACK CLUSTER TO`実行した後にTiFlashレプリカデータが誤って削除され、データ異常[＃8777](https://github.com/pingcap/tiflash/issues/8777) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)が発生する可能性がある問題を修正しました。
    -   結合に非等価条件[＃8791](https://github.com/pingcap/tiflash/issues/8791) @ [ウィンドトーカー](https://github.com/windtalker)が含まれている場合に、 TiFlash Anti Semi Join が誤った結果を返す可能性がある問題を修正しました。

-   ツール

    -   バックアップと復元 (BR)

        -   TiKVノード[＃50566](https://github.com/pingcap/tidb/issues/50566) @ [リーヴルス](https://github.com/Leavrth)にリーダーがいないためにデータの復元が遅くなる問題を修正しました
        -   `--filter`オプションを指定した後でも、完全な復元を行うにはターゲット クラスターが空である必要があるという問題を修正しました[＃51009](https://github.com/pingcap/tidb/issues/51009) @ [3ポイントシュート](https://github.com/3pointer)
        -   データの復元に失敗した後、チェックポイントから再開するとエラー`the target cluster is not fresh`が発生する問題を修正しました[＃50232](https://github.com/pingcap/tidb/issues/50232) @ [リーヴルス](https://github.com/Leavrth)
        -   ログバックアップタスクを停止すると TiDB がクラッシュする問題を修正[＃50839](https://github.com/pingcap/tidb/issues/50839) @ [ユジュンセン](https://github.com/YuJuncen)
        -   古いバージョン[＃49466](https://github.com/pingcap/tidb/issues/49466) @ [3ポイントシュート](https://github.com/3pointer)のバックアップからデータを復元するときに`Unsupported collation`エラーが報告される問題を修正しました
        -   タスク初期化中にPDへの接続に失敗すると、ログバックアップタスクは開始できるが正常に動作しない問題を修正[＃16056](https://github.com/tikv/tikv/issues/16056) @ [ユジュンセン](https://github.com/YuJuncen)
        -   BRが外部storageファイル[＃48452](https://github.com/pingcap/tidb/issues/48452) @ [3エースショーハンド](https://github.com/3AceShowHand)に対して誤ったURIを生成する問題を修正
        -   同じノード[＃50445](https://github.com/pingcap/tidb/issues/50445) @ [3ポイントシュート](https://github.com/3pointer)で TiKV IP アドレスを変更した後にログ バックアップが停止する問題を修正しました
        -   S3 [＃49942](https://github.com/pingcap/tidb/issues/49942) @ [リーヴルス](https://github.com/Leavrth)からファイル コンテンツを読み取っているときにエラーが発生した場合にBR が再試行できない問題を修正しました

    -   TiCDC

        -   Syncpoint が有効な場合にエラーが発生し、シンクモジュールが正常に再起動しない問題を修正 ( `enable-sync-point = true` ) [＃10091](https://github.com/pingcap/tiflow/issues/10091) @ [ヒック](https://github.com/hicqu)
        -   storageシンク[＃10352](https://github.com/pingcap/tiflow/issues/10352) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)の使用時に、storageサービスによって生成されたファイルシーケンス番号が正しく増加しない可能性がある問題を修正しました。
        -   同期ポイントテーブルが誤って複製される可能性がある問題を修正[＃10576](https://github.com/pingcap/tiflow/issues/10576) @ [アズドンメン](https://github.com/asddongmen)
        -   Apache Pulsarをダウンストリーム[＃10602](https://github.com/pingcap/tiflow/issues/10602) @ [アズドンメン](https://github.com/asddongmen)として使用すると、OAuth2.0、TLS、mTLSが正しく有効化できない問題を修正
        -   複数のチェンジフィード[＃10430](https://github.com/pingcap/tiflow/issues/10430) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)を同時に作成すると TiCDC が`ErrChangeFeedAlreadyExists`エラーを返す問題を修正しました
        -   極端なケースでチェンジフィード`resolved ts`が進まない問題を修正[＃10157](https://github.com/pingcap/tiflow/issues/10157) @ [スドジ](https://github.com/sdojjy)
        -   特定の特殊なシナリオで TiCDC が TiKV との接続を誤って閉じる問題を修正[＃10239](https://github.com/pingcap/tiflow/issues/10239) @ [ヒック](https://github.com/hicqu)
        -   オブジェクトstorageサービス[＃10137](https://github.com/pingcap/tiflow/issues/10137) @ [スドジ](https://github.com/sdojjy)にデータを複製するときに TiCDCサーバーがpanic可能性がある問題を修正しました
        -   アップストリームテーブル[＃10522](https://github.com/pingcap/tiflow/issues/10522) @ [スドジ](https://github.com/sdojjy)で`TRUNCATE PARTITION`を実行した後に、changefeed がエラーを報告する問題を修正しました。
        -   `ignore-event`で`add table partition`イベントをフィルタリングするように設定した後、TiCDC が関連パーティションの他のタイプの DML 変更をダウンストリーム[＃10524](https://github.com/pingcap/tiflow/issues/10524) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)に複製しない問題を修正しました。
        -   `kv-client`初期化[＃10095](https://github.com/pingcap/tiflow/issues/10095) @ [3エースショーハンド](https://github.com/3AceShowHand)中に発生する可能性のあるデータ競合問題を修正

    -   TiDB データ移行 (DM)

        -   下流のテーブル構造に`shard_row_id_bits` [＃10308](https://github.com/pingcap/tiflow/issues/10308) @ [GMHDBJD](https://github.com/GMHDBJD)が含まれている場合に移行タスクエラーが発生する問題を修正しました
        -   DM が「イベント タイプ切り捨てが無効です」というエラーに遭遇し、アップグレードが失敗する問題を修正しました[＃10282](https://github.com/pingcap/tiflow/issues/10282) @ [GMHDBJD](https://github.com/GMHDBJD)
