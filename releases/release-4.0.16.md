---
title: TiDB 4.0.16 Release Notes
summary: TiDB 4.0.16は2021年12月17日にリリースされました。このリリースには、TiKVとツールの互換性変更、TiDB、TiKV、ツールの改善、TiDB、TiKV、PD、 TiFlash、TiDB Binlog、TiCDCのバグ修正が含まれています。これらのバグ修正により、クエリパニック、誤った結果、パニック、メモリリークなどのさまざまな問題が修正されています。また、TiCDCレプリケーションの中断、コンテナ環境におけるOOM、メモリリークの問題も修正されています。
---

# TiDB 4.0.16 リリースノート {#tidb-4-0-16-release-notes}

発売日：2021年12月17日

TiDBバージョン: 4.0.16

## 互換性の変更 {#compatibility-changes}

-   TiKV

    -   v4.0.16より前では、TiDBが無効なUTF-8文字列をReal型に変換すると、直接エラーが報告されていました。v4.0.16以降、TiDBは文字列内の有効なUTF-8プレフィックスに従って変換処理を行います。 [＃11466](https://github.com/tikv/tikv/issues/11466)

-   ツール

    -   TiCDC

        -   TiCDC が Kafka クラスターに大きすぎるメッセージを送信しないように、Kafka シンク`max-message-bytes`のデフォルト値を 1 MB に変更します。 [＃2962](https://github.com/pingcap/tiflow/issues/2962)
        -   TiCDC がメッセージを Kafka パーティション間でより均等に分散するように、Kafka シンク`partition-num`のデフォルト値を 3 に変更します[＃3337](https://github.com/pingcap/tiflow/issues/3337)

## 改善点 {#improvements}

-   TiDB

    -   Grafanaのバージョンを7.5.7から7.5.11にアップグレードします。

-   TiKV

    -   バックアップと復元を使用してデータを復元する場合、またはTiDB Lightning のローカル バックエンドを使用してデータをインポートする場合に、zstd アルゴリズムを採用して SST ファイルを圧縮することで、ディスク領域の消費量を削減します。 [＃11469](https://github.com/tikv/tikv/issues/11469)

-   ツール

    -   Backup & Restore (BR)

        -   復元の堅牢性を向上させる[＃27421](https://github.com/pingcap/tidb/issues/27421)

    -   TiCDC

        -   頻繁な etcd 書き込みが PD サービスに影響を与えないように、EtcdWorker にティック頻度制限を追加します[＃3112](https://github.com/pingcap/tiflow/issues/3112)
        -   TiKV リロードのレート制限制御を最適化して、チェンジフィード初期化中の gPRC 輻輳を軽減します[＃3110](https://github.com/pingcap/tiflow/issues/3110)

## バグ修正 {#bug-fixes}

-   TiDB

    -   コスト見積もりために範囲をポイントに変換するときに統計モジュールのオーバーフローによって発生するクエリpanicを修正しました [＃23625](https://github.com/pingcap/tidb/issues/23625)
    -   `ENUM`型データを制御関数のパラメータとして使用した場合に、制御関数の誤った結果（ `IF`や`CASE WHEN`など）が返される問題を修正しました[＃23114](https://github.com/pingcap/tidb/issues/23114)
    -   `GREATEST`関数が`tidb_enable_vectorized_expression` ( `on`または`off` ) の値が異なるために矛盾した結果を返す問題を修正しました。 [＃29434](https://github.com/pingcap/tidb/issues/29434)
    -   一部のケースでプレフィックスインデックスにインデックス結合を適用するとpanicする問題を修正[＃24547](https://github.com/pingcap/tidb/issues/24547)
    -   プランナーが場合によっては無効なプランをキャッシュする可能性がある問題を修正`join` [＃28087](https://github.com/pingcap/tidb/issues/28087)
    -   `sql_mode`が空の場合にTiDBが非NULL列に`null`挿入できないバグを修正[＃11648](https://github.com/pingcap/tidb/issues/11648)
    -   関数`GREATEST`と`LEAST`の間違った結果型を修正[＃29019](https://github.com/pingcap/tidb/issues/29019)
    -   グローバルレベルの権限を付与および取り消す操作`grant`および`revoke`を実行するときに発生する`privilege check fail`エラーを修正します[＃29675](https://github.com/pingcap/tidb/issues/29675)
    -   `ENUM`データ型で`CASE WHEN`関数を使用するときにpanicを修正 [＃29357](https://github.com/pingcap/tidb/issues/29357)
    -   ベクトル化された式の関数`microsecond`の誤った結果を修正 [＃29244](https://github.com/pingcap/tidb/issues/29244)
    -   ベクトル化された式の関数`hour`の誤った結果を修正します [＃28643](https://github.com/pingcap/tidb/issues/28643)
    -   楽観的トランザクションの競合によりトランザクションが互いにブロックされる可能性がある問題を修正[＃11148](https://github.com/tikv/tikv/issues/11148)
    -   `auto analyze`の結果のログ情報が不完全である問題を修正 [＃29188](https://github.com/pingcap/tidb/issues/29188)
    -   `SQL_MODE` &#39;NO_ZERO_IN_DATE&#39; の場合に無効なデフォルト日付を使用してもエラーが報告されない問題を修正しました[＃26766](https://github.com/pingcap/tidb/issues/26766)
    -   Grafanaのコプロセッサーキャッシュパネルにメトリクスが表示されない問題を修正しました。これで、Grafanaは`hits` / `miss` / `evict` の数値を表示します。 [＃26338](https://github.com/pingcap/tidb/issues/26338)
    -   同じパーティションを同時に切り捨てるとDDL文がスタックする問題を修正しました[＃26229](https://github.com/pingcap/tidb/issues/26229)
    -   `Decimal`を`String`に変換するときに長さ情報が間違っている問題を修正しました[＃29417](https://github.com/pingcap/tidb/issues/29417)
    -   `NATURAL JOIN`複数のテーブルを結合するために使用したときにクエリ結果に余分な列が残る問題を修正[＃29481](https://github.com/pingcap/tidb/issues/29481)
    -   `IndexScan`プレフィックス インデックスを使用している場合に、 `TopN`が誤って`indexPlan`にプッシュダウンされる問題を修正しました。 [＃29711](https://github.com/pingcap/tidb/issues/29711)
    -   `DOUBLE`型のAUTO_INCREMENT列でトランザクションを再試行するとデータ破損が発生する問題を修正[＃29892](https://github.com/pingcap/tidb/issues/29892)

-   TiKV

    -   極端な状況でリージョンのマージ、ConfChange、スナップショットが同時に発生した場合に発生するpanicの問題を修正しました[＃11475](https://github.com/tikv/tikv/issues/11475)
    -   小数点以下の除算結果がゼロの場合の負の符号の問題を修正しました[＃29586](https://github.com/pingcap/tidb/issues/29586)
    -   TiKV メトリクスでインスタンスごとの gRPC リクエストの平均レイテンシーが不正確になる問題を修正しました [＃11299](https://github.com/tikv/tikv/issues/11299)
    -   下流データベースが見つからない場合に発生する TiCDCpanicの問題を修正しました[＃11123](https://github.com/tikv/tikv/issues/11123)
    -   チャネルがいっぱいになるとRaft接続が切断される問題を修正[＃11047](https://github.com/tikv/tikv/issues/11047)
    -   TiDBが`Max` `Min`の`Int64`型が符号付き整数かどうかを正しく識別できず、 `Max` / `Min` の計算結果が間違ってしまう問題を修正しました。 [＃10158](https://github.com/tikv/tikv/issues/10158)
    -   輻輳エラーによりCDCがスキャン再試行を頻繁に追加する問題を修正 [＃11082](https://github.com/tikv/tikv/issues/11082)

-   PD

    -   TiKVノードが削除された後に発生するpanic問題を修正[＃4344](https://github.com/tikv/pd/issues/4344)
    -   スタックしたリージョン同期機能によって発生するリーダー選出の遅延を修正 [＃3936](https://github.com/tikv/pd/issues/3936)
    -   退去リーダースケジューラが不健全なピアを持つリージョンをスケジュールできるようにサポート[＃4093](https://github.com/tikv/pd/issues/4093)

-   TiFlash

    -   ライブラリ`nsl`がないため、一部のプラットフォームでTiFlashが起動に失敗する問題を修正しました。

-   ツール

    -   TiDB Binlog

        -   1 GBを超えるトランザクションを転送するときにDrainerが終了するバグを修正しました[＃28659](https://github.com/pingcap/tidb/issues/28659)

    -   TiCDC

        -   チェンジフィードチェックポイントラグの負の値エラーを修正 [＃3010](https://github.com/pingcap/tiflow/issues/3010)
        -   コンテナ環境のOOMを修正[＃1798](https://github.com/pingcap/tiflow/issues/1798)
        -   複数の TiKV がクラッシュした場合や強制再起動中に TiCDC レプリケーションが中断される問題を修正[＃3288](https://github.com/pingcap/tiflow/issues/3288)
        -   DDL 処理後のメモリリークの問題を修正 [＃3174](https://github.com/pingcap/tiflow/issues/3174)
        -   ErrGCTTLExceeded エラーが発生したときに changefeed が十分に速く失敗しない問題を修正しました[＃3111](https://github.com/pingcap/tiflow/issues/3111)
        -   上流の TiDB インスタンスが予期せず終了すると、TiCDC レプリケーション タスクが終了する可能性がある問題を修正しました[＃3061](https://github.com/pingcap/tiflow/issues/3061)
        -   TiKV が同じリージョンに重複したリクエストを送信したときに TiCDC プロセスがpanicになる可能性がある問題を修正しました。 [＃2386](https://github.com/pingcap/tiflow/issues/2386)
        -   TiCDCによって生成されるKafkaメッセージの量が`max-message-size` に制限されない問題を修正 [＃2962](https://github.com/pingcap/tiflow/issues/2962)
        -   `tikv_cdc_min_resolved_ts_no_change_for_1m`チェンジフィードがないときに警告が続く問題を修正[＃11017](https://github.com/tikv/tikv/issues/11017)
        -   Kafka メッセージの書き込み中にエラーが発生すると、TiCDC 同期タスクが一時停止する可能性がある問題を修正しました[＃2978](https://github.com/pingcap/tiflow/issues/2978)
        -   `force-replicate`有効になっているときに、有効なインデックスのない一部のパーティションテーブルが無視される可能性がある問題を修正[＃2834](https://github.com/pingcap/tiflow/issues/2834)
        -   新しい変更フィードを作成するときに発生するメモリリークの問題を修正しました [＃2389](https://github.com/pingcap/tiflow/issues/2389)
        -   シンクコンポーネントの前進によりデータの不整合が発生する可能性がある問題を修正しました[＃3503](https://github.com/pingcap/tiflow/issues/3503)
        -   株価データのスキャンに時間がかかりすぎると、TiKV が GC を実行するため株価データのスキャンが失敗する可能性がある問題を修正しました[＃2470](https://github.com/pingcap/tiflow/issues/2470)
        -   changefeed update コマンドがグローバルコマンドラインパラメータを認識しない問題を修正[＃2803](https://github.com/pingcap/tiflow/issues/2803)
