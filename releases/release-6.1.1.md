---
title: TiDB 6.1.1 Release Notes
summary: TiDB 6.1.1 は 2022 年 9 月 1 日にリリースされました。変更点には、大文字と小文字を区別しない SHOW DATABASES LIKE` ステートメント、`tidb_enable_outer_join_reorder` のデフォルト値の変更、オプティマイザーとメトリック応答の圧縮の改善が含まれます。バグ修正では、`INL_HASH_JOIN` のハング、`UPDATE` ステートメント実行中のパニック、不正なクエリ結果などの問題に対処しています。その他の変更点には、さまざまな品質基準のマルチレベル サポートと `TiDB-community-toolkit` バイナリ パッケージへの追加が含まれます。
---

# TiDB 6.1.1 リリースノート {#tidb-6-1-1-release-notes}

発売日: 2022年9月1日

TiDB バージョン: 6.1.1

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [実稼働環境への導入](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   ティビ

    -   `SHOW DATABASES LIKE …`文を大文字と小文字を区別しない[＃34766](https://github.com/pingcap/tidb/issues/34766) @ [エ1イヤ1](https://github.com/e1ijah1)
    -   デフォルト値[`tidb_enable_outer_join_reorder`](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610)を`1`から`0`に変更します。これにより、結合順序の外部結合のサポートがデフォルトで無効になります。

-   診断

    -   デフォルトで継続プロファイリング機能を無効にします。これにより、この機能が有効になっている場合に発生する可能性のあるTiFlashクラッシュの問題を回避できます。詳細については、 [＃5687](https://github.com/pingcap/tiflash/issues/5687) @ [モーニクス](https://github.com/mornyx)を参照してください。

## その他の変更 {#other-changes}

-   `TiDB-community-toolkit`バイナリパッケージに以下の内容を追加します。詳細は[TiDB インストール パッケージ](/binary-package.md)参照してください。

    -   `server-{version}-linux-amd64.tar.gz`
    -   `grafana-{version}-linux-amd64.tar.gz`
    -   `alertmanager-{version}-linux-amd64.tar.gz`
    -   `prometheus-{version}-linux-amd64.tar.gz`
    -   `blackbox_exporter-{version}-linux-amd64.tar.gz`
    -   `node_exporter-{version}-linux-amd64.tar.gz`

-   オペレーティングシステムとCPUアーキテクチャの組み合わせに応じて、異なる品質基準に対するマルチレベルサポートを導入します[OSおよびプラットフォームの要件](https://docs.pingcap.com/tidb/v6.1/hardware-and-software-requirements#os-and-platform-requirements)参照してください。

## 改善点 {#improvements}

-   ティビ

    -   新しいオプティマイザ`SEMI_JOIN_REWRITE`を追加して、 `EXISTS`クエリ[＃35323](https://github.com/pingcap/tidb/issues/35323) @ [ウィノロス](https://github.com/winoros)のパフォーマンスを向上させます。

-   ティクヴ

    -   HTTP ボディのサイズを縮小するために、gzip を使用してメトリック応答を圧縮することをサポートします[＃12355](https://github.com/tikv/tikv/issues/12355) @ [ウィノロス](https://github.com/winoros)
    -   [`server.simplify-metrics`](https://docs.pingcap.com/tidb/v6.1/tikv-configuration-file#simplify-metrics-new-in-v611)の構成項目[＃12355](https://github.com/tikv/tikv/issues/12355) @ [栄光](https://github.com/glorv)を使用して一部のメトリックをフィルタリングすることにより、各リクエストに対して返されるデータの量を削減することをサポートします。
    -   RocksDBで同時に実行されるサブコンパクション操作の数を動的に変更する機能をサポート ( `rocksdb.max-sub-compactions` ) [＃13145](https://github.com/tikv/tikv/issues/13145) @ [イーサフロー](https://github.com/ethercflow)

-   PD

    -   特定のステージ[＃4990](https://github.com/tikv/pd/issues/4990) @ [バッファフライ](https://github.com/bufferflies)のバランスリージョンのスケジュール速度を向上

-   ツール

    -   TiDB Lightning

        -   `stale command`などのエラーに対して再試行メカニズムを追加して、インポート成功率[＃36877](https://github.com/pingcap/tidb/issues/36877) @ [D3ハンター](https://github.com/D3Hunter)を向上させます

    -   TiDB データ移行 (DM)

        -   ユーザーはライトニングローダー[＃5505](https://github.com/pingcap/tiflow/issues/5505) @ [ブチュイトウデゴウ](https://github.com/buchuitoudegou)の同時実行数を手動で設定できます。

    -   ティCDC

        -   シンク URI パラメータ`transaction-atomicity`を追加して、チェンジフィード内の大規模なトランザクションの分割をサポートします。これにより、大規模なトランザクション[＃5231](https://github.com/pingcap/tiflow/issues/5231) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)のレイテンシーとメモリ消費を大幅に削減できます。
        -   マルチリージョンシナリオでのランタイムコンテキスト切り替えによって発生するパフォーマンスオーバーヘッドを削減[＃5610](https://github.com/pingcap/tiflow/issues/5610) @ [ヒック](https://github.com/hicqu)
        -   MySQLシンクを強化してセーフモードを自動的にオフにする[＃5611](https://github.com/pingcap/tiflow/issues/5611) @ [金星の上](https://github.com/overvenus)

## バグ修正 {#bug-fixes}

-   ティビ

    -   `LIMIT` [＃35638](https://github.com/pingcap/tidb/issues/35638) @ [グオシャオゲ](https://github.com/guo-shaoge)と併用すると`INL_HASH_JOIN`ハングする可能性がある問題を修正
    -   `UPDATE`ステートメント[＃32311](https://github.com/pingcap/tidb/issues/32311) @ [イサール](https://github.com/Yisaer)を実行するときに TiDB がpanicになる可能性がある問題を修正しました
    -   `SHOW COLUMNS`ステートメント[＃36496](https://github.com/pingcap/tidb/issues/36496) @ [タンジェンタ](https://github.com/tangenta)を実行するときに TiDB がコプロセッサ要求を送信する可能性があるバグを修正しました。
    -   `SHOW WARNINGS`ステートメント[＃31569](https://github.com/pingcap/tidb/issues/31569) @ [ジグアン](https://github.com/zyguan)を実行すると TiDB が`invalid memory address or nil pointer dereference`エラーを返す可能性があるバグを修正しました。
    -   静的パーティションプルーニングモードで、テーブルが空の場合に集計条件を含む SQL 文が間違った結果を返す可能性があるバグを修正[＃35295](https://github.com/pingcap/tidb/issues/35295) @ [天菜まお](https://github.com/tiancaiamao)
    -   結合したテーブルの再配置操作が誤って外部結合条件[＃37238](https://github.com/pingcap/tidb/issues/37238) @ [ウィノロス](https://github.com/winoros)をプッシュダウンする問題を修正しました。
    -   CTE スキーマ ハッシュ コードが誤って複製され、CTE が複数回参照されると`Can't find column ... in schema ...`エラーが発生する問題を修正しました[＃35404](https://github.com/pingcap/tidb/issues/35404) @ [アイリンキッド](https://github.com/AilinKid)
    -   一部の右外部結合シナリオで結合順序が間違っていると、クエリ結果[＃36912](https://github.com/pingcap/tidb/issues/36912) @ [ウィノロス](https://github.com/winoros)が間違ってしまう問題を修正しました。
    -   EqualAll ケース[＃34584](https://github.com/pingcap/tidb/issues/34584) @ [修正DB](https://github.com/fixdb)でTiFlash `firstrow`集計関数の null フラグが誤って推論される問題を修正
    -   `IGNORE_PLAN_CACHE`ヒント[＃34596](https://github.com/pingcap/tidb/issues/34596) @ [ふーふー](https://github.com/fzzf678)でバインディングを作成するとプラン キャッシュが機能しない問題を修正しました
    -   ハッシュパーティションウィンドウと単一パーティションウィンドウ[＃35990](https://github.com/pingcap/tidb/issues/35990) @ [リトルフォール](https://github.com/LittleFall)の間に`EXCHANGE`演算子が欠落している問題を修正しました。
    -   パーティションテーブルがインデックスを完全に使用してデータをスキャンできない場合がある問題を修正[＃33966](https://github.com/pingcap/tidb/issues/33966) @ [ミョンス](https://github.com/mjonss)
    -   集計が[＃35295](https://github.com/pingcap/tidb/issues/35295) @ [天菜まお](https://github.com/tiancaiamao)にプッシュダウンされた後に部分集計に誤ったデフォルト値が設定された場合の誤ったクエリ結果の問題を修正しました
    -   パーティション化されたテーブルをクエリすると、場合によっては`index-out-of-range`エラーが発生する可能性がある問題を修正しました[＃35181](https://github.com/pingcap/tidb/issues/35181) @ [ミョンス](https://github.com/mjonss)
    -   クエリ条件でパーティション キーが使用され、照合がクエリ パーティション テーブル[＃32749](https://github.com/pingcap/tidb/issues/32749) @ [ミョンス](https://github.com/mjonss)の照合と異なる場合にパーティションが誤ってプルーニングされる問題を修正しました。
    -   TiDB Binlogが有効な場合、 `ALTER SEQUENCE`ステートメントを実行するとメタデータ バージョンが間違って発生し、 Drainer が[＃36276](https://github.com/pingcap/tidb/issues/36276) @ [アイリンキッド](https://github.com/AilinKid)で終了する可能性がある問題を修正しました。
    -   極端なケースで起動時に誤った TiDB ステータスが表示される問題を修正[＃36791](https://github.com/pingcap/tidb/issues/36791) @ [xhebox](https://github.com/xhebox)
    -   TiDBダッシュボード[＃35153](https://github.com/pingcap/tidb/issues/35153) @ [時間と運命](https://github.com/time-and-fate)でパーティションテーブルの実行プランをクエリするときに発生する可能性のある`UnknownPlanID`の問題を修正しました。
    -   LOAD DATA ステートメント[＃35198](https://github.com/pingcap/tidb/issues/35198) @ [スペードA-タン](https://github.com/SpadeA-Tang)で列リストが機能しない問題を修正
    -   TiDB Binlogを有効にして重複した値を挿入すると発生する`data and columnID count not match`エラーの問題を修正[＃33608](https://github.com/pingcap/tidb/issues/33608) @ [ジグアン](https://github.com/zyguan)
    -   `tidb_gc_life_time` [＃35392](https://github.com/pingcap/tidb/issues/35392) @ [トンスネークリン](https://github.com/TonsnakeLin)の制限を解除
    -   空のフィールドターミネータが使用されている場合の`LOAD DATA`文のデッドループを修正[＃33298](https://github.com/pingcap/tidb/issues/33298) @ [ジグアン](https://github.com/zyguan)
    -   可用性を向上させるために、不健全な TiKV ノードにリクエストを送信しないようにする[＃34906](https://github.com/pingcap/tidb/issues/34906) @ [スティクナーフ](https://github.com/sticnarf)

-   ティクヴ

    -   Raftstoreがビジー状態の場合にリージョンが重複する可能性があるバグを修正[＃13160](https://github.com/tikv/tikv/issues/13160) @ [5kbpsの](https://github.com/5kbpers)
    -   リージョンハートビートが中断された後にPDがTiKVに再接続しない問題を修正[＃12934](https://github.com/tikv/tikv/issues/12934) @ [バッファフライ](https://github.com/bufferflies)
    -   空の文字列[＃12673](https://github.com/tikv/tikv/issues/12673) @ [うわー](https://github.com/wshwsh12)型変換を実行するときに TiKV がパニックになる問題を修正
    -   TiKV と PD [＃12518](https://github.com/tikv/tikv/issues/12518) @ [5kbpsの](https://github.com/5kbpers)間のリージョンサイズ設定が一致しない問題を修正
    -   Raft Engineが有効になっているときに暗号化キーがクリーンアップされない問題を修正[＃12890](https://github.com/tikv/tikv/issues/12890) @ [タボキ](https://github.com/tabokie)
    -   ピアが同時に分割され、破棄されたときに発生する可能性のあるpanic問題を修正[＃12825](https://github.com/tikv/tikv/issues/12825) @ [ビジージェイ](https://github.com/BusyJay)
    -   リージョンマージプロセス[＃12663](https://github.com/tikv/tikv/issues/12663) @ [ビジージェイ](https://github.com/BusyJay)でソースピアがスナップショットによってログをキャッチアップするときに発生する可能性のあるpanic問題を修正しました。
    -   PDクライアントがエラー[＃12345](https://github.com/tikv/tikv/issues/12345) @ [コナー1996](https://github.com/Connor1996)に遭遇したときに発生するPDクライアントの頻繁な再接続の問題を修正
    -   Raft Engine [＃13123](https://github.com/tikv/tikv/issues/13123) @ [タボキ](https://github.com/tabokie)で並列リカバリが有効になっている場合に発生する可能性のあるpanicを修正
    -   新しいリージョンのコミットログ期間が長すぎるため、QPS が[＃13077](https://github.com/tikv/tikv/issues/13077) @ [コナー1996](https://github.com/Connor1996)低下する問題を修正しました。
    -   Raft Engineが有効になっているときに稀に発生するパニックを修正[＃12698](https://github.com/tikv/tikv/issues/12698) @ [タボキ](https://github.com/tabokie)
    -   proc ファイルシステム (procfs) が見つからない場合に冗長なログ警告を回避する[＃13116](https://github.com/tikv/tikv/issues/13116) @ [タボキ](https://github.com/tabokie)
    -   ダッシュボード[＃13086](https://github.com/tikv/tikv/issues/13086) @ [栄光](https://github.com/glorv)の`Unified Read Pool CPU`の誤った表現を修正
    -   リージョンが大きい場合、デフォルトの[`region-split-check-diff`](/tikv-configuration-file.md#region-split-check-diff)バケット サイズ[＃12598](https://github.com/tikv/tikv/issues/12598) @ [トニー](https://github.com/tonyxuqqi)よりも大きくなる可能性がある問題を修正しました。
    -   スナップショットの適用が中止され、 Raft Engineが有効になっている場合に TiKV がpanicになる可能性がある問題を修正[＃12470](https://github.com/tikv/tikv/issues/12470) @ [タボキ](https://github.com/tabokie)
    -   PDクライアントがデッドロックを引き起こす可能性がある問題を修正[＃13191](https://github.com/tikv/tikv/issues/13191) @ [バッファフライ](https://github.com/bufferflies) [＃12933](https://github.com/tikv/tikv/issues/12933) @ [バートンチン](https://github.com/BurtonQin)

-   PD

    -   クラスタノードのラベル構成が無効な場合にオンラインの進行状況が不正確になる問題を修正[＃5234](https://github.com/tikv/pd/issues/5234) @ [rleungx](https://github.com/rleungx)
    -   `enable-forwarding`が有効になっている場合に gRPC がエラーを不適切に処理する問題によって発生する PD パニックを修正[＃5373](https://github.com/tikv/pd/issues/5373) @ [バッファフライ](https://github.com/bufferflies)
    -   `/regions/replicated`間違ったステータス[＃5095](https://github.com/tikv/pd/issues/5095) @ [rleungx](https://github.com/rleungx)を返す可能性がある問題を修正

-   TiFlash

    -   状況によっては、クラスター化インデックスを持つテーブルの列を削除した後にTiFlash がクラッシュする問題を修正[＃5154](https://github.com/pingcap/tiflash/issues/5154) @ [ホンユンヤン](https://github.com/hongyunyan)
    -   `format`関数が`Data truncated`エラー[＃4891](https://github.com/pingcap/tiflash/issues/4891) @ [翻訳者](https://github.com/xzhangxian1008)を返す可能性がある問題を修正しました
    -   一部の古いデータがstorageに残り、削除できない問題を修正[＃5659](https://github.com/pingcap/tiflash/issues/5659) @ [リデズ](https://github.com/lidezhu)
    -   一部のエッジケースで不要な CPU 使用率を修正[＃5409](https://github.com/pingcap/tiflash/issues/5409) @ [そよ風のような](https://github.com/breezewish)
    -   IPv6 [＃5247](https://github.com/pingcap/tiflash/issues/5247) @ [ソロッツ](https://github.com/solotzg)使用するクラスターでTiFlashが動作しないバグを修正
    -   並列集計[＃5356](https://github.com/pingcap/tiflash/issues/5356) @ [ゲンリキ](https://github.com/gengliqi)のエラーによりTiFlash がクラッシュする可能性があるバグを修正
    -   `MinTSOScheduler`クエリエラー[＃5556](https://github.com/pingcap/tiflash/issues/5556) @ [風の話し手](https://github.com/windtalker)の場合にスレッドリソースがリークする可能性があるバグを修正

-   ツール

    -   TiDB Lightning

        -   TiDB が IPv6 ホスト[＃35880](https://github.com/pingcap/tidb/issues/35880) @ [D3ハンター](https://github.com/D3Hunter)を使用している場合にTiDB Lightning がTiDB に接続できない問題を修正しました
        -   再試行メカニズム[＃36566](https://github.com/pingcap/tidb/issues/36566) @ [D3ハンター](https://github.com/D3Hunter)を追加して`read index not ready`エラーを修正します
        -   サーバーモード[＃36374](https://github.com/pingcap/tidb/issues/36374) @ [リチュンジュ](https://github.com/lichunzhu)でログ内の機密情報が印刷される問題を修正
        -   TiDB Lightning がParquet ファイル内のスラッシュ、数字、または非 ASCII 文字で始まる列をサポートしない問題を修正[＃36980](https://github.com/pingcap/tidb/issues/36980) @ [D3ハンター](https://github.com/D3Hunter)
        -   重複排除により極端な場合にTiDB Lightning がpanicを起こす可能性がある問題を修正[＃34163](https://github.com/pingcap/tidb/issues/34163) @ [フォワードスター](https://github.com/ForwardStar)

    -   TiDB データ移行 (DM)

        -   DM [＃6161](https://github.com/pingcap/tiflow/issues/6161) @ [フォワードスター](https://github.com/ForwardStar)で`txn-entry-size-limit`設定項目が有効にならない問題を修正
        -   `check-task`コマンドが特殊文字[＃5895](https://github.com/pingcap/tiflow/issues/5895) @ [エコー1996](https://github.com/Ehco1996)を処理できない問題を修正
        -   `query-status` [＃4811](https://github.com/pingcap/tiflow/issues/4811) @ [翻訳者](https://github.com/lyzx2001)で起こり得るデータ競合の問題を修正
        -   `operate-schema`コマンド[＃5688](https://github.com/pingcap/tiflow/issues/5688) @ [フォワードスター](https://github.com/ForwardStar)の異なる出力形式を修正
        -   リレーがエラー[＃6193](https://github.com/pingcap/tiflow/issues/6193) @ [ランス6716](https://github.com/lance6716)に遭遇したときの goroutine リークを修正
        -   DB Conn [＃3733](https://github.com/pingcap/tiflow/issues/3733) @ [ランス6716](https://github.com/lance6716)を取得する際に DM ワーカーがスタックする可能性がある問題を修正しました。
        -   TiDBがIPv6ホスト[＃6249](https://github.com/pingcap/tiflow/issues/6249) @ [D3ハンター](https://github.com/D3Hunter)を使用するとDMが起動に失敗する問題を修正

    -   ティCDC

        -   間違った最大互換バージョン番号[＃6039](https://github.com/pingcap/tiflow/issues/6039) @ [ハイラスティン](https://github.com/Rustin170506)を修正
        -   完全に起動する前に HTTP リクエストを受信すると CDCサーバーがpanicを起こす可能性があるバグを修正[＃5639](https://github.com/pingcap/tiflow/issues/5639) @ [アズドンメン](https://github.com/asddongmen)
        -   チェンジフィード同期ポイントが有効な場合の DDL シンクpanic問題を修正[＃4934](https://github.com/pingcap/tiflow/issues/4934) @ [アズドンメン](https://github.com/asddongmen)
        -   同期ポイントが有効になっている場合に、一部のシナリオで変更フィードがスタックする問題を修正[＃6827](https://github.com/pingcap/tiflow/issues/6827) @ [ヒック](https://github.com/hicqu)
        -   CDCサーバーの再起動後にchangefeed APIが正常に動作しないバグを修正[＃5837](https://github.com/pingcap/tiflow/issues/5837) @ [アズドンメン](https://github.com/asddongmen)
        -   ブラックホールシンク[＃6206](https://github.com/pingcap/tiflow/issues/6206) @ [アズドンメン](https://github.com/asddongmen)のデータ競合問題を修正
        -   `enable-old-value = false` [＃6198](https://github.com/pingcap/tiflow/issues/6198) @ [ハイラスティン](https://github.com/Rustin170506)を設定すると TiCDCpanic問題を修正
        -   再実行ログ機能が有効になっている場合のデータ一貫性の問題を修正[＃6189](https://github.com/pingcap/tiflow/issues/6189) [＃6368](https://github.com/pingcap/tiflow/issues/6368) [＃6277](https://github.com/pingcap/tiflow/issues/6277) [＃6456](https://github.com/pingcap/tiflow/issues/6456) [＃6695](https://github.com/pingcap/tiflow/issues/6695) [＃6764](https://github.com/pingcap/tiflow/issues/6764) [＃6859](https://github.com/pingcap/tiflow/issues/6859) @ [アズドンメン](https://github.com/asddongmen)
        -   非同期で再実行イベントを書き込むことで、再実行ログのパフォーマンス低下を修正[＃6011](https://github.com/pingcap/tiflow/issues/6011) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   MySQLシンクがIPv6アドレス[＃6135](https://github.com/pingcap/tiflow/issues/6135) @ [ハイラスティン](https://github.com/Rustin170506)に接続できない問題を修正

    -   バックアップと復元 (BR)

        -   RawKVモード[＃35279](https://github.com/pingcap/tidb/issues/35279) @ [3ポインター](https://github.com/3pointer)でBRが`ErrRestoreTableIDMismatch`を報告するバグを修正
        -   大規模クラスタ バックアップ[＃30087](https://github.com/pingcap/tidb/issues/30087) @ [モクイシュル28](https://github.com/MoCuishle28)での S3 レート制限によって発生するバックアップ障害を修正するために、バックアップ データ ディレクトリ構造を調整します。
        -   サマリーログ[＃35553](https://github.com/pingcap/tidb/issues/35553) @ [ixuh12](https://github.com/ixuh12)のバックアップ時間の誤りを修正

    -   Dumpling

        -   GetDSNがIPv6 [＃36112](https://github.com/pingcap/tidb/issues/36112) @ [D3ハンター](https://github.com/D3Hunter)をサポートしない問題を修正

    -   TiDBBinlog

        -   `compressor`が`gzip` [＃1152](https://github.com/pingcap/tidb-binlog/issues/1152) @ [リチュンジュ](https://github.com/lichunzhu)に設定されている場合に、 Drainer がPumpにリクエストを正しく送信できないバグを修正しました。
