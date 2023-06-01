---
title: TiDB 4.0.3 Release Notes
---

# TiDB 4.0.3 リリースノート {#tidb-4-0-3-release-notes}

発売日：2020年7月24日

TiDB バージョン: 4.0.3

## 新機能 {#new-features}

-   TiDB ダッシュボード

    -   TiDB ダッシュボードの詳細なバージョン情報を表示する[<a href="https://github.com/pingcap-incubator/tidb-dashboard/pull/679">#679</a>](https://github.com/pingcap-incubator/tidb-dashboard/pull/679)
    -   サポートされていないブラウザまたは古いブラウザに関するブラウザ互換性に関する通知を表示する[<a href="https://github.com/pingcap-incubator/tidb-dashboard/pull/654">#654</a>](https://github.com/pingcap-incubator/tidb-dashboard/pull/654)
    -   **SQL ステートメント**での検索のサポート[<a href="https://github.com/pingcap-incubator/tidb-dashboard/pull/658">#658</a>](https://github.com/pingcap-incubator/tidb-dashboard/pull/658)ページ

-   TiFlash

    -   TiFlashプロキシにファイル暗号化を実装する

-   ツール

    -   バックアップと復元 (BR)

        -   zstd、lz4、または snappy [<a href="https://github.com/pingcap/br/pull/404">#404</a>](https://github.com/pingcap/br/pull/404)を使用したバックアップ ファイルの圧縮をサポート

    -   TiCDC

        -   MQ シンク URI [<a href="https://github.com/pingcap/tiflow/pull/706">#706</a>](https://github.com/pingcap/tiflow/pull/706)で`kafka-client-id`の構成をサポート
        -   オフラインでの構成更新のサポート`changefeed` [<a href="https://github.com/pingcap/tiflow/pull/699">#699</a>](https://github.com/pingcap/tiflow/pull/699)
        -   サポート設定カスタマイズ`changefeed`名前[<a href="https://github.com/pingcap/tiflow/pull/727">#727</a>](https://github.com/pingcap/tiflow/pull/727)
        -   TLS および MySQL SSL 接続をサポート[<a href="https://github.com/pingcap/tiflow/pull/347">#347</a>](https://github.com/pingcap/tiflow/pull/347)
        -   Avro 形式[<a href="https://github.com/pingcap/tiflow/pull/753">#753</a>](https://github.com/pingcap/tiflow/pull/753)での変更の出力をサポート
        -   Apache Pulsar シンク[<a href="https://github.com/pingcap/tiflow/pull/751">#751</a>](https://github.com/pingcap/tiflow/pull/751)のサポート

    -   Dumpling

        -   特殊な CSV 区切り文字と区切り文字[<a href="https://github.com/pingcap/dumpling/pull/116">#116</a>](https://github.com/pingcap/dumpling/pull/116)をサポート
        -   出力ファイル名の形式指定をサポート[<a href="https://github.com/pingcap/dumpling/pull/122">#122</a>](https://github.com/pingcap/dumpling/pull/122)

## 改善点 {#improvements}

-   TiDB

    -   SQL クエリのログ記録時に感度を解除するかどうかを制御する`tidb_log_desensitization`グローバル変数を追加します[<a href="https://github.com/pingcap/tidb/pull/18581">#18581</a>](https://github.com/pingcap/tidb/pull/18581)
    -   デフォルトで`tidb_allow_batch_cop`を有効にします[<a href="https://github.com/pingcap/tidb/pull/18552">#18552</a>](https://github.com/pingcap/tidb/pull/18552)
    -   クエリのキャンセルを高速化する[<a href="https://github.com/pingcap/tidb/pull/18505">#18505</a>](https://github.com/pingcap/tidb/pull/18505)
    -   `tidb_decode_plan`結果[<a href="https://github.com/pingcap/tidb/pull/18501">#18501</a>](https://github.com/pingcap/tidb/pull/18501)にヘッダーを追加します
    -   構成チェッカーを以前のバージョンの構成ファイルと互換性のあるものにする[<a href="https://github.com/pingcap/tidb/pull/18046">#18046</a>](https://github.com/pingcap/tidb/pull/18046)
    -   デフォルトで実行情報の収集を有効にする[<a href="https://github.com/pingcap/tidb/pull/18518">#18518</a>](https://github.com/pingcap/tidb/pull/18518)
    -   `tiflash_tables`および`tiflash_segments`システム テーブルを追加します[<a href="https://github.com/pingcap/tidb/pull/18536">#18536</a>](https://github.com/pingcap/tidb/pull/18536)
    -   `AUTO RANDOM`実験的機能から外し、一般提供を発表します。改善点と互換性の変更は次のとおりです。
        -   構成ファイル内の`experimental.allow-auto-random`非推奨にします。この項目がどのように構成されているかに関係なく、いつでも列に`AUTO RANDOM`機能を定義できます。 [<a href="https://github.com/pingcap/tidb/pull/18613">#18613</a>](https://github.com/pingcap/tidb/pull/18613) [<a href="https://github.com/pingcap/tidb/pull/18623">#18623</a>](https://github.com/pingcap/tidb/pull/18623)
        -   `tidb_allow_auto_random_explicit_insert`セッション変数を追加して、 `AUTO RANDOM`の列への明示的な書き込みを制御します。デフォルト値は`false`です。これは、列への明示的な書き込みによって引き起こされる予期しない`AUTO_RANDOM_BASE`更新を回避するためです。 [<a href="https://github.com/pingcap/tidb/pull/18508">#18508</a>](https://github.com/pingcap/tidb/pull/18508)
        -   `BIGINT`と`UNSIGNED BIGINT`列でのみ`AUTO_RANDOM`の定義を許可し、シャード ビットの最大数を`15`に制限します。これにより、割り当て可能なスペースが急速に消費されるのを回避できます[<a href="https://github.com/pingcap/tidb/pull/18538">#18538</a>](https://github.com/pingcap/tidb/pull/18538)
        -   列`BIGINT`に属性`AUTO_RANDOM`を定義し、主キー[<a href="https://github.com/pingcap/tidb/pull/17987">#17987</a>](https://github.com/pingcap/tidb/pull/17987)に負の値を挿入する場合、更新`AUTO_RANDOM_BASE`をトリガーしないでください。
        -   `UNSIGNED BIGINT`列に`AUTO_RANDOM`属性を定義する場合、ID 割り当てに整数の最上位ビットを使用します。これにより、より多くの割り当て可能な領域が得られます[<a href="https://github.com/pingcap/tidb/pull/18404">#18404</a>](https://github.com/pingcap/tidb/pull/18404)
        -   `SHOW CREATE TABLE` [<a href="https://github.com/pingcap/tidb/pull/18316">#18316</a>](https://github.com/pingcap/tidb/pull/18316)の結果の`AUTO_RANDOM`属性の更新をサポート

-   TiKV

    -   バックアップ スレッド プールのサイズを制御するための新しい`backup.num-threads`構成の導入[<a href="https://github.com/tikv/tikv/pull/8199">#8199</a>](https://github.com/tikv/tikv/pull/8199)
    -   スナップショットの受信時にストア ハートビートを送信しない[<a href="https://github.com/tikv/tikv/pull/8136">#8136</a>](https://github.com/tikv/tikv/pull/8136)
    -   共有ブロックキャッシュの容量の動的変更をサポート[<a href="https://github.com/tikv/tikv/pull/8232">#8232</a>](https://github.com/tikv/tikv/pull/8232)

-   PD

    -   JSON形式のログをサポート[<a href="https://github.com/pingcap/pd/pull/2565">#2565</a>](https://github.com/pingcap/pd/pull/2565)

-   TiDB ダッシュボード

    -   コールド論理範囲[<a href="https://github.com/pingcap-incubator/tidb-dashboard/pull/674">#674</a>](https://github.com/pingcap-incubator/tidb-dashboard/pull/674)の Key Visualizer バケット マージを改善します。
    -   整合性[<a href="https://github.com/pingcap-incubator/tidb-dashboard/pull/684">#684</a>](https://github.com/pingcap-incubator/tidb-dashboard/pull/684)のために`disable-telemetry`構成アイテムの名前を`enable-telemetry`に変更します。
    -   ページ切り替え時にプログレスバーを表示する[<a href="https://github.com/pingcap-incubator/tidb-dashboard/pull/661">#661</a>](https://github.com/pingcap-incubator/tidb-dashboard/pull/661)
    -   スペース区切り文字がある場合、低速ログ検索がログ検索と同じ動作になるようにしました[<a href="https://github.com/pingcap-incubator/tidb-dashboard/pull/682">#682</a>](https://github.com/pingcap-incubator/tidb-dashboard/pull/682)

-   TiFlash

    -   Grafana の**DDL ジョブ**パネルの単位を`operations per minute`に変更します。
    -   Grafana に新しいダッシュボードを追加して、 **TiFlash-Proxy**に関する詳細なメトリクスを表示します
    -   TiFlashプロキシの IOPS を削減する

-   ツール

    -   TiCDC

        -   メトリクス[<a href="https://github.com/pingcap/tiflow/pull/695">#695</a>](https://github.com/pingcap/tiflow/pull/695)のテーブル ID をテーブル名に置き換えます。

    -   バックアップと復元 (BR)

        -   JSONログの出力をサポート[<a href="https://github.com/pingcap/br/issues/336">#336</a>](https://github.com/pingcap/br/issues/336)
        -   実行時における pprof の有効化のサポート[<a href="https://github.com/pingcap/br/pull/372">#372</a>](https://github.com/pingcap/br/pull/372)
        -   リストア中に DDL を同時に送信することで DDL 実行を高速化します[<a href="https://github.com/pingcap/br/pull/377">#377</a>](https://github.com/pingcap/br/pull/377)

    -   TiDB Lightning

        -   `black-white-list`を廃止し、より新しくわかりやすいフィルター形式に変更します[<a href="https://github.com/pingcap/tidb-lightning/pull/332">#332</a>](https://github.com/pingcap/tidb-lightning/pull/332)

## バグの修正 {#bug-fixes}

-   TiDB

    -   実行中にエラーが発生した場合、 `IndexHashJoin`の場合は空のセットの代わりにエラーを返します[<a href="https://github.com/pingcap/tidb/pull/18586">#18586</a>](https://github.com/pingcap/tidb/pull/18586)
    -   gRPC TransportReader が壊れたときに繰り返されるpanicを修正します[<a href="https://github.com/pingcap/tidb/pull/18562">#18562</a>](https://github.com/pingcap/tidb/pull/18562)
    -   Green GC がオフライン ストアのロックをスキャンしないため、データが不完全になる可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/pull/18550">#18550</a>](https://github.com/pingcap/tidb/pull/18550)
    -   TiFlashエンジン[<a href="https://github.com/pingcap/tidb/pull/18534">#18534</a>](https://github.com/pingcap/tidb/pull/18534)を使用した非読み取り専用ステートメントの処理を禁止します
    -   クエリ接続がパニックになったときに実際のエラー メッセージを返す[<a href="https://github.com/pingcap/tidb/pull/18500">#18500</a>](https://github.com/pingcap/tidb/pull/18500)
    -   `ADMIN REPAIR TABLE`実行で TiDB ノード[<a href="https://github.com/pingcap/tidb/pull/18323">#18323</a>](https://github.com/pingcap/tidb/pull/18323)上のテーブル メタデータのリロードに失敗する問題を修正します。
    -   あるトランザクションで書き込まれ削除された主キーのロックが別のトランザクションによって解決されるために発生するデータの不整合の問題を修正します[<a href="https://github.com/pingcap/tidb/pull/18291">#18291</a>](https://github.com/pingcap/tidb/pull/18291)
    -   こぼれるディスクをうまく機能させる[<a href="https://github.com/pingcap/tidb/pull/18288">#18288</a>](https://github.com/pingcap/tidb/pull/18288)
    -   生成された列[<a href="https://github.com/pingcap/tidb/pull/17907">#17907</a>](https://github.com/pingcap/tidb/pull/17907)を含むテーブルで`REPLACE INTO`ステートメントが機能するときに報告されるエラーを修正します。
    -   `IndexHashJoin`と`IndexMergeJoin`ワーカーがpanic場合に OOM エラーを返す[<a href="https://github.com/pingcap/tidb/pull/18527">#18527</a>](https://github.com/pingcap/tidb/pull/18527)
    -   `Index Join`で使用されるインデックスに整数の主キー[<a href="https://github.com/pingcap/tidb/pull/18565">#18565</a>](https://github.com/pingcap/tidb/pull/18565)含まれている場合、特殊な場合に`Index Join`を実行すると誤った結果が返される可能性があるバグを修正
    -   クラスターで新しい照合順序が有効になっている場合、トランザクション内の新しい照合順序を持つ列で更新されたデータが一意のインデックス[<a href="https://github.com/pingcap/tidb/pull/18703">#18703</a>](https://github.com/pingcap/tidb/pull/18703)を介して読み取れないという問題を修正します。

-   TiKV

    -   マージ中に読み取りで古いデータが取得される可能性がある問題を修正[<a href="https://github.com/tikv/tikv/pull/8113">#8113</a>](https://github.com/tikv/tikv/pull/8113)
    -   照合順序がTiKV [<a href="https://github.com/tikv/tikv/pull/8108">#8108</a>](https://github.com/tikv/tikv/pull/8108)にプッシュダウンされると、 `min` / `max`関数で照合が機能しない問題を修正

-   PD

    -   サーバーがクラッシュした場合、TSO ストリームの作成がしばらくブロックされる可能性がある問題を修正します[<a href="https://github.com/pingcap/pd/pull/2648">#2648</a>](https://github.com/pingcap/pd/pull/2648)
    -   `getSchedulers`データ競合が発生する可能性がある問題を修正[<a href="https://github.com/pingcap/pd/pull/2638">#2638</a>](https://github.com/pingcap/pd/pull/2638)
    -   スケジューラを削除するとデッドロックが発生する可能性がある問題を修正[<a href="https://github.com/pingcap/pd/pull/2637">#2637</a>](https://github.com/pingcap/pd/pull/2637)
    -   `balance-leader-scheduler`を有効にした場合に配置ルールが考慮されないバグを修正[<a href="https://github.com/pingcap/pd/pull/2636">#2636</a>](https://github.com/pingcap/pd/pull/2636)
    -   サービス`safepoint`が正しく設定できない場合があり、 BRと団子[<a href="https://github.com/pingcap/pd/pull/2635">#2635</a>](https://github.com/pingcap/pd/pull/2635)が失敗する可能性がある問題を修正
    -   `hot region scheduler`の対象ストアが誤って選択される問題を修正[<a href="https://github.com/pingcap/pd/pull/2627">#2627</a>](https://github.com/pingcap/pd/pull/2627)
    -   PDリーダーの切り替え時にTSOリクエストに時間がかかりすぎる問題を修正[<a href="https://github.com/pingcap/pd/pull/2622">#2622</a>](https://github.com/pingcap/pd/pull/2622)
    -   リーダー変更後のスケジューラが古くなる問題を修正[<a href="https://github.com/pingcap/pd/pull/2608">#2608</a>](https://github.com/pingcap/pd/pull/2608)
    -   配置ルールが有効になっている場合、リージョンのレプリカを最適な場所に調整できない場合がある問題を修正します[<a href="https://github.com/pingcap/pd/pull/2605">#2605</a>](https://github.com/pingcap/pd/pull/2605)
    -   デプロイディレクトリ[<a href="https://github.com/pingcap/pd/pull/2600">#2600</a>](https://github.com/pingcap/pd/pull/2600)の変更に応じてストアのデプロイパスが更新されない問題を修正
    -   `store limit`が 0 にならないようにする[<a href="https://github.com/pingcap/pd/pull/2588">#2588</a>](https://github.com/pingcap/pd/pull/2588)

-   TiDB ダッシュボード

    -   TiDB がスケールアウトされている場合の TiDB 接続エラーを修正[<a href="https://github.com/pingcap-incubator/tidb-dashboard/pull/689">#689</a>](https://github.com/pingcap-incubator/tidb-dashboard/pull/689)
    -   ログ検索ページ[<a href="https://github.com/pingcap-incubator/tidb-dashboard/pull/680">#680</a>](https://github.com/pingcap-incubator/tidb-dashboard/pull/680)でTiFlashインスタンスが表示されない問題を修正
    -   概要ページ[<a href="https://github.com/pingcap-incubator/tidb-dashboard/pull/663">#663</a>](https://github.com/pingcap-incubator/tidb-dashboard/pull/663)を更新した後にメトリック選択がリセットされる問題を修正
    -   一部の TLS シナリオでの接続の問題を修正します[<a href="https://github.com/pingcap-incubator/tidb-dashboard/pull/660">#660</a>](https://github.com/pingcap-incubator/tidb-dashboard/pull/660)
    -   言語ドロップダウンボックスが正しく表示されない場合がある問題を修正[<a href="https://github.com/pingcap-incubator/tidb-dashboard/pull/677">#677</a>](https://github.com/pingcap-incubator/tidb-dashboard/pull/677)

-   TiFlash

    -   主キー列の名前を変更した後にTiFlash がクラッシュする問題を修正
    -   `Learner Read`と`Remove Region`を同時に実行するとデッドロックが発生する可能性がある問題を修正

-   ツール

    -   TiCDC

        -   TiCDC が場合によってメモリリークを起こす問題を修正[<a href="https://github.com/pingcap/tiflow/pull/704">#704</a>](https://github.com/pingcap/tiflow/pull/704)
        -   引用符で囲まれていないテーブル名により SQL 構文エラー[<a href="https://github.com/pingcap/tiflow/pull/676">#676</a>](https://github.com/pingcap/tiflow/pull/676)が発生する問題を修正します。
        -   `p.stop`が[<a href="https://github.com/pingcap/tiflow/pull/693">#693</a>](https://github.com/pingcap/tiflow/pull/693)を呼び出された後、プロセッサが完全に終了しない問題を修正

    -   バックアップと復元 (BR)

        -   バックアップ時間がマイナス[<a href="https://github.com/pingcap/br/pull/405">#405</a>](https://github.com/pingcap/br/pull/405)になる場合がある問題を修正

    -   Dumpling

        -   Dumpling で`--r`を指定した場合に`NULL`値が省略される問題を修正[<a href="https://github.com/pingcap/dumpling/pull/119">#119</a>](https://github.com/pingcap/dumpling/pull/119)
        -   ダンプするテーブルに対してテーブルのフラッシュが機能しないことがあるバグを修正[<a href="https://github.com/pingcap/dumpling/pull/117">#117</a>](https://github.com/pingcap/dumpling/pull/117)

    -   TiDB Lightning

        -   `--log-file`が反映されない問題を修正[<a href="https://github.com/pingcap/tidb-lightning/pull/345">#345</a>](https://github.com/pingcap/tidb-lightning/pull/345)

    -   TiDBBinlog

        -   TiDB Binlog がTLS を有効にしてダウンストリームにデータをレプリケートするときに、チェックポイント[<a href="https://github.com/pingcap/tidb-binlog/pull/988">#988</a>](https://github.com/pingcap/tidb-binlog/pull/988)の更新に使用されるデータベース ドライバーで TLS が有効になっていないために発生するDrainerを開始できない問題を修正します。
