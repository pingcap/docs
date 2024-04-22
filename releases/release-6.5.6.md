---
title: TiDB 6.5.6 Release Notes
summary: TiDB 6.5.6は2023年12月7日にリリースされました。このバージョンでは、セキュリティ強化モードでの設定変更やオプティマイザの制御などが行われています。さらに、TiCDC Changefeedに新しい構成項目が導入され、TiDBやTiKV、PD、TiFlash、ツールなどの改善点やバグの修正も含まれています。
---

# TiDB 6.5.6 リリースノート {#tidb-6-5-6-release-notes}

発売日：2023年12月7日

TiDB バージョン: 6.5.6

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [インストールパッケージ](https://www.pingcap.com/download/?version=v6.5.6#version-list)

## 互換性の変更 {#compatibility-changes}

-   ユーザー[#47665](https://github.com/pingcap/tidb/issues/47665) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)の潜在的な接続問題を防ぐために、Security強化モード (SEM) で[`require_secure_transport`](https://docs.pingcap.com/tidb/v6.5/system-variables#require_secure_transport-new-in-v610) ～ `ON`の設定を禁止します。
-   [`tidb_opt_enable_hash_join`](https://docs.pingcap.com/tidb/v6.5/system-variables#tidb_opt_enable_hash_join-new-in-v656)システム変数を導入して、オプティマイザがテーブル[#46695](https://github.com/pingcap/tidb/issues/46695) @ [コードプレイ](https://github.com/coderplay)のハッシュ結合を選択するかどうかを制御します。
-   さらにテストを行った後、 TiCDC Changefeed構成項目[`case-sensitive`](/ticdc/ticdc-changefeed-config.md)のデフォルト値が`true`から`false`に変更されました。これは、デフォルトでは、TiCDC 構成ファイル内のテーブル名とデータベース名は大文字と小文字が区別されないことを意味します[#10047](https://github.com/pingcap/tiflow/issues/10047) @ [スドジ](https://github.com/sdojjy)
-   TiCDC Changefeed、次の新しい構成項目が導入されています。
    -   [`sql-mode`](/ticdc/ticdc-changefeed-config.md) : TiCDC がデータ[#9876](https://github.com/pingcap/tiflow/issues/9876) @ [東門](https://github.com/asddongmen)を複製するときに TiCDC が DDL ステートメントを解析するために使用する[SQLモード](/ticdc/ticdc-ddl.md#sql-mode)を設定できるようにします。
    -   [`encoding-worker-num`](/ticdc/ticdc-changefeed-config.md)および[`flush-worker-num`](/ticdc/ticdc-changefeed-config.md) : さまざまなマシン[#10048](https://github.com/pingcap/tiflow/issues/10048) @ [CharlesCheung96](https://github.com/CharlesCheung96)の仕様に基づいて、REDO モジュールのさまざまな同時実行パラメータを設定できます。
    -   [`compression`](/ticdc/ticdc-changefeed-config.md) : REDO ログ ファイル[#10176](https://github.com/pingcap/tiflow/issues/10176) @ [スドジ](https://github.com/sdojjy)の圧縮動作を構成できます。
    -   [`sink.cloud-storage-config`](/ticdc/ticdc-changefeed-config.md) : データをオブジェクトstorage[#10109](https://github.com/pingcap/tiflow/issues/10109) @ [CharlesCheung96](https://github.com/CharlesCheung96)にレプリケートするときに、履歴データの自動クリーンアップを設定できます。

## 改善点 {#improvements}

-   TiDB

    -   [`FLASHBACK CLUSTER TO TSO`](https://docs.pingcap.com/tidb/v6.5/sql-statement-flashback-cluster)構文[#48372](https://github.com/pingcap/tidb/issues/48372) @ [ボーンチェンジャー](https://github.com/BornChanger)をサポートします

-   TiKV

    -   OOM [#15458](https://github.com/tikv/tikv/issues/15458) @ [オーバーヴィーナス](https://github.com/overvenus)を防ぐためにリゾルバーのメモリ使用量を最適化します。
    -   Router オブジェクトの LRUCache を削除してメモリ使用量を削減し、OOM [#15430](https://github.com/tikv/tikv/issues/15430) @ [コナー1996](https://github.com/Connor1996)を防止します。
    -   `apply_router`および`raft_router`メトリクスに`alive`および`leak`モニタリング ディメンションを追加します[#15357](https://github.com/tikv/tikv/issues/15357) @ [トニーシュクキ](https://github.com/tonyxuqqi)

-   PD

    -   Grafana ダッシュボード[#6975](https://github.com/tikv/pd/issues/6975) @ [ディスク化](https://github.com/disksing)に`Status`や`Sync Progress` for `DR Auto-Sync`などの監視指標を追加します。

-   ツール

    -   バックアップと復元 (BR)

        -   スナップショット バックアップの復元中に、特定のネットワーク エラーが発生すると、 BR は再試行します[#48528](https://github.com/pingcap/tidb/issues/48528) @ [レヴルス](https://github.com/Leavrth)
        -   `delete range`シナリオにポイントインタイム リカバリ (PITR) の新しい統合テストを導入し、PITR の安定性を強化します[#47738](https://github.com/pingcap/tidb/issues/47738) @ [レヴルス](https://github.com/Leavrth)
        -   タイムアウト障害が発生した場合、またはリージョンスキャッター[#47236](https://github.com/pingcap/tidb/issues/47236) @ [レヴルス](https://github.com/Leavrth)のキャンセルが発生した場合、スナップショットのリカバリ中にリージョンスキャッターの自動再試行を有効にします。
        -   BR は、 `merge-schedule-limit`構成を`0` [#7148](https://github.com/tikv/pd/issues/7148) @ [ボーンチェンジャー](https://github.com/3pointer)に設定することで、リージョンのマージを一時停止できます。

    -   TiCDC

        -   `sink-uri`構成[#10106](https://github.com/pingcap/tiflow/issues/10106) @ [3エースショーハンド](https://github.com/3AceShowHand)で`content-compatible=true`を設定することにより、 TiCDC Canal-JSON コンテンツ形式[公式の Canal 出力のコンテンツ形式と互換性があります](https://docs.pingcap.com/tidb/v6.5/ticdc-canal-json#compatibility-with-the-official-canal)の作成をサポート
        -   `ADD INDEX` DDL 操作を複製する実行ロジックを最適化して、後続の DML ステートメントのブロックを回避します[#9644](https://github.com/pingcap/tiflow/issues/9644) @ [スドジ](https://github.com/sdojjy)
        -   アップストリーム TiKV [#11390](https://github.com/tikv/tikv/issues/11390) @ [ひっくり返る](https://github.com/hicqu)に対する TiCDC インクリメンタル スキャンの影響を軽減します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   HashJoin オペレーターがプローブ[#48082](https://github.com/pingcap/tidb/issues/48082) @ [wshwsh12](https://github.com/wshwsh12)を実行するとチャンクが再利用できない問題を修正
    -   `AUTO_ID_CACHE=1`を[#46444](https://github.com/pingcap/tidb/issues/46444) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)に設定すると`Duplicate entry`発生する場合がある問題を修正
    -   2 つのサブクエリ[#46160](https://github.com/pingcap/tidb/issues/46160) @ [qw4990](https://github.com/qw4990)を結合するときに`TIDB_INLJ`ヒントが有効にならない問題を修正
    -   TiDB の再起動後に DDL 操作が停止する可能性がある問題を修正[#46751](https://github.com/pingcap/tidb/issues/46751) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   不適切な MDL 処理[#46920](https://github.com/pingcap/tidb/issues/46920) @ [wjhuang2016](https://github.com/wjhuang2016)が原因で DDL 操作が永続的にブロックされる可能性がある問題を修正します。
    -   `MERGE_JOIN`の結果が正しくない問題を修正[#46580](https://github.com/pingcap/tidb/issues/46580) @ [qw4990](https://github.com/qw4990)
    -   Sort オペレーターにより、スピル プロセス[#47538](https://github.com/pingcap/tidb/issues/47538) @ [ウィンドトーカー](https://github.com/windtalker)中に TiDB がクラッシュする可能性がある問題を修正します。
    -   CAST に精度の損失がない[#45199](https://github.com/pingcap/tidb/issues/45199) @ [アイリンキッド](https://github.com/AilinKid)のときに、 `cast(col)=range`条件によってフルスキャンが発生する問題を修正します。
    -   `batch-client` `client-go` @ [クレイジークス520](https://github.com/crazycs520) [#47691](https://github.com/pingcap/tidb/issues/47691)panicの問題を修正
    -   非整数クラスター化インデックス[#47350](https://github.com/pingcap/tidb/issues/47350) @ [タンジェンタ](https://github.com/tangenta)での分割テーブル操作の禁止
    -   時間変換[#42439](https://github.com/pingcap/tidb/issues/42439) @ [qw4990](https://github.com/qw4990)中の準備済みプラン キャッシュと準備されていないプラン キャッシュの動作間の非互換性の問題を修正しました。
    -   インジェスト モード[#39641](https://github.com/pingcap/tidb/issues/39641) @ [タンジェンタ](https://github.com/tangenta)を使用して空のテーブルにインデックスを作成できない場合がある問題を修正
    -   パーティション交換[#46492](https://github.com/pingcap/tidb/issues/46492) @ [むじょん](https://github.com/mjonss)時にパーティション定義に準拠しないデータを検出できない問題を修正
    -   `GROUP_CONCAT`が`ORDER BY`列[#41986](https://github.com/pingcap/tidb/issues/41986) @ [アイリンキッド](https://github.com/AilinKid)を解析できない問題を修正
    -   深くネストされた式に対して HashCode が繰り返し計算され、メモリ使用量が増加し、OOM [#42788](https://github.com/pingcap/tidb/issues/42788) @ [アイリンキッド](https://github.com/AilinKid)が発生する問題を修正します。
    -   MPP 実行プランの Union を介して集計がプッシュダウンされると、結果が正しくない[#45850](https://github.com/pingcap/tidb/issues/45850) @ [アイリンキッド](https://github.com/AilinKid)という問題を修正します。
    -   `INDEX_LOOKUP_HASH_JOIN` [#47788](https://github.com/pingcap/tidb/issues/47788) @ [シーライズ](https://github.com/SeaRise)でのメモリ使用量の推定が正しくない問題を修正
    -   `plan replayer`で生成された zip ファイルを TiDB [#46474](https://github.com/pingcap/tidb/issues/46474) @ [ヤンケオ](https://github.com/YangKeao)にインポートし直すことができない問題を修正
    -   `N` in `LIMIT N` [#43285](https://github.com/pingcap/tidb/issues/43285) @ [qw4990](https://github.com/qw4990)が大きすぎることによって引き起こされる誤ったコスト見積もりを修正しました。
    -   統計[#35948](https://github.com/pingcap/tidb/issues/35948) @ [こんにちはラスティン](https://github.com/hi-rustin)の TopN 構造を構築するときに発生する可能性があるpanicの問題を修正しました。
    -   MPP で計算した`COUNT(INT)`の結果が[#48643](https://github.com/pingcap/tidb/issues/48643) @ [アイリンキッド](https://github.com/AilinKid)と正しくない場合がある問題を修正
    -   `tidb_enable_ordered_result_mode`を有効にした場合にpanicが発生することがある問題を修正[#45044](https://github.com/pingcap/tidb/issues/45044) @ [qw4990](https://github.com/qw4990)
    -   ウィンドウ関数[#46177](https://github.com/pingcap/tidb/issues/46177) @ [qw4990](https://github.com/qw4990)によって導入される並べ替えを削減するために、オプティマイザーが誤って IndexFullScan を選択する問題を修正します。
    -   述語が共通テーブル式[#47881](https://github.com/pingcap/tidb/issues/47881) @ [ウィノロス](https://github.com/winoros)にプッシュダウンされると結果が正しくなくなることがある問題を修正
    -   最初のサブノードとして DUAL テーブルを使用して`UNION ALL`を実行すると、エラー[#48755](https://github.com/pingcap/tidb/issues/48755) @ [ウィノロス](https://github.com/winoros)が発生する可能性がある問題を修正します。
    -   特定の状況で列の枝刈りがpanicを引き起こす可能性がある問題を修正[#47331](https://github.com/pingcap/tidb/issues/47331) @ [こんにちはラスティン](https://github.com/hi-rustin)
    -   集計関数またはウィンドウ関数を含む共通テーブル式 (CTE) が他の再帰 CTE [#47603](https://github.com/pingcap/tidb/issues/47603) [#47711](https://github.com/pingcap/tidb/issues/47711) @ [エルサ0520](https://github.com/elsa0520)によって参照される場合に発生する可能性がある構文エラーの問題を修正します。
    -   プリペアドステートメント[#46817](https://github.com/pingcap/tidb/issues/46817) @ [ジャッキースプ](https://github.com/jackysp)で`QB_NAME`ヒントを使用すると例外が発生することがある問題を修正
    -   `AUTO_ID_CACHE=1` [#46324](https://github.com/pingcap/tidb/issues/46324) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)を使用する場合の Goroutine リークの問題を修正
    -   [#32110](https://github.com/pingcap/tidb/issues/32110) @ [7月2993](https://github.com/july2993)をシャットダウンするときに TiDB がpanicになる可能性がある問題を修正
    -   TiDB スキーマ キャッシュ[#48281](https://github.com/pingcap/tidb/issues/48281) @ [cfzjywxk](https://github.com/cfzjywxk)からスキーマ差分コミット バージョンを読み取るときに、MVCC インターフェイスでロックが処理されない問題を修正します。
    -   テーブル[#47064](https://github.com/pingcap/tidb/issues/47064) @ [ジフフスト](https://github.com/jiyfhust)の名前変更によって発生する`information_schema.columns`の重複行の問題を修正します。
    -   `LOAD DATA REPLACE INTO`ステートメントのバグを修正[#47995](https://github.com/pingcap/tidb/issues/47995) ) @ [ランス6716](https://github.com/lance6716)
    -   PDリーダーの誤動作により`IMPORT INTO`タスクが1分間失敗する問題を修正[#48307](https://github.com/pingcap/tidb/issues/48307) @ [D3ハンター](https://github.com/D3Hunter)
    -   日付型フィールド[#47426](https://github.com/pingcap/tidb/issues/47426) @ [タンジェンタ](https://github.com/tangenta)にインデックスを作成することによって発生する`ADMIN CHECK`の失敗の問題を修正します。
    -   `TABLESAMPLE` [#48253](https://github.com/pingcap/tidb/issues/48253) @ [タンジェンタ](https://github.com/tangenta)によって返されるソートされていない行データの問題を修正します。
    -   DDL `jobID`が 0 [#46296](https://github.com/pingcap/tidb/issues/46296) @ [ジフフスト](https://github.com/jiyfhust)に復元されるときに発生する TiDB ノードのpanic問題を修正

-   TiKV

    -   ピアを移動するとFollower Readのパフォーマンスが低下する可能性がある問題を修正[#15468](https://github.com/tikv/tikv/issues/15468) @ [ユジュンセン](https://github.com/YuJuncen)
    -   raftstore-applys [#15371](https://github.com/tikv/tikv/issues/15371) @ [コナー1996](https://github.com/Connor1996)が増加し続けるデータ エラーを修正
    -   オンライン ワークロード[#15565](https://github.com/tikv/tikv/issues/15565) @ [ランス6716](https://github.com/lance6716)があるときにTiDB Lightningチェックサム コプロセッサのリクエストがタイムアウトになる問題を修正
    -   バージョン`lz4-sys`を 1.9.4 [#15621](https://github.com/tikv/tikv/issues/15621) @ [SpadeA-Tang](https://github.com/SpadeA-Tang)にアップグレードして、セキュリティの問題を修正します
    -   バージョン`tokio`を 6.5 [#15621](https://github.com/tikv/tikv/issues/15621) @ [リククスサシネーター](https://github.com/LykxSassinator)にアップグレードして、セキュリティの問題を修正します
    -   `flatbuffer` [#15621](https://github.com/tikv/tikv/issues/15621) @ [トニーシュクキ](https://github.com/tonyxuqqi)を削除してセキュリティ問題を修正します
    -   TiKV ストアが[#15679](https://github.com/tikv/tikv/issues/15679) @ [ひっくり返る](https://github.com/hicqu)にパーティション化されている場合に、 resolved-tsラグが増加する問題を修正
    -   TiKV の再起動時に発生し、適用されていないRaftログが大量にある TiKV OOM 問題を修正します[#15770](https://github.com/tikv/tikv/issues/15770) @ [オーバーヴィーナス](https://github.com/overvenus)
    -   リージョンがマージされた後、古いピアが保持され、 resolved-ts がブロックされる問題を修正[#15919](https://github.com/tikv/tikv/issues/15919) @ [オーバーヴィーナス](https://github.com/overvenus)
    -   クラウド環境[#15832](https://github.com/tikv/tikv/issues/15832) @ [コナー1996](https://github.com/Connor1996)のGrafanaでスケジューラーコマンド変数が正しくない問題を修正
    -   Titanの`blob-run-mode`オンライン[#15978](https://github.com/tikv/tikv/issues/15978) @ [トニーシュクキ](https://github.com/tonyxuqqi)に更新できない問題を修正
    -   リージョン[#13311](https://github.com/tikv/tikv/issues/13311) @ [cfzjywxk](https://github.com/cfzjywxk)間のメタデータの不一致により TiKV がパニックになる問題を修正
    -   Online Unsafe Recovery [#15629](https://github.com/tikv/tikv/issues/15629) @ [コナー1996](https://github.com/Connor1996)中にリーダーが強制終了されると TiKV がパニックになる問題を修正
    -   [#15817](https://github.com/tikv/tikv/issues/15817) @ [コナー1996](https://github.com/Connor1996)のスケールアウト時に DR Auto-Sync のジョイント状態がタイムアウトになる可能性がある問題を修正
    -   Raftピア[#16069](https://github.com/tikv/tikv/issues/16069) @ [オーバーヴィーナス](https://github.com/overvenus)を削除するときに TiKV コプロセッサが古いデータを返す可能性がある問題を修正
    -   resolved-tsが 2 時間[#39130](https://github.com/pingcap/tidb/issues/39130) @ [オーバーヴィーナス](https://github.com/overvenus)ブロックされる可能性がある問題を修正
    -   `notLeader`または`regionNotFound` [#15712](https://github.com/tikv/tikv/issues/15712) @ [ヒューシャープ](https://github.com/HuSharp)に遭遇したときにフラッシュバックがスタックすることがある問題を修正

-   PD

    -   プラグインのディレクトリとファイルの潜在的なセキュリティ リスクを修正[#7094](https://github.com/tikv/pd/issues/7094) @ [ヒューシャープ](https://github.com/HuSharp)
    -   変更された分離レベルがデフォルトの配置ルール[#7121](https://github.com/tikv/pd/issues/7121) @ [ルルンクス](https://github.com/rleungx)に同期されない問題を修正します。
    -   `evict-leader-scheduler`が設定[#6897](https://github.com/tikv/pd/issues/6897) @ [ヒューシャープ](https://github.com/HuSharp)を失う可能性がある問題を修正
    -   空のリージョンをカウントする方法により、 BR [#7148](https://github.com/tikv/pd/issues/7148) @ [閉所性発熱](https://github.com/CabinfeverB)の回復プロセス中にリージョンのバランスが崩れる可能性がある問題を修正
    -   配置ルールの構成が複雑な場合、データ レプリケーション自動同期 (DR Auto-Sync) モードを採用しているクラスターで`canSync`と`hasMajority`正しく計算されないことがある問題を修正[#7201](https://github.com/tikv/pd/issues/7201) @ [ディスク化](https://github.com/disksing)
    -   データ レプリケーション自動同期 (DR Auto-Sync) モード[#7221](https://github.com/tikv/pd/issues/7221) @ [ディスク化](https://github.com/disksing)を採用しているクラスターで`available_stores`が正しく計算されない問題を修正します。
    -   データ レプリケーション自動同期 (DR Auto-Sync) モード[#7218](https://github.com/tikv/pd/issues/7218) @ [ディスク化](https://github.com/disksing)を採用しているクラスターでセカンダリ AZ がダウンしている場合、プライマリ AZ が TiKV ノードを追加できない問題を修正します。
    -   大規模なクラスターに複数の TiKV ノードを追加すると、TiKVハートビートレポートが遅くなったりスタックしたりする可能性がある問題を修正します[#7248](https://github.com/tikv/pd/issues/7248) @ [ルルンクス](https://github.com/rleungx)
    -   TiKV ノードが利用できない場合に PD が通常のピアを削除する可能性がある問題を修正[#7249](https://github.com/tikv/pd/issues/7249) @ [lhy1024](https://github.com/lhy1024)
    -   DR自動同期モード[#6988](https://github.com/tikv/pd/issues/6988) @ [ヒューシャープ](https://github.com/HuSharp)でリーダーの切り替えに時間がかかる問題を修正
    -   いくつかのセキュリティ問題を修正するには、Gin Web Framework のバージョンを v1.8.1 から v1.9.1 にアップグレードします[#7438](https://github.com/tikv/pd/issues/7438) @ [ニューベル](https://github.com/niubell)

-   TiFlash

    -   Grafana [#7713](https://github.com/pingcap/tiflash/issues/7713) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)で`max_snapshot_lifetime`メトリクスが正しく表示されない問題を修正
    -   `ALTER TABLE ... EXCHANGE PARTITION ...`ステートメントを実行するとpanic[#8372](https://github.com/pingcap/tiflash/issues/8372) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)が発生する問題を修正
    -   MemoryTracker によって報告されるメモリ使用量が不正確である問題を修正[#8128](https://github.com/pingcap/tiflash/issues/8128) @ [ジンヘリン](https://github.com/JinheLin)

-   ツール

    -   バックアップと復元 (BR)

        -   大きな幅のテーブル[#15714](https://github.com/tikv/tikv/issues/15714) @ [ユジュンセン](https://github.com/YuJuncen)をバックアップするときに、一部のシナリオでログ バックアップが停止する可能性がある問題を修正します。
        -   頻繁にフラッシュするとログのバックアップが停止する問題を修正します[#15602](https://github.com/tikv/tikv/issues/15602) @ [3ポインター](https://github.com/3pointer)
        -   EC2 メタデータ接続のリセット後の再試行により、バックアップと復元のパフォーマンスが低下する問題を修正します[#47650](https://github.com/pingcap/tidb/issues/47650) @ [レヴルス](https://github.com/Leavrth)
        -   1 分以内に PITR を複数回実行するとデータ損失[#15483](https://github.com/tikv/tikv/issues/15483) @ [ユジュンセン](https://github.com/YuJuncen)が発生する可能性がある問題を修正
        -   BR SQL コマンドと CLI のデフォルト値が異なるため、OOM の問題が発生する可能性があるという問題を修正します[#48000](https://github.com/pingcap/tidb/issues/48000) @ [ユジュンセン](https://github.com/YuJuncen)
        -   PD 所有者が[#47533](https://github.com/pingcap/tidb/issues/47533) @ [ユジュンセン](https://github.com/YuJuncen)に移管されるとログ バックアップがpanicになる問題を修正
        -   BR が外部storageファイル[#48452](https://github.com/pingcap/tidb/issues/48452) @ [3エースショーハンド](https://github.com/3AceShowHand)に対して間違った URI を生成する問題を修正

    -   TiCDC

        -   アップストリーム[#9739](https://github.com/pingcap/tiflow/issues/9739) @ [ひっくり返る](https://github.com/hicqu)で損失のある DDL ステートメントを実行すると TiCDCサーバーがpanic可能性がある問題を修正
        -   REDO ログ機能を有効にして`RESUME`を実行すると、レプリケーション タスクがエラーを報告する問題を修正します[#9769](https://github.com/pingcap/tiflow/issues/9769) @ [ひっくり返る](https://github.com/hicqu)
        -   TiKV ノードがクラッシュ[#9741](https://github.com/pingcap/tiflow/issues/9741) @ [スドジ](https://github.com/sdojjy)したときにレプリケーション ラグが長くなる問題を修正
        -   データを TiDB または MySQL [#9988](https://github.com/pingcap/tiflow/issues/9988) @ [東門](https://github.com/asddongmen)にレプリケートするときに、 `WHERE`ステートメントが条件として主キーを使用しない問題を修正します。
        -   レプリケーション タスクのワークロードが TiCDC ノード[#9839](https://github.com/pingcap/tiflow/issues/9839) @ [3エースショーハンド](https://github.com/3AceShowHand)全体に均等に分散されない問題を修正します。
        -   REDO ログが有効になっている場合に DDL ステートメントをレプリケートする間隔が長すぎる問題を修正します[#9960](https://github.com/pingcap/tiflow/issues/9960) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   ターゲットテーブルが削除され、アップストリーム[#10079](https://github.com/pingcap/tiflow/issues/10079) @ [東門](https://github.com/asddongmen)で再作成された場合、チェンジフィードが双方向レプリケーション モードで DML イベントをレプリケートできない問題を修正します。
        -   オブジェクトstorageサービス[#10041](https://github.com/pingcap/tiflow/issues/10041) @ [CharlesCheung96](https://github.com/CharlesCheung96)にデータをレプリケートするときに、NFS ファイルが多すぎるためにレプリケーション ラグが長くなる問題を修正します。
        -   データをオブジェクトstorageサービス[#10137](https://github.com/pingcap/tiflow/issues/10137) @ [スドジ](https://github.com/sdojjy)にレプリケートするときに TiCDCサーバーがpanicになる可能性がある問題を修正します。
        -   PD のスケールアップおよびスケールダウン中に TiCDC が無効な古いアドレスにアクセスする問題を修正します[#9584](https://github.com/pingcap/tiflow/issues/9584) @ [フビンジ](https://github.com/fubinzh) @ [東門](https://github.com/asddongmen)
        -   一部のオペレーティング システム[#9762](https://github.com/pingcap/tiflow/issues/9762) @ [スドジ](https://github.com/sdojjy)で、間違ったメモリ情報を取得すると OOM の問題が発生する可能性がある問題を修正します。

    -   TiDB データ移行 (DM)

        -   DM が楽観的モード[#9788](https://github.com/pingcap/tiflow/issues/9788) @ [GMHDBJD](https://github.com/GMHDBJD)でパーティション DDL をスキップする問題を修正
        -   オンライン DDL [#9587](https://github.com/pingcap/tiflow/issues/9587) @ [GMHDBJD](https://github.com/GMHDBJD)をスキップすると、DM がアップストリーム テーブル スキーマを適切に追跡できない問題を修正します。
        -   失敗した DDL がスキップされ、後続の DDL が実行されない場合、DM から返されるレプリケーション ラグが増大し続ける問題を修正します[#9605](https://github.com/pingcap/tiflow/issues/9605) @ [D3ハンター](https://github.com/D3Hunter)
        -   楽観的モード[#9588](https://github.com/pingcap/tiflow/issues/9588) @ [GMHDBJD](https://github.com/GMHDBJD)でタスクを再開すると、DM がすべての DML をスキップする問題を修正します。

    -   TiDB Lightning

        -   `write to tikv with no leader returned`エラー[#45673](https://github.com/pingcap/tidb/issues/45673) @ [ランス6716](https://github.com/lance6716)が発生するとデータのインポートが失敗する問題を修正
        -   HTTP 再試行リクエストが現在のリクエスト コンテンツ[#47930](https://github.com/pingcap/tidb/issues/47930) @ [ランス6716](https://github.com/lance6716)を使用しないため、データのインポートが失敗する問題を修正します。
        -   TiDB Lightningが`writeToTiKV` [#46321](https://github.com/pingcap/tidb/issues/46321) @ [ランス6716](https://github.com/lance6716)中にスタックする問題を修正
        -   物理インポートモード[#45507](https://github.com/pingcap/tidb/issues/45507) @ [ミタルリシャブ](https://github.com/mittalrishabh)で不要な`get_regions`コールを削除

    -   TiDBBinlog

        -   1 GB [#28659](https://github.com/pingcap/tidb/issues/28659) @ [ジャッキースプ](https://github.com/jackysp)を超えるトランザクションを転送するときにDrainerが終了する問題を修正
