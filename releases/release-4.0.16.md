---
title: TiDB 4.0.16 Release Notes
summary: TiDB 4.0.16 は 2021 年 12 月 17 日にリリースされました。このリリースには、TiKV とツールの互換性の変更、TiDB、TiKV、ツールの改善、TiDB、TiKV、PD、 TiFlash、TiDB Binlog、TiCDC のバグ修正が含まれています。バグ修正では、クエリ パニック、誤った結果、パニック、メモリリークなどのさまざまな問題に対処しています。このリリースには、TiCDC レプリケーションの中断、コンテナー環境での OOM、メモリリークの問題の修正も含まれています。
---

# TiDB 4.0.16 リリースノート {#tidb-4-0-16-release-notes}

発売日: 2021年12月17日

TiDB バージョン: 4.0.16

## 互換性の変更 {#compatibility-changes}

-   ティクヴ

    -   v4.0.16より前では、TiDBが不正なUTF-8文字列をReal型に変換すると、エラーが直接報告されていました。v4.0.16以降では、TiDBは文字列[＃11466](https://github.com/tikv/tikv/issues/11466)の有効なUTF-8プレフィックスに従って変換を処理します。

-   ツール

    -   ティCDC

        -   TiCDC が Kafka クラスター[＃2962](https://github.com/pingcap/tiflow/issues/2962)に大きすぎるメッセージを送信しないように、Kafka シンク`max-message-bytes`のデフォルト値を 1 MB に変更します。
        -   TiCDC がメッセージを Kafka パーティション間でより均等に分散するように、Kafka シンクのデフォルト値を`partition-num`から 3 に変更します[＃3337](https://github.com/pingcap/tiflow/issues/3337)

## 改善点 {#improvements}

-   ティビ

    -   Grafanaのバージョンを7.5.7から7.5.11にアップグレードします

-   ティクヴ

    -   バックアップと復元を使用してデータを復元する場合、またはTiDB Lightning [＃11469](https://github.com/tikv/tikv/issues/11469)のローカル バックエンドを使用してデータをインポートする場合に、zstd アルゴリズムを採用して SST ファイルを圧縮することで、ディスク領域の消費量を削減します。

-   ツール

    -   バックアップと復元 (BR)

        -   復元の堅牢性を向上させる[＃27421](https://github.com/pingcap/tidb/issues/27421)

    -   ティCDC

        -   頻繁な etcd 書き込みが PD サービスに影響を与えないように、EtcdWorker にティック頻度制限を追加します[＃3112](https://github.com/pingcap/tiflow/issues/3112)
        -   TiKV リロードのレート制限制御を最適化して、チェンジフィード初期化中の gPRC 輻輳を軽減します[＃3110](https://github.com/pingcap/tiflow/issues/3110)

## バグ修正 {#bug-fixes}

-   ティビ

    -   コスト見積もりの​​ために範囲をポイントに変換するときに統計モジュールのオーバーフローによって発生するクエリpanicを修正[＃23625](https://github.com/pingcap/tidb/issues/23625)
    -   `ENUM`型データを制御関数のパラメータとして使用する場合の、制御関数( `IF`や`CASE WHEN`など) の誤った結果を修正[＃23114](https://github.com/pingcap/tidb/issues/23114)
    -   `GREATEST`関数が`tidb_enable_vectorized_expression` ( `on`または`off` ) [＃29434](https://github.com/pingcap/tidb/issues/29434)の値が異なるために矛盾した結果を返す問題を修正しました。
    -   プレフィックスインデックスにインデックス結合を適用するときに発生するpanicを修正[＃24547](https://github.com/pingcap/tidb/issues/24547)
    -   プランナーが`join`の無効なプランをキャッシュする場合がある問題を修正[＃28087](https://github.com/pingcap/tidb/issues/28087)
    -   `sql_mode`が空の場合に TiDB が`null`非 NULL 列に挿入できないバグを修正[＃11648](https://github.com/pingcap/tidb/issues/11648)
    -   関数`GREATEST`と`LEAST`の間違った結果型を修正[＃29019](https://github.com/pingcap/tidb/issues/29019)
    -   グローバルレベルの権限を付与および取り消す`grant`および`revoke`操作を実行するときに発生する`privilege check fail`エラーを修正します[＃29675](https://github.com/pingcap/tidb/issues/29675)
    -   `ENUM`データ型[＃29357](https://github.com/pingcap/tidb/issues/29357)で`CASE WHEN`関数を使用するときに発生するpanicを修正
    -   ベクトル化された式[＃29244](https://github.com/pingcap/tidb/issues/29244)の関数`microsecond`の誤った結果を修正
    -   ベクトル化された式[＃28643](https://github.com/pingcap/tidb/issues/28643)の関数`hour`の誤った結果を修正
    -   楽観的トランザクションの競合によりトランザクションが互いにブロックされる可能性がある問題を修正[＃11148](https://github.com/tikv/tikv/issues/11148)
    -   `auto analyze`結果[＃29188](https://github.com/pingcap/tidb/issues/29188)からの不完全なログ情報の問題を修正
    -   `SQL_MODE`が &#39;NO_ZERO_IN_DATE&#39; の場合に無効なデフォルト日付を使用してもエラーが報告されない問題を修正しました[＃26766](https://github.com/pingcap/tidb/issues/26766)
    -   Grafanaのコプロセッサーキャッシュパネルにメトリックが表示されない問題を修正しました。現在、Grafanaは`hits` / `miss` / `evict` [＃26338](https://github.com/pingcap/tidb/issues/26338)の数を表示します。
    -   同じパーティションを同時に切り捨てると DDL ステートメントがスタックする問題を修正しました[＃26229](https://github.com/pingcap/tidb/issues/26229)
    -   `Decimal` `String`に変換するときに長さ情報が間違っている問題を修正しました[＃29417](https://github.com/pingcap/tidb/issues/29417)
    -   `NATURAL JOIN`複数のテーブルを結合するために使用した場合、クエリ結果に余分な列が含まれる問題を修正[＃29481](https://github.com/pingcap/tidb/issues/29481)
    -   `IndexScan`プレフィックス インデックス[＃29711](https://github.com/pingcap/tidb/issues/29711)使用する場合に`TopN`誤って`indexPlan`にプッシュダウンされる問題を修正しました。
    -   `DOUBLE`種類の自動インクリメント列を使用してトランザクションを再試行すると、データが破損する問題を修正しました[＃29892](https://github.com/pingcap/tidb/issues/29892)

-   ティクヴ

    -   極端な状況でリージョンのマージ、ConfChange、スナップショットが同時に発生した場合に発生するpanicの問題を修正[＃11475](https://github.com/tikv/tikv/issues/11475)
    -   小数点以下の除算結果がゼロの場合の負の符号の問題を修正[＃29586](https://github.com/pingcap/tidb/issues/29586)
    -   TiKV メトリック[＃11299](https://github.com/tikv/tikv/issues/11299)でインスタンスごとの gRPC リクエストの平均レイテンシーが不正確になる問題を修正
    -   ダウンストリームデータベースが見つからない場合に発生する TiCDCpanicの問題を修正[＃11123](https://github.com/tikv/tikv/issues/11123)
    -   チャネルがいっぱいになるとRaft接続が切断される問題を修正[＃11047](https://github.com/tikv/tikv/issues/11047)
    -   TiDBが`Max`関数の`Int64`型`Min`符号付き整数であるかどうかを正しく識別できず、 `Max` / `Min` [＃10158](https://github.com/tikv/tikv/issues/10158)の計算結果が間違ってしまう問題を修正しました。
    -   輻輳エラー[＃11082](https://github.com/tikv/tikv/issues/11082)によりCDCがスキャン再試行を頻繁に追加する問題を修正

-   PD

    -   TiKVノードが削除された後に発生するpanic問題を修正[＃4344](https://github.com/tikv/pd/issues/4344)
    -   スタックしたリージョン同期装置[＃3936](https://github.com/tikv/pd/issues/3936)によって発生するリーダー選出の遅延を修正
    -   エビクトリーダースケジューラが不健全なピアを持つ領域をスケジュールできるようにサポート[＃4093](https://github.com/tikv/pd/issues/4093)

-   TiFlash

    -   ライブラリ`nsl`がないため、一部のプラットフォームでTiFlash が起動しない問題を修正しました。

-   ツール

    -   TiDBBinlog

        -   1 GB を超えるトランザクションを転送するときにDrainer が終了するバグを修正[＃28659](https://github.com/pingcap/tidb/issues/28659)

    -   ティCDC

        -   チェンジフィードチェックポイントラグ[＃3010](https://github.com/pingcap/tiflow/issues/3010)の負の値エラーを修正
        -   コンテナ環境の OOM を修正[＃1798](https://github.com/pingcap/tiflow/issues/1798)
        -   複数の TiKV がクラッシュした場合や強制再起動中に TiCDC レプリケーションが中断される問題を修正[＃3288](https://github.com/pingcap/tiflow/issues/3288)
        -   DDL [＃3174](https://github.com/pingcap/tiflow/issues/3174)の処理後のメモリリークの問題を修正
        -   ErrGCTTLExceeded エラーが発生したときに changefeed が十分に速く失敗しない問題を修正[＃3111](https://github.com/pingcap/tiflow/issues/3111)
        -   上流の TiDB インスタンスが予期せず終了すると TiCDC レプリケーション タスクが終了する可能性がある問題を修正[＃3061](https://github.com/pingcap/tiflow/issues/3061)
        -   TiKV が同じリージョン[＃2386](https://github.com/pingcap/tiflow/issues/2386)に重複したリクエストを送信したときに TiCDC プロセスがpanicになる可能性がある問題を修正しました。
        -   TiCDCによって生成されるKafkaメッセージの量が`max-message-size` [＃2962](https://github.com/pingcap/tiflow/issues/2962)に制限されない問題を修正
        -   `tikv_cdc_min_resolved_ts_no_change_for_1m`チェンジフィードがない場合に警告が継続する問題を修正[＃11017](https://github.com/tikv/tikv/issues/11017)
        -   Kafka メッセージの書き込み中にエラーが発生すると TiCDC 同期タスクが一時停止する可能性がある問題を修正[＃2978](https://github.com/pingcap/tiflow/issues/2978)
        -   `force-replicate`が有効になっている場合に、有効なインデックスのない一部のパーティションテーブルが無視される可能性がある問題を修正[＃2834](https://github.com/pingcap/tiflow/issues/2834)
        -   新しい変更フィード[＃2389](https://github.com/pingcap/tiflow/issues/2389)作成するときに発生するメモリリークの問題を修正しました
        -   シンクコンポーネントの進行によりデータの不整合が発生する可能性がある問題を修正しました[＃3503](https://github.com/pingcap/tiflow/issues/3503)
        -   株価データのスキャンに時間がかかりすぎると、TiKV が GC を実行するため株価データのスキャンが失敗する可能性がある問題を修正[＃2470](https://github.com/pingcap/tiflow/issues/2470)
        -   changefeed update コマンドがグローバルコマンドラインパラメータを認識しない問題を修正[＃2803](https://github.com/pingcap/tiflow/issues/2803)
