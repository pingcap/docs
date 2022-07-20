---
title: TiDB 4.0.3 Release Notes
---

# TiDB4.0.3リリースノート {#tidb-4-0-3-release-notes}

発売日：2020年7月24日

TiDBバージョン：4.0.3

## 新機能 {#new-features}

-   TiDBダッシュボード

    -   詳細なTiDBダッシュボードのバージョン情報を表示する[＃679](https://github.com/pingcap-incubator/tidb-dashboard/pull/679)
    -   サポートされていないブラウザまたは古いブラウザのブラウザ互換性通知を表示する[＃654](https://github.com/pingcap-incubator/tidb-dashboard/pull/654)
    -   **SQLステートメント**ページ[＃658](https://github.com/pingcap-incubator/tidb-dashboard/pull/658)での検索のサポート

-   TiFlash

    -   TiFlashプロキシにファイル暗号化を実装する

-   ツール

    -   バックアップと復元（BR）

        -   zstd、lz4、または[＃404](https://github.com/pingcap/br/pull/404)を使用したバックアップファイルの圧縮をサポートする

    -   TiCDC

        -   MQシンクでの構成`kafka-client-id`のサポート[＃706](https://github.com/pingcap/tiflow/pull/706)
        -   `changefeed`の構成をオフラインで更新することをサポート[＃699](https://github.com/pingcap/tiflow/pull/699)
        -   カスタマイズされた`changefeed`名[＃727](https://github.com/pingcap/tiflow/pull/727)の設定をサポート
        -   TLSおよびMySQLSSL接続をサポート[＃347](https://github.com/pingcap/tiflow/pull/347)
        -   Avro形式での変更の出力をサポート[＃753](https://github.com/pingcap/tiflow/pull/753)
        -   ApachePulsarシンクをサポートする[＃751](https://github.com/pingcap/tiflow/pull/751)

    -   Dumpling

        -   専用のCSV区切り文字と区切り文字をサポートする[＃116](https://github.com/pingcap/dumpling/pull/116)
        -   出力ファイル名の形式の指定をサポート[＃122](https://github.com/pingcap/dumpling/pull/122)

## 改善 {#improvements}

-   TiDB

    -   `tidb_log_desensitization`のグローバル変数を追加して、SQLクエリをログに記録するときに感度を下げるかどうかを制御します[＃18581](https://github.com/pingcap/tidb/pull/18581)
    -   デフォルトで`tidb_allow_batch_cop`を有効にする[＃18552](https://github.com/pingcap/tidb/pull/18552)
    -   クエリのキャンセルを高速化[＃18505](https://github.com/pingcap/tidb/pull/18505)
    -   `tidb_decode_plan`の結果[＃18501](https://github.com/pingcap/tidb/pull/18501)のヘッダーを追加します
    -   構成チェッカーを以前のバージョンの構成ファイルと互換性があるようにする[＃18046](https://github.com/pingcap/tidb/pull/18046)
    -   デフォルトで実行情報の収集を有効にする[＃18518](https://github.com/pingcap/tidb/pull/18518)
    -   `tiflash_tables`と`tiflash_segments`のシステムテーブルを追加します[＃18536](https://github.com/pingcap/tidb/pull/18536)
    -   実験的機能から`AUTO RANDOM`移動し、その一般提供を発表します。改善点と互換性の変更は次のとおりです。
        -   構成ファイルで`experimental.allow-auto-random`を廃止します。このアイテムがどのように構成されていても、列に`AUTO RANDOM`の機能をいつでも定義できます。 [＃18613](https://github.com/pingcap/tidb/pull/18613) [＃18623](https://github.com/pingcap/tidb/pull/18623)
        -   `tidb_allow_auto_random_explicit_insert`セッション変数を追加して、 `AUTO RANDOM`列への明示的な書き込みを制御します。デフォルト値は`false`です。これは、列への明示的な書き込みによって引き起こされる`AUTO_RANDOM_BASE`しない更新を回避するためです。 [＃18508](https://github.com/pingcap/tidb/pull/18508)
        -   `BIGINT`列と`UNSIGNED BIGINT`列にのみ`AUTO_RANDOM`を定義できるようにし、シャードビットの最大数を`15`に制限します。これにより、割り当て可能なスペースが急速に消費されるのを防ぎます[＃18538](https://github.com/pingcap/tidb/pull/18538)
        -   `BIGINT`列に`AUTO_RANDOM`属性を定義し、主キー[＃17987](https://github.com/pingcap/tidb/pull/17987)に負の値を挿入するときに、 `AUTO_RANDOM_BASE`更新をトリガーしないでください。
        -   `UNSIGNED BIGINT`列に`AUTO_RANDOM`属性を定義する場合は、ID割り当てに整数の最上位ビットを使用します。これにより、より多くの割り当て可能スペースが取得されます[＃18404](https://github.com/pingcap/tidb/pull/18404)
        -   `SHOW CREATE TABLE`の結果で`AUTO_RANDOM` [＃18316](https://github.com/pingcap/tidb/pull/18316)の更新をサポート

-   TiKV

    -   新しい`backup.num-threads`構成を導入して、バックアップスレッドプール[＃8199](https://github.com/tikv/tikv/pull/8199)のサイズを制御します。
    -   スナップショットを受信するときにストアのハートビートを送信しない[＃8136](https://github.com/tikv/tikv/pull/8136)
    -   共有ブロックキャッシュの容量の動的変更をサポート[＃8232](https://github.com/tikv/tikv/pull/8232)

-   PD

    -   JSON形式のログ[＃2565](https://github.com/pingcap/pd/pull/2565)をサポートする

-   TiDBダッシュボード

    -   コールド論理範囲のキービジュアライザーバケットマージを改善する[＃674](https://github.com/pingcap-incubator/tidb-dashboard/pull/674)
    -   一貫性を保つために、構成アイテムの名前を`disable-telemetry`から`enable-telemetry`に変更します[＃684](https://github.com/pingcap-incubator/tidb-dashboard/pull/684)
    -   ページを切り替えるときにプログレスバーを表示する[＃661](https://github.com/pingcap-incubator/tidb-dashboard/pull/661)
    -   スペース区切り文字がある場合、低速ログ検索がログ検索と同じ動作に従うようになります[＃682](https://github.com/pingcap-incubator/tidb-dashboard/pull/682)

-   TiFlash

    -   Grafanaの**DDLジョブ**パネルの単位を`operations per minute`に変更します
    -   Grafanaに新しいダッシュボードを追加して、 **TiFlash-Proxy**に関するその他の指標を表示します
    -   TiFlashプロキシのIOPSを削減

-   ツール

    -   TiCDC

        -   メトリック[＃695](https://github.com/pingcap/tiflow/pull/695)でテーブルIDをテーブル名に置き換えます

    -   バックアップと復元（BR）

        -   JSONログの出力をサポート[＃336](https://github.com/pingcap/br/issues/336)
        -   実行時[＃372](https://github.com/pingcap/br/pull/372)でのpprofの有効化のサポート
        -   復元中にDDLを同時に送信することにより、DDLの実行を高速化します[＃377](https://github.com/pingcap/br/pull/377)

    -   TiDB Lightning

        -   `black-white-list`を廃止し、より新しくて理解しやすいフィルター形式[＃332](https://github.com/pingcap/tidb-lightning/pull/332)を使用する

## バグの修正 {#bug-fixes}

-   TiDB

    -   実行中にエラーが発生した場合、 `IndexHashJoin`の空のセットではなくエラーを返します[＃18586](https://github.com/pingcap/tidb/pull/18586)
    -   gRPCtransportReaderが壊れたときに繰り返し発生するpanicを修正[＃18562](https://github.com/pingcap/tidb/pull/18562)
    -   GreenGCがオフラインストアのロックをスキャンしない問題を修正します。これによりデータが不完全になる可能性があります[＃18550](https://github.com/pingcap/tidb/pull/18550)
    -   TiFlashエンジン[＃18534](https://github.com/pingcap/tidb/pull/18534)を使用した非読み取り専用ステートメントの処理を禁止する
    -   クエリ接続がパニックになったときに実際のエラーメッセージを返す[＃18500](https://github.com/pingcap/tidb/pull/18500)
    -   `ADMIN REPAIR TABLE`の実行でTiDBノード[＃18323](https://github.com/pingcap/tidb/pull/18323)のテーブルメタデータの再読み込みに失敗する問題を修正します。
    -   あるトランザクションで書き込まれ、削除された主キーのロックが別のトランザクションによって解決されるために発生したデータの不整合の問題を修正します[＃18291](https://github.com/pingcap/tidb/pull/18291)
    -   こぼれたディスクをうまく機能させる[＃18288](https://github.com/pingcap/tidb/pull/18288)
    -   生成された列[＃17907](https://github.com/pingcap/tidb/pull/17907)を含むテーブルで`REPLACE INTO`ステートメントが機能するときに報告されるエラーを修正します
    -   `IndexHashJoin`人と`IndexMergeJoin`人のワーカーがpanicになったときにOOMエラーを返します[＃18527](https://github.com/pingcap/tidb/pull/18527)
    -   `Index Join`で使用されるインデックスに整数の主キー[＃18565](https://github.com/pingcap/tidb/pull/18565)が含まれている場合に、 `Index Join`を実行すると、特殊なケースで誤った結果が返される可能性があるというバグを修正します。
    -   クラスタで新しい照合順序が有効になっている場合、トランザクション内の新しい照合順序で列で更新されたデータを一意のインデックス[＃18703](https://github.com/pingcap/tidb/pull/18703)から読み取ることができないという問題を修正します。

-   TiKV

    -   マージ中に読み取りで古いデータが取得される可能性がある問題を修正します[＃8113](https://github.com/tikv/tikv/pull/8113)
    -   集約がTiKV5にプッシュダウンされると、 `min` / `max`関数で照合順序が機能しない問題を修正し[＃8108](https://github.com/tikv/tikv/pull/8108) 。

-   PD

    -   サーバーがクラッシュした場合にTSOストリームの作成がしばらくブロックされる可能性がある問題を修正します[＃2648](https://github.com/pingcap/pd/pull/2648)
    -   `getSchedulers`がデータ競合[＃2638](https://github.com/pingcap/pd/pull/2638)を引き起こす可能性がある問題を修正します
    -   スケジューラーを削除するとデッドロックが発生する可能性がある問題を修正します[＃2637](https://github.com/pingcap/pd/pull/2637)
    -   `balance-leader-scheduler`が有効になっているときに配置ルールが考慮されないというバグを修正します[＃2636](https://github.com/pingcap/pd/pull/2636)
    -   サービス`safepoint`を正しく設定できないことがあり、BRと餃子が失敗する可能性がある問題を修正します[＃2635](https://github.com/pingcap/pd/pull/2635)
    -   `hot region scheduler`のターゲットストアが誤って選択される問題を修正します[＃2627](https://github.com/pingcap/pd/pull/2627)
    -   PDリーダーが切り替えられたときにTSO要求に時間がかかりすぎる可能性がある問題を修正します[＃2622](https://github.com/pingcap/pd/pull/2622)
    -   リーダー変更後の古いスケジューラーの問題を修正[＃2608](https://github.com/pingcap/pd/pull/2608)
    -   配置ルールが有効になっている場合、リージョンのレプリカを最適な場所に調整できないことがある問題を修正します[＃2605](https://github.com/pingcap/pd/pull/2605)
    -   デプロイメントディレクトリの変更に応じてストアのデプロイメントパスが更新されない問題を修正します[＃2600](https://github.com/pingcap/pd/pull/2600)
    -   `store limit`がゼロに変わるのを防ぐ[＃2588](https://github.com/pingcap/pd/pull/2588)

-   TiDBダッシュボード

    -   TiDBがスケールアウトされたときのTiDB接続エラーを修正[＃689](https://github.com/pingcap-incubator/tidb-dashboard/pull/689)
    -   TiFlashインスタンスがログ検索ページに表示されない問題を修正します[＃680](https://github.com/pingcap-incubator/tidb-dashboard/pull/680)
    -   概要ページ[＃663](https://github.com/pingcap-incubator/tidb-dashboard/pull/663)を更新した後のメトリック選択のリセットの問題を修正します
    -   一部のTLSシナリオでの接続の問題を修正する[＃660](https://github.com/pingcap-incubator/tidb-dashboard/pull/660)
    -   言語ドロップダウンボックスが正しく表示されない場合がある問題を修正します[＃677](https://github.com/pingcap-incubator/tidb-dashboard/pull/677)

-   TiFlash

    -   主キー列の名前を変更した後にTiFlashがクラッシュする問題を修正します
    -   同時`Learner Read`と`Remove Region`がデッドロックを引き起こす可能性がある問題を修正します

-   ツール

    -   TiCDC

        -   場合によってはTiCDCがメモリをリークする問題を修正します[＃704](https://github.com/pingcap/tiflow/pull/704)
        -   引用符で囲まれていないテーブル名がSQL構文エラー[＃676](https://github.com/pingcap/tiflow/pull/676)を引き起こす問題を修正します
        -   `p.stop`が[＃693](https://github.com/pingcap/tiflow/pull/693)と呼ばれた後、プロセッサが完全に終了しない問題を修正します。

    -   バックアップと復元（BR）

        -   バックアップ時間がマイナスになる可能性がある問題を修正します[＃405](https://github.com/pingcap/br/pull/405)

    -   Dumpling

        -   `--r`が指定されている場合にDumplingが`NULL`の値を省略してしまう問題を修正します[＃119](https://github.com/pingcap/dumpling/pull/119)
        -   テーブルがダンプするためにテーブルのフラッシュが機能しない可能性があるバグを修正します[＃117](https://github.com/pingcap/dumpling/pull/117)

    -   TiDB Lightning

        -   `--log-file`が有効にならない問題を修正します[＃345](https://github.com/pingcap/tidb-lightning/pull/345)

    -   TiDB Binlog

        -   TiDB BinlogがTLSを有効にしてデータをダウンストリームに複製すると、チェックポイント[＃988](https://github.com/pingcap/tidb-binlog/pull/988)の更新に使用されるデータベースドライバーでTLSが有効になっていないために発生するDrainerを開始できない問題を修正します。
