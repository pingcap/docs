---
title: TiDB 7.1.3 Release Notes
summary: TiDB 7.1.3は2023年12月21日にリリースされました。このバージョンでは、TiCDC Changefeed構成項目のデフォルト値が変更され、新しい構成項目が導入されました。また、TiDB、PD、ツール、TiCDC、TiDB Lightning、TiKV、TiFlashなどの改善点やバグの修正が含まれています。
---

# TiDB 7.1.3 リリースノート {#tidb-7-1-3-release-notes}

発売日：2023年12月21日

TiDB バージョン: 7.1.3

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup) | [インストールパッケージ](https://www.pingcap.com/download/?version=v7.1.3#version-list)

## 互換性の変更 {#compatibility-changes}

-   さらにテストを行った後、 TiCDC Changefeed構成項目[`case-sensitive`](/ticdc/ticdc-changefeed-config.md)のデフォルト値が`true`から`false`に変更されました。これは、デフォルトでは、TiCDC 構成ファイル内のテーブル名とデータベース名は大文字と小文字が区別されないことを意味します[#10047](https://github.com/pingcap/tiflow/issues/10047) @ [スドジ](https://github.com/sdojjy)
-   TiCDC Changefeed、次の新しい構成項目が導入されています。
    -   [`sql-mode`](/ticdc/ticdc-changefeed-config.md) : TiCDC がデータ[#9876](https://github.com/pingcap/tiflow/issues/9876) @ [東門](https://github.com/asddongmen)を複製するときに TiCDC が DDL ステートメントを解析するために使用する[SQLモード](/ticdc/ticdc-ddl.md#sql-mode)を設定できるようにします。
    -   [`encoding-worker-num`](/ticdc/ticdc-changefeed-config.md)および[`flush-worker-num`](/ticdc/ticdc-changefeed-config.md) : さまざまなマシン[#10048](https://github.com/pingcap/tiflow/issues/10048) @ [CharlesCheung96](https://github.com/CharlesCheung96)の仕様に基づいて、REDO モジュールのさまざまな同時実行パラメータを設定できます。
    -   [`compression`](/ticdc/ticdc-changefeed-config.md) : REDO ログ ファイル[#10176](https://github.com/pingcap/tiflow/issues/10176) @ [スドジ](https://github.com/sdojjy)の圧縮動作を構成できます。
    -   [`sink.cloud-storage-config`](/ticdc/ticdc-changefeed-config.md) : データをオブジェクトstorage[#10109](https://github.com/pingcap/tiflow/issues/10109) @ [CharlesCheung96](https://github.com/CharlesCheung96)にレプリケートするときに、履歴データの自動クリーンアップを設定できます。

## 改善点 {#improvements}

-   TiDB

    -   [`FLASHBACK CLUSTER TO TSO`](https://docs.pingcap.com/tidb/v7.1/sql-statement-flashback-cluster)構文[#48372](https://github.com/pingcap/tidb/issues/48372) @ [ボーンチェンジャー](https://github.com/BornChanger)をサポートします

-   PD

    -   リソース制御クライアントの構成取得方法を強化し、最新の構成を動的に取得できるようにしました[#7043](https://github.com/tikv/pd/issues/7043) @ [ノールーシュ](https://github.com/nolouch)

-   ツール

    -   バックアップと復元 (BR)

        -   タイムアウト障害が発生した場合、またはリージョンスキャッター[#47236](https://github.com/pingcap/tidb/issues/47236) @ [レヴルス](https://github.com/Leavrth)のキャンセルが発生した場合、スナップショットのリカバリ中にリージョンスキャッターの自動再試行を有効にします。
        -   スナップショット バックアップの復元中に、特定のネットワーク エラーが発生すると、 BR は再試行します[#48528](https://github.com/pingcap/tidb/issues/48528) @ [レヴルス](https://github.com/Leavrth)
        -   `delete range`シナリオにポイントインタイム リカバリ (PITR) の新しい統合テストを導入し、PITR の安定性を強化します[#47738](https://github.com/pingcap/tidb/issues/47738) @ [レヴルス](https://github.com/Leavrth)

    -   TiCDC

        -   TiCDC ノードがデータを TiDB [#9935](https://github.com/pingcap/tiflow/issues/9935) @ [3エースショーハンド](https://github.com/3AceShowHand)に複製するときのメモリ消費を最適化します。
        -   一部のアラーム ルール[#9266](https://github.com/pingcap/tiflow/issues/9266) @ [東門](https://github.com/asddongmen)を最適化します。
        -   S3 へのデータの並列書き込みや lz4 圧縮アルゴリズム[#10176](https://github.com/pingcap/tiflow/issues/10176) [#10226](https://github.com/pingcap/tiflow/issues/10226) @ [スドジ](https://github.com/sdojjy)の採用など、REDO ログのパフォーマンスを最適化します。
        -   並列処理[#10098](https://github.com/pingcap/tiflow/issues/10098) @ [CharlesCheung96](https://github.com/CharlesCheung96)を増やすことで、データをオブジェクトstorageにレプリケートする TiCDC のパフォーマンスを向上させます。
        -   アップストリーム TiKV [#11390](https://github.com/tikv/tikv/issues/11390) @ [ひっくり返る](https://github.com/hicqu)に対する TiCDC インクリメンタル スキャンの影響を軽減します。
        -   `sink-uri`構成[#10106](https://github.com/pingcap/tiflow/issues/10106) @ [3エースショーハンド](https://github.com/3AceShowHand)で`content-compatible=true`を設定することにより、 TiCDC Canal-JSON コンテンツ形式[公式の Canal 出力のコンテンツ形式と互換性があります](https://docs.pingcap.com/tidb/v6.5/ticdc-canal-json#compatibility-with-the-official-canal)の作成をサポート

    -   TiDB Lightning

        -   PD リーダー変更[#45301](https://github.com/pingcap/tidb/issues/45301) @ [ランス6716](https://github.com/lance6716)による`GetTS`失敗に対する再試行メカニズムを追加

## バグの修正 {#bug-fixes}

-   TiDB

    -   メモリ制限[#49096](https://github.com/pingcap/tidb/issues/49096) @ [アイリンキッド](https://github.com/AilinKid%7D)を超えると、共通テーブル式 (CTE) を含むクエリが予期せずスタックする問題を修正します。
    -   `tidb_server_memory_limit` [#48741](https://github.com/pingcap/tidb/issues/48741) @ [徐淮嶼](https://github.com/XuHuaiyu)による長期的なメモリ負荷により TiDB の CPU 使用率が高くなる問題を修正
    -   `tidb_max_chunk_size`が小さい値[#48808](https://github.com/pingcap/tidb/issues/48808) @ [グオシャオゲ](https://github.com/guo-shaoge)に設定されている場合、CTE を含むクエリで`runtime error: index out of range [32] with length 32`が報告される問題を修正します。
    -   `ENUM`型のカラムを結合キー[#48991](https://github.com/pingcap/tidb/issues/48991) @ [ウィノロス](https://github.com/winoros)として使用した場合、クエリ結果が正しくない問題を修正
    -   再帰 CTE [#47711](https://github.com/pingcap/tidb/issues/47711) @ [エルサ0520](https://github.com/elsa0520)の集計関数またはウィンドウ関数によって引き起こされる解析エラーを修正しました。
    -   `UPDATE`ステートメントが誤って PointGet [#47445](https://github.com/pingcap/tidb/issues/47445) @ [こんにちはラスティン](https://github.com/hi-rustin)に変換される可能性がある問題を修正
    -   TiDB が`stats_history`テーブル[#48431](https://github.com/pingcap/tidb/issues/48431) @ [ホーキングレイ](https://github.com/hawkingrei)でガベージコレクションを実行するときに発生する可能性がある OOM 問題を修正します。
    -   同じクエリ プランに異なる`PLAN_DIGEST`値、場合によっては[#47634](https://github.com/pingcap/tidb/issues/47634) @ [キングディラン](https://github.com/King-Dylan)含まれる問題を修正
    -   大量のメモリを消費する[#47779](https://github.com/pingcap/tidb/issues/47779) @ [ホーキングレイ](https://github.com/hawkingrei)のときに`GenJSONTableFromStats`強制終了できない問題を修正
    -   述語が共通テーブル式[#47881](https://github.com/pingcap/tidb/issues/47881) @ [ウィノロス](https://github.com/winoros)にプッシュダウンされると結果が正しくなくなることがある問題を修正
    -   `AUTO_ID_CACHE=1`を[#46444](https://github.com/pingcap/tidb/issues/46444) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)に設定すると`Duplicate entry`発生する場合がある問題を修正
    -   監査ログ用のエンタープライズ プラグインが使用されている場合、TiDBサーバーが大量のリソースを消費する可能性がある問題を修正[#49273](https://github.com/pingcap/tidb/issues/49273) @ [ルクワンチャオ](https://github.com/lcwangchao)
    -   正常なシャットダウン[#36793](https://github.com/pingcap/tidb/issues/36793) @ [bb7133](https://github.com/bb7133)中に TiDBサーバーがpanicになる可能性がある問題を修正
    -   多数のテーブル[#48869](https://github.com/pingcap/tidb/issues/48869) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)がある場合、 `AUTO_ID_CACHE=1`テーブルによって gRPC クライアント リークが発生する可能性がある問題を修正します。
    -   `ErrLoadDataInvalidURI` (無効な S3 URI エラー) [#48164](https://github.com/pingcap/tidb/issues/48164) @ [ランス6716](https://github.com/lance6716)の誤ったエラー メッセージを修正しました。
    -   パーティション列タイプが`DATETIME` [#48814](https://github.com/pingcap/tidb/issues/48814) @ [クレイジークス520](https://github.com/crazycs520)の場合、 `ALTER TABLE ... LAST PARTITION`の実行が失敗する問題を修正
    -   `IMPORT INTO`実行中の実際のエラー メッセージが他のエラー メッセージ[#47992](https://github.com/pingcap/tidb/issues/47992) [#47781](https://github.com/pingcap/tidb/issues/47781) @ [D3ハンター](https://github.com/D3Hunter)によって上書きされる可能性がある問題を修正します。
    -   cgroup v2 コンテナにデプロイされた TiDB が検出できない問題を修正[#48342](https://github.com/pingcap/tidb/issues/48342) @ [D3ハンター](https://github.com/D3Hunter)
    -   最初のサブノードとして DUAL テーブルを使用して`UNION ALL`を実行すると、エラー[#48755](https://github.com/pingcap/tidb/issues/48755) @ [ウィノロス](https://github.com/winoros)が発生する可能性がある問題を修正します。
    -   DDL `jobID`が 0 [#46296](https://github.com/pingcap/tidb/issues/46296) @ [ジフフスト](https://github.com/jiyfhust)に復元されるときに発生する TiDB ノードのpanic問題を修正
    -   `TABLESAMPLE` [#48253](https://github.com/pingcap/tidb/issues/48253) @ [タンジェンタ](https://github.com/tangenta)によって返されるソートされていない行データの問題を修正します。
    -   `tidb_enable_ordered_result_mode`を有効にした場合にpanicが発生することがある問題を修正[#45044](https://github.com/pingcap/tidb/issues/45044) @ [qw4990](https://github.com/qw4990)
    -   ウィンドウ関数[#46177](https://github.com/pingcap/tidb/issues/46177) @ [qw4990](https://github.com/qw4990)によって導入される並べ替えを削減するために、オプティマイザーが誤って IndexFullScan を選択する問題を修正します。
    -   TiDB スキーマ キャッシュ[#48281](https://github.com/pingcap/tidb/issues/48281) @ [cfzjywxk](https://github.com/cfzjywxk)からスキーマ差分コミット バージョンを読み取るときに、MVCC インターフェイスでロックが処理されない問題を修正します。
    -   `INDEX_LOOKUP_HASH_JOIN` [#47788](https://github.com/pingcap/tidb/issues/47788) @ [シーライズ](https://github.com/SeaRise)でのメモリ使用量の推定が正しくない問題を修正
    -   PDリーダーの誤動作により`IMPORT INTO`タスクが1分間失敗する問題を修正[#48307](https://github.com/pingcap/tidb/issues/48307) @ [D3ハンター](https://github.com/D3Hunter)
    -   `batch-client` `client-go` @ [クレイジークス520](https://github.com/crazycs520) [#47691](https://github.com/pingcap/tidb/issues/47691)panicの問題を修正
    -   特定の状況で列の枝刈りがpanicを引き起こす可能性がある問題を修正[#47331](https://github.com/pingcap/tidb/issues/47331) @ [こんにちはラスティン](https://github.com/hi-rustin)
    -   TiDB が`systemd` [#47442](https://github.com/pingcap/tidb/issues/47442) @ [ホーキングレイ](https://github.com/hawkingrei)で起動されたときに`cgroup`リソース制限を読み込まない問題を修正
    -   集計関数またはウィンドウ関数を含む共通テーブル式 (CTE) が他の再帰 CTE [#47603](https://github.com/pingcap/tidb/issues/47603) [#47711](https://github.com/pingcap/tidb/issues/47711) @ [エルサ0520](https://github.com/elsa0520)によって参照される場合に発生する可能性がある構文エラーの問題を修正します。
    -   統計[#35948](https://github.com/pingcap/tidb/issues/35948) @ [こんにちはラスティン](https://github.com/hi-rustin)の TopN 構造を構築するときに発生する可能性があるpanicの問題を修正しました。
    -   MPP で計算した`COUNT(INT)`の結果が[#48643](https://github.com/pingcap/tidb/issues/48643) @ [アイリンキッド](https://github.com/AilinKid)と正しくない場合がある問題を修正
    -   HashJoin オペレーターがプローブ[#48082](https://github.com/pingcap/tidb/issues/48082) @ [wshwsh12](https://github.com/wshwsh12)を実行するとチャンクが再利用できない問題を修正

-   TiKV

    -   TiKV の実行が非常に遅い場合、リージョンマージ[#16111](https://github.com/tikv/tikv/issues/16111) @ [オーバーヴィーナス](https://github.com/overvenus)後にpanicが発生する可能性がある問題を修正
    -   解決済み TS が 2 時間ブロックされる可能性がある問題を修正[#15520](https://github.com/tikv/tikv/issues/15520) [#39130](https://github.com/pingcap/tidb/issues/39130) @ [オーバーヴィーナス](https://github.com/overvenus)
    -   raft ログ[#15800](https://github.com/tikv/tikv/issues/15800) @ [トニーシュクキ](https://github.com/tonyxuqqi)を追加できないため、TiKV が`ServerIsBusy`エラーを報告する問題を修正します。
    -   BR が[#15684](https://github.com/tikv/tikv/issues/15684) @ [ユジュンセン](https://github.com/YuJuncen)でクラッシュすると、スナップショットの復元が停止する可能性がある問題を修正
    -   大規模なトランザクション[#14864](https://github.com/tikv/tikv/issues/14864) @ [オーバーヴィーナス](https://github.com/overvenus)を追跡するときに、古い読み取りの解決された TS によって TiKV OOM の問題が発生する可能性がある問題を修正
    -   破損した SST ファイルが他の TiKV ノード[#15986](https://github.com/tikv/tikv/issues/15986) @ [コナー1996](https://github.com/Connor1996)に拡散する可能性がある問題を修正
    -   [#15817](https://github.com/tikv/tikv/issues/15817) @ [コナー1996](https://github.com/Connor1996)のスケールアウト時に DR Auto-Sync のジョイント状態がタイムアウトになる可能性がある問題を修正
    -   クラウド環境[#15832](https://github.com/tikv/tikv/issues/15832) @ [コナー1996](https://github.com/Connor1996)のGrafanaでスケジューラーコマンド変数が正しくない問題を修正
    -   リージョンがマージされた後、古いピアが保持され、 resolved-ts がブロックされる問題を修正[#15919](https://github.com/tikv/tikv/issues/15919) @ [オーバーヴィーナス](https://github.com/overvenus)
    -   Online Unsafe Recovery がマージ中止[#15580](https://github.com/tikv/tikv/issues/15580) @ [v01dstar](https://github.com/v01dstar)を処理できない問題を修正
    -   TiKV の再起動時に発生し、適用されていないRaftログが大量にある TiKV OOM 問題を修正します[#15770](https://github.com/tikv/tikv/issues/15770) @ [オーバーヴィーナス](https://github.com/overvenus)
    -   バージョン`lz4-sys`を 1.9.4 [#15621](https://github.com/tikv/tikv/issues/15621) @ [SpadeA-Tang](https://github.com/SpadeA-Tang)にアップグレードして、セキュリティの問題を修正します
    -   Titanの`blob-run-mode`オンライン[#15978](https://github.com/tikv/tikv/issues/15978) @ [トニーシュクキ](https://github.com/tonyxuqqi)に更新できない問題を修正
    -   PD と TiKV の間のネットワークの中断により PITR がスタックする可能性がある問題を修正します[#15279](https://github.com/tikv/tikv/issues/15279) @ [ユジュンセン](https://github.com/YuJuncen)
    -   Raftピア[#16069](https://github.com/tikv/tikv/issues/16069) @ [オーバーヴィーナス](https://github.com/overvenus)を削除するときに TiKV コプロセッサが古いデータを返す可能性がある問題を修正

-   PD

    -   `CALIBRATE RESOURCE` [#45166](https://github.com/pingcap/tidb/issues/45166) @ [キャビンフィーバーB](https://github.com/CabinfeverB)を実行すると、TiDB ダッシュボードで`resource_manager_resource_unit`メトリクスが空になる問題を修正
    -   [ワークロードによる調整] ページでエラー[#48162](https://github.com/pingcap/tidb/issues/48162) @ [キャビンフィーバーB](https://github.com/CabinfeverB)が報告される問題を修正します。
    -   リソース グループを削除すると DDL アトミック性[#45050](https://github.com/pingcap/tidb/issues/45050) @ [グロルフ](https://github.com/glorv)が損傷する可能性がある問題を修正します。
    -   PD リーダーが移動され、新しいリーダーと PD クライアントの間にネットワーク分割がある場合、PD クライアントがリーダー[#7416](https://github.com/tikv/pd/issues/7416) @ [キャビンフィーバーB](https://github.com/CabinfeverB)の情報を更新できない問題を修正します
    -   大規模なクラスターに複数の TiKV ノードを追加すると、TiKVハートビートレポートが遅くなったりスタックしたりする可能性がある問題を修正します[#7248](https://github.com/tikv/pd/issues/7248) @ [ルルンクス](https://github.com/rleungx)
    -   TiDB ダッシュボードが PD `trace`データを正しく読み取れない問題を修正[#7253](https://github.com/tikv/pd/issues/7253) @ [ノールーシュ](https://github.com/nolouch)
    -   Jin Web Framework のバージョンを v1.8.1 から v1.9.1 [#7438](https://github.com/tikv/pd/issues/7438) @ [ニューベル](https://github.com/niubell)にアップグレードすることで、いくつかのセキュリティ問題を修正します。
    -   ルール チェッカーが配置ルール[#7185](https://github.com/tikv/pd/issues/7185) @ [ノールーシュ](https://github.com/nolouch)の設定に従って学習者を追加しない問題を修正
    -   TiKV ノードが利用できない場合に PD が通常のピアを削除する可能性がある問題を修正[#7249](https://github.com/tikv/pd/issues/7249) @ [lhy1024](https://github.com/lhy1024)
    -   DR自動同期モード[#6988](https://github.com/tikv/pd/issues/6988) @ [ヒューシャープ](https://github.com/HuSharp)でリーダーの切り替えに時間がかかる問題を修正

-   TiFlash

    -   `ALTER TABLE ... EXCHANGE PARTITION ...`ステートメントを実行するとpanic[#8372](https://github.com/pingcap/tiflash/issues/8372) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)が発生する問題を修正
    -   TiFlash がクエリ[#8447](https://github.com/pingcap/tiflash/issues/8447) @ [ジンヘリン](https://github.com/JinheLin)中にメモリ制限に遭遇した場合のメモリリークの問題を修正
    -   `FLASHBACK DATABASE` [#8450](https://github.com/pingcap/tiflash/issues/8450) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)を実行した後もTiFlashレプリカのデータがガベージ コレクションされる問題を修正
    -   Grafana [#8076](https://github.com/pingcap/tiflash/issues/8076) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)の一部のパネルの最大パーセンタイル時間の誤った表示を修正
    -   クエリが予期しないエラー メッセージ「FineGrainedShuffleWriter-V1 のブロック スキーマの不一致」を返す問題を修正します[#8111](https://github.com/pingcap/tiflash/issues/8111) @ [シーライズ](https://github.com/SeaRise)

-   ツール

    -   バックアップと復元 (BR)

        -   BR SQL コマンドと CLI のデフォルト値が異なるため、OOM の問題が発生する可能性があるという問題を修正します[#48000](https://github.com/pingcap/tidb/issues/48000) @ [ユジュンセン](https://github.com/YuJuncen)
        -   大きな幅のテーブル[#15714](https://github.com/tikv/tikv/issues/15714) @ [ユジュンセン](https://github.com/YuJuncen)をバックアップするときに、一部のシナリオでログ バックアップが停止する可能性がある問題を修正します。
        -   BR が外部storageファイル[#48452](https://github.com/pingcap/tidb/issues/48452) @ [3エースショーハンド](https://github.com/3AceShowHand)に対して間違った URI を生成する問題を修正
        -   EC2 メタデータ接続のリセット後の再試行により、バックアップと復元のパフォーマンスが低下する問題を修正します[#47650](https://github.com/pingcap/tidb/issues/47650) @ [レヴルス](https://github.com/Leavrth)
        -   タスクの初期化中に PD への接続に失敗すると、ログ バックアップ タスクが開始できるが、正しく動作しない問題を修正[#16056](https://github.com/tikv/tikv/issues/16056) @ [ユジュンセン](https://github.com/YuJuncen)

    -   TiCDC

        -   特定のシナリオ[#9812](https://github.com/pingcap/tiflow/issues/9812) @ [東門](https://github.com/asddongmen)で`DELETE`ステートメントをレプリケートするときに、 `WHERE`句が条件として主キーを使用しない問題を修正します。
        -   データをオブジェクトstorage[#10041](https://github.com/pingcap/tiflow/issues/10041) [#10044](https://github.com/pingcap/tiflow/issues/10044) @ [CharlesCheung96](https://github.com/CharlesCheung96)にレプリケートするときに、特定の特殊なシナリオでレプリケーション タスクがスタックする問題を修正します。
        -   同期ポイントとやり直しログ[#10091](https://github.com/pingcap/tiflow/issues/10091) @ [CharlesCheung96](https://github.com/CharlesCheung96)を有効にした後、特定の特殊なシナリオでレプリケーション タスクがスタックする問題を修正します。
        -   特定の特別なシナリオ[#10239](https://github.com/pingcap/tiflow/issues/10239) @ [ひっくり返る](https://github.com/hicqu)で、TiCDC が誤って TiKV との接続を閉じる問題を修正します。
        -   ターゲットテーブルが削除され、アップストリーム[#10079](https://github.com/pingcap/tiflow/issues/10079) @ [東門](https://github.com/asddongmen)で再作成された場合、チェンジフィードが双方向レプリケーション モードで DML イベントをレプリケートできない問題を修正します。
        -   データをオブジェクト ストア シンク[#10041](https://github.com/pingcap/tiflow/issues/10041) @ [CharlesCheung96](https://github.com/CharlesCheung96)にレプリケートするときに NFS ディレクトリにアクセスすることによって発生するパフォーマンスの問題を修正します。
        -   データをオブジェクトstorageサービス[#10137](https://github.com/pingcap/tiflow/issues/10137) @ [スドジ](https://github.com/sdojjy)にレプリケートするときに TiCDCサーバーがpanicになる可能性がある問題を修正します。
        -   REDO ログが有効になっている場合に DDL ステートメントをレプリケートする間隔が長すぎる問題を修正します[#9960](https://github.com/pingcap/tiflow/issues/9960) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   REDO ログが有効になっている場合に、NFS 障害が原因でオーナー ノードがスタックする問題を修正[#9886](https://github.com/pingcap/tiflow/issues/9886) @ [3エースショーハンド](https://github.com/3AceShowHand)

    -   TiDB データ移行 (DM)

        -   `CompareGTID` [#9676](https://github.com/pingcap/tiflow/issues/9676) @ [GMHDBJD](https://github.com/GMHDBJD)に不適切なアルゴリズムが使用されたため、DM のパフォーマンスが低下する問題を修正

    -   TiDB Lightning

        -   PD リーダーが強制終了されているか、PD リクエストの処理が遅いためにデータのインポートが失敗する問題を修正[#46950](https://github.com/pingcap/tidb/issues/46950) [#48075](https://github.com/pingcap/tidb/issues/48075) @ [D3ハンター](https://github.com/D3Hunter)
        -   TiDB Lightning が`writeToTiKV` [#46321](https://github.com/pingcap/tidb/issues/46321) [#48352](https://github.com/pingcap/tidb/issues/48352) @ [ランス6716](https://github.com/lance6716)中にスタックする問題を修正
        -   HTTP 再試行リクエストが現在のリクエスト コンテンツ[#47930](https://github.com/pingcap/tidb/issues/47930) @ [ランス6716](https://github.com/lance6716)を使用しないため、データのインポートが失敗する問題を修正します。
        -   物理インポートモード[#45507](https://github.com/pingcap/tidb/issues/45507) @ [ミタルリシャブ](https://github.com/mittalrishabh)で不要な`get_regions`コールを削除
