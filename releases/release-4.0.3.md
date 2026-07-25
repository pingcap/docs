---
title: TiDB 4.0.3 Release Notes
summary: TiDB 4.0.3は2020年7月24日にリリースされました。新機能には、TiDB Dashboardの改善、 TiFlashファイルの暗号化、各種ツールのサポートが含まれます。TiDB、TiKV、PD、TiDB Dashboardの機能強化に加え、TiDB、TiKV、PD、TiDB Dashboard、 TiFlash、TiCDC、バックアップ＆リストア、 Dumpling、 TiDB Lightning、TiDB Binlogのバグ修正も実装されました。
---

# TiDB 4.0.3 リリースノート {#tidb-4-0-3-release-notes}

発売日：2020年7月24日

TiDB バージョン: 4.0.3

## 新機能 {#new-features}

-   TiDB Dashboard

    -   TiDB Dashboardの詳細なバージョン情報を表示する[＃679](https://github.com/pingcap-incubator/tidb-dashboard/pull/679)
    -   サポートされていないブラウザまたは古いブラウザのブラウザ互換性に関する通知を表示する[＃654](https://github.com/pingcap-incubator/tidb-dashboard/pull/654)
    -   **SQL文の**ページでの検索をサポート [＃658](https://github.com/pingcap-incubator/tidb-dashboard/pull/658)

-   TiFlash

    -   TiFlashプロキシでファイル暗号化を実装する

-   ツール

    -   Backup & Restore (BR)

        -   zstd、lz4、snappy を使用したバックアップファイルの圧縮をサポート [＃404](https://github.com/pingcap/br/pull/404)

    -   TiCDC

        -   MQ sink-uri で`kafka-client-id`構成をサポート [＃706](https://github.com/pingcap/tiflow/pull/706)
        -   `changefeed`構成のオフライン更新をサポート[＃699](https://github.com/pingcap/tiflow/pull/699)
        -   サポート設定カスタマイズ`changefeed`名前[＃727](https://github.com/pingcap/tiflow/pull/727)
        -   TLSおよびMySQL SSL接続サポート [＃347](https://github.com/pingcap/tiflow/pull/347)
        -   Avro 形式での変更の出力をサポート [＃753](https://github.com/pingcap/tiflow/pull/753)
        -   Apache Pulsar シンクサポートする [＃751](https://github.com/pingcap/tiflow/pull/751)

    -   Dumpling

        -   特殊なCSV区切り文字と区切り文字サポート [＃116](https://github.com/pingcap/dumpling/pull/116)
        -   出力ファイル名の形式の指定をサポート[＃122](https://github.com/pingcap/dumpling/pull/122)

## 改善点 {#improvements}

-   TiDB

    -   SQLクエリをログに記録するときに感度を下げるかどうかを制御する`tidb_log_desensitization`グローバル変数を追加します[＃18581](https://github.com/pingcap/tidb/pull/18581)
    -   デフォルトで`tidb_allow_batch_cop`有効にする[＃18552](https://github.com/pingcap/tidb/pull/18552)
    -   クエリのキャンセルを高速化[＃18505](https://github.com/pingcap/tidb/pull/18505)
    -   `tidb_decode_plan`の結果にヘッダーを追加 [＃18501](https://github.com/pingcap/tidb/pull/18501)
    -   構成チェッカーを以前のバージョンの構成ファイルと互換性のあるものにする [＃18046](https://github.com/pingcap/tidb/pull/18046)
    -   実行情報の収集をデフォルトで有効にする[＃18518](https://github.com/pingcap/tidb/pull/18518)
    -   システムテーブル`tiflash_tables`と`tiflash_segments`を追加する[＃18536](https://github.com/pingcap/tidb/pull/18536)
    -   `AUTO RANDOM`実験的機能から一般公開となり、リリースされました。改善点と互換性の変更点は以下の通りです。
        -   設定ファイル内の`experimental.allow-auto-random`非推奨です。この項目の設定に関わらず、列の`AUTO RANDOM`機能はいつでも定義できます[＃18613](https://github.com/pingcap/tidb/pull/18613) [＃18623](https://github.com/pingcap/tidb/pull/18623)
        -   `AUTO RANDOM`列への明示的な書き込みを制御するために、セッション変数`tidb_allow_auto_random_explicit_insert`追加します。デフォルト値は`false`です。これは、列への明示的な書き込みによって発生する予期し`AUTO_RANDOM_BASE`更新を回避するためです[＃18508](https://github.com/pingcap/tidb/pull/18508)
        -   `BIGINT`列と`UNSIGNED BIGINT`列にのみ`AUTO_RANDOM`を定義できるようにし、シャードビットの最大数を`15`に制限することで、割り当て可能なスペースが急速に消費されるのを回避します[＃18538](https://github.com/pingcap/tidb/pull/18538)
        -   `BIGINT`列に`AUTO_RANDOM`属性を定義し、主キーに負の値を挿入するときに`AUTO_RANDOM_BASE`更新をトリガーしないでください。 [＃17987](https://github.com/pingcap/tidb/pull/17987)
        -   `UNSIGNED BIGINT`列に`AUTO_RANDOM`属性を定義するときに、IDの割り当てに整数の最上位ビットを使用します。これにより、割り当て可能なスペースが増えます。 [＃18404](https://github.com/pingcap/tidb/pull/18404)
        -   `SHOW CREATE TABLE` の結果の`AUTO_RANDOM`属性の更新をサポートします [＃18316](https://github.com/pingcap/tidb/pull/18316)

-   TiKV

    -   バックアップスレッドプールのサイズを制御するための新しい`backup.num-threads`構成を導入する [＃8199](https://github.com/tikv/tikv/pull/8199)
    -   スナップショット受信時にストアハートビートを送信しない [＃8136](https://github.com/tikv/tikv/pull/8136)
    -   共有ブロックキャッシュの容量を動的に変更する機能をサポート[＃8232](https://github.com/tikv/tikv/pull/8232)

-   PD

    -   JSON形式のログサポート [＃2565](https://github.com/pingcap/pd/pull/2565)

-   TiDB Dashboard

    -   コールド論理範囲の Key Visualizer バケット マージの改善 [＃674](https://github.com/pingcap-incubator/tidb-dashboard/pull/674)
    -   一貫性を保つために構成項目`disable-telemetry`の名前を`enable-telemetry`に変更します[＃684](https://github.com/pingcap-incubator/tidb-dashboard/pull/684)
    -   ページ切り替え時にプログレスバーを表示する[＃661](https://github.com/pingcap-incubator/tidb-dashboard/pull/661)
    -   スペース区切り文字がある場合、低速ログ検索がログ検索と同じ動作をすることを確認します[＃682](https://github.com/pingcap-incubator/tidb-dashboard/pull/682)

-   TiFlash

    -   Grafanaの**DDLジョブ**パネルの単位を`operations per minute`に変更します
    -   **TiFlash-Proxy**に関するより多くのメトリクスを表示するためにGrafanaに新しいダッシュボードを追加します
    -   TiFlashプロキシのIOPSを削減する

-   ツール

    -   TiCDC

        -   メトリクステーブルIDをテーブル名に置き換える [＃695](https://github.com/pingcap/tiflow/pull/695)

    -   Backup & Restore (BR)

        -   JSONログの出力をサポート[＃336](https://github.com/pingcap/br/issues/336)
        -   実行時にpprofを有効にするサポート[＃372](https://github.com/pingcap/br/pull/372)
        -   復元中にDDLを同時に送信することでDDL実行を高速化[＃377](https://github.com/pingcap/br/pull/377)

    -   TiDB Lightning

        -   `black-white-list`を廃止し、より新しくて分かりやすいフィルター形式導入する [＃332](https://github.com/pingcap/tidb-lightning/pull/332)

## バグ修正 {#bug-fixes}

-   TiDB

    -   実行中にエラーが発生した場合、 `IndexHashJoin`空集合の代わりにエラーを返します[＃18586](https://github.com/pingcap/tidb/pull/18586)
    -   gRPC トランスポートリーダーが壊れているときに繰り返し発生するpanicを修正[＃18562](https://github.com/pingcap/tidb/pull/18562)
    -   Green GC がオフライン ストアのロックをスキャンしないため、データの不完全性が発生する可能性がある問題を修正しました[＃18550](https://github.com/pingcap/tidb/pull/18550)
    -   TiFlashエンジンを使用して非読み取り専用ステートメントの処理を禁止する [＃18534](https://github.com/pingcap/tidb/pull/18534)
    -   クエリ接続がパニックになったときに実際のエラーメッセージを返す[＃18500](https://github.com/pingcap/tidb/pull/18500)
    -   `ADMIN REPAIR TABLE`目の実行で TiDB ノードのテーブル メタデータの再ロードに失敗する問題を修正しました。 [＃18323](https://github.com/pingcap/tidb/pull/18323)
    -   あるトランザクションで書き込まれ、削除された主キーのロックが別のトランザクションによって解決されたために発生したデータの不整合の問題を修正しました[＃18291](https://github.com/pingcap/tidb/pull/18291)
    -   スピルディスクをうまく機能させる[＃18288](https://github.com/pingcap/tidb/pull/18288)
    -   生成された列を含むテーブルで`REPLACE INTO`文が機能するときに報告されるエラーを修正します [＃17907](https://github.com/pingcap/tidb/pull/17907)
    -   `IndexHashJoin`と`IndexMergeJoin`ワーカーがpanicときにOOMエラーを返す[＃18527](https://github.com/pingcap/tidb/pull/18527)
    -   `Index Join`で使用されるインデックスに整数の主キーが含まれている場合、特別なケースで`Index Join`実行によって誤った結果が返される可能性があるバグを修正しました。 [＃18565](https://github.com/pingcap/tidb/pull/18565)
    -   クラスターで新しい照合順序が有効になっている場合、トランザクションで新しい照合順序を持つ列に更新されたデータが一意インデックスを通じて読み取れない問題を修正しました。 [＃18703](https://github.com/pingcap/tidb/pull/18703)

-   TiKV

    -   マージ中に読み取りで古いデータが取得される可能性がある問題を修正[＃8113](https://github.com/tikv/tikv/pull/8113)
    -   集計が TiKV にプッシュダウンされたときに`min` `max`で照合順序が機能しない問題を修正しました [＃8108](https://github.com/tikv/tikv/pull/8108)

-   PD

    -   サーバーがクラッシュした場合にTSOストリームの作成がしばらくブロックされる可能性がある問題を修正しました[＃2648](https://github.com/pingcap/pd/pull/2648)
    -   `getSchedulers`データ競合を引き起こす可能性がある問題を修正[＃2638](https://github.com/pingcap/pd/pull/2638)
    -   スケジューラを削除するとデッドロックが発生する可能性がある問題を修正[＃2637](https://github.com/pingcap/pd/pull/2637)
    -   `balance-leader-scheduler`が有効になっているときに配置ルールが考慮されないバグを修正[＃2636](https://github.com/pingcap/pd/pull/2636)
    -   サービス`safepoint`が正しく設定されない場合があり、 BRとDumplingが失敗する可能性がある問題を修正[＃2635](https://github.com/pingcap/pd/pull/2635)
    -   `hot region scheduler`の対象ストアが誤って選択されている問題を修正[＃2627](https://github.com/pingcap/pd/pull/2627)
    -   PDリーダーが切り替えられたときにTSOリクエストに時間がかかりすぎる可能性がある問題を修正[＃2622](https://github.com/pingcap/pd/pull/2622)
    -   リーダー変更後の古いスケジューラの問題を修正[＃2608](https://github.com/pingcap/pd/pull/2608)
    -   配置ルールが有効になっているときに、リージョンのレプリカを最適な場所に調整できないことがある問題を修正しました[＃2605](https://github.com/pingcap/pd/pull/2605)
    -   展開ディレクトリの変更に応じてストアの展開パスが更新されない問題を修正 [＃2600](https://github.com/pingcap/pd/pull/2600)
    -   `store limit` 0になるのを防ぐ[＃2588](https://github.com/pingcap/pd/pull/2588)

-   TiDB Dashboard

    -   TiDB がスケールアウトされたときの TiDB 接続エラーを修正[＃689](https://github.com/pingcap-incubator/tidb-dashboard/pull/689)
    -   ログ検索ページにTiFlashインスタンスが表示されない問題を修正 [＃680](https://github.com/pingcap-incubator/tidb-dashboard/pull/680)
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

    -   Backup & Restore (BR)

        -   バックアップ時間がマイナスになる可能性がある問題を修正 [＃405](https://github.com/pingcap/br/pull/405)

    -   Dumpling

        -   Dumplingが`--r`を指定した場合に`NULL`値を省略する問題を修正[＃119](https://github.com/pingcap/dumpling/pull/119)
        -   テーブルのフラッシュがテーブルをダンプに実行できない可能性があるバグを修正しました [＃117](https://github.com/pingcap/dumpling/pull/117)

    -   TiDB Lightning

        -   `--log-file`が有効にならない問題を修正[＃345](https://github.com/pingcap/tidb-lightning/pull/345)

    -   TiDB Binlog

        -   TiDB Binlog がTLS を有効にしてダウンストリームにデータを複製する場合、チェックポイント更新に使用されるデータベース ドライバーで TLS が有効になっていないためにDrainerを起動できない問題を修正しました。 [＃988](https://github.com/pingcap/tidb-binlog/pull/988)
