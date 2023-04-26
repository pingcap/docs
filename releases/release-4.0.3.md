---
title: TiDB 4.0.3 Release Notes
---

# TiDB 4.0.3 リリースノート {#tidb-4-0-3-release-notes}

発売日：2020年7月24日

TiDB バージョン: 4.0.3

## 新機能 {#new-features}

-   TiDB ダッシュボード

    -   詳細な TiDB ダッシュボードのバージョン情報を表示する[#679](https://github.com/pingcap-incubator/tidb-dashboard/pull/679)
    -   サポートされていないブラウザーまたは古いブラウザーのブラウザー互換性通知を表示する[#654](https://github.com/pingcap-incubator/tidb-dashboard/pull/654)
    -   **SQL ステートメント**ページ[#658](https://github.com/pingcap-incubator/tidb-dashboard/pull/658)での検索のサポート

-   TiFlash

    -   TiFlashプロキシにファイル暗号化を実装する

-   ツール

    -   バックアップと復元 (BR)

        -   zstd、lz4、または snappy [#404](https://github.com/pingcap/br/pull/404)を使用したバックアップ ファイルの圧縮をサポート

    -   TiCDC

        -   MQ sync-uri [#706](https://github.com/pingcap/tiflow/pull/706)で`kafka-client-id`の構成をサポート
        -   `changefeed`構成のオフライン更新をサポート[#699](https://github.com/pingcap/tiflow/pull/699)
        -   サポート設定のカスタマイズ`changefeed`名前[#727](https://github.com/pingcap/tiflow/pull/727)
        -   TLS および MySQL SSL 接続をサポート[#347](https://github.com/pingcap/tiflow/pull/347)
        -   Avro フォーマット[#753](https://github.com/pingcap/tiflow/pull/753)での変更の出力をサポート
        -   Apache Pulsar シンク[#751](https://github.com/pingcap/tiflow/pull/751)のサポート

    -   Dumpling

        -   専用の CSV 区切り記号と区切り記号[#116](https://github.com/pingcap/dumpling/pull/116)をサポートします
        -   出力ファイル名のフォーマット指定に対応[#122](https://github.com/pingcap/dumpling/pull/122)

## 改良点 {#improvements}

-   TiDB

    -   `tidb_log_desensitization`グローバル変数を追加して、SQL クエリのログ記録時に感度低下を行うかどうかを制御します[#18581](https://github.com/pingcap/tidb/pull/18581)
    -   デフォルトで`tidb_allow_batch_cop`を有効にする[#18552](https://github.com/pingcap/tidb/pull/18552)
    -   クエリのキャンセルを高速化する[#18505](https://github.com/pingcap/tidb/pull/18505)
    -   `tidb_decode_plan`結果[#18501](https://github.com/pingcap/tidb/pull/18501)のヘッダーを追加します
    -   構成チェッカーを以前のバージョンの構成ファイルと互換性を持たせる[#18046](https://github.com/pingcap/tidb/pull/18046)
    -   デフォルトで実行情報の収集を有効にする[#18518](https://github.com/pingcap/tidb/pull/18518)
    -   `tiflash_tables`と`tiflash_segments`システム テーブルを追加します[#18536](https://github.com/pingcap/tidb/pull/18536)
    -   実験的機能から`AUTO RANDOM`移動し、一般提供を発表します。改善点と互換性の変更は次のとおりです。
        -   構成ファイルで`experimental.allow-auto-random`非推奨にします。この項目がどのように構成されていても、列の`AUTO RANDOM`機能をいつでも定義できます。 [#18613](https://github.com/pingcap/tidb/pull/18613) [#18623](https://github.com/pingcap/tidb/pull/18623)
        -   `tidb_allow_auto_random_explicit_insert`セッション変数を追加して、 `AUTO RANDOM`列への明示的な書き込みを制御します。デフォルト値は`false`です。これは、列への明示的な書き込みによって引き起こされる予期しない`AUTO_RANDOM_BASE`更新を回避するためです。 [#18508](https://github.com/pingcap/tidb/pull/18508)
        -   `BIGINT`と`UNSIGNED BIGINT`列でのみ`AUTO_RANDOM`を定義できるようにし、シャード ビットの最大数を`15`に制限します。これにより、割り当て可能な領域が急速に消費されるのを回避します[#18538](https://github.com/pingcap/tidb/pull/18538)
        -   `BIGINT`列に`AUTO_RANDOM`属性を定義し、主キー[#17987](https://github.com/pingcap/tidb/pull/17987)に負の値を挿入するときに`AUTO_RANDOM_BASE`更新をトリガーしない
        -   `UNSIGNED BIGINT`列に`AUTO_RANDOM`属性を定義する場合は、ID の割り当てに整数の最上位ビットを使用します。これにより、より多くの割り当て可能なスペースが得られます[#18404](https://github.com/pingcap/tidb/pull/18404)
        -   `SHOW CREATE TABLE` [#18316](https://github.com/pingcap/tidb/pull/18316)の結果の`AUTO_RANDOM`属性の更新をサポート

-   TiKV

    -   新しい`backup.num-threads`構成を導入して、バックアップ スレッド プールのサイズを制御します[#8199](https://github.com/tikv/tikv/pull/8199)
    -   スナップショットの受信時にストア ハートビートを送信しない[#8136](https://github.com/tikv/tikv/pull/8136)
    -   共有ブロック キャッシュの容量を動的に変更するサポート[#8232](https://github.com/tikv/tikv/pull/8232)

-   PD

    -   JSON 形式のログをサポート[#2565](https://github.com/pingcap/pd/pull/2565)

-   TiDB ダッシュボード

    -   コールド論理範囲[#674](https://github.com/pingcap-incubator/tidb-dashboard/pull/674)のキー ビジュアライザー バケット マージを改善する
    -   一貫性のために`disable-telemetry`から`enable-telemetry`構成アイテムの名前を変更します[#684](https://github.com/pingcap-incubator/tidb-dashboard/pull/684)
    -   ページ切り替え時にプログレスバーを表示する[#661](https://github.com/pingcap-incubator/tidb-dashboard/pull/661)
    -   スペース区切り文字がある場合、低速ログ検索がログ検索と同じ動作に従うようになりました[#682](https://github.com/pingcap-incubator/tidb-dashboard/pull/682)

-   TiFlash

    -   Grafana の**DDL ジョブ**パネルの単位を`operations per minute`に変更します。
    -   Grafana に新しいダッシュボードを追加して、 **TiFlash-Proxy**に関するより多くのメトリックを表示します
    -   TiFlashプロキシで IOPS を減らす

-   ツール

    -   TiCDC

        -   メトリクス[#695](https://github.com/pingcap/tiflow/pull/695)のテーブル ID をテーブル名に置き換えます

    -   バックアップと復元 (BR)

        -   JSON ログ出力のサポート[#336](https://github.com/pingcap/br/issues/336)
        -   実行時の pprof の有効化をサポート[#372](https://github.com/pingcap/br/pull/372)
        -   リストア中に DDL を同時に送信することにより、DDL の実行を高速化します[#377](https://github.com/pingcap/br/pull/377)

    -   TiDB Lightning

        -   より新しく、より理解しやすいフィルター形式で`black-white-list`非推奨にする[#332](https://github.com/pingcap/tidb-lightning/pull/332)

## バグの修正 {#bug-fixes}

-   TiDB

    -   実行中にエラーが発生した場合、 `IndexHashJoin`空のセットの代わりにエラーを返す[#18586](https://github.com/pingcap/tidb/pull/18586)
    -   gRPC transportReader が壊れているときに繰り返されるpanicを修正します[#18562](https://github.com/pingcap/tidb/pull/18562)
    -   Green GC がオフライン ストアのロックをスキャンしないため、データが不完全になる可能性がある問題を修正します[#18550](https://github.com/pingcap/tidb/pull/18550)
    -   TiFlashエンジン[#18534](https://github.com/pingcap/tidb/pull/18534)を使用した非読み取り専用ステートメントの処理を禁止する
    -   クエリ接続がパニックになったときに実際のエラー メッセージを返す[#18500](https://github.com/pingcap/tidb/pull/18500)
    -   `ADMIN REPAIR TABLE`実行で TiDB ノード[#18323](https://github.com/pingcap/tidb/pull/18323)のテーブル メタデータのリロードに失敗する問題を修正します。
    -   [#18291](https://github.com/pingcap/tidb/pull/18291)つのトランザクションで書き込まれ、削除された主キーのロックが別のトランザクションによって解決されるために発生したデータの不整合の問題を修正します。
    -   こぼれるディスクをうまく機能させる[#18288](https://github.com/pingcap/tidb/pull/18288)
    -   生成された列[#17907](https://github.com/pingcap/tidb/pull/17907)を含むテーブルで`REPLACE INTO`ステートメントが機能するときに報告されるエラーを修正します。
    -   `IndexHashJoin`と`IndexMergeJoin`ワーカーがpanicたときに OOM エラーを返す[#18527](https://github.com/pingcap/tidb/pull/18527)
    -   `Index Join`で使用されるインデックスに整数の主キー[#18565](https://github.com/pingcap/tidb/pull/18565)含まれている場合、特殊なケースで`Index Join`の実行が間違った結果を返す可能性があるというバグを修正します
    -   クラスターで新しい照合順序が有効になっている場合、トランザクションで新しい照合順序を使用して列で更新されたデータを一意のインデックス[#18703](https://github.com/pingcap/tidb/pull/18703)から読み取ることができないという問題を修正します。

-   TiKV

    -   マージ中に読み取りが古いデータを取得する可能性がある問題を修正します[#8113](https://github.com/tikv/tikv/pull/8113)
    -   TiKV [#8108](https://github.com/tikv/tikv/pull/8108)にアグリゲーションをプッシュダウンすると、 `min` / `max`関数で照合順序が機能しない問題を修正

-   PD

    -   サーバーがクラッシュした場合、TSO ストリームの作成がしばらくブロックされる可能性がある問題を修正します[#2648](https://github.com/pingcap/pd/pull/2648)
    -   `getSchedulers`データ競合が発生する可能性がある問題を修正[#2638](https://github.com/pingcap/pd/pull/2638)
    -   スケジューラを削除するとデッドロックが発生する可能性がある問題を修正します[#2637](https://github.com/pingcap/pd/pull/2637)
    -   `balance-leader-scheduler`が有効の場合、配置ルールが考慮されないバグを修正[#2636](https://github.com/pingcap/pd/pull/2636)
    -   サービス`safepoint`が正しく設定されず、 BRと餃子が失敗する場合がある問題を修正します[#2635](https://github.com/pingcap/pd/pull/2635)
    -   `hot region scheduler`の対象店舗が間違って選択されていた問題を修正[#2627](https://github.com/pingcap/pd/pull/2627)
    -   PD リーダーが切り替えられたときに TSO 要求に時間がかかりすぎることがある問題を修正します[#2622](https://github.com/pingcap/pd/pull/2622)
    -   リーダーの変更後の古いスケジューラの問題を修正します[#2608](https://github.com/pingcap/pd/pull/2608)
    -   配置ルールが有効になっている場合、リージョンのレプリカを最適な場所に調整できないことがあるという問題を修正します[#2605](https://github.com/pingcap/pd/pull/2605)
    -   配置ディレクトリの変更に伴い、ストアの配置パスが更新されない問題を修正[#2600](https://github.com/pingcap/pd/pull/2600)
    -   `store limit`が 0 に変わるのを防ぐ[#2588](https://github.com/pingcap/pd/pull/2588)

-   TiDB ダッシュボード

    -   TiDB がスケールアウトされたときの TiDB 接続エラーを修正します[#689](https://github.com/pingcap-incubator/tidb-dashboard/pull/689)
    -   ログ検索ページ[#680](https://github.com/pingcap-incubator/tidb-dashboard/pull/680)でTiFlashインスタンスが表示されない問題を修正
    -   概要ページを更新した後にメトリック選択がリセットされる問題を修正します[#663](https://github.com/pingcap-incubator/tidb-dashboard/pull/663)
    -   一部の TLS シナリオでの接続の問題を修正する[#660](https://github.com/pingcap-incubator/tidb-dashboard/pull/660)
    -   言語ドロップダウンボックスが正しく表示されない場合がある問題を修正[#677](https://github.com/pingcap-incubator/tidb-dashboard/pull/677)

-   TiFlash

    -   主キー列の名前を変更するとTiFlash がクラッシュする問題を修正
    -   `Learner Read`と`Remove Region`の同時実行でデッドロックが発生する可能性がある問題を修正

-   ツール

    -   TiCDC

        -   場合によっては TiCDC でメモリリークが発生する問題を修正[#704](https://github.com/pingcap/tiflow/pull/704)
        -   引用符で囲まれていないテーブル名が原因で SQL 構文エラー[#676](https://github.com/pingcap/tiflow/pull/676)が発生する問題を修正します
        -   `p.stop`が[#693](https://github.com/pingcap/tiflow/pull/693)と呼ばれた後、プロセッサが完全に終了しないという問題を修正します。

    -   バックアップと復元 (BR)

        -   バックアップ時間がマイナスになる問題を修正[#405](https://github.com/pingcap/br/pull/405)

    -   Dumpling

        -   Dumpling で`--r`を指定すると`NULL`値が省略される問題を修正[#119](https://github.com/pingcap/dumpling/pull/119)
        -   ダンプするテーブルに対してテーブルのフラッシュが機能しない可能性があるバグを修正します[#117](https://github.com/pingcap/dumpling/pull/117)

    -   TiDB Lightning

        -   `--log-file`が効かない問題を修正[#345](https://github.com/pingcap/tidb-lightning/pull/345)

    -   TiDBBinlog

        -   TiDB Binlog がTLS を有効にしてダウンストリームにデータをレプリケートすると、チェックポイント[#988](https://github.com/pingcap/tidb-binlog/pull/988)の更新に使用されるデータベース ドライバーで TLS が有効になっていないために発生するDrainerを開始できない問題を修正します。
