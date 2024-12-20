---
title: TiDB 6.5.6 Release Notes
summary: TiDB 6.5.6 の改善点とバグ修正について説明します。
---

# TiDB 6.5.6 リリースノート {#tidb-6-5-6-release-notes}

発売日: 2023年12月7日

TiDB バージョン: 6.5.6

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [実稼働環境への導入](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   Security強化モード (SEM) で[`require_secure_transport`](https://docs.pingcap.com/tidb/v6.5/system-variables#require_secure_transport-new-in-v610) ～ `ON`設定を禁止して、ユーザー[＃47665](https://github.com/pingcap/tidb/issues/47665) @ [天菜まお](https://github.com/tiancaiamao)の潜在的な接続問題を防ぎます。
-   オプティマイザがテーブル[＃46695](https://github.com/pingcap/tidb/issues/46695) @ [コーダープレイ](https://github.com/coderplay)に対してハッシュ結合を選択するかどうかを制御する[`tidb_opt_enable_hash_join`](https://docs.pingcap.com/tidb/v6.5/system-variables#tidb_opt_enable_hash_join-new-in-v656)システム変数を導入します。
-   さらにテストを行った結果、 TiCDC Changefeed構成項目[`case-sensitive`](/ticdc/ticdc-changefeed-config.md)のデフォルト値が`true`から`false`に変更されました。つまり、デフォルトでは、TiCDC 構成ファイル内のテーブル名とデータベース名は大文字と小文字が区別されません[＃10047](https://github.com/pingcap/tiflow/issues/10047) @ [スドジ](https://github.com/sdojjy)
-   TiCDC Changefeed、次の新しい構成項目が導入されています。
    -   [`sql-mode`](/ticdc/ticdc-changefeed-config.md) : TiCDC がデータを複製するときに DDL ステートメントを解析するために使用する[SQL モード](https://docs.pingcap.com/tidb/v6.5/ticdc-ddl#sql-mode)を設定できます[＃9876](https://github.com/pingcap/tiflow/issues/9876) @ [アズドンメン](https://github.com/asddongmen)
    -   [`encoding-worker-num`](/ticdc/ticdc-changefeed-config.md)と[`flush-worker-num`](/ticdc/ticdc-changefeed-config.md) : 異なるマシンの仕様に基づいて、再実行モジュールの異なる同時実行パラメータを設定できます[＃10048](https://github.com/pingcap/tiflow/issues/10048) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
    -   [`compression`](/ticdc/ticdc-changefeed-config.md) : REDOログファイルの圧縮動作を設定できます[＃10176](https://github.com/pingcap/tiflow/issues/10176) @ [スドジ](https://github.com/sdojjy)
    -   [`changefeed-error-stuck-duration`](/ticdc/ticdc-changefeed-config.md) : 内部エラーまたは例外が発生したときに、変更フィードが自動的に再試行できる期間を設定できます[＃9875](https://github.com/pingcap/tiflow/issues/9875) @ [アズドンメン](https://github.com/asddongmen)
    -   [`sink.cloud-storage-config`](/ticdc/ticdc-changefeed-config.md) : オブジェクトstorageにデータを複製するときに履歴データの自動クリーンアップを設定できます[＃10109](https://github.com/pingcap/tiflow/issues/10109) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)

## 改善点 {#improvements}

-   ティビ

    -   [`FLASHBACK CLUSTER TO TSO`](https://docs.pingcap.com/tidb/v6.5/sql-statement-flashback-cluster)構文[＃48372](https://github.com/pingcap/tidb/issues/48372) @ [ボーンチェンジャー](https://github.com/BornChanger)をサポート

-   ティクヴ

    -   OOM [＃15458](https://github.com/tikv/tikv/issues/15458) @ [金星の上](https://github.com/overvenus)防ぐためにリゾルバのメモリ使用量を最適化します
    -   ルータオブジェクトのLRUCacheを排除してメモリ使用量を削減し、OOM [＃15430](https://github.com/tikv/tikv/issues/15430) @ [コナー1996](https://github.com/Connor1996)を防止します。
    -   `apply_router`と`raft_router`メトリック[＃15357](https://github.com/tikv/tikv/issues/15357)に`alive`と`leak`監視ディメンションを追加します[トニー](https://github.com/tonyxuqqi)

-   PD

    -   Grafanaダッシュボード[＃6975](https://github.com/tikv/pd/issues/6975) @ [ディスク](https://github.com/disksing)に`Status`と`Sync Progress` `DR Auto-Sync`のような監視メトリックを追加します

-   ツール

    -   バックアップと復元 (BR)

        -   スナップショットバックアップの復元中に、 BR は特定のネットワークエラーが発生すると再試行します[＃48528](https://github.com/pingcap/tidb/issues/48528) @ [リーヴルス](https://github.com/Leavrth)
        -   `delete range`シナリオでポイントインタイムリカバリ (PITR) の新しい統合テストを導入し、PITR の安定性を向上[＃47738](https://github.com/pingcap/tidb/issues/47738) @ [リーヴルス](https://github.com/Leavrth)
        -   タイムアウトエラーまたはリージョンスキャッタ[＃47236](https://github.com/pingcap/tidb/issues/47236) @ [リーヴルス](https://github.com/Leavrth)のキャンセルが発生した場合に、スナップショットリカバリ中にリージョンスキャッタの自動再試行を有効にする
        -   BRは、 `merge-schedule-limit`構成を`0` [＃7148](https://github.com/tikv/pd/issues/7148) @ [ボーンチェンジャー](https://github.com/3pointer)に設定することで、リージョンのマージを一時停止できます。

    -   ティCDC

        -   `sink-uri`構成[＃10106](https://github.com/pingcap/tiflow/issues/10106) @ [3エースショーハンド](https://github.com/3AceShowHand)で`content-compatible=true`設定することにより、 TiCDC Canal-JSON コンテンツ形式[公式Canal出力のコンテンツフォーマットと互換性がある](https://docs.pingcap.com/tidb/v6.5/ticdc-canal-json#compatibility-with-the-official-canal)の作成をサポートします。
        -   `ADD INDEX` DDL操作を複製する実行ロジックを最適化して、後続のDMLステートメント[＃9644](https://github.com/pingcap/tiflow/issues/9644) @ [スドジ](https://github.com/sdojjy)をブロックしないようにします。
        -   TiCDC 増分スキャンによる上流 TiKV [＃11390](https://github.com/tikv/tikv/issues/11390) @ [ヒック](https://github.com/hicqu)への影響を軽減

## バグ修正 {#bug-fixes}

-   ティビ

    -   HashJoin 演算子がプローブ[＃48082](https://github.com/pingcap/tidb/issues/48082) @ [うわー](https://github.com/wshwsh12)実行するときにチャンクを再利用できない問題を修正しました。
    -   `AUTO_ID_CACHE=1`が[＃46444](https://github.com/pingcap/tidb/issues/46444) @ [天菜まお](https://github.com/tiancaiamao)に設定されている場合に`Duplicate entry`発生する可能性がある問題を修正しました
    -   2つのサブクエリ[＃46160](https://github.com/pingcap/tidb/issues/46160) @ [qw4990](https://github.com/qw4990)を結合するときに`TIDB_INLJ`ヒントが有効にならない問題を修正
    -   TiDB の再起動後に DDL 操作が停止する可能性がある問題を修正[＃46751](https://github.com/pingcap/tidb/issues/46751) @ [翻訳:](https://github.com/wjhuang2016)
    -   不正な MDL 処理により DDL 操作が永久にブロックされる可能性がある問題を修正[＃46920](https://github.com/pingcap/tidb/issues/46920) @ [翻訳:](https://github.com/wjhuang2016)
    -   `MERGE_JOIN`の結果が間違っている問題を修正[＃46580](https://github.com/pingcap/tidb/issues/46580) @ [qw4990](https://github.com/qw4990)
    -   ソート演算子によりスピル処理中に TiDB がクラッシュする可能性がある問題を修正[＃47538](https://github.com/pingcap/tidb/issues/47538) @ [風の話し手](https://github.com/windtalker)
    -   CAST に精度損失がない場合に`cast(col)=range`条件で FullScan が発生する問題を修正[＃45199](https://github.com/pingcap/tidb/issues/45199) @ [アイリンキッド](https://github.com/AilinKid)
    -   `batch-client` in `client-go` [＃47691](https://github.com/pingcap/tidb/issues/47691) @ [クレイジーcs520](https://github.com/crazycs520)のpanic問題を修正
    -   非整数クラスター化インデックス[＃47350](https://github.com/pingcap/tidb/issues/47350) @ [タンジェンタ](https://github.com/tangenta)でのテーブル分割操作を禁止する
    -   時間変換[＃42439](https://github.com/pingcap/tidb/issues/42439) @ [qw4990](https://github.com/qw4990)中に準備済みプラン キャッシュと準備されていないプラン キャッシュの動作間の非互換性の問題を修正しました
    -   取り込みモード[＃39641](https://github.com/pingcap/tidb/issues/39641) @ [タンジェンタ](https://github.com/tangenta)を使用して空のテーブルにインデックスを作成できないことがある問題を修正しました。
    -   パーティション交換[＃46492](https://github.com/pingcap/tidb/issues/46492) @ [ミョンス](https://github.com/mjonss)中にパーティション定義に準拠していないデータを検出できない問題を修正
    -   `GROUP_CONCAT` `ORDER BY`列[＃41986](https://github.com/pingcap/tidb/issues/41986) @ [アイリンキッド](https://github.com/AilinKid)を解析できない問題を修正
    -   深くネストされた式に対してハッシュコードが繰り返し計算され、メモリ使用量が増加し、OOM [＃42788](https://github.com/pingcap/tidb/issues/42788) @ [アイリンキッド](https://github.com/AilinKid)発生する問題を修正しました。
    -   MPP 実行プランで集計がユニオンを介してプッシュダウンされると、結果が正しくなくなる問題を修正しました[＃45850](https://github.com/pingcap/tidb/issues/45850) @ [アイリンキッド](https://github.com/AilinKid)
    -   `INDEX_LOOKUP_HASH_JOIN` [＃47788](https://github.com/pingcap/tidb/issues/47788) @ [シーライズ](https://github.com/SeaRise)でのメモリ使用量の推定が不正確になる問題を修正
    -   `plan replayer`で生成された zip ファイルを TiDB [＃46474](https://github.com/pingcap/tidb/issues/46474) @ [ヤンケオ](https://github.com/YangKeao)にインポートできない問題を修正
    -   `N` in `LIMIT N` [＃43285](https://github.com/pingcap/tidb/issues/43285) @ [qw4990](https://github.com/qw4990)が大きすぎるために生じた誤ったコスト見積りを修正
    -   統計[＃35948](https://github.com/pingcap/tidb/issues/35948) @ [ハイラスティン](https://github.com/Rustin170506)の TopN 構造を構築するときに発生する可能性のあるpanic問題を修正しました。
    -   MPP によって計算された`COUNT(INT)`の結果が正しくない可能性がある問題を修正[＃48643](https://github.com/pingcap/tidb/issues/48643) @ [アイリンキッド](https://github.com/AilinKid)
    -   `tidb_enable_ordered_result_mode`が有効になっている場合にpanicが発生する可能性がある問題を修正[＃45044](https://github.com/pingcap/tidb/issues/45044) @ [qw4990](https://github.com/qw4990)
    -   ウィンドウ関数[＃46177](https://github.com/pingcap/tidb/issues/46177) @ [qw4990](https://github.com/qw4990)によって導入されたソートを減らすために、オプティマイザが誤って IndexFullScan を選択する問題を修正しました。
    -   述語が共通テーブル式[＃47881](https://github.com/pingcap/tidb/issues/47881) @ [ウィノロス](https://github.com/winoros)にプッシュダウンされたときに結果が不正確になる可能性がある問題を修正しました
    -   最初のサブノードとしてDUALテーブルを使用して`UNION ALL`実行するとエラー[＃48755](https://github.com/pingcap/tidb/issues/48755) @ [ウィノロス](https://github.com/winoros)が発生する可能性がある問題を修正しました
    -   特定の状況で列の整理によってpanicが発生する可能性がある問題を修正[＃47331](https://github.com/pingcap/tidb/issues/47331) @ [ハイラスティン](https://github.com/Rustin170506)
    -   集計関数またはウィンドウ関数を含む共通テーブル式 (CTE) が他の再帰 CTE によって参照される場合に発生する可能性のある構文エラーの問題を修正しました[＃47603](https://github.com/pingcap/tidb/issues/47603) [＃47711](https://github.com/pingcap/tidb/issues/47711) @ [エルサ0520](https://github.com/elsa0520)
    -   プリペアドステートメント[＃46817](https://github.com/pingcap/tidb/issues/46817) @ [ジャッキー](https://github.com/jackysp)で`QB_NAME`ヒントを使用すると例外が発生する可能性がある問題を修正しました
    -   `AUTO_ID_CACHE=1` [＃46324](https://github.com/pingcap/tidb/issues/46324) @ [天菜まお](https://github.com/tiancaiamao)使用時の Goroutine リークの問題を修正
    -   [＃32110](https://github.com/pingcap/tidb/issues/32110) @ [2993年7月](https://github.com/july2993)をシャットダウンするときに TiDB がpanicになる可能性がある問題を修正しました
    -   TiDB スキーマ キャッシュ[＃48281](https://github.com/pingcap/tidb/issues/48281) @ [翻訳](https://github.com/cfzjywxk)からスキーマ diff コミット バージョンを読み取るときに MVCC インターフェイスでロックが処理されない問題を修正しました。
    -   テーブル[＃47064](https://github.com/pingcap/tidb/issues/47064) @ [ジフハウス](https://github.com/jiyfhust)名前変更によって発生する`information_schema.columns`の重複行の問題を修正
    -   `LOAD DATA REPLACE INTO`文のバグを修正[＃47995](https://github.com/pingcap/tidb/issues/47995) ) @ [ランス6716](https://github.com/lance6716)
    -   PDリーダーの故障により1分間に`IMPORT INTO`タスクが失敗する問題を修正[＃48307](https://github.com/pingcap/tidb/issues/48307) @ [D3ハンター](https://github.com/D3Hunter)
    -   日付型フィールド[＃47426](https://github.com/pingcap/tidb/issues/47426) @ [タンジェンタ](https://github.com/tangenta)にインデックスを作成することによって発生する`ADMIN CHECK`の障害の問題を修正
    -   `TABLESAMPLE` [＃48253](https://github.com/pingcap/tidb/issues/48253) @ [タンジェンタ](https://github.com/tangenta)によって返される未ソートの行データの問題を修正
    -   DDL `jobID`が 0 [＃46296](https://github.com/pingcap/tidb/issues/46296) @ [ジフハウス](https://github.com/jiyfhust)に復元されたときに発生する TiDB ノードpanicの問題を修正しました。

-   ティクヴ

    -   ピアを移動するとFollower Readのパフォーマンスが低下する可能性がある問題を修正[＃15468](https://github.com/tikv/tikv/issues/15468) @ [ユジュンセン](https://github.com/YuJuncen)
    -   raftstore-applys [＃15371](https://github.com/tikv/tikv/issues/15371) @ [コナー1996](https://github.com/Connor1996)が継続的に増加するデータエラーを修正
    -   オンラインワークロード[＃15565](https://github.com/tikv/tikv/issues/15565) @ [ランス6716](https://github.com/lance6716)がある場合にTiDB Lightningチェックサム コプロセッサの要求がタイムアウトする問題を修正しました
    -   `lz4-sys`のバージョンを 1.9.4 [＃15621](https://github.com/tikv/tikv/issues/15621) @ [スペードA-タン](https://github.com/SpadeA-Tang)にアップグレードしてセキュリティ問題を修正
    -   `tokio`のバージョンを 6.5 [＃15621](https://github.com/tikv/tikv/issues/15621) @ [リクササシネーター](https://github.com/LykxSassinator)にアップグレードしてセキュリティ問題を修正
    -   `flatbuffer` [＃15621](https://github.com/tikv/tikv/issues/15621) @ [トニー](https://github.com/tonyxuqqi)を削除してセキュリティ問題を修正
    -   TiKV ストアが[＃15679](https://github.com/tikv/tikv/issues/15679) @ [ヒック](https://github.com/hicqu)に分割されているときに、 resolved-tsラグが増加する問題を修正しました。
    -   TiKV を再起動したときに、適用されていないRaftログが多数ある場合に発生する TiKV OOM 問題を修正しました[＃15770](https://github.com/tikv/tikv/issues/15770) @ [金星の上](https://github.com/overvenus)
    -   リージョン[＃15919](https://github.com/tikv/tikv/issues/15919)が[金星の上](https://github.com/overvenus)にマージされた後、古いピアが保持され、resolved-tsがブロックされる問題を修正しました。
    -   クラウド環境の Grafana でスケジューラ コマンド変数が正しくない問題を修正[＃15832](https://github.com/tikv/tikv/issues/15832) @ [コナー1996](https://github.com/Connor1996)
    -   Titanの`blob-run-mode`がオンライン[＃15978](https://github.com/tikv/tikv/issues/15978) @ [トニー](https://github.com/tonyxuqqi)更新できない問題を修正
    -   リージョン[＃13311](https://github.com/tikv/tikv/issues/13311)と[翻訳](https://github.com/cfzjywxk)の間でメタデータが一致しないために TiKV がパニックになる問題を修正しました。
    -   オンラインアンセーフリカバリ[＃15629](https://github.com/tikv/tikv/issues/15629) @ [コナー1996](https://github.com/Connor1996)中にリーダーが強制終了するとTiKVがパニックになる問題を修正
    -   [＃15817](https://github.com/tikv/tikv/issues/15817) @ [コナー1996](https://github.com/Connor1996)にスケールアウトするときに DR 自動同期のジョイント状態がタイムアウトする可能性がある問題を修正しました。
    -   Raftピア[＃16069](https://github.com/tikv/tikv/issues/16069) @ [金星の上](https://github.com/overvenus)を削除するときに TiKV コプロセッサが古いデータを返す可能性がある問題を修正しました。
    -   resolved-tsが2時間ブロックされる可能性がある問題を修正[＃39130](https://github.com/pingcap/tidb/issues/39130) @ [金星の上](https://github.com/overvenus)
    -   `notLeader`または`regionNotFound` [＃15712](https://github.com/tikv/tikv/issues/15712) @ [ヒューシャープ](https://github.com/HuSharp)に遭遇するとフラッシュバックが停止する可能性がある問題を修正しました

-   PD

    -   プラグインディレクトリとファイルの潜在的なセキュリティリスクを修正[＃7094](https://github.com/tikv/pd/issues/7094) @ [ヒューシャープ](https://github.com/HuSharp)
    -   変更された分離レベルがデフォルトの配置ルール[＃7121](https://github.com/tikv/pd/issues/7121) @ [rleungx](https://github.com/rleungx)に同期されない問題を修正しました
    -   `evict-leader-scheduler`構成[＃6897](https://github.com/tikv/pd/issues/6897) @ [ヒューシャープ](https://github.com/HuSharp)失う可能性がある問題を修正
    -   BR [＃7148](https://github.com/tikv/pd/issues/7148) @ [キャビンフィーバー](https://github.com/CabinfeverB)の回復プロセス中に、空のリージョンをカウントする方法によってリージョンのバランスが崩れる可能性がある問題を修正しました。
    -   配置ルールの構成が複雑な場合に、データレプリケーション自動同期 (DR 自動同期) モードを採用しているクラスターで`canSync`と`hasMajority`誤って計算される可能性がある問題を修正しました[＃7201](https://github.com/tikv/pd/issues/7201) @ [ディスク](https://github.com/disksing)
    -   データレプリケーション自動同期（DR自動同期）モード[＃7221](https://github.com/tikv/pd/issues/7221) @ [ディスク](https://github.com/disksing)を採用しているクラスターで`available_stores`誤って計算される問題を修正
    -   データレプリケーション自動同期 (DR 自動同期) モード[＃7218](https://github.com/tikv/pd/issues/7218) @ [ディスク](https://github.com/disksing)を採用しているクラスターで、セカンダリ AZ がダウンしているときにプライマリ AZ が TiKV ノードを追加できない問題を修正しました。
    -   大規模なクラスターに複数の TiKV ノードを追加すると、TiKVハートビートレポートが遅くなったり停止したりする可能性がある問題を修正しました[＃7248](https://github.com/tikv/pd/issues/7248) @ [rleungx](https://github.com/rleungx)
    -   TiKV ノードが利用できない場合に PD が通常のピアを削除する可能性がある問題を修正[＃7249](https://github.com/tikv/pd/issues/7249) @ [翻訳者](https://github.com/lhy1024)
    -   DR自動同期モード[＃6988](https://github.com/tikv/pd/issues/6988) @ [ヒューシャープ](https://github.com/HuSharp)でリーダーの切り替えに時間がかかる問題を修正
    -   Gin Web Framework のバージョンを v1.8.1 から v1.9.1 にアップグレードして、いくつかのセキュリティ問題を修正しました[＃7438](https://github.com/tikv/pd/issues/7438) @ [ニューベル](https://github.com/niubell)

-   TiFlash

    -   Grafana [＃7713](https://github.com/pingcap/tiflash/issues/7713) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)で`max_snapshot_lifetime`メトリックが正しく表示されない問題を修正
    -   `ALTER TABLE ... EXCHANGE PARTITION ...`文を実行するとpanic[＃8372](https://github.com/pingcap/tiflash/issues/8372) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)発生する問題を修正
    -   MemoryTracker によって報告されるメモリ使用量が不正確であるという問題を修正[＃8128](https://github.com/pingcap/tiflash/issues/8128) @ [ジンヘリン](https://github.com/JinheLin)

-   ツール

    -   バックアップと復元 (BR)

        -   大規模なワイドテーブル[＃15714](https://github.com/tikv/tikv/issues/15714) @ [ユジュンセン](https://github.com/YuJuncen)をバックアップするときに、一部のシナリオでログバックアップが停止する可能性がある問題を修正しました。
        -   頻繁なフラッシュによりログバックアップが停止する問題を修正[＃15602](https://github.com/tikv/tikv/issues/15602) @ [3ポインター](https://github.com/3pointer)
        -   EC2 メタデータ接続のリセット後の再試行により、バックアップと復元のパフォーマンスが低下する問題を修正[＃47650](https://github.com/pingcap/tidb/issues/47650) @ [リーヴルス](https://github.com/Leavrth)
        -   1分以内にPITRを複数回実行するとデータが失われる可能性がある問題を修正[＃15483](https://github.com/tikv/tikv/issues/15483) @ [ユジュンセン](https://github.com/YuJuncen)
        -   BR SQL コマンドと CLI のデフォルト値が異なるため、OOM の問題が発生する可能性がある問題を修正しました[＃48000](https://github.com/pingcap/tidb/issues/48000) @ [ユジュンセン](https://github.com/YuJuncen)
        -   PD 所有者が[＃47533](https://github.com/pingcap/tidb/issues/47533) @ [ユジュンセン](https://github.com/YuJuncen)に転送されるとログ バックアップがpanicになる可能性がある問題を修正しました
        -   BR が外部storageファイル[＃48452](https://github.com/pingcap/tidb/issues/48452) @ [3エースショーハンド](https://github.com/3AceShowHand)に対して誤った URI を生成する問題を修正

    -   ティCDC

        -   アップストリーム[＃9739](https://github.com/pingcap/tiflow/issues/9739) @ [ヒック](https://github.com/hicqu)で損失のある DDL ステートメントを実行するときに TiCDCサーバーがpanicになる可能性がある問題を修正しました。
        -   再実行ログ機能を有効にして`RESUME`実行すると、レプリケーションタスクがエラーを報告する問題を修正[＃9769](https://github.com/pingcap/tiflow/issues/9769) @ [ヒック](https://github.com/hicqu)
        -   TiKVノードがクラッシュするとレプリケーションラグが長くなる問題を修正[＃9741](https://github.com/pingcap/tiflow/issues/9741) @ [スドジ](https://github.com/sdojjy)
        -   `WHERE`ステートメントが TiDB または MySQL [＃9988](https://github.com/pingcap/tiflow/issues/9988) @ [アズドンメン](https://github.com/asddongmen)にデータを複製するときに主キーを条件として使用しない問題を修正しました
        -   レプリケーションタスクのワークロードが TiCDC ノード[＃9839](https://github.com/pingcap/tiflow/issues/9839) @ [3エースショーハンド](https://github.com/3AceShowHand)間で均等に分散されない問題を修正しました。
        -   REDOログが有効になっている場合にDDL文の複製間隔が長すぎる問題を修正[＃9960](https://github.com/pingcap/tiflow/issues/9960) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   ターゲット テーブルが削除され、アップストリーム[＃10079](https://github.com/pingcap/tiflow/issues/10079) @ [アズドンメン](https://github.com/asddongmen)で再作成された場合、変更フィードが双方向レプリケーション モードで DML イベントをレプリケートできない問題を修正しました。
        -   オブジェクトstorageサービスにデータを複製するときに、NFS ファイルが多すぎるためにレプリケーションの遅延が長くなる問題を修正[＃10041](https://github.com/pingcap/tiflow/issues/10041) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   オブジェクトstorageサービス[＃10137](https://github.com/pingcap/tiflow/issues/10137) @ [スドジ](https://github.com/sdojjy)にデータを複製するときに TiCDCサーバーがpanicになる可能性がある問題を修正しました
        -   PD のスケールアップおよびスケールダウン中に TiCDC が無効な古いアドレスにアクセスする問題を修正[＃9584](https://github.com/pingcap/tiflow/issues/9584) @ [ふびんず](https://github.com/fubinzh) @ [アズドンメン](https://github.com/asddongmen)
        -   間違ったメモリ情報を取得すると、一部のオペレーティング システムで OOM 問題が発生する可能性がある問題を修正しました[＃9762](https://github.com/pingcap/tiflow/issues/9762) @ [スドジ](https://github.com/sdojjy)

    -   TiDB データ移行 (DM)

        -   DM が楽観的モード[＃9788](https://github.com/pingcap/tiflow/issues/9788) @ [GMHDBJD](https://github.com/GMHDBJD)でパーティション DDL をスキップする問題を修正
        -   オンライン DDL [＃9587](https://github.com/pingcap/tiflow/issues/9587) @ [GMHDBJD](https://github.com/GMHDBJD)をスキップするときに DM が上流のテーブル スキーマを適切に追跡できない問題を修正しました。
        -   失敗した DDL がスキップされ、後続の DDL が実行されない場合に、DM によって返されるレプリケーション ラグが増大し続ける問題を修正[＃9605](https://github.com/pingcap/tiflow/issues/9605) @ [D3ハンター](https://github.com/D3Hunter)
        -   楽観的モード[＃9588](https://github.com/pingcap/tiflow/issues/9588) @ [GMHDBJD](https://github.com/GMHDBJD)でタスクを再開するときに DM がすべての DML をスキップする問題を修正

    -   TiDB Lightning

        -   `write to tikv with no leader returned`エラー[＃45673](https://github.com/pingcap/tidb/issues/45673) @ [ランス6716](https://github.com/lance6716)が発生したときにデータのインポートが失敗する問題を修正しました
        -   HTTP再試行リクエストが現在のリクエストコンテンツ[＃47930](https://github.com/pingcap/tidb/issues/47930) @ [ランス6716](https://github.com/lance6716)を使用しないため、データのインポートが失敗する問題を修正しました
        -   `writeToTiKV` [＃46321](https://github.com/pingcap/tidb/issues/46321) @ [ランス6716](https://github.com/lance6716)中にTiDB Lightning が停止する問題を修正
        -   物理インポートモード[＃45507](https://github.com/pingcap/tidb/issues/45507) @ [ミッタルリシャブ](https://github.com/mittalrishabh)で不要な`get_regions`呼び出しを削除します

    -   TiDBBinlog

        -   1 GB [＃28659](https://github.com/pingcap/tidb/issues/28659) @ [ジャッキー](https://github.com/jackysp)を超えるトランザクションを転送するときにDrainer が終了する問題を修正
