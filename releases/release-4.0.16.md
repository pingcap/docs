---
title: TiDB 4.0.16 Release Notes
summary: TiDB 4.0.16は2021年12月17日にリリースされました。このリリースには、TiKVとツールの互換性変更、TiDB、TiKV、ツールの改善、TiDB、TiKV、PD、 TiFlash、TiDB Binlog、TiCDCのバグ修正が含まれています。これらのバグ修正により、クエリパニック、誤った結果、パニック、メモリリークなどのさまざまな問題が修正されています。また、TiCDCレプリケーションの中断、コンテナ環境におけるOOM、メモリリークの問題も修正されています。
---

# TiDB 4.0.16 リリースノート {#tidb-4-0-16-release-notes}

発売日：2021年12月17日

TiDB バージョン: 4.0.16

## 互換性の変更 {#compatibility-changes}

-   TiKV

    -   v4.0.16より前では、TiDBが不正なUTF-8文字列をReal型に変換すると、直接エラーが報告されていました。v4.0.16以降、TiDBは文字列[＃11466](https://github.com/tikv/tikv/issues/11466)内の有効なUTF-8プレフィックスに従って変換処理を行います。

-   ツール

    -   TiCDC

        -   TiCDC が Kafka クラスター[＃2962](https://github.com/pingcap/tiflow/issues/2962)に大きすぎるメッセージを送信しないように、Kafka シンク`max-message-bytes`のデフォルト値を 1 MB に変更します。
        -   TiCDC がメッセージを Kafka パーティション間でより均等に分散するように、Kafka シンク`partition-num`のデフォルト値を 3 に変更します[＃3337](https://github.com/pingcap/tiflow/issues/3337)

## 改善点 {#improvements}

-   TiDB

    -   Grafanaのバージョンを7.5.7から7.5.11にアップグレードします

-   TiKV

    -   バックアップと復元を使用してデータを復元する場合、またはTiDB Lightning [＃11469](https://github.com/tikv/tikv/issues/11469)のローカル バックエンドを使用してデータをインポートする場合に、zstd アルゴリズムを採用して SST ファイルを圧縮することにより、ディスク領域の消費量を削減します。

-   ツール

    -   バックアップと復元 (BR)

        -   復元の堅牢性を向上させる[＃27421](https://github.com/pingcap/tidb/issues/27421)

    -   TiCDC

        -   頻繁な etcd 書き込みが PD サービスに影響を与えないように、EtcdWorker にティック頻度制限を追加します[＃3112](https://github.com/pingcap/tiflow/issues/3112)
        -   TiKVリロードのレート制限制御を最適化して、チェンジフィード初期化中のgPRC輻輳を軽減します[＃3110](https://github.com/pingcap/tiflow/issues/3110)

## バグ修正 {#bug-fixes}

-   TiDB

    -   コスト見積もりの範囲をポイントに変換するときに統計モジュールのオーバーフローによって発生するクエリpanicを修正[＃23625](https://github.com/pingcap/tidb/issues/23625)
    -   `ENUM`型データを制御関数のパラメータとして使用した場合に、制御関数の誤った結果（ `IF`や`CASE WHEN`など）が修正されました[＃23114](https://github.com/pingcap/tidb/issues/23114)
    -   `GREATEST`関数が`tidb_enable_vectorized_expression` ( `on`または`off` ) [＃29434](https://github.com/pingcap/tidb/issues/29434)の値が異なるために矛盾した結果を返す問題を修正しました。
    -   一部のケースでプレフィックスインデックスにインデックス結合を適用するとpanicする問題を修正[＃24547](https://github.com/pingcap/tidb/issues/24547)
    -   プランナーが`join`の無効なプランをキャッシュする可能性がある問題を修正しました[＃28087](https://github.com/pingcap/tidb/issues/28087)
    -   `sql_mode`が空の場合にTiDBが非NULL列に`null`挿入できないバグを修正[＃11648](https://github.com/pingcap/tidb/issues/11648)
    -   関数`GREATEST`と`LEAST`間違った結果型を修正[＃29019](https://github.com/pingcap/tidb/issues/29019)
    -   グローバルレベルの権限を付与および取り消すための`grant`および`revoke`操作を実行するときに発生する`privilege check fail`エラーを修正します[＃29675](https://github.com/pingcap/tidb/issues/29675)
    -   `ENUM`データ型[＃29357](https://github.com/pingcap/tidb/issues/29357)で`CASE WHEN`関数を使用するときに発生するpanicを修正
    -   ベクトル化された式[＃29244](https://github.com/pingcap/tidb/issues/29244)の関数`microsecond`の誤った結果を修正
    -   ベクトル化された式[＃28643](https://github.com/pingcap/tidb/issues/28643)の関数`hour`の誤った結果を修正します
    -   楽観的トランザクションの競合によりトランザクションが互いにブロックされる可能性がある問題を修正[＃11148](https://github.com/tikv/tikv/issues/11148)
    -   `auto analyze`の結果[＃29188](https://github.com/pingcap/tidb/issues/29188)のログ情報が不完全である問題を修正
    -   `SQL_MODE` 「NO_ZERO_IN_DATE」の場合に無効なデフォルト日付を使用してもエラーが報告されない問題を修正しました[＃26766](https://github.com/pingcap/tidb/issues/26766)
    -   Grafanaのコプロセッサーキャッシュパネルにメトリクスが表示されない問題を修正しました。これで、Grafanaは`hits` / `miss` / `evict` [＃26338](https://github.com/pingcap/tidb/issues/26338)の数値を表示します。
    -   同じパーティションを同時に切り捨てるとDDL文がスタックする問題を修正しました[＃26229](https://github.com/pingcap/tidb/issues/26229)
    -   `Decimal` `String`に変換するときに長さ情報が間違っている問題を修正しました[＃29417](https://github.com/pingcap/tidb/issues/29417)
    -   `NATURAL JOIN`複数のテーブルを結合するために使用した場合のクエリ結果に余分な列が含まれる問題を修正[＃29481](https://github.com/pingcap/tidb/issues/29481)
    -   `IndexScan`プレフィックス インデックス[＃29711](https://github.com/pingcap/tidb/issues/29711)使用する場合に、 `TopN`が誤って`indexPlan`にプッシュダウンされる問題を修正しました。
    -   `DOUBLE`種類の自動インクリメント列を使用してトランザクションを再試行すると、データ破損が発生する問題を修正しました[＃29892](https://github.com/pingcap/tidb/issues/29892)

-   TiKV

    -   極端な状況でリージョンのマージ、ConfChange、スナップショットが同時に発生した場合に発生するpanicの問題を修正しました[＃11475](https://github.com/tikv/tikv/issues/11475)
    -   小数点以下の除算結果がゼロの場合の負の符号の問題を修正しました[＃29586](https://github.com/pingcap/tidb/issues/29586)
    -   TiKV メトリクス[＃11299](https://github.com/tikv/tikv/issues/11299)でインスタンスごとの gRPC リクエストの平均レイテンシーが不正確になる問題を修正しました
    -   下流データベースが見つからない場合に発生する TiCDCpanicの問題を修正しました[＃11123](https://github.com/tikv/tikv/issues/11123)
    -   チャネルがいっぱいになるとRaft接続が切断される問題を修正[＃11047](https://github.com/tikv/tikv/issues/11047)
    -   TiDBが`Max` `Min`の`Int64`型が符号付き整数であるかどうかを正しく識別できず、 `Max` / `Min` [＃10158](https://github.com/tikv/tikv/issues/10158)の計算結果が間違ってしまう問題を修正しました。
    -   輻輳エラー[＃11082](https://github.com/tikv/tikv/issues/11082)によりCDCがスキャン再試行を頻繁に追加する問題を修正

-   PD

    -   TiKVノードが削除された後に発生するpanic問題を修正[＃4344](https://github.com/tikv/pd/issues/4344)
    -   リージョン同期が停止したことによるリーダー選出の遅延を修正[＃3936](https://github.com/tikv/pd/issues/3936)
    -   退去リーダースケジューラが不健全なピアを持つ領域をスケジュールできるようにサポート[＃4093](https://github.com/tikv/pd/issues/4093)

-   TiFlash

    -   ライブラリ`nsl`がないため、一部のプラットフォームでTiFlashが起動に失敗する問題を修正しました。

-   ツール

    -   TiDBBinlog

        -   1 GBを超えるトランザクションを転送するときにDrainerが終了するバグを修正しました[＃28659](https://github.com/pingcap/tidb/issues/28659)

    -   TiCDC

        -   チェンジフィードチェックポイントラグ[＃3010](https://github.com/pingcap/tiflow/issues/3010)の負の値エラーを修正
        -   コンテナ環境のOOMを修正[＃1798](https://github.com/pingcap/tiflow/issues/1798)
        -   複数の TiKV がクラッシュした場合や強制再起動中に TiCDC レプリケーションが中断される問題を修正[＃3288](https://github.com/pingcap/tiflow/issues/3288)
        -   DDL [＃3174](https://github.com/pingcap/tiflow/issues/3174)処理後のメモリリークの問題を修正
        -   ErrGCTTLExceeded エラーが発生したときに changefeed が十分に速く失敗しない問題を修正しました[＃3111](https://github.com/pingcap/tiflow/issues/3111)
        -   上流の TiDB インスタンスが予期せず終了すると、TiCDC レプリケーション タスクが終了する可能性がある問題を修正しました[＃3061](https://github.com/pingcap/tiflow/issues/3061)
        -   TiKVが同じリージョン[＃2386](https://github.com/pingcap/tiflow/issues/2386)に重複したリクエストを送信した場合にTiCDCプロセスがpanic可能性がある問題を修正しました
        -   TiCDCによって生成されるKafkaメッセージの量が`max-message-size` [＃2962](https://github.com/pingcap/tiflow/issues/2962)に制限されない問題を修正
        -   `tikv_cdc_min_resolved_ts_no_change_for_1m`チェンジフィードがないときに警告が続く問題を修正[＃11017](https://github.com/tikv/tikv/issues/11017)
        -   Kafka メッセージの書き込み中にエラーが発生すると TiCDC 同期タスクが一時停止する可能性がある問題を修正[＃2978](https://github.com/pingcap/tiflow/issues/2978)
        -   `force-replicate`有効になっているときに、有効なインデックスのない一部のパーティションテーブルが無視される可能性がある問題を修正[＃2834](https://github.com/pingcap/tiflow/issues/2834)
        -   新しい変更フィード[＃2389](https://github.com/pingcap/tiflow/issues/2389)を作成するときに発生するメモリリークの問題を修正しました
        -   シンクコンポーネントの前進によりデータの不整合が発生する可能性がある問題を修正しました[＃3503](https://github.com/pingcap/tiflow/issues/3503)
        -   株価データのスキャンに時間がかかりすぎると、TiKV が GC を実行するため株価データのスキャンが失敗する可能性がある問題を修正しました[＃2470](https://github.com/pingcap/tiflow/issues/2470)
        -   changefeed 更新コマンドがグローバルコマンドラインパラメータを認識しない問題を修正[＃2803](https://github.com/pingcap/tiflow/issues/2803)
