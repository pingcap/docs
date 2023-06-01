---
title: TiDB 6.1.1 Release Notes
---

# TiDB 6.1.1 リリースノート {#tidb-6-1-1-release-notes}

発売日：2022年9月1日

TiDB バージョン: 6.1.1

クイックアクセス: [インストールパッケージ](https://www.pingcap.com/download/?version=v6.1.1#version-list)

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   `SHOW DATABASES LIKE …`ステートメントの大文字と小文字を区別しないようにします[e1ijah1](https://github.com/e1ijah1)
    -   デフォルト値[`tidb_enable_outer_join_reorder`](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610) `1`から`0`に変更します。これにより、Join Reorder によるアウター結合のサポートがデフォルトで無効になります。

-   診断

    -   継続的プロファイリング機能をデフォルトで無効にすると、この機能が有効になっているときに発生する可能性のあるTiFlashクラッシュの問題が回避されます。詳細は[モニクス](https://github.com/mornyx)を参照してください。

## その他の変更点 {#other-changes}

-   `TiDB-community-toolkit`バイナリ パッケージに以下の内容を追加します。詳細は[TiDB インストール パッケージ](/binary-package.md)を参照してください。

    -   `server-{version}-linux-amd64.tar.gz`
    -   `grafana-{version}-linux-amd64.tar.gz`
    -   `alertmanager-{version}-linux-amd64.tar.gz`
    -   `prometheus-{version}-linux-amd64.tar.gz`
    -   `blackbox_exporter-{version}-linux-amd64.tar.gz`
    -   `node_exporter-{version}-linux-amd64.tar.gz`

-   オペレーティング システムと CPU アーキテクチャの組み合わせに関するさまざまな品質基準に対するマルチレベルのサポートを導入します。 [OS とプラットフォームの要件](https://docs.pingcap.com/tidb/v6.1/hardware-and-software-requirements#os-and-platform-requirements)を参照してください。

## 改善点 {#improvements}

-   TiDB

    -   新しいオプティマイザ`SEMI_JOIN_REWRITE`を追加して、 `EXISTS`クエリ[ウィノロス](https://github.com/winoros)のパフォーマンスを向上させます。

-   TiKV

    -   gzip を使用したメトリクス応答の圧縮をサポートし、HTTP 本文のサイズ[ウィノロス](https://github.com/winoros)を削減します。
    -   [グロルフ](https://github.com/glorv)を使用して一部のメトリクスをフィルタリングすることにより、リクエストごとに返されるデータ量の削減をサポートします。
    -   RocksDB で同時に実行されるサブコンパクション操作の数の動的変更をサポート ( `rocksdb.max-sub-compactions` ) [エーテルフロー](https://github.com/ethercflow)

-   PD

    -   特定のステージ[バッファフライ](https://github.com/bufferflies)におけるバランスリージョンのスケジューリング速度を向上させます。

-   ツール

    -   TiDB Lightning

        -   `stale command`などのエラーに対する再試行メカニズムを追加して、インポート成功率[D3ハンター](https://github.com/D3Hunter)を向上させます。

    -   TiDB データ移行 (DM)

        -   ユーザーは、Lightning Loader [ブチュイトデゴウ](https://github.com/buchuitoudegou)の同時実行量を手動で設定できます。

    -   TiCDC

        -   シンク URI パラメーター`transaction-atomicity`を追加して、変更フィード内の大規模なトランザクションの分割をサポートします。これにより、大規模なトランザクションのレイテンシーとメモリ消費量を大幅に削減できます[CharlesCheung96](https://github.com/CharlesCheung96)
        -   マルチリージョン シナリオ[ひっくり返る](https://github.com/hicqu)でのランタイム コンテキストの切り替えによって生じるパフォーマンスのオーバーヘッドを削減します。
        -   MySQL シンクを強化してセーフ モードを自動的にオフにする[オーバーヴィーナス](https://github.com/overvenus)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `INL_HASH_JOIN` `LIMIT` [グオシャオゲ](https://github.com/guo-shaoge)と一緒に使用するとハングする可能性がある問題を修正
    -   `UPDATE`ステートメント[イーサール](https://github.com/Yisaer)の実行時に TiDB がpanic可能性がある問題を修正
    -   `SHOW COLUMNS`ステートメント[タンジェンタ](https://github.com/tangenta)の実行時に TiDB がコプロセッサ リクエストを送信する可能性があるバグを修正
    -   `SHOW WARNINGS`ステートメント[ジグアン](https://github.com/zyguan)を実行すると TiDB が`invalid memory address or nil pointer dereference`エラーを返すことがあるバグを修正
    -   静的パーティション プルーン モードにおいて、テーブルが空の場合に集計条件を含む SQL ステートメントが間違った結果を返す可能性があるバグを修正[ティエンチャイアマオ](https://github.com/tiancaiamao)
    -   結合したテーブルの再配置操作により誤って外部結合条件[ウィノロス](https://github.com/winoros)がプッシュダウンされる問題を修正します。
    -   CTE スキーマのハッシュ コードが誤って複製され、CTE が複数回参照されると`Can't find column ... in schema ...`エラーが発生する問題を修正[アイリンキッド](https://github.com/AilinKid)
    -   一部の右外部結合シナリオで結合の再順序が間違っていると、間違ったクエリ結果[ウィノロス](https://github.com/winoros)が発生する問題を修正します。
    -   EqualAll case [修正データベース](https://github.com/fixdb)でのTiFlash `firstrow`集約関数の null フラグが誤って推論される問題を修正
    -   `IGNORE_PLAN_CACHE`ヒント[fzzf678](https://github.com/fzzf678)でバインディングが作成されるとプラン キャッシュが機能しない問題を修正
    -   ハッシュ パーティション ウィンドウと単一パーティション ウィンドウ[リトルフォール](https://github.com/LittleFall)の間に`EXCHANGE`演算子が欠落している問題を修正
    -   場合によっては、パーティション テーブルがインデックスを完全に使用してデータをスキャンできない問題を修正します[むじょん](https://github.com/mjonss)
    -   集計がプッシュダウンされた後、部分集計に間違ったデフォルト値が設定されている場合に、間違ったクエリ結果が表示される問題を修正します[ティエンチャイアマオ](https://github.com/tiancaiamao)
    -   場合によってはパーティション テーブルのクエリで`index-out-of-range`エラーが発生することがある問題を修正します[むじょん](https://github.com/mjonss)
    -   クエリ条件でパーティション キーが使用されており、照合順序がクエリ パーティション テーブル[むじょん](https://github.com/mjonss)の照合順序と異なる場合、パーティションが誤ってプルーニングされる問題を修正します。
    -   TiDB Binlogが有効な場合、 `ALTER SEQUENCE`ステートメントを実行するとメタデータのバージョンが間違って、 Drainerが終了する可能性がある問題を修正します[アイリンキッド](https://github.com/AilinKid)
    -   一部の極端なケースで起動時に表示される可能性がある不正な TiDB ステータスの問題を修正します[ゼボックス](https://github.com/xhebox)
    -   TiDB ダッシュボード[時間と運命](https://github.com/time-and-fate)でパーティション化されたテーブルの実行プランをクエリするときに発生する潜在的な問題`UnknownPlanID`修正します。
    -   LOAD DATA ステートメント[SpadeA-Tang](https://github.com/SpadeA-Tang)で列リストが機能しない問題を修正します。
    -   TiDB Binlogが有効になっている場合に重複した値を挿入するときに発生する`data and columnID count not match`エラーの問題を修正します[ジグアン](https://github.com/zyguan)
    -   `tidb_gc_life_time` [トンスネークリン](https://github.com/TonsnakeLin)の制限を削除します
    -   空のフィールドターミネータが使用されている場合の`LOAD DATA`ステートメントのデッドループを修正[ジグアン](https://github.com/zyguan)
    -   可用性を向上させるために、異常な TiKV ノードへのリクエストの送信を回避します[スティックナーフ](https://github.com/sticnarf)

-   TiKV

    -   Raftstoreがビジー[5kbps](https://github.com/5kbpers)の場合リージョンが重なる可能性があるバグを修正
    -   リージョンハートビートが中断された後、PD が TiKV に再接続しない問題を修正[バッファフライ](https://github.com/bufferflies)
    -   空の文字列[wshwsh12](https://github.com/wshwsh12)の型変換を実行すると TiKV がパニックになる問題を修正
    -   TiKV と PD [5kbps](https://github.com/5kbpers)の間の一貫性のないリージョンサイズ構成の問題を修正
    -   Raft Engineが有効になっている場合に暗号化キーがクリーンアップされない問題を修正[タボキー](https://github.com/tabokie)
    -   ピアの分割と破棄が同時に行われるときに発生する可能性があるpanicの問題を修正[ビジージェイ](https://github.com/BusyJay)
    -   リージョンマージ プロセス[ビジージェイ](https://github.com/BusyJay)でソース ピアがスナップショットによってログを追いつくときに発生する可能性があるpanicの問題を修正します。
    -   PD クライアントでエラー[コナー1996](https://github.com/Connor1996)が発生したときに発生する、PD クライアントの再接続が頻繁に発生する問題を修正します。
    -   Raft Engine [タボキー](https://github.com/tabokie)で並列リカバリが有効になっている場合の潜在的なpanicを修正
    -   新しいリージョンのコミット ログ期間が長すぎるため、QPS が[コナー1996](https://github.com/Connor1996)低下する問題を修正します。
    -   Raft Engine が有効になっている場合にまれに発生するパニックを修正[タボキー](https://github.com/tabokie)
    -   proc ファイルシステム (procfs) が見つからない場合の冗長なログ警告を回避します[タボキー](https://github.com/tabokie)
    -   ダッシュボード[グロルフ](https://github.com/glorv)の`Unified Read Pool CPU`の間違った式を修正
    -   リージョンが大きい場合、デフォルトの[トニーシュクキ](https://github.com/tonyxuqqi)より大きくなる可能性がある問題を修正
    -   スナップショットの適用が中止され、 Raft Engineが有効になっている場合に TiKV がpanicになる可能性がある問題を修正[タボキー](https://github.com/tabokie)
    -   PD クライアントがデッドロックを引き起こす可能性がある問題を修正[バートン秦](https://github.com/BurtonQin)

-   PD

    -   クラスタノードのラベル設定が無効な場合、オンラインの進行状況が不正確になる問題を修正[ルルンクス](https://github.com/rleungx)
    -   `enable-forwarding`が有効になっている場合に gRPC がエラーを不適切に処理する問題によって引き起こされる PD パニックを修正[バッファフライ](https://github.com/bufferflies)
    -   `/regions/replicated`間違ったステータス[ルルンクス](https://github.com/rleungx)を返す可能性がある問題を修正

-   TiFlash

    -   一部の状況でクラスター化インデックスを持つテーブルの列を削除した後にTiFlash がクラッシュする問題を修正[ホンユニャン](https://github.com/hongyunyan)
    -   `format`関数が`Data truncated`エラー[xzhangxian1008](https://github.com/xzhangxian1008)を返す可能性がある問題を修正します。
    -   一部の古いデータがstorageに残り、削除できない可能性がある問題を修正します[リデズ](https://github.com/lidezhu)
    -   一部のエッジケースでの不必要な CPU 使用率を修正[ブリーズウィッシュ](https://github.com/breezewish)
    -   IPv6 [ソロッツグ](https://github.com/solotzg)を使用したクラスターでTiFlashが動作できないバグを修正
    -   並列集計[ゲンリチ](https://github.com/gengliqi)のエラーによりTiFlash がクラッシュする可能性があるバグを修正
    -   `MinTSOScheduler`クエリエラー[ウィンドトーカー](https://github.com/windtalker)の場合にスレッドリソースがリークする可能性があるバグを修正

-   ツール

    -   TiDB Lightning

        -   TiDB が IPv6 ホスト[D3ハンター](https://github.com/D3Hunter)を使用している場合、 TiDB Lightningが TiDB に接続できない問題を修正
        -   再試行メカニズム[D3ハンター](https://github.com/D3Hunter)を追加して`read index not ready`エラーを修正
        -   ログ内の機密情報がサーバーモード[リチュンジュ](https://github.com/lichunzhu)で出力される問題を修正
        -   TiDB Lightning がParquet ファイル[D3ハンター](https://github.com/D3Hunter)でスラッシュ、数字、または非 ASCII 文字で始まる列をサポートしない問題を修正します。
        -   重複排除により、極端な場合にTiDB Lightning がpanicを引き起こす可能性がある問題を修正します[フォワードスター](https://github.com/ForwardStar)

    -   TiDB データ移行 (DM)

        -   DM [フォワードスター](https://github.com/ForwardStar)で`txn-entry-size-limit`設定項目が有効にならない問題を修正
        -   `check-task`コマンドが特殊文字[Ehco1996](https://github.com/Ehco1996)を処理できない問題を修正
        -   `query-status` [lyzx2001](https://github.com/lyzx2001)で発生する可能性のあるデータ競合の問題を修正
        -   `operate-schema`コマンド[フォワードスター](https://github.com/ForwardStar)の異なる出力形式を修正
        -   リレーがエラー[ランス6716](https://github.com/lance6716)に遭遇したときの goroutine リークを修正
        -   DB Conn [ランス6716](https://github.com/lance6716)を取得するときに DM Worker がスタックすることがある問題を修正
        -   TiDB が IPv6 ホスト[D3ハンター](https://github.com/D3Hunter)を使用する場合に DM が起動できない問題を修正

    -   TiCDC

        -   間違った最大互換バージョン番号[こんにちはラスティン](https://github.com/hi-rustin)を修正
        -   cdcサーバーが完全に起動する前に HTTP リクエストを受信するとpanicを引き起こす可能性があるバグを修正[東門](https://github.com/asddongmen)
        -   チェンジフィード同期ポイントが有効になっている場合の ddl シンクpanicの問題を修正[東門](https://github.com/asddongmen)
        -   同期ポイントが有効になっている場合、一部のシナリオで変更フィードがスタックする問題を修正[ひっくり返る](https://github.com/hicqu)
        -   CDCサーバーの再起動後にchangefeed APIが正常に動作しないバグを修正[東門](https://github.com/asddongmen)
        -   ブラック ホール シンク[東門](https://github.com/asddongmen)のデータ競合問題を修正
        -   `enable-old-value = false` [こんにちはラスティン](https://github.com/hi-rustin)を設定した場合の TiCDCpanicの問題を修正
        -   REDO ログ機能が有効になっている場合のデータ整合性の問題を修正[東門](https://github.com/asddongmen)
        -   REDO イベントを非同期に書き込むことで、REDO ログのパフォーマンスの低下を修正[CharlesCheung96](https://github.com/CharlesCheung96)
        -   MySQL シンクが IPv6 アドレス[こんにちはラスティン](https://github.com/hi-rustin)に接続できない問題を修正

    -   バックアップと復元 (BR)

        -   RawKV モード[3ポインター](https://github.com/3pointer)でBR が`ErrRestoreTableIDMismatch`を報告するバグを修正
        -   バックアップ データ ディレクトリ構造を調整して、大規模クラスタ バックアップ[モクイシュル28](https://github.com/MoCuishle28)での S3 レート制限によって引き起こされるバックアップの失敗を修正します。
        -   概要ログ[ixuh12](https://github.com/ixuh12)の誤ったバックアップ時間を修正しました。

    -   Dumpling

        -   GetDSN が IPv6 [D3ハンター](https://github.com/D3Hunter)をサポートしていない問題を修正

    -   TiDBBinlog

        -   `compressor`を`gzip` [リチュンジュ](https://github.com/lichunzhu)に設定すると、 DrainerがPumpにリクエストを正しく送信できないバグを修正
