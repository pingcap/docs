---
title: TiDB 6.1.1 Release Notes
---

# TiDB 6.1.1 リリースノート {#tidb-6-1-1-release-notes}

発売日：2022年9月1日

TiDB バージョン: 6.1.1

クイック アクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [インストール パッケージ](https://www.pingcap.com/download/?version=v6.1.1#version-list)

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   `SHOW DATABASES LIKE …`ステートメントを大文字と小文字を区別しない[#34766](https://github.com/pingcap/tidb/issues/34766) @ [e1ijah1](https://github.com/e1ijah1)にする
    -   デフォルト値の[`tidb_enable_outer_join_reorder`](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610) `1`から`0`に変更します。これにより、Join Reorder の Outer Join のサポートがデフォルトで無効になります。

-   診断

    -   連続プロファイリング機能をデフォルトで無効にします。これにより、この機能が有効になっているときに発生する可能性のあるTiFlashクラッシュの問題を回避できます。詳細は[#5687](https://github.com/pingcap/tiflash/issues/5687) @ [モニクス](https://github.com/mornyx)を参照

## その他の変更 {#other-changes}

-   `TiDB-community-toolkit`バイナリパッケージに以下の内容を追加します。詳細については、 [TiDB インストール パッケージ](/binary-package.md)を参照してください。

    -   `server-{version}-linux-amd64.tar.gz`
    -   `grafana-{version}-linux-amd64.tar.gz`
    -   `alertmanager-{version}-linux-amd64.tar.gz`
    -   `prometheus-{version}-linux-amd64.tar.gz`
    -   `blackbox_exporter-{version}-linux-amd64.tar.gz`
    -   `node_exporter-{version}-linux-amd64.tar.gz`

-   オペレーティング システムと CPU アーキテクチャの組み合わせに関するさまざまな品質基準のマルチレベル サポートを導入します。 [OS とプラットフォームの要件](https://docs.pingcap.com/tidb/v6.1/hardware-and-software-requirements#os-and-platform-requirements)を参照してください。

## 改良点 {#improvements}

-   TiDB

    -   新しいオプティマイザ`SEMI_JOIN_REWRITE`を追加して、 `EXISTS`クエリ[#35323](https://github.com/pingcap/tidb/issues/35323) @ [ウィノロス](https://github.com/winoros)のパフォーマンスを向上させます

-   TiKV

    -   gzip を使用したメトリクス応答の圧縮をサポートして、HTTP 本文のサイズを縮小します[#12355](https://github.com/tikv/tikv/issues/12355) @ [ウィノロス](https://github.com/winoros)
    -   [`server.simplify-metrics`](https://docs.pingcap.com/tidb/v6.1/tikv-configuration-file#simplify-metrics-new-in-v611)構成アイテム[#12355](https://github.com/tikv/tikv/issues/12355) @ [栄光](https://github.com/glorv)を使用して一部のメトリックを除外することにより、各リクエストで返されるデータ量の削減をサポートします
    -   RocksDB で同時に実行されるサブ圧縮操作の数を動的に変更するサポート ( `rocksdb.max-sub-compactions` ) [#13145](https://github.com/tikv/tikv/issues/13145) @ [イーサフロー](https://github.com/ethercflow)

-   PD

    -   特定のステージ[#4990](https://github.com/tikv/pd/issues/4990) @ [バタフライ](https://github.com/bufferflies)でのバランスリージョンのスケジューリング速度を向上させます

-   ツール

    -   TiDB Lightning

        -   インポートの成功率を向上させるために`stale command`などのエラーに対する再試行メカニズムを追加します[#36877](https://github.com/pingcap/tidb/issues/36877) @ [D3ハンター](https://github.com/D3Hunter)

    -   TiDB データ移行 (DM)

        -   ユーザーは、Lightning ローダー[#5505](https://github.com/pingcap/tiflow/issues/5505) @ [ぶちゅとでごう](https://github.com/buchuitoudegou)の同時実行量を手動で設定できます

    -   TiCDC

        -   変更フィードでの大規模なトランザクションの分割をサポートするために、シンク uri パラメーター`transaction-atomicity`を追加します。これにより、大規模なトランザクションのレイテンシーとメモリ消費を大幅に削減できます[#5231](https://github.com/pingcap/tiflow/issues/5231) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)
        -   マルチリージョン シナリオ[#5610](https://github.com/pingcap/tiflow/issues/5610) @ [ヒック](https://github.com/hicqu)でランタイム コンテキストの切り替えによって発生するパフォーマンス オーバーヘッドを削減する
        -   MySQL シンクを拡張してセーフ モードを自動的にオフにする[#5611](https://github.com/pingcap/tiflow/issues/5611) @ [大静脈](https://github.com/overvenus)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `LIMIT` [#35638](https://github.com/pingcap/tidb/issues/35638) @ [グオシャオゲ](https://github.com/guo-shaoge)で使用すると`INL_HASH_JOIN`がハングする問題を修正
    -   `UPDATE`ステートメント[#32311](https://github.com/pingcap/tidb/issues/32311) @ [イサール](https://github.com/Yisaer)を実行すると TiDB がpanicになることがある問題を修正します。
    -   `SHOW COLUMNS`ステートメント[#36496](https://github.com/pingcap/tidb/issues/36496) @ [接線](https://github.com/tangenta)の実行時に TiDB がコプロセッサー要求を送信する可能性があるバグを修正します。
    -   `SHOW WARNINGS`ステートメント[#31569](https://github.com/pingcap/tidb/issues/31569) @ [ジグアン](https://github.com/zyguan)を実行すると、TiDB が`invalid memory address or nil pointer dereference`エラーを返すことがあるバグを修正
    -   静的パーティションのプルーニング モードで、テーブルが空の場合に集計条件を含む SQL ステートメントが間違った結果を返す可能性があるというバグを修正します[#35295](https://github.com/pingcap/tidb/issues/35295) @ [ティアンカイマオ](https://github.com/tiancaiamao)
    -   結合したテーブルの再配置操作が Outer Join 条件[#37238](https://github.com/pingcap/tidb/issues/37238) @ [ウィノロス](https://github.com/winoros)を誤ってプッシュ ダウンする問題を修正します。
    -   CTE スキーマ ハッシュ コードが誤って複製され、CTE が複数回参照されると`Can't find column ... in schema ...`エラーが発生する問題を修正します[#35404](https://github.com/pingcap/tidb/issues/35404) @ [アイリンキッド](https://github.com/AilinKid)
    -   一部の右外部結合シナリオで結合の並べ替えが間違っていると、間違ったクエリ結果[#36912](https://github.com/pingcap/tidb/issues/36912) @ [ウィノロス](https://github.com/winoros)が発生する問題を修正します。
    -   EqualAll ケース[#34584](https://github.com/pingcap/tidb/issues/34584) @ [fixdb](https://github.com/fixdb)でTiFlash `firstrow`集計関数の null フラグが誤って推論される問題を修正します。
    -   `IGNORE_PLAN_CACHE`ヒント[#34596](https://github.com/pingcap/tidb/issues/34596) @ [fzzf678](https://github.com/fzzf678)でバインドを作成すると、Plan Cache が機能しない問題を修正します。
    -   ハッシュ パーティション ウィンドウと単一パーティション ウィンドウ[#35990](https://github.com/pingcap/tidb/issues/35990) @ [リトルフォール](https://github.com/LittleFall)の間で`EXCHANGE`演算子が欠落している問題を修正します。
    -   場合によっては、分割されたテーブルがインデックスを完全に使用してデータをスキャンできないという問題を修正します[#33966](https://github.com/pingcap/tidb/issues/33966) @ [ミヨンス](https://github.com/mjonss)
    -   集計が[#35295](https://github.com/pingcap/tidb/issues/35295) @ [ティアンカイマオ](https://github.com/tiancaiamao)にプッシュ ダウンされた後、部分集計に間違った既定値が設定されている場合に、間違ったクエリ結果が返される問題を修正します。
    -   パーティション化されたテーブルをクエリすると、場合によっては`index-out-of-range`エラー[#35181](https://github.com/pingcap/tidb/issues/35181) @ [ミヨンス](https://github.com/mjonss)が発生する可能性がある問題を修正します
    -   パーティション キーがクエリ条件で使用され、照合がクエリ パーティション テーブル[#32749](https://github.com/pingcap/tidb/issues/32749) @ [ミヨンス](https://github.com/mjonss)のものと異なる場合、パーティションが誤ってプルーニングされる問題を修正します。
    -   TiDB Binlogが有効な場合に`ALTER SEQUENCE`ステートメントを実行すると、間違ったメタデータ バージョンが発生し、 Drainerが[#36276](https://github.com/pingcap/tidb/issues/36276) @ [アイリンキッド](https://github.com/AilinKid)で終了する問題を修正します。
    -   いくつかの極端なケースで、起動時に誤った TiDB ステータスが表示される問題を修正します[#36791](https://github.com/pingcap/tidb/issues/36791) @ [xhebox](https://github.com/xhebox)
    -   TiDB ダッシュボード[#35153](https://github.com/pingcap/tidb/issues/35153) @ [時間と運命](https://github.com/time-and-fate)でパーティション分割されたテーブルの実行プランをクエリするときに発生する可能性のある`UnknownPlanID`問題を修正します。
    -   LOAD DATA ステートメントで列リストが機能しない問題を修正[#35198](https://github.com/pingcap/tidb/issues/35198) @ [スペード・ア・タン](https://github.com/SpadeA-Tang)
    -   TiDB Binlog を有効にして重複値を挿入すると`data and columnID count not match`エラーが発生する問題を修正[#33608](https://github.com/pingcap/tidb/issues/33608) @ [ジグアン](https://github.com/zyguan)
    -   `tidb_gc_life_time` [#35392](https://github.com/pingcap/tidb/issues/35392) @ [トンスネークリン](https://github.com/TonsnakeLin)の制限を取り除く
    -   空のフィールド ターミネータが使用された場合の`LOAD DATA`ステートメントのデッド ループを修正[#33298](https://github.com/pingcap/tidb/issues/33298) @ [ジグアン](https://github.com/zyguan)
    -   可用性を向上させるために、異常な TiKV ノードにリクエストを送信しないようにする[#34906](https://github.com/pingcap/tidb/issues/34906) @ [スティックナーフ](https://github.com/sticnarf)

-   TiKV

    -   Raftstoreが忙しい[#13160](https://github.com/tikv/tikv/issues/13160) @ [5kbps](https://github.com/5kbpers)の場合、リージョンが重複する可能性があるバグを修正します
    -   リージョンのハートビートが中断された後、PD が TiKV に再接続しない問題を修正します[#12934](https://github.com/tikv/tikv/issues/12934) @ [バタフライ](https://github.com/bufferflies)
    -   空の文字列[#12673](https://github.com/tikv/tikv/issues/12673) @ [wshwsh12](https://github.com/wshwsh12)の型変換を実行すると TiKV がパニックになる問題を修正
    -   TiKV と PD [#12518](https://github.com/tikv/tikv/issues/12518) @ [5kbps](https://github.com/5kbpers)の間でリージョンサイズの設定が一致しない問題を修正
    -   Raft Engineが有効になっているときに暗号化キーがクリーンアップされない問題を修正します[#12890](https://github.com/tikv/tikv/issues/12890) @ [タボキー](https://github.com/tabokie)
    -   ピアの分割と破棄が同時に行われると発生する可能性があるpanicの問題を修正します[#12825](https://github.com/tikv/tikv/issues/12825) @ [ビジージェイ](https://github.com/BusyJay)
    -   ソース ピアがリージョンマージ プロセス[#12663](https://github.com/tikv/tikv/issues/12663) @ [ビジージェイ](https://github.com/BusyJay)でスナップショットによってログをキャッチするときに発生する可能性があるpanicの問題を修正します。
    -   PD クライアントがエラー[#12345](https://github.com/tikv/tikv/issues/12345) @ [コナー1996](https://github.com/Connor1996)に遭遇したときに発生する PD クライアントの再接続が頻繁に発生する問題を修正します。
    -   Raft Engine [#13123](https://github.com/tikv/tikv/issues/13123) @ [タボキー](https://github.com/tabokie)で並列リカバリが有効になっている場合に発生する可能性のあるpanicを修正
    -   新しいリージョンのコミット ログ期間が長すぎるため、QPS が[#13077](https://github.com/tikv/tikv/issues/13077) @ [コナー1996](https://github.com/Connor1996)低下する問題を修正します。
    -   Raft Engine が有効になっているときのまれなパニックを修正[#12698](https://github.com/tikv/tikv/issues/12698) @ [タボキー](https://github.com/tabokie)
    -   proc ファイルシステム (procfs) が見つからない場合に冗長なログ警告を回避する[#13116](https://github.com/tikv/tikv/issues/13116) @ [タボキー](https://github.com/tabokie)
    -   ダッシュボード[#13086](https://github.com/tikv/tikv/issues/13086) @ [栄光](https://github.com/glorv)の`Unified Read Pool CPU`の間違った表現を修正
    -   リージョンが大きい場合、デフォルトの[`region-split-check-diff`](/tikv-configuration-file.md#region-split-check-diff)バケット サイズ[#12598](https://github.com/tikv/tikv/issues/12598) @ [tonyxuqqi](https://github.com/tonyxuqqi)よりも大きくなる可能性があるという問題を修正します
    -   スナップショットの適用が中止され、 Raft Engineが有効になっている場合に TiKV がpanic可能性がある問題を修正します[#12470](https://github.com/tikv/tikv/issues/12470) @ [タボキー](https://github.com/tabokie)
    -   PD クライアントがデッドロックを引き起こす可能性がある問題を修正します[#13191](https://github.com/tikv/tikv/issues/13191) @ [バタフライ](https://github.com/bufferflies) [#12933](https://github.com/tikv/tikv/issues/12933) @ [バートンチン](https://github.com/BurtonQin)

-   PD

    -   クラスタ ノードのラベル構成が無効な場合、オンラインの進行状況が不正確になる問題を修正します[#5234](https://github.com/tikv/pd/issues/5234) @ [ルルング](https://github.com/rleungx)
    -   `enable-forwarding`が有効な場合に gRPC がエラーを不適切に処理するという問題によって引き起こされる PD パニックを修正します[#5373](https://github.com/tikv/pd/issues/5373) @ [バタフライ](https://github.com/bufferflies)
    -   `/regions/replicated`が間違ったステータス[#5095](https://github.com/tikv/pd/issues/5095) @ [ルルング](https://github.com/rleungx)を返すことがある問題を修正

-   TiFlash

    -   一部の状況で、クラスター化されたインデックスを含むテーブルの列を削除した後にTiFlash がクラッシュする問題を修正します[#5154](https://github.com/pingcap/tiflash/issues/5154) @ [ホンユニャン](https://github.com/hongyunyan)
    -   `format`関数が`Data truncated`エラー[#4891](https://github.com/pingcap/tiflash/issues/4891) @ [xzhangxian1008](https://github.com/xzhangxian1008)を返す可能性がある問題を修正します。
    -   一部の古いデータがstorageに残り、削除できない可能性があるという問題を修正します[#5659](https://github.com/pingcap/tiflash/issues/5659) @ [リデジュ](https://github.com/lidezhu)
    -   一部のエッジケースでの不必要な CPU 使用率を修正[#5409](https://github.com/pingcap/tiflash/issues/5409) @ [そよ風](https://github.com/breezewish)
    -   IPv6 [#5247](https://github.com/pingcap/tiflash/issues/5247) @ [ソロツグ](https://github.com/solotzg)を使用したクラスタでTiFlash が動作しない不具合を修正
    -   並列集計[#5356](https://github.com/pingcap/tiflash/issues/5356) @ [ゲンリキ](https://github.com/gengliqi)でエラーによりTiFlashがクラッシュすることがある不具合を修正
    -   クエリエラー[#5556](https://github.com/pingcap/tiflash/issues/5556) @ [風の語り手](https://github.com/windtalker)が`MinTSOScheduler`の場合にスレッドリソースがリークする可能性があるバグを修正

-   ツール

    -   TiDB Lightning

        -   TiDB が IPv6 ホスト[#35880](https://github.com/pingcap/tidb/issues/35880) @ [D3ハンター](https://github.com/D3Hunter)を使用している場合、 TiDB Lightning がTiDB への接続に失敗する問題を修正します。
        -   再試行メカニズム[#36566](https://github.com/pingcap/tidb/issues/36566) @ [D3ハンター](https://github.com/D3Hunter)を追加して、 `read index not ready`エラーを修正します。
        -   ログの機密情報がサーバーモード[#36374](https://github.com/pingcap/tidb/issues/36374) @ [リチュンジュ](https://github.com/lichunzhu)で出力される問題を修正します。
        -   TiDB Lightning が、 Parquet ファイル[#36980](https://github.com/pingcap/tidb/issues/36980) @ [D3ハンター](https://github.com/D3Hunter)でスラッシュ、数字、または非 ASCII 文字で始まる列をサポートしていないという問題を修正します
        -   重複除外が極端な場合にTiDB Lightning でpanicを引き起こす可能性がある問題を修正します[#34163](https://github.com/pingcap/tidb/issues/34163) @ [フォワードスター](https://github.com/ForwardStar)

    -   TiDB データ移行 (DM)

        -   [#6161](https://github.com/pingcap/tiflow/issues/6161) @ [フォワードスター](https://github.com/ForwardStar)で設定項目`txn-entry-size-limit`が反映されない問題を修正
        -   `check-task`コマンドが特殊文字[#5895](https://github.com/pingcap/tiflow/issues/5895) @ [Ehco1996](https://github.com/Ehco1996)を処理できない問題を修正
        -   `query-status` [#4811](https://github.com/pingcap/tiflow/issues/4811) @ [lyzx2001](https://github.com/lyzx2001)でデータ競合が発生する可能性がある問題を修正
        -   `operate-schema`コマンド[#5688](https://github.com/pingcap/tiflow/issues/5688) @ [フォワードスター](https://github.com/ForwardStar)の異なる出力形式を修正
        -   リレーがエラー[#6193](https://github.com/pingcap/tiflow/issues/6193) @ [ランス6716](https://github.com/lance6716)に遭遇したときのゴルーチン リークを修正
        -   DB Conn [#3733](https://github.com/pingcap/tiflow/issues/3733) @ [ランス6716](https://github.com/lance6716)の取得時に DM Worker がスタックする問題を修正
        -   TiDB が IPv6 ホスト[#6249](https://github.com/pingcap/tiflow/issues/6249) @ [D3ハンター](https://github.com/D3Hunter)を使用している場合に DM の起動に失敗する問題を修正

    -   TiCDC

        -   誤った最大互換バージョン番号[#6039](https://github.com/pingcap/tiflow/issues/6039) @ [ハイラスチン](https://github.com/hi-rustin)を修正
        -   cdc サーバーが完全に開始する前に HTTP 要求を受信すると、cdcサーバーがpanicになる可能性があるバグを修正します[#5639](https://github.com/pingcap/tiflow/issues/5639) @ [アスドンメン](https://github.com/asddongmen)
        -   changefeed 同期ポイントが有効になっている場合の ddl シンクpanicの問題を修正します[#4934](https://github.com/pingcap/tiflow/issues/4934) @ [アスドンメン](https://github.com/asddongmen)
        -   同期ポイントが有効になっていると、一部のシナリオで変更フィードが停止する問題を修正します[#6827](https://github.com/pingcap/tiflow/issues/6827) @ [ヒック](https://github.com/hicqu)
        -   cdcサーバーの再起動後、changefeed APIが正常に動作しない不具合を修正[#5837](https://github.com/pingcap/tiflow/issues/5837) @ [アスドンメン](https://github.com/asddongmen)
        -   ブラック ホール シンク[#6206](https://github.com/pingcap/tiflow/issues/6206) @ [アスドンメン](https://github.com/asddongmen)でのデータ競合の問題を修正
        -   `enable-old-value = false` [#6198](https://github.com/pingcap/tiflow/issues/6198) @ [ハイラスチン](https://github.com/hi-rustin)を設定したときの TiCDCpanicの問題を修正します。
        -   REDO ログ機能が有効になっている場合のデータの一貫性の問題を修正します[#6189](https://github.com/pingcap/tiflow/issues/6189) [#6368](https://github.com/pingcap/tiflow/issues/6368) [#6277](https://github.com/pingcap/tiflow/issues/6277) [#6456](https://github.com/pingcap/tiflow/issues/6456) [#6695](https://github.com/pingcap/tiflow/issues/6695) [#6764](https://github.com/pingcap/tiflow/issues/6764) [#6859](https://github.com/pingcap/tiflow/issues/6859) @ [アスドンメン](https://github.com/asddongmen)
        -   REDO イベントを非同期に書き込むことにより、REDO ログのパフォーマンスの低下を修正します[#6011](https://github.com/pingcap/tiflow/issues/6011) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)
        -   MySQL シンクが IPv6 アドレス[#6135](https://github.com/pingcap/tiflow/issues/6135) @ [ハイラスチン](https://github.com/hi-rustin)に接続できない問題を修正

    -   バックアップと復元 (BR)

        -   RawKV モード[#35279](https://github.com/pingcap/tidb/issues/35279) @ [3ポインター](https://github.com/3pointer)でBR が`ErrRestoreTableIDMismatch`を報告するバグを修正
        -   バックアップ データのディレクトリ構造を調整して、大規模なクラスター バックアップ[#30087](https://github.com/pingcap/tidb/issues/30087) @ [MoCuishle28](https://github.com/MoCuishle28)での S3 レート制限によって引き起こされるバックアップの失敗を修正します。
        -   要約ログ[#35553](https://github.com/pingcap/tidb/issues/35553) @ [ixuh12](https://github.com/ixuh12)の誤ったバックアップ時刻を修正

    -   Dumpling

        -   GetDSN が IPv6 [#36112](https://github.com/pingcap/tidb/issues/36112) @ [D3ハンター](https://github.com/D3Hunter)をサポートしていない問題を修正

    -   TiDBBinlog

        -   `compressor`が`gzip` [#1152](https://github.com/pingcap/tidb-binlog/issues/1152) @ [リチュンジュ](https://github.com/lichunzhu)に設定されている場合、 Drainer がPumpに正しくリクエストを送信できないというバグを修正します
