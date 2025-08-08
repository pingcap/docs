---
title: TiDB 4.0.3 Release Notes
summary: TiDB 4.0.3は2020年7月24日にリリースされました。新機能には、TiDBダッシュボードの改善、 TiFlashファイルの暗号化、各種ツールのサポートが含まれます。TiDB、TiKV、PD、TiDBダッシュボードの機能強化に加え、TiDB、TiKV、PD、TiDBダッシュボード、 TiFlash、TiCDC、バックアップ＆リストア、 Dumpling、 TiDB Lightning、TiDB Binlogのバグ修正も実装されました。
---

# TiDB 4.0.3 リリースノート {#tidb-4-0-3-release-notes}

発売日：2020年7月24日

TiDB バージョン: 4.0.3

## 新機能 {#new-features}

-   TiDBダッシュボード

    -   TiDBダッシュボードの詳細なバージョン情報を表示する[＃679](https://github.com/pingcap-incubator/tidb-dashboard/pull/679)
    -   サポートされていないブラウザまたは古いブラウザのブラウザ互換性に関する通知を表示する[＃654](https://github.com/pingcap-incubator/tidb-dashboard/pull/654)
    -   **SQL文の**ページ[＃658](https://github.com/pingcap-incubator/tidb-dashboard/pull/658)での検索をサポート

-   TiFlash

    -   TiFlashプロキシでファイル暗号化を実装する

-   ツール

    -   バックアップと復元 (BR)

        -   zstd、lz4、snappy [＃404](https://github.com/pingcap/br/pull/404)を使用したバックアップファイルの圧縮をサポート

    -   TiCDC

        -   MQ sink-uri [＃706](https://github.com/pingcap/tiflow/pull/706)で`kafka-client-id`構成をサポート
        -   `changefeed`構成のオフライン更新をサポート[＃699](https://github.com/pingcap/tiflow/pull/699)
        -   サポート設定カスタマイズ`changefeed`名前[＃727](https://github.com/pingcap/tiflow/pull/727)
        -   TLSおよびMySQL SSL接続[＃347](https://github.com/pingcap/tiflow/pull/347)サポート
        -   Avro 形式[＃753](https://github.com/pingcap/tiflow/pull/753)での変更の出力をサポート
        -   Apache Pulsar シンク[＃751](https://github.com/pingcap/tiflow/pull/751)サポートする

    -   Dumpling

        -   特殊なCSV区切り文字と区切り文字[＃116](https://github.com/pingcap/dumpling/pull/116)サポート
        -   出力ファイル名の形式の指定をサポート[＃122](https://github.com/pingcap/dumpling/pull/122)

## 改善点 {#improvements}

-   TiDB

    -   SQLクエリをログに記録するときに感度を下げるかどうかを制御する`tidb_log_desensitization`グローバル変数を追加します[＃18581](https://github.com/pingcap/tidb/pull/18581)
    -   デフォルトで`tidb_allow_batch_cop`有効にする[＃18552](https://github.com/pingcap/tidb/pull/18552)
    -   クエリのキャンセルを高速化[＃18505](https://github.com/pingcap/tidb/pull/18505)
    -   `tidb_decode_plan`の結果[＃18501](https://github.com/pingcap/tidb/pull/18501)にヘッダーを追加
    -   構成チェッカーを以前のバージョンの構成ファイル[＃18046](https://github.com/pingcap/tidb/pull/18046)と互換性のあるものにする
    -   実行情報の収集をデフォルトで有効にする[＃18518](https://github.com/pingcap/tidb/pull/18518)
    -   システムテーブル`tiflash_tables`と`tiflash_segments`を追加する[＃18536](https://github.com/pingcap/tidb/pull/18536)
    -   `AUTO RANDOM`実験的機能から一般公開となり、リリースされました。改善点と互換性の変更点は以下の通りです。
        -   設定ファイル内の`experimental.allow-auto-random`非推奨です。この項目の設定に関わらず、列の`AUTO RANDOM`機能はいつでも定義できます[＃18613](https://github.com/pingcap/tidb/pull/18613) [＃18623](https://github.com/pingcap/tidb/pull/18623)
        -   `AUTO RANDOM`列への明示的な書き込みを制御するために、セッション変数`tidb_allow_auto_random_explicit_insert`追加します。デフォルト値は`false`です。これは、列への明示的な書き込みによって発生する予期し`AUTO_RANDOM_BASE`更新を回避するためです[＃18508](https://github.com/pingcap/tidb/pull/18508)
        -   `BIGINT`列と`UNSIGNED BIGINT`列にのみ`AUTO_RANDOM`定義できるようにし、シャードビットの最大数を`15`に制限することで、割り当て可能なスペースが急速に消費されるのを回避します[＃18538](https://github.com/pingcap/tidb/pull/18538)
        -   `BIGINT`列目に`AUTO_RANDOM`属性を定義し、主キー[＃17987](https://github.com/pingcap/tidb/pull/17987)に負の値を挿入するときに`AUTO_RANDOM_BASE`更新をトリガーしないでください。
        -   `UNSIGNED BIGINT`列に`AUTO_RANDOM`属性を定義するときに、IDの割り当てに整数の最上位ビットを使用します。これにより、割り当て可能なスペースが[＃18404](https://github.com/pingcap/tidb/pull/18404)増えます。
        -   `SHOW CREATE TABLE` [＃18316](https://github.com/pingcap/tidb/pull/18316)の結果の`AUTO_RANDOM`属性の更新をサポートします

-   TiKV

    -   バックアップスレッドプール[＃8199](https://github.com/tikv/tikv/pull/8199)のサイズを制御するための新しい`backup.num-threads`構成を導入する
    -   スナップショット[＃8136](https://github.com/tikv/tikv/pull/8136)受信時にストアハートビートを送信しない
    -   共有ブロックキャッシュの容量を動的に変更する機能をサポート[＃8232](https://github.com/tikv/tikv/pull/8232)

-   PD

    -   JSON形式のログ[＃2565](https://github.com/pingcap/pd/pull/2565)サポート

-   TiDBダッシュボード

    -   コールド論理範囲[＃674](https://github.com/pingcap-incubator/tidb-dashboard/pull/674)の Key Visualizer バケット マージの改善
    -   一貫性を保つために構成項目`disable-telemetry`の名前を`enable-telemetry`に変更します[＃684](https://github.com/pingcap-incubator/tidb-dashboard/pull/684)
    -   ページ切り替え時にプログレスバーを表示する[＃661](https://github.com/pingcap-incubator/tidb-dashboard/pull/661)
    -   スペース区切り文字がある場合、低速ログ検索がログ検索と同じ動作をすることを確認します[＃682](https://github.com/pingcap-incubator/tidb-dashboard/pull/682)

-   TiFlash

    -   Grafanaの**DDLジョブ**パネルの単位を`operations per minute`に変更します
    -   **TiFlash-Proxy**に関するより多くのメトリクスを表示するためにGrafanaに新しいダッシュボードを追加します
    -   TiFlashプロキシのIOPSを削減する

-   ツール

    -   TiCDC

        -   メトリクス[＃695](https://github.com/pingcap/tiflow/pull/695)テーブルIDをテーブル名に置き換える

    -   バックアップと復元 (BR)

        -   JSONログの出力をサポート[＃336](https://github.com/pingcap/br/issues/336)
        -   実行時にpprofを有効にするサポート[＃372](https://github.com/pingcap/br/pull/372)
        -   復元中にDDLを同時に送信することでDDL実行を高速化[＃377](https://github.com/pingcap/br/pull/377)

    -   TiDB Lightning

        -   `black-white-list`を廃止し、より新しくて分かりやすいフィルター形式[＃332](https://github.com/pingcap/tidb-lightning/pull/332)導入する

## バグ修正 {#bug-fixes}

-   TiDB

    -   実行中にエラーが発生した場合、 `IndexHashJoin`空集合の代わりにエラーを返します[＃18586](https://github.com/pingcap/tidb/pull/18586)
    -   gRPC トランスポートリーダーが壊れているときに繰り返し発生するpanicを修正[＃18562](https://github.com/pingcap/tidb/pull/18562)
    -   Green GC がオフライン ストアのロックをスキャンしないため、データの不完全性が発生する可能性がある問題を修正しました[＃18550](https://github.com/pingcap/tidb/pull/18550)
    -   TiFlashエンジン[＃18534](https://github.com/pingcap/tidb/pull/18534)を使用して非読み取り専用ステートメントの処理を禁止する
    -   クエリ接続がパニックになったときに実際のエラーメッセージを返す[＃18500](https://github.com/pingcap/tidb/pull/18500)
    -   `ADMIN REPAIR TABLE`目の実行で TiDB ノード[＃18323](https://github.com/pingcap/tidb/pull/18323)のテーブル メタデータの再ロードに失敗する問題を修正しました。
    -   あるトランザクションで書き込まれ、削除された主キーのロックが別のトランザクションによって解決されたために発生したデータの不整合の問題を修正しました[＃18291](https://github.com/pingcap/tidb/pull/18291)
    -   スピルディスクをうまく機能させる[＃18288](https://github.com/pingcap/tidb/pull/18288)
    -   生成された列[＃17907](https://github.com/pingcap/tidb/pull/17907)を含むテーブルで`REPLACE INTO`文が機能するときに報告されるエラーを修正します
    -   `IndexHashJoin`と`IndexMergeJoin`ワーカーがpanicときにOOMエラーを返す[＃18527](https://github.com/pingcap/tidb/pull/18527)
    -   `Index Join`で使用されるインデックスに整数の主キー[＃18565](https://github.com/pingcap/tidb/pull/18565)が含まれている場合、特別なケースで`Index Join`実行によって誤った結果が返される可能性があるバグを修正しました。
    -   クラスターで新しい照合順序が有効になっている場合、トランザクションで新しい照合順序を持つ列に更新されたデータが一意のインデックス[＃18703](https://github.com/pingcap/tidb/pull/18703)を通じて読み取れない問題を修正しました。

-   TiKV

    -   マージ中に読み取りで古いデータが取得される可能性がある問題を修正[＃8113](https://github.com/tikv/tikv/pull/8113)
    -   集計が TiKV [＃8108](https://github.com/tikv/tikv/pull/8108)にプッシュダウンされたときに`min` `max`で照合順序が機能しない問題を修正しました

-   PD

    -   サーバーがクラッシュした場合にTSOストリームの作成がしばらくブロックされる可能性がある問題を修正しました[＃2648](https://github.com/pingcap/pd/pull/2648)
    -   `getSchedulers`データ競合を引き起こす可能性がある問題を修正[＃2638](https://github.com/pingcap/pd/pull/2638)
    -   スケジューラを削除するとデッドロックが発生する可能性がある問題を修正[＃2637](https://github.com/pingcap/pd/pull/2637)
    -   `balance-leader-scheduler`が有効になっているときに配置ルールが考慮されないバグを修正[＃2636](https://github.com/pingcap/pd/pull/2636)
    -   サービス`safepoint`が正しく設定されない場合があり、 BRとダンプリングが失敗する可能性がある問題を修正しました[＃2635](https://github.com/pingcap/pd/pull/2635)
    -   `hot region scheduler`の対象店舗が誤って選択されている問題を修正[＃2627](https://github.com/pingcap/pd/pull/2627)
    -   PDリーダーが切り替えられたときにTSOリクエストに時間がかかりすぎる可能性がある問題を修正[＃2622](https://github.com/pingcap/pd/pull/2622)
    -   リーダー変更後の古いスケジューラの問題を修正[＃2608](https://github.com/pingcap/pd/pull/2608)
    -   配置ルールが有効になっているときに、リージョンのレプリカを最適な場所に調整できないことがある問題を修正しました[＃2605](https://github.com/pingcap/pd/pull/2605)
    -   展開ディレクトリ[＃2600](https://github.com/pingcap/pd/pull/2600)の変更に応じてストアの展開パスが更新されない問題を修正
    -   `store limit` 0になるのを防ぐ[＃2588](https://github.com/pingcap/pd/pull/2588)

-   TiDBダッシュボード

    -   TiDB がスケールアウトされたときの TiDB 接続エラーを修正[＃689](https://github.com/pingcap-incubator/tidb-dashboard/pull/689)
    -   ログ検索ページ[＃680](https://github.com/pingcap-incubator/tidb-dashboard/pull/680)にTiFlashインスタンスが表示されない問題を修正
    -   概要ページを更新した後にメトリック選択がリセットされる問題を修正[＃663](https://github.com/pingcap-incubator/tidb-dashboard/pull/663)
    -   一部の TLS シナリオでの接続の問題を修正[＃660](https://github.com/pingcap-incubator/tidb-dashboard/pull/660)
    -   言語ドロップダウンボックスが一部のケースで正しく表示されない問題を修正[＃677](https://github.com/pingcap-incubator/tidb-dashboard/pull/677)

-   TiFlash

    -   主キー列の名前を変更した後にTiFlashがクラッシュする問題を修正
    -   同時実行`Learner Read`と`Remove Region`デッドロックを引き起こす可能性がある問題を修正

-   ツール

    -   TiCDC

        -   TiCDC がメモリを起こす場合がある問題を修正[＃704](https://github.com/pingcap/tiflow/pull/704)
        -   引用符で囲まれていないテーブル名がSQL構文エラーを引き起こす問題を修正[＃676](https://github.com/pingcap/tiflow/pull/676)
        -   `p.stop`が呼び出された後にプロセッサが完全に終了しない問題を修正[＃693](https://github.com/pingcap/tiflow/pull/693)

    -   バックアップと復元 (BR)

        -   バックアップ時間がマイナス[＃405](https://github.com/pingcap/br/pull/405)になる可能性がある問題を修正

    -   Dumpling

        -   Dumplingが`--r`指定した場合に`NULL`値を省略する問題を修正[＃119](https://github.com/pingcap/dumpling/pull/119)
        -   テーブルのフラッシュがテーブルをダンプ[＃117](https://github.com/pingcap/dumpling/pull/117)に実行できない可能性があるバグを修正しました

    -   TiDB Lightning

        -   `--log-file`が有効にならない問題を修正[＃345](https://github.com/pingcap/tidb-lightning/pull/345)

    -   TiDBBinlog

        -   TiDB Binlog がTLS を有効にしてダウンストリームにデータを複製する場合、チェックポイント[＃988](https://github.com/pingcap/tidb-binlog/pull/988)更新に使用されるデータベース ドライバーで TLS が有効になっていないためにDrainerを起動できない問題を修正しました。
