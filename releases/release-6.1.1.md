---
title: TiDB 6.1.1 Release Notes
summary: TiDB 6.1.1は2022年9月1日にリリースされました。変更点には、大文字と小文字を区別しない「SHOW DATABASES LIKE」ステートメント、「tidb_enable_outer_join_reorder」のデフォルト値の変更、オプティマイザーとメトリクスレスポンスの圧縮の改善が含まれます。バグ修正では、「INL_HASH_JOIN」のハング、UPDATE`ステートメント実行中のパニック、クエリ結果の誤りなどの問題が修正されています。その他の変更点には、異なる品質基準に対するマルチレベルサポートと、「TiDB-community-toolkit」バイナリパッケージへの追加が含まれます。
---

# TiDB 6.1.1 Release Notes {#tidb-6-1-1-release-notes}

発売日：2022年9月1日

TiDB バージョン: 6.1.1

Quick access: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   `SHOW DATABASES LIKE …`文を大文字と小文字を区別しない[＃34766](https://github.com/pingcap/tidb/issues/34766) @ [エリヤ1](https://github.com/e1ijah1)
    -   デフォルト値[`tidb_enable_outer_join_reorder`](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610)を`1`から`0`に変更します。これにより、結合順序変更の外部結合のサポートがデフォルトで無効になります。

-   診断

    -   継続的プロファイリング機能はデフォルトで無効になっています。これにより、この機能が有効になっている場合に発生する可能性のあるTiFlashのクラッシュ問題を回避できます。詳細については、 [＃5687](https://github.com/pingcap/tiflash/issues/5687) @ [モーニクス](https://github.com/mornyx)をご覧ください。

## Other changes {#other-changes}

-   `TiDB-community-toolkit`バイナリパッケージに以下の内容を追加します。詳細は[TiDB Installation Packages](/binary-package.md)参照してください。

    -   `server-{version}-linux-amd64.tar.gz`
    -   `grafana-{version}-linux-amd64.tar.gz`
    -   `alertmanager-{version}-linux-amd64.tar.gz`
    -   `prometheus-{version}-linux-amd64.tar.gz`
    -   `blackbox_exporter-{version}-linux-amd64.tar.gz`
    -   `node_exporter-{version}-linux-amd64.tar.gz`

-   オペレーティングシステムとCPUアーキテクチャの組み合わせに応じて、異なる品質基準に対する多層的なサポートを導入します。1 [OSおよびプラットフォームの要件](https://docs.pingcap.com/tidb/v6.1/hardware-and-software-requirements#os-and-platform-requirements)参照してください。

## 改善点 {#improvements}

-   TiDB

    -   新しいオプティマイザ`SEMI_JOIN_REWRITE`を追加して、 `EXISTS`クエリ[＃35323](https://github.com/pingcap/tidb/issues/35323) @ [ウィノロス](https://github.com/winoros)のパフォーマンスを向上させます。

-   TiKV

    -   HTTPボディサイズを[#12355](https://github.com/tikv/tikv/issues/12355) @ [ウィノロス](https://github.com/winoros)に削減するために、gzipを使用してメトリック応答を圧縮することをサポートします。
    -   [`server.simplify-metrics`](https://docs.pingcap.com/tidb/v6.1/tikv-configuration-file#simplify-metrics-new-in-v611)構成項目[＃12355](https://github.com/tikv/tikv/issues/12355) @ [栄光](https://github.com/glorv)を使用して一部のメトリックをフィルタリングすることにより、各リクエストに対して返されるデータの量を削減することをサポートします。
    -   RocksDBで同時に実行されるサブコンパクション操作の数を動的に変更する機能をサポート ( `rocksdb.max-sub-compactions` ) [#13145](https://github.com/tikv/tikv/issues/13145) @ [ethercflow](https://github.com/ethercflow)

-   PD

    -   Improve the scheduling speed of Balance Region in specific stages [＃4990](https://github.com/tikv/pd/issues/4990) @[bufferflies](https://github.com/bufferflies)

-   ツール

    -   TiDB Lightning

        -   `stale command`ようなエラーが発生した場合に再試行メカニズムを追加して、インポート成功率[＃36877](https://github.com/pingcap/tidb/issues/36877) @ [D3ハンター](https://github.com/D3Hunter)向上させます

    -   TiDB データ移行 (DM)

        -   ユーザーはライトニングローダー[＃5505](https://github.com/pingcap/tiflow/issues/5505)と[ブチュイトデゴウ](https://github.com/buchuitoudegou)同時実行数を手動で設定できます。

    -   TiCDC

        -   シンクURIパラメータ`transaction-atomicity`を追加し、チェンジフィード内の大規模トランザクションの分割をサポートします。これにより、大規模トランザクションのレイテンシーとメモリ消費を大幅に削減できます[＃5231](https://github.com/pingcap/tiflow/issues/5231) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   マルチリージョンシナリオにおける実行時コンテキスト切り替えによるパフォーマンスオーバーヘッドを削減[＃5610](https://github.com/pingcap/tiflow/issues/5610) @ [ヒック](https://github.com/hicqu)
        -   MySQLシンクを強化してセーフモードを自動的にオフにする[＃5611](https://github.com/pingcap/tiflow/issues/5611) @ [金星の上](https://github.com/overvenus)

## バグ修正 {#bug-fixes}

-   TiDB

    -   `LIMIT` [＃35638](https://github.com/pingcap/tidb/issues/35638) @ [グオシャオゲ](https://github.com/guo-shaoge)と併用すると`INL_HASH_JOIN`ハングする可能性がある問題を修正しました
    -   `UPDATE`文[＃32311](https://github.com/pingcap/tidb/issues/32311) @ [イーサール](https://github.com/Yisaer)の実行時に TiDB がpanic可能性がある問題を修正しました
    -   `SHOW COLUMNS`文[＃36496](https://github.com/pingcap/tidb/issues/36496) @ [接線](https://github.com/tangenta)を実行するときに TiDB がコプロセッサ要求を送信する可能性があるバグを修正しました。
    -   TiDBが`SHOW WARNINGS`ステートメント[＃31569](https://github.com/pingcap/tidb/issues/31569) @ [ジグアン](https://github.com/zyguan)を実行するときに`invalid memory address or nil pointer dereference`エラーを返す可能性があるバグを修正しました
    -   静的パーティションプルーニングモードで、テーブルが空の場合に集計条件を含むSQL文が間違った結果を返す可能性があるバグを修正[＃35295](https://github.com/pingcap/tidb/issues/35295) @ [天菜まお](https://github.com/tiancaiamao)
    -   Fix the issue that the Join Reorder operation will mistakenly push down its Outer Join condition [＃37238](https://github.com/pingcap/tidb/issues/37238) @[winoros](https://github.com/winoros)
    -   CTE スキーマハッシュコードが誤って複製され、CTE が複数回参照されると`Can't find column ... in schema ...`エラーが発生する問題を修正しました[＃35404](https://github.com/pingcap/tidb/issues/35404) @ [アイリンキッド](https://github.com/AilinKid)
    -   一部の右外部結合シナリオで結合順序が間違っていると、間違ったクエリ結果[＃36912](https://github.com/pingcap/tidb/issues/36912) @ [winoros](https://github.com/winoros)が発生する問題を修正しました。
    -   EqualAll の場合[＃34584](https://github.com/pingcap/tidb/issues/34584) @ [修正データベース](https://github.com/fixdb)でTiFlash `firstrow`集計関数の誤って推論された null フラグの問題を修正しました
    -   `IGNORE_PLAN_CACHE`ヒント[＃34596](https://github.com/pingcap/tidb/issues/34596) @ [fzzf678](https://github.com/fzzf678)でバインディングを作成するとプラン キャッシュが機能しない問題を修正しました
    -   ハッシュパーティションウィンドウと単一パーティションウィンドウ[＃35990](https://github.com/pingcap/tidb/issues/35990) @ [リトルフォール](https://github.com/LittleFall)の間に`EXCHANGE`演算子が欠落している問題を修正しました。
    -   パーティションテーブルがインデックスを完全に使用してデータをスキャンできない場合がある問題を修正[#33966](https://github.com/pingcap/tidb/issues/33966) @ [mjonss](https://github.com/mjonss)
    -   集計が[＃35295](https://github.com/pingcap/tidb/issues/35295) @ [天菜まお](https://github.com/tiancaiamao)にプッシュダウンされた後に部分集計に間違ったデフォルト値が設定された場合の間違ったクエリ結果の問題を修正しました
    -   パーティションテーブルをクエリすると、場合によっては[＃35181](https://github.com/pingcap/tidb/issues/35181) @ [mjonss](https://github.com/mjonss)で`index-out-of-range`エラーが発生する可能性がある問題を修正しました。
    -   クエリ条件でパーティションキーが使用され、照合がクエリパーティションテーブル[＃32749](https://github.com/pingcap/tidb/issues/32749) @ [ミョンス](https://github.com/mjonss)の照合と異なる場合にパーティションが誤ってプルーニングされる問題を修正しました。
    -   TiDB Binlogが有効な場合、 `ALTER SEQUENCE`文を実行するとメタデータ バージョンが間違って発生し、 Drainer が[#36276](https://github.com/pingcap/tidb/issues/36276) @ [アイリンキッド](https://github.com/AilinKid)で終了する可能性がある問題を修正しました。
    -   極端なケースで起動時に誤った TiDB ステータスが表示される問題を修正[＃36791](https://github.com/pingcap/tidb/issues/36791) @ [xhebox](https://github.com/xhebox)
    -   TiDBダッシュボード[＃35153](https://github.com/pingcap/tidb/issues/35153) @ [時間と運命](https://github.com/time-and-fate)でパーティションテーブルの実行プランをクエリするときに発生する可能性のある`UnknownPlanID`問題を修正しました。
    -   Fix the issue that the column list does not work in the LOAD DATA statement [＃35198](https://github.com/pingcap/tidb/issues/35198) @[スペードA-タン](https://github.com/SpadeA-Tang)
    -   TiDB Binlogを有効にして重複した値を挿入すると発生する`data and columnID count not match`エラーの問題を修正[＃33608](https://github.com/pingcap/tidb/issues/33608) @ [ジグアン](https://github.com/zyguan)
    -   `tidb_gc_life_time` [＃35392](https://github.com/pingcap/tidb/issues/35392) @ [トンスネークリン](https://github.com/TonsnakeLin)の制限を解除
    -   空のフィールド終端文字が使用されている場合の`LOAD DATA`文のデッドループを修正[#33298](https://github.com/pingcap/tidb/issues/33298) @ [ジグアン](https://github.com/zyguan)
    -   可用性を向上させるために、不健全な TiKV ノードへのリクエストの送信を避ける[＃34906](https://github.com/pingcap/tidb/issues/34906) @ [スティクナーフ](https://github.com/sticnarf)

-   TiKV

    -   Raftstoreがビジー状態の場合にリージョンが重複する可能性があるバグを修正[＃13160](https://github.com/tikv/tikv/issues/13160) @ [5kbps](https://github.com/5kbpers)
    -   リージョンハートビートが中断された後にPDがTiKVに再接続しない問題を修正[＃12934](https://github.com/tikv/tikv/issues/12934) @ [バッファフライ](https://github.com/bufferflies)
    -   空の文字列[＃12673](https://github.com/tikv/tikv/issues/12673) @ [wshwsh12](https://github.com/wshwsh12)型変換を実行するときに TiKV がパニックになる問題を修正しました
    -   TiKVとPD [#12518](https://github.com/tikv/tikv/issues/12518) @ [5kbps](https://github.com/5kbpers)間のリージョンサイズ設定が一致しない問題を修正
    -   Raft Engineが有効になっているときに暗号化キーがクリーンアップされない問題を修正[＃12890](https://github.com/tikv/tikv/issues/12890) @ [タボキ](https://github.com/tabokie)
    -   Fix the panic issue that might occur when a peer is being split and destroyed at the same time [#12825](https://github.com/tikv/tikv/issues/12825) @[ビジージェイ](https://github.com/BusyJay)
    -   リージョンマージプロセス[＃12663](https://github.com/tikv/tikv/issues/12663) @ [BusyJay](https://github.com/BusyJay)でソースピアがスナップショットによってログをキャッチアップするときに発生する可能性のあるpanic問題を修正しました。
    -   PDクライアントがエラー[＃12345](https://github.com/tikv/tikv/issues/12345) @ [コナー1996](https://github.com/Connor1996)に遭遇したときに発生するPDクライアントの頻繁な再接続の問題を修正しました
    -   Raft Engine [＃13123](https://github.com/tikv/tikv/issues/13123) @ [タボキ](https://github.com/tabokie)で並列リカバリが有効になっている場合に発生する可能性のあるpanicを修正しました
    -   新しいリージョンのコミットログ期間が長すぎるため、QPS が[#13077](https://github.com/tikv/tikv/issues/13077) @ [コナー1996](https://github.com/Connor1996)低下する問題を修正しました。
    -   Raft Engineが有効になっているときに稀に発生するパニックを修正[＃12698](https://github.com/tikv/tikv/issues/12698) @ [タボキ](https://github.com/tabokie)
    -   proc ファイルシステム (procfs) が見つからない場合に冗長なログ警告を回避する[＃13116](https://github.com/tikv/tikv/issues/13116) @ [タボキ](https://github.com/tabokie)
    -   ダッシュボード[＃13086](https://github.com/tikv/tikv/issues/13086) @ [栄光](https://github.com/glorv)の`Unified Read Pool CPU`の誤った表現を修正
    -   リージョンが大きい場合、デフォルトの[`region-split-check-diff`](/tikv-configuration-file.md#region-split-check-diff)バケット サイズ[＃12598](https://github.com/tikv/tikv/issues/12598) @ [トニー・シュッキ](https://github.com/tonyxuqqi)よりも大きくなる可能性がある問題を修正しました。
    -   スナップショットの適用が中止され、 Raft Engineが有効になっている場合に TiKV がpanic可能性がある問題を修正[＃12470](https://github.com/tikv/tikv/issues/12470) @ [タボキ](https://github.com/tabokie)
    -   Fix the issue that the PD client might cause deadlocks [＃13191](https://github.com/tikv/tikv/issues/13191) @[バッファフライ](https://github.com/bufferflies) [＃12933](https://github.com/tikv/tikv/issues/12933) @[バートンチン](https://github.com/BurtonQin)

-   PD

    -   クラスタノードのラベル構成が無効な場合にオンラインの進行状況が不正確になる問題を修正[＃5234](https://github.com/tikv/pd/issues/5234) @ [rleungx](https://github.com/rleungx)
    -   `enable-forwarding`有効になっているときに gRPC がエラーを不適切に処理する問題によって発生する PD パニックを修正[＃5373](https://github.com/tikv/pd/issues/5373) @ [bufferflies](https://github.com/bufferflies)
    -   `/regions/replicated`間違ったステータス[＃5095](https://github.com/tikv/pd/issues/5095) @ [rleungx](https://github.com/rleungx)を返す可能性がある問題を修正しました

-   TiFlash

    -   状況によっては、クラスター化インデックスを持つテーブルの列を削除した後にTiFlash がクラッシュする問題を修正[＃5154](https://github.com/pingcap/tiflash/issues/5154) @ [ホンユニャン](https://github.com/hongyunyan)
    -   `format`関数が`Data truncated`エラー[＃4891](https://github.com/pingcap/tiflash/issues/4891) @ [xzhangxian1008](https://github.com/xzhangxian1008)を返す可能性がある問題を修正しました
    -   一部の古いデータがstorageに残り、削除できない問題を修正[＃5659](https://github.com/pingcap/tiflash/issues/5659) @ [リデズ](https://github.com/lidezhu)
    -   一部のエッジケースで不要な CPU 使用率を修正[＃5409](https://github.com/pingcap/tiflash/issues/5409) @ [そよ風のような](https://github.com/breezewish)
    -   IPv6 [＃5247](https://github.com/pingcap/tiflash/issues/5247) @ [ソロツグ](https://github.com/solotzg)を使用するクラスターでTiFlash が動作できないバグを修正しました
    -   並列集約[#5356](https://github.com/pingcap/tiflash/issues/5356) @ [ゲンリキ](https://github.com/gengliqi)エラーによりTiFlashがクラッシュする可能性があるバグを修正
    -   Fix a bug that thread resources might leak in case of `MinTSOScheduler` query errors [#5556](https://github.com/pingcap/tiflash/issues/5556) @[ウィンドトーカー](https://github.com/windtalker)

-   ツール

    -   TiDB Lightning

        -   TiDBがIPv6ホスト[#35880](https://github.com/pingcap/tidb/issues/35880) @ [D3ハンター](https://github.com/D3Hunter)を使用しているときにTiDB LightningがTiDBに接続できない問題を修正しました
        -   再試行メカニズム[#36566](https://github.com/pingcap/tidb/issues/36566) @ [D3Hunter](https://github.com/D3Hunter)を追加して`read index not ready`エラーを修正します
        -   Fix the issue that sensitive information in logs is printed in server mode [＃36374](https://github.com/pingcap/tidb/issues/36374) @[リチュンジュ](https://github.com/lichunzhu)
        -   TiDB Lightning がParquet ファイル内のスラッシュ、数字、または非 ASCII 文字で始まる列をサポートしない問題を修正[＃36980](https://github.com/pingcap/tidb/issues/36980) @ [D3ハンター](https://github.com/D3Hunter)
        -   重複排除により極端な場合にTiDB Lightning がpanicを起こす可能性がある問題を修正[＃34163](https://github.com/pingcap/tidb/issues/34163) @ [フォワードスター](https://github.com/ForwardStar)

    -   TiDB データ移行 (DM)

        -   DM [＃6161](https://github.com/pingcap/tiflow/issues/6161) @ [フォワードスター](https://github.com/ForwardStar)で`txn-entry-size-limit`設定項目が有効にならない問題を修正
        -   `check-task`コマンドが特殊文字[#5895](https://github.com/pingcap/tiflow/issues/5895) @ [エコー1996](https://github.com/Ehco1996)を処理できない問題を修正
        -   `query-status` [#4811](https://github.com/pingcap/tiflow/issues/4811) @ [lyzx2001](https://github.com/lyzx2001)で発生する可能性のあるデータ競合の問題を修正
        -   `operate-schema`コマンド[＃5688](https://github.com/pingcap/tiflow/issues/5688) @ [ForwardStar](https://github.com/ForwardStar)の異なる出力形式を修正
        -   リレーがエラー[＃6193](https://github.com/pingcap/tiflow/issues/6193) @ [ランス6716](https://github.com/lance6716)に遭遇したときの goroutine リークを修正
        -   DB Conn [＃3733](https://github.com/pingcap/tiflow/issues/3733) @ [ランス6716](https://github.com/lance6716)を取得する際に DM ワーカーがスタックする可能性がある問題を修正しました
        -   TiDBがIPv6ホスト[＃6249](https://github.com/pingcap/tiflow/issues/6249) @ [D3ハンター](https://github.com/D3Hunter)を使用するとDMが起動に失敗する問題を修正

    -   TiCDC

        -   互換性のある最大バージョン番号[＃6039](https://github.com/pingcap/tiflow/issues/6039) @ [ハイラスティン](https://github.com/Rustin170506)の誤りを修正
        -   Fix a bug that may cause the cdc server to panic when it receives an HTTP request before it fully starts [＃5639](https://github.com/pingcap/tiflow/issues/5639) @[アズドンメン](https://github.com/asddongmen)
        -   チェンジフィード同期ポイントが有効な場合の DDL シンクpanic問題を修正[＃4934](https://github.com/pingcap/tiflow/issues/4934) @ [アズドンメン](https://github.com/asddongmen)
        -   同期ポイントが有効な場合に、一部のシナリオでチェンジフィードがスタックする問題を修正[＃6827](https://github.com/pingcap/tiflow/issues/6827) @ [ヒック](https://github.com/hicqu)
        -   CDCサーバーの再起動後にchangefeed APIが正常に動作しないバグを修正[＃5837](https://github.com/pingcap/tiflow/issues/5837) @ [アズドンメン](https://github.com/asddongmen)
        -   ブラックホールシンク[＃6206](https://github.com/pingcap/tiflow/issues/6206) @ [アズドンメン](https://github.com/asddongmen)のデータ競合問題を修正
        -   `enable-old-value = false` [#6198](https://github.com/pingcap/tiflow/issues/6198) @ [ハイラスティン](https://github.com/Rustin170506)を設定すると TiCDCpanic問題を修正しました
        -   再実行ログ機能が有効になっている場合のデータ一貫性の問題を修正[＃6189](https://github.com/pingcap/tiflow/issues/6189) [＃6368](https://github.com/pingcap/tiflow/issues/6368) [＃6277](https://github.com/pingcap/tiflow/issues/6277) [＃6456](https://github.com/pingcap/tiflow/issues/6456) [＃6695](https://github.com/pingcap/tiflow/issues/6695) [#6764](https://github.com/pingcap/tiflow/issues/6764) [＃6859](https://github.com/pingcap/tiflow/issues/6859) @ [アズドンメン](https://github.com/asddongmen)
        -   非同期的に再実行イベントを書き込むことで、再実行ログのパフォーマンス低下を修正[＃6011](https://github.com/pingcap/tiflow/issues/6011) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   MySQLシンクがIPv6アドレス[＃6135](https://github.com/pingcap/tiflow/issues/6135) @ [ハイラスティン](https://github.com/Rustin170506)に接続できない問題を修正

    -   バックアップと復元 (BR)

        -   RawKVモード[＃35279](https://github.com/pingcap/tidb/issues/35279) @ [3ポイントシュート](https://github.com/3pointer)でBRが`ErrRestoreTableIDMismatch`報告するバグを修正
        -   大規模クラスタバックアップ[#30087](https://github.com/pingcap/tidb/issues/30087) @ [モクイシュル28](https://github.com/MoCuishle28)での S3 レート制限によるバックアップ失敗を修正するために、バックアップデータディレクトリ構造を調整します。
        -   サマリーログ[#35553](https://github.com/pingcap/tidb/issues/35553) @ [ixuh12](https://github.com/ixuh12)のバックアップ時間の誤りを修正

    -   Dumpling

        -   GetDSNがIPv6 [＃36112](https://github.com/pingcap/tidb/issues/36112) @ [D3ハンター](https://github.com/D3Hunter)をサポートしない問題を修正

    -   TiDB Binlog

        -   `compressor` `gzip` [＃1152](https://github.com/pingcap/tidb-binlog/issues/1152) @ [リチュンジュ](https://github.com/lichunzhu)に設定されている場合に、 Drainer がPumpにリクエストを正しく送信できないバグを修正しました。
