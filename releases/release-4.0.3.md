---
title: TiDB 4.0.3 Release Notes
---

# TiDB 4.0.3 リリースノート {#tidb-4-0-3-release-notes}

発売日：2020年7月24日

TiDB バージョン: 4.0.3

## 新機能 {#new-features}

-   TiDB ダッシュボード

    -   TiDB ダッシュボードの詳細なバージョン情報を表示する[#679](https://github.com/pingcap-incubator/tidb-dashboard/pull/679)
    -   サポートされていないブラウザまたは古いブラウザに関するブラウザ互換性に関する通知を表示する[#654](https://github.com/pingcap-incubator/tidb-dashboard/pull/654)
    -   **SQL ステートメント**での検索のサポート[#658](https://github.com/pingcap-incubator/tidb-dashboard/pull/658)ページ

-   TiFlash

    -   TiFlashプロキシにファイル暗号化を実装する

-   ツール

    -   バックアップと復元 (BR)

        -   zstd、lz4、または snappy [#404](https://github.com/pingcap/br/pull/404)を使用したバックアップ ファイルの圧縮をサポート

    -   TiCDC

        -   MQ シンク URI [#706](https://github.com/pingcap/tiflow/pull/706)で`kafka-client-id`の構成をサポート
        -   オフラインでの構成更新のサポート`changefeed` [#699](https://github.com/pingcap/tiflow/pull/699)
        -   サポート設定カスタマイズ`changefeed`名前[#727](https://github.com/pingcap/tiflow/pull/727)
        -   TLS および MySQL SSL 接続をサポート[#347](https://github.com/pingcap/tiflow/pull/347)
        -   Avro 形式[#753](https://github.com/pingcap/tiflow/pull/753)での変更の出力をサポート
        -   Apache Pulsar シンク[#751](https://github.com/pingcap/tiflow/pull/751)のサポート

    -   Dumpling

        -   特殊な CSV 区切り文字と区切り文字[#116](https://github.com/pingcap/dumpling/pull/116)をサポート
        -   出力ファイル名の形式指定をサポート[#122](https://github.com/pingcap/dumpling/pull/122)

## 改善点 {#improvements}

-   TiDB

    -   SQL クエリのログ記録時に感度を解除するかどうかを制御する`tidb_log_desensitization`グローバル変数を追加します[#18581](https://github.com/pingcap/tidb/pull/18581)
    -   デフォルトで`tidb_allow_batch_cop`を有効にします[#18552](https://github.com/pingcap/tidb/pull/18552)
    -   クエリのキャンセルを高速化する[#18505](https://github.com/pingcap/tidb/pull/18505)
    -   `tidb_decode_plan`結果[#18501](https://github.com/pingcap/tidb/pull/18501)にヘッダーを追加します
    -   構成チェッカーを以前のバージョンの構成ファイルと互換性のあるものにする[#18046](https://github.com/pingcap/tidb/pull/18046)
    -   デフォルトで実行情報の収集を有効にする[#18518](https://github.com/pingcap/tidb/pull/18518)
    -   `tiflash_tables`および`tiflash_segments`システム テーブルを追加します[#18536](https://github.com/pingcap/tidb/pull/18536)
    -   `AUTO RANDOM`実験的機能から外し、一般提供を発表します。改善点と互換性の変更は次のとおりです。
        -   構成ファイルの`experimental.allow-auto-random`非推奨にします。この項目がどのように構成されているかに関係なく、いつでも列に`AUTO RANDOM`機能を定義できます。 [#18613](https://github.com/pingcap/tidb/pull/18613) [#18623](https://github.com/pingcap/tidb/pull/18623)
        -   `tidb_allow_auto_random_explicit_insert`セッション変数を追加して、 `AUTO RANDOM`の列への明示的な書き込みを制御します。デフォルト値は`false`です。これは、列への明示的な書き込みによって引き起こされる予期しない`AUTO_RANDOM_BASE`更新を回避するためです。 [#18508](https://github.com/pingcap/tidb/pull/18508)
        -   `BIGINT`と`UNSIGNED BIGINT`列でのみ`AUTO_RANDOM`の定義を許可し、シャード ビットの最大数を`15`に制限します。これにより、割り当て可能なスペースが急速に消費されるのを回避できます[#18538](https://github.com/pingcap/tidb/pull/18538)
        -   列`BIGINT`に属性`AUTO_RANDOM`を定義し、主キー[#17987](https://github.com/pingcap/tidb/pull/17987)に負の値を挿入する場合、更新`AUTO_RANDOM_BASE`をトリガーしないでください。
        -   `UNSIGNED BIGINT`列に`AUTO_RANDOM`属性を定義する場合、ID 割り当てに整数の最上位ビットを使用します。これにより、より多くの割り当て可能な領域が得られます[#18404](https://github.com/pingcap/tidb/pull/18404)
        -   `SHOW CREATE TABLE` [#18316](https://github.com/pingcap/tidb/pull/18316)の結果の`AUTO_RANDOM`属性の更新をサポート

-   TiKV

    -   バックアップ スレッド プールのサイズを制御するための新しい`backup.num-threads`構成の導入[#8199](https://github.com/tikv/tikv/pull/8199)
    -   スナップショットの受信時にストア ハートビートを送信しない[#8136](https://github.com/tikv/tikv/pull/8136)
    -   共有ブロックキャッシュの容量の動的変更をサポート[#8232](https://github.com/tikv/tikv/pull/8232)

-   PD

    -   JSON形式のログをサポート[#2565](https://github.com/pingcap/pd/pull/2565)

-   TiDB ダッシュボード

    -   コールド論理範囲[#674](https://github.com/pingcap-incubator/tidb-dashboard/pull/674)の Key Visualizer バケット マージを改善します。
    -   整合性[#684](https://github.com/pingcap-incubator/tidb-dashboard/pull/684)のために`disable-telemetry`構成アイテムの名前を`enable-telemetry`に変更します。
    -   ページ切り替え時にプログレスバーを表示する[#661](https://github.com/pingcap-incubator/tidb-dashboard/pull/661)
    -   スペース区切り文字がある場合、低速ログ検索がログ検索と同じ動作になるようにしました[#682](https://github.com/pingcap-incubator/tidb-dashboard/pull/682)

-   TiFlash

    -   Grafana の**DDL ジョブ**パネルの単位を`operations per minute`に変更します。
    -   Grafana に新しいダッシュボードを追加して、 **TiFlash-Proxy**に関する詳細なメトリクスを表示します
    -   TiFlashプロキシの IOPS を削減する

-   ツール

    -   TiCDC

        -   メトリクス[#695](https://github.com/pingcap/tiflow/pull/695)のテーブル ID をテーブル名に置き換えます。

    -   バックアップと復元 (BR)

        -   JSONログの出力をサポート[#336](https://github.com/pingcap/br/issues/336)
        -   実行時における pprof の有効化のサポート[#372](https://github.com/pingcap/br/pull/372)
        -   リストア中に DDL を同時に送信することで DDL 実行を高速化します[#377](https://github.com/pingcap/br/pull/377)

    -   TiDB Lightning

        -   `black-white-list`を廃止し、より新しくわかりやすいフィルター形式に変更します[#332](https://github.com/pingcap/tidb-lightning/pull/332)

## バグの修正 {#bug-fixes}

-   TiDB

    -   実行中にエラーが発生した場合、 `IndexHashJoin`の場合は空のセットの代わりにエラーを返します[#18586](https://github.com/pingcap/tidb/pull/18586)
    -   gRPC TransportReader が壊れたときに繰り返されるpanicを修正します[#18562](https://github.com/pingcap/tidb/pull/18562)
    -   Green GC がオフライン ストアのロックをスキャンしないため、データが不完全になる可能性がある問題を修正します[#18550](https://github.com/pingcap/tidb/pull/18550)
    -   TiFlashエンジン[#18534](https://github.com/pingcap/tidb/pull/18534)を使用した非読み取り専用ステートメントの処理を禁止します
    -   クエリ接続がパニックになったときに実際のエラー メッセージを返す[#18500](https://github.com/pingcap/tidb/pull/18500)
    -   `ADMIN REPAIR TABLE`実行で TiDB ノード[#18323](https://github.com/pingcap/tidb/pull/18323)上のテーブル メタデータのリロードに失敗する問題を修正します。
    -   あるトランザクションで書き込まれ削除された主キーのロックが別のトランザクションによって解決されるために発生するデータの不整合の問題を修正します[#18291](https://github.com/pingcap/tidb/pull/18291)
    -   こぼれるディスクをうまく機能させる[#18288](https://github.com/pingcap/tidb/pull/18288)
    -   生成された列[#17907](https://github.com/pingcap/tidb/pull/17907)を含むテーブルで`REPLACE INTO`ステートメントが機能するときに報告されるエラーを修正します。
    -   `IndexHashJoin`と`IndexMergeJoin`ワーカーがpanic場合に OOM エラーを返す[#18527](https://github.com/pingcap/tidb/pull/18527)
    -   `Index Join`で使用されるインデックスに整数の主キー[#18565](https://github.com/pingcap/tidb/pull/18565)含まれている場合、特殊な場合に`Index Join`を実行すると誤った結果が返される可能性があるバグを修正
    -   クラスターで新しい照合順序が有効になっている場合、トランザクション内の新しい照合順序を持つ列で更新されたデータが一意のインデックス[#18703](https://github.com/pingcap/tidb/pull/18703)を介して読み取れないという問題を修正します。

-   TiKV

    -   マージ中に読み取りで古いデータが取得される可能性がある問題を修正[#8113](https://github.com/tikv/tikv/pull/8113)
    -   照合順序がTiKV [#8108](https://github.com/tikv/tikv/pull/8108)にプッシュダウンされると、 `min` / `max`関数で照合が機能しない問題を修正

-   PD

    -   サーバーがクラッシュした場合、TSO ストリームの作成がしばらくブロックされる可能性がある問題を修正します[#2648](https://github.com/pingcap/pd/pull/2648)
    -   `getSchedulers`データ競合が発生する可能性がある問題を修正[#2638](https://github.com/pingcap/pd/pull/2638)
    -   スケジューラを削除するとデッドロックが発生する可能性がある問題を修正[#2637](https://github.com/pingcap/pd/pull/2637)
    -   `balance-leader-scheduler`を有効にした場合に配置ルールが考慮されないバグを修正[#2636](https://github.com/pingcap/pd/pull/2636)
    -   サービス`safepoint`が正しく設定できない場合があり、 BRと団子[#2635](https://github.com/pingcap/pd/pull/2635)が失敗する可能性がある問題を修正
    -   `hot region scheduler`の対象ストアが誤って選択される問題を修正[#2627](https://github.com/pingcap/pd/pull/2627)
    -   PDリーダーの切り替え時にTSOリクエストに時間がかかりすぎる問題を修正[#2622](https://github.com/pingcap/pd/pull/2622)
    -   リーダー変更後のスケジューラが古くなる問題を修正[#2608](https://github.com/pingcap/pd/pull/2608)
    -   配置ルールが有効になっている場合、リージョンのレプリカを最適な場所に調整できない場合がある問題を修正します[#2605](https://github.com/pingcap/pd/pull/2605)
    -   デプロイディレクトリ[#2600](https://github.com/pingcap/pd/pull/2600)の変更に応じてストアのデプロイパスが更新されない問題を修正
    -   `store limit`が 0 にならないようにする[#2588](https://github.com/pingcap/pd/pull/2588)

-   TiDB ダッシュボード

    -   TiDB がスケールアウトされている場合の TiDB 接続エラーを修正[#689](https://github.com/pingcap-incubator/tidb-dashboard/pull/689)
    -   ログ検索ページ[#680](https://github.com/pingcap-incubator/tidb-dashboard/pull/680)でTiFlashインスタンスが表示されない問題を修正
    -   概要ページ[#663](https://github.com/pingcap-incubator/tidb-dashboard/pull/663)を更新した後にメトリック選択がリセットされる問題を修正
    -   一部の TLS シナリオでの接続の問題を修正します[#660](https://github.com/pingcap-incubator/tidb-dashboard/pull/660)
    -   言語ドロップダウンボックスが正しく表示されない場合がある問題を修正[#677](https://github.com/pingcap-incubator/tidb-dashboard/pull/677)

-   TiFlash

    -   主キー列の名前を変更した後にTiFlash がクラッシュする問題を修正
    -   `Learner Read`と`Remove Region`を同時に実行するとデッドロックが発生する可能性がある問題を修正

-   ツール

    -   TiCDC

        -   TiCDC が場合によってメモリリークを起こす問題を修正[#704](https://github.com/pingcap/tiflow/pull/704)
        -   引用符で囲まれていないテーブル名により SQL 構文エラー[#676](https://github.com/pingcap/tiflow/pull/676)が発生する問題を修正します。
        -   `p.stop`が[#693](https://github.com/pingcap/tiflow/pull/693)を呼び出された後、プロセッサが完全に終了しない問題を修正

    -   バックアップと復元 (BR)

        -   バックアップ時間がマイナス[#405](https://github.com/pingcap/br/pull/405)になる場合がある問題を修正

    -   Dumpling

        -   Dumpling で`--r`を指定した場合に`NULL`値が省略される問題を修正[#119](https://github.com/pingcap/dumpling/pull/119)
        -   ダンプするテーブルに対してテーブルのフラッシュが機能しないことがあるバグを修正[#117](https://github.com/pingcap/dumpling/pull/117)

    -   TiDB Lightning

        -   `--log-file`が反映されない問題を修正[#345](https://github.com/pingcap/tidb-lightning/pull/345)

    -   TiDBBinlog

        -   TiDB Binlog がTLS を有効にしてダウンストリームにデータをレプリケートするときに、チェックポイント[#988](https://github.com/pingcap/tidb-binlog/pull/988)の更新に使用されるデータベース ドライバーで TLS が有効になっていないために発生するDrainerを開始できない問題を修正します。
