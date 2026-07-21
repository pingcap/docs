---
title: TiDB 7.1.3 Release Notes
summary: TiDB 7.1.3 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 7.1.3 リリースノート {#tidb-7-1-3-release-notes}

発売日：2023年12月21日

TiDB バージョン: 7.1.3

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   さらなるテストの結果、 TiCDC Changefeed構成項目[`case-sensitive`](/ticdc/ticdc-changefeed-config.md)のデフォルト値が`true`から`false`に変更されました。これは、デフォルトでは TiCDC 構成ファイル内のテーブル名とデータベース名が大文字と小文字を区別しないことを意味します[＃10047](https://github.com/pingcap/tiflow/issues/10047) @ [sdojjy](https://github.com/sdojjy)
-   TiCDC Changefeed、次の新しい構成項目が導入されています。
    -   [`sql-mode`](/ticdc/ticdc-changefeed-config.md) : TiCDC がデータを複製するときに DDL ステートメントを解析するために使用する[SQLモード](https://docs.pingcap.com/tidb/v7.1/ticdc-ddl#sql-mode)設定できます[＃9876](https://github.com/pingcap/tiflow/issues/9876) @ [asddongmen](https://github.com/asddongmen)
    -   [`encoding-worker-num`](/ticdc/ticdc-changefeed-config.md)と[`flush-worker-num`](/ticdc/ticdc-changefeed-config.md) : 異なるマシンの仕様に基づいて、再実行モジュールに異なる同時実行パラメータを設定できます[＃10048](https://github.com/pingcap/tiflow/issues/10048) @ [CharlesCheung96](https://github.com/CharlesCheung96)
    -   [`compression`](/ticdc/ticdc-changefeed-config.md) : REDOログファイルの圧縮動作を設定できます[＃10176](https://github.com/pingcap/tiflow/issues/10176) @ [sdojjy](https://github.com/sdojjy)
    -   [`sink.cloud-storage-config`](/ticdc/ticdc-changefeed-config.md) : オブジェクトストレージにデータを複製するときに履歴データの自動クリーンアップを設定できます[チャールズ・チュン96](https://github.com/CharlesCheung96) [＃10109](https://github.com/pingcap/tiflow/issues/10109)

## 改善点 {#improvements}

-   TiDB

    -   [`FLASHBACK CLUSTER TO TSO`](https://docs.pingcap.com/tidb/v7.1/sql-statement-flashback-cluster)構文をサポート [＃48372](https://github.com/pingcap/tidb/issues/48372) @ [BornChanger](https://github.com/BornChanger)

-   PD

    -   リソース制御クライアントの構成取得方法を強化し、最新の構成を動的に取得する[＃7043](https://github.com/tikv/pd/issues/7043) @ [nolouch](https://github.com/nolouch)

-   ツール

    -   Backup & Restore (BR)

        -   タイムアウトエラーまたはリージョンスキャッタのキャンセルが発生した場合に、スナップショットリカバリ中にリージョンスキャッタの自動再試行を有効にする [＃47236](https://github.com/pingcap/tidb/issues/47236) @ [Leavrth](https://github.com/Leavrth)
        -   スナップショットバックアップの復元中に、 BRは特定のネットワークエラーが発生すると再試行します[＃48528](https://github.com/pingcap/tidb/issues/48528) @ [Leavrth](https://github.com/Leavrth)
        -   `delete range`シナリオで Point-In-Time Recovery (PITR) の新しい統合テストを導入し、PITR の安定性を強化します。 [＃47738](https://github.com/pingcap/tidb/issues/47738) @ [Leavrth](https://github.com/Leavrth)

    -   TiCDC

        -   TiCDCノードがTiDB にデータを複製する際のメモリ消費を最適化します [＃9935](https://github.com/pingcap/tiflow/issues/9935) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   いくつかのアラームルールを最適化[＃9266](https://github.com/pingcap/tiflow/issues/9266) @ [asddongmen](https://github.com/asddongmen)
        -   S3へのデータの並列書き込みやlz4圧縮アルゴリズムの採用など、REDOログのパフォーマンスを最適化します[＃10176](https://github.com/pingcap/tiflow/issues/10176) [＃10226](https://github.com/pingcap/tiflow/issues/10226) @ [sdojjy](https://github.com/sdojjy)
        -   並列度を増やすことで、TiCDC がオブジェクトストレージにデータを複製する際のパフォーマンスが向上します。 [＃10098](https://github.com/pingcap/tiflow/issues/10098) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   TiCDC 増分スキャンによる上流 TiKV への影響を軽減 [＃11390](https://github.com/tikv/tikv/issues/11390) @ [hicqu](https://github.com/hicqu)
        -   `sink-uri`構成で`content-compatible=true`設定することにより、 TiCDC Canal-JSON コンテンツ フォーマット[公式Canal出力のコンテンツ形式と互換性がある](https://docs.pingcap.com/tidb/v6.5/ticdc-canal-json#compatibility-with-the-official-canal)作成をサポートします。 [＃10106](https://github.com/pingcap/tiflow/issues/10106) @ [3AceShowHand](https://github.com/3AceShowHand)

    -   TiDB Lightning

        -   PDリーダーの変更による`GetTS`失敗に対して再試行メカニズムを追加（ @ [lance6716](https://github.com/lance6716) [＃45301](https://github.com/pingcap/tidb/issues/45301)

## バグ修正 {#bug-fixes}

-   TiDB

    -   共通テーブル式 (CTE) を含むクエリがメモリ制限を超えたときに予期せず停止する問題を修正[＃49096](https://github.com/pingcap/tidb/issues/49096) @ [AilinKid](https://github.com/AilinKid)
    -   `tidb_server_memory_limit` による長期メモリ圧迫により TiDB の CPU 使用率が上昇する問題を修正 [＃48741](https://github.com/pingcap/tidb/issues/48741) @ [XuHuaiyu](https://github.com/XuHuaiyu)
    -   CTE を含むクエリが、 `tidb_max_chunk_size`小さい値に設定されている場合に`runtime error: index out of range [32] with length 32`報告する問題を修正しました。 [＃48808](https://github.com/pingcap/tidb/issues/48808) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   `ENUM`型の列を結合キーとして使用した場合にクエリ結果が正しくない問題を修正しました [＃48991](https://github.com/pingcap/tidb/issues/48991) @ [winoros](https://github.com/winoros)
    -   再帰CTE 内の集計関数またはウィンドウ関数によって発生する解析エラーを修正 [＃47711](https://github.com/pingcap/tidb/issues/47711) @ [elsa0520](https://github.com/elsa0520)
    -   `UPDATE`文が PointGet に誤って変換される可能性がある問題を修正しました [＃47445](https://github.com/pingcap/tidb/issues/47445) @ [Rustin170506](https://github.com/Rustin170506)
    -   TiDBが`stats_history`テーブルでガベージコレクションを実行するときに発生する可能性のあるOOM問題を修正しました。 [＃48431](https://github.com/pingcap/tidb/issues/48431) @ [hawkingrei](https://github.com/hawkingrei)
    -   同じクエリプランで、場合によってはの異なる`PLAN_DIGEST`値が発生する問題を修正しました [＃47634](https://github.com/pingcap/tidb/issues/47634) @ [King-Dylan](https://github.com/King-Dylan)
    -   `GenJSONTableFromStats`大量のメモリを消費すると強制終了できない問題を修正[＃47779](https://github.com/pingcap/tidb/issues/47779) @ [hawkingrei](https://github.com/hawkingrei)
    -   述語が共通テーブル式にプッシュダウンされたときに結果が不正確になる可能性がある問題を修正しました [＃47881](https://github.com/pingcap/tidb/issues/47881) @ [winoros](https://github.com/winoros)
    -   `AUTO_ID_CACHE=1` に設定されている場合に`Duplicate entry`発生する可能性がある問題を修正しました [＃46444](https://github.com/pingcap/tidb/issues/46444) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   監査ログ用のEnterpriseプラグインを使用すると、TiDBサーバーが大量のリソースを消費する可能性がある問題を修正[＃49273](https://github.com/pingcap/tidb/issues/49273) @ [lcwangchao](https://github.com/lcwangchao)
    -   正常なシャットダウン中に TiDBサーバーがpanic可能性がある問題を修正[＃36793](https://github.com/pingcap/tidb/issues/36793) @ [bb7133](https://github.com/bb7133)
    -   テーブルがと多数ある場合に、テーブルが`AUTO_ID_CACHE=1`の場合に gRPC クライアント リークが発生する可能性がある問題を修正しました。 [＃48869](https://github.com/pingcap/tidb/issues/48869) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   `ErrLoadDataInvalidURI`の誤ったエラーメッセージを修正 (無効な S3 URI エラー) [＃48164](https://github.com/pingcap/tidb/issues/48164) @ [lance6716](https://github.com/lance6716)
    -   パーティション列タイプが`DATETIME` の場合に`ALTER TABLE ... LAST PARTITION`実行が失敗する問題を修正しました [＃48814](https://github.com/pingcap/tidb/issues/48814) @ [crazycs520](https://github.com/crazycs520)
    -   `IMPORT INTO`実行中に実際のエラーメッセージが他のエラーメッセージによって上書きされる可能性がある問題を修正[＃47992](https://github.com/pingcap/tidb/issues/47992) [＃47781](https://github.com/pingcap/tidb/issues/47781) @ [D3Hunter](https://github.com/D3Hunter)
    -   cgroup v2コンテナにデプロイされたTiDBが検出できない問題を修正[＃48342](https://github.com/pingcap/tidb/issues/48342) @ [D3Hunter](https://github.com/D3Hunter)
    -   DUALテーブルを最初のサブノードとして`UNION ALL`を実行するとエラーが発生する可能性がある問題を修正しました。 [＃48755](https://github.com/pingcap/tidb/issues/48755) @ [winoros](https://github.com/winoros)
    -   DDL `jobID`が 0 に復元されたときに発生する TiDB ノードpanicの問題を修正しました [＃46296](https://github.com/pingcap/tidb/issues/46296) @ [jiyfhust](https://github.com/jiyfhust)
    -   `TABLESAMPLE` によって返されるソートされていない行データの問題を修正しました [＃48253](https://github.com/pingcap/tidb/issues/48253) @ [tangenta](https://github.com/tangenta)
    -   `tidb_enable_ordered_result_mode`有効になっているときにpanicが発生する可能性がある問題を修正[＃45044](https://github.com/pingcap/tidb/issues/45044) @ [qw4990](https://github.com/qw4990)
    -   ウィンドウ関数によって導入されたソートを削減するために、オプティマイザが誤って IndexFullScan を選択する問題を修正しました。 [＃46177](https://github.com/pingcap/tidb/issues/46177) @ [qw4990](https://github.com/qw4990)
    -   TiDBスキーマキャッシュからスキーマ差分コミットバージョンを読み取るときにMVCCインターフェースでロックを処理しない問題を修正しました [＃48281](https://github.com/pingcap/tidb/issues/48281) @ [cfzjywxk](https://github.com/cfzjywxk)
    -   `INDEX_LOOKUP_HASH_JOIN` でのメモリ使用量の見積もりが間違っている問題を修正 [＃47788](https://github.com/pingcap/tidb/issues/47788) @ [SeaRise](https://github.com/SeaRise)
    -   PDリーダーの故障により1分間に`IMPORT INTO`タスクが失敗する問題を修正[＃48307](https://github.com/pingcap/tidb/issues/48307) @ [D3Hunter](https://github.com/D3Hunter)
    -   `batch-client` in `client-go` のpanic問題を修正 [＃47691](https://github.com/pingcap/tidb/issues/47691) @ [crazycs520](https://github.com/crazycs520)
    -   特定の状況で列の整理によってpanicが発生する可能性がある問題を修正[＃47331](https://github.com/pingcap/tidb/issues/47331) @ [Rustin170506](https://github.com/Rustin170506)
    -   TiDB が`systemd` で起動したときに`cgroup`リソース制限を読み取らない問題を修正しました [＃47442](https://github.com/pingcap/tidb/issues/47442) @ [hawkingrei](https://github.com/hawkingrei)
    -   集計関数またはウィンドウ関数を含む共通テーブル式 (CTE) が他の再帰 CTE によって参照されるときに発生する可能性のある構文エラーの問題を修正しました[＃47603](https://github.com/pingcap/tidb/issues/47603) [＃47711](https://github.com/pingcap/tidb/issues/47711) @ [elsa0520](https://github.com/elsa0520)
    -   統計 TopN 構造を構築するときに発生する可能性のあるpanic問題を修正しました。 [＃35948](https://github.com/pingcap/tidb/issues/35948) @ [Rustin170506](https://github.com/Rustin170506)
    -   MPPで計算された`COUNT(INT)`の結果が正しくない可能性がある問題を修正[＃48643](https://github.com/pingcap/tidb/issues/48643) @ [AilinKid](https://github.com/AilinKid)
    -   HashJoin演算子がプローブ実行するときにチャンクを再利用できない問題を修正しました [＃48082](https://github.com/pingcap/tidb/issues/48082) @ [wshwsh12](https://github.com/wshwsh12)

-   TiKV

    -   TiKV の実行速度が非常に遅い場合、リージョンと[金星の上](https://github.com/overvenus)マージ後にpanicする可能性がある問題を修正しました。 [＃16111](https://github.com/tikv/tikv/issues/16111)
    -   解決済みのTSが2時間ブロックされる可能性がある問題を修正[＃15520](https://github.com/tikv/tikv/issues/15520) [＃39130](https://github.com/pingcap/tidb/issues/39130) @ [overvenus](https://github.com/overvenus)
    -   TiKVがraft log を追加できないため`ServerIsBusy`エラーを報告する問題を修正しました。 [＃15800](https://github.com/tikv/tikv/issues/15800) @ [tonyxuqqi](https://github.com/tonyxuqqi)
    -   BRがクラッシュしたときにスナップショットの復元が停止する可能性がある問題を修正しました [＃15684](https://github.com/tikv/tikv/issues/15684) @ [YuJuncen](https://github.com/YuJuncen)
    -   大規模なトランザクションを追跡するときに、古い読み取りの解決済み TS が TiKV OOM 問題を引き起こす可能性がある問題を修正しました [＃14864](https://github.com/tikv/tikv/issues/14864) @ [overvenus](https://github.com/overvenus)
    -   破損したSSTファイルが他のTiKVノードに広がる可能性がある問題を修正 [＃15986](https://github.com/tikv/tikv/issues/15986) @ [Connor1996](https://github.com/Connor1996)
    -   にスケールアウトするときに DR 自動同期のジョイント状態がタイムアウトする可能性がある問題を修正しました [＃15817](https://github.com/tikv/tikv/issues/15817) @ [Connor1996](https://github.com/Connor1996)
    -   クラウド環境のGrafanaでスケジューラコマンド変数が正しくない問題を修正[＃15832](https://github.com/tikv/tikv/issues/15832) @ [Connor1996](https://github.com/Connor1996)
    -   リージョンを[金星の上](https://github.com/overvenus)にマージした後、古いピアが保持され、resolved-tsがブロックされる問題を修正しました。 [＃15919](https://github.com/tikv/tikv/issues/15919)
    -   オンラインアンセーフリカバリがマージ中止を処理できない問題を修正 [＃15580](https://github.com/tikv/tikv/issues/15580) @ [v01dstar](https://github.com/v01dstar)
    -   TiKV を再起動したときに発生する TiKV OOM 問題を修正し、適用されていないRaftログが多数存在するようになりました[＃15770](https://github.com/tikv/tikv/issues/15770) @ [overvenus](https://github.com/overvenus)
    -   `lz4-sys`のバージョンを 1.9.4 にアップグレードしてセキュリティ問題を修正しました [＃15621](https://github.com/tikv/tikv/issues/15621) @ [SpadeA-Tang](https://github.com/SpadeA-Tang)
    -   Titanの`blob-run-mode`がオンラインに更新できない問題を修正 [＃15978](https://github.com/tikv/tikv/issues/15978) @ [tonyxuqqi](https://github.com/tonyxuqqi)
    -   PDとTiKV間のネットワーク中断によりPITRが停止する可能性がある問題を修正しました [＃15279](https://github.com/tikv/tikv/issues/15279) @ [YuJuncen](https://github.com/YuJuncen)
    -   Raftピアを削除するときに TiKV コプロセッサが古いデータを返す可能性がある問題を修正しました [＃16069](https://github.com/tikv/tikv/issues/16069) @ [overvenus](https://github.com/overvenus)

-   PD

    -   `CALIBRATE RESOURCE` を実行すると TiDB Dashboardの`resource_manager_resource_unit`メトリックが空になる問題を修正しました [＃45166](https://github.com/pingcap/tidb/issues/45166) @ [CabinfeverB](https://github.com/CabinfeverB)
    -   ワークロードによる調整ページでエラーが報告される問題を修正しました [＃48162](https://github.com/pingcap/tidb/issues/48162) @ [CabinfeverB](https://github.com/CabinfeverB)
    -   リソース グループを削除すると DDL の原子性が損なわれる可能性がある問題を修正しました [＃45050](https://github.com/pingcap/tidb/issues/45050) @ [glorv](https://github.com/glorv)
    -   PDリーダーが転送され、新しいリーダーとPDクライアントの間にネットワークパーティションがある場合、PDクライアントがリーダーの情報を更新できない問題を修正しました。 [＃7416](https://github.com/tikv/pd/issues/7416) @ [CabinfeverB](https://github.com/CabinfeverB)
    -   大規模クラスタに複数の TiKV ノードを追加すると、TiKVハートビートレポートが遅くなったり停止したりする可能性がある問題を修正しました[＃7248](https://github.com/tikv/pd/issues/7248) @ [rleungx](https://github.com/rleungx)
    -   TiDB DashboardがPD `trace`データを正しく読み取れない問題を修正[＃7253](https://github.com/tikv/pd/issues/7253) @ [nolouch](https://github.com/nolouch)
    -   Gin Web Framework のバージョンを v1.8.1 から v1.9.1 にアップグレードして、いくつかのセキュリティ問題を修正しました[＃7438](https://github.com/tikv/pd/issues/7438) @ [niubell](https://github.com/niubell)
    -   ルールチェッカーが配置ルール設定に従ってラーナーを追加しない問題を修正しました [＃7185](https://github.com/tikv/pd/issues/7185) @ [nolouch](https://github.com/nolouch)
    -   TiKVノードが利用できない場合にPDが通常のピアを削除する可能性がある問題を修正[＃7249](https://github.com/tikv/pd/issues/7249) @ [lhy1024](https://github.com/lhy1024)
    -   DR自動同期モードでリーダーの切り替えに時間がかかる問題を修正 [＃6988](https://github.com/tikv/pd/issues/6988) @ [HuSharp](https://github.com/HuSharp)

-   TiFlash

    -   `ALTER TABLE ... EXCHANGE PARTITION ...`文を実行するとpanicが発生する問題を修正 [＃8372](https://github.com/pingcap/tiflash/issues/8372) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   クエリ中にTiFlash がメモリ制限に遭遇するとメモリリークが発生する問題を修正しました。 [＃8447](https://github.com/pingcap/tiflash/issues/8447) @ [JinheLin](https://github.com/JinheLin)
    -   `FLASHBACK DATABASE` を実行した後もTiFlashレプリカのデータがガベージコレクションされる問題を修正しました [＃8450](https://github.com/pingcap/tiflash/issues/8450) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   Grafana の一部のパネルの最大パーセンタイル時間の表示が誤っていた問題を修正 [＃8076](https://github.com/pingcap/tiflash/issues/8076) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   クエリが予期しないエラーメッセージ「FineGrainedShuffleWriter-V1 でブロックスキーマが一致しません」を返す問題を修正[＃8111](https://github.com/pingcap/tiflash/issues/8111) @ [SeaRise](https://github.com/SeaRise)

-   ツール

    -   Backup & Restore (BR)

        -   BR SQL コマンドと CLI のデフォルト値が異なるため、OOM の問題が発生する可能性がある問題を修正しました[＃48000](https://github.com/pingcap/tidb/issues/48000) @ [YuJuncen](https://github.com/YuJuncen)
        -   大規模なワイドテーブルをバックアップするときに、一部のシナリオでログバックアップが停止する可能性がある問題を修正しました。 [＃15714](https://github.com/tikv/tikv/issues/15714) @ [YuJuncen](https://github.com/YuJuncen)
        -   BRが外部ストレージファイルに対して誤ったURIを生成する問題を修正 [＃48452](https://github.com/pingcap/tidb/issues/48452) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   EC2 メタデータ接続のリセット後の再試行により、バックアップとリストアのパフォーマンスが低下する問題を修正[＃47650](https://github.com/pingcap/tidb/issues/47650) @ [Leavrth](https://github.com/Leavrth)
        -   タスク初期化中にPDへの接続に失敗すると、ログバックアップタスクは開始できるが正常に動作しない問題を修正[＃16056](https://github.com/tikv/tikv/issues/16056) @ [YuJuncen](https://github.com/YuJuncen)

    -   TiCDC

        -   特定のシナリオで`DELETE`ステートメントを複製するときに、 `WHERE`句が主キーを条件として使用しない問題を修正しました[＃9812](https://github.com/pingcap/tiflow/issues/9812) @ [asddongmen](https://github.com/asddongmen)
        -   オブジェクトストレージにデータを複製する際に、特定の特殊なシナリオでレプリケーションタスクが停止する問題を修正[＃10041](https://github.com/pingcap/tiflow/issues/10041) [＃10044](https://github.com/pingcap/tiflow/issues/10044) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   同期ポイントとREDOログを有効にした後、特定のシナリオでレプリケーションタスクが停止する問題を修正しました。 [＃10091](https://github.com/pingcap/tiflow/issues/10091) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   特定の特殊なシナリオで TiCDC が TiKV との接続を誤って閉じる問題を修正[＃10239](https://github.com/pingcap/tiflow/issues/10239) @ [hicqu](https://github.com/hicqu)
        -   ターゲットテーブルが削除され、その後アップストリームで再作成された場合、変更フィードが双方向レプリケーションモードで DML イベントをレプリケートできない問題を修正しました。 [＃10079](https://github.com/pingcap/tiflow/issues/10079) @ [asddongmen](https://github.com/asddongmen)
        -   オブジェクトストアシンクにデータを複製するときに NFS ディレクトリにアクセスすることによって発生するパフォーマンスの問題を修正しました [＃10041](https://github.com/pingcap/tiflow/issues/10041) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   オブジェクトストレージサービスにデータを複製するときに TiCDCサーバーがpanic可能性がある問題を修正しました [＃10137](https://github.com/pingcap/tiflow/issues/10137) @ [sdojjy](https://github.com/sdojjy)
        -   REDOログが有効な場合にDDL文の複製間隔が長すぎる問題を修正[＃9960](https://github.com/pingcap/tiflow/issues/9960) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   REDOログが有効な場合にNFS障害によりオーナーノードが停止する問題を修正[＃9886](https://github.com/pingcap/tiflow/issues/9886) @ [3AceShowHand](https://github.com/3AceShowHand)

    -   TiDB Data Migration (DM)

        -   `CompareGTID` に不適切なアルゴリズムが使用されることで DM のパフォーマンスが低下する問題を修正しました [＃9676](https://github.com/pingcap/tiflow/issues/9676) @ [GMHDBJD](https://github.com/GMHDBJD)

    -   TiDB Lightning

        -   PDリーダーが強制終了されたり、PDリクエストの処理が遅いためにデータのインポートが失敗する問題を修正[＃46950](https://github.com/pingcap/tidb/issues/46950) [＃48075](https://github.com/pingcap/tidb/issues/48075) @ [D3Hunter](https://github.com/D3Hunter)
        -   TiDB Lightningが`writeToTiKV` の間に停止する問題を修正しました [＃48352](https://github.com/pingcap/tidb/issues/48352) @ [lance6716](https://github.com/lance6716) [＃46321](https://github.com/pingcap/tidb/issues/46321)
        -   HTTP再試行リクエストが現在のリクエストコンテンツを使用しないため、データのインポートが失敗する問題を修正しました [＃47930](https://github.com/pingcap/tidb/issues/47930) @ [lance6716](https://github.com/lance6716)
        -   物理インポートモードで不要な`get_regions`呼び出しを削除します [＃45507](https://github.com/pingcap/tidb/issues/45507) @ [mittalrishabh](https://github.com/mittalrishabh)
