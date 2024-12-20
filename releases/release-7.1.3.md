---
title: TiDB 7.1.3 Release Notes
summary: TiDB 7.1.3 の互換性の変更、改善、バグ修正について説明します。
---

# TiDB 7.1.3 リリースノート {#tidb-7-1-3-release-notes}

発売日: 2023年12月21日

TiDB バージョン: 7.1.3

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [実稼働環境への導入](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   さらにテストを行った結果、 TiCDC Changefeed構成項目[`case-sensitive`](/ticdc/ticdc-changefeed-config.md)のデフォルト値が`true`から`false`に変更されました。つまり、デフォルトでは、TiCDC 構成ファイル内のテーブル名とデータベース名は大文字と小文字が区別されません[＃10047](https://github.com/pingcap/tiflow/issues/10047) @ [スドジ](https://github.com/sdojjy)
-   TiCDC Changefeed、次の新しい構成項目が導入されています。
    -   [`sql-mode`](/ticdc/ticdc-changefeed-config.md) : TiCDC がデータを複製するときに DDL ステートメントを解析するために使用する[SQL モード](https://docs.pingcap.com/tidb/v7.1/ticdc-ddl#sql-mode)を設定できます[＃9876](https://github.com/pingcap/tiflow/issues/9876) @ [アズドンメン](https://github.com/asddongmen)
    -   [`encoding-worker-num`](/ticdc/ticdc-changefeed-config.md)と[`flush-worker-num`](/ticdc/ticdc-changefeed-config.md) : 異なるマシンの仕様に基づいて、再実行モジュールの異なる同時実行パラメータを設定できます[＃10048](https://github.com/pingcap/tiflow/issues/10048) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
    -   [`compression`](/ticdc/ticdc-changefeed-config.md) : REDOログファイルの圧縮動作を設定できます[＃10176](https://github.com/pingcap/tiflow/issues/10176) @ [スドジ](https://github.com/sdojjy)
    -   [`sink.cloud-storage-config`](/ticdc/ticdc-changefeed-config.md) : オブジェクトstorageにデータを複製するときに履歴データの自動クリーンアップを設定できます[＃10109](https://github.com/pingcap/tiflow/issues/10109) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)

## 改善点 {#improvements}

-   ティビ

    -   [`FLASHBACK CLUSTER TO TSO`](https://docs.pingcap.com/tidb/v7.1/sql-statement-flashback-cluster)構文[＃48372](https://github.com/pingcap/tidb/issues/48372) @ [ボーンチェンジャー](https://github.com/BornChanger)をサポート

-   PD

    -   リソース制御クライアントの構成取得方法を強化し、最新の構成を動的に取得する[＃7043](https://github.com/tikv/pd/issues/7043) @ [ノルーシュ](https://github.com/nolouch)

-   ツール

    -   バックアップと復元 (BR)

        -   タイムアウトエラーまたはリージョンスキャッタ[＃47236](https://github.com/pingcap/tidb/issues/47236) @ [リーヴルス](https://github.com/Leavrth)のキャンセルが発生した場合に、スナップショットリカバリ中にリージョンスキャッタの自動再試行を有効にする
        -   スナップショットバックアップの復元中に、 BR は特定のネットワークエラーが発生すると再試行します[＃48528](https://github.com/pingcap/tidb/issues/48528) @ [リーヴルス](https://github.com/Leavrth)
        -   `delete range`シナリオでポイントインタイムリカバリ (PITR) の新しい統合テストを導入し、PITR の安定性を向上[＃47738](https://github.com/pingcap/tidb/issues/47738) @ [リーヴルス](https://github.com/Leavrth)

    -   ティCDC

        -   TiCDCノードがTiDB [＃9935](https://github.com/pingcap/tiflow/issues/9935) @ [3エースショーハンド](https://github.com/3AceShowHand)にデータを複製する際のメモリ消費を最適化します
        -   いくつかのアラームルールを最適化[＃9266](https://github.com/pingcap/tiflow/issues/9266) @ [アズドンメン](https://github.com/asddongmen)
        -   S3へのデータの並列書き込みやlz4圧縮アルゴリズムの採用など、REDOログのパフォーマンスを最適化します[＃10176](https://github.com/pingcap/tiflow/issues/10176) [＃10226](https://github.com/pingcap/tiflow/issues/10226) @ [スドジ](https://github.com/sdojjy)
        -   並列処理[＃10098](https://github.com/pingcap/tiflow/issues/10098) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)を増やすことで、TiCDC がオブジェクトstorageにデータを複製する際のパフォーマンスが向上します。
        -   TiCDC 増分スキャンによる上流 TiKV [＃11390](https://github.com/tikv/tikv/issues/11390) @ [ヒック](https://github.com/hicqu)への影響を軽減
        -   `sink-uri`構成[＃10106](https://github.com/pingcap/tiflow/issues/10106) @ [3エースショーハンド](https://github.com/3AceShowHand)で`content-compatible=true`設定することにより、 TiCDC Canal-JSON コンテンツ形式[公式Canal出力のコンテンツフォーマットと互換性がある](https://docs.pingcap.com/tidb/v6.5/ticdc-canal-json#compatibility-with-the-official-canal)の作成をサポートします。

    -   TiDB Lightning

        -   PDリーダーの変更による`GetTS`失敗に対して再試行メカニズムを追加[＃45301](https://github.com/pingcap/tidb/issues/45301) @ [ランス6716](https://github.com/lance6716)

## バグ修正 {#bug-fixes}

-   ティビ

    -   メモリ制限を超えると、共通テーブル式 (CTE) を含むクエリが予期せず停止する問題を修正[＃49096](https://github.com/pingcap/tidb/issues/49096) @ [アイリンキッド](https://github.com/AilinKid)
    -   `tidb_server_memory_limit` [＃48741](https://github.com/pingcap/tidb/issues/48741) @ [徐懐玉](https://github.com/XuHuaiyu)による長期メモリ圧迫により TiDB の CPU 使用率が高くなる問題を修正
    -   CTE を含むクエリで、 `tidb_max_chunk_size`小さい値[＃48808](https://github.com/pingcap/tidb/issues/48808) @ [グオシャオゲ](https://github.com/guo-shaoge)に設定されている場合に`runtime error: index out of range [32] with length 32`報告される問題を修正しました。
    -   `ENUM`型の列を結合キー[＃48991](https://github.com/pingcap/tidb/issues/48991) @ [ウィノロス](https://github.com/winoros)として使用した場合にクエリ結果が正しくない問題を修正
    -   再帰 CTE [＃47711](https://github.com/pingcap/tidb/issues/47711) @ [エルサ0520](https://github.com/elsa0520)の集計関数またはウィンドウ関数によって発生する解析エラーを修正
    -   `UPDATE`文が誤って PointGet [＃47445](https://github.com/pingcap/tidb/issues/47445) @ [ハイラスティン](https://github.com/Rustin170506)に変換される可能性がある問題を修正しました
    -   TiDBが`stats_history`テーブル[＃48431](https://github.com/pingcap/tidb/issues/48431) @ [ホーキングレイ](https://github.com/hawkingrei)でガベージコレクションを実行するときに発生する可能性のあるOOM問題を修正しました。
    -   同じクエリプランで`PLAN_DIGEST`値が[＃47634](https://github.com/pingcap/tidb/issues/47634) @ [キング・ディラン](https://github.com/King-Dylan)の場合に異なる問題を修正
    -   `GenJSONTableFromStats`大量のメモリを消費すると強制終了できない問題を修正[＃47779](https://github.com/pingcap/tidb/issues/47779) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   述語が共通テーブル式[＃47881](https://github.com/pingcap/tidb/issues/47881) @ [ウィノロス](https://github.com/winoros)にプッシュダウンされたときに結果が不正確になる可能性がある問題を修正しました
    -   `AUTO_ID_CACHE=1`が[＃46444](https://github.com/pingcap/tidb/issues/46444) @ [天菜まお](https://github.com/tiancaiamao)に設定されている場合に`Duplicate entry`発生する可能性がある問題を修正しました
    -   監査ログ用のエンタープライズプラグインを使用すると、TiDBサーバーが大量のリソースを消費する可能性がある問題を修正[＃49273](https://github.com/pingcap/tidb/issues/49273) @ [lcwangchao](https://github.com/lcwangchao)
    -   正常なシャットダウン中に TiDBサーバーがpanicになる可能性がある問題を修正[＃36793](https://github.com/pingcap/tidb/issues/36793) @ [bb7133](https://github.com/bb7133)
    -   テーブルが[＃48869](https://github.com/pingcap/tidb/issues/48869) @ [天菜まお](https://github.com/tiancaiamao)と多数ある場合に、テーブルが`AUTO_ID_CACHE=1`の場合に gRPC クライアント リークが発生する可能性がある問題を修正しました。
    -   `ErrLoadDataInvalidURI`の誤ったエラー メッセージを修正 (無効な S3 URI エラー) [＃48164](https://github.com/pingcap/tidb/issues/48164) @ [ランス6716](https://github.com/lance6716)
    -   パーティション列タイプが`DATETIME` [＃48814](https://github.com/pingcap/tidb/issues/48814) @ [クレイジーcs520](https://github.com/crazycs520)の場合に`ALTER TABLE ... LAST PARTITION`実行が失敗する問題を修正
    -   `IMPORT INTO`実行中の実際のエラーメッセージが他のエラーメッセージによって上書きされる可能性がある問題を修正[＃47992](https://github.com/pingcap/tidb/issues/47992) [＃47781](https://github.com/pingcap/tidb/issues/47781) @ [D3ハンター](https://github.com/D3Hunter)
    -   cgroup v2コンテナにデプロイされたTiDBが検出できない問題を修正[＃48342](https://github.com/pingcap/tidb/issues/48342) @ [D3ハンター](https://github.com/D3Hunter)
    -   最初のサブノードとしてDUALテーブルを使用して`UNION ALL`実行するとエラー[＃48755](https://github.com/pingcap/tidb/issues/48755) @ [ウィノロス](https://github.com/winoros)が発生する可能性がある問題を修正しました
    -   DDL `jobID`が 0 [＃46296](https://github.com/pingcap/tidb/issues/46296) @ [ジフハウス](https://github.com/jiyfhust)に復元されたときに発生する TiDB ノードpanicの問題を修正しました。
    -   `TABLESAMPLE` [＃48253](https://github.com/pingcap/tidb/issues/48253) @ [タンジェンタ](https://github.com/tangenta)によって返される未ソートの行データの問題を修正
    -   `tidb_enable_ordered_result_mode`が有効になっている場合にpanicが発生する可能性がある問題を修正[＃45044](https://github.com/pingcap/tidb/issues/45044) @ [qw4990](https://github.com/qw4990)
    -   ウィンドウ関数[＃46177](https://github.com/pingcap/tidb/issues/46177) @ [qw4990](https://github.com/qw4990)によって導入されたソートを減らすために、オプティマイザが誤って IndexFullScan を選択する問題を修正しました。
    -   TiDB スキーマ キャッシュ[＃48281](https://github.com/pingcap/tidb/issues/48281) @ [翻訳](https://github.com/cfzjywxk)からスキーマ diff コミット バージョンを読み取るときに MVCC インターフェイスでロックが処理されない問題を修正しました。
    -   `INDEX_LOOKUP_HASH_JOIN` [＃47788](https://github.com/pingcap/tidb/issues/47788) @ [シーライズ](https://github.com/SeaRise)でのメモリ使用量の推定が不正確になる問題を修正
    -   PDリーダーの故障により1分間に`IMPORT INTO`タスクが失敗する問題を修正[＃48307](https://github.com/pingcap/tidb/issues/48307) @ [D3ハンター](https://github.com/D3Hunter)
    -   `batch-client` in `client-go` [＃47691](https://github.com/pingcap/tidb/issues/47691) @ [クレイジーcs520](https://github.com/crazycs520)のpanic問題を修正
    -   特定の状況で列の整理によってpanicが発生する可能性がある問題を修正[＃47331](https://github.com/pingcap/tidb/issues/47331) @ [ハイラスティン](https://github.com/Rustin170506)
    -   TiDB が`systemd` [＃47442](https://github.com/pingcap/tidb/issues/47442) @ [ホーキングレイ](https://github.com/hawkingrei)で起動したときに`cgroup`リソース制限を読み取らない問題を修正しました
    -   集計関数またはウィンドウ関数を含む共通テーブル式 (CTE) が他の再帰 CTE によって参照される場合に発生する可能性のある構文エラーの問題を修正しました[＃47603](https://github.com/pingcap/tidb/issues/47603) [＃47711](https://github.com/pingcap/tidb/issues/47711) @ [エルサ0520](https://github.com/elsa0520)
    -   統計[＃35948](https://github.com/pingcap/tidb/issues/35948) @ [ハイラスティン](https://github.com/Rustin170506)の TopN 構造を構築するときに発生する可能性のあるpanic問題を修正しました。
    -   MPP によって計算された`COUNT(INT)`の結果が正しくない可能性がある問題を修正[＃48643](https://github.com/pingcap/tidb/issues/48643) @ [アイリンキッド](https://github.com/AilinKid)
    -   HashJoin 演算子がプローブ[＃48082](https://github.com/pingcap/tidb/issues/48082) @ [うわー](https://github.com/wshwsh12)を実行するときにチャンクを再利用できない問題を修正しました。

-   ティクヴ

    -   TiKV の実行速度が非常に遅い場合、リージョン[＃16111](https://github.com/tikv/tikv/issues/16111)と[金星の上](https://github.com/overvenus)マージ後にpanicが発生する可能性がある問題を修正しました。
    -   解決済みのTSが2時間ブロックされる可能性がある問題を修正[＃15520](https://github.com/tikv/tikv/issues/15520) [＃39130](https://github.com/pingcap/tidb/issues/39130) @ [金星の上](https://github.com/overvenus)
    -   TiKV がラフトログ[＃15800](https://github.com/tikv/tikv/issues/15800) @ [トニー](https://github.com/tonyxuqqi)を追加できないため`ServerIsBusy`エラーを報告する問題を修正しました。
    -   BRがクラッシュしたときにスナップショットの復元が停止する可能性がある問題を修正[＃15684](https://github.com/tikv/tikv/issues/15684) @ [ユジュンセン](https://github.com/YuJuncen)
    -   大規模なトランザクションを追跡するときに、古い読み取りの解決済み TS によって TiKV OOM の問題が発生する可能性がある問題を修正[＃14864](https://github.com/tikv/tikv/issues/14864) @ [金星の上](https://github.com/overvenus)
    -   破損した SST ファイルが他の TiKV ノード[＃15986](https://github.com/tikv/tikv/issues/15986) @ [コナー1996](https://github.com/Connor1996)に拡散する可能性がある問題を修正
    -   [＃15817](https://github.com/tikv/tikv/issues/15817) @ [コナー1996](https://github.com/Connor1996)にスケールアウトするときに DR 自動同期のジョイント状態がタイムアウトする可能性がある問題を修正しました。
    -   クラウド環境の Grafana でスケジューラ コマンド変数が正しくない問題を修正[＃15832](https://github.com/tikv/tikv/issues/15832) @ [コナー1996](https://github.com/Connor1996)
    -   リージョン[＃15919](https://github.com/tikv/tikv/issues/15919)が[金星の上](https://github.com/overvenus)にマージされた後、古いピアが保持され、resolved-tsがブロックされる問題を修正しました。
    -   オンラインの安全でないリカバリがマージ中止[＃15580](https://github.com/tikv/tikv/issues/15580) @ [v01dスター](https://github.com/v01dstar)処理できない問題を修正
    -   TiKV を再起動したときに、適用されていないRaftログが多数ある場合に発生する TiKV OOM 問題を修正しました[＃15770](https://github.com/tikv/tikv/issues/15770) @ [金星の上](https://github.com/overvenus)
    -   `lz4-sys`のバージョンを 1.9.4 [＃15621](https://github.com/tikv/tikv/issues/15621) @ [スペードA-タン](https://github.com/SpadeA-Tang)にアップグレードしてセキュリティ問題を修正
    -   Titanの`blob-run-mode`がオンライン[＃15978](https://github.com/tikv/tikv/issues/15978) @ [トニー](https://github.com/tonyxuqqi)更新できない問題を修正
    -   PDとTiKV間のネットワーク中断によりPITRが[＃15279](https://github.com/tikv/tikv/issues/15279) @ [ユジュンセン](https://github.com/YuJuncen)で停止する可能性がある問題を修正
    -   Raftピア[＃16069](https://github.com/tikv/tikv/issues/16069) @ [金星の上](https://github.com/overvenus)を削除するときに TiKV コプロセッサが古いデータを返す可能性がある問題を修正しました。

-   PD

    -   `CALIBRATE RESOURCE` [＃45166](https://github.com/pingcap/tidb/issues/45166) @ [キャビンフィーバーB](https://github.com/CabinfeverB)を実行すると TiDB ダッシュボードで`resource_manager_resource_unit`メトリックが空になる問題を修正しました
    -   ワークロードによる調整ページでエラー[＃48162](https://github.com/pingcap/tidb/issues/48162) @ [キャビンフィーバーB](https://github.com/CabinfeverB)が報告される問題を修正しました
    -   リソース グループを削除すると DDL アトミック性が損なわれる可能性がある問題を修正[＃45050](https://github.com/pingcap/tidb/issues/45050) @ [栄光](https://github.com/glorv)
    -   PDリーダーが転送され、新しいリーダーとPDクライアントの間にネットワークパーティションがある場合、PDクライアントがリーダー[＃7416](https://github.com/tikv/pd/issues/7416) @ [キャビンフィーバーB](https://github.com/CabinfeverB)の情報を更新できない問題を修正しました。
    -   大規模なクラスターに複数の TiKV ノードを追加すると、TiKVハートビートレポートが遅くなったり停止したりする可能性がある問題を修正しました[＃7248](https://github.com/tikv/pd/issues/7248) @ [rleungx](https://github.com/rleungx)
    -   TiDBダッシュボードがPD `trace`データを正しく読み取れない問題を修正[＃7253](https://github.com/tikv/pd/issues/7253) @ [ノルーシュ](https://github.com/nolouch)
    -   Gin Web Framework のバージョンを v1.8.1 から v1.9.1 にアップグレードして、いくつかのセキュリティ問題を修正しました[＃7438](https://github.com/tikv/pd/issues/7438) @ [ニューベル](https://github.com/niubell)
    -   ルールチェッカーが配置ルール[＃7185](https://github.com/tikv/pd/issues/7185) @ [ノルーシュ](https://github.com/nolouch)の設定に従って学習者を追加しない問題を修正しました。
    -   TiKV ノードが利用できない場合に PD が通常のピアを削除する可能性がある問題を修正[＃7249](https://github.com/tikv/pd/issues/7249) @ [翻訳者](https://github.com/lhy1024)
    -   DR自動同期モード[＃6988](https://github.com/tikv/pd/issues/6988) @ [ヒューシャープ](https://github.com/HuSharp)でリーダーの切り替えに時間がかかる問題を修正

-   TiFlash

    -   `ALTER TABLE ... EXCHANGE PARTITION ...`文を実行するとpanic[＃8372](https://github.com/pingcap/tiflash/issues/8372) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)発生する問題を修正
    -   クエリ[＃8447](https://github.com/pingcap/tiflash/issues/8447) @ [ジンヘリン](https://github.com/JinheLin)中にTiFlash がメモリ制限に遭遇した場合のメモリリークの問題を修正しました。
    -   `FLASHBACK DATABASE` [＃8450](https://github.com/pingcap/tiflash/issues/8450) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を実行した後もTiFlashレプリカのデータがガベージ コレクションされる問題を修正しました。
    -   Grafana [＃8076](https://github.com/pingcap/tiflash/issues/8076) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)の一部のパネルの最大パーセンタイル時間の誤った表示を修正
    -   クエリが予期しないエラー メッセージ「FineGrainedShuffleWriter-V1 でブロック スキーマが一致しません」を返す問題を修正[＃8111](https://github.com/pingcap/tiflash/issues/8111) @ [シーライズ](https://github.com/SeaRise)

-   ツール

    -   バックアップと復元 (BR)

        -   BR SQL コマンドと CLI のデフォルト値が異なるため、OOM の問題が発生する可能性がある問題を修正しました[＃48000](https://github.com/pingcap/tidb/issues/48000) @ [ユジュンセン](https://github.com/YuJuncen)
        -   大規模なワイドテーブル[＃15714](https://github.com/tikv/tikv/issues/15714) @ [ユジュンセン](https://github.com/YuJuncen)をバックアップするときに、一部のシナリオでログバックアップが停止する可能性がある問題を修正しました。
        -   BR が外部storageファイル[＃48452](https://github.com/pingcap/tidb/issues/48452) @ [3エースショーハンド](https://github.com/3AceShowHand)に対して誤った URI を生成する問題を修正
        -   EC2 メタデータ接続のリセット後の再試行により、バックアップと復元のパフォーマンスが低下する問題を修正[＃47650](https://github.com/pingcap/tidb/issues/47650) @ [リーヴルス](https://github.com/Leavrth)
        -   タスク初期化中にPDへの接続に失敗すると、ログバックアップタスクは開始できるが正常に動作しない問題を修正[＃16056](https://github.com/tikv/tikv/issues/16056) @ [ユジュンセン](https://github.com/YuJuncen)

    -   ティCDC

        -   特定のシナリオで`DELETE`ステートメントを複製するときに、 `WHERE`句が主キーを条件として使用しない問題を修正しました[＃9812](https://github.com/pingcap/tiflow/issues/9812) @ [アズドンメン](https://github.com/asddongmen)
        -   オブジェクトstorageにデータを複製するときに、特定の特殊なシナリオでレプリケーションタスクが停止する問題を修正[＃10041](https://github.com/pingcap/tiflow/issues/10041) [＃10044](https://github.com/pingcap/tiflow/issues/10044) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   同期ポイントとREDOログ[＃10091](https://github.com/pingcap/tiflow/issues/10091) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)を有効にした後、特定の特別なシナリオでレプリケーションタスクが停止する問題を修正しました。
        -   特定の特殊なシナリオで TiCDC が TiKV との接続を誤って閉じる問題を修正[＃10239](https://github.com/pingcap/tiflow/issues/10239) @ [ヒック](https://github.com/hicqu)
        -   ターゲット テーブルが削除され、アップストリーム[＃10079](https://github.com/pingcap/tiflow/issues/10079) @ [アズドンメン](https://github.com/asddongmen)で再作成された場合、変更フィードが双方向レプリケーション モードで DML イベントをレプリケートできない問題を修正しました。
        -   オブジェクト ストア シンク[＃10041](https://github.com/pingcap/tiflow/issues/10041) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)にデータを複製するときに NFS ディレクトリにアクセスすることによって発生するパフォーマンスの問題を修正しました。
        -   オブジェクトstorageサービス[＃10137](https://github.com/pingcap/tiflow/issues/10137) @ [スドジ](https://github.com/sdojjy)にデータを複製するときに TiCDCサーバーがpanicになる可能性がある問題を修正しました
        -   REDOログが有効になっている場合にDDL文の複製間隔が長すぎる問題を修正[＃9960](https://github.com/pingcap/tiflow/issues/9960) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   REDOログが有効になっている場合にNFS障害により所有者ノードが停止する問題を修正[＃9886](https://github.com/pingcap/tiflow/issues/9886) @ [3エースショーハンド](https://github.com/3AceShowHand)

    -   TiDB データ移行 (DM)

        -   `CompareGTID` [＃9676](https://github.com/pingcap/tiflow/issues/9676) @ [GMHDBJD](https://github.com/GMHDBJD)に不適切なアルゴリズムが使用されることで DM のパフォーマンスが低下する問題を修正しました

    -   TiDB Lightning

        -   PDリーダーが強制終了されたり、PDリクエストの処理が遅いためにデータのインポートが失敗する問題を修正[＃46950](https://github.com/pingcap/tidb/issues/46950) [＃48075](https://github.com/pingcap/tidb/issues/48075) @ [D3ハンター](https://github.com/D3Hunter)
        -   TiDB Lightningが`writeToTiKV` [＃46321](https://github.com/pingcap/tidb/issues/46321) [＃48352](https://github.com/pingcap/tidb/issues/48352) @ [ランス6716](https://github.com/lance6716)の間に停止する問題を修正
        -   HTTP再試行リクエストが現在のリクエストコンテンツ[＃47930](https://github.com/pingcap/tidb/issues/47930) @ [ランス6716](https://github.com/lance6716)を使用しないため、データのインポートが失敗する問題を修正しました
        -   物理インポートモード[＃45507](https://github.com/pingcap/tidb/issues/45507) @ [ミッタルリシャブ](https://github.com/mittalrishabh)で不要な`get_regions`呼び出しを削除します
